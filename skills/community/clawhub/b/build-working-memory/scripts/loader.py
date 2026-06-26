"""Load budget-aware working-memory context for a new session.

This loader implements phased retrieval over the layered memory system:
- fast orientation (`state.json`)
- continuity anchor (`resumption.md`)
- contextual memory (`MEMORY.md`, `threads.md`, recent daily logs)
- optional deep recall helpers (`archive.md`, `events.json`)

Usage:
    loader = MemoryLoader("./project-root")
    context = loader.load_session_context(user_message="Which happened first, X or Y?")
    print(context.text)
    print(context.metadata)

Use `phase_4_event_lookup()` when the question is event- or date-sensitive and
structured events should supplement ordinary file retrieval.
"""

import json
import re
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional


# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

@dataclass
class BudgetConfig:
    """Token budget allocation (approximate, based on ~4 chars per token)."""
    total_memory_cap: int = 5000
    phase_1_2_reserve: int = 500
    phase_3_cap: int = 2500
    phase_4_cap: int = 3000
    phase_4_per_retrieval: int = 2000
    chars_per_token: int = 4  # rough estimate for budget tracking


@dataclass
class TimeGapStrategy:
    """Loading strategy thresholds based on hours since last session."""
    light: float = 2.0          # < 2h: skip Phase 3
    standard: float = 24.0      # 2-24h: normal Phases 1-3
    full_reload: float = 168.0  # 1-7 days: preload recent daily logs
    # > 168h (7 days): deep reload, treat resumption as potentially stale


# ---------------------------------------------------------------------------
# Data structures
# ---------------------------------------------------------------------------

@dataclass
class LoadedContent:
    """A single piece of loaded memory with its source and cost."""
    source: str          # file path or identifier
    section: str         # which part of the file (or "full")
    text: str
    token_estimate: int
    phase: int           # which retrieval phase loaded this


@dataclass
class SessionContext:
    """The assembled memory context ready for injection into a system prompt."""
    contents: list[LoadedContent] = field(default_factory=list)
    total_tokens: int = 0
    metadata: dict = field(default_factory=dict)

    @property
    def text(self) -> str:
        """Concatenate all loaded content into a single memory block."""
        parts = []
        for c in self.contents:
            parts.append(f"<!-- source: {c.source} ({c.section}) -->\n{c.text}")
        return "\n\n---\n\n".join(parts)

    def add(self, content: LoadedContent, budget: BudgetConfig) -> bool:
        """Add content if within budget. Returns False if budget exceeded."""
        if self.total_tokens + content.token_estimate > budget.total_memory_cap:
            return False
        self.contents.append(content)
        self.total_tokens += content.token_estimate
        return True


# ---------------------------------------------------------------------------
# Loader
# ---------------------------------------------------------------------------

class MemoryLoader:
    def __init__(self, root: str, budget: Optional[BudgetConfig] = None):
        self.root = Path(root)
        self.budget = budget or BudgetConfig()
        self.time_gaps = TimeGapStrategy()

    # -- Helpers -------------------------------------------------------------

    def _estimate_tokens(self, text: str) -> int:
        return len(text) // self.budget.chars_per_token

    def _read(self, relative_path: str) -> str:
        full = self.root / relative_path
        if not full.exists():
            return ""
        return full.read_text(encoding="utf-8")

    def _load(self, path: str, section: str, text: str, phase: int) -> LoadedContent:
        return LoadedContent(
            source=path,
            section=section,
            text=text,
            token_estimate=self._estimate_tokens(text),
            phase=phase,
        )

    def _hours_since_last_session(self, state: dict) -> float:
        ts = state.get("last_session", {}).get("timestamp")
        if not ts:
            return float("inf")
        last = datetime.fromisoformat(ts.replace("Z", "+00:00"))
        now = datetime.now(timezone.utc)
        return (now - last).total_seconds() / 3600

    # -- Phase 1: Orient -----------------------------------------------------

    def phase_1_orient(self) -> tuple[dict, dict]:
        """Read state.json, return (state_dict, decisions)."""
        raw = self._read("memory/state.json")
        if not raw:
            return {}, {"time_gap": float("inf"), "strategy": "full_reload"}

        state = json.loads(raw)
        gap = self._hours_since_last_session(state)

        if gap < self.time_gaps.light:
            strategy = "light"
        elif gap < self.time_gaps.standard:
            strategy = "standard"
        elif gap < self.time_gaps.full_reload:
            strategy = "full_reload"
        else:
            strategy = "deep_reload"

        decisions = {
            "time_gap_hours": round(gap, 1),
            "strategy": strategy,
            "active_thread_ids": [
                t["id"] for t in state.get("active_threads", [])
            ],
            "flags": state.get("flags", {}),
            "style_hint": state.get("context_hints", {}).get("conversation_style"),
        }
        return state, decisions

    # -- Phase 2: Anchor -----------------------------------------------------

    def phase_2_anchor(self, decisions: dict) -> LoadedContent:
        """Read resumption.md as the subjective continuity bridge."""
        text = self._read("memory/resumption.md")
        if decisions["strategy"] == "deep_reload":
            # Mark as potentially stale
            text = (
                "<!-- NOTE: 7+ days since last session. "
                "This resumption note may be stale. -->\n\n" + text
            )
        return self._load("memory/resumption.md", "full", text, phase=2)

    # -- Phase 3: Context ----------------------------------------------------

    def phase_3_context(
        self,
        decisions: dict,
        user_message: Optional[str] = None,
    ) -> list[LoadedContent]:
        """Load MEMORY.md and threads based on context signals."""
        results = []

        # Determine branch
        branch = self._classify_branch(decisions, user_message)
        decisions["phase_3_branch"] = branch

        if branch == "continue_thread":
            thread_id = self._match_thread(decisions, user_message)
            if thread_id:
                thread_text = self._extract_thread(thread_id)
                if thread_text:
                    results.append(self._load(
                        "memory/threads.md", f"thread:{thread_id}",
                        thread_text, phase=3
                    ))
            # Load only relevant MEMORY.md section
            memory_section = self._extract_memory_section("About This Project")
            if memory_section:
                results.append(self._load(
                    "MEMORY.md", "About This Project", memory_section, phase=3
                ))

        elif branch == "new_or_ambiguous":
            # Load full MEMORY.md (Active + Fading)
            memory_text = self._read("MEMORY.md")
            results.append(self._load("MEMORY.md", "full", memory_text, phase=3))
            # Load thread headers only
            headers = self._extract_thread_headers()
            if headers:
                results.append(self._load(
                    "memory/threads.md", "headers_only", headers, phase=3
                ))

        elif branch == "maintenance":
            memory_text = self._read("MEMORY.md")
            results.append(self._load("MEMORY.md", "full", memory_text, phase=3))
            # Load recent daily log summaries
            for log_content in self._recent_daily_summaries(count=5):
                results.append(log_content)

        # For full_reload and deep_reload, also preload recent daily logs
        if decisions["strategy"] in ("full_reload", "deep_reload"):
            for log_content in self._recent_daily_summaries(count=3):
                if not any(r.source == log_content.source for r in results):
                    results.append(log_content)

        return results

    def _classify_branch(self, decisions: dict, message: Optional[str]) -> str:
        """Determine which Phase 3 branch to take."""
        if decisions["flags"].get("memory_review_due"):
            return "maintenance"
        if message and self._message_matches_thread(message, decisions):
            return "continue_thread"
        return "new_or_ambiguous"

    def _message_matches_thread(self, message: str, decisions: dict) -> bool:
        """Simple heuristic: does the message reference an active thread?"""
        msg_lower = message.lower()
        # Check against active thread titles from state
        for tid in decisions.get("active_thread_ids", []):
            # Extract keywords from thread ID
            keywords = tid.replace("thread-", "").replace("-", " ").split()
            if any(kw in msg_lower for kw in keywords):
                return True
        # Check for continuation signals
        continuation_signals = [
            "continue", "let's keep going", "where were we",
            "pick up", "back to", "as we discussed", "next step",
        ]
        return any(signal in msg_lower for signal in continuation_signals)

    def _match_thread(self, decisions: dict, message: Optional[str]) -> Optional[str]:
        """Return the best-matching thread ID."""
        if not message:
            # Default to primary active thread
            threads = decisions.get("active_thread_ids", [])
            return threads[0] if threads else None
        msg_lower = message.lower()
        for tid in decisions.get("active_thread_ids", []):
            keywords = tid.replace("thread-", "").replace("-", " ").split()
            if any(kw in msg_lower for kw in keywords):
                return tid
        # Default to first active
        threads = decisions.get("active_thread_ids", [])
        return threads[0] if threads else None

    def _extract_thread(self, thread_id: str) -> Optional[str]:
        """Extract a single thread's full content from threads.md."""
        text = self._read("memory/threads.md")
        if not text:
            return None
        # Find thread by ID marker
        pattern = rf"(## Thread:.*?\n- \*\*ID\*\*: {re.escape(thread_id)}.*?)(?=\n## |\n# |$)"
        match = re.search(pattern, text, re.DOTALL)
        return match.group(1).strip() if match else None

    def _extract_thread_headers(self) -> str:
        """Extract just the title + status + current position of each thread."""
        text = self._read("memory/threads.md")
        if not text:
            return ""
        headers = []
        current_header = []
        in_header = False
        for line in text.split("\n"):
            if line.startswith("## Thread:"):
                if current_header:
                    headers.append("\n".join(current_header))
                current_header = [line]
                in_header = True
            elif in_header:
                if line.startswith("### Current Position"):
                    current_header.append(line)
                    # Grab the next non-empty line as position summary
                    continue
                elif line.startswith("- **ID**:") or line.startswith("- **Status**:"):
                    current_header.append(line)
                elif line.startswith("###") and "Current Position" not in line:
                    # End of header zone
                    in_header = False
                    headers.append("\n".join(current_header))
                    current_header = []
                elif current_header and "Current Position" in current_header[-1]:
                    current_header.append(line)
        if current_header:
            headers.append("\n".join(current_header))
        return "\n\n".join(headers)

    def _extract_memory_section(self, heading: str) -> Optional[str]:
        """Extract a specific section from MEMORY.md by heading."""
        text = self._read("MEMORY.md")
        if not text:
            return None
        pattern = rf"(### {re.escape(heading)}.*?)(?=\n### |\n## |\n---|\Z)"
        match = re.search(pattern, text, re.DOTALL)
        return match.group(1).strip() if match else None

    def _recent_daily_summaries(self, count: int = 5) -> list[LoadedContent]:
        """Load summary sections from the most recent daily logs.

        Canonical location is flat ``memory/YYYY-MM-DD.md``.  Only falls back to
        ``memory/daily/`` when the flat directory contains no date-named logs.
        """
        memory_dir = self.root / "memory"
        flat_logs = sorted(memory_dir.glob("[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9].md"), reverse=True)
        if flat_logs:
            logs = flat_logs[:count]
        else:
            legacy_dir = memory_dir / "daily"
            logs = sorted(legacy_dir.glob("[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9].md"), reverse=True)[:count] if legacy_dir.exists() else []
        results = []
        for log_path in logs:
            text = log_path.read_text(encoding="utf-8")
            summary = self._extract_log_sections(text, ["Session Summary", "Decisions"])
            if summary:
                rel = f"memory/{log_path.name}"
                results.append(self._load(rel, "summary+decisions", summary, phase=3))
        return results

    @staticmethod
    def _extract_log_sections(text: str, headings: list[str]) -> str:
        """Extract specific ## sections from a daily log."""
        sections = []
        for heading in headings:
            pattern = rf"(## {re.escape(heading)}.*?)(?=\n## |\Z)"
            match = re.search(pattern, text, re.DOTALL)
            if match:
                sections.append(match.group(1).strip())
        return "\n\n".join(sections)

    # -- Phase 4: Deep Recall ------------------------------------------------

    def phase_4_targeted_lookup(self, daily_log_ref: str, section: Optional[str] = None) -> Optional[LoadedContent]:
        """Load a specific daily log or section of it."""
        text = self._read(daily_log_ref)
        if not text:
            return None
        if section:
            extracted = self._extract_log_sections(text, [section])
            return self._load(daily_log_ref, section, extracted, phase=4) if extracted else None
        return self._load(daily_log_ref, "full", text, phase=4)

    def phase_4_index_search(self, query: str) -> list[str]:
        """Search the index for daily logs matching a query. Returns log paths."""
        index_text = self._read("memory/index.md")
        if not index_text:
            # Fall back to scanning filenames
            return self._scan_daily_logs_by_filename(query)
        matches = []
        for line in index_text.split("\n"):
            if "|" in line and query.lower() in line.lower():
                # Extract date from the table row
                parts = [p.strip() for p in line.split("|")]
                if len(parts) > 1 and re.match(r"\d{4}-\d{2}-\d{2}", parts[1]):
                    matches.append(f"memory/{parts[1]}.md")
        return matches

    def phase_4_archive_recovery(self, topic: str) -> Optional[LoadedContent]:
        """Search archive for a topic and return matching entry."""
        text = self._read("memory/archive.md")
        if not text or topic.lower() not in text.lower():
            return None
        return self._load("memory/archive.md", f"search:{topic}", text, phase=4)

    # Common words to skip when matching event queries
    _STOP_WORDS = frozenset(
        "a an the is was were are been be have has had do does did will would "
        "shall should can could may might must need dare let get got its it "
        "for of on in to at by with from and or but not no nor so yet both "
        "each every all any few more most other some such than too very also "
        "just about after before between during into through over under above "
        "what when where which who whom how that this these those my your his "
        "her our their its me him us them i you he she we they who whom whose "
        "happen happened happens did went going".split()
    )

    def phase_4_event_lookup(self, query: str, max_results: int = 12) -> Optional[LoadedContent]:
        """Load structured events matching a query for date-sensitive recall.

        Uses entity-level matching: extracts meaningful tokens from the query
        (skipping stop words and short tokens), then scores events by how many
        query entities appear in the event text or object_hint.
        """
        raw = self._read("memory/events.json")
        if not raw:
            return None
        try:
            payload = json.loads(raw)
        except Exception:
            return None
        events = payload.get("events", [])
        if not events:
            return None

        # Extract meaningful query tokens
        q_tokens = {
            tok for tok in re.findall(r"[a-z0-9]+", query.lower())
            if len(tok) > 2 and tok not in self._STOP_WORDS
        }
        if not q_tokens:
            return None

        # Score events by token overlap
        scored = []
        for ev in events:
            hay = ((ev.get("text") or "") + " " + (ev.get("object_hint") or "")).lower()
            hits = sum(1 for tok in q_tokens if tok in hay)
            if hits > 0:
                # Boost events with normalized dates (more useful for temporal queries)
                date_boost = 1 if ev.get("normalized_date") else 0
                scored.append((hits + date_boost, ev))

        if not scored:
            return None

        scored.sort(key=lambda x: x[0], reverse=True)
        matched = [ev for _, ev in scored[:max_results]]

        lines = ["# Structured Events", ""]
        for ev in matched:
            date_str = ev.get("normalized_date") or ev.get("relative_time") or "unknown"
            lines.append(
                f"- [{ev.get('event_type', '?')}/{ev.get('action', '?')}] "
                f"{ev.get('text', '')} "
                f"(object={ev.get('object_hint', '?')}, date={date_str})"
            )
        return self._load("memory/events.json", f"query:{query}", "\n".join(lines), phase=4)

    def _scan_daily_logs_by_filename(self, query: str) -> list[str]:
        """Fallback: return recent logs when no index is available.

        Scans canonical flat ``memory/`` first, falls back to ``memory/daily/``.
        """
        memory_dir = self.root / "memory"
        date_glob = "[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9].md"
        flat_logs = sorted(memory_dir.glob(date_glob), reverse=True)
        if flat_logs:
            return [f"memory/{p.name}" for p in flat_logs[:10]]
        legacy_dir = memory_dir / "daily"
        if legacy_dir.exists():
            return [f"memory/{p.name}" for p in sorted(legacy_dir.glob(date_glob), reverse=True)[:10]]
        return []

    # -- Orchestrator --------------------------------------------------------

    def load_session_context(
        self,
        user_message: Optional[str] = None,
    ) -> SessionContext:
        """
        Main entry point. Runs the retrieval workflow and returns
        assembled context ready for system prompt injection.
        """
        ctx = SessionContext()

        # Phase 1: Orient
        state, decisions = self.phase_1_orient()
        ctx.metadata["decisions"] = decisions

        # Phase 2: Anchor (always)
        anchor = self.phase_2_anchor(decisions)
        ctx.add(anchor, self.budget)

        # Phase 3: Context (conditional)
        if decisions["strategy"] != "light":
            phase_3_contents = self.phase_3_context(decisions, user_message)
            for content in phase_3_contents:
                if not ctx.add(content, self.budget):
                    ctx.metadata["budget_exceeded_at"] = content.source
                    break

        ctx.metadata["total_tokens"] = ctx.total_tokens
        ctx.metadata["sources_loaded"] = [c.source for c in ctx.contents]
        return ctx


# ---------------------------------------------------------------------------
# CLI smoke test
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    import sys

    root = sys.argv[1] if len(sys.argv) > 1 else "."
    message = sys.argv[2] if len(sys.argv) > 2 else None

    loader = MemoryLoader(root)
    context = loader.load_session_context(user_message=message)

    print("=== Loading Decisions ===")
    print(json.dumps(context.metadata, indent=2))
    print(f"\n=== Loaded {len(context.contents)} sources, ~{context.total_tokens} tokens ===")
    for c in context.contents:
        print(f"  Phase {c.phase}: {c.source} ({c.section}) — ~{c.token_estimate} tokens")
    print(f"\n=== Memory Block ({len(context.text)} chars) ===")
    print(context.text[:500] + "..." if len(context.text) > 500 else context.text)

    if message:
        event_lookup = loader.phase_4_event_lookup(message)
        if event_lookup:
            print("\n=== Phase 4 Event Lookup Preview ===")
            print(event_lookup.text[:500] + "..." if len(event_lookup.text) > 500 else event_lookup.text)
