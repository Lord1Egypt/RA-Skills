#!/usr/bin/env python3
"""Portable JSON CLI for Crun media tasks and agent skills."""

from __future__ import annotations

import os
import sys
import time
import argparse
import http.client
import json
import mimetypes
from datetime import date
from pathlib import Path
from typing import Any, Optional
from urllib.error import HTTPError, URLError
from urllib.parse import quote, urlencode, urlsplit
from urllib.request import Request, urlopen

DEFAULT_BASE_URL = "https://api.crun.ai"
DEFAULT_BASE_URL_CHINA = "https://api.crunai.com"  # for mainland China regions
DEFAULT_REQUEST_RETRIES = 2
SUCCESS_CODE = 200
CHUNK_SIZE = 5 * 1024 * 1024
TERMINAL_STATUSES = {"success", "failed"}
RETRYABLE_HTTP_STATUS_CODES = {408, 429, 500, 502, 503, 504}

TEMPLATE_PLATFORMS = {
    "kling": {
        "path": "/api/v1/client/job/kling-templates",
        "template_parameter": "template_id",
    },
    "vidu": {
        "path": "/api/v1/client/job/vidu-templates",
        "template_parameter": "template",
    },
    "bytedance": {
        "path": "/api/v1/client/job/bytedance-templates",
        "template_parameter": "template_id",
    },
}

API_KEY_ENV = "CRUN_API_KEY"
API_KEY_PREFIX = "ak_"
API_KEY_LENGTH = 35

DEFAULT_CATALOG = Path(__file__).resolve().parent.parent / "catalog" / "models.json"
DEFAULT_OUTPUT_DIR = Path.home() / ".crun" / "output" / date.today().strftime("%Y-%m-%d")
CLI_SCRIPT_PATH = Path(__file__).resolve()
HOME_ENV_FILE = Path.home() / ".crun" / ".env"


class CrunError(RuntimeError):
    def __init__(self, message: str, *, payload: Any = None):
        super().__init__(message)
        self.payload = payload


class CrunNetworkError(CrunError):
    pass


def read_dotenv_value(path: Path, name: str) -> Optional[str]:
    """Read one value from a .env file without external dependencies."""
    try:
        lines = path.read_text(encoding="utf-8-sig").splitlines()
    except FileNotFoundError:
        return None
    except OSError as exc:
        raise CrunError(f"Cannot read API key configuration file: {path}") from exc

    result: Optional[str] = None
    for raw_line in lines:
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        if line.startswith("export "):
            line = line[7:].lstrip()
        key, separator, raw_value = line.partition("=")
        if not separator or key.strip() != name:
            continue

        value = raw_value.strip()
        if value[:1] in {"'", '"'}:
            closing_quote = value.find(value[0], 1)
            if closing_quote != -1:
                value = value[1:closing_quote]
        elif " #" in value:
            value = value.split(" #", 1)[0].rstrip()
        result = value
    return result


def validate_api_key(api_key: str, source: str) -> str:
    api_key = api_key.strip()
    if not api_key.startswith(API_KEY_PREFIX) or len(api_key) != API_KEY_LENGTH:
        raise CrunError(
            f"Invalid CRUN_API_KEY in {source}; expected 'ak_' followed by 32 characters"
        )
    return api_key


def api_key_configuration_options() -> list[dict[str, Any]]:
    """Permanent setup methods, ordered by recommendation.

    The recommended method is the CLI's own `config set-api-key` command, which
    persists the key into the home `~/.crun/.env` file; the environment
    variable is the alternative. Commands embed the absolute script path so
    they run from any working directory.
    """
    cli_command = f'python "{CLI_SCRIPT_PATH}" config set-api-key <your_api_key>'
    return [
        {
            "method": "cli_config_command",
            "location": str(HOME_ENV_FILE),
            "recommended": True,
            "commands": {
                "macos_linux": cli_command,
                "windows_cmd": cli_command,
                "windows_powershell": cli_command,
            },
        },
        {
            "method": "environment_variable",
            "location": API_KEY_ENV,
            "commands": {
                "macos_linux": (
                    f"echo 'export {API_KEY_ENV}=<your_api_key>' >> ~/.bashrc"
                    "   # use ~/.zshrc on macOS zsh; open a new terminal to apply"
                ),
                "windows_cmd": f"setx {API_KEY_ENV} <your_api_key>",
                "windows_powershell": (
                    f"[Environment]::SetEnvironmentVariable('{API_KEY_ENV}','<your_api_key>','User')"
                ),
            },
        },
    ]


def set_api_key(api_key: str) -> dict[str, Any]:
    """Validate the key and persist it into ~/.crun/.env (create or replace)."""
    api_key = validate_api_key(api_key, "config set-api-key argument")
    key_line = f"{API_KEY_ENV}={api_key}"

    lines: list[str] = []
    try:
        lines = HOME_ENV_FILE.read_text(encoding="utf-8-sig").splitlines()
    except FileNotFoundError:
        pass
    except OSError as exc:
        raise CrunError(f"Cannot read API key configuration file: {HOME_ENV_FILE}") from exc

    replaced = False
    for index, raw_line in enumerate(lines):
        stripped = raw_line.strip()
        if stripped.startswith("export "):
            stripped = stripped[7:].lstrip()
        if stripped.partition("=")[0].strip() == API_KEY_ENV:
            lines[index] = key_line
            replaced = True
    if not replaced:
        lines.append(key_line)

    try:
        HOME_ENV_FILE.parent.mkdir(parents=True, exist_ok=True)
        HOME_ENV_FILE.write_text("\n".join(lines) + "\n", encoding="utf-8")
    except OSError as exc:
        raise CrunError(f"Cannot write API key configuration file: {HOME_ENV_FILE}") from exc

    return {
        "ok": True,
        "action": "replaced" if replaced else "created",
        "location": str(HOME_ENV_FILE),
        "verify_with": f'python "{CLI_SCRIPT_PATH}" credits',
    }


def resolve_api_key() -> str:
    home_api_key = read_dotenv_value(HOME_ENV_FILE, API_KEY_ENV)
    if home_api_key:
        return validate_api_key(home_api_key, str(HOME_ENV_FILE))

    environment_api_key = os.getenv(API_KEY_ENV, "").strip()
    if environment_api_key:
        return validate_api_key(environment_api_key, f"environment variable {API_KEY_ENV}")

    raise CrunError(
        "CRUN_API_KEY is not configured. Configure it with the recommended "
        f'command: python "{CLI_SCRIPT_PATH}" config set-api-key <your_api_key>, '
        f"or set the {API_KEY_ENV} environment variable.",
        payload={"configuration_options": api_key_configuration_options()},
    )


class CrunClient:
    def __init__(
        self,
        base_url: str,
        api_key: str,
        request_timeout: float = 30.0,
        request_retries: int = DEFAULT_REQUEST_RETRIES,
    ):
        if not api_key:
            raise CrunError("CRUN_API_KEY is required for remote commands")
        if request_retries < 0:
            raise CrunError("request_retries must be zero or greater")
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key
        self.request_timeout = request_timeout
        self.request_retries = request_retries

    def request(
        self,
        method: str,
        path: str,
        *,
        query: Optional[dict[str, Any]] = None,
        body: Optional[dict[str, Any]] = None,
        retry: bool = True,
    ) -> Any:
        url = f"{self.base_url}{path}"
        if query:
            filtered = {key: value for key, value in query.items() if value is not None}
            if filtered:
                url = f"{url}?{urlencode(filtered)}"
        data = json.dumps(body).encode("utf-8") if body is not None else None
        request = Request(
            url,
            data=data,
            method=method,
            headers={
                "Accept": "application/json",
                "Content-Type": "application/json",
                "X-API-KEY": self.api_key,
                "User-Agent": "crun-agent-skills/1",
            },
        )
        attempts = self.request_retries + 1 if retry else 1
        for attempt in range(attempts):
            try:
                with urlopen(request, timeout=self.request_timeout) as response:
                    payload = json.loads(response.read().decode("utf-8"))
            except HTTPError as exc:
                raw = exc.read().decode("utf-8", errors="replace")
                try:
                    payload = json.loads(raw)
                except json.JSONDecodeError:
                    payload = {"message": raw or str(exc)}
                if retry and exc.code in RETRYABLE_HTTP_STATUS_CODES and attempt < attempts - 1:
                    self._sleep_before_retry(attempt)
                    continue
                raise CrunError(f"Crun HTTP error {exc.code}", payload=payload) from exc
            except URLError as exc:
                if retry and attempt < attempts - 1:
                    self._sleep_before_retry(attempt)
                    continue
                raise self._network_error(f"Crun network error: {exc.reason}") from exc
            except (TimeoutError, OSError) as exc:
                if retry and attempt < attempts - 1:
                    self._sleep_before_retry(attempt)
                    continue
                raise self._network_error(f"Crun request failed: {exc}") from exc
            except json.JSONDecodeError as exc:
                raise CrunError("Crun returned invalid JSON") from exc

            if not isinstance(payload, dict):
                raise CrunError("Crun returned an unexpected response", payload=payload)
            if payload.get("code") != SUCCESS_CODE:
                raise CrunError(str(payload.get("message") or "Crun request failed"), payload=payload)
            return payload.get("data")

        raise CrunError("Crun request retry loop exited unexpectedly")

    @staticmethod
    def _sleep_before_retry(attempt: int) -> None:
        time.sleep(min(2 ** attempt, 4.0))

    def _network_error(self, message: str) -> CrunNetworkError:
        """Build the terminal network error raised after all retries are exhausted."""
        hint = None
        if self.base_url == DEFAULT_BASE_URL:
            hint = (
                f"If you are in mainland China, try the China endpoint {DEFAULT_BASE_URL_CHINA} "
                f"by passing --base-url {DEFAULT_BASE_URL_CHINA} or setting "
                f"CRUN_BASE_URL={DEFAULT_BASE_URL_CHINA}."
            )
        return CrunNetworkError(
            f"{message}. {hint}" if hint else message,
            payload={"base_url": self.base_url, "suggested_base_url": DEFAULT_BASE_URL_CHINA} if hint else None,
        )

    def credits(self) -> dict[str, Any]:
        return self.request("GET", "/api/v1/client/account/balance")

    def list_models(self, modality: Optional[str] = None, operation: Optional[str] = None) -> dict[str, Any]:
        return self.request(
            "GET",
            "/api/v1/client/job/Models",
            query={"modality": modality, "operation": operation},
        )

    def describe_model(self, model: str) -> dict[str, Any]:
        return self.request("GET", f"/api/v1/client/job/Models/{quote(model, safe='/')}")

    def list_templates(
        self,
        platform: str,
        page: int = 1,
        page_size: int = 20,
        template_id: Optional[str] = None,
    ) -> dict[str, Any]:
        config = TEMPLATE_PLATFORMS[platform]
        query: dict[str, Any] = {
            "page": page,
            "page_size": page_size,
            config["template_parameter"]: template_id,
        }
        return self.request("GET", config["path"], query=query)

    def estimate_task(self, payload: dict[str, Any]) -> dict[str, Any]:
        return self.request("POST", "/api/v1/client/job/EstimateTask", body=payload)

    def create_task(self, payload: dict[str, Any]) -> dict[str, Any]:
        # Never retry this POST automatically: a retry can create and charge a duplicate task.
        return self.request("POST", "/api/v1/client/job/CreateTask", body=payload, retry=False)

    def task_info(self, task_id: str) -> dict[str, Any]:
        return self.request("GET", "/api/v1/client/job/TaskInfo", query={"task_id": task_id})

    def upload_file(self, file_path: Path, content_type: Optional[str] = None) -> dict[str, Any]:
        file_path = file_path.expanduser().resolve()
        if not file_path.is_file():
            raise CrunError(f"Upload file not found: {file_path}")
        if not file_path.suffix:
            raise CrunError("Upload file must have an extension")

        content_type = content_type or mimetypes.guess_type(file_path.name)[0]
        if not content_type:
            raise CrunError("Cannot infer the file MIME type; pass --content-type")
        upload = self.request(
            "GET",
            "/api/v1/client/files/upload-url",
            query={"content_type": content_type, "ext": file_path.suffix.lower()},
        )
        presigned_url = upload.get("presigned_url")
        file_url = upload.get("file_url")
        if not isinstance(presigned_url, str) or not isinstance(file_url, str):
            raise CrunError("Crun returned an invalid upload URL response", payload=upload)

        put_file_to_presigned_url(presigned_url, file_path, content_type, self.request_timeout)
        return {
            "file_url": file_url,
            "local_path": str(file_path),
            "content_type": content_type,
            "size_bytes": file_path.stat().st_size,
        }

    def wait_for_task(
        self,
        task_id: str,
        timeout_seconds: float,
        poll_interval: float,
        output_dir: Optional[Path] = None,
    ) -> dict[str, Any]:
        deadline = time.monotonic() + timeout_seconds
        last_data: Optional[dict[str, Any]] = None
        while True:
            try:
                last_data = self.task_info(task_id)
            except CrunNetworkError:
                if time.monotonic() >= deadline:
                    raise
                time.sleep(min(poll_interval, max(0.0, deadline - time.monotonic())))
                continue
            if str(last_data.get("status", "")).lower() in TERMINAL_STATUSES:
                task = normalize_task(last_data)
                return download_task_media(task, output_dir) if output_dir else task
            if time.monotonic() >= deadline:
                raise CrunError(
                    f"Local wait timed out for task {task_id}; do not create another task. "
                    "Resume with 'task wait' or inspect once with 'task status' using this task ID.",
                    payload={
                        "task_id": task_id,
                        "last_task": last_data,
                        "resume_with": {"command": "task wait", "task_id": task_id},
                    },
                )
            time.sleep(min(poll_interval, max(0.0, deadline - time.monotonic())))


def normalize_task(data: dict[str, Any]) -> dict[str, Any]:
    result = data.get("result") if isinstance(data.get("result"), dict) else {}
    status = str(data.get("status", "unknown")).lower()
    message = result.get("message")
    return {
        "ok": status == "success",
        "task_id": data.get("task_id"),
        "status": status,
        "model": (data.get("param") or {}).get("model") if isinstance(data.get("param"), dict) else None,
        "provider": data.get("provider"),
        "model_version": data.get("model_version"),
        "create_at": data.get("create_at"),
        "credits": data.get("credits"),
        "local_media_paths": [],
        "media_urls": result.get("media_urls") or [],
        "media_info": result.get("media_info") or {},
        "suno_data": result.get("suno_data") or [],
        "usage": result.get("usage") or {},
        "error": None if status == "success" else (message or data.get("message")),
        "raw_result": result,
    }


def put_file_to_presigned_url(presigned_url: str, file_path: Path, content_type: str, timeout: float) -> None:
    parsed = urlsplit(presigned_url)
    if parsed.scheme not in {"http", "https"} or not parsed.hostname:
        raise CrunError("Crun returned an invalid presigned upload URL")

    connection_class = http.client.HTTPSConnection if parsed.scheme == "https" else http.client.HTTPConnection
    connection = connection_class(parsed.hostname, parsed.port, timeout=timeout)
    target = parsed.path or "/"
    if parsed.query:
        target = f"{target}?{parsed.query}"
    try:
        connection.putrequest("PUT", target)
        connection.putheader("Content-Type", content_type)
        connection.putheader("Content-Length", str(file_path.stat().st_size))
        connection.endheaders()
        with file_path.open("rb") as source:
            while chunk := source.read(1024 * 1024):
                connection.send(chunk)
        response = connection.getresponse()
        if not 200 <= response.status < 300:
            detail = response.read(1024).decode("utf-8", errors="replace")
            raise CrunError(f"R2 upload failed with HTTP {response.status}", payload={"message": detail})
    except (OSError, http.client.HTTPException) as exc:
        raise CrunNetworkError(f"R2 upload failed: {exc}") from exc
    finally:
        connection.close()


def download_task_media(task: dict[str, Any], output_dir: Path) -> dict[str, Any]:
    task_id = str(task.get("task_id") or "unknown-task")
    task_dir = output_dir.expanduser().resolve() / task_id
    local_media_paths: list[str] = []
    download_errors: list[dict[str, str]] = []

    for index, media_url in enumerate(task.get("media_urls") or [], start=1):
        if not isinstance(media_url, str):
            download_errors.append({"media_url": str(media_url), "error": "media URL is not a string"})
            continue
        parsed = urlsplit(media_url)
        if parsed.scheme not in {"http", "https"}:
            download_errors.append({"media_url": media_url, "error": "media URL is not HTTP(S)"})
            continue
        suffix = Path(parsed.path).suffix or ".bin"
        target = task_dir / f"{index:02d}{suffix}"
        temporary = target.with_suffix(f"{target.suffix}.part")
        try:
            task_dir.mkdir(parents=True, exist_ok=True)
            request = Request(media_url, headers={"User-Agent": "crun-agent-skills/1"})
            with urlopen(request, timeout=30.0) as response, temporary.open("wb") as destination:
                while chunk := response.read(CHUNK_SIZE):
                    destination.write(chunk)
            temporary.replace(target)
            local_media_paths.append(str(target))
        except (OSError, HTTPError, URLError, TimeoutError, ValueError) as exc:
            temporary.unlink(missing_ok=True)
            download_errors.append({"media_url": media_url, "error": str(exc)})

    task["local_media_paths"] = local_media_paths
    if download_errors:
        task["media_download_errors"] = download_errors
    return task


def read_json_argument(value: str) -> dict[str, Any]:
    """Parse JSON supplied directly as a CLI argument."""
    parsed = json.loads(value)
    if not isinstance(parsed, dict):
        raise CrunError("JSON input must be an object")
    return parsed


def read_json_source(value: Optional[str], file_path: Optional[str], label: str) -> dict[str, Any]:
    """Read one JSON object from an argument, a UTF-8 file, or stdin."""
    if value is not None:
        return read_json_argument(value)
    if file_path is None:
        raise CrunError(f"Missing {label} JSON source")
    try:
        if file_path == "-":
            raw_bytes = sys.stdin.buffer.read()
        else:
            raw_bytes = Path(file_path).read_bytes()
    except OSError as exc:
        raise CrunError(f"Cannot read {label} JSON from {file_path}: {exc}") from exc
    try:
        raw = raw_bytes.decode("utf-8-sig")
    except UnicodeDecodeError as exc:
        source = "stdin" if file_path == "-" else file_path
        raise CrunError(
            f"{label} JSON from {source} is not valid UTF-8. Save it as UTF-8 and pass it with --{label}-file.",
            payload={"message": str(exc), "source": source},
        ) from exc
    if not raw.strip():
        raise CrunError(f"{label.capitalize()} JSON source is empty: {file_path}")
    return read_json_argument(raw)


def load_catalog(path: Path) -> dict[str, Any]:
    try:
        catalog = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise CrunError(f"Model catalog not found: {path}") from exc
    if not isinstance(catalog, dict) or not isinstance(catalog.get("models"), list):
        raise CrunError(f"Invalid model catalog: {path}")
    return catalog


def route_model(catalog: dict[str, Any], intent: dict[str, Any]) -> dict[str, Any]:
    modality = str(intent.get("modality") or "").lower()
    operation = str(intent.get("operation") or "").lower()
    references = intent.get("reference_media") or []
    if not operation:
        if modality == "image":
            operation = "image-edit" if references else "text-to-image"
        elif modality == "video":
            operation = "image-to-video" if references else "text-to-video"
        elif modality == "audio":
            operation = "music-generate"
    if not modality or not operation:
        raise CrunError("Routing intent requires modality and operation")

    native_audio = bool(intent.get("native_audio"))
    quality = str(intent.get("quality") or "balanced").lower()
    speed = str(intent.get("speed") or "balanced").lower()
    candidates: list[tuple[int, dict[str, Any]]] = []
    for model in catalog["models"]:
        if model.get("modality") != modality or operation not in model.get("operations", []):
            continue
        if native_audio and not model.get("supports_native_audio"):
            continue
        score = int(model.get("routing_priority", 0))
        if quality in {"best", "high", "quality"} and model.get("quality_tier") == "high":
            score += 25
        if speed in {"fast", "quick"} and model.get("speed_tier") == "fast":
            score += 25
        if references and model.get("supports_reference"):
            score += 10
        candidates.append((score, model))
    if not candidates:
        raise CrunError(
            "No model matches the routing intent",
            payload={"intent": intent, "modality": modality, "operation": operation},
        )
    candidates.sort(key=lambda item: (-item[0], item[1]["model"]))
    return {
        "intent": {**intent, "modality": modality, "operation": operation},
        "selected": candidates[0][1],
        "alternatives": [model for _, model in candidates[1:4]],
    }


def make_payload(model: str, input_data: dict[str, Any], callback_url: Optional[str] = None) -> dict[str, Any]:
    payload: dict[str, Any] = {"model": model, "input": input_data}
    if callback_url:
        payload["callback_url"] = callback_url
    return payload


def emit_task_created(task_id: str) -> None:
    """Expose the remote ID before a potentially long local polling wait."""
    print(
        json.dumps({"event": "task_created", "task_id": task_id}, ensure_ascii=False),
        file=sys.stderr,
        flush=True,
    )


def client_from_args(args: argparse.Namespace) -> CrunClient:
    return CrunClient(args.base_url, resolve_api_key(), args.request_timeout, args.request_retries)


def add_remote_options(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--base-url", default=os.getenv("CRUN_BASE_URL", DEFAULT_BASE_URL))
    parser.add_argument("--request-timeout", type=float, default=30.0)
    parser.add_argument(
        "--request-retries",
        type=int,
        default=DEFAULT_REQUEST_RETRIES,
        help="Retries for transient safe requests; CreateTask is never retried (default: 2)",
    )


def add_wait_options(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--timeout-seconds", type=float, default=120.0)
    parser.add_argument("--poll-interval", type=float, default=5.0)


def add_output_options(parser: argparse.ArgumentParser) -> None:
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=DEFAULT_OUTPUT_DIR,
        help="Directory for downloaded completed media (default: ~/.crun/output/yyyy-mm-dd)",
    )


def add_json_source_options(parser: argparse.ArgumentParser, name: str) -> None:
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument(f"--{name}-json")
    source.add_argument(
        f"--{name}-file",
        metavar="PATH",
        help=f"Read {name} JSON from a UTF-8 file, or use '-' to read stdin",
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--catalog", type=Path, default=DEFAULT_CATALOG)
    subparsers = parser.add_subparsers(dest="command", required=True)

    credits = subparsers.add_parser("credits", help="Get account credits")  # noqa
    add_remote_options(credits)

    config = subparsers.add_parser("config", help="Configure the CLI (API key)")
    config_sub = config.add_subparsers(dest="config_command", required=True)
    set_key = config_sub.add_parser("set-api-key", help="Validate and persist the API key into ~/.crun/.env")
    set_key.add_argument("api_key", help="Crun API key ('ak_' followed by 32 characters)")

    models = subparsers.add_parser("models", help="List, describe, or route models")
    model_sub = models.add_subparsers(dest="models_command", required=True)
    model_list = model_sub.add_parser("list")
    model_list.add_argument("--local", action="store_true")
    model_list.add_argument("--modality")
    model_list.add_argument("--operation")
    add_remote_options(model_list)
    describe = model_sub.add_parser("describe")
    describe.add_argument("--model", required=True)
    add_remote_options(describe)
    route = model_sub.add_parser("route")
    add_json_source_options(route, "intent")

    templates = subparsers.add_parser("templates", help="List effect templates by platform")
    template_sub = templates.add_subparsers(dest="templates_command", required=True)
    template_list = template_sub.add_parser("list")
    template_list.add_argument("--platform", required=True, choices=tuple(TEMPLATE_PLATFORMS))
    template_list.add_argument("--page", default=1)
    template_list.add_argument("--page-size", default=20, help="Number of templates to return per page, Max: 50")
    template_list.add_argument("--template-id", help="Return one exact template ID when supported")
    add_remote_options(template_list)

    task = subparsers.add_parser("task", help="Estimate, create, inspect, or run tasks")
    task_sub = task.add_subparsers(dest="task_command", required=True)
    for name in ("estimate", "create", "run"):
        command = task_sub.add_parser(name)
        command.add_argument("--model", required=True)
        add_json_source_options(command, "input")
        command.add_argument("--callback-url")
        add_remote_options(command)
        if name == "run":
            add_wait_options(command)
            add_output_options(command)
    status = task_sub.add_parser("status")
    status.add_argument("--task-id", required=True)
    add_remote_options(status)
    add_output_options(status)
    wait = task_sub.add_parser("wait", help="Wait for an existing task; never creates a task")
    wait.add_argument("--task-id", required=True)
    add_remote_options(wait)
    add_wait_options(wait)
    add_output_options(wait)

    upload = subparsers.add_parser("upload", help="Upload a local media file and return its Crun resource URL")
    upload.add_argument("file", type=Path, help="Local image, video, or audio file to upload")
    upload.add_argument("--content-type", help="Override the MIME type inferred from the file extension")
    add_remote_options(upload)

    media = subparsers.add_parser("media", help="Route and run a broad media request")
    media_sub = media.add_subparsers(dest="media_command", required=True)
    media_run = media_sub.add_parser("run")
    add_json_source_options(media_run, "intent")
    add_json_source_options(media_run, "input")
    media_run.add_argument("--model", help="Override model routing")
    media_run.add_argument("--callback-url")
    media_run.add_argument("--check-credits", action="store_true", help=argparse.SUPPRESS)
    add_remote_options(media_run)
    add_wait_options(media_run)
    add_output_options(media_run)
    return parser


def execute(args: argparse.Namespace) -> Any:
    if args.command == "credits":
        return client_from_args(args).credits()

    if args.command == "config":
        if args.config_command == "set-api-key":
            return set_api_key(args.api_key)
        raise CrunError("Unsupported config command")

    if args.command == "upload":
        return client_from_args(args).upload_file(args.file, args.content_type)

    if args.command == "models":
        if args.models_command == "route":
            return route_model(
                load_catalog(args.catalog),
                read_json_source(args.intent_json, args.intent_file, "intent")
            )
        if args.models_command == "describe":
            return client_from_args(args).describe_model(args.model)
        if args.local:
            models = load_catalog(args.catalog)["models"]
            models = [
                model for model in models
                if (not args.modality or model.get("modality") == args.modality or model.get(
                    "model_type") == args.modality)
                   and (not args.operation or args.operation in model.get("operations", []))
            ]
            return {"total": len(models), "models": models}
        return client_from_args(args).list_models(args.modality, args.operation)

    if args.command == "templates" and args.templates_command == "list":
        return client_from_args(args).list_templates(
            args.platform,
            args.page,
            args.page_size,
            args.template_id,
        )

    if args.command == "task":
        client = client_from_args(args)
        if args.task_command == "status":
            return download_task_media(normalize_task(client.task_info(args.task_id)), args.output_dir)
        if args.task_command == "wait":
            return client.wait_for_task(args.task_id, args.timeout_seconds, args.poll_interval, args.output_dir)
        payload = make_payload(
            args.model, read_json_source(args.input_json, args.input_file, "input"), args.callback_url
        )
        if args.task_command == "estimate":
            return client.estimate_task(payload)
        created = client.create_task(payload)
        if args.task_command == "create":
            return created
        emit_task_created(created["task_id"])
        return client.wait_for_task(created["task_id"], args.timeout_seconds, args.poll_interval, args.output_dir)

    if args.command == "media" and args.media_command == "run":
        if args.intent_file == "-" and args.input_file == "-":
            raise CrunError("Intent and input cannot both read from stdin; put at least one JSON object in a file")
        intent = read_json_source(args.intent_json, args.intent_file, "intent")
        routing = route_model(load_catalog(args.catalog), intent)
        model = args.model or routing["selected"]["model"]
        payload = make_payload(model, read_json_source(args.input_json, args.input_file, "input"), args.callback_url)
        client = client_from_args(args)
        estimate = client.estimate_task(payload) if args.check_credits else None
        if estimate and not estimate.get("affordable"):
            raise CrunError(
                "Insufficient credits for the selected task",
                payload={"routing": routing, "estimate": estimate}
            )
        created = client.create_task(payload)
        emit_task_created(created["task_id"])
        completed = client.wait_for_task(created["task_id"], args.timeout_seconds, args.poll_interval, args.output_dir)
        return {"routing": routing, "estimate": estimate, "task": completed}
    raise CrunError("Unsupported command")


def main() -> int:
    args = build_parser().parse_args()
    try:
        result = execute(args)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0
    except (CrunError, json.JSONDecodeError, OSError) as exc:
        payload = exc.payload if isinstance(exc, CrunError) else None
        print(
            json.dumps({"ok": False, "error": str(exc), "details": payload}, ensure_ascii=False, indent=2),
            file=sys.stderr
        )
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
