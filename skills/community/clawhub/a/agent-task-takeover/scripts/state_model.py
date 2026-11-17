#!/usr/bin/env python3
"""Agent-neutral helpers for reconstructing task state from artifacts.

No store paths, tool names, or platform APIs are baked in. Callers supply
timestamps and filesystem facts, which keeps every decision testable with
synthetic fixtures on any machine. Python 3.8+ / stdlib only.
"""
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

UNKNOWN = "unknown"
STALE = "stale"
CURRENT = "current"

# A transcript older than this, relative to the newest task artifact, is not
# treated as usable evidence for the current state of the task.
DEFAULT_FRESHNESS_WINDOW = 3 * 24 * 3600
# Shared-store writes inside this window are only a hint, never a blocker.
DEFAULT_ACTIVE_WINDOW = 300


def classify_pipeline(source_mtime, deliverable_mtime, gate_ok=None):
    """Compare the newest source artifact with the newest deliverable.

    STALE means sources changed after the last export, or a validation gate
    failed: re-exporting is the likely missing action. CURRENT means the
    deliverable reflects the newest source. UNKNOWN means insufficient data.
    """
    if source_mtime is None or deliverable_mtime is None:
        return UNKNOWN
    if source_mtime > deliverable_mtime or gate_ok is False:
        return STALE
    return CURRENT


def reconstruct_needed(session_ref, session_mtime, artifact_mtime,
                       window=DEFAULT_FRESHNESS_WINDOW):
    """Decide whether transcript-based takeover is impossible or untrustworthy.

    A missing session, a session without activity, or a transcript plainly
    older than the newest task artifact all require artifact-based rebuilding.
    """
    if not session_ref or session_mtime is None:
        return True
    if artifact_mtime is None:
        return False
    return artifact_mtime - session_mtime > window


def needs_confirmation(session_mtime, artifact_mtime, now, candidate_count=1,
                       window=DEFAULT_FRESHNESS_WINDOW):
    """Guard against taking over the wrong or a stale session.

    Treat short names, numbers and relative phrases as ambiguous: multiple
    plausible candidates, an old session, or newer task artifacts all require
    an explicit confirmation of the takeover target.
    """
    if candidate_count > 1 or session_mtime is None:
        return True
    if artifact_mtime is not None and artifact_mtime - session_mtime > window:
        return True
    return (now - session_mtime) > window


def liveness_signal(store_mtime, session_mtime, artifact_mtime, now,
                    active_window=DEFAULT_ACTIVE_WINDOW):
    """Return (is_active, basis), preferring task artifacts over shared stores.

    Several sessions commonly share one store, so a recent store write does
    not prove that the target task is still being edited.
    """
    if artifact_mtime is not None:
        reference, basis = artifact_mtime, "artifacts"
    elif session_mtime is not None:
        reference, basis = session_mtime, "session"
    elif store_mtime is not None:
        reference, basis = store_mtime, "store"
    else:
        return (False, "no-evidence")
    return (0 <= now - reference <= active_window, basis)


def verify_claims(claims, exists, contains=None):
    """Check file claims from a handoff against the filesystem.

    claims: iterable of paths, or dicts with 'path' and an optional 'marker'
    used as a cheap content spot-check. Returns a list of conflicts; an
    unverified claim must be reported as unverified, never trusted.
    """
    conflicts = []
    for claim in claims:
        if isinstance(claim, dict):
            path, marker = claim.get("path"), claim.get("marker")
        else:
            path, marker = claim, None
        if not path:
            continue
        if not exists(path):
            conflicts.append({"path": path, "reason": "missing"})
            continue
        if marker and contains and not contains(path, marker):
            conflicts.append({"path": path, "reason": "marker-mismatch"})
    return conflicts


@dataclass
class TaskState:
    """Common shape for the takeover report, independent of any agent."""

    objective: str = ""
    session_ref: Optional[str] = None
    evidence: List[Dict[str, Any]] = field(default_factory=list)
    last_actions: List[Dict[str, Any]] = field(default_factory=list)
    pipeline: str = UNKNOWN
    deliverables: List[Dict[str, Any]] = field(default_factory=list)
    conflicts: List[Dict[str, Any]] = field(default_factory=list)
    decisions: List[str] = field(default_factory=list)
    blocked: List[str] = field(default_factory=list)
    next_moves: List[str] = field(default_factory=list)
    final_pointer: Optional[str] = None

    def report(self):
        """Render the fixed six-plus-one section takeover report skeleton."""
        def bullets(items):
            return "\n".join("- " + str(item) for item in items) or "- (none)"

        sections = [
            "## Objective",
            self.objective or "(unknown)",
            "",
            "## Evidence",
            bullets(
                "{kind} | {source} | {timestamp} | confidence={confidence}".format(
                    kind=e.get("kind", "?"),
                    source=e.get("source", "?"),
                    timestamp=e.get("timestamp", "?"),
                    confidence=e.get("confidence", "?"),
                )
                for e in self.evidence
            ),
            "",
            "## Timeline",
            bullets(
                "{timestamp}  {description}".format(
                    timestamp=a.get("timestamp", "?"),
                    description=a.get("description", "?"),
                )
                for a in self.last_actions
            ),
            "",
            "## Work State",
            "Pipeline: " + self.pipeline,
            "Decisions: " + (", ".join(self.decisions) or "(none)"),
            "Blocked: " + (", ".join(self.blocked) or "(none)"),
            "",
            "## Mismatches",
            bullets(
                "{path}: {reason}".format(
                    path=c.get("path", "?"), reason=c.get("reason", "?")
                )
                for c in self.conflicts
            ),
            "",
            "## Deliverables",
            bullets(
                "{path} ({role})".format(
                    path=d.get("path", "?"), role=d.get("role", "history")
                )
                for d in self.deliverables
            ),
            "Final: " + (self.final_pointer or "(unset)"),
            "",
            "## Next Move",
            bullets(self.next_moves),
        ]
        return "\n".join(sections)


def _self_check():
    """Exercise every helper on synthetic inputs; exit 0 when all hold."""
    checks = []
    checks.append(classify_pipeline(200, 100) == STALE)
    checks.append(classify_pipeline(100, 200) == CURRENT)
    checks.append(classify_pipeline(100, 200, gate_ok=False) == STALE)
    checks.append(classify_pipeline(None, 200) == UNKNOWN)
    checks.append(reconstruct_needed(None, None, None) is True)
    checks.append(reconstruct_needed("s1", 100, None) is False)
    checks.append(reconstruct_needed("s1", 100, 100 + DEFAULT_FRESHNESS_WINDOW + 1) is True)
    checks.append(needs_confirmation(100, None, 200, candidate_count=2) is True)
    checks.append(needs_confirmation(100, None, 200, candidate_count=1) is False)
    checks.append(liveness_signal(200, 100, None, now=250)[0] is True)
    checks.append(liveness_signal(200, 100, None, now=250 + DEFAULT_ACTIVE_WINDOW + 1)[0] is False)
    checks.append(verify_claims(
        [{"path": "/x", "marker": "ok"}],
        exists=lambda p: p == "/x",
        contains=lambda p, m: True,
    ) == [])
    checks.append(verify_claims(
        [{"path": "/x", "marker": "ok"}],
        exists=lambda p: p == "/x",
        contains=lambda p, m: False,
    )[0]["reason"] == "marker-mismatch")
    state = TaskState(objective="t", next_moves=["a"])
    report = state.report()
    checks.append(all(h in report for h in
                      ("## Objective", "## Evidence", "## Timeline",
                       "## Work State", "## Mismatches", "## Deliverables",
                       "## Next Move")))
    bad = [i for i, ok in enumerate(checks) if not ok]
    if bad:
        print("FAILED checks: " + ", ".join(str(i) for i in bad))
        return 1
    print("state_model self-check: {} checks passed".format(len(checks)))
    return 0


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1 and sys.argv[1] == "--self-check":
        raise SystemExit(_self_check())
    print(__doc__)
    print("This module is a library for scripts and agents. Run "
          "`python state_model.py --self-check` to verify it.")
    raise SystemExit(0)
