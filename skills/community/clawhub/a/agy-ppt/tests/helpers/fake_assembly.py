#!/usr/bin/env python3
"""Deterministic fake PPTX assembly step for Phase 9 fault injection.

Mirrors the *contract* of ``scripts/assemble_ppt.py`` (read the qa_passed slide
images, write one deck file) without importing ``python-pptx`` and without ever
regenerating, rewriting or deleting a slide image. On failure it writes nothing,
so a failed assembly can never leave a half-written deck behind.

The number of leading failures is scriptable via ``fail_times``, which is how
"assembly failed once, then was fixed" is simulated without touching production
code.
"""

from __future__ import annotations

import hashlib
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

RESULT_SCHEMA = "agy-ppt/fake-assembly-result/1"

STATUS_COMPLETED = "completed"
STATUS_ERROR = "error"

ERROR_ASSEMBLY_FAILED = "ASSEMBLY_FAILED"
ERROR_ASSEMBLY_INPUT_MISSING = "ASSEMBLY_INPUT_MISSING"

SLIDE_QA_PASSED = "qa_passed"
SLIDE_ASSEMBLED = "assembled"

# Not a real OOXML package; only used to prove a deck file was produced exactly
# once, by exactly one successful assembly run.
_FAKE_PPTX_PAYLOAD = b"PK\x03\x04fake-pptx-package\n"


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")


@dataclass
class AssemblyCall:
    attempt: int
    status: str
    error_code: str | None
    slides: list[str]
    image_digests: dict[str, str]


@dataclass
class FakeAssembly:
    """Scriptable assembly step. ``fail_times`` leading runs fail, then succeed."""

    workspace_root: Path
    output_name: str = "deck.pptx"
    fail_times: int = 0
    fail_error_code: str = ERROR_ASSEMBLY_FAILED
    calls: list[AssemblyCall] = field(default_factory=list)

    def __post_init__(self) -> None:
        self.workspace_root = Path(self.workspace_root)

    @property
    def call_count(self) -> int:
        return len(self.calls)

    @property
    def output_path(self) -> Path:
        return self.workspace_root / self.output_name

    def fix(self) -> None:
        """Simulate 'the assembly bug was fixed'."""
        self.fail_times = 0

    # -- the single assembly turn -----------------------------------------
    def run(self, state: Any) -> dict[str, Any]:
        """Assemble the deck from qa_passed slides. Never mutates ``state``."""
        attempt = len(self.calls) + 1
        slides = [
            slide_id
            for slide_id, slide in sorted(state.data["slides"].items())
            if slide.get("status") in (SLIDE_QA_PASSED, SLIDE_ASSEMBLED)
        ]
        digests: dict[str, str] = {}
        missing: list[str] = []
        for slide_id in slides:
            image_path = state.data["slides"][slide_id].get("image_path")
            resolved = (self.workspace_root / image_path) if image_path else None
            if resolved is None or not resolved.is_file() or resolved.stat().st_size == 0:
                missing.append(slide_id)
                continue
            digests[image_path] = hashlib.sha256(resolved.read_bytes()).hexdigest()

        if missing:
            return self._record(attempt, STATUS_ERROR, ERROR_ASSEMBLY_INPUT_MISSING, slides,
                                digests, detail={"missing_images": missing})

        if attempt <= self.fail_times:
            # Failure must leave the workspace exactly as it was: no deck file,
            # no touched slide image.
            return self._record(attempt, STATUS_ERROR, self.fail_error_code, slides, digests)

        self.output_path.parent.mkdir(parents=True, exist_ok=True)
        self.output_path.write_bytes(_FAKE_PPTX_PAYLOAD)
        return self._record(attempt, STATUS_COMPLETED, None, slides, digests)

    def _record(
        self,
        attempt: int,
        status: str,
        error_code: str | None,
        slides: list[str],
        digests: dict[str, str],
        detail: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        self.calls.append(AssemblyCall(attempt, status, error_code, slides, digests))
        result: dict[str, Any] = {
            "schema": RESULT_SCHEMA,
            "status": status,
            "control": "returned_to_agy",
            "next_step_owner": "AGY",
            "attempt": attempt,
            "slides": slides,
            "timestamp": _now_iso(),
        }
        if error_code is not None:
            result["error_code"] = error_code
            result["error_message"] = f"injected assembly fault {error_code} (attempt {attempt})"
        else:
            result["output_path"] = self.output_path.relative_to(self.workspace_root).as_posix()
        if detail:
            result.update(detail)
        return result
