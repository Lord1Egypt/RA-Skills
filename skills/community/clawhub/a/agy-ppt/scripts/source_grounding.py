#!/usr/bin/env python3
"""Phase 12 -- deterministic source-grounding & traceability contracts.

This module is a **sidecar** to the frozen Project State control plane
(``project_state.py``). It never imports from, modifies, or is imported by
``ProjectState``. It follows the exact same relationship ``project_state.py``
itself has to the upstream ``prompts/slide_XX.json`` files: additive,
referencing shared IDs (``slide_id``), never duplicating or overriding
anything the frozen state machine owns.

Two layers, never confused (see ``docs/source-grounding.md``):

* **Layer A -- Semantic Evidence Creation (AGY-owned).** AGY reads the source
  material, decides what the source units are, which source unit(s) support a
  slide claim, whether that support actually holds, what a source's numeric
  value means, and what a modal/responsibility clause means. All of this is
  semantic judgement. This module never computes any of it.
* **Layer B -- Deterministic Contract Validation (this module).** Schema
  shape, ID uniqueness, referenced-ID existence (no dangling references),
  required-field presence, legal status values, HIGH-priority coverage
  accounting, and resume-safe persistence. This module never claims a slide
  fact is true; it only checks that AGY's own persisted judgement is
  structurally well-formed and internally consistent.

Four sidecar artifacts live beside ``project_state.json`` in the same
workspace (never inside it, never inside the git repository):

* ``source_inventory.json``   -- stable source units carved out of the input
  material (schema: ``schemas/source_inventory.schema.json``)
* ``claim_traceability.json`` -- which source unit(s) support which slide
  claim, and AGY's support judgement (schema:
  ``schemas/claim_traceability.schema.json``)
* ``source_coverage.json``    -- deterministic accounting of every source
  unit, so a HIGH-priority unit can never silently disappear (schema:
  ``schemas/source_coverage.schema.json``)
* ``source_grounded_qa.json`` -- the final report, explicitly split into
  ``deterministic_findings`` (computed here) and ``semantic_findings`` (AGY's
  own judgement, persisted verbatim) (schema:
  ``schemas/source_grounded_qa.schema.json``)

Optional capability: a project that has no source document at all simply
never creates ``source_inventory.json`` (or creates one with
``"enabled": false``). :func:`source_grounding_enabled` is the single
place that decides this, so creative/no-source decks are never forced through
this workflow -- see ``is_source_grounding_project`` below.

This module intentionally does NOT:

* parse PDFs, DOCX, or any real document format (Phase 12.1/12.2 scope is the
  contract + deterministic validators, not a document parser);
* judge whether a claim is factually true;
* store the confidential source text itself (only a minimal locator and an
  optional caller-supplied sha256 digest for change detection);
* touch ``project_state.py``'s phase/slide state machines, its ``blocked``
  semantics, or the Phase 10.2/10.3 retry/operator-blocker policy.
"""

from __future__ import annotations

import hashlib
import json
import os
import re
import tempfile
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable

SCHEMA_VERSION = "1"

# ---------------------------------------------------------------------------
# Filenames (sidecar artifacts, beside project_state.json)
# ---------------------------------------------------------------------------
SOURCE_INVENTORY_FILENAME = "source_inventory.json"
CLAIM_TRACEABILITY_FILENAME = "claim_traceability.json"
SOURCE_COVERAGE_FILENAME = "source_coverage.json"
SOURCE_GROUNDED_QA_FILENAME = "source_grounded_qa.json"

# ---------------------------------------------------------------------------
# Error contract (distinct from IMAGE_* worker errors and from
# PROJECT_STATE_INVALID / INVALID_STATE_TRANSITION / WORKER_RESULT_INVALID)
# ---------------------------------------------------------------------------
ERROR_SOURCE_INVENTORY_INVALID = "SOURCE_INVENTORY_INVALID"
ERROR_TRACEABILITY_INVALID = "TRACEABILITY_INVALID"
ERROR_SOURCE_REFERENCE_MISSING = "SOURCE_REFERENCE_MISSING"
ERROR_SOURCE_COVERAGE_INCOMPLETE = "SOURCE_COVERAGE_INCOMPLETE"
ERROR_GROUNDED_QA_INCOMPLETE = "GROUNDED_QA_INCOMPLETE"
ERROR_SOURCE_CHANGED = "SOURCE_CHANGED"

# ---------------------------------------------------------------------------
# Vocabularies
# ---------------------------------------------------------------------------
PRIORITIES = ("HIGH", "MEDIUM", "LOW")
LOCATOR_KINDS = ("page", "section", "line_range", "generic")
SUPPORT_STATUSES = (
    "supported",
    "partially_supported",
    "unsupported",
    "not_applicable",
    "pending_review",
)
COVERAGE_STATUSES = (
    "covered",
    "speaker_notes_only",
    "intentionally_omitted",
    "not_applicable",
    "unaccounted",
)
QA_STATUSES = ("pending", "reviewed")
AGY_QA_OUTCOMES = (None, "passed", "passed_with_notes", "failed", "pending")

_PROJECT_ID_RE = re.compile(r"^[A-Za-z0-9._-]+$")
_SLIDE_ID_RE = re.compile(r"^slide_[0-9]{2,}$")
_SOURCE_ID_RE = re.compile(r"^src_[A-Za-z0-9._-]+$")
_UNIT_ID_RE = re.compile(r"^su:[A-Za-z0-9._-]+:[a-f0-9]{8,}$")
_CLAIM_ID_RE = re.compile(r"^cl:[A-Za-z0-9._-]+:[0-9]{2,}$")
_DIGEST_RE = re.compile(r"^[a-f0-9]{64}$")

_CREDENTIAL_KEY_RE = re.compile(
    r"(?i)(?:^|_)(?:api_key|apikey|access_token|refresh_token|id_token|bearer_token|session_token|secret|password)$"
)


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")


# ---------------------------------------------------------------------------
# Exceptions
# ---------------------------------------------------------------------------
class SourceGroundingError(Exception):
    """Base error carrying a stable error_code, matching project_state.py's convention."""

    error_code = ERROR_SOURCE_INVENTORY_INVALID

    def __init__(self, message: str, error_code: str | None = None) -> None:
        super().__init__(message)
        if error_code is not None:
            self.error_code = error_code


class SourceInventoryInvalid(SourceGroundingError):
    error_code = ERROR_SOURCE_INVENTORY_INVALID


class TraceabilityInvalid(SourceGroundingError):
    error_code = ERROR_TRACEABILITY_INVALID


class SourceReferenceMissing(SourceGroundingError):
    error_code = ERROR_SOURCE_REFERENCE_MISSING


class SourceCoverageIncomplete(SourceGroundingError):
    error_code = ERROR_SOURCE_COVERAGE_INCOMPLETE


class GroundedQaIncomplete(SourceGroundingError):
    error_code = ERROR_GROUNDED_QA_INCOMPLETE


class SourceChanged(SourceGroundingError):
    error_code = ERROR_SOURCE_CHANGED


# ---------------------------------------------------------------------------
# Path safety / atomic write (mirrors project_state.py's own helpers so the
# two sidecar layers behave identically on disk without importing each other)
# ---------------------------------------------------------------------------
def _resolve_within(workspace_root: Path, value: str, label: str) -> Path:
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
        raise SourceGroundingError(f"{label} {value!r} resolves outside the workspace root")
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


def _reject_credentials(obj: Any, errors: list[str], path: str = "") -> None:
    if isinstance(obj, dict):
        for key, value in obj.items():
            if isinstance(key, str) and _CREDENTIAL_KEY_RE.search(key):
                errors.append(f"credential-shaped key not allowed: {path}{key}")
            _reject_credentials(value, errors, f"{path}{key}.")
    elif isinstance(obj, list):
        for i, item in enumerate(obj):
            _reject_credentials(item, errors, f"{path}{i}.")


# ---------------------------------------------------------------------------
# Stable IDs
# ---------------------------------------------------------------------------
def compute_unit_id(source_id: str, locator: dict[str, Any]) -> str:
    """Deterministic, resume-safe unit id derived from (source_id, locator).

    Recomputing this from the same ``source_id`` + ``locator`` on a later
    process/run always yields the same id -- it is not a random UUID and it
    never contains an absolute local path.
    """
    if not _SOURCE_ID_RE.match(source_id or ""):
        raise SourceInventoryInvalid(f"invalid source_id: {source_id!r}")
    canonical = json.dumps(locator, sort_keys=True, ensure_ascii=False)
    digest = hashlib.sha256(f"{source_id}\n{canonical}".encode("utf-8")).hexdigest()[:12]
    return f"su:{source_id}:{digest}"


def compute_source_digest(content: bytes | str) -> str:
    """sha256 hex digest for change detection. Never stores the content itself."""
    if isinstance(content, str):
        content = content.encode("utf-8")
    return hashlib.sha256(content).hexdigest()


def make_claim_id(slide_id: str, sequence: int) -> str:
    if not _SLIDE_ID_RE.match(slide_id or ""):
        raise TraceabilityInvalid(f"invalid slide_id: {slide_id!r}")
    if sequence < 1:
        raise TraceabilityInvalid("claim sequence must be >= 1")
    return f"cl:{slide_id}:{sequence:02d}"


# ---------------------------------------------------------------------------
# Locator validation
# ---------------------------------------------------------------------------
def validate_locator(locator: Any) -> list[str]:
    errors: list[str] = []
    if not isinstance(locator, dict):
        return ["locator must be an object"]
    kind = locator.get("kind")
    if kind not in LOCATOR_KINDS:
        errors.append(f"locator.kind must be one of {LOCATOR_KINDS}")
        return errors
    if kind in ("page", "line_range"):
        start = locator.get("start")
        if not isinstance(start, int) or isinstance(start, bool) or start < 1:
            errors.append(f"locator.start must be a positive integer for kind={kind!r}")
        end = locator.get("end")
        if end is not None and (not isinstance(end, int) or isinstance(end, bool) or end < 1):
            errors.append(f"locator.end must be a positive integer or null for kind={kind!r}")
    elif kind in ("section", "generic"):
        label = locator.get("label")
        if not isinstance(label, str) or not label.strip():
            errors.append(f"locator.label must be a non-empty string for kind={kind!r}")
    return errors


# ---------------------------------------------------------------------------
# Enablement (optional capability)
# ---------------------------------------------------------------------------
def source_inventory_path(workspace_root: str | Path) -> Path:
    return Path(workspace_root) / SOURCE_INVENTORY_FILENAME


def source_grounding_enabled(workspace_root: str | Path) -> bool:
    """True only when ``source_inventory.json`` exists AND says ``enabled: true``.

    A project with no such file (the common case -- a purely creative,
    no-source deck) is never required to have any of the other three
    artifacts. This is the single switch every other function in this module
    checks before requiring anything.
    """
    path = source_inventory_path(workspace_root)
    if not path.is_file():
        return False
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return False
    return bool(isinstance(data, dict) and data.get("enabled") is True)


# ---------------------------------------------------------------------------
# SourceInventory
# ---------------------------------------------------------------------------
@dataclass
class SourceInventory:
    workspace_root: Path
    data: dict[str, Any]

    @classmethod
    def initialize(cls, workspace_root: str | Path, project_id: str) -> "SourceInventory":
        root = Path(os.path.realpath(os.path.expanduser(str(workspace_root))))
        if not _PROJECT_ID_RE.match(project_id or ""):
            raise SourceInventoryInvalid("project_id must match ^[A-Za-z0-9._-]+$")
        now = now_iso()
        data = {
            "schema_version": SCHEMA_VERSION,
            "project_id": project_id,
            "enabled": True,
            "created_at": now,
            "updated_at": now,
            "sources": [],
            "units": [],
        }
        errors = validate_source_inventory(data)
        if errors:
            raise SourceInventoryInvalid("; ".join(errors))
        return cls(root, data)

    @classmethod
    def load(cls, workspace_root: str | Path) -> "SourceInventory":
        root = Path(os.path.realpath(os.path.expanduser(str(workspace_root))))
        path = source_inventory_path(root)
        if not path.exists():
            raise SourceInventoryInvalid(f"source inventory not found: {path}")
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            raise SourceInventoryInvalid(f"source inventory is corrupt and was not overwritten: {exc}")
        errors = validate_source_inventory(data)
        if errors:
            raise SourceInventoryInvalid("; ".join(errors))
        return cls(root, data)

    def save(self) -> Path:
        self.data["updated_at"] = now_iso()
        errors = validate_source_inventory(self.data)
        if errors:
            raise SourceInventoryInvalid("refusing to save invalid source inventory: " + "; ".join(errors))
        path = source_inventory_path(self.workspace_root)
        _atomic_write_json(path, self.data)
        return path

    def add_source(self, source_id: str, source_type: str, *, label: str | None = None,
                    source_digest: str | None = None, metadata: dict[str, Any] | None = None) -> dict[str, Any]:
        if any(s["source_id"] == source_id for s in self.data["sources"]):
            raise SourceInventoryInvalid(f"source already exists: {source_id}")
        entry = {
            "source_id": source_id,
            "source_type": source_type,
            "label": label,
            "source_digest": source_digest,
            "metadata": metadata,
        }
        self.data["sources"].append(entry)
        return entry

    def add_unit(self, source_id: str, unit_type: str, locator: dict[str, Any], priority: str, *,
                 title: str | None = None, metadata: dict[str, Any] | None = None) -> dict[str, Any]:
        if priority not in PRIORITIES:
            raise SourceInventoryInvalid(f"invalid priority: {priority!r}")
        loc_errors = validate_locator(locator)
        if loc_errors:
            raise SourceInventoryInvalid("; ".join(loc_errors))
        if not any(s["source_id"] == source_id for s in self.data["sources"]):
            raise SourceInventoryInvalid(f"unknown source_id: {source_id}")
        unit_id = compute_unit_id(source_id, locator)
        if any(u["unit_id"] == unit_id for u in self.data["units"]):
            # Resume-safe: adding the identical (source_id, locator) again is a
            # no-op, not a duplicate-id error.
            return next(u for u in self.data["units"] if u["unit_id"] == unit_id)
        entry = {
            "unit_id": unit_id,
            "source_id": source_id,
            "unit_type": unit_type,
            "locator": locator,
            "title": title,
            "priority": priority,
            "metadata": metadata,
        }
        self.data["units"].append(entry)
        return entry

    def unit_ids(self) -> set[str]:
        return {u["unit_id"] for u in self.data["units"]}

    def source_ids(self) -> set[str]:
        return {s["source_id"] for s in self.data["sources"]}

    def source_changed(self, source_id: str, current_digest: str) -> bool:
        """True when a source's recorded digest differs from ``current_digest``.

        Never compares or stores the confidential source text itself -- only
        the caller-supplied sha256 digest.
        """
        source = next((s for s in self.data["sources"] if s["source_id"] == source_id), None)
        if source is None:
            raise SourceReferenceMissing(f"unknown source_id: {source_id}")
        recorded = source.get("source_digest")
        if recorded is None:
            return False
        return recorded != current_digest


def validate_source_inventory(data: Any) -> list[str]:
    errors: list[str] = []
    if not isinstance(data, dict):
        return ["source inventory must be a JSON object"]
    if data.get("schema_version") != SCHEMA_VERSION:
        errors.append(f"schema_version must be {SCHEMA_VERSION!r}")
    project_id = data.get("project_id")
    if not isinstance(project_id, str) or not _PROJECT_ID_RE.match(project_id or ""):
        errors.append("project_id must match ^[A-Za-z0-9._-]+$")
    if not isinstance(data.get("enabled"), bool):
        errors.append("enabled must be a boolean")

    sources = data.get("sources")
    if not isinstance(sources, list):
        errors.append("sources must be a list")
        sources = []
    seen_source_ids: set[str] = set()
    for i, source in enumerate(sources):
        if not isinstance(source, dict):
            errors.append(f"sources[{i}] must be an object")
            continue
        source_id = source.get("source_id")
        if not isinstance(source_id, str) or not _SOURCE_ID_RE.match(source_id or ""):
            errors.append(f"sources[{i}].source_id must match ^src_[A-Za-z0-9._-]+$")
        elif source_id in seen_source_ids:
            errors.append(f"duplicate source_id: {source_id}")
        else:
            seen_source_ids.add(source_id)
        if not isinstance(source.get("source_type"), str) or not source.get("source_type"):
            errors.append(f"sources[{i}].source_type must be a non-empty string")
        digest = source.get("source_digest")
        if digest is not None and not _DIGEST_RE.match(str(digest)):
            errors.append(f"sources[{i}].source_digest must be a 64-hex sha256 digest or null")

    units = data.get("units")
    if not isinstance(units, list):
        errors.append("units must be a list")
        units = []
    seen_unit_ids: set[str] = set()
    for i, unit in enumerate(units):
        if not isinstance(unit, dict):
            errors.append(f"units[{i}] must be an object")
            continue
        unit_id = unit.get("unit_id")
        if not isinstance(unit_id, str) or not _UNIT_ID_RE.match(unit_id or ""):
            errors.append(f"units[{i}].unit_id must match ^su:<source_id>:<hex>$")
        elif unit_id in seen_unit_ids:
            errors.append(f"duplicate unit_id: {unit_id}")
        else:
            seen_unit_ids.add(unit_id)
        unit_source_id = unit.get("source_id")
        if unit_source_id not in seen_source_ids:
            errors.append(f"units[{i}].source_id references unknown source: {unit_source_id!r}")
        if not isinstance(unit.get("unit_type"), str) or not unit.get("unit_type"):
            errors.append(f"units[{i}].unit_type must be a non-empty string")
        if unit.get("priority") not in PRIORITIES:
            errors.append(f"units[{i}].priority must be one of {PRIORITIES}")
        loc_errors = validate_locator(unit.get("locator"))
        errors.extend(f"units[{i}].{e}" for e in loc_errors)
        # unit_id must actually be derivable from (source_id, locator).
        if isinstance(unit_id, str) and _UNIT_ID_RE.match(unit_id or "") and isinstance(unit_source_id, str):
            try:
                expected = compute_unit_id(unit_source_id, unit.get("locator") or {})
            except SourceGroundingError:
                expected = None
            if expected is not None and expected != unit_id:
                errors.append(
                    f"units[{i}].unit_id {unit_id!r} is not derivable from its own "
                    f"source_id+locator (expected {expected!r})"
                )

    _reject_credentials(data, errors)
    return errors


# ---------------------------------------------------------------------------
# ClaimTraceability
# ---------------------------------------------------------------------------
@dataclass
class ClaimTraceability:
    workspace_root: Path
    data: dict[str, Any]

    @classmethod
    def initialize(cls, workspace_root: str | Path, project_id: str) -> "ClaimTraceability":
        root = Path(os.path.realpath(os.path.expanduser(str(workspace_root))))
        if not _PROJECT_ID_RE.match(project_id or ""):
            raise TraceabilityInvalid("project_id must match ^[A-Za-z0-9._-]+$")
        now = now_iso()
        data = {
            "schema_version": SCHEMA_VERSION,
            "project_id": project_id,
            "created_at": now,
            "updated_at": now,
            "claims": [],
        }
        return cls(root, data)

    @classmethod
    def state_path(cls, workspace_root: str | Path) -> Path:
        return Path(workspace_root) / CLAIM_TRACEABILITY_FILENAME

    @classmethod
    def load(cls, workspace_root: str | Path) -> "ClaimTraceability":
        root = Path(os.path.realpath(os.path.expanduser(str(workspace_root))))
        path = cls.state_path(root)
        if not path.exists():
            raise TraceabilityInvalid(f"claim traceability not found: {path}")
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            raise TraceabilityInvalid(f"claim traceability is corrupt and was not overwritten: {exc}")
        return cls(root, data)

    def save(self, *, known_unit_ids: set[str] | None = None, known_slide_ids: set[str] | None = None) -> Path:
        self.data["updated_at"] = now_iso()
        errors = validate_claim_traceability(self.data, known_unit_ids=known_unit_ids, known_slide_ids=known_slide_ids)
        if errors:
            raise TraceabilityInvalid("refusing to save invalid claim traceability: " + "; ".join(errors))
        path = self.state_path(self.workspace_root)
        _atomic_write_json(path, self.data)
        return path

    def upsert_claim(
        self,
        slide_id: str,
        sequence: int,
        claim_text: str,
        source_unit_ids: Iterable[str],
        support_status: str,
        *,
        evidence_note: str | None = None,
        numeric_evidence: dict[str, Any] | None = None,
        modal_evidence: dict[str, Any] | None = None,
        qa_status: str = "pending",
    ) -> dict[str, Any]:
        """Idempotent: calling this again with the same (slide_id, sequence)
        updates the existing claim in place rather than duplicating it, so
        resume never inflates the claim list.
        """
        if support_status not in SUPPORT_STATUSES:
            raise TraceabilityInvalid(f"invalid support_status: {support_status!r}")
        if qa_status not in QA_STATUSES:
            raise TraceabilityInvalid(f"invalid qa_status: {qa_status!r}")
        claim_id = make_claim_id(slide_id, sequence)
        entry = {
            "claim_id": claim_id,
            "slide_id": slide_id,
            "claim_text": claim_text,
            "source_unit_ids": list(source_unit_ids),
            "support_status": support_status,
            "evidence_note": evidence_note,
            "numeric_evidence": numeric_evidence,
            "modal_evidence": modal_evidence,
            "qa_status": qa_status,
        }
        for i, existing in enumerate(self.data["claims"]):
            if existing["claim_id"] == claim_id:
                self.data["claims"][i] = entry
                return entry
        self.data["claims"].append(entry)
        return entry

    def claim_ids(self) -> set[str]:
        return {c["claim_id"] for c in self.data["claims"]}

    def unsupported_claim_ids(self) -> list[str]:
        return [c["claim_id"] for c in self.data["claims"] if c["support_status"] == "unsupported"]


def validate_claim_traceability(
    data: Any,
    *,
    known_unit_ids: set[str] | None = None,
    known_slide_ids: set[str] | None = None,
) -> list[str]:
    errors: list[str] = []
    if not isinstance(data, dict):
        return ["claim traceability must be a JSON object"]
    if data.get("schema_version") != SCHEMA_VERSION:
        errors.append(f"schema_version must be {SCHEMA_VERSION!r}")
    project_id = data.get("project_id")
    if not isinstance(project_id, str) or not _PROJECT_ID_RE.match(project_id or ""):
        errors.append("project_id must match ^[A-Za-z0-9._-]+$")

    claims = data.get("claims")
    if not isinstance(claims, list):
        errors.append("claims must be a list")
        claims = []
    seen_claim_ids: set[str] = set()
    for i, claim in enumerate(claims):
        if not isinstance(claim, dict):
            errors.append(f"claims[{i}] must be an object")
            continue
        claim_id = claim.get("claim_id")
        if not isinstance(claim_id, str) or not _CLAIM_ID_RE.match(claim_id or ""):
            errors.append(f"claims[{i}].claim_id must match ^cl:<slide_id>:<NN>$")
        elif claim_id in seen_claim_ids:
            errors.append(f"duplicate claim_id: {claim_id}")
        else:
            seen_claim_ids.add(claim_id)

        slide_id = claim.get("slide_id")
        if not isinstance(slide_id, str) or not _SLIDE_ID_RE.match(slide_id or ""):
            errors.append(f"claims[{i}].slide_id must match ^slide_[0-9]{{2,}}$")
        elif known_slide_ids is not None and slide_id not in known_slide_ids:
            errors.append(f"claims[{i}].slide_id references unknown slide: {slide_id!r}")

        if not isinstance(claim.get("claim_text"), str) or not claim.get("claim_text", "").strip():
            errors.append(f"claims[{i}].claim_text must be a non-empty string")

        source_unit_ids = claim.get("source_unit_ids")
        if not isinstance(source_unit_ids, list):
            errors.append(f"claims[{i}].source_unit_ids must be a list")
        else:
            for unit_id in source_unit_ids:
                if not isinstance(unit_id, str) or not _UNIT_ID_RE.match(unit_id or ""):
                    errors.append(f"claims[{i}].source_unit_ids contains an invalid id: {unit_id!r}")
                elif known_unit_ids is not None and unit_id not in known_unit_ids:
                    errors.append(f"claims[{i}].source_unit_ids references unknown unit: {unit_id!r}")

        if claim.get("support_status") not in SUPPORT_STATUSES:
            errors.append(f"claims[{i}].support_status must be one of {SUPPORT_STATUSES}")
        if claim.get("qa_status", "pending") not in QA_STATUSES:
            errors.append(f"claims[{i}].qa_status must be one of {QA_STATUSES}")

    _reject_credentials(data, errors)
    return errors


# ---------------------------------------------------------------------------
# SourceCoverage
# ---------------------------------------------------------------------------
@dataclass
class SourceCoverage:
    workspace_root: Path
    data: dict[str, Any]

    @classmethod
    def initialize(cls, workspace_root: str | Path, project_id: str) -> "SourceCoverage":
        root = Path(os.path.realpath(os.path.expanduser(str(workspace_root))))
        if not _PROJECT_ID_RE.match(project_id or ""):
            raise SourceCoverageIncomplete("project_id must match ^[A-Za-z0-9._-]+$")
        now = now_iso()
        data = {
            "schema_version": SCHEMA_VERSION,
            "project_id": project_id,
            "created_at": now,
            "updated_at": now,
            "entries": [],
        }
        return cls(root, data)

    @classmethod
    def state_path(cls, workspace_root: str | Path) -> Path:
        return Path(workspace_root) / SOURCE_COVERAGE_FILENAME

    @classmethod
    def load(cls, workspace_root: str | Path) -> "SourceCoverage":
        root = Path(os.path.realpath(os.path.expanduser(str(workspace_root))))
        path = cls.state_path(root)
        if not path.exists():
            raise SourceCoverageIncomplete(f"source coverage not found: {path}")
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            raise SourceCoverageIncomplete(f"source coverage is corrupt and was not overwritten: {exc}")
        return cls(root, data)

    def save(self, *, known_unit_ids: set[str] | None = None,
             known_claim_ids: set[str] | None = None) -> Path:
        self.data["updated_at"] = now_iso()
        errors = validate_source_coverage(
            self.data, known_unit_ids=known_unit_ids, known_claim_ids=known_claim_ids
        )
        if errors:
            raise SourceCoverageIncomplete("refusing to save invalid source coverage: " + "; ".join(errors))
        path = self.state_path(self.workspace_root)
        _atomic_write_json(path, self.data)
        return path

    def upsert_entry(
        self,
        source_unit_id: str,
        priority: str,
        coverage_status: str,
        *,
        covered_by_slide_ids: Iterable[str] = (),
        covered_by_claim_ids: Iterable[str] = (),
        omission_reason: str | None = None,
    ) -> dict[str, Any]:
        """Idempotent per source_unit_id; does not duplicate/inflate accounting."""
        if priority not in PRIORITIES:
            raise SourceCoverageIncomplete(f"invalid priority: {priority!r}")
        if coverage_status not in COVERAGE_STATUSES:
            raise SourceCoverageIncomplete(f"invalid coverage_status: {coverage_status!r}")
        if coverage_status == "intentionally_omitted" and not omission_reason:
            raise SourceCoverageIncomplete("intentionally_omitted requires a non-empty omission_reason")
        entry = {
            "source_unit_id": source_unit_id,
            "priority": priority,
            "coverage_status": coverage_status,
            "covered_by_slide_ids": sorted(set(covered_by_slide_ids)),
            "covered_by_claim_ids": sorted(set(covered_by_claim_ids)),
            "omission_reason": omission_reason,
        }
        for i, existing in enumerate(self.data["entries"]):
            if existing["source_unit_id"] == source_unit_id:
                self.data["entries"][i] = entry
                return entry
        self.data["entries"].append(entry)
        return entry

    def unaccounted_high_priority(self) -> list[str]:
        return [
            e["source_unit_id"]
            for e in self.data["entries"]
            if e["priority"] == "HIGH" and e["coverage_status"] == "unaccounted"
        ]

    def accounted_unit_ids(self) -> set[str]:
        return {e["source_unit_id"] for e in self.data["entries"]}


def validate_source_coverage(
    data: Any,
    *,
    known_unit_ids: set[str] | None = None,
    known_claim_ids: set[str] | None = None,
) -> list[str]:
    errors: list[str] = []
    if not isinstance(data, dict):
        return ["source coverage must be a JSON object"]
    if data.get("schema_version") != SCHEMA_VERSION:
        errors.append(f"schema_version must be {SCHEMA_VERSION!r}")
    project_id = data.get("project_id")
    if not isinstance(project_id, str) or not _PROJECT_ID_RE.match(project_id or ""):
        errors.append("project_id must match ^[A-Za-z0-9._-]+$")

    entries = data.get("entries")
    if not isinstance(entries, list):
        errors.append("entries must be a list")
        entries = []
    seen: set[str] = set()
    for i, entry in enumerate(entries):
        if not isinstance(entry, dict):
            errors.append(f"entries[{i}] must be an object")
            continue
        unit_id = entry.get("source_unit_id")
        if not isinstance(unit_id, str) or not _UNIT_ID_RE.match(unit_id or ""):
            errors.append(f"entries[{i}].source_unit_id must match ^su:<source_id>:<hex>$")
        elif unit_id in seen:
            errors.append(f"duplicate accounting for source_unit_id: {unit_id} (would inflate coverage)")
        else:
            seen.add(unit_id)
        if known_unit_ids is not None and isinstance(unit_id, str) and unit_id not in known_unit_ids:
            errors.append(f"entries[{i}].source_unit_id references unknown unit: {unit_id!r}")
        if entry.get("priority") not in PRIORITIES:
            errors.append(f"entries[{i}].priority must be one of {PRIORITIES}")
        if entry.get("coverage_status") not in COVERAGE_STATUSES:
            errors.append(f"entries[{i}].coverage_status must be one of {COVERAGE_STATUSES}")
        if entry.get("coverage_status") == "intentionally_omitted" and not entry.get("omission_reason"):
            errors.append(f"entries[{i}]: intentionally_omitted requires a non-empty omission_reason")
        # A speaker-notes-only unit must actually point at the speaker-note
        # claim(s) that carry it, otherwise "covered in the notes" would be an
        # unverifiable assertion (Phase 12.3, docs/source-grounding.md §18).
        if entry.get("coverage_status") == "speaker_notes_only":
            note_claims = entry.get("covered_by_claim_ids")
            if not isinstance(note_claims, list) or not note_claims:
                errors.append(
                    f"entries[{i}]: speaker_notes_only requires at least one covered_by_claim_ids entry"
                )
        for claim_id in entry.get("covered_by_claim_ids") or []:
            if not isinstance(claim_id, str) or not _CLAIM_ID_RE.match(claim_id or ""):
                errors.append(f"entries[{i}].covered_by_claim_ids contains an invalid id: {claim_id!r}")
            elif known_claim_ids is not None and claim_id not in known_claim_ids:
                errors.append(f"entries[{i}].covered_by_claim_ids references unknown claim: {claim_id!r}")

    if known_unit_ids is not None:
        missing = known_unit_ids - seen
        for unit_id in sorted(missing):
            errors.append(f"source unit has no coverage accounting at all: {unit_id}")

    _reject_credentials(data, errors)
    return errors


# ---------------------------------------------------------------------------
# SourceGroundedQaReport
# ---------------------------------------------------------------------------
def build_grounded_qa_report(
    project_id: str,
    inventory: SourceInventory,
    traceability: ClaimTraceability,
    coverage: SourceCoverage,
    known_slide_ids: set[str],
    *,
    semantic_findings: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Assemble the final report. Deterministic findings are computed here;
    semantic findings are supplied by the caller (AGY) verbatim and never
    inferred.
    """
    unit_ids = inventory.unit_ids()
    claim_ids = traceability.claim_ids()

    dangling_source_references: list[str] = []
    dangling_slide_references: list[str] = []
    invalid_references: list[str] = []
    for claim in traceability.data.get("claims", []):
        for unit_id in claim.get("source_unit_ids", []):
            if unit_id not in unit_ids:
                dangling_source_references.append(f"{claim.get('claim_id')} -> {unit_id}")
        if claim.get("slide_id") not in known_slide_ids:
            dangling_slide_references.append(f"{claim.get('claim_id')} -> {claim.get('slide_id')}")

    for entry in coverage.data.get("entries", []):
        if entry.get("source_unit_id") not in unit_ids:
            invalid_references.append(f"coverage -> {entry.get('source_unit_id')}")
        for claim_id in entry.get("covered_by_claim_ids", []):
            if claim_id not in claim_ids:
                invalid_references.append(f"coverage({entry.get('source_unit_id')}) -> {claim_id}")

    high_priority_omissions = coverage.unaccounted_high_priority()

    report = {
        "schema_version": SCHEMA_VERSION,
        "project_id": project_id,
        "generated_at": now_iso(),
        "summary": {
            "total_source_units": len(inventory.data.get("units", [])),
            "total_claims": len(traceability.data.get("claims", [])),
            "high_priority_units": sum(
                1 for u in inventory.data.get("units", []) if u.get("priority") == "HIGH"
            ),
        },
        "deterministic_findings": {
            "dangling_source_references": dangling_source_references,
            "dangling_slide_references": dangling_slide_references,
            "high_priority_omissions": high_priority_omissions,
            "invalid_references": invalid_references,
        },
        "semantic_findings": semantic_findings or {
            "unsupported_claims": traceability.unsupported_claim_ids(),
            "numeric_findings": [],
            "modal_findings": [],
            "agy_qa_outcome": None,
        },
    }
    return report


def grounded_qa_path(workspace_root: str | Path) -> Path:
    return Path(workspace_root) / SOURCE_GROUNDED_QA_FILENAME


def save_grounded_qa_report(workspace_root: str | Path, report: dict[str, Any]) -> Path:
    errors = validate_source_grounded_qa(report)
    if errors:
        raise GroundedQaIncomplete("refusing to save invalid grounded QA report: " + "; ".join(errors))
    path = grounded_qa_path(workspace_root)
    _atomic_write_json(path, report)
    return path


def load_grounded_qa_report(workspace_root: str | Path) -> dict[str, Any]:
    path = grounded_qa_path(workspace_root)
    if not path.exists():
        raise GroundedQaIncomplete(f"grounded QA report not found: {path}")
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise GroundedQaIncomplete(f"grounded QA report is corrupt and was not overwritten: {exc}")
    errors = validate_source_grounded_qa(data)
    if errors:
        raise GroundedQaIncomplete("; ".join(errors))
    return data


def validate_source_grounded_qa(data: Any) -> list[str]:
    errors: list[str] = []
    if not isinstance(data, dict):
        return ["grounded QA report must be a JSON object"]
    if data.get("schema_version") != SCHEMA_VERSION:
        errors.append(f"schema_version must be {SCHEMA_VERSION!r}")
    project_id = data.get("project_id")
    if not isinstance(project_id, str) or not _PROJECT_ID_RE.match(project_id or ""):
        errors.append("project_id must match ^[A-Za-z0-9._-]+$")
    if not isinstance(data.get("generated_at"), str):
        errors.append("generated_at must be a string")

    det = data.get("deterministic_findings")
    if not isinstance(det, dict):
        errors.append("deterministic_findings must be an object")
    else:
        for key in (
            "dangling_source_references",
            "dangling_slide_references",
            "high_priority_omissions",
            "invalid_references",
        ):
            if not isinstance(det.get(key), list):
                errors.append(f"deterministic_findings.{key} must be a list")

    sem = data.get("semantic_findings")
    if not isinstance(sem, dict):
        errors.append("semantic_findings must be an object")
    else:
        outcome = sem.get("agy_qa_outcome")
        if outcome not in AGY_QA_OUTCOMES:
            errors.append(f"semantic_findings.agy_qa_outcome must be one of {AGY_QA_OUTCOMES}")

    _reject_credentials(data, errors)
    return errors


# ---------------------------------------------------------------------------
# Phase 12.3 -- workflow integration layer
#
# One core implementation (:func:`evaluate_assembly_gate`); everything else
# (the backward-compatible :func:`assembly_precondition_errors`, the
# ``validate_source_grounding.py`` CLI adapter) delegates to it. There is
# deliberately no second copy of this validation logic anywhere.
# ---------------------------------------------------------------------------

#: AGY semantic Content-QA outcomes that are acceptable for assembly.
ACCEPTED_QA_OUTCOMES = ("passed", "passed_with_notes")

#: Support statuses that still need an explicit AGY resolution before
#: assembly. ``partially_supported`` is deliberately NOT here: it is already
#: an explicit AGY decision (normally paired with an ``evidence_note``),
#: whereas ``unsupported`` and ``pending_review`` mean "not yet resolved".
UNRESOLVED_SUPPORT_STATUSES = ("unsupported", "pending_review")


def unresolved_claim_ids(traceability: "ClaimTraceability") -> list[str]:
    """Claims whose AGY support decision is still unresolved.

    A source-driven deck must not be assembled while a factual claim is still
    ``unsupported`` or ``pending_review``. Resolution is always an AGY action
    (revise the claim, map an additional source unit, remove the claim, or
    confirm support after review) -- this module only detects the unresolved
    state and hands control back.
    """
    return [
        c["claim_id"]
        for c in traceability.data.get("claims", [])
        if c.get("support_status") in UNRESOLVED_SUPPORT_STATUSES
    ]


def verify_source_digests(
    inventory: "SourceInventory", current_source_digests: dict[str, str]
) -> list[str]:
    """Compare recorded source digests against freshly computed ones.

    ``current_source_digests`` maps ``source_id`` -> current sha256 hex digest.
    AGY (or whatever re-reads the source) computes these; this module never
    reads the source document itself. A mismatch means previously persisted
    traceability/coverage/QA evidence describes a different revision of the
    source and must not be silently reused.
    """
    errors: list[str] = []
    for source in inventory.data.get("sources", []):
        source_id = source.get("source_id")
        recorded = source.get("source_digest")
        if recorded is None:
            continue
        current = current_source_digests.get(source_id)
        if current is None:
            continue
        if current != recorded:
            errors.append(
                f"{ERROR_SOURCE_CHANGED}: source {source_id} digest changed "
                f"(recorded {recorded[:12]}..., current {current[:12]}...); "
                "existing grounding evidence is stale and must be revalidated"
            )
    return errors


@dataclass
class GroundingGateResult:
    """Structured outcome of the deterministic grounding gate."""

    enabled: bool
    ready: bool
    errors: list[str]
    error_codes: list[str]

    def to_dict(self) -> dict[str, Any]:
        return {
            "source_grounding_enabled": self.enabled,
            "ready": self.ready,
            "errors": list(self.errors),
            "error_codes": sorted(set(self.error_codes)),
        }


def evaluate_assembly_gate(
    workspace_root: str | Path,
    known_slide_ids: set[str],
    *,
    current_source_digests: dict[str, str] | None = None,
    require_grounded_qa: bool = True,
) -> GroundingGateResult:
    """The single deterministic grounding gate AGY calls before assembly.

    When source grounding is disabled (no ``source_inventory.json``, or
    ``enabled: false``) this returns ``ready=True`` immediately: a purely
    creative deck is never forced through this workflow.

    When enabled, it checks -- structurally only, never semantically:

    * ``source_inventory.json`` / ``claim_traceability.json`` /
      ``source_coverage.json`` load and validate
    * no dangling ``source_unit_id`` / ``slide_id`` references
    * coverage accounting is complete and not inflated
    * no HIGH-priority source unit left ``unaccounted``
    * no claim left ``unsupported`` / ``pending_review``
    * source digests still match (stale-evidence detection)
    * ``source_grounded_qa.json`` exists, is structurally valid, and AGY's own
      ``semantic_findings.agy_qa_outcome`` is an accepted value

    A failure here is a **grounding precondition failure**, not an assembly
    failure: ``assemble_ppt.py`` is never invoked, so this must not be
    confused with, or recorded as, the Phase 9 assembly-failure recovery path.
    It is also not a project blocker on its own -- it is a recoverable AGY
    workflow issue handed back for repair.
    """
    if not source_grounding_enabled(workspace_root):
        return GroundingGateResult(enabled=False, ready=True, errors=[], error_codes=[])

    errors: list[str] = []
    codes: list[str] = []

    try:
        inventory = SourceInventory.load(workspace_root)
    except SourceGroundingError as exc:
        return GroundingGateResult(
            enabled=True,
            ready=False,
            errors=[f"source_inventory.json invalid: {exc}"],
            error_codes=[exc.error_code],
        )

    try:
        traceability = ClaimTraceability.load(workspace_root)
    except SourceGroundingError as exc:
        return GroundingGateResult(
            enabled=True,
            ready=False,
            errors=[f"claim_traceability.json invalid: {exc}"],
            error_codes=[exc.error_code],
        )

    try:
        coverage = SourceCoverage.load(workspace_root)
    except SourceGroundingError as exc:
        return GroundingGateResult(
            enabled=True,
            ready=False,
            errors=[f"source_coverage.json invalid: {exc}"],
            error_codes=[exc.error_code],
        )

    trace_errors = validate_claim_traceability(
        traceability.data, known_unit_ids=inventory.unit_ids(), known_slide_ids=known_slide_ids
    )
    if trace_errors:
        errors.append("claim_traceability.json has dangling/invalid references: " + "; ".join(trace_errors))
        codes.append(ERROR_TRACEABILITY_INVALID)

    coverage_errors = validate_source_coverage(
        coverage.data, known_unit_ids=inventory.unit_ids(), known_claim_ids=traceability.claim_ids()
    )
    if coverage_errors:
        errors.append("source_coverage.json has accounting problems: " + "; ".join(coverage_errors))
        codes.append(ERROR_SOURCE_COVERAGE_INCOMPLETE)

    unaccounted_high = coverage.unaccounted_high_priority()
    if unaccounted_high:
        errors.append(f"HIGH priority source units are unaccounted: {sorted(unaccounted_high)}")
        codes.append(ERROR_SOURCE_COVERAGE_INCOMPLETE)

    unresolved = unresolved_claim_ids(traceability)
    if unresolved:
        errors.append(
            f"claims still need an explicit AGY resolution (unsupported/pending_review): {sorted(unresolved)}"
        )
        codes.append(ERROR_TRACEABILITY_INVALID)

    if current_source_digests:
        digest_errors = verify_source_digests(inventory, current_source_digests)
        if digest_errors:
            errors.extend(digest_errors)
            codes.append(ERROR_SOURCE_CHANGED)

    if require_grounded_qa:
        try:
            report = load_grounded_qa_report(workspace_root)
        except SourceGroundingError as exc:
            errors.append(f"source_grounded_qa.json not usable: {exc}")
            codes.append(exc.error_code)
        else:
            outcome = report.get("semantic_findings", {}).get("agy_qa_outcome")
            if outcome not in ACCEPTED_QA_OUTCOMES:
                errors.append(
                    f"AGY Content QA outcome is {outcome!r}; assembly requires one of "
                    f"{list(ACCEPTED_QA_OUTCOMES)}"
                )
                codes.append(ERROR_GROUNDED_QA_INCOMPLETE)

    return GroundingGateResult(
        enabled=True, ready=not errors, errors=errors, error_codes=codes
    )


def assembly_precondition_errors(
    workspace_root: str | Path,
    known_slide_ids: set[str],
    *,
    current_source_digests: dict[str, str] | None = None,
    require_grounded_qa: bool = True,
) -> list[str]:
    """Backward-compatible thin wrapper over :func:`evaluate_assembly_gate`.

    Returns an empty list when source grounding is disabled or when the gate
    is fully satisfied. Kept as a list-returning helper because that is the
    shape earlier Phase 12.2 callers/tests already use; the logic itself lives
    only in :func:`evaluate_assembly_gate`.
    """
    return evaluate_assembly_gate(
        workspace_root,
        known_slide_ids,
        current_source_digests=current_source_digests,
        require_grounded_qa=require_grounded_qa,
    ).errors


if __name__ == "__main__":  # pragma: no cover - thin CLI shim
    import argparse

    parser = argparse.ArgumentParser(description="AGY PPT source-grounding sidecar validator")
    parser.add_argument("workspace_root")
    parser.add_argument("--check-assembly", action="store_true")
    args = parser.parse_args()

    if args.check_assembly:
        try:
            state_slide_ids: set[str] = set()
            import project_state as _ps  # local import to avoid a hard dependency at module load time

            state = _ps.ProjectState.load(args.workspace_root)
            state_slide_ids = set(state.data["slides"].keys())
        except Exception as exc:  # noqa: BLE001 - best-effort CLI helper only
            print(json.dumps({"error": f"could not load project_state.json: {exc}"}, indent=2))
            raise SystemExit(2)
        result = evaluate_assembly_gate(args.workspace_root, state_slide_ids)
        print(json.dumps(result.to_dict(), ensure_ascii=False, indent=2))
        raise SystemExit(0 if result.ready else 1)

    enabled = source_grounding_enabled(args.workspace_root)
    print(json.dumps({"source_grounding_enabled": enabled}, indent=2))
