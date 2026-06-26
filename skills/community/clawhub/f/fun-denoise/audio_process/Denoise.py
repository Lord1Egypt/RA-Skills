# -*- coding: utf-8 -*-
# Copyright (c) Alibaba, Inc. and its affiliates.

import json
import platform
import threading
import time
import uuid
from dataclasses import dataclass, field
from typing import Dict, Optional, Any

import websocket

import dashscope
from dashscope.common.error import InputRequired, InvalidTask, ModelRequired
from dashscope.common.logging import logger
from dashscope.protocol.websocket import (
    ACTION_KEY,
    EVENT_KEY,
    HEADER,
    TASK_ID,
    ActionType,
    EventType,
)


class ResultCallback:
    """
    An interface that defines callback methods for getting audio denoise results.
    Derive from this class and implement its function to provide your own data.
    """

    def on_open(self) -> None:
        pass

    def on_complete(self) -> None:
        pass

    def on_error(self, message) -> None:
        pass

    def on_close(self) -> None:
        pass

    def on_event(self, result: 'DenoiseResult') -> None:
        pass


@dataclass
class DenoiseResult:
    """
    Result of audio denoise processing.

    Attributes:
        audio_frame: Processed audio data (bytes)
        output: Output information including sample_rate_out, voice_quality, valid_speech_ms
        usage: Usage statistics including duration
        request_id: Request ID
    """

    audio_frame: Optional[bytes] = None
    output: Optional[Dict[str, Any]] = None
    usage: Optional[Dict[str, Any]] = None
    request_id: Optional[str] = None


@dataclass
class DenoiseParam:
    """
    Parameters for audio denoise processing.

    Attributes:
        model: Model name (default: "fun-audio-denoising")
        apikey: API key for authentication
        format: Audio format (pcm, wav, mp3, aac, opus, amr)
        sample_rate_in: Input audio sample rate (required for PCM format, default 16000)
        sample_rate_out: Output audio sample rate (must be > 0)
        enable_denoise: Whether to enable denoise processing (default True)
        url: Audio file URL (for URL-based upload)
        workspace: Dashscope workspace ID
        headers: User-defined headers
    """

    model: str = "fun-audio-denoising"
    apikey: Optional[str] = None
    format: str = "wav"
    sample_rate_in: int = 16000
    sample_rate_out: Optional[int] = None
    enable_denoise: bool = True
    url: Optional[str] = None
    workspace: Optional[str] = None
    headers: Optional[Dict[str, str]] = None
    parameters: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        result = {
            "model": self.model,
            "format": self.format,
            "sample_rate_in": self.sample_rate_in,
            "enable_denoise": self.enable_denoise,
        }
        if self.sample_rate_out is not None:
            result["sample_rate_out"] = self.sample_rate_out
        if self.url is not None:
            result["url"] = self.url
        return result


class Denoise:
    def __init__(
        self,
        param: Optional[DenoiseParam] = None,
        callback: Optional[ResultCallback] = None,
        url: Optional[str] = None,
        headers: Optional[Dict[str, str]] = None,
        workspace: Optional[str] = None,
    ):
        """
        Audio Denoise SDK for real-time audio processing.

        Parameters:
        -----------
        param: DenoiseParam
            Configuration for audio denoise processing.
        callback: ResultCallback
            Callback to receive real-time processing results.
        url: str
            Dashscope WebSocket URL.
        headers: Dict
            User-defined headers.
        workspace: str
            Dashscope workspace ID.
        """
        self.ws = None
        self.start_event = threading.Event()
        self.complete_event = threading.Event()
        self._stopped = threading.Event()
        self._audio_data: bytes = b""
        self._is_started = False
        self._cancel = False
        self._cancel_lock = threading.Lock()
        self.async_call = True
        self._is_first = True
        self._start_stream_timestamp = -1
        self._first_package_timestamp = -1
        self._recv_audio_length = 0
        self.last_response = None
        self._close_ws_after_use = True

        # Initialize parameters
        self._update_params(param, callback, url, headers, workspace)

    def _update_params(
        self,
        param: Optional[DenoiseParam],
        callback: Optional[ResultCallback],
        url: Optional[str],
        headers: Optional[Dict[str, str]],
        workspace: Optional[str],
    ):
        if url is None:
            url = dashscope.base_websocket_api_url
        self.url = url

        # Use provided param or create default
        if param is None:
            param = DenoiseParam()

        # Set API key
        if param.apikey is None:
            self.apikey = dashscope.api_key
        else:
            self.apikey = param.apikey

        if self.apikey is None:
            raise InputRequired("apikey is required!")

        self.param = param
        self.headers = headers
        self.workspace = workspace
        self.callback = callback

        if not self.callback:
            self.async_call = False

        # Generate task ID
        self.task_id = uuid.uuid4().hex
        self.last_request_id = self.task_id

    def _get_websocket_headers(self) -> Dict[str, str]:
        ua = (
            f"dashscope/1.18.0; python/{platform.python_version()}; "
            f"platform/{platform.platform()}; "
            f"processor/{platform.processor()}"
        )
        headers = {
            "user-agent": ua,
            "Authorization": "Bearer " + self.apikey,
        }
        if self.headers:
            headers = {**headers, **self.headers}
        if self.workspace:
            headers = {**headers, "X-DashScope-WorkSpace": self.workspace}
        return headers

    def _send_str(self, data: str):
        logger.debug(">>>send %s", data)
        self.ws.send(data)

    def _connect(self, timeout_seconds=5) -> None:
        """
        Establish a connection to the Dashscope WebSocket server.
        """
        self.ws = websocket.WebSocketApp(
            self.url,
            header=self._get_websocket_headers(),
            on_message=self.on_message,
            on_error=self.on_error,
            on_close=self.on_close,
            on_open=self.on_open,
        )
        self.thread = threading.Thread(target=self.ws.run_forever)
        self.thread.daemon = True
        self.thread.start()
        # Wait for connection to establish
        start_time = time.time()
        while (
            not (self.ws.sock and self.ws.sock.connected)
            and (time.time() - start_time) < timeout_seconds
        ):
            time.sleep(0.1)
        if not (self.ws.sock and self.ws.sock.connected):
            raise TimeoutError(
                "websocket connection could not established within 5s. "
                "Please check your network connection, firewall settings, or server status."
            )

    def _is_connected(self) -> bool:
        """
        Returns True if the connection is established and still exists;
        otherwise, returns False.
        """
        if not self.ws:
            return False
        if not (self.ws.sock and self.ws.sock.connected):
            return False
        return True

    def _reset(self):
        self.start_event.clear()
        self.complete_event.clear()
        self._stopped.clear()
        self._audio_data: bytes = b""
        self._is_started = False
        self._cancel = False
        self.async_call = True
        self._is_first = True
        self._start_stream_timestamp = -1
        self._first_package_timestamp = -1
        self._recv_audio_length = 0
        self.last_response = None

    def _get_start_request(self) -> str:
        """Generate run-task request."""
        cmd = {
            HEADER: {
                ACTION_KEY: ActionType.START,
                TASK_ID: self.task_id,
                "streaming": "duplex",
            },
            "payload": {
                "task_group": "audio",
                "task": "audio-process",
                "function": "process",
                "model": self.param.model,
                "parameters": self.param.to_dict(),
                "input": {},
            },
        }
        return json.dumps(cmd)

    def _get_finish_request(self) -> str:
        """Generate finish-task request."""
        cmd = {
            HEADER: {
                ACTION_KEY: ActionType.FINISHED,
                TASK_ID: self.task_id,
                "streaming": "duplex",
            },
            "payload": {
                "input": {},
            },
        }
        return json.dumps(cmd)

    def connect(self, timeout_seconds=5) -> None:
        """
        Establish a connection to the Dashscope WebSocket server.

        Parameters:
        -----------
        timeout_seconds: int
            Timeout in seconds for connection establishment.
        """
        self._connect(timeout_seconds)

    def _start_stream(self):
        """Start the denoise processing stream."""
        self._start_stream_timestamp = time.time() * 1000
        self._first_package_timestamp = -1
        self._recv_audio_length = 0

        if self._is_started:
            raise InvalidTask("task has already started.")

        # Establish WebSocket connection
        if self.ws is None:
            self._connect(5)

        # Send run-task command
        request = self._get_start_request()
        logger.debug(">>>send run-task: %s", request)
        self._send_str(request)

        if not self.start_event.wait(10):
            raise TimeoutError("start audio denoise failed within 10s.")

        self._is_started = True

    def start_task(self) -> None:
        """
        Start the audio denoise task.
        """
        if self._is_started:
            raise InvalidTask("audio denoise has already started.")
        self._start_stream()

    def send_audio_frame(self, audio_data: bytes) -> None:
        """
        Send audio frame data for processing.

        Parameters:
        -----------
        audio_data: bytes
            Audio data in bytes format.
        """
        if not self._is_started:
            raise InvalidTask("audio denoise has not been started.")

        if self._stopped.is_set():
            raise InvalidTask("audio denoise task has stopped.")

        logger.debug(">>>send binary %s", len(audio_data))
        self.ws.send(audio_data, websocket.ABNF.OPCODE_BINARY)

    def stop_task(self) -> None:
        """
        Stop the audio denoise task.
        """
        if not self._is_started:
            raise InvalidTask("audio denoise has not been started.")
        if self._stopped.is_set():
            return

        request = self._get_finish_request()
        self._send_str(request)

    def sync_stop_task(self, complete_timeout_millis=600000):
        """
        Synchronously stop the audio denoise task.
        Wait for all remaining processing to complete before returning.

        Parameters:
        -----------
        complete_timeout_millis: int
            Timeout in milliseconds. If None or <= 0, wait indefinitely.
        """
        if not self._is_started:
            raise InvalidTask("audio denoise has not been started.")
        if self._stopped.is_set():
            raise InvalidTask("audio denoise task has stopped.")

        self.stop_task()

        if complete_timeout_millis is not None and complete_timeout_millis > 0:
            if not self.complete_event.wait(timeout=complete_timeout_millis / 1000):
                raise TimeoutError(
                    f"audio denoise wait for complete timeout "
                    f"{complete_timeout_millis}ms"
                )
        else:
            self.complete_event.wait()

        if self._close_ws_after_use:
            self.close()

        self._stopped.set()
        self._is_started = False

    def cancel(self):
        """
        Immediately terminate the audio denoise task.
        """
        if not self._is_started:
            raise InvalidTask("audio denoise has not been started.")
        if self._stopped.is_set():
            return

        self.stop_task()
        self.ws.close()
        self.start_event.set()
        self.complete_event.set()

    def on_open(self, ws):
        """WebSocket connection opened callback."""
        logger.info("WebSocket connection opened")
        if self.callback:
            self.callback.on_open()

    def on_message(self, ws, message):
        """WebSocket message received callback."""
        if isinstance(message, str):
            logger.debug("<<<recv %s", message)
            try:
                json_data = json.loads(message)
                self.last_response = json_data

                if "header" in json_data:
                    header = json_data["header"]
                    if EVENT_KEY in header:
                        event = header[EVENT_KEY]

                        if event == "task-started":
                            self.start_event.set()
                            self._first_package_timestamp = -1

                        elif event == "task-finished":
                            self.complete_event.set()
                            if self.callback:
                                self.callback.on_complete()
                                self.callback.on_close()

                        elif event == "task-failed":
                            self.start_event.set()
                            self.complete_event.set()
                            error_message = "Unknown error"
                            if "error_message" in header:
                                error_message = header["error_message"]

                            if self.async_call:
                                self.callback.on_error(error_message)
                                self.callback.on_close()
                            else:
                                logger.error(f"TaskFailed: {message}")
                                raise Exception(f"TaskFailed: {error_message}")

                        elif event == "result-generated":
                            if self.callback:
                                result = DenoiseResult()
                                if TASK_ID in header:
                                    result.request_id = header[TASK_ID]
                                if "payload" in json_data:
                                    payload = json_data["payload"]
                                    if "output" in payload:
                                        result.output = payload["output"]
                                    if "usage" in payload:
                                        result.usage = payload["usage"]
                                self.callback.on_event(result)

            except json.JSONDecodeError:
                logger.error("Failed to parse message as JSON.")
                raise Exception("Failed to parse message as JSON.")

        elif isinstance(message, (bytes, bytearray)):
            # Binary audio data
            logger.debug("<<<recv binary %s", len(message))

            if self._recv_audio_length == 0:
                self._first_package_timestamp = time.time() * 1000
                logger.debug(
                    "first package delay %s",
                    self._first_package_timestamp - self._start_stream_timestamp,
                )

            self._recv_audio_length += len(message)

            # Only save audio data in non-async mode
            if not self.async_call:
                self._audio_data += message

            if self.callback:
                result = DenoiseResult()
                result.audio_frame = bytes(message)
                self.callback.on_event(result)

    def on_error(self, ws, error):
        """WebSocket error callback."""
        logger.error(f"websocket error: {error}")
        if self.callback:
            self.callback.on_error(str(error))

        # Release waiting events
        if self.start_event.is_set() and not self.complete_event.is_set():
            self.complete_event.set()

    def on_close(self, ws, close_status_code, close_msg):
        """WebSocket connection closed callback."""
        logger.debug(f"websocket closed: {close_status_code} - {close_msg}")

    def close(self):
        """Close WebSocket connection."""
        if self.ws:
            self.ws.close()

    def get_last_request_id(self) -> str:
        """Get the last request ID."""
        return self.last_request_id

    def update_param_and_callback(
        self, param: DenoiseParam, callback: ResultCallback
    ):
        """
        Update parameters and callback for reuse.

        Parameters:
        -----------
        param: DenoiseParam
            New parameters for audio denoise.
        callback: ResultCallback
            New callback for receiving results.
        """
        self._reset()
        self.param = param
        self.callback = callback
        self.async_call = self.callback is not None
        self.task_id = uuid.uuid4().hex
        self.last_request_id = self.task_id
