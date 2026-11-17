#!/usr/bin/env python3
"""Deterministic fake Codex image worker for Phase 9 fault injection.

The fake worker returns exactly the same result contract the real adapter
(``scripts/codex_image_adapter.py``) returns -- ``agy-ppt/codex-image-adapter-result/1``
-- so :meth:`project_state.ProjectState.record_worker_result` validates it the
same way it validates a real Codex result. It never spawns a process, never
imports ``subprocess``, never touches ``$CODEX_HOME``, and never reads an API
key, so it consumes no subscription quota.

What can be controlled per slide (:class:`SlidePlan`):

* ``fault``            -- which fault to inject (see the ``FAULT_*`` constants)
* ``succeed_on``       -- the generation number at which the fault clears
                          (``succeed_on=2`` -> generation 1 faults, 2 succeeds)
* ``create_artifact``  -- whether a *successful* turn writes an artifact at
                          ``output_path`` (set ``False`` to model "success was
                          reported but nothing landed on disk")
* ``fault_artifact``   -- whether a faulted / interrupted turn nevertheless
                          leaves an artifact at ``output_path`` (used by the
                          interrupted-generation scenario)
* ``ambiguous_count``  -- how many candidate artifacts a turn leaves behind
* ``invalid_artifact`` -- write a non-image payload instead of a raster image

Faults model the adapter's error contract:

===============================  ==========================================
``FAULT_NONE``                   completed result + valid artifact
``IMAGE_GENERATION_FAILED``      the render turn failed, no artifact
``IMAGE_BACKEND_UNAVAILABLE``    built-in ``image_gen`` not exposed
``IMAGE_ARTIFACT_AMBIGUOUS``     >=2 valid candidates, adapter refuses to guess
``IMAGE_OUTPUT_INVALID``         artifact produced but not a readable image
``CODEX_TIMEOUT``                the render turn exceeded its deadline
``interrupted``                  the worker process dies mid-turn (raises)
===============================  ==========================================

An ``interrupted`` plan raises :class:`FakeWorkerInterrupted` instead of
returning a result: that is the whole point of the interrupted-generation
scenario, because AGY never receives a result to record.
"""

from __future__ import annotations

import base64
import hashlib
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

RESULT_SCHEMA = "agy-ppt/codex-image-adapter-result/1"
BACKEND = "codex_builtin_imagegen"

STATUS_COMPLETED = "completed"
STATUS_ERROR = "error"

# ---------------------------------------------------------------------------
# Fault vocabulary
# ---------------------------------------------------------------------------
FAULT_NONE = "success"
FAULT_GENERATION_FAILED = "IMAGE_GENERATION_FAILED"
FAULT_BACKEND_UNAVAILABLE = "IMAGE_BACKEND_UNAVAILABLE"
FAULT_ARTIFACT_AMBIGUOUS = "IMAGE_ARTIFACT_AMBIGUOUS"
FAULT_ARTIFACT_NOT_FOUND = "IMAGE_ARTIFACT_NOT_FOUND"
FAULT_OUTPUT_INVALID = "IMAGE_OUTPUT_INVALID"
FAULT_TIMEOUT = "CODEX_TIMEOUT"
FAULT_INTERRUPTED = "interrupted"

FAULTS = (
    FAULT_NONE,
    FAULT_GENERATION_FAILED,
    FAULT_BACKEND_UNAVAILABLE,
    FAULT_ARTIFACT_AMBIGUOUS,
    FAULT_ARTIFACT_NOT_FOUND,
    FAULT_OUTPUT_INVALID,
    FAULT_TIMEOUT,
    FAULT_INTERRUPTED,
)

# Faults that surface as a structured error result (not an exception).
ERROR_FAULTS = frozenset(
    {
        FAULT_GENERATION_FAILED,
        FAULT_BACKEND_UNAVAILABLE,
        FAULT_ARTIFACT_AMBIGUOUS,
        FAULT_ARTIFACT_NOT_FOUND,
        FAULT_OUTPUT_INVALID,
        FAULT_TIMEOUT,
    }
)

# A real, minimal 1x1 PNG: `codex_image_adapter.sniff_image` accepts it.
_PNG_1X1 = base64.b64decode(
    "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAAC0lEQVR42mP8/x8AAwMCAO+ip1sAAAAASUVORK5CYII="
)
# Deliberately not an image: used for the IMAGE_OUTPUT_INVALID fault.
_NOT_AN_IMAGE = b"this is not a raster image, it is a truncated text blob\n"

DEFAULT_OUTPUT_DIR = "origin_image"
# Stands in for `$CODEX_HOME/generated_images/<thread_id>/` without touching a
# real Codex home. Lives inside the temporary workspace.
STAGING_DIR = ".fake_generated_images"


class FakeWorkerInterrupted(RuntimeError):
    """The fake worker 'process' died mid-turn; AGY never gets a result."""

    def __init__(self, slide_id: str, generation: int) -> None:
        super().__init__(f"fake worker interrupted during {slide_id} generation {generation}")
        self.slide_id = slide_id
        self.generation = generation


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")


@dataclass
class SlidePlan:
    """Scripted behaviour for one slide."""

    fault: str = FAULT_NONE
    succeed_on: int | None = None
    create_artifact: bool = True
    fault_artifact: bool = False
    ambiguous_count: int = 2
    invalid_artifact: bool = False
    output_dir: str = DEFAULT_OUTPUT_DIR

    def __post_init__(self) -> None:
        if self.fault not in FAULTS:
            raise ValueError(f"unknown fault: {self.fault!r}")
        if self.succeed_on is not None and self.succeed_on < 1:
            raise ValueError("succeed_on must be >= 1")

    def fault_for(self, generation: int) -> str:
        """Which fault applies to this generation number."""
        if self.fault == FAULT_NONE:
            return FAULT_NONE
        if self.succeed_on is not None and generation >= self.succeed_on:
            return FAULT_NONE
        return self.fault


@dataclass
class WorkerCall:
    slide_id: str
    generation: int
    operation: str
    fault: str
    status: str


@dataclass
class FakeImageWorker:
    """A scriptable stand-in for the AGY -> Codex image worker.

    ``plans`` maps ``slide_id`` -> :class:`SlidePlan`. Slides without a plan use
    ``default_plan`` (success by default).
    """

    workspace_root: Path
    plans: dict[str, SlidePlan] = field(default_factory=dict)
    default_plan: SlidePlan = field(default_factory=SlidePlan)
    calls: list[WorkerCall] = field(default_factory=list)

    def __post_init__(self) -> None:
        self.workspace_root = Path(self.workspace_root)

    # -- scripting ---------------------------------------------------------
    def set_plan(self, slide_id: str, **kwargs: Any) -> SlidePlan:
        plan = SlidePlan(**kwargs)
        self.plans[slide_id] = plan
        return plan

    def plan_for(self, slide_id: str) -> SlidePlan:
        return self.plans.get(slide_id, self.default_plan)

    def clear_fault(self, slide_id: str) -> None:
        """Simulate 'the backend came back' / 'the bug was fixed'."""
        self.plans[slide_id] = SlidePlan()

    def clear_all_faults(self) -> None:
        self.plans = {}
        self.default_plan = SlidePlan()

    # -- call bookkeeping --------------------------------------------------
    def calls_for(self, slide_id: str) -> list[WorkerCall]:
        return [c for c in self.calls if c.slide_id == slide_id]

    @property
    def call_count(self) -> int:
        return len(self.calls)

    # -- the single render turn -------------------------------------------
    def run(
        self,
        slide_id: str,
        generation: int,
        operation: str = "generate",
        output_path: str | None = None,
    ) -> dict[str, Any]:
        """Perform exactly one fake render turn and return a worker result."""
        plan = self.plan_for(slide_id)
        fault = plan.fault_for(generation)
        rel_output = output_path or f"{plan.output_dir}/{slide_id}.png"

        if fault == FAULT_INTERRUPTED:
            if plan.fault_artifact:
                # A crash *after* the artifact landed is a different recovery
                # case than a crash before it; both are scriptable.
                self._write_artifact(rel_output, invalid=plan.invalid_artifact)
            self.calls.append(
                WorkerCall(slide_id, generation, operation, fault, "interrupted")
            )
            raise FakeWorkerInterrupted(slide_id, generation)

        if fault == FAULT_NONE:
            if plan.create_artifact:
                self._write_artifact(rel_output, invalid=plan.invalid_artifact)
            self.calls.append(
                WorkerCall(slide_id, generation, operation, fault, STATUS_COMPLETED)
            )
            return self._completed(slide_id, operation, generation, rel_output)

        diagnostics_extra: dict[str, Any] = {}
        if plan.fault_artifact:
            # A faulted turn that still left something at the output path.
            self._write_artifact(rel_output, invalid=plan.invalid_artifact)
        if fault == FAULT_ARTIFACT_AMBIGUOUS:
            candidates = self._write_candidates(slide_id, generation, plan.ambiguous_count)
            diagnostics_extra["artifact_discovery"] = {
                "method": "before_after_diff",
                "candidates": candidates,
                "ambiguous": True,
            }
        elif fault == FAULT_OUTPUT_INVALID:
            # The real adapter validates the discovered artifact *before*
            # copying it to output_path, so the workspace output path stays
            # untouched. The rejected payload only exists in staging.
            rejected = self._write_staged(slide_id, generation, "rejected.png", _NOT_AN_IMAGE)
            diagnostics_extra["artifact_discovery"] = {
                "method": "before_after_diff",
                "candidates": [rejected],
                "ambiguous": False,
            }

        self.calls.append(WorkerCall(slide_id, generation, operation, fault, STATUS_ERROR))
        return self._error(slide_id, operation, generation, fault, diagnostics_extra)

    # -- result builders ---------------------------------------------------
    def _diagnostics(self, slide_id: str, generation: int, extra: dict[str, Any]) -> dict[str, Any]:
        diagnostics = {
            "auth": "chatgpt_cli_session",
            "api_fallback_used": False,
            "thread_id": f"fake-thread-{slide_id}-gen{generation}",
            "fake_worker": True,
        }
        diagnostics.update(extra)
        return diagnostics

    def _completed(
        self, slide_id: str, operation: str, generation: int, rel_output: str
    ) -> dict[str, Any]:
        return {
            "schema": RESULT_SCHEMA,
            "status": STATUS_COMPLETED,
            "control": "returned_to_agy",
            "next_step_owner": "AGY",
            "slide_id": slide_id,
            "operation": operation,
            "backend": BACKEND,
            "output_path": rel_output,
            "run_id": self._run_id(slide_id, generation),
            "timestamp": _now_iso(),
            "warnings": [],
            "diagnostics": self._diagnostics(slide_id, generation, {}),
        }

    def _error(
        self,
        slide_id: str,
        operation: str,
        generation: int,
        error_code: str,
        diagnostics_extra: dict[str, Any],
    ) -> dict[str, Any]:
        return {
            "schema": RESULT_SCHEMA,
            "status": STATUS_ERROR,
            "control": "returned_to_agy",
            "next_step_owner": "AGY",
            "slide_id": slide_id,
            "operation": operation,
            "backend": BACKEND,
            "error_code": error_code,
            "error_message": f"injected fault {error_code} for {slide_id}",
            "run_id": self._run_id(slide_id, generation),
            "timestamp": _now_iso(),
            "warnings": [],
            "diagnostics": self._diagnostics(slide_id, generation, diagnostics_extra),
        }

    def _run_id(self, slide_id: str, generation: int) -> str:
        return f"fake-{slide_id}-gen{generation}"

    # -- filesystem effects ------------------------------------------------
    def _write_artifact(self, rel_output: str, invalid: bool = False) -> Path:
        path = self.workspace_root / rel_output
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(_NOT_AN_IMAGE if invalid else _PNG_1X1)
        return path

    def _write_staged(self, slide_id: str, generation: int, name: str, payload: bytes) -> str:
        rel = f"{STAGING_DIR}/{slide_id}-gen{generation}/{name}"
        path = self.workspace_root / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(payload)
        return rel

    def _write_candidates(self, slide_id: str, generation: int, count: int) -> list[str]:
        candidates = []
        for index in range(max(2, count)):
            candidates.append(
                self._write_staged(slide_id, generation, f"candidate_{index}.png", _PNG_1X1)
            )
        return candidates


# ---------------------------------------------------------------------------
# Artifact inspection helpers (used by assertions)
# ---------------------------------------------------------------------------
def is_valid_png(path: Path) -> bool:
    try:
        return path.is_file() and path.read_bytes().startswith(b"\x89PNG\r\n\x1a\n")
    except OSError:
        return False


def digest_tree(root: Path, rel_dir: str = DEFAULT_OUTPUT_DIR) -> dict[str, str]:
    """Content digests for every file under ``root/rel_dir``.

    Used to prove that a later failure (assembly, another slide) never rewrote
    an already-approved slide image.
    """
    base = Path(root) / rel_dir
    digests: dict[str, str] = {}
    if not base.is_dir():
        return digests
    for path in sorted(base.rglob("*")):
        if path.is_file():
            digests[path.relative_to(root).as_posix()] = hashlib.sha256(
                path.read_bytes()
            ).hexdigest()
    return digests
