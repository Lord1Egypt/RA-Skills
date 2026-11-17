"""
Brain Enhancement: skill-oracle

Enriches skill doc queries with brain catalog standards.
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


def get_catalog_context() -> dict:
    """Query brain for catalog standards."""
    if _brain is None:
        return {"enhanced": False, "context": ""}

    try:
        result = _brain.query("skill documentation and catalog standards")
        if result.get("confidence", 0) > 0.2:
            return {
                "enhanced": True,
                "context": result.get("answer", ""),
                "confidence": result.get("confidence", 0),
            }
    except Exception:
        pass

    return {"enhanced": False, "context": ""}


def enhance_oracle_prompt(legacy_prompt: str) -> str:
    """Inject brain context into oracle prompt."""
    result = get_catalog_context()
    if result["enhanced"]:
        return f"Catalog Standards:\n{result['context']}\n\n---\n\n{legacy_prompt}"
    return legacy_prompt
