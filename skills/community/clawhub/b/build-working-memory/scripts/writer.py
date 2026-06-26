"""Capture and persist layered working memory at session end.

Use this writer for deterministic file updates instead of ad hoc markdown edits.
It writes flat daily logs, updates thread/state/resumption files, and appends
structured events for later date-aware retrieval.

Typical usage:
    writer = MemoryWriter("./project-root")
    writer.note_thread_touched("thread-wm-design")
    writer.note_decision("Chose YAML over TOML for config", "Better multi-line support")
    writer.note_open_question("Should config be user-editable at runtime?")
    writer.note_event(
        "issue",
        "I had an issue with my car's GPS system on 3/22.",
        action="issue",
        object_hint="car gps system",
        normalized_date="2023-03-22",
    )
    writer.end_session(
        session_summary="Prototyped retrieval workflow and event capture.",
        resumption_note="Next session should test retrieval against real benchmark cases.",
        thread_updates={
            "thread-wm-design": {
                "current_position": "Event-aware retrieval is implemented; next step is evaluation.",
                "new_open_questions": ["How should counting-before-threshold questions be handled?"],
            }
        },
        mood="focused, building momentum",
    )
"""

import json
import re
from datetime import datetime, timezone
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional


@dataclass
class SessionCapture:
    """Accumulates observations during a session before writing."""
    decisions: list[dict] = field(default_factory=list)
    open_questions: list[str] = field(default_factory=list)
    patterns: list[str] = field(default_factory=list)
    emotional_notes: list[str] = field(default_factory=list)
    thread_refs: list[str] = field(default_factory=list)
    structured_events: list[dict] = field(default_factory=list)


class MemoryWriter:
    def __init__(self, root: str):
        self.root = Path(root)
        self.capture = SessionCapture()
        self.session_start = datetime.now(timezone.utc)

    # -- Mid-Session Capture -------------------------------------------------

    def note_decision(self, decision: str, reasoning: str):
        self.capture.decisions.append({
            "decision": decision,
            "reasoning": reasoning,
        })

    def note_open_question(self, question: str):
        self.capture.open_questions.append(question)

    def note_pattern(self, pattern: str):
        self.capture.patterns.append(pattern)

    def note_emotional_tone(self, note: str):
        self.capture.emotional_notes.append(note)

    def note_thread_touched(self, thread_id: str):
        if thread_id not in self.capture.thread_refs:
            self.capture.thread_refs.append(thread_id)

    def note_event(
        self,
        event_type: str,
        text: str,
        action: str = "generic",
        object_hint: Optional[str] = None,
        normalized_date: Optional[str] = None,
        relative_time: Optional[str] = None,
        session_id: Optional[str] = None,
        timestamp: Optional[str] = None,
    ):
        self.capture.structured_events.append({
            "event_type": event_type,
            "action": action,
            "object_hint": object_hint,
            "text": text,
            "normalized_date": normalized_date,
            "relative_time": relative_time,
            "session_id": session_id,
            "timestamp": timestamp,
            "has_explicit_date": bool(normalized_date),
            "has_relative_time": bool(relative_time),
        })

    # -- End of Session Writes -----------------------------------------------

    def end_session(
        self,
        session_summary: str,
        resumption_note: str,
        thread_updates: Optional[dict] = None,
        mood: str = "",
        session_events: Optional[str] = None,
    ):
        """
        Persist all session memory. Call this at the end of every session.

        Args:
            session_summary: High-level summary of what happened
            resumption_note: First-person handoff for next session
            thread_updates: Dict of thread_id -> update fields
            mood: Tonal/emotional observation
            session_events: Detailed account of what happened (optional,
                            if more granularity is needed than the summary)
        """
        now = datetime.now(timezone.utc)
        today = now.strftime("%Y-%m-%d")
        duration = int((now - self.session_start).total_seconds() / 60)

        # 1. Write daily log
        self._write_daily_log(today, now, duration, session_summary, session_events, mood)

        # 2. Update threads
        if thread_updates:
            self._update_threads(thread_updates)

        # 3. Append structured events
        self._append_events()

        # 4. Update state.json
        self._update_state(now, today, duration)

        # 5. Write resumption note
        self._write_resumption(resumption_note, today)

        # 6. Check if memory review is due
        self._check_maintenance_flags()

    def _write_daily_log(
        self, today: str, now: datetime, duration: int,
        summary: str, events: Optional[str], mood: str,
    ):
        """Write or append to today's daily log."""
        memory_dir = self.root / "memory"
        memory_dir.mkdir(parents=True, exist_ok=True)
        log_path = memory_dir / f"{today}.md"

        threads_str = ", ".join(self.capture.thread_refs) if self.capture.thread_refs else "—"

        sections = []

        # Header (only if new file)
        if not log_path.exists():
            sections.append(f"# Daily Log — {today}\n")

        sections.append(
            f"> Session: {now.strftime('%H:%M')} UTC, ~{duration} min\n"
            f"> Thread(s) active: {threads_str}\n"
        )

        # Summary
        sections.append(f"## Session Summary\n\n{summary}\n")

        # Detailed events (optional)
        if events:
            sections.append(f"## What Happened\n\n{events}\n")

        # Decisions
        if self.capture.decisions:
            rows = ["| Decision | Reasoning | Ref |", "|----------|-----------|-----|"]
            for d in self.capture.decisions:
                ref = ", ".join(self.capture.thread_refs) if self.capture.thread_refs else "—"
                rows.append(f"| {d['decision']} | {d['reasoning']} | {ref} |")
            sections.append(f"## Decisions\n\n" + "\n".join(rows) + "\n")

        # Open questions
        if self.capture.open_questions:
            qs = "\n".join(f"- {q}" for q in self.capture.open_questions)
            sections.append(f"## Open Questions (New This Session)\n\n{qs}\n")

        # Patterns
        if self.capture.patterns:
            ps = "\n".join(f"- {p}" for p in self.capture.patterns)
            sections.append(f"## Patterns Noticed\n\n{ps}\n")

        # Emotional/tonal notes
        tonal = self.capture.emotional_notes + ([mood] if mood else [])
        if tonal:
            sections.append(f"## Emotional/Tonal Notes\n\n" + "\n".join(tonal) + "\n")

        # Write
        content = "\n---\n\n".join(sections)
        mode = "a" if log_path.exists() else "w"
        with open(log_path, mode, encoding="utf-8") as f:
            if mode == "a":
                f.write("\n\n---\n\n")  # separator between sessions on same day
            f.write(content)

    def _update_threads(self, updates: dict):
        """Update thread entries in threads.md."""
        threads_path = self.root / "memory" / "threads.md"
        if not threads_path.exists():
            return

        text = threads_path.read_text(encoding="utf-8")

        for thread_id, changes in updates.items():
            # Update "Current Position"
            if "current_position" in changes:
                pattern = (
                    rf"(- \*\*ID\*\*: {re.escape(thread_id)}.*?"
                    r"### Current Position\n)(.*?)(\n### )"
                )
                replacement = rf"\g<1>{changes['current_position']}\n\3"
                text = re.sub(pattern, replacement, text, flags=re.DOTALL)

            # Update "Last touched"
            today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
            text = re.sub(
                rf"(- \*\*ID\*\*: {re.escape(thread_id)}.*?- \*\*Last touched\*\*: )\d{{4}}-\d{{2}}-\d{{2}}",
                rf"\g<1>{today}",
                text,
                flags=re.DOTALL,
            )

            # Add new open questions
            if "new_open_questions" in changes:
                for q in changes["new_open_questions"]:
                    # Find the Open Questions section for this thread
                    oq_pattern = (
                        rf"(- \*\*ID\*\*: {re.escape(thread_id)}.*?"
                        r"### Open Questions\n)(.*?)(\n### |\n## |\n# )"
                    )
                    match = re.search(oq_pattern, text, re.DOTALL)
                    if match:
                        existing = match.group(2)
                        new_entry = f"- [ ] {q}\n"
                        text = text[:match.start(2)] + existing + new_entry + text[match.end(2):]

            # Close (check off) questions
            if "closed_questions" in changes:
                for q in changes["closed_questions"]:
                    escaped = re.escape(q)
                    text = re.sub(
                        rf"- \[ \] {escaped}",
                        f"- [x] {q}",
                        text,
                    )

        threads_path.write_text(text, encoding="utf-8")

    def _append_events(self):
        """Append structured events to memory/events.json if any were captured."""
        if not self.capture.structured_events:
            return
        events_path = self.root / "memory" / "events.json"
        if events_path.exists():
            try:
                payload = json.loads(events_path.read_text(encoding="utf-8"))
            except Exception:
                payload = {"events": []}
        else:
            payload = {"events": []}
        existing = payload.get("events", [])
        existing.extend(self.capture.structured_events)
        payload["events"] = existing
        events_path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    def _update_state(self, now: datetime, today: str, duration: int):
        """Update state.json with current session info."""
        state_path = self.root / "memory" / "state.json"
        if state_path.exists():
            state = json.loads(state_path.read_text(encoding="utf-8"))
        else:
            state = {}

        # Update last session
        state["last_session"] = {
            "timestamp": now.isoformat().replace("+00:00", "Z"),
            "duration_minutes": duration,
            "daily_log": f"memory/{today}.md",
        }

        # Increment counters
        counters = state.get("session_counter", {"total": 0, "this_week": 0, "since_last_memory_review": 0})
        counters["total"] = counters.get("total", 0) + 1
        counters["since_last_memory_review"] = counters.get("since_last_memory_review", 0) + 1
        state["session_counter"] = counters

        # Update active threads with touch timestamps
        for thread in state.get("active_threads", []):
            if thread["id"] in self.capture.thread_refs:
                thread["last_touched"] = today

        # Update pending questions
        existing_qs = state.get("pending_questions", [])
        new_qs = [q for q in self.capture.open_questions if q not in existing_qs]
        state["pending_questions"] = existing_qs + new_qs

        state_path.write_text(
            json.dumps(state, indent=2, ensure_ascii=False),
            encoding="utf-8",
        )

    def _write_resumption(self, note: str, today: str):
        """Overwrite resumption.md with the new handoff note."""
        path = self.root / "memory" / "resumption.md"
        content = f"# Resumption Note\n\n> Written: {today}, end of session\n> For: my next session self\n\n---\n\n{note}\n"
        path.write_text(content, encoding="utf-8")

    def _check_maintenance_flags(self):
        """Set flags if maintenance is due."""
        state_path = self.root / "memory" / "state.json"
        if not state_path.exists():
            return

        state = json.loads(state_path.read_text(encoding="utf-8"))
        flags = state.get("flags", {})

        # Memory review due every 5 sessions
        if state.get("session_counter", {}).get("since_last_memory_review", 0) >= 5:
            flags["memory_review_due"] = True

        # Check for archive candidates (entries in Fading for 20+ sessions)
        # Simplified: just set the flag if fading entries exist
        memory_text = self._read_file("MEMORY.md")
        if "## Fading" in memory_text and memory_text.split("## Fading")[1].strip():
            flags["archive_candidates_exist"] = True

        state["flags"] = flags
        state_path.write_text(json.dumps(state, indent=2, ensure_ascii=False), encoding="utf-8")

    def _read_file(self, relative_path: str) -> str:
        full = self.root / relative_path
        return full.read_text(encoding="utf-8") if full.exists() else ""


# ---------------------------------------------------------------------------
# CLI smoke test
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    import sys

    root = sys.argv[1] if len(sys.argv) > 1 else "."
    writer = MemoryWriter(root)

    writer.note_decision(
        "Implemented four-phase retrieval",
        "Balances cost vs. completeness; 80% of sessions should stay in Phases 1-3"
    )
    writer.note_open_question("How to handle concurrent sessions?")
    writer.note_pattern("Testing by trying to break the schema before approving")
    writer.note_thread_touched("thread-wm-design")
    writer.note_event(
        "issue",
        "I had an issue with my car's GPS system on 3/22.",
        action="issue",
        object_hint="car gps system",
        normalized_date="2023-03-22",
    )

    writer.end_session(
        session_summary="Built the retrieval workflow and event-aware memory capture.",
        resumption_note="Retrieval workflow is prototyped. Next: test it with real data.",
        thread_updates={
            "thread-wm-design": {
                "current_position": "Retrieval workflow prototyped. Moving to integration testing.",
            }
        },
        mood="productive, momentum building",
    )
    print("Session ended. Files and event ledger updated.")
