from __future__ import annotations

import json
import logging
import re
import subprocess
import threading
from collections import deque
from pathlib import Path
from queue import Queue
from typing import Any, Deque, Dict, Iterator, Mapping, Optional, Sequence

from .errors import LarkCliError

LOGGER = logging.getLogger(__name__)
IMAGE_KEY = re.compile(r"\b(img_[A-Za-z0-9_-]+)\b")
TOKEN_REDACTIONS = (
    re.compile(r"Bearer\s+\S+", re.IGNORECASE),
    re.compile(r"\bt-[A-Za-z0-9_-]{12,}\b"),
)


def _redact(value: str) -> str:
    result = value
    for pattern in TOKEN_REDACTIONS:
        result = pattern.sub("[REDACTED_TOKEN]", result)
    return result


def _find_image_key(value: Any) -> Optional[str]:
    if isinstance(value, str):
        match = IMAGE_KEY.search(value)
        return match.group(1) if match else None
    if isinstance(value, Mapping):
        for child in value.values():
            found = _find_image_key(child)
            if found:
                return found
    if isinstance(value, list):
        for child in value:
            found = _find_image_key(child)
            if found:
                return found
    return None


def _find_string(value: Any, key: str) -> Optional[str]:
    """在 lark-cli 的不同响应信封中递归查找指定字符串字段。"""

    if isinstance(value, Mapping):
        candidate = value.get(key)
        if isinstance(candidate, str) and candidate:
            return candidate
        for child in value.values():
            found = _find_string(child, key)
            if found:
                return found
    if isinstance(value, list):
        for child in value:
            found = _find_string(child, key)
            if found:
                return found
    return None


class LarkClient:
    def __init__(self, binary: str = "lark-cli") -> None:
        self.binary = binary

    def _run(
        self,
        args: list[str],
        *,
        cwd: Optional[Path] = None,
        input_text: Optional[str] = None,
    ) -> Dict[str, Any]:
        try:
            completed = subprocess.run(
                [self.binary, *args],
                cwd=str(cwd) if cwd else None,
                input=input_text,
                capture_output=True,
                text=True,
                check=False,
            )
        except OSError as exc:
            raise LarkCliError(f"无法启动 lark-cli：{exc}") from exc
        if completed.returncode != 0:
            detail = _redact((completed.stderr or completed.stdout).strip()[-2000:])
            raise LarkCliError(f"lark-cli 调用失败：{detail}")
        output = completed.stdout.strip()
        if not output:
            return {}
        try:
            value = json.loads(output)
        except json.JSONDecodeError as exc:
            raise LarkCliError(f"lark-cli 返回了非 JSON 结果：{output[-1000:]}") from exc
        if not isinstance(value, dict):
            raise LarkCliError("lark-cli 返回结果不是 JSON 对象")
        if isinstance(value.get("code"), int) and value["code"] != 0:
            raise LarkCliError(
                f"飞书 API 错误 {value['code']}：{_redact(str(value.get('msg', '')))}"
            )
        return value

    def resolve_image_key(self, event: Mapping[str, Any]) -> str:
        key = _find_image_key(event.get("content"))
        if key:
            return key
        message_id = str(event["message_id"])
        detail = self._run(
            [
                "im",
                "+messages-mget",
                "--message-ids",
                message_id,
                "--format",
                "json",
                "--as",
                "bot",
            ]
        )
        key = _find_image_key(detail)
        if not key:
            raise LarkCliError("图片消息中没有找到 img_ 开头的资源 key")
        return key

    def download_image(
        self, message_id: str, image_key: str, output_dir: Path
    ) -> Path:
        output_dir.mkdir(mode=0o700, parents=True, exist_ok=True)
        base_name = re.sub(r"[^A-Za-z0-9_-]", "_", message_id)
        before = set(output_dir.glob(f"{base_name}*"))
        self._run(
            [
                "im",
                "+messages-resources-download",
                "--message-id",
                message_id,
                "--file-key",
                image_key,
                "--type",
                "image",
                "--output",
                base_name,
                "--as",
                "bot",
            ],
            cwd=output_dir,
        )
        candidates = sorted(
            set(output_dir.glob(f"{base_name}*")) - before,
            key=lambda item: item.stat().st_mtime,
            reverse=True,
        )
        exact = output_dir / base_name
        if exact.exists():
            return exact
        if not candidates:
            candidates = sorted(
                output_dir.glob(f"{base_name}*"),
                key=lambda item: item.stat().st_mtime,
                reverse=True,
            )
        if not candidates:
            raise LarkCliError("lark-cli 报告下载成功，但没有找到本地图片")
        return candidates[0]

    def upload_approval_file(self, image_path: Path, upload_type: str) -> str:
        if upload_type not in {"image", "attachment"}:
            raise ValueError("upload_type 必须是 image 或 attachment")
        result = self._run(
            [
                "api",
                "POST",
                "/approval/openapi/v2/file/upload",
                "--file",
                f"content={image_path}",
                "--data",
                "-",
                "--as",
                "bot",
            ],
            input_text=json.dumps(
                {"name": image_path.name, "type": upload_type},
                ensure_ascii=False,
                separators=(",", ":"),
            ),
        )
        code = result.get("data", {}).get("code")
        if not code:
            raise LarkCliError("审批文件上传响应中缺少 data.code")
        return str(code)

    def create_approval(self, payload: Mapping[str, Any]) -> Dict[str, Any]:
        return self._run(
            [
                "api",
                "POST",
                "/open-apis/approval/v4/instances",
                "--data",
                "-",
                "--as",
                "bot",
            ],
            input_text=json.dumps(
                payload, ensure_ascii=False, separators=(",", ":")
            ),
        )

    def reply(self, message_id: str, text: str, idempotency_key: str) -> None:
        self._run(
            [
                "im",
                "+messages-reply",
                "--message-id",
                message_id,
                "--text",
                text,
                "--idempotency-key",
                idempotency_key[:64],
                "--as",
                "bot",
            ]
        )

    def send_card(
        self,
        user_id: str,
        card: Mapping[str, Any],
        idempotency_key: str,
    ) -> str:
        """向指定用户私聊发送交互卡片，并返回卡片消息 ID。"""

        result = self._run(
            [
                "im",
                "+messages-send",
                "--user-id",
                user_id,
                "--msg-type",
                "interactive",
                "--content",
                json.dumps(card, ensure_ascii=False, separators=(",", ":")),
                "--idempotency-key",
                idempotency_key[:50],
                "--as",
                "bot",
            ]
        )
        message_id = _find_string(result, "message_id")
        if not message_id:
            raise LarkCliError("发送确认卡片的响应中缺少 message_id")
        return message_id

    def update_card(self, token: str, card: Mapping[str, Any]) -> None:
        """使用卡片回调 token 将原卡片更新为最终处理状态。"""

        self._run(
            [
                "api",
                "POST",
                "/open-apis/interactive/v1/card/update",
                "--data",
                "-",
                "--as",
                "bot",
            ],
            input_text=json.dumps(
                {"token": token, "card": card},
                ensure_ascii=False,
                separators=(",", ":"),
            ),
        )

    def stream_events(
        self,
        event_keys: Sequence[str],
        ready_timeout: int = 30,
    ) -> Iterator[Dict[str, Any]]:
        """并发监听多个飞书事件，并在同一迭代器中逐条产出。"""

        if not event_keys:
            return

        processes: Dict[str, subprocess.Popen[str]] = {}
        ready_events: Dict[str, threading.Event] = {}
        stderr_tails: Dict[str, Deque[str]] = {}
        output_queue: Queue[tuple[str, Any]] = Queue()

        def drain_stderr(event_key: str, process: subprocess.Popen[str]) -> None:
            assert process.stderr is not None
            for raw_line in process.stderr:
                line = _redact(raw_line.rstrip())
                stderr_tails[event_key].append(line)
                if f"[event] ready event_key={event_key}" in line:
                    ready_events[event_key].set()
                LOGGER.info("lark-event[%s]: %s", event_key, line)

        def drain_stdout(event_key: str, process: subprocess.Popen[str]) -> None:
            assert process.stdout is not None
            for raw_line in process.stdout:
                line = raw_line.strip()
                if not line:
                    continue
                try:
                    event = json.loads(line)
                except json.JSONDecodeError:
                    LOGGER.warning(
                        "忽略 %s 的非 JSON 事件行：%s", event_key, line[:500]
                    )
                    continue
                if isinstance(event, dict):
                    output_queue.put(("event", event))
            output_queue.put(("exit", (event_key, process.wait())))

        try:
            for event_key in event_keys:
                command = [
                    self.binary,
                    "event",
                    "consume",
                    event_key,
                    "--as",
                    "bot",
                ]
                try:
                    process = subprocess.Popen(
                        command,
                        stdin=subprocess.PIPE,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE,
                        text=True,
                        bufsize=1,
                    )
                except OSError as exc:
                    raise LarkCliError(
                        f"无法启动飞书事件监听 {event_key}：{exc}"
                    ) from exc
                processes[event_key] = process
                ready_events[event_key] = threading.Event()
                stderr_tails[event_key] = deque(maxlen=30)
                threading.Thread(
                    target=drain_stderr,
                    args=(event_key, process),
                    daemon=True,
                ).start()
                threading.Thread(
                    target=drain_stdout,
                    args=(event_key, process),
                    daemon=True,
                ).start()

            for event_key in event_keys:
                if not ready_events[event_key].wait(timeout=ready_timeout):
                    raise LarkCliError(
                        f"飞书事件监听 {event_key} 未就绪："
                        + "\n".join(stderr_tails[event_key])
                    )

            active = set(event_keys)
            while active:
                item_type, value = output_queue.get()
                if item_type == "event":
                    yield value
                    continue
                event_key, return_code = value
                active.discard(event_key)
                raise LarkCliError(
                    f"飞书事件监听 {event_key} 异常退出（{return_code}）："
                    + "\n".join(stderr_tails[event_key])
                )
        finally:
            for process in processes.values():
                if process.poll() is None:
                    process.terminate()
            for process in processes.values():
                if process.poll() is None:
                    try:
                        process.wait(timeout=10)
                    except subprocess.TimeoutExpired:
                        LOGGER.error("飞书事件监听未能在 10 秒内优雅退出")

    def stream_message_events(self, ready_timeout: int = 30) -> Iterator[Dict[str, Any]]:
        """兼容原接口：只监听图片消息事件。"""

        yield from self.stream_events(
            ["im.message.receive_v1"],
            ready_timeout=ready_timeout,
        )

    def stream_invoice_events(
        self, ready_timeout: int = 30
    ) -> Iterator[Dict[str, Any]]:
        """同时监听发票图片与确认卡片按钮回调。"""

        yield from self.stream_events(
            ["im.message.receive_v1", "card.action.trigger"],
            ready_timeout=ready_timeout,
        )
