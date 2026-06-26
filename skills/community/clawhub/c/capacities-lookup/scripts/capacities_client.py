from __future__ import annotations

import json
import os
import time
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any


class CapacitiesError(RuntimeError):
    pass


class CapacitiesConfigError(CapacitiesError):
    pass


class CapacitiesAuthError(CapacitiesError):
    pass


class CapacitiesRateLimitError(CapacitiesError):
    pass


class CapacitiesRequestError(CapacitiesError):
    pass


def _detect_workspace_root() -> Path:
    env_root = os.environ.get("CAPACITIES_WORKSPACE_ROOT", "").strip()
    if env_root:
        return Path(env_root).expanduser().resolve()

    candidates: list[Path] = []
    cwd = Path.cwd().resolve()
    candidates.extend([cwd, *cwd.parents])

    script_path = Path(__file__).resolve()
    candidates.extend(script_path.parents)

    seen: set[Path] = set()
    for candidate in candidates:
        if candidate in seen:
            continue
        seen.add(candidate)
        if (candidate / "AGENTS.md").exists():
            return candidate
        if (candidate / "config" / "capacities.json").exists():
            return candidate

    return Path(__file__).resolve().parents[3]


WORKSPACE_ROOT = _detect_workspace_root()
CONFIG_PATH = WORKSPACE_ROOT / "config" / "capacities.json"


def load_config() -> dict[str, Any]:
    config: dict[str, Any] = {
        "apiBaseUrl": os.environ.get("CAPACITIES_API_BASE_URL", "https://api.capacities.io"),
        "timeoutMs": int(os.environ.get("CAPACITIES_TIMEOUT_MS", "15000")),
        "lookupCacheTtlSeconds": int(os.environ.get("CAPACITIES_LOOKUP_CACHE_TTL_SECONDS", "86400")),
        "verifySpacesOnSync": True,
        "defaultResultLimit": int(os.environ.get("CAPACITIES_DEFAULT_RESULT_LIMIT", "10")),
        "cacheSchemaVersion": 1,
    }

    if CONFIG_PATH.exists():
        with CONFIG_PATH.open("r", encoding="utf-8") as f:
            file_config = json.load(f)
        config.update(file_config)

    env_space_id = os.environ.get("CAPACITIES_SPACE_ID", "").strip()
    if env_space_id:
        config["mainSpaceId"] = env_space_id

    required = ["mainSpaceId", "apiBaseUrl", "timeoutMs"]
    missing = [key for key in required if not config.get(key)]
    if missing:
        raise CapacitiesConfigError(
            "Missing required Capacities config. Set CAPACITIES_SPACE_ID or config/capacities.json with mainSpaceId. "
            f"Missing: {', '.join(missing)}"
        )
    return config


def get_token() -> str:
    token = os.environ.get("CAPACITIES_API_TOKEN", "").strip()
    if not token:
        raise CapacitiesAuthError("CAPACITIES_API_TOKEN is not set")
    return token


def _read_error_body(exc: urllib.error.HTTPError) -> str:
    try:
        body = exc.read().decode("utf-8", errors="replace")
    except Exception:
        body = ""
    return body[:500]


def request(method: str, path: str, json_body: dict[str, Any] | None = None, retries: int = 2) -> dict[str, Any]:
    config = load_config()
    token = get_token()
    url = config["apiBaseUrl"].rstrip("/") + path
    timeout_seconds = max(int(config["timeoutMs"]) / 1000, 1)

    body_bytes = None
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/json",
    }
    if json_body is not None:
        body_bytes = json.dumps(json_body).encode("utf-8")
        headers["Content-Type"] = "application/json"

    last_error: Exception | None = None
    for attempt in range(retries + 1):
        req = urllib.request.Request(url, data=body_bytes, headers=headers, method=method.upper())
        try:
            with urllib.request.urlopen(req, timeout=timeout_seconds) as resp:
                raw = resp.read().decode("utf-8", errors="replace")
                if not raw.strip():
                    return {}
                return json.loads(raw)
        except urllib.error.HTTPError as exc:
            body = _read_error_body(exc)
            if exc.code == 401:
                raise CapacitiesAuthError("Capacities API returned 401 Unauthorized") from exc
            if exc.code == 429:
                reset = exc.headers.get("RateLimit-Reset") or exc.headers.get("Retry-After")
                if attempt < retries:
                    sleep_seconds = int(reset) if (reset and str(reset).isdigit()) else (attempt + 1)
                    time.sleep(max(sleep_seconds, 1))
                    continue
                raise CapacitiesRateLimitError(f"Capacities API rate limited request to {path}; reset={reset}") from exc
            if exc.code >= 500 and attempt < retries:
                time.sleep(attempt + 1)
                continue
            raise CapacitiesRequestError(f"Capacities API error {exc.code} for {path}: {body}") from exc
        except urllib.error.URLError as exc:
            last_error = exc
            if attempt < retries:
                time.sleep(attempt + 1)
                continue
            raise CapacitiesRequestError(f"Network error calling Capacities API {path}: {exc}") from exc
        except json.JSONDecodeError as exc:
            raise CapacitiesRequestError(f"Invalid JSON returned by Capacities API for {path}") from exc

    raise CapacitiesRequestError(f"Request failed for {path}: {last_error}")


def get_spaces() -> dict[str, Any]:
    return request("GET", "/spaces")


def get_space_info(space_id: str) -> dict[str, Any]:
    return request("GET", f"/space-info?spaceid={space_id}")


def lookup(space_id: str, search_term: str) -> dict[str, Any]:
    return request("POST", "/lookup", {"spaceId": space_id, "searchTerm": search_term})
