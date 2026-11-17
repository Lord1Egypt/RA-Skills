#!/usr/bin/env python3
"""
AI Quota & Limits Collector (Zero-Leakage Architecture)
Collects real-time quota telemetry across AI providers.
Enforces strict file permission checks (0600) and domain pinning.
"""

import os
import sys
import stat
import json
import urllib.request
import urllib.parse
from datetime import datetime, timezone
from pathlib import Path

DEFAULT_CONFIG_PATH = os.path.expanduser("~/.config/ai-quota-dashboard/config.json")
DEFAULT_OUTPUT_PATH = "/tmp/ai_quota_cache.json"

def audit_file_permissions(filepath: str) -> None:
    """Verifies that credentials files are readable by the owner only."""
    p = Path(filepath).resolve()
    if not p.exists():
        return
    mode = stat.S_IMODE(p.stat().st_mode)
    if mode & (stat.S_IRWXG | stat.S_IRWXO):
        raise PermissionError(
            f"Security Violation: {p} has permissive permissions {oct(mode)}. "
            f"Run `chmod 600 {p}` to restrict access."
        )

def safe_https_get(url: str, headers: dict, pinned_domain: str, proxy: str = None) -> dict:
    """Performs an HTTPS GET request strictly pinned to the verified provider domain."""
    parsed = urllib.parse.urlparse(url)
    if parsed.scheme != "https":
        raise ValueError(f"Insecure protocol: {parsed.scheme}. HTTPS is required.")
    if parsed.netloc != pinned_domain:
        raise ValueError(f"Domain mismatch: got {parsed.netloc}, expected {pinned_domain}.")

    req = urllib.request.Request(url, headers=headers)
    handlers = []
    if proxy:
        handlers.append(urllib.request.ProxyHandler({"http": proxy, "https": proxy}))
    opener = urllib.request.build_opener(*handlers)

    with opener.open(req, timeout=12) as resp:
        return json.loads(resp.read().decode("utf-8"))

def collect_openrouter(config: dict, proxy: str = None) -> list:
    key = config.get("api_key")
    if not key:
        return []
    url = "https://openrouter.ai/api/v1/auth/key"
    pinned = "openrouter.ai"
    try:
        data = safe_https_get(url, {"Authorization": f"Bearer {key}"}, pinned, proxy)
        kd = data.get("data", {})
        limit = kd.get("limit") or 0.0
        usage = kd.get("usage") or 0.0
        remaining = kd.get("limit_remaining")
        return [{
            "provider": "OpenRouter",
            "account": kd.get("label", "Default Key"),
            "category": "api_credits",
            "used": round(usage, 4),
            "limit": round(limit, 4) if limit else "Pay-as-you-go",
            "remaining": round(remaining, 4) if remaining is not None else None,
            "unit": "USD",
            "status": "healthy" if (remaining is None or remaining > 0) else "exhausted"
        }]
    except Exception as e:
        return [{"provider": "OpenRouter", "error": str(e), "status": "error"}]

def collect_elevenlabs(config: dict, proxy: str = None) -> list:
    key = config.get("api_key")
    if not key:
        return []
    url = "https://api.elevenlabs.io/v1/user/subscription"
    pinned = "api.elevenlabs.io"
    try:
        data = safe_https_get(url, {"xi-api-key": key}, pinned, proxy)
        used = data.get("character_count", 0)
        limit = data.get("character_limit", 0)
        reset_ts = data.get("next_character_count_reset_unix", 0)
        reset_iso = datetime.fromtimestamp(reset_ts, tz=timezone.utc).isoformat() if reset_ts else None
        pct = round((used / limit) * 100, 1) if limit > 0 else 0
        return [{
            "provider": "ElevenLabs",
            "account": data.get("tier", "Standard"),
            "category": "voice_quota",
            "used": used,
            "limit": limit,
            "percent_used": pct,
            "unit": "characters",
            "resets_at": reset_iso,
            "status": "warning" if pct > 85 else "healthy"
        }]
    except Exception as e:
        return [{"provider": "ElevenLabs", "error": str(e), "status": "error"}]

def main():
    config_path = os.environ.get("QUOTA_CONFIG_PATH", DEFAULT_CONFIG_PATH)
    output_path = os.environ.get("QUOTA_OUTPUT_PATH", DEFAULT_OUTPUT_PATH)

    if not os.path.exists(config_path):
        print(f"Config file not found at {config_path}. Create it using config.example.json.")
        sys.exit(0)

    audit_file_permissions(config_path)

    with open(config_path, "r", encoding="utf-8") as f:
        config = json.load(f)

    proxy = config.get("proxy")
    providers_cfg = config.get("providers", {})
    results = []

    if "openrouter" in providers_cfg:
        results.extend(collect_openrouter(providers_cfg["openrouter"], proxy))
    if "elevenlabs" in providers_cfg:
        results.extend(collect_elevenlabs(providers_cfg["elevenlabs"], proxy))

    payload = {
        "collected_at": datetime.now(timezone.utc).isoformat(),
        "providers": results
    }

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2, ensure_ascii=False)

    print(f"Quota telemetry updated successfully -> {output_path}")

if __name__ == "__main__":
    main()
