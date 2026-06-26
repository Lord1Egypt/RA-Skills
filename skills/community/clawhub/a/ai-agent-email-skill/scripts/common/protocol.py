import io
import json
import sys
from typing import Any, Callable

from .errors import SkillError, SCHEMA_VERSION


def read_request() -> dict[str, Any]:
    raw = ""
    if hasattr(sys.stdin, "buffer"):
        raw = io.TextIOWrapper(sys.stdin.buffer, encoding="utf-8").read().strip()
    else:
        raw = sys.stdin.read().strip()
    if not raw:
        return {"schemaVersion": SCHEMA_VERSION, "data": {}}
    try:
        payload = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise SkillError("VALIDATION_ERROR", "stdin must be valid JSON", {"error": str(exc)}) from exc

    if not isinstance(payload, dict):
        raise SkillError("VALIDATION_ERROR", "request root must be a JSON object")

    data = payload.get("data", {})
    if data is None:
        payload["data"] = {}
    elif not isinstance(data, dict):
        raise SkillError("VALIDATION_ERROR", "data must be an object")

    payload.setdefault("schemaVersion", SCHEMA_VERSION)
    return payload


def write_success(request: dict[str, Any], data: dict[str, Any]) -> None:
    response: dict[str, Any] = {
        "ok": True,
        "requestId": request.get("requestId"),
        "schemaVersion": request.get("schemaVersion", SCHEMA_VERSION),
        "data": data,
    }
    sys.stdout.write(json.dumps(response, ensure_ascii=True))


def _stderr_log(payload: dict[str, Any]) -> None:
    sys.stderr.write(json.dumps(payload, ensure_ascii=True) + "\n")


def write_error(request: dict[str, Any] | None, exc: SkillError) -> None:
    response: dict[str, Any] = {
        "ok": False,
        "requestId": (request or {}).get("requestId"),
        "schemaVersion": (request or {}).get("schemaVersion", SCHEMA_VERSION),
        "error": exc.as_dict(),
    }
    _stderr_log(
        {
            "level": "ERROR",
            "code": exc.code,
            "message": exc.message,
            "requestId": (request or {}).get("requestId"),
        }
    )
    sys.stdout.write(json.dumps(response, ensure_ascii=True))


def write_unknown_error(request: dict[str, Any] | None, exc: Exception) -> None:
    response: dict[str, Any] = {
        "ok": False,
        "requestId": (request or {}).get("requestId"),
        "schemaVersion": (request or {}).get("schemaVersion", SCHEMA_VERSION),
        "error": {
            "code": "INTERNAL_ERROR",
            "message": "Unexpected error",
            "details": {"type": type(exc).__name__, "message": str(exc)},
        },
    }
    _stderr_log(
        {
            "level": "ERROR",
            "code": "INTERNAL_ERROR",
            "message": str(exc),
            "type": type(exc).__name__,
            "requestId": (request or {}).get("requestId"),
        }
    )
    sys.stdout.write(json.dumps(response, ensure_ascii=True))


def with_runtime(handler: Callable[[dict[str, Any]], dict[str, Any]]) -> int:
    request: dict[str, Any] | None = None
    try:
        request = read_request()
        data = handler(request)
        write_success(request, data)
        return 0
    except SkillError as exc:
        write_error(request, exc)
        return 1
    except Exception as exc:
        write_unknown_error(request, exc)
        return 2
