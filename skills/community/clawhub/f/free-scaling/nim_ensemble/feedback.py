"""User feedback loop for ELO updates.

Stores recent scale() results with context so that user feedback
(Discord reactions, CLI corrections) can be resolved to ELO updates.

Flow:
  1. scale() call → log_result() stores votes + answer + metadata
  2. User reacts (👍 confirm, ❌ wrong, 🔴 override to X)
  3. resolve_feedback() looks up the result and calls elo.update_from_override()

Storage: ~/.cache/free-scaling/feedback.json (last 200 entries, FIFO)
"""
from __future__ import annotations

import json
import os
import time
from pathlib import Path
from tempfile import NamedTemporaryFile
from threading import Lock

from . import elo

STATE_DIR = Path(os.environ.get("FREE_SCALING_STATE_DIR",
                                os.path.expanduser("~/.cache/free-scaling")))
FEEDBACK_FILE = STATE_DIR / "feedback.json"
MAX_ENTRIES = 200

_lock = Lock()


def _load() -> list:
    if FEEDBACK_FILE.exists():
        try:
            with open(FEEDBACK_FILE) as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            pass
    return []


def _save(entries: list):
    STATE_DIR.mkdir(parents=True, exist_ok=True)
    entries = entries[-MAX_ENTRIES:]
    with NamedTemporaryFile("w", dir=STATE_DIR, prefix="feedback-", suffix=".tmp", delete=False) as f:
        json.dump(entries, f, indent=2)
        tmp_name = f.name
    Path(tmp_name).replace(FEEDBACK_FILE)


def log_result(
    question: str,
    answer: str,
    votes: list[tuple[str, str, str | float]],
    tag: str = None,
    message_id: str = None,
    metadata: dict = None,
) -> str:
    """Log a scale() result for future feedback resolution.
    
    Args:
        question: The question asked
        answer: Final majority answer
        votes: [(model, answer, weight_or_raw), ...]
        tag: Category tag (e.g. "email-triage", "sanity-check")
        message_id: Discord message ID for reaction-based feedback
        metadata: Extra context (email subject, etc.)
    
    Returns:
        Entry ID (timestamp-based) for lookup.
    """
    entry_id = f"fb-{int(time.time() * 1000)}"
    entry = {
        "id": entry_id,
        "t": time.time(),
        "question": question[:200],
        "answer": answer,
        "votes": [(m, a, str(w)) for m, a, w in votes],
        "tag": tag,
        "message_id": message_id,
        "metadata": metadata or {},
        "resolved": False,
    }
    
    with _lock:
        entries = _load()
        entries.append(entry)
        _save(entries)
    return entry_id


def resolve_feedback(
    entry_id: str = None,
    message_id: str = None,
    correct_answer: str = None,
    confirmed: bool = False,
) -> dict:
    """Resolve feedback for a logged result.
    
    Args:
        entry_id: Direct lookup by entry ID
        message_id: Lookup by Discord message ID
        correct_answer: The right answer (override signal)
        confirmed: True = original answer was correct (👍 signal)
    
    Returns:
        dict with: resolved, entry_id, elo_updates
    """
    with _lock:
        entries = _load()

        # Find the entry
        entry = None
        for e in entries:
            if entry_id and e["id"] == entry_id:
                entry = e
                break
            if message_id and e.get("message_id") == message_id and not e.get("resolved"):
                entry = e
                break

        if not entry:
            return {"resolved": False, "error": "Entry not found"}

        if entry.get("resolved"):
            return {"resolved": False, "error": "Already resolved"}

        # Reconstruct votes as tuples
        votes = [(m, a, r) for m, a, r in entry["votes"]]

        if confirmed:
            # User confirmed the majority answer was correct
            elo.update_from_override(votes, entry["answer"].strip().upper())
            entry["resolved"] = True
            entry["feedback"] = "confirmed"
        elif correct_answer:
            # User says the correct answer was something else
            normalized_answer = correct_answer.strip().upper()
            elo.update_from_override(votes, normalized_answer)
            entry["resolved"] = True
            entry["feedback"] = f"override:{normalized_answer}"
        else:
            return {"resolved": False, "error": "Need either confirmed=True or correct_answer"}

        _save(entries)

        return {
            "resolved": True,
            "entry_id": entry["id"],
            "original_answer": entry["answer"],
            "feedback": entry["feedback"],
            "models_affected": [m for m, _, _ in votes],
        }


def resolve_by_reaction(message_id: str, emoji: str) -> dict:
    """Resolve feedback from a Discord reaction.
    
    Emoji mapping:
        👍 / ✅  → confirm (original answer correct)
        ❌ / 👎  → reject (mark wrong, but no override — models get penalty)
        🅰️       → Panel A was right (boost A models, penalize B)
        🅱️       → Panel B was right (boost B models, penalize A)
        🔴       → should have been URGENT
        🟡       → should have been NORMAL
        ⚪       → should have been IGNORE
        🟢       → should have been SAFE / YES / COMPLIANT
        🔥       → should have been VULNERABLE / CRITICAL
    """
    CONFIRM_EMOJI = {"👍", "✅", "🫡"}
    REJECT_EMOJI = {"❌", "👎"}
    AB_EMOJI = {"🅰️": "A", "🅱️": "B",
                "\U0001f170\ufe0f": "A", "\U0001f171\ufe0f": "B",  # variant forms
                "🇦": "A", "🇧": "B"}  # regional indicators as fallback
    OVERRIDE_MAP = {
        "🔴": "URGENT",
        "🟡": "NORMAL",
        "⚪": "IGNORE",
        "🟢": "SAFE",
        "🔥": "VULNERABLE",
    }
    
    if emoji in CONFIRM_EMOJI:
        return resolve_feedback(message_id=message_id, confirmed=True)
    elif emoji in REJECT_EMOJI:
        with _lock:
            entries = _load()
            for e in entries:
                if e.get("message_id") == message_id and not e.get("resolved"):
                    votes = [(m, a, r) for m, a, r in e["votes"]]
                    elo.update_from_override(votes, "__REJECTED__")
                    e["resolved"] = True
                    e["feedback"] = "rejected"
                    _save(entries)
                    return {"resolved": True, "entry_id": e["id"], "feedback": "rejected"}
            return {"resolved": False, "error": "Entry not found"}
    elif emoji in AB_EMOJI:
        return _resolve_ab(message_id, AB_EMOJI[emoji])
    elif emoji in OVERRIDE_MAP:
        return resolve_feedback(message_id=message_id, correct_answer=OVERRIDE_MAP[emoji])
    else:
        return {"resolved": False, "error": f"Unknown emoji: {emoji}"}


def _resolve_ab(message_id: str, winner: str) -> dict:
    """Resolve A/B split — boost winning panel, penalize losing panel.
    
    winner: "A" (champion panel) or "B" (challenger panel)
    
    Looks up both tag=*-A and tag=*-B entries for this message.
    """
    with _lock:
        entries = _load()

        # Find A and B entries for this message
        a_entry = None
        b_entry = None
        for e in entries:
            if e.get("message_id") == message_id and not e.get("resolved"):
                tag = e.get("tag", "") or ""
                if tag.endswith("-A"):
                    a_entry = e
                elif tag.endswith("-B"):
                    b_entry = e

        # If we only have one entry, the A/B was logged in the same entry
        # (from scale() auto-logging). Look for any unresolved entry.
        if not a_entry and not b_entry:
            for e in entries:
                if e.get("message_id") == message_id and not e.get("resolved"):
                    a_entry = e
                    break

        resolved_ids = []

        if a_entry:
            a_votes = [(m, a, r) for m, a, r in a_entry["votes"]]
            if winner == "A":
                elo.update_from_override(a_votes, a_entry["answer"].strip().upper())
                a_entry["feedback"] = "ab_winner"
            else:
                # A lost — penalize A models
                elo.update_from_override(a_votes, "__AB_LOSER__")
                a_entry["feedback"] = "ab_loser"
            a_entry["resolved"] = True
            resolved_ids.append(a_entry["id"])

        if b_entry:
            b_votes = [(m, a, r) for m, a, r in b_entry["votes"]]
            if winner == "B":
                elo.update_from_override(b_votes, b_entry["answer"].strip().upper())
                b_entry["feedback"] = "ab_winner"
            else:
                elo.update_from_override(b_votes, "__AB_LOSER__")
                b_entry["feedback"] = "ab_loser"
            b_entry["resolved"] = True
            resolved_ids.append(b_entry["id"])

        if not resolved_ids:
            return {"resolved": False, "error": "No A/B entries found for this message"}

        _save(entries)
        return {
            "resolved": True,
            "winner": winner,
            "resolved_ids": resolved_ids,
            "feedback": f"ab_winner={winner}",
        }


def pending(limit: int = 10) -> list:
    """List recent unresolved feedback entries."""
    entries = _load()
    unresolved = [e for e in entries if not e.get("resolved")]
    return unresolved[-limit:]


def stats() -> dict:
    """Feedback stats."""
    entries = _load()
    total = len(entries)
    resolved = sum(1 for e in entries if e.get("resolved"))
    confirmed = sum(1 for e in entries if e.get("feedback") == "confirmed")
    overridden = sum(1 for e in entries if (e.get("feedback") or "").startswith("override:"))
    rejected = sum(1 for e in entries if e.get("feedback") == "rejected")
    
    return {
        "total": total,
        "resolved": resolved,
        "unresolved": total - resolved,
        "confirmed": confirmed,
        "overridden": overridden,
        "rejected": rejected,
    }
