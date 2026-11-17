#!/usr/bin/env python3
"""AGY-owned deterministic project state for the agy-ppt workflow.

AGY is the only Orchestrator / Single Source of Decision. This module is pure,
deterministic infrastructure: it never makes presentation, outline, copy, or
visual-QA decisions, never calls a worker, never auto-advances a phase on a
guess, and never picks an image. It only records and validates the state that
AGY drives.

Relationship to the upstream codex-ppt state (deliberately additive, not a
second copy of the same data):

* ``prepare_slide_prompts.py`` still produces ``prompts/slide_XX.json`` (the
  full image prompt + input images) and ``slide_jobs.json`` (the upstream
  subagent dispatch/record ledger). Those remain the source of truth for the
  *prompt* and the *input images*.
* This module owns the *AGY control plane* the upstream lacks: the deck-level
  phase machine, the per-slide state machine, the generation counter, the
  attempt history, resume/recovery, idempotency, and worker-result validation.
* It references the same on-disk artifacts (``prompts/slide_XX.json`` as
  ``job_path`` and ``origin_image/slide_XX.png`` as ``image_path``) instead of
  duplicating prompt/image payloads.

State ownership is ``AGY only``. Workers return results; AGY records them here.
A Codex ``generated`` result never becomes ``qa_passed`` automatically — only
AGY can make the visual-QA transition.

First version is ``sequential_only``; parallel generation is intentionally out
of scope but the model does not preclude adding it later.
"""

from __future__ import annotations

import json
import os
import re
import tempfile
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable

SCHEMA_VERSION = "1"
CONTROLLER = "agy"
STATE_FILENAME = "project_state.json"

# ---------------------------------------------------------------------------
# Error contract
# ---------------------------------------------------------------------------
ERROR_PROJECT_STATE_INVALID = "PROJECT_STATE_INVALID"
ERROR_INVALID_STATE_TRANSITION = "INVALID_STATE_TRANSITION"
ERROR_WORKER_RESULT_INVALID = "WORKER_RESULT_INVALID"

# Worker-reported error code this policy layer acts on for the consecutive
# generic-failure retry limit (Phase 10.2). Only this specific, already-known
# error_code is in scope; nothing here infers quota from a returncode.
ERROR_IMAGE_GENERATION_FAILED = "IMAGE_GENERATION_FAILED"

# Worker error codes this layer understands and preserves (never swallows).
KNOWN_WORKER_ERROR_CODES = frozenset(
    {
        "ENGINEERING_WORKER_UNAVAILABLE",
        "ENGINEERING_AGENT_UNAVAILABLE",
        "ENGINEERING_AGENT_SCOPE_LOST",
        "IMAGE_BACKEND_UNAVAILABLE",
        "IMAGE_ARTIFACT_AMBIGUOUS",
        "IMAGE_ARTIFACT_NOT_FOUND",
        "IMAGE_GENERATION_FAILED",
        "IMAGE_OUTPUT_INVALID",
        "IMAGE_OUTPUT_PATH_CONFLICT",
        "CODEX_TIMEOUT",
        "CODEX_CLI_UNAVAILABLE",
        "CODEX_AUTH_UNAVAILABLE",
    }
)

# ---------------------------------------------------------------------------
# Phases
# ---------------------------------------------------------------------------
PHASE_INTAKE = "intake"
PHASE_OUTLINE = "outline"
PHASE_STYLE = "style"
PHASE_SAMPLE = "sample"
PHASE_SLIDE_GENERATION = "slide_generation"
PHASE_VISUAL_QA = "visual_qa"
PHASE_ASSEMBLY = "assembly"
PHASE_COMPLETE = "complete"
PHASE_BLOCKED = "blocked"

PHASES = (
    PHASE_INTAKE,
    PHASE_OUTLINE,
    PHASE_STYLE,
    PHASE_SAMPLE,
    PHASE_SLIDE_GENERATION,
    PHASE_VISUAL_QA,
    PHASE_ASSEMBLY,
    PHASE_COMPLETE,
    PHASE_BLOCKED,
)

# Legal forward phase transitions (excluding the universal `-> blocked`, and
# the resume-from-blocked path handled separately).
PHASE_TRANSITIONS: dict[str, frozenset[str]] = {
    PHASE_INTAKE: frozenset({PHASE_OUTLINE}),
    PHASE_OUTLINE: frozenset({PHASE_STYLE}),
    PHASE_STYLE: frozenset({PHASE_SAMPLE}),
    PHASE_SAMPLE: frozenset({PHASE_SLIDE_GENERATION}),
    PHASE_SLIDE_GENERATION: frozenset({PHASE_VISUAL_QA}),
    PHASE_VISUAL_QA: frozenset({PHASE_ASSEMBLY, PHASE_SLIDE_GENERATION}),
    PHASE_ASSEMBLY: frozenset({PHASE_COMPLETE}),
    PHASE_COMPLETE: frozenset(),
    PHASE_BLOCKED: frozenset(),
}

# ---------------------------------------------------------------------------
# Slide states
# ---------------------------------------------------------------------------
SLIDE_PLANNED = "planned"
SLIDE_READY = "ready"
SLIDE_GENERATING = "generating"
SLIDE_GENERATED = "generated"
SLIDE_QA_PASSED = "qa_passed"
SLIDE_QA_FAILED = "qa_failed"
SLIDE_GENERATION_FAILED = "generation_failed"
SLIDE_ASSEMBLED = "assembled"
SLIDE_BLOCKED = "blocked"

SLIDE_STATES = (
    SLIDE_PLANNED,
    SLIDE_READY,
    SLIDE_GENERATING,
    SLIDE_GENERATED,
    SLIDE_QA_PASSED,
    SLIDE_QA_FAILED,
    SLIDE_GENERATION_FAILED,
    SLIDE_ASSEMBLED,
    SLIDE_BLOCKED,
)

SLIDE_TRANSITIONS: dict[str, frozenset[str]] = {
    SLIDE_PLANNED: frozenset({SLIDE_READY}),
    SLIDE_READY: frozenset({SLIDE_GENERATING}),
    SLIDE_GENERATING: frozenset({SLIDE_GENERATED, SLIDE_GENERATION_FAILED}),
    SLIDE_GENERATED: frozenset({SLIDE_QA_PASSED, SLIDE_QA_FAILED}),
    SLIDE_QA_FAILED: frozenset({SLIDE_READY}),
    SLIDE_QA_PASSED: frozenset({SLIDE_ASSEMBLED}),
    SLIDE_GENERATION_FAILED: frozenset({SLIDE_READY}),
    SLIDE_ASSEMBLED: frozenset(),
    SLIDE_BLOCKED: frozenset(),
}

# Slide transitions that represent a visual-QA judgement. Only AGY may perform
# them; a worker recording must never drive these.
QA_JUDGEMENT_TRANSITIONS = frozenset({(SLIDE_GENERATED, SLIDE_QA_PASSED), (SLIDE_GENERATED, SLIDE_QA_FAILED)})

_SLIDE_ID_RE = re.compile(r"^slide_[0-9]{2,}$")
_PROJECT_ID_RE = re.compile(r"^[A-Za-z0-9._-]+$")


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")


# ---------------------------------------------------------------------------
# Exceptions
# ---------------------------------------------------------------------------
class ProjectStateError(Exception):
    """Base error carrying a stable error_code for AGY."""

    error_code = ERROR_PROJECT_STATE_INVALID

    def __init__(self, message: str, error_code: str | None = None) -> None:
        super().__init__(message)
        if error_code is not None:
            self.error_code = error_code


class ProjectStateInvalid(ProjectStateError):
    error_code = ERROR_PROJECT_STATE_INVALID


class InvalidStateTransition(ProjectStateError):
    error_code = ERROR_INVALID_STATE_TRANSITION


class WorkerResultInvalid(ProjectStateError):
    error_code = ERROR_WORKER_RESULT_INVALID


# ---------------------------------------------------------------------------
# Path safety
# ---------------------------------------------------------------------------
def _resolve_within(workspace_root: Path, value: str, label: str) -> Path:
    """Resolve ``value`` and ensure it stays inside ``workspace_root``."""
    root = Path(os.path.realpath(str(workspace_root)))
    raw = Path(os.path.expanduser(value))
    candidate = raw if raw.is_absolute() else root / raw
    resolved = Path(os.path.normpath(str(candidate)))
    check = resolved
    if not resolved.exists():
        parent_real = Path(os.path.realpath(str(resolved.parent)))
        check = parent_real / resolved.name
    else:
        check = Path(os.path.realpath(str(resolved)))
    if check != root and root not in check.parents:
        raise ProjectStateInvalid(f"{label} {value!r} resolves outside the workspace root")
    return resolved


def _atomic_write_json(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    body = json.dumps(data, ensure_ascii=False, indent=2) + "\n"
    fd, temp_name = tempfile.mkstemp(prefix=f".{path.name}.", suffix=".tmp", dir=path.parent)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as handle:
            handle.write(body)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temp_name, path)
    finally:
        if os.path.exists(temp_name):
            os.unlink(temp_name)


# ---------------------------------------------------------------------------
# Validation
# ---------------------------------------------------------------------------
def validate_state(state: Any) -> list[str]:
    """Return a list of human-readable validation errors (empty when valid)."""
    errors: list[str] = []
    if not isinstance(state, dict):
        return ["project state must be a JSON object"]

    if state.get("schema_version") != SCHEMA_VERSION:
        errors.append(f"schema_version must be {SCHEMA_VERSION!r}")
    project_id = state.get("project_id")
    if not isinstance(project_id, str) or not _PROJECT_ID_RE.match(project_id or ""):
        errors.append("project_id must be a non-empty id matching ^[A-Za-z0-9._-]+$")
    if state.get("controller") != CONTROLLER:
        errors.append("controller must be 'agy'")
    if state.get("phase") not in PHASES:
        errors.append(f"phase must be one of {', '.join(PHASES)}")
    if state.get("sequential_only") is not True:
        errors.append("sequential_only must be true (parallel generation is out of scope)")

    slides = state.get("slides")
    if not isinstance(slides, dict):
        errors.append("slides must be an object")
        return errors

    for slide_id, slide in slides.items():
        if not _SLIDE_ID_RE.match(str(slide_id)):
            errors.append(f"slide id {slide_id!r} must match ^slide_[0-9]{{2,}}$")
        if not isinstance(slide, dict):
            errors.append(f"slide {slide_id} must be an object")
            continue
        if slide.get("status") not in SLIDE_STATES:
            errors.append(f"slide {slide_id} status is invalid")
        generation = slide.get("generation")
        if not isinstance(generation, int) or isinstance(generation, bool) or generation < 0:
            errors.append(f"slide {slide_id} generation must be a non-negative integer")
        attempts = slide.get("attempts", [])
        if not isinstance(attempts, list):
            errors.append(f"slide {slide_id} attempts must be a list")
            continue
        for i, attempt in enumerate(attempts):
            if not isinstance(attempt, dict):
                errors.append(f"slide {slide_id} attempt {i} must be an object")
                continue
            for key in ("generation", "worker", "status", "idempotency_key", "at"):
                if key not in attempt:
                    errors.append(f"slide {slide_id} attempt {i} missing {key}")
            if attempt.get("worker") not in (None, "codex", "kiro"):
                errors.append(f"slide {slide_id} attempt {i} worker must be codex or kiro")

    _reject_credentials(state, errors)
    return errors


_CREDENTIAL_KEY_RE = re.compile(
    r"(?i)(?:^|_)(?:api_key|apikey|access_token|refresh_token|id_token|bearer_token|session_token|secret|password)$"
)


def _reject_credentials(obj: Any, errors: list[str], path: str = "") -> None:
    """Guard: project state must never carry credential-shaped keys."""
    if isinstance(obj, dict):
        for key, value in obj.items():
            if isinstance(key, str) and _CREDENTIAL_KEY_RE.search(key):
                errors.append(f"credential-shaped key not allowed in project state: {path}{key}")
            _reject_credentials(value, errors, f"{path}{key}.")
    elif isinstance(obj, list):
        for i, item in enumerate(obj):
            _reject_credentials(item, errors, f"{path}{i}.")


# ---------------------------------------------------------------------------
# ProjectState
# ---------------------------------------------------------------------------
@dataclass
class ProjectState:
    workspace_root: Path
    data: dict[str, Any]

    # -- construction ------------------------------------------------------
    @classmethod
    def initialize(
        cls,
        workspace_root: str | Path,
        project_id: str,
        slide_ids: Iterable[str] | None = None,
        deck_spec_path: str | None = None,
        slide_jobs_path: str | None = None,
    ) -> "ProjectState":
        root = Path(os.path.realpath(os.path.expanduser(str(workspace_root))))
        if not _PROJECT_ID_RE.match(project_id or ""):
            raise ProjectStateInvalid("project_id must match ^[A-Za-z0-9._-]+$")
        slides: dict[str, Any] = {}
        for sid in slide_ids or []:
            if not _SLIDE_ID_RE.match(sid):
                raise ProjectStateInvalid(f"slide id {sid!r} must match ^slide_[0-9]{{2,}}$")
            slides[sid] = {
                "status": SLIDE_PLANNED,
                "generation": 0,
                "generating_attempt": None,
                "job_path": None,
                "image_path": None,
                "aspect_ratio": None,
                "blocker": None,
                "attempts": [],
            }
        now = now_iso()
        data = {
            "schema_version": SCHEMA_VERSION,
            "project_id": project_id,
            "controller": CONTROLLER,
            "phase": PHASE_INTAKE,
            "phase_before_block": None,
            "sequential_only": True,
            "created_at": now,
            "updated_at": now,
            "outline": {"status": "pending"},
            "style": {"status": "pending"},
            "sample": {"status": "pending"},
            "deck_spec_path": deck_spec_path,
            "slide_jobs_path": slide_jobs_path,
            "history": [],
            "slides": slides,
        }
        errors = validate_state(data)
        if errors:
            raise ProjectStateInvalid("; ".join(errors))
        return cls(root, data)

    @classmethod
    def state_path(cls, workspace_root: str | Path) -> Path:
        return Path(workspace_root) / STATE_FILENAME

    @classmethod
    def load(cls, workspace_root: str | Path) -> "ProjectState":
        root = Path(os.path.realpath(os.path.expanduser(str(workspace_root))))
        path = cls.state_path(root)
        if not path.exists():
            raise ProjectStateInvalid(f"project state not found: {path}")
        try:
            raw = path.read_text(encoding="utf-8")
            data = json.loads(raw)
        except (OSError, json.JSONDecodeError) as exc:
            # Corrupt state must NOT be silently reset. Report and stop.
            raise ProjectStateInvalid(f"project state is corrupt and was not overwritten: {exc}")
        errors = validate_state(data)
        if errors:
            raise ProjectStateInvalid("project state failed validation: " + "; ".join(errors))
        return cls(root, data)

    # -- persistence -------------------------------------------------------
    def save(self) -> Path:
        self.data["updated_at"] = now_iso()
        errors = validate_state(self.data)
        if errors:
            # Never overwrite a good on-disk file with invalid state.
            raise ProjectStateInvalid("refusing to save invalid project state: " + "; ".join(errors))
        path = self.state_path(self.workspace_root)
        _atomic_write_json(path, self.data)
        return path

    # -- accessors ---------------------------------------------------------
    @property
    def phase(self) -> str:
        return self.data["phase"]

    @property
    def project_id(self) -> str:
        return self.data["project_id"]

    def slide(self, slide_id: str) -> dict[str, Any]:
        slides = self.data["slides"]
        if slide_id not in slides:
            raise ProjectStateInvalid(f"unknown slide: {slide_id}")
        return slides[slide_id]

    def add_slide(self, slide_id: str) -> dict[str, Any]:
        if not _SLIDE_ID_RE.match(slide_id):
            raise ProjectStateInvalid(f"slide id {slide_id!r} must match ^slide_[0-9]{{2,}}$")
        if slide_id in self.data["slides"]:
            raise ProjectStateInvalid(f"slide already exists: {slide_id}")
        self.data["slides"][slide_id] = {
            "status": SLIDE_PLANNED,
            "generation": 0,
            "generating_attempt": None,
            "job_path": None,
            "image_path": None,
            "aspect_ratio": None,
            "blocker": None,
            "attempts": [],
        }
        return self.data["slides"][slide_id]

    # -- gates -------------------------------------------------------------
    def set_gate(self, gate: str, status: str) -> None:
        if gate not in ("outline", "style", "sample"):
            raise ProjectStateInvalid(f"unknown gate: {gate}")
        if status not in ("pending", "approved", "rejected"):
            raise ProjectStateInvalid(f"invalid gate status: {status}")
        self.data[gate] = {**self.data.get(gate, {}), "status": status}

    # -- phase transitions -------------------------------------------------
    def set_phase(self, target: str, note: str | None = None) -> None:
        """AGY-driven phase transition. Never guesses; rejects illegal jumps."""
        current = self.data["phase"]
        if target not in PHASES:
            raise InvalidStateTransition(f"unknown phase: {target}")
        if target == current:
            return
        if target == PHASE_BLOCKED:
            # Any phase may go to blocked; remember where to resume.
            self.data["phase_before_block"] = current
            self._record_phase_history(current, target, note)
            self.data["phase"] = PHASE_BLOCKED
            return
        if current == PHASE_BLOCKED:
            # Resume must be explicitly targeted by AGY. Only allow resuming to
            # the remembered phase or a legal successor of it.
            before = self.data.get("phase_before_block")
            allowed = {before} | PHASE_TRANSITIONS.get(before, frozenset()) if before else set()
            if target not in allowed:
                raise InvalidStateTransition(
                    f"cannot resume from blocked to {target!r}; "
                    f"resume target must be {sorted(allowed)} (phase before block: {before!r})"
                )
            self.data["phase_before_block"] = None
            self._record_phase_history(current, target, note)
            self.data["phase"] = target
            return
        if target not in PHASE_TRANSITIONS.get(current, frozenset()):
            raise InvalidStateTransition(f"illegal phase transition: {current} -> {target}")
        self._record_phase_history(current, target, note)
        self.data["phase"] = target

    def _record_phase_history(self, frm: str, to: str, note: str | None) -> None:
        self.data.setdefault("history", []).append(
            {"from": frm, "to": to, "at": now_iso(), "note": note}
        )

    # -- slide transitions -------------------------------------------------
    def set_slide_status(
        self,
        slide_id: str,
        target: str,
        by: str = CONTROLLER,
        note: str | None = None,
    ) -> None:
        """Transition a slide. QA-judgement transitions require by == 'agy'.

        ``by`` records the actor that requested the transition. Workers never
        call this directly (they hand results to :meth:`record_worker_result`),
        but this argument makes the ownership rule explicit and testable: only
        AGY may perform a visual-QA judgement (generated -> qa_passed/qa_failed).
        """
        slide = self.slide(slide_id)
        current = slide["status"]
        if target not in SLIDE_STATES:
            raise InvalidStateTransition(f"unknown slide status: {target}")
        if target == current:
            return
        if target == SLIDE_BLOCKED:
            slide["phase_before_block"] = current
            slide["status"] = SLIDE_BLOCKED
            return
        if current == SLIDE_BLOCKED:
            before = slide.get("phase_before_block")
            allowed = {before} | SLIDE_TRANSITIONS.get(before, frozenset()) if before else set()
            if target not in allowed:
                raise InvalidStateTransition(
                    f"cannot resume slide {slide_id} from blocked to {target!r}; "
                    f"allowed: {sorted(allowed)}"
                )
            slide["phase_before_block"] = None
            slide["status"] = target
            return
        if target not in SLIDE_TRANSITIONS.get(current, frozenset()):
            raise InvalidStateTransition(
                f"illegal slide transition for {slide_id}: {current} -> {target}"
            )
        if (current, target) in QA_JUDGEMENT_TRANSITIONS and by != CONTROLLER:
            raise InvalidStateTransition(
                f"visual-QA judgement {current} -> {target} is AGY-only; got by={by!r}"
            )
        slide["status"] = target

    # -- generation dispatch ----------------------------------------------
    def begin_generation(self, slide_id: str, job_path: str | None = None) -> int:
        """Mark a slide as generating and bump the generation counter.

        Returns the generation number of this in-flight attempt. Must be called
        from ``ready`` (planned -> ready happens first). Increments generation
        exactly once per real Codex call.
        """
        slide = self.slide(slide_id)
        if slide["status"] != SLIDE_READY:
            raise InvalidStateTransition(
                f"slide {slide_id} must be 'ready' before generating; got {slide['status']}"
            )
        slide["generation"] = int(slide.get("generation", 0)) + 1
        slide["generating_attempt"] = slide["generation"]
        if job_path is not None:
            slide["job_path"] = self._safe_rel(job_path, "job_path")
        slide["status"] = SLIDE_GENERATING
        return slide["generation"]

    # -- worker result recording ------------------------------------------
    def record_worker_result(
        self,
        slide_id: str,
        result: dict[str, Any],
        idempotency_key: str | None = None,
    ) -> dict[str, Any]:
        """Record a Codex image worker result against an in-flight generation.

        This transitions ``generating -> generated`` on success or
        ``generating -> generation_failed`` on error. It NEVER performs the
        visual-QA judgement and NEVER changes the project phase.

        Idempotency: recording the same completed result twice (same
        idempotency key) does not add a duplicate attempt, does not bump the
        generation counter, and does not re-transition.
        """
        validate_worker_result(result)  # raises WorkerResultInvalid on bad shape
        if _result_sets_phase(result):
            raise WorkerResultInvalid("worker result must not set a project phase")

        slide = self.slide(slide_id)

        # Idempotency first: if this exact result was already recorded, return
        # the existing attempt without re-transitioning or bumping anything —
        # even if the slide has already moved on from 'generating'.
        if idempotency_key is not None:
            for existing in slide.get("attempts", []):
                if existing.get("idempotency_key") == idempotency_key:
                    return existing

        if slide["status"] != SLIDE_GENERATING:
            raise InvalidStateTransition(
                f"slide {slide_id} must be 'generating' to record a result; got {slide['status']}"
            )

        generation = int(slide.get("generating_attempt") or slide.get("generation") or 0)
        key = idempotency_key or _derive_idempotency_key(slide_id, generation, result)

        # Idempotency (derived key): if an attempt with this key already exists.
        for existing in slide.get("attempts", []):
            if existing.get("idempotency_key") == key:
                return existing

        status = result.get("status")
        attempt = {
            "generation": generation,
            "worker": "codex",
            "status": status,
            "operation": result.get("operation"),
            "backend": result.get("backend"),
            "output_path": result.get("output_path"),
            "error_code": result.get("error_code"),
            "idempotency_key": key,
            "at": now_iso(),
            "diagnostics": _sanitize_diagnostics(result.get("diagnostics")),
        }
        slide.setdefault("attempts", []).append(attempt)
        slide["generating_attempt"] = None

        if status == "completed":
            if result.get("output_path"):
                slide["image_path"] = self._safe_rel(result["output_path"], "output_path")
            slide["status"] = SLIDE_GENERATED
        else:
            # Preserve the worker error; do not swallow it.
            slide["status"] = SLIDE_GENERATION_FAILED
            slide["blocker"] = {
                "reason": "codex generation failed",
                "error_code": result.get("error_code"),
                "at": now_iso(),
            }
        return attempt

    def record_engineering_result(self, result: dict[str, Any]) -> dict[str, Any]:
        """Validate and return a Kiro engineering result verbatim.

        Engineering results never touch slide or phase state. Kiro cannot
        advance the deck workflow; AGY reads the (preserved) result and decides.
        """
        validate_worker_result(result)
        if _result_sets_phase(result):
            raise WorkerResultInvalid("engineering result must not set a project phase")
        return result

    # -- consecutive generic-failure retry policy (Phase 10.2) --------------
    def consecutive_failure_streak(self, slide_id: str, error_code: str = ERROR_IMAGE_GENERATION_FAILED) -> int:
        """Count the current trailing run of same-``error_code`` attempts.

        Scoped to this slide only: an unrelated failure on another slide can
        never inflate or reset this count. The streak is derived entirely from
        the existing ``attempts`` history (no new persisted field), and resets
        to 0 the moment the most recent attempts include a ``completed`` one
        more recently than a failure of ``error_code``.
        """
        streak = 0
        for attempt in reversed(self.slide(slide_id).get("attempts", [])):
            if attempt.get("status") == "error" and attempt.get("error_code") == error_code:
                streak += 1
                continue
            break
        return streak

    def may_retry_immediately(
        self, slide_id: str, error_code: str = ERROR_IMAGE_GENERATION_FAILED
    ) -> bool:
        """Whether AGY may dispatch one more immediate attempt for this slide.

        Policy: a generic ``IMAGE_GENERATION_FAILED`` may be retried once
        immediately. A second *consecutive* occurrence for the same slide must
        not be retried a third time immediately; the caller is expected to
        block the slide and the project instead (see
        :meth:`block_after_repeated_failure`). A success resets the streak, and
        a different slide's failure never contributes to this count.
        """
        return self.consecutive_failure_streak(slide_id, error_code) < 2

    def block_after_repeated_failure(
        self, slide_id: str, error_code: str = ERROR_IMAGE_GENERATION_FAILED
    ) -> None:
        """Stop retrying a slide that failed the same way twice in a row.

        Moves the affected slide to ``blocked`` (remembering its prior status
        for resume) and the whole project to ``blocked`` (remembering
        ``slide_generation`` as ``phase_before_block``), so no further
        ready/planned slide is dispatched until AGY explicitly resumes. This
        never reclassifies the worker's ``error_code``; it only records AGY's
        own decision not to retry a third time.
        """
        slide = self.slide(slide_id)
        if slide["status"] != SLIDE_GENERATION_FAILED:
            raise InvalidStateTransition(
                f"slide {slide_id} must be 'generation_failed' to apply the repeated-failure "
                f"block; got {slide['status']}"
            )
        slide["blocker"] = {
            "reason": "repeated_image_backend_failure",
            "error_code": error_code,
            "retry_immediately": False,
            "at": now_iso(),
        }
        self.set_slide_status(slide_id, SLIDE_BLOCKED)
        if self.phase != PHASE_BLOCKED:
            self.set_phase(PHASE_BLOCKED, note="repeated_image_backend_failure")

    def block_for_operator_confirmed_quota(self, note: str | None = None) -> None:
        """Record an operator-confirmed subscription-quota block on the project.

        This is an orchestration/operator decision, never a worker error_code.
        It must only be called when AGY or the user has confirmed quota
        exhaustion through an external channel (e.g. the ChatGPT/Codex billing
        UI); it never infers quota from a subprocess returncode or from
        ``IMAGE_GENERATION_FAILED`` alone. The most recent worker error_code (if
        any) is preserved unchanged in the slide's own ``blocker``/``attempts``;
        this method only adds a project-level note so provenance stays
        separate: worker evidence vs. operator decision.
        """
        self.data["operator_blocker"] = {
            "reason": "subscription_quota_exhausted",
            "confirmed_by": "operator",
            "at": now_iso(),
            "note": note,
        }
        if self.phase != PHASE_BLOCKED:
            self.set_phase(PHASE_BLOCKED, note=note or "subscription_quota_exhausted")

    # -- resume / recovery -------------------------------------------------
    def recover_interrupted(self, artifact_exists: dict[str, bool] | None = None) -> list[str]:
        """Deterministically recover slides left in 'generating' after a crash.

        A slide stuck in ``generating`` cannot be assumed successful. Recovery
        is based on recorded attempts and (optionally) confirmed artifacts:

        * If a recorded attempt for the in-flight generation shows ``completed``
          and the artifact is confirmed to exist -> ``generated``.
        * Otherwise the outcome is unknown -> ``generation_failed`` so AGY can
          decide to retry or block. Never marks unknown work as success.

        ``artifact_exists`` maps ``image_path`` (workspace-relative) to a bool.
        When omitted, existence is checked on disk inside the workspace.

        Returns the list of slide ids that were recovered.
        """
        recovered: list[str] = []
        for slide_id, slide in self.data["slides"].items():
            if slide.get("status") != SLIDE_GENERATING:
                continue
            gen = int(slide.get("generating_attempt") or slide.get("generation") or 0)
            completed_attempt = next(
                (
                    a
                    for a in slide.get("attempts", [])
                    if a.get("generation") == gen and a.get("status") == "completed"
                ),
                None,
            )
            confirmed = False
            if completed_attempt is not None:
                image_path = slide.get("image_path") or completed_attempt.get("output_path")
                if image_path:
                    if artifact_exists is not None:
                        confirmed = bool(artifact_exists.get(image_path))
                    else:
                        confirmed = self._artifact_on_disk(image_path)
            if completed_attempt is not None and confirmed:
                slide["status"] = SLIDE_GENERATED
                slide["generating_attempt"] = None
                if slide.get("image_path") is None and completed_attempt.get("output_path"):
                    slide["image_path"] = self._safe_rel(
                        completed_attempt["output_path"], "output_path"
                    )
            else:
                slide["status"] = SLIDE_GENERATION_FAILED
                slide["generating_attempt"] = None
                slide["blocker"] = {
                    "reason": "interrupted during generation; outcome unconfirmed",
                    "error_code": None,
                    "at": now_iso(),
                }
            recovered.append(slide_id)
        return recovered

    def _artifact_on_disk(self, image_path: str) -> bool:
        try:
            resolved = _resolve_within(self.workspace_root, image_path, "image_path")
        except ProjectStateError:
            return False
        return resolved.is_file() and resolved.stat().st_size > 0

    def _safe_rel(self, value: str, label: str) -> str:
        resolved = _resolve_within(self.workspace_root, value, label)
        try:
            return resolved.relative_to(self.workspace_root).as_posix()
        except ValueError:
            return resolved.as_posix()

    # -- reporting ---------------------------------------------------------
    def summary(self) -> dict[str, Any]:
        counts = {state: 0 for state in SLIDE_STATES}
        for slide in self.data["slides"].values():
            status = slide.get("status")
            if status in counts:
                counts[status] += 1
        total = len(self.data["slides"])
        return {
            "project_id": self.project_id,
            "controller": self.data["controller"],
            "phase": self.phase,
            "sequential_only": self.data["sequential_only"],
            "slides_total": total,
            "planned": counts[SLIDE_PLANNED],
            "ready": counts[SLIDE_READY],
            "generating": counts[SLIDE_GENERATING],
            "generated": counts[SLIDE_GENERATED],
            "qa_passed": counts[SLIDE_QA_PASSED],
            "qa_failed": counts[SLIDE_QA_FAILED],
            "generation_failed": counts[SLIDE_GENERATION_FAILED],
            "assembled": counts[SLIDE_ASSEMBLED],
            "failed": counts[SLIDE_GENERATION_FAILED] + counts[SLIDE_QA_FAILED],
            "blocked": counts[SLIDE_BLOCKED],
            "operator_blocker": self.data.get("operator_blocker"),
        }


# ---------------------------------------------------------------------------
# Worker result validation (module-level, reusable)
# ---------------------------------------------------------------------------
_CODEX_ERROR_CODES = frozenset(
    {
        "IMAGE_BACKEND_UNAVAILABLE",
        "CODEX_CLI_UNAVAILABLE",
        "CODEX_AUTH_UNAVAILABLE",
        "IMAGE_GENERATION_FAILED",
        "IMAGE_ARTIFACT_NOT_FOUND",
        "IMAGE_ARTIFACT_AMBIGUOUS",
        "IMAGE_OUTPUT_INVALID",
        "IMAGE_OUTPUT_PATH_CONFLICT",
        "CODEX_TIMEOUT",
        "IMAGE_TASK_INVALID",
    }
)


def _result_sets_phase(result: dict[str, Any]) -> bool:
    return "phase" in result or "project_phase" in result


def validate_worker_result(result: Any) -> str:
    """Validate a worker result and return its kind ('codex' or 'kiro').

    Raises :class:`WorkerResultInvalid` on any contract violation. Codex and
    Kiro results are intentionally different shapes.
    """
    if not isinstance(result, dict):
        raise WorkerResultInvalid("worker result must be a JSON object")

    # Kiro engineering result (has the bridge schema tag).
    if result.get("schema") == "agy-ppt/kiro-acp-bridge-result/1":
        if result.get("control") != "returned_to_agy":
            raise WorkerResultInvalid("kiro result must have control == 'returned_to_agy'")
        if "status" not in result:
            raise WorkerResultInvalid("kiro result missing status")
        return "kiro"

    # Codex image result.
    missing = [k for k in ("status", "slide_id", "operation", "backend") if k not in result]
    if missing:
        raise WorkerResultInvalid(f"codex result missing required fields: {', '.join(missing)}")
    if result.get("status") not in ("completed", "error"):
        raise WorkerResultInvalid("codex result status must be 'completed' or 'error'")
    if result.get("backend") != "codex_builtin_imagegen":
        raise WorkerResultInvalid("codex result backend must be 'codex_builtin_imagegen'")
    if not _SLIDE_ID_RE.match(str(result.get("slide_id"))):
        raise WorkerResultInvalid("codex result slide_id must match ^slide_[0-9]{2,}$")
    if result.get("operation") not in ("generate", "regenerate", "probe"):
        raise WorkerResultInvalid("codex result operation is invalid")

    status = result.get("status")
    error_code = result.get("error_code")
    if status == "completed":
        if error_code:
            raise WorkerResultInvalid("completed codex result must not carry an error_code")
        if not result.get("output_path"):
            raise WorkerResultInvalid("completed codex result must include output_path")
    else:  # error
        if not error_code:
            raise WorkerResultInvalid("codex error result must include error_code")
        if error_code not in _CODEX_ERROR_CODES:
            raise WorkerResultInvalid(f"unknown codex error_code: {error_code}")

    diagnostics = result.get("diagnostics")
    if diagnostics is not None:
        if not isinstance(diagnostics, dict):
            raise WorkerResultInvalid("codex diagnostics must be an object")
        if diagnostics.get("api_fallback_used") is True:
            raise WorkerResultInvalid("codex result reports api_fallback_used=true (forbidden)")
    return "codex"


def _sanitize_diagnostics(diagnostics: Any) -> dict[str, Any] | None:
    """Keep a small, credential-free subset of diagnostics in the attempt.

    thread_id is retained for traceability but is NOT used as the project
    idempotency key.
    """
    if not isinstance(diagnostics, dict):
        return None
    keep = {}
    for key in ("auth", "api_fallback_used", "thread_id", "artifact_discovery"):
        if key in diagnostics:
            keep[key] = diagnostics[key]
    errors: list[str] = []
    _reject_credentials(keep, errors)
    if errors:
        return {"auth": diagnostics.get("auth"), "api_fallback_used": diagnostics.get("api_fallback_used")}
    return keep or None


def _derive_idempotency_key(slide_id: str, generation: int, result: dict[str, Any]) -> str:
    """Stable idempotency key for an attempt.

    Prefers an explicit worker run id if present, then falls back to a stable
    composition of slide_id + generation + output_path/error_code. Codex
    thread_id is intentionally not the primary key (a thread may not map 1:1 to
    a project attempt), though it is stored in diagnostics for traceability.
    """
    diagnostics = result.get("diagnostics") if isinstance(result.get("diagnostics"), dict) else {}
    run_id = result.get("run_id") or result.get("attempt_id") or diagnostics.get("run_id")
    if run_id:
        return f"{slide_id}:{run_id}"
    tail = result.get("output_path") or result.get("error_code") or result.get("status") or ""
    return f"{slide_id}:gen{generation}:{tail}"


if __name__ == "__main__":  # pragma: no cover - thin CLI shim
    import argparse

    parser = argparse.ArgumentParser(description="AGY PPT project state inspector")
    parser.add_argument("workspace_root")
    parser.add_argument("--summary", action="store_true")
    args = parser.parse_args()
    state = ProjectState.load(args.workspace_root)
    if args.summary:
        print(json.dumps(state.summary(), ensure_ascii=False, indent=2))
    else:
        print(json.dumps(state.data, ensure_ascii=False, indent=2))
