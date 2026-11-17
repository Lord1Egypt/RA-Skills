"""Verify Zotero collection ingest allocation, provenance, and page hygiene."""

from __future__ import annotations

import json
import re
from collections.abc import Mapping
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml

from .plan import load_snapshot

_ALLOWED_STATUSES = {"ingested", "allocated_elsewhere", "omitted"}
_CONTROL_RE = re.compile(r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]")
_PRIVATE_PATH_RE = re.compile(
    r"(?:[A-Za-z]:\\Users\\[^\r\n]+|/(?:Users|home)/[^/\r\n]+)",
    flags=re.IGNORECASE,
)
_TRAILING_RE = re.compile(r"[ \t]+$", flags=re.MULTILINE)
_HEADING_RE = re.compile(r"^##\s+(.+?)\s*$", flags=re.MULTILINE)
_ITEM_KEY_RE = re.compile(r"^[A-Z0-9]{8}$")


class IngestVerificationError(ValueError):
    """Raised when an allocation ledger cannot be interpreted safely."""


@dataclass(frozen=True)
class Allocation:
    item_index: int
    item_key: str
    status: str
    pages: tuple[str, ...] = ()
    omission_reason: str = ""


@dataclass(frozen=True)
class IngestIssue:
    severity: str
    code: str
    message: str
    item_key: str = ""
    page: str = ""


@dataclass(frozen=True)
class IngestVerificationReport:
    collection_key: str
    snapshot_count: int
    allocation_count: int
    errors: tuple[IngestIssue, ...]
    warnings: tuple[IngestIssue, ...]

    @property
    def passed(self) -> bool:
        return not self.errors


@dataclass(frozen=True)
class _PageAudit:
    stem: str
    frontmatter: Mapping[str, Any]
    text: str
    headings: tuple[str, ...]
    knowledge_length: int


def _load_structured(path: Path) -> Mapping[str, Any]:
    source = Path(path)
    try:
        if source.suffix.lower() == ".json":
            data = json.loads(source.read_text(encoding="utf-8"))
        else:
            data = yaml.safe_load(source.read_text(encoding="utf-8"))
    except (OSError, ValueError, TypeError, yaml.YAMLError) as exc:
        raise IngestVerificationError(
            "allocation ledger is unreadable or invalid YAML/JSON"
        ) from exc
    if not isinstance(data, Mapping):
        raise IngestVerificationError("allocation ledger root must be a mapping")
    return data


def _normalize_page(value: Any) -> str:
    raw = str(value or "").strip().replace("\\", "/")
    if not raw:
        raise IngestVerificationError("allocation page name cannot be empty")
    path = Path(raw)
    if path.is_absolute() or ".." in path.parts:
        raise IngestVerificationError(
            "allocation page must be a wiki-relative page stem"
        )
    raw = raw.removeprefix("wiki/")
    if "/" in raw:
        raise IngestVerificationError("allocation page must not contain subdirectories")
    if raw.lower().endswith(".md"):
        raw = raw[:-3]
    if not raw:
        raise IngestVerificationError("allocation page stem cannot be empty")
    return raw


def load_allocation_ledger(path: Path) -> tuple[str, int, tuple[Allocation, ...]]:
    data = _load_structured(path)
    unknown_root = sorted(set(data) - {"version", "collection", "allocations"})
    if unknown_root:
        raise IngestVerificationError(
            f"allocation ledger contains unknown fields: {unknown_root}"
        )
    if data.get("version") != 1:
        raise IngestVerificationError("allocation ledger must declare version: 1")
    collection = data.get("collection") or {}
    if not isinstance(collection, Mapping):
        raise IngestVerificationError("allocation collection must be a mapping")
    unknown_collection = sorted(set(collection) - {"key", "snapshot_count"})
    if unknown_collection:
        raise IngestVerificationError(
            f"allocation collection contains unknown fields: {unknown_collection}"
        )
    collection_key = str(collection.get("key") or "").strip().upper()
    snapshot_count = collection.get("snapshot_count")
    if not _ITEM_KEY_RE.fullmatch(collection_key):
        raise IngestVerificationError(
            "allocation collection.key must be 8 ASCII letters/digits"
        )
    if not isinstance(snapshot_count, int) or snapshot_count < 0:
        raise IngestVerificationError(
            "allocation collection.snapshot_count must be a non-negative integer"
        )

    raw_allocations = data.get("allocations")
    if not isinstance(raw_allocations, list):
        raise IngestVerificationError("allocations must be a list")
    allocations: list[Allocation] = []
    for index, raw in enumerate(raw_allocations):
        if not isinstance(raw, Mapping):
            raise IngestVerificationError(f"allocations[{index}] must be a mapping")
        unknown = sorted(
            set(raw) - {"item_index", "item_key", "status", "pages", "omission_reason"}
        )
        if unknown:
            raise IngestVerificationError(
                f"allocations[{index}] contains unknown fields: {unknown}"
            )
        item_index = raw.get("item_index")
        if not isinstance(item_index, int) or item_index < 1:
            raise IngestVerificationError(
                f"allocations[{index}].item_index must be a positive integer"
            )
        item_key = str(raw.get("item_key") or "").strip().upper()
        if not _ITEM_KEY_RE.fullmatch(item_key):
            raise IngestVerificationError(f"allocations[{index}].item_key is invalid")
        status = str(raw.get("status") or "").strip()
        if status not in _ALLOWED_STATUSES:
            raise IngestVerificationError(
                f"allocations[{index}].status must be one of {sorted(_ALLOWED_STATUSES)}"
            )
        raw_pages = raw.get("pages") or []
        if isinstance(raw_pages, str):
            raw_pages = [raw_pages]
        if not isinstance(raw_pages, list):
            raise IngestVerificationError(f"allocations[{index}].pages must be a list")
        pages = tuple(_normalize_page(value) for value in raw_pages)
        if len(pages) != len(set(pages)):
            raise IngestVerificationError(
                f"allocations[{index}].pages contains duplicates"
            )
        allocations.append(
            Allocation(
                item_index=item_index,
                item_key=item_key,
                status=status,
                pages=pages,
                omission_reason=str(raw.get("omission_reason") or "").strip(),
            )
        )
    return collection_key, snapshot_count, tuple(allocations)


def _issue(
    severity: str,
    code: str,
    message: str,
    *,
    item_key: str = "",
    page: str = "",
) -> IngestIssue:
    return IngestIssue(severity, code, message, item_key=item_key, page=page)


def _split_frontmatter(text: str) -> tuple[Mapping[str, Any], str]:
    normalized = text.lstrip("\ufeff").replace("\r\n", "\n").replace("\r", "\n")
    if not normalized.startswith("---\n"):
        raise IngestVerificationError("page is missing YAML frontmatter")
    end = normalized.find("\n---\n", 4)
    if end < 0:
        raise IngestVerificationError("page frontmatter is not terminated")
    raw = normalized[4:end]
    try:
        frontmatter = yaml.safe_load(raw) or {}
    except yaml.YAMLError as exc:
        raise IngestVerificationError("page frontmatter is invalid YAML") from exc
    if not isinstance(frontmatter, Mapping):
        raise IngestVerificationError("page frontmatter must be a mapping")
    return frontmatter, normalized[end + 5 :]


def _audit_page(path: Path) -> tuple[_PageAudit | None, list[IngestIssue]]:
    issues: list[IngestIssue] = []
    stem = path.stem
    try:
        raw = path.read_bytes()
        text = raw.decode("utf-8-sig")
    except (OSError, UnicodeDecodeError):
        return None, [
            _issue(
                "error",
                "unreadable-page",
                "allocated page is not readable UTF-8",
                page=stem,
            )
        ]

    scan_text = text.replace("\r\n", "\n").replace("\r", "\n")
    if _CONTROL_RE.search(scan_text):
        issues.append(
            _issue(
                "error",
                "control-character",
                "page contains forbidden control characters",
                page=stem,
            )
        )
    if _TRAILING_RE.search(scan_text):
        issues.append(
            _issue(
                "error",
                "trailing-whitespace",
                "page contains trailing spaces or tabs",
                page=stem,
            )
        )
    if _PRIVATE_PATH_RE.search(scan_text):
        issues.append(
            _issue(
                "error",
                "private-path-leak",
                "page contains a machine-specific user path",
                page=stem,
            )
        )

    try:
        frontmatter, body = _split_frontmatter(text)
    except IngestVerificationError as exc:
        issues.append(_issue("error", "invalid-frontmatter", str(exc), page=stem))
        return None, issues

    if not re.search(r"^#\s+\S", body, flags=re.MULTILINE):
        issues.append(
            _issue("error", "missing-title", "page is missing an H1 title", page=stem)
        )
    h1 = re.search(r"^#\s+.+?$", body, flags=re.MULTILINE)
    first_h2 = re.search(r"^##\s+", body, flags=re.MULTILINE)
    definition = ""
    if h1:
        end = first_h2.start() if first_h2 else len(body)
        definition = body[h1.end() : end].strip().lstrip(">").strip()
    if len(definition) < 20:
        issues.append(
            _issue(
                "error",
                "missing-definition",
                "page lacks a one-sentence definition",
                page=stem,
            )
        )

    headings = tuple(match.strip() for match in _HEADING_RE.findall(body))
    normalized_headings = {heading.casefold() for heading in headings}
    required = {
        "related": {"related pages", "相关页面"},
        "sources": {"sources", "来源"},
        "changelog": {"changelog", "变更日志"},
    }
    for code, aliases in required.items():
        if not normalized_headings & aliases:
            issues.append(
                _issue(
                    "error",
                    f"missing-{code}",
                    f"page is missing the {code} section",
                    page=stem,
                )
            )

    invariant_aliases = set().union(*required.values())
    knowledge_headings = [
        heading for heading in headings if heading.casefold() not in invariant_aliases
    ]
    if not knowledge_headings:
        issues.append(
            _issue(
                "error",
                "missing-knowledge-content",
                "page has no source-dependent knowledge section",
                page=stem,
            )
        )
    knowledge_length = 0
    for heading in knowledge_headings:
        match = re.search(rf"^##\s+{re.escape(heading)}\s*$", body, flags=re.MULTILINE)
        if not match:
            continue
        next_match = re.search(r"^##\s+", body[match.end() :], flags=re.MULTILINE)
        end = match.end() + next_match.start() if next_match else len(body)
        knowledge_length += len(body[match.end() : end].strip())
    if knowledge_length < 40:
        issues.append(
            _issue(
                "error",
                "shallow-knowledge-content",
                "source-dependent knowledge content is too short",
                page=stem,
            )
        )

    return _PageAudit(stem, frontmatter, text, headings, knowledge_length), issues


def verify_collection_ingest(
    wiki_dir: Path,
    snapshot_path: Path,
    allocation_path: Path,
) -> IngestVerificationReport:
    """Verify one collection snapshot against its allocation ledger and wiki pages."""
    errors: list[IngestIssue] = []
    warnings: list[IngestIssue] = []
    try:
        _, _, snapshot_collection_key, snapshot_items = load_snapshot(
            Path(snapshot_path)
        )
    except (OSError, ValueError, TypeError, yaml.YAMLError) as exc:
        return IngestVerificationReport(
            "",
            0,
            0,
            (_issue("error", "invalid-snapshot", str(exc)),),
            (),
        )
    try:
        collection_key, declared_count, allocations = load_allocation_ledger(
            Path(allocation_path)
        )
    except IngestVerificationError as exc:
        return IngestVerificationReport(
            snapshot_collection_key,
            len(snapshot_items),
            0,
            (_issue("error", "invalid-allocation-ledger", str(exc)),),
            (),
        )

    snapshot_count = len(snapshot_items)
    allocation_count = len(allocations)
    if collection_key != snapshot_collection_key:
        errors.append(
            _issue(
                "error",
                "collection-key-mismatch",
                "snapshot and allocation collection keys differ",
            )
        )
    if declared_count != snapshot_count:
        errors.append(
            _issue(
                "error",
                "snapshot-count-mismatch",
                "declared snapshot_count does not match the snapshot",
            )
        )
    if allocation_count != snapshot_count:
        errors.append(
            _issue(
                "error",
                "allocation-count-mismatch",
                "allocation count does not match the snapshot",
            )
        )

    keys = [allocation.item_key for allocation in allocations]
    indices = [allocation.item_index for allocation in allocations]
    if len(keys) != len(set(keys)):
        errors.append(
            _issue(
                "error",
                "duplicate-item-key",
                "allocation ledger contains duplicate item keys",
            )
        )
    if len(indices) != len(set(indices)):
        errors.append(
            _issue(
                "error",
                "duplicate-item-index",
                "allocation ledger contains duplicate item indices",
            )
        )
    if sorted(set(indices)) != list(range(1, snapshot_count + 1)):
        errors.append(
            _issue(
                "error",
                "item-index-gap",
                "item indices must cover 1..snapshot_count exactly",
            )
        )

    snapshot_keys = {item.item_key for item in snapshot_items}
    allocation_keys = set(keys)
    if snapshot_keys != allocation_keys:
        errors.append(
            _issue(
                "error",
                "snapshot-allocation-mismatch",
                "snapshot and allocation item-key sets differ",
            )
        )

    wiki_root = Path(wiki_dir).resolve()
    page_cache: dict[str, _PageAudit | None] = {}
    for allocation in allocations:
        if allocation.status == "omitted":
            if not allocation.omission_reason:
                errors.append(
                    _issue(
                        "error",
                        "missing-omission-reason",
                        "omitted item lacks a concrete omission reason",
                        item_key=allocation.item_key,
                    )
                )
            if allocation.pages:
                errors.append(
                    _issue(
                        "error",
                        "omitted-item-has-pages",
                        "omitted item must not allocate wiki pages",
                        item_key=allocation.item_key,
                    )
                )
            continue
        if not allocation.pages:
            errors.append(
                _issue(
                    "error",
                    "missing-page-allocation",
                    "non-omitted item must allocate at least one wiki page",
                    item_key=allocation.item_key,
                )
            )
            continue

        for stem in allocation.pages:
            page_path = (wiki_root / f"{stem}.md").resolve()
            try:
                page_path.relative_to(wiki_root)
            except ValueError:
                errors.append(
                    _issue(
                        "error",
                        "page-path-escape",
                        "allocated page resolves outside wiki root",
                        item_key=allocation.item_key,
                        page=stem,
                    )
                )
                continue
            if not page_path.exists():
                errors.append(
                    _issue(
                        "error",
                        "missing-page",
                        "allocated page does not exist",
                        item_key=allocation.item_key,
                        page=stem,
                    )
                )
                continue
            if stem not in page_cache:
                audit, page_issues = _audit_page(page_path)
                page_cache[stem] = audit
                errors.extend(
                    issue for issue in page_issues if issue.severity == "error"
                )
                warnings.extend(
                    issue for issue in page_issues if issue.severity == "warning"
                )
            audit = page_cache[stem]
            if audit is None:
                continue
            sources_meta = audit.frontmatter.get("sources_meta") or []
            if not isinstance(sources_meta, list):
                errors.append(
                    _issue(
                        "error",
                        "invalid-sources-meta",
                        "sources_meta must be a list",
                        item_key=allocation.item_key,
                        page=stem,
                    )
                )
                continue
            bound_keys = [
                str(raw.get("zotero_item_key") or "").strip().upper()
                for raw in sources_meta
                if isinstance(raw, Mapping) and raw.get("zotero_item_key")
            ]
            if len(bound_keys) != len(set(bound_keys)):
                errors.append(
                    _issue(
                        "error",
                        "duplicate-sources-meta",
                        "page contains duplicate Zotero item bindings",
                        page=stem,
                    )
                )
            if bound_keys.count(allocation.item_key) != 1:
                errors.append(
                    _issue(
                        "error",
                        "missing-provenance-binding",
                        "allocated page must bind the item exactly once in sources_meta",
                        item_key=allocation.item_key,
                        page=stem,
                    )
                )

    signature_groups: dict[tuple[str, ...], list[_PageAudit]] = {}
    for audit in page_cache.values():
        if audit is not None:
            signature = tuple(heading.casefold() for heading in audit.headings)
            signature_groups.setdefault(signature, []).append(audit)
    for audits in signature_groups.values():
        if len(audits) < 3:
            continue
        lengths = [audit.knowledge_length for audit in audits]
        if min(lengths) > 0 and max(lengths) / min(lengths) <= 1.2:
            warnings.append(
                _issue(
                    "warning",
                    "template-collapse",
                    "three or more pages share the same section template and near-identical depth; review source-specific structure",
                )
            )

    return IngestVerificationReport(
        collection_key=collection_key,
        snapshot_count=snapshot_count,
        allocation_count=allocation_count,
        errors=tuple(errors),
        warnings=tuple(warnings),
    )


def ingest_report_to_manifest(report: IngestVerificationReport) -> dict[str, Any]:
    """Serialize the verifier result without page contents or private paths."""

    def serialize(issue: IngestIssue) -> dict[str, Any]:
        row: dict[str, Any] = {
            "code": issue.code,
            "message": issue.message,
        }
        if issue.item_key:
            row["item_key"] = issue.item_key
        if issue.page:
            row["page"] = issue.page
        return row

    return {
        "version": 1,
        "mode": "collection-ingest-verification",
        "collection_key": report.collection_key,
        "passed": report.passed,
        "summary": {
            "snapshot_items": report.snapshot_count,
            "allocations": report.allocation_count,
            "errors": len(report.errors),
            "warnings": len(report.warnings),
        },
        "errors": [serialize(issue) for issue in report.errors],
        "warnings": [serialize(issue) for issue in report.warnings],
    }
