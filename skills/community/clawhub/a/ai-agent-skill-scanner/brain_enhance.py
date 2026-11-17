"""
Brain Enhancement: skill-vetter-plus

Enriches security vetting with brain policies.
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


def get_security_context() -> dict:
    """Query brain for security rules."""
    if _brain is None:
        return {"enhanced": False, "context": ""}

    try:
        result = _brain.strategy("security policy and code review requirements")
        if result.get("confidence", 0) > 0.2:
            return {
                "enhanced": True,
                "context": result.get("answer", ""),
                "confidence": result.get("confidence", 0),
            }
    except Exception:
        pass

    return {"enhanced": False, "context": ""}


def enhance_vetting_prompt(legacy_prompt: str) -> str:
    """Inject brain security context into vetting prompt."""
    result = get_security_context()
    if result["enhanced"]:
        return f"Security Policy Context:\n{result['context']}\n\n---\n\n{legacy_prompt}"
    return legacy_prompt
