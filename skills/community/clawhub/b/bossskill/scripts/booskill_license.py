import hashlib
import json
import os
import platform
import sqlite3
import urllib.error
import urllib.request
from datetime import datetime, timedelta, timezone
from pathlib import Path


LICENSE_SERVER_URL = os.environ.get("BOOSKILL_LICENSE_SERVER", "https://bt.fanfan.la").rstrip("/")
CORE_SERVER_URL = os.environ.get("BOOSKILL_CORE_SERVER", f"{LICENSE_SERVER_URL}/api/core").rstrip("/")
LICENSE_CACHE_HOURS = int(os.environ.get("BOOSKILL_LICENSE_CACHE_HOURS", "72"))

COMMERCIAL_COMMANDS = {
    "assistant-action",
    "engine-link-brief",
    "conversation-intelligence",
    "secretary-flow",
    "proactive-secretary",
    "decision-advisor",
    "boss-cockpit",
    "profile-completion-brief",
    "sop-opportunity-brief",
    "usage-test-plan",
    "boss-preferences",
    "boss-learning-brief",
    "natural-followup-v2",
    "evening-review-v2",
    "advice-calibration",
    "secretary-rhythm",
    "boss-loop-v2",
    "tomorrow-command-plan",
    "record-correction",
    "correction-brief",
    "next-best-questions",
    "execution-closure-brief",
    "execution-score",
    "execution-training-plan",
    "execution-risk-brief",
    "advice-quality-check",
    "unknown-topic-learning-card",
    "industry-playbook",
    "knowledge-brief",
    "weekly-review",
    "evening-review",
    "task-followup-brief",
    "tomorrow-priorities",
    "deep-industry-pack",
    "customer-followup-strategy",
    "team-diagnosis-deep",
    "task-review-chaser",
    "metric-diagnosis-deep",
    "knowledge-growth-brief",
}


def cache_path(db_path):
    base = Path(db_path).resolve().parent if db_path else Path.cwd()
    return base / ".booskill_license.json"


def machine_id():
    raw = "|".join([platform.node(), platform.system(), platform.machine(), str(Path.home())])
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()[:32]


def read_license_key(db_path):
    env_key = os.environ.get("BOOSKILL_LICENSE_KEY", "").strip()
    if env_key:
        return env_key
    path = cache_path(db_path)
    if path.exists():
        try:
            return json.loads(path.read_text(encoding="utf-8")).get("license_key", "").strip()
        except json.JSONDecodeError:
            return ""
    return ""


def write_cache(db_path, data):
    path = cache_path(db_path)
    existing = {}
    if path.exists():
        try:
            existing = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            existing = {}
    existing.update(data)
    existing["checked_at"] = datetime.now(timezone.utc).isoformat()
    path.write_text(json.dumps(existing, ensure_ascii=False, indent=2), encoding="utf-8")


def cached_authorized(db_path):
    path = cache_path(db_path)
    if not path.exists():
        return False, "no_cache"
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
        checked_at = datetime.fromisoformat(data.get("checked_at", ""))
    except Exception:
        return False, "bad_cache"
    if data.get("allowed") and checked_at + timedelta(hours=LICENSE_CACHE_HOURS) >= datetime.now(timezone.utc):
        return True, "cached"
    return False, "cache_expired"


def request_license(endpoint, payload):
    data = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    request = urllib.request.Request(
        f"{LICENSE_SERVER_URL}{endpoint}",
        data=data,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(request, timeout=12) as response:
        return json.loads(response.read().decode("utf-8"))


def request_core(endpoint, payload):
    data = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    request = urllib.request.Request(
        f"{CORE_SERVER_URL}{endpoint}",
        data=data,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(request, timeout=60) as response:
        return json.loads(response.read().decode("utf-8"))


def activate_license(db_path, license_key):
    payload = {
        "license_key": license_key.strip(),
        "machine_id": machine_id(),
        "feature_name": "activate",
    }
    result = request_license("/api/license/activate", payload)
    result["license_key"] = license_key.strip()
    write_cache(db_path, result)
    return result


def check_license(db_path, feature_name):
    key = read_license_key(db_path)
    if not key:
        return {"allowed": False, "plan": "free", "reason": "missing_license_key"}
    payload = {
        "license_key": key,
        "machine_id": machine_id(),
        "feature_name": feature_name,
    }
    try:
        result = request_license("/api/license/check", payload)
        result["license_key"] = key
        write_cache(db_path, result)
        return result
    except (urllib.error.URLError, TimeoutError, OSError):
        allowed, reason = cached_authorized(db_path)
        return {"allowed": allowed, "plan": "authorized" if allowed else "free", "reason": reason}


def require_authorized(command, db_path):
    if os.environ.get("BOOSKILL_SKIP_LICENSE") == "1":
        return
    if command not in COMMERCIAL_COMMANDS:
        return
    result = check_license(db_path, command)
    if result.get("allowed"):
        return
    print(json.dumps({
        "intent": "license_required",
        "allowed": False,
        "plan": "free",
        "reason": result.get("reason", "not_authorized"),
        "message": "当前为免费版，只能使用基础客户/团队/任务记录、简单 Web 控制台和基础训练功能。该功能需要授权版。",
        "activate_command": "python scripts/startup_os_db.py activate-license --db startup_os.sqlite3 --license-key YOUR_LICENSE_KEY",
        "license_server": LICENSE_SERVER_URL,
    }, ensure_ascii=False, indent=2))
    raise SystemExit(2)


def cloud_enabled():
    return os.environ.get("BOOSKILL_CORE_MODE", "cloud").lower() != "local"


def core_payload(command, db_path, args, db_export=None):
    command_args = {
        "project_id": getattr(args, "project_id", None),
        "name": getattr(args, "name", None),
        "text": getattr(args, "text", None),
        "owner": getattr(args, "owner", None),
        "title": getattr(args, "title", None),
        "topic": getattr(args, "topic", None),
        "content_json": getattr(args, "content_json", None),
        "confidence": getattr(args, "confidence", None),
        "customer_id": getattr(args, "customer_id", None),
        "industry": getattr(args, "industry", None),
    }
    return {
        "command": command,
        "args": {key: value for key, value in command_args.items() if value not in [None, ""]},
        "license_key": read_license_key(db_path),
        "machine_id": machine_id(),
        "privacy_mode": "no_local_database_upload",
    }


def run_cloud_core(command, db_path, args, db_export=None):
    return request_core("/run", core_payload(command, db_path, args, db_export))
