import json
import os
import pathlib
import re
import urllib.error
import urllib.request
from typing import Any

SKILL_ID = "billcat-save-my-money"
EXTRACT_BILL_URL = "https://billcat.cn/api/app/openclaw/extractbill"
SKILL_API_URL = "https://billcat.cn/api/app/openclaw/skill"


def load_key_from_openclaw_config() -> str | None:
    config_path = pathlib.Path.home() / ".openclaw" / "openclaw.json"
    if not config_path.exists():
        return None

    try:
        data = json.loads(config_path.read_text(encoding="utf-8", errors="ignore"))
    except Exception:
        return None

    entries = (((data.get("skills") or {}).get("entries")) or {})
    skill_entry = entries.get(SKILL_ID) or {}

    env_value = ((skill_entry.get("env") or {}).get("BILLCAT_API_KEY"))
    if isinstance(env_value, str) and env_value.strip():
        return env_value.strip()

    api_key = skill_entry.get("apiKey")
    if isinstance(api_key, str) and api_key.strip():
        return api_key.strip()

    return None


def load_key() -> str | None:
    key = os.environ.get("BILLCAT_API_KEY")
    if key and key.strip():
        return key.strip()

    key = load_key_from_openclaw_config()
    if key:
        return key

    env_path = pathlib.Path.home() / ".openclaw" / ".env"
    if env_path.exists():
        try:
            txt = env_path.read_text(encoding="utf-8", errors="ignore")
            match = re.search(r"^\s*BILLCAT_API_KEY\s*=\s*(.+?)\s*$", txt, re.M)
            if match:
                value = match.group(1).strip().strip('"').strip("'")
                if value:
                    return value
        except Exception:
            pass

    return None


def post_json(url: str, payload: dict[str, Any], timeout: int = 30) -> Any:
    key = load_key()
    if not key:
        raise SystemExit(
            "Missing BILLCAT_API_KEY. Get it from the 乖猫记账 app, then set env var BILLCAT_API_KEY or add it to ~/.openclaw/.env"
        )

    body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    request = urllib.request.Request(
        url,
        data=body,
        headers={
            "Accept": "application/json",
            "Authorization": f"Bearer {key}",
            "Content-Type": "application/json",
        },
        method="POST",
    )

    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            raw_body = response.read().decode("utf-8", errors="replace")
    except urllib.error.HTTPError as exc:
        error_body = exc.read().decode("utf-8", errors="replace")
        raise SystemExit(f"BillCat HTTP {exc.code}: {error_body[:500]}") from exc
    except urllib.error.URLError as exc:
        raise SystemExit(f"BillCat request failed: {exc}") from exc

    try:
        return json.loads(raw_body)
    except json.JSONDecodeError as exc:
        raise SystemExit(f"BillCat returned non-JSON response: {raw_body[:500]}") from exc


def pick(obj: dict[str, Any], *names: str) -> Any:
    for name in names:
        if name in obj:
            return obj[name]
    return None
