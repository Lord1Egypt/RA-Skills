"""
Brain Enhancement: cold-outreach-pro

Enhances outreach messages with brand positioning from the brain.
"""

import sys
from pathlib import Path

# Add brain to path
brain_path = Path("/data/.openclaw/workspace/company-brain")
if str(brain_path) not in sys.path:
    sys.path.insert(0, str(brain_path))

try:
    from brain_wrapper import Brain
    _brain = Brain()
except Exception:
    _brain = None


def enhance_outreach(company: str, role: str = None) -> dict:
    """
    Query brain for company-specific messaging guidance.
    Returns dict with enhanced context or empty fallback.
    """
    if _brain is None:
        return {"enhanced": False, "context": "", "confidence": 0}

    try:
        # Strategy context
        result = _brain.strategy(f"brand voice positioning for outreach to {company}")
        if result.get("confidence", 0) > 0.2:
            return {
                "enhanced": True,
                "context": result.get("answer", ""),
                "confidence": result.get("confidence", 0),
                "sources": result.get("sources", []),
            }

        # Fallback: generic brand voice
        result = _brain.strategy("brand voice default")
        if result.get("confidence", 0) > 0.2:
            return {
                "enhanced": True,
                "context": result.get("answer", ""),
                "confidence": result.get("confidence", 0),
            }
    except Exception:
        pass

    return {"enhanced": False, "context": "", "confidence": 0}


def enhance_prompt(legacy_prompt: str, company: str = None) -> str:
    """Convenience: return brain-enhanced prompt or legacy unchanged."""
    result = enhance_outreach(company or "prospect")
    if result["enhanced"]:
        return f"Brand Context:\n{result['context']}\n\n---\n\n{legacy_prompt}"
    return legacy_prompt
