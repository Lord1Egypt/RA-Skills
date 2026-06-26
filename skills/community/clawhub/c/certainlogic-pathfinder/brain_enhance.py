"""
Brain Enhancement: certainlogic-pathfinder

Enriches audit tracking with brain context about quality standards.
"""

import sys
from pathlib import Path

brain_path = Path("/data/.openclaw/workspace/company-brain")
if str(brain_path) not in sys.path:
    sys.path.insert(0, str(brain_path))

try:
    from brain_wrapper import Brain
    _brain = Brain()
except Exception:
    _brain = None


def get_audit_context(task_type: str = "general") -> dict:
    """Query brain for audit standards."""
    if _brain is None:
        return {"enhanced": False, "context": ""}

    try:
        result = _brain.query("audit trail requirements and logging standards")
        if result.get("confidence", 0) > 0.2:
            return {
                "enhanced": True,
                "context": result.get("answer", ""),
                "confidence": result.get("confidence", 0),
            }
    except Exception:
        pass

    return {"enhanced": False, "context": ""}


def enhance_audit_record(record: dict) -> dict:
    """Add brain context to an audit record if available."""
    result = get_audit_context(record.get("task_type", "general"))
    if result["enhanced"]:
        record["brain_context"] = result["context"]
        record["brain_confidence"] = result["confidence"]
    return record
