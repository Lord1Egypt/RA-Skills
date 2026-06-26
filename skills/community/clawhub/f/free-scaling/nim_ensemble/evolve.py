"""Panel evolution — weekly promotion/demotion based on ELO.

Call evolve() weekly to:
1. Check if ELO-ranked top-3 differs from current static panel
2. If so, update models.py PANELS["general"] and log the change
3. Bench models that fell too far behind

This is the "gradient step" — small, data-driven panel updates.
"""
from __future__ import annotations

import json
import time
from pathlib import Path

from . import elo
from .models import PANELS, MODELS


def evolve(dry_run: bool = True, min_calls: int = 30) -> dict:
    """Evaluate whether panel should change based on ELO data.
    
    Args:
        dry_run: If True, report what would change but don't write.
        min_calls: Minimum calls per model before considering promotion.
    
    Returns:
        dict with: changed, current_panel, proposed_panel, elo_rankings, reason
    """
    ranked = elo.rank(min_calls=min_calls)
    
    if len(ranked) < 3:
        return {
            "changed": False,
            "reason": f"Not enough data — only {len(ranked)} models with ≥{min_calls} calls. Need 3.",
            "current_panel": PANELS.get("general", []),
            "proposed_panel": None,
            "elo_rankings": [(a, s["elo"], s["calls"]) for a, s in ranked],
        }
    
    current = set(PANELS.get("general", []))
    proposed = [alias for alias, _ in ranked[:3]]
    proposed_set = set(proposed)
    
    # Check if panel actually changed
    if current == proposed_set:
        return {
            "changed": False,
            "reason": "Current panel matches ELO top-3. No change needed.",
            "current_panel": PANELS.get("general", []),
            "proposed_panel": proposed,
            "elo_rankings": [(a, s["elo"], s["calls"]) for a, s in ranked],
        }
    
    # Calculate ELO gaps
    top_elo = ranked[0][1]["elo"]
    demoted = current - proposed_set
    promoted = proposed_set - current
    
    result = {
        "changed": True,
        "current_panel": PANELS.get("general", []),
        "proposed_panel": proposed,
        "promoted": list(promoted),
        "demoted": list(demoted),
        "elo_rankings": [(a, s["elo"], s["calls"]) for a, s in ranked],
        "reason": f"ELO data suggests: promote {promoted}, demote {demoted}",
    }
    
    if not dry_run:
        # Update the runtime PANELS dict (in-memory only for this process)
        PANELS["general"] = proposed
        PANELS["arbiter"] = [proposed[0]]
        
        # Log the evolution
        log_dir = Path(elo.STATE_DIR) / "evolution"
        log_dir.mkdir(parents=True, exist_ok=True)
        log_file = log_dir / f"evolution-{int(time.time())}.json"
        with open(log_file, "w") as f:
            json.dump(result, f, indent=2, default=str)
        
        result["log_file"] = str(log_file)
    
    return result


def report() -> str:
    """Human-readable evolution report for cron output."""
    lines = [elo.summary(), ""]
    
    ev = evolve(dry_run=True)
    lines.append("--- Panel Evolution Check ---")
    lines.append(f"Current: {ev['current_panel']}")
    
    if ev["changed"]:
        lines.append(f"Proposed: {ev['proposed_panel']}")
        lines.append(f"Promote: {ev.get('promoted', [])}")
        lines.append(f"Demote: {ev.get('demoted', [])}")
        lines.append("⚠️ Panel change recommended. Run `evolve(dry_run=False)` to apply.")
    else:
        lines.append(f"Status: {ev['reason']}")
    
    return "\n".join(lines)
