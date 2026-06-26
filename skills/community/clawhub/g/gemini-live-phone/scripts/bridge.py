#!/usr/bin/env python3
"""
Gemini Live Phone Bridge
========================
FastAPI server bridging Twilio Media Streams ↔ Google Gemini Live API.
No STT/TTS middleware — Gemini handles audio natively (in and out).

Architecture:
  Phone ↔ Twilio ↔ WebSocket (μ-law 8kHz) ↔ Bridge (PCM transcoding) ↔ Gemini Live API

Usage:
  python bridge.py [OPTIONS]

  uvicorn bridge:app --host 0.0.0.0 --port 3335
"""

import argparse
import asyncio
import audioop  # audioop-lts for Python 3.13+
import base64
import datetime
import json
import logging
import os
import platform
import struct
import time
from contextlib import asynccontextmanager
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Request, APIRouter
from fastapi.responses import Response
from google import genai
from google.genai import types as genai_types
from twilio.rest import Client as TwilioClient

# ---------------------------------------------------------------------------
# OpenClaw-compatible structured file logger
# ---------------------------------------------------------------------------

OPENCLAW_LOG_DIR = Path(os.getenv("OPENCLAW_LOG_DIR", "/tmp/openclaw"))
SUBSYSTEM = "gemini-live-bridge"


class OpenClawFileHandler(logging.Handler):
    """Writes JSON log lines to /tmp/openclaw/openclaw-YYYY-MM-DD.log
    matching OpenClaw's native log format so `openclaw logs` picks them up."""

    def __init__(self):
        super().__init__()
        self._current_date: str = ""
        self._file = None
        OPENCLAW_LOG_DIR.mkdir(parents=True, exist_ok=True)

    def _rotate_if_needed(self, now_date: str):
        if now_date != self._current_date:
            if self._file:
                self._file.close()
            path = OPENCLAW_LOG_DIR / f"openclaw-{now_date}.log"
            self._file = open(path, "a", encoding="utf-8")
            self._current_date = now_date

    def emit(self, record: logging.LogRecord):
        try:
            now = datetime.datetime.now(datetime.timezone.utc)
            now_date = now.strftime("%Y-%m-%d")
            self._rotate_if_needed(now_date)
            ts = now.isoformat(timespec="milliseconds").replace("+00:00", "+00:00")

            level_map = {
                logging.DEBUG: ("DEBUG", 1),
                logging.INFO: ("INFO", 3),
                logging.WARNING: ("WARN", 4),
                logging.ERROR: ("ERROR", 5),
                logging.CRITICAL: ("FATAL", 6),
            }
            level_name, level_id = level_map.get(record.levelno, ("INFO", 3))

            entry = {
                "0": json.dumps({"subsystem": SUBSYSTEM}),
                "1": record.getMessage(),
                "_meta": {
                    "runtime": "python",
                    "runtimeVersion": platform.python_version(),
                    "hostname": platform.node(),
                    "name": json.dumps({"subsystem": SUBSYSTEM}),
                    "parentNames": ["openclaw"],
                    "date": ts,
                    "logLevelId": level_id,
                    "logLevelName": level_name,
                    "path": {
                        "filePath": record.pathname,
                        "fileNameWithLine": f"{record.filename}:{record.lineno}",
                        "method": record.funcName or "",
                    },
                },
                "time": ts,
            }

            self._file.write(json.dumps(entry) + "\n")
            self._file.flush()
        except Exception:
            self.handleError(record)


# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

@dataclass
class BridgeConfig:
    # Twilio
    twilio_account_sid: str = os.getenv("TWILIO_ACCOUNT_SID", "ACbdb5def0f217c61d3eea837e4807c0ce")
    twilio_auth_token: str = os.getenv("TWILIO_AUTH_TOKEN", "")
    twilio_from: str = os.getenv("TWILIO_FROM", "+17866558779")
    
    # Gemini
    gemini_api_key: str = os.getenv("GEMINI_API_KEY", os.getenv("GOOGLE_API_KEY", ""))
    gemini_model: str = "gemini-2.5-flash-native-audio-latest"
    gemini_voice: str = "Kore"
    
    # Server
    host: str = "0.0.0.0"
    port: int = 3335
    public_url: str = os.getenv("PUBLIC_URL", "https://athena.abfs.tech/gemini-live")
    route_prefix: str = "/gemini-live"
    
    # System prompt
    system_prompt: str = (
        "You are Marcia, a professional and friendly telephone operator. "
        "Always start with a short warm greeting (1-2 sentences) before the conversation. "
        "Keep your responses short and conversational — this is a phone call, not an essay. "
        "Match the caller's language (Portuguese or English). "
        "Be helpful, warm, and natural."
    )
    
    # Call settings
    max_duration: int = 300
    log_level: str = "info"
    
    # VAD settings
    vad_enabled: bool = True
    vad_silence_ms: int = 500
    vad_energy_threshold: float = 0.01
    vad_speech_min_ms: int = 100
    vad_prefix_ms: int = 200
    
    # Echo suppression
    echo_multiplier: float = 3.0
    echo_decay_ms: int = 300
    
    # Recording
    default_record: bool = False


# ---------------------------------------------------------------------------
# Globals
# ---------------------------------------------------------------------------

config = BridgeConfig()
twilio_client: Optional[TwilioClient] = None
active_calls: dict = {}
logger = logging.getLogger("gemini-live-bridge")

router = APIRouter(prefix="/gemini-live")


def log_call_event(call_sid: str, event: str, **kwargs):
    """Log a structured call event to both Python logger and OpenClaw logs."""
    details = {"call_sid": call_sid, "event": event, **kwargs}
    logger.info(f"[{call_sid}] {event}: {json.dumps({k: v for k, v in kwargs.items()})}")

# ---------------------------------------------------------------------------
# Audio helpers
# ---------------------------------------------------------------------------

MULAW_RATE = 8000
MULAW_SAMPLE_WIDTH = 1  # 8-bit μ-law
PCM_RATE = 24000  # Gemini expects 24kHz
PCM_SAMPLE_WIDTH = 2  # 16-bit PCM


def mulaw_to_pcm16_24k(mulaw_bytes: bytes) -> bytes:
    """Convert 8kHz μ-law to 24kHz 16-bit PCM for Gemini."""
    # μ-law → 16-bit PCM at 8kHz
    pcm_8k = audioop.ulaw2lin(mulaw_bytes, PCM_SAMPLE_WIDTH)
    # Resample 8kHz → 24kHz (3x)
    pcm_24k, _ = audioop.ratecv(pcm_8k, PCM_SAMPLE_WIDTH, 1, MULAW_RATE, PCM_RATE, None)
    return pcm_24k


def pcm16_24k_to_mulaw(pcm_bytes: bytes) -> bytes:
    """Convert 24kHz 16-bit PCM from Gemini to 8kHz μ-law for Twilio."""
    # Resample 24kHz → 8kHz
    pcm_8k, _ = audioop.ratecv(pcm_bytes, PCM_SAMPLE_WIDTH, 1, PCM_RATE, MULAW_RATE, None)
    # 16-bit PCM → μ-law
    mulaw = audioop.lin2ulaw(pcm_8k, PCM_SAMPLE_WIDTH)
    return mulaw


def compute_rms(pcm_bytes: bytes) -> float:
    """Compute RMS energy of 16-bit PCM audio."""
    if len(pcm_bytes) < 2:
        return 0.0
    rms = audioop.rms(pcm_bytes, PCM_SAMPLE_WIDTH)
    return rms / 32768.0  # Normalize to 0.0-1.0


# ---------------------------------------------------------------------------
# VAD State
# ---------------------------------------------------------------------------

@dataclass
class VADState:
    is_speaking: bool = False
    silence_start: Optional[float] = None
    speech_start: Optional[float] = None
    agent_speaking: bool = False
    agent_speech_end: Optional[float] = None
    greeting_done: bool = False  # Gate: suppress VAD until first Gemini turn completes
    
    def get_threshold(self, base_threshold: float) -> float:
        """Dynamic threshold — elevated during/after agent speech to suppress echo."""
        if self.agent_speaking:
            return base_threshold * config.echo_multiplier
        if self.agent_speech_end:
            elapsed = (time.monotonic() - self.agent_speech_end) * 1000
            if elapsed < config.echo_decay_ms:
                # Linear decay from multiplier back to 1.0
                factor = 1.0 + (config.echo_multiplier - 1.0) * (1.0 - elapsed / config.echo_decay_ms)
                return base_threshold * factor
        return base_threshold


# ---------------------------------------------------------------------------
# Gemini session handler
# ---------------------------------------------------------------------------

async def run_call(ws: WebSocket, start_data: dict, system_prompt: str,
                   voice: str, model: str, call_sid: str):
    """Main call loop: bridge Twilio WebSocket ↔ Gemini Live session."""
    stream_sid = start_data.get("streamSid", "")
    call_start = time.monotonic()
    vad = VADState()
    
    active_calls[call_sid] = {
        "start": call_start,
        "stream_sid": stream_sid,
        "status": "connected",
        "vad_events": 0,
    }
    
    logger.info(f"[{call_sid}] Starting Gemini session: model={model}, voice={voice}")
    
    # Initialize Gemini client
    client = genai.Client(api_key=config.gemini_api_key)
    
    realtime_input_cfg = None
    if config.vad_enabled:
        # Disable automatic VAD so we can send explicit activityStart/activityEnd
        realtime_input_cfg = genai_types.RealtimeInputConfig(
            automatic_activity_detection=genai_types.AutomaticActivityDetection(disabled=True),
        )
    
    gemini_config = genai_types.LiveConnectConfig(
        response_modalities=["AUDIO"],
        speech_config=genai_types.SpeechConfig(
            voice_config=genai_types.VoiceConfig(
                prebuilt_voice_config=genai_types.PrebuiltVoiceConfig(voice_name=voice)
            )
        ),
        system_instruction=genai_types.Content(
            parts=[genai_types.Part(text=system_prompt)]
        ),
        realtime_input_config=realtime_input_cfg,
    )
    
    try:
        async with client.aio.live.connect(model=model, config=gemini_config) as session:
            logger.info(f"[{call_sid}] Gemini session connected")
            
            # Send initial greeting as text — Gemini will generate audio
            await session.send_client_content(
                turns=genai_types.Content(
                    role="user",
                    parts=[genai_types.Part(text="The call just connected. Please greet the caller warmly.")]
                ),
                turn_complete=True,
            )
            
            # Tasks for concurrent send/receive
            stop_event = asyncio.Event()
            
            async def receive_from_twilio():
                """Read audio from Twilio WebSocket, transcode, send to Gemini."""
                try:
                    while not stop_event.is_set():
                        try:
                            msg = await asyncio.wait_for(ws.receive_text(), timeout=1.0)
                        except asyncio.TimeoutError:
                            continue
                        
                        data = json.loads(msg)
                        event = data.get("event")
                        
                        if event == "media":
                            payload = data["media"]["payload"]
                            mulaw_bytes = base64.b64decode(payload)
                            pcm_24k = mulaw_to_pcm16_24k(mulaw_bytes)
                            
                            # VAD processing
                            if config.vad_enabled and vad.greeting_done:
                                rms = compute_rms(pcm_24k)
                                threshold = vad.get_threshold(config.vad_energy_threshold)
                                now = time.monotonic()
                                
                                if rms > threshold:
                                    if not vad.is_speaking:
                                        if vad.speech_start is None:
                                            vad.speech_start = now
                                        elif (now - vad.speech_start) * 1000 >= config.vad_speech_min_ms:
                                            vad.is_speaking = True
                                            vad.silence_start = None
                                            active_calls[call_sid]["vad_events"] = active_calls[call_sid].get("vad_events", 0) + 1
                                            log_call_event(call_sid, "vad_activity_start",
                                                           rms=round(rms, 4), threshold=round(threshold, 4),
                                                           elapsed_s=round(time.monotonic() - call_start, 1),
                                                           vad_event_num=active_calls[call_sid]["vad_events"])
                                            await session.send_realtime_input(
                                                activity_start=genai_types.ActivityStart()
                                            )
                                    else:
                                        vad.silence_start = None
                                else:
                                    vad.speech_start = None
                                    if vad.is_speaking:
                                        if vad.silence_start is None:
                                            vad.silence_start = now
                                        elif (now - vad.silence_start) * 1000 >= config.vad_silence_ms:
                                            vad.is_speaking = False
                                            log_call_event(call_sid, "vad_activity_end",
                                                           silence_ms=round((now - vad.silence_start) * 1000),
                                                           elapsed_s=round(time.monotonic() - call_start, 1))
                                            await session.send_realtime_input(
                                                activity_end=genai_types.ActivityEnd()
                                            )
                            
                            # Send audio to Gemini
                            await session.send_realtime_input(
                                audio=genai_types.Blob(data=pcm_24k, mime_type="audio/pcm;rate=24000")
                            )
                        
                        elif event == "stop":
                            logger.info(f"[{call_sid}] Twilio stream stopped")
                            stop_event.set()
                            break
                
                except WebSocketDisconnect:
                    logger.info(f"[{call_sid}] Twilio WebSocket disconnected")
                    stop_event.set()
                except Exception as e:
                    logger.error(f"[{call_sid}] Error receiving from Twilio: {e}")
                    stop_event.set()
            
            async def send_to_twilio():
                """Read audio from Gemini, transcode, send to Twilio WebSocket."""
                try:
                    while not stop_event.is_set():
                        try:
                            turn = session.receive()
                            async for response in turn:
                                if stop_event.is_set():
                                    break
                                
                                # Check for audio data in server content
                                if response.server_content:
                                    sc = response.server_content
                                    
                                    if sc.model_turn and sc.model_turn.parts:
                                        vad.agent_speaking = True
                                        for part in sc.model_turn.parts:
                                            if part.inline_data and part.inline_data.data:
                                                pcm_data = part.inline_data.data
                                                if isinstance(pcm_data, str):
                                                    pcm_data = base64.b64decode(pcm_data)
                                                
                                                mulaw = pcm16_24k_to_mulaw(pcm_data)
                                                payload = base64.b64encode(mulaw).decode("ascii")
                                                
                                                media_msg = {
                                                    "event": "media",
                                                    "streamSid": stream_sid,
                                                    "media": {"payload": payload},
                                                }
                                                try:
                                                    await ws.send_text(json.dumps(media_msg))
                                                except Exception:
                                                    stop_event.set()
                                                    break
                                    
                                    if sc.turn_complete:
                                        vad.agent_speaking = False
                                        vad.agent_speech_end = time.monotonic()
                                        if not vad.greeting_done:
                                            vad.greeting_done = True
                                            log_call_event(call_sid, "greeting_done",
                                                           elapsed_s=round(time.monotonic() - call_start, 1))
                                
                                if response.tool_call:
                                    logger.info(f"[{call_sid}] Tool call from Gemini (ignored): {response.tool_call}")
                        
                        except Exception as e:
                            if not stop_event.is_set():
                                logger.error(f"[{call_sid}] Error in Gemini receive: {e}")
                            break
                
                except Exception as e:
                    logger.error(f"[{call_sid}] Error sending to Twilio: {e}")
                    stop_event.set()
            
            # Run both directions concurrently
            tasks = [
                asyncio.create_task(receive_from_twilio()),
                asyncio.create_task(send_to_twilio()),
            ]
            
            # Also set a max duration timeout
            async def max_duration_watchdog():
                await asyncio.sleep(config.max_duration)
                if not stop_event.is_set():
                    logger.warning(f"[{call_sid}] Max duration ({config.max_duration}s) reached")
                    stop_event.set()
            
            tasks.append(asyncio.create_task(max_duration_watchdog()))
            
            done, pending = await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)
            stop_event.set()
            for t in pending:
                t.cancel()
                try:
                    await t
                except (asyncio.CancelledError, Exception):
                    pass
    
    except Exception as e:
        logger.error(f"[{call_sid}] Gemini session error: {e}")
    
    finally:
        duration = time.monotonic() - call_start
        vad_events = active_calls.get(call_sid, {}).get("vad_events", 0)
        log_call_event(call_sid, "call_ended",
                       duration_s=round(duration, 1), vad_events=vad_events,
                       model=model, voice=voice)
        active_calls.pop(call_sid, None)


# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------

@router.get("/status")
async def status():
    return {
        "status": "running",
        "model": config.gemini_model,
        "voice": config.gemini_voice,
        "from": config.twilio_from,
        "active_calls": len(active_calls),
        "calls": {k: {"duration": time.monotonic() - v["start"], "vad_events": v.get("vad_events", 0)}
                  for k, v in active_calls.items()},
        "vad_enabled": config.vad_enabled,
    }


@router.api_route("/incoming", methods=["GET", "POST"])
async def incoming_call(request: Request):
    """TwiML response for inbound calls — connects to WebSocket media stream."""
    twiml = f"""<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Connect>
        <Stream url="wss://{request.headers.get('host', 'athena.abfs.tech')}{config.route_prefix}/stream">
            <Parameter name="direction" value="inbound" />
        </Stream>
    </Connect>
</Response>"""
    return Response(content=twiml, media_type="application/xml")


@router.websocket("/stream")
async def websocket_stream(ws: WebSocket):
    """WebSocket endpoint for Twilio Media Streams."""
    await ws.accept()
    logger.info("WebSocket connected")
    
    start_data = None
    call_sid = "unknown"
    
    try:
        # Wait for the start event
        while True:
            msg = await asyncio.wait_for(ws.receive_text(), timeout=30.0)
            data = json.loads(msg)
            if data.get("event") == "start":
                start_data = data.get("start", {})
                call_sid = start_data.get("callSid", "unknown")
                logger.info(f"[{call_sid}] Stream started: {json.dumps(start_data, indent=2)}")
                break
            elif data.get("event") == "connected":
                logger.info("Stream connected event received")
                continue
        
        if start_data:
            await run_call(ws, start_data, config.system_prompt,
                          config.gemini_voice, config.gemini_model, call_sid)
    
    except asyncio.TimeoutError:
        logger.warning("WebSocket timed out waiting for start event")
    except WebSocketDisconnect:
        logger.info(f"[{call_sid}] WebSocket disconnected")
    except Exception as e:
        logger.error(f"[{call_sid}] WebSocket error: {e}")


@router.post("/call")
async def make_call(request: Request):
    """Initiate an outbound call via Twilio → Gemini Live."""
    body = await request.json()
    to = body.get("to")
    greeting = body.get("greeting", "")
    from_number = body.get("from", config.twilio_from)
    record = body.get("record", config.default_record)
    
    if not to:
        return {"error": "Missing 'to' parameter"}
    
    if not twilio_client:
        return {"error": "Twilio client not initialized (missing auth token)"}
    
    # Build TwiML for outbound call
    twiml_url = f"{config.public_url}/twiml"
    status_url = f"{config.public_url}/call-status"
    
    try:
        call = twilio_client.calls.create(
            to=to,
            from_=from_number,
            url=twiml_url,
            status_callback=status_url,
            status_callback_event=["initiated", "ringing", "answered", "completed"],
            record=record,
        )
        logger.info(f"Outbound call initiated: {call.sid} to {to}")
        return {"call_sid": call.sid, "to": to, "from": from_number, "status": "initiated"}
    except Exception as e:
        logger.error(f"Failed to create call: {e}")
        return {"error": str(e)}


@router.api_route("/twiml", methods=["GET", "POST"])
async def twiml_for_outbound(request: Request):
    """TwiML for outbound calls — connects to the same WebSocket stream."""
    twiml = f"""<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Connect>
        <Stream url="wss://{request.headers.get('host', 'athena.abfs.tech')}{config.route_prefix}/stream">
            <Parameter name="direction" value="outbound" />
        </Stream>
    </Connect>
</Response>"""
    return Response(content=twiml, media_type="application/xml")


@router.api_route("/call-status", methods=["GET", "POST"])
async def call_status(request: Request):
    """Receive Twilio call status webhooks."""
    if request.method == "POST":
        form = await request.form()
        data = dict(form)
    else:
        data = dict(request.query_params)
    
    call_sid = data.get("CallSid", "unknown")
    status = data.get("CallStatus", "unknown")
    logger.info(f"[{call_sid}] Call status: {status}")
    
    # Update active call status
    if call_sid in active_calls:
        active_calls[call_sid]["status"] = status
    
    return Response(status_code=204)


@router.api_route("/recording-status", methods=["GET", "POST"])
async def recording_status(request: Request):
    """Receive Twilio recording status webhooks."""
    if request.method == "POST":
        form = await request.form()
        data = dict(form)
    else:
        data = dict(request.query_params)
    
    logger.info(f"Recording status: {data.get('RecordingStatus', 'unknown')} "
                f"SID: {data.get('RecordingSid', 'unknown')}")
    return Response(status_code=204)


# ---------------------------------------------------------------------------
# App
# ---------------------------------------------------------------------------

@asynccontextmanager
async def lifespan(app: FastAPI):
    global twilio_client
    
    # Load Twilio auth token
    if not config.twilio_auth_token:
        # Try to load from env file or secrets
        auth = os.getenv("TWILIO_AUTH_TOKEN", "")
        if auth:
            config.twilio_auth_token = auth
    
    if config.twilio_account_sid and config.twilio_auth_token:
        twilio_client = TwilioClient(config.twilio_account_sid, config.twilio_auth_token)
        logger.info(f"Twilio client initialized: {config.twilio_account_sid}")
    else:
        logger.warning("Twilio auth token not set — outbound calls disabled")
    
    if not config.gemini_api_key:
        logger.error("GEMINI_API_KEY / GOOGLE_API_KEY not set!")
    
    logger.info(f"Bridge starting: model={config.gemini_model}, voice={config.gemini_voice}, "
                f"from={config.twilio_from}, VAD={'on' if config.vad_enabled else 'off'}")
    
    yield
    
    logger.info("Bridge shutting down")


app = FastAPI(title="Gemini Live Phone Bridge", lifespan=lifespan)
app.include_router(router)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def parse_args():
    p = argparse.ArgumentParser(description="Gemini Live Phone Bridge")
    p.add_argument("--host", default="0.0.0.0")
    p.add_argument("--port", type=int, default=3335)
    p.add_argument("--model", default=config.gemini_model)
    p.add_argument("--voice", default=config.gemini_voice)
    p.add_argument("--from-number", default=config.twilio_from)
    p.add_argument("--system-prompt", default=config.system_prompt)
    p.add_argument("--max-duration", type=int, default=300)
    p.add_argument("--log-level", default="info", choices=["debug", "info", "warning", "error"])
    p.add_argument("--record", action="store_true", default=False)
    
    # VAD
    p.add_argument("--vad-enabled", action="store_true", default=True)
    p.add_argument("--no-vad", dest="vad_enabled", action="store_false")
    p.add_argument("--vad-silence-ms", type=int, default=500)
    p.add_argument("--vad-energy-threshold", type=float, default=0.01)
    p.add_argument("--vad-speech-min-ms", type=int, default=100)
    p.add_argument("--vad-prefix-ms", type=int, default=200)
    
    # Echo suppression
    p.add_argument("--echo-multiplier", type=float, default=3.0)
    p.add_argument("--echo-decay-ms", type=int, default=300)
    
    return p.parse_args()


if __name__ == "__main__":
    import uvicorn
    
    args = parse_args()
    
    config.host = args.host
    config.port = args.port
    config.gemini_model = args.model
    config.gemini_voice = args.voice
    config.twilio_from = args.from_number
    config.system_prompt = args.system_prompt
    config.max_duration = args.max_duration
    config.log_level = args.log_level
    config.default_record = args.record
    config.vad_enabled = args.vad_enabled
    config.vad_silence_ms = args.vad_silence_ms
    config.vad_energy_threshold = args.vad_energy_threshold
    config.vad_speech_min_ms = args.vad_speech_min_ms
    config.vad_prefix_ms = args.vad_prefix_ms
    config.echo_multiplier = args.echo_multiplier
    config.echo_decay_ms = args.echo_decay_ms
    
    logging.basicConfig(
        level=getattr(logging, config.log_level.upper()),
        format="%(asctime)s [%(name)s] %(levelname)s: %(message)s",
    )
    
    # Add OpenClaw structured file handler so `openclaw logs` sees our events
    openclaw_handler = OpenClawFileHandler()
    openclaw_handler.setLevel(logging.INFO)
    logging.getLogger("gemini-live-bridge").addHandler(openclaw_handler)
    
    uvicorn.run(app, host=config.host, port=config.port, log_level=config.log_level)
