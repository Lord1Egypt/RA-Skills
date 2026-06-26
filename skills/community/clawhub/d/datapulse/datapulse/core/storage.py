"""Persistence for structured records and markdown output."""

from __future__ import annotations

import json
import os
from dataclasses import asdict, dataclass, field
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

from .models import DataPulseItem
from .triage import normalize_review_state
from .utils import content_fingerprint, content_hash, get_domain_tag


class UnifiedInbox:
    """Append-only JSON memory with bounded size and deduplication."""

    def __init__(self, path: str):
        self.path: Path = Path(path)
        self.items: list[DataPulseItem] = []
        self._fingerprints: set[str] = set()
        self.max_items = int(os.getenv("DATAPULSE_MAX_INBOX", "500"))
        self.max_days = int(os.getenv("DATAPULSE_KEEP_DAYS", "30"))
        self._load()

    def _load(self) -> None:
        if not self.path.exists():
            self.items = []
            return

        try:
            data = json.loads(self.path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            self.items = []
            return

        loaded = []
        for row in data if isinstance(data, list) else []:
            try:
                loaded.append(DataPulseItem.from_dict(row))
            except (KeyError, TypeError, ValueError):
                continue
        self.items = loaded
        self._prune()
        self._rebuild_fingerprints()

    def _prune(self) -> None:
        cutoff = datetime.now(timezone.utc) - timedelta(days=max(0, self.max_days))
        retained: list[DataPulseItem] = []
        for item in self.items:
            try:
                ts = datetime.fromisoformat(item.fetched_at)
            except Exception:
                retained.append(item)
                continue
            if ts.tzinfo is None:
                ts = ts.replace(tzinfo=timezone.utc)
            else:
                ts = ts.astimezone(timezone.utc)
            if ts >= cutoff:
                retained.append(item)

        # Deduplicate
        dedup: dict[str, DataPulseItem] = {}
        for item in retained:
            dedup[item.id] = item

        ordered = sorted(dedup.values(), key=lambda i: i.fetched_at, reverse=True)
        self.items = ordered[: self.max_items]
        self._rebuild_fingerprints()

    def _rebuild_fingerprints(self) -> None:
        """Rebuild fingerprint set from current items."""
        self._fingerprints = set()
        for item in self.items:
            if len(item.content) >= 50:
                self._fingerprints.add(content_fingerprint(item.content))

    def add(self, item: DataPulseItem, *, fingerprint_dedup: bool = True) -> bool:
        # ID dedup (existing behaviour)
        if any(existing.id == item.id for existing in self.items):
            return False
        # Fingerprint dedup for content >= 50 chars
        if fingerprint_dedup and len(item.content) >= 50:
            fp = content_fingerprint(item.content)
            if fp in self._fingerprints:
                return False
            self._fingerprints.add(fp)
        self.items.append(item)
        self.items.sort(key=lambda i: i.fetched_at, reverse=True)
        self.items = self.items[: self.max_items]
        return True

    def save(self) -> None:
        self._prune()
        payload = [item.to_dict() for item in self.items]
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")

    def query(self, limit: int = 20, min_confidence: float = 0.0) -> list[DataPulseItem]:
        filtered = [item for item in self.items if item.confidence >= min_confidence]
        return sorted(filtered, key=lambda i: i.confidence, reverse=True)[:limit]

    def all_items(self, min_confidence: float = 0.0) -> list[DataPulseItem]:
        return [item for item in self.items if item.confidence >= min_confidence]

    def get(self, item_id: str) -> DataPulseItem | None:
        for item in self.items:
            if item.id == item_id:
                return item
        return None

    def delete(self, item_id: str) -> DataPulseItem | None:
        for index, item in enumerate(self.items):
            if item.id != item_id:
                continue
            removed = self.items.pop(index)
            self._rebuild_fingerprints()
            return removed
        return None

    def mark_processed(self, item_id: str, processed: bool = True) -> bool:
        for item in self.items:
            if item.id == item_id:
                item.processed = processed
                if processed and item.review_state == "new":
                    item.review_state = "triaged"
                elif not processed and item.review_state == "triaged":
                    item.review_state = normalize_review_state("", processed=False)
                return True
        return False

    def query_unprocessed(self, limit: int = 20, min_confidence: float = 0.0) -> list[DataPulseItem]:
        filtered = [
            item for item in self.items
            if not item.processed and item.confidence >= min_confidence
        ]
        return sorted(filtered, key=lambda i: i.confidence, reverse=True)[:limit]


@dataclass
class MarkdownProjectionResult:
    """Fail-open result for Markdown projection sinks."""

    mode: str
    status: str
    reason: str = ""
    target_paths: list[str] = field(default_factory=list)
    written_paths: list[str] = field(default_factory=list)
    failures: list[dict[str, str]] = field(default_factory=list)

    @property
    def primary_path(self) -> str | None:
        return self.written_paths[0] if self.written_paths else None

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def _direct_markdown_target_from_env() -> Path | None:
    explicit = os.getenv("DATAPULSE_MARKDOWN_PATH", "").strip()
    if not explicit:
        return None
    return Path(explicit).expanduser()


def _obsidian_markdown_target_from_env() -> Path | None:
    vault = os.getenv("OBSIDIAN_VAULT", "").strip()
    if not vault:
        return None
    return Path(vault).expanduser() / "01-收集箱" / "datapulse-inbox.md"


def _output_markdown_target_from_env() -> Path | None:
    output_dir = os.getenv("OUTPUT_DIR", "").strip()
    if not output_dir:
        return None
    return Path(output_dir).expanduser() / "datapulse-hub.md"


def _storage_markdown_target(path: str | None = None) -> Path | None:
    if path:
        return Path(path).expanduser()
    return _direct_markdown_target_from_env() or _output_markdown_target_from_env()


def _normalize_projection_mode(mode: str | None) -> str:
    normalized = str(mode or "").strip().lower() or "auto"
    if normalized in {"auto", "disabled", "obsidian", "storage", "hybrid"}:
        return normalized
    return "auto"


def _dedupe_targets(targets: list[Path]) -> list[Path]:
    unique: list[Path] = []
    seen: set[str] = set()
    for target in targets:
        key = str(target.expanduser())
        if key in seen:
            continue
        seen.add(key)
        unique.append(target)
    return unique


def _projection_targets(*, mode: str, path: str | None = None) -> list[Path]:
    if path:
        return [Path(path).expanduser()]
    if mode == "disabled":
        return []
    if mode == "auto":
        direct_target = _direct_markdown_target_from_env()
        if direct_target is not None:
            return [direct_target]
        obsidian_target = _obsidian_markdown_target_from_env()
        if obsidian_target is not None:
            return [obsidian_target]
        output_target = _output_markdown_target_from_env()
        if output_target is not None:
            return [output_target]
        return []
    if mode == "obsidian":
        target = _obsidian_markdown_target_from_env()
        return [target] if target is not None else []
    if mode == "storage":
        target = _storage_markdown_target()
        return [target] if target is not None else []
    return _dedupe_targets(
        [
            target
            for target in (
                _obsidian_markdown_target_from_env(),
                _storage_markdown_target(),
            )
            if target is not None
        ]
    )


def _append_markdown(target: Path, item: DataPulseItem) -> None:
    target.parent.mkdir(parents=True, exist_ok=True)
    snippet = item.content[:1800].replace("\n", "\n")
    excerpt = item.confidence_factors or []
    with target.open("a", encoding="utf-8") as f:
        f.write(f"\n## [{item.title}]({item.url})\n")
        f.write(f"- source: {item.source_name} / {item.source_type.value}\n")
        f.write(f"- fetched: {item.fetched_at[:16]}\n")
        f.write(f"- confidence: {item.confidence:.3f}\n")
        f.write(f"- tags: {', '.join(item.tags)}\n")
        f.write(f"- factors: {', '.join(excerpt)}\n")
        f.write(f"\n{snippet}\n")
        f.write("\n---\n")


def project_markdown(
    item: DataPulseItem,
    *,
    mode: str | None = None,
    path: str | None = None,
) -> MarkdownProjectionResult:
    requested_mode = mode or os.getenv("DATAPULSE_MARKDOWN_PROJECTION", "auto")
    normalized_mode = _normalize_projection_mode(requested_mode)
    targets = _projection_targets(mode=normalized_mode, path=path)

    if not targets:
        if normalized_mode == "disabled":
            reason = "projection_disabled"
            status = "disabled"
        elif normalized_mode == "auto":
            reason = "no_projection_target_configured"
            status = "disabled"
        else:
            reason = "projection_target_unavailable"
            status = "degraded"
        return MarkdownProjectionResult(
            mode=normalized_mode,
            status=status,
            reason=reason,
            target_paths=[],
        )

    target_paths = [str(target) for target in targets]
    written_paths: list[str] = []
    failures: list[dict[str, str]] = []

    for target in targets:
        try:
            _append_markdown(target, item)
            written_paths.append(str(target))
        except OSError as exc:
            failures.append({"path": str(target), "error": str(exc)})

    if failures:
        reason = "projection_partial_failure" if written_paths else "projection_write_failed"
        status = "degraded"
    else:
        reason = "projection_completed"
        status = "projected"

    return MarkdownProjectionResult(
        mode=normalized_mode,
        status=status,
        reason=reason,
        target_paths=target_paths,
        written_paths=written_paths,
        failures=failures,
    )


def save_markdown(item: DataPulseItem, path: str | None = None) -> str | None:
    return project_markdown(item, path=path).primary_path


def output_record_md(item: DataPulseItem) -> str:
    """Build markdown document content for one record."""
    domain = get_domain_tag(item.url)
    lines: list[str] = [
        "---",
        f"id: {item.id}",
        f"source_type: {item.source_type.value}",
        f"source_name: {item.source_name}",
        f"title: {item.title}",
        f"url: {item.url}",
        f"fetched_at: {item.fetched_at}",
        f"parser: {item.parser}",
        f"language: {item.language}",
        f"confidence: {item.confidence}",
        f"domain: {domain}",
        f"content_hash: {content_hash(item.content)}",
        "---",
        "",
        f"# {item.title}",
        "",
        f"- Source: {item.source_name}",
        f"- URL: {item.url}",
        f"- Confidence: {item.confidence:.3f}",
        f"- Parser reliability hints: {', '.join(item.confidence_factors)}",
        "",
        item.content,
    ]
    return "\n".join(lines)
