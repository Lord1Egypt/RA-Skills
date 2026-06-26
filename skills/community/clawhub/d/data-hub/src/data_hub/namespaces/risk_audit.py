import json

from pydantic import ValidationError

from ..constants import RISK_AUDIT_KEY
from ..errors import format_validation_error
from ..models import RiskAuditModel


def push(memory: dict, data: dict) -> tuple[dict, str | None]:
    try:
        validated = RiskAuditModel(**data)
    except ValidationError as e:
        return memory, format_validation_error(e)

    risk = memory.get("risk_audit", {})
    new_risk = {**risk, RISK_AUDIT_KEY: validated.model_dump()}
    return {**memory, "risk_audit": new_risk}, None


def get(memory: dict) -> dict | None:
    return memory.get("risk_audit", {}).get(RISK_AUDIT_KEY)


def save_snapshot(data: dict, path: str) -> str | None:
    try:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        return None
    except OSError as e:
        return f"[SNAPSHOT_ERROR] Failed to save snapshot: {e}"


def load_snapshot(path: str) -> tuple[dict | None, str | None]:
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data, None
    except FileNotFoundError:
        return None, f"[SNAPSHOT_ERROR] Snapshot file not found: {path}"
    except (json.JSONDecodeError, OSError) as e:
        return None, f"[SNAPSHOT_ERROR] Failed to load snapshot: {e}"
