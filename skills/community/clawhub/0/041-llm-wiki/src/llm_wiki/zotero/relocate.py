"""Plan and apply controlled Zotero attachment relocation.

The module intentionally separates filesystem work from the Zotero adapter.  It
supports a dry-run without a write key and applies only a verified, in-place
attachment path update.  It never clones or deletes Zotero items and never
edits notes.
"""

from __future__ import annotations

import hashlib
import os
import shutil
import tempfile
from collections.abc import Mapping
from dataclasses import dataclass, field
from pathlib import Path, PurePosixPath
from typing import Any, Protocol

import yaml

from ..agent_logger import get_logger
from ..alias_template import render_alias_template
from ..sanitizer import sanitize_title_stem
from .local import (
    ATTACHMENTS_PREFIX,
    AttachmentRepointResult,
    LocalItem,
    LocalWriteError,
)

LOG = get_logger("zotero_relocate")

DEFAULT_METADATA_PATH = Path("sources") / "zotero" / "metadata.yaml"
DEFAULT_MAX_COMPONENT_BYTES = 120
DEFAULT_MAX_COLLISION_ATTEMPTS = 100
_ALLOWED_SYMLINK_MODES = {"metadata", "copy", "hardlink"}
_SUPPORTED_LINK_MODES = {"linked_file", "imported_file"}


class RelocationError(RuntimeError):
    """Raised when an attachment cannot be relocated safely."""


class AttachmentAdapter(Protocol):
    async def get_item(self, item_key: str) -> LocalItem: ...

    async def repoint_attachment(
        self,
        item_key: str,
        target_path: str,
        *,
        expected_parent_item: str | None = None,
    ) -> AttachmentRepointResult: ...


@dataclass(frozen=True)
class FileFingerprint:
    size: int
    sha256: str


@dataclass(frozen=True)
class RelocationSettings:
    enabled: bool
    root: Path
    storage_root: Path | None
    path_template: str
    max_component_bytes: int = DEFAULT_MAX_COMPONENT_BYTES
    collision_policy: str = "suffix"
    max_collision_attempts: int = DEFAULT_MAX_COLLISION_ATTEMPTS
    delete_source: bool = False
    allowed_source_roots: tuple[Path, ...] = ()
    update_metadata: bool = True
    materialize_aliases: bool = True
    on_symlink_error: str = "metadata"
    base_dir_relative: bool = False

    @classmethod
    def from_mapping(
        cls,
        mapping: Mapping[str, Any],
        *,
        project_root: Path,
        root_override: str | None = None,
        storage_root_override: str | None = None,
        pattern_override: str | None = None,
        delete_source_override: bool = False,
    ) -> RelocationSettings:
        section = dict(mapping or {})
        raw_root = root_override if root_override is not None else section.get("root")
        if not str(raw_root or "").strip():
            raise RelocationError(
                "zotero_relocation.root is required; use an absolute managed attachment root"
            )
        root = _require_absolute_root(raw_root, "zotero_relocation.root")
        project = project_root.resolve()
        if root == project or _is_within(root, project / "sources"):
            raise RelocationError(
                "zotero_relocation.root must not be the project root or inside project sources"
            )

        raw_storage = (
            storage_root_override
            if storage_root_override is not None
            else section.get("storage_root")
        )
        storage_root = (
            _require_absolute_root(raw_storage, "zotero_relocation.storage_root")
            if str(raw_storage or "").strip()
            else None
        )
        raw_allowed = section.get("allowed_source_roots") or []
        if not isinstance(raw_allowed, (list, tuple)):
            raise RelocationError(
                "zotero_relocation.allowed_source_roots must be a list"
            )
        allowed = tuple(
            _require_absolute_root(value, "zotero_relocation.allowed_source_roots")
            for value in raw_allowed
            if str(value or "").strip()
        )
        max_bytes = _positive_int(
            section.get("max_component_bytes", DEFAULT_MAX_COMPONENT_BYTES),
            "max_component_bytes",
        )
        max_attempts = _positive_int(
            section.get("max_collision_attempts", DEFAULT_MAX_COLLISION_ATTEMPTS),
            "max_collision_attempts",
        )
        collision = str(section.get("collision_policy", "suffix")).strip().lower()
        if collision != "suffix":
            raise RelocationError("collision_policy must be 'suffix'")
        symlink_mode = str(section.get("on_symlink_error", "metadata")).strip().lower()
        if symlink_mode not in _ALLOWED_SYMLINK_MODES:
            raise RelocationError(
                f"on_symlink_error must be one of {sorted(_ALLOWED_SYMLINK_MODES)}"
            )
        pattern = str(
            pattern_override
            if pattern_override is not None
            else section.get("path_template") or ""
        ).strip()
        if not pattern:
            raise RelocationError("zotero_relocation.path_template must not be empty")

        return cls(
            enabled=bool(section.get("enabled", False)),
            root=root,
            storage_root=storage_root,
            path_template=pattern,
            max_component_bytes=max_bytes,
            collision_policy=collision,
            max_collision_attempts=max_attempts,
            delete_source=bool(section.get("delete_source", False))
            or delete_source_override,
            allowed_source_roots=allowed,
            update_metadata=bool(section.get("update_metadata", True)),
            materialize_aliases=bool(section.get("materialize_aliases", True)),
            on_symlink_error=symlink_mode,
            base_dir_relative=bool(section.get("base_dir_relative", False)),
        )


@dataclass(frozen=True)
class MetadataBinding:
    collection_index: int
    item_index: int
    attachment_index: int
    collection_name: str
    collection_key: str
    item_title: str
    item_key: str
    attachment_key: str
    local_path: Path
    source_alias: Path
    filename: str


class MetadataStore:
    """Minimal, versioned access to the private Zotero metadata document."""

    def __init__(self, path: Path, data: dict[str, Any]) -> None:
        self.path = path
        self.data = data
        self._locations: dict[str, tuple[int, int, int]] = {}
        self._index_locations()

    @classmethod
    def load(cls, path: Path) -> MetadataStore:
        try:
            data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
        except (OSError, yaml.YAMLError) as exc:
            raise RelocationError(f"cannot read Zotero metadata: {path}") from exc
        if not isinstance(data, dict) or data.get("version") != 1:
            raise RelocationError("metadata.yaml must declare version: 1")
        if not isinstance(data.get("collections", []), list):
            raise RelocationError("metadata.yaml collections must be a list")
        return cls(path, data)

    def _index_locations(self) -> None:
        for collection_index, collection in enumerate(self.data.get("collections", [])):
            if not isinstance(collection, dict):
                raise RelocationError(
                    "metadata.yaml collection entries must be mappings"
                )
            for item_index, item in enumerate(collection.get("items", [])):
                if not isinstance(item, dict):
                    raise RelocationError("metadata.yaml item entries must be mappings")
                for attachment_index, attachment in enumerate(
                    item.get("attachments", [])
                ):
                    if not isinstance(attachment, dict):
                        raise RelocationError(
                            "metadata.yaml attachment entries must be mappings"
                        )
                    key = (
                        str(attachment.get("zotero_attachment_key") or "")
                        .strip()
                        .upper()
                    )
                    if not key:
                        raise RelocationError(
                            "metadata.yaml attachment is missing zotero_attachment_key"
                        )
                    if key in self._locations:
                        raise RelocationError(
                            f"duplicate attachment key in metadata.yaml: {key}"
                        )
                    self._locations[key] = (
                        collection_index,
                        item_index,
                        attachment_index,
                    )

    def bindings(
        self,
        *,
        item_keys: set[str] | None = None,
        attachment_keys: set[str] | None = None,
    ) -> list[MetadataBinding]:
        selected: list[MetadataBinding] = []
        for collection_index, collection in enumerate(self.data.get("collections", [])):
            collection_name = str(collection.get("name") or "")
            collection_key = str(collection.get("zotero_collection_key") or "")
            for item_index, item in enumerate(collection.get("items", [])):
                item_key = str(item.get("zotero_item_key") or "").strip().upper()
                if item_keys and item_key not in item_keys:
                    continue
                item_title = str(item.get("title") or "")
                for attachment_index, attachment in enumerate(
                    item.get("attachments", [])
                ):
                    attachment_key = (
                        str(attachment.get("zotero_attachment_key") or "")
                        .strip()
                        .upper()
                    )
                    if attachment_keys and attachment_key not in attachment_keys:
                        continue
                    selected.append(
                        MetadataBinding(
                            collection_index,
                            item_index,
                            attachment_index,
                            collection_name,
                            collection_key,
                            item_title,
                            item_key,
                            attachment_key,
                            Path(str(attachment.get("local_path") or "")),
                            Path(str(attachment.get("source_alias") or "")),
                            str(attachment.get("filename") or ""),
                        )
                    )
        return selected

    def update_local_path(self, attachment_key: str, target: Path) -> None:
        key = str(attachment_key).strip().upper()
        location = self._locations.get(key)
        if location is None:
            raise RelocationError(f"attachment key not found in metadata.yaml: {key}")
        collection_index, item_index, attachment_index = location
        attachment = self.data["collections"][collection_index]["items"][item_index][
            "attachments"
        ][attachment_index]
        attachment["local_path"] = str(target)

    def references_path(self, source: Path, *, excluding: str) -> bool:
        candidate = _absolute_candidate(source)
        excluded = str(excluding).strip().upper()
        for binding in self.bindings():
            if binding.attachment_key == excluded:
                continue
            if (
                binding.local_path
                and _absolute_candidate(binding.local_path) == candidate
            ):
                return True
        return False

    def write_atomic(self) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        fd, raw_tmp = tempfile.mkstemp(
            prefix=f".{self.path.name}.", suffix=".tmp", dir=self.path.parent
        )
        tmp = Path(raw_tmp)
        try:
            with os.fdopen(fd, "w", encoding="utf-8") as handle:
                yaml.safe_dump(self.data, handle, allow_unicode=True, sort_keys=False)
                handle.flush()
                os.fsync(handle.fileno())
            if self.path.exists():
                os.chmod(tmp, self.path.stat().st_mode & 0o777)
            os.replace(tmp, self.path)
        except (OSError, yaml.YAMLError) as exc:
            raise RelocationError(
                f"cannot atomically update Zotero metadata: {self.path}"
            ) from exc
        finally:
            if tmp.exists():
                tmp.unlink()


@dataclass(frozen=True)
class RelocationPlan:
    binding: MetadataBinding
    status: str
    reason: str = ""
    source: Path | None = None
    target: Path | None = None
    source_fingerprint: FileFingerprint | None = None
    source_resolution: str = ""
    target_exists: bool = False
    target_same_content: bool = False
    stored_path: str = ""
    item: LocalItem | None = field(default=None, repr=False, compare=False)

    def manifest(self) -> dict[str, Any]:
        return {
            "item_key": self.binding.item_key,
            "attachment_key": self.binding.attachment_key,
            "title": self.binding.item_title,
            "status": self.status,
            "reason": self.reason,
            "source": str(self.source) if self.source else "",
            "target": str(self.target) if self.target else "",
            "zotero_path": self.stored_path,
            "source_resolution": self.source_resolution,
            "target_exists": self.target_exists,
            "target_same_content": self.target_same_content,
        }


@dataclass
class RelocationReport:
    applied: bool
    plans: list[RelocationPlan]
    results: list[dict[str, Any]] = field(default_factory=list)

    @property
    def failed_count(self) -> int:
        return sum(
            1
            for result in self.results
            if result.get("status", "").startswith(
                ("error", "blocked", "missing", "collision")
            )
        )

    def manifest(self) -> dict[str, Any]:
        return {
            "version": 1,
            "mode": "apply" if self.applied else "dry-run",
            "plans": [plan.manifest() for plan in self.plans],
            "results": self.results,
        }


def _positive_int(value: Any, name: str) -> int:
    try:
        number = int(value)
    except (TypeError, ValueError) as exc:
        raise RelocationError(f"{name} must be a positive integer") from exc
    if number <= 0:
        raise RelocationError(f"{name} must be a positive integer")
    return number


def _require_absolute_root(raw: Any, label: str) -> Path:
    path = Path(str(raw or "")).expanduser()
    if not path.is_absolute():
        raise RelocationError(f"{label} must be an absolute path")
    return path.resolve()


def _absolute_candidate(path: Path) -> Path:
    return path if path.is_absolute() else path.absolute()


def _is_within(path: Path, root: Path) -> bool:
    try:
        path.relative_to(root)
    except ValueError:
        return False
    return True


def _validate_metadata_path(path: Path, project_root: Path) -> Path:
    root = project_root.resolve()
    resolved = path if path.is_absolute() else root / path
    resolved = resolved.resolve()
    allowed = (root / "sources" / "zotero").resolve()
    if resolved != allowed / "metadata.yaml" or not resolved.exists():
        raise RelocationError(
            "metadata path must be the existing project sources/zotero/metadata.yaml"
        )
    return resolved


def _validate_alias_path(project_root: Path, alias: Path) -> Path:
    if alias.is_absolute():
        raise RelocationError("source_alias must be relative to the project root")
    normalized = Path(os.path.normpath(alias.as_posix()))
    allowed = Path("sources") / "zotero"
    if normalized == allowed or not _is_within(normalized, allowed):
        raise RelocationError("source_alias must stay under sources/zotero")
    result = project_root.resolve() / normalized
    if any(part == ".." for part in normalized.parts):
        raise RelocationError("source_alias must not contain parent traversal")
    return result


def _check_target_path(root: Path, relative: Path) -> Path:
    if relative.is_absolute() or any(
        part in {"", ".", ".."} for part in relative.parts
    ):
        raise RelocationError(
            "generated attachment target must be a safe relative path"
        )
    target = root / relative
    resolved_root = root.resolve()
    resolved_target = target.resolve(strict=False)
    if not _is_within(resolved_target, resolved_root):
        raise RelocationError("generated attachment target escapes the managed root")
    current = resolved_root
    for part in relative.parts[:-1]:
        current = current / part
        if current.exists() and current.is_symlink():
            raise RelocationError(
                "generated attachment target crosses an existing symlink"
            )
    if target.exists() and target.is_symlink():
        raise RelocationError("refusing to use a symlink as an attachment target")
    return target


def _file_fingerprint(path: Path) -> FileFingerprint:
    try:
        size = path.stat().st_size
        digest = hashlib.sha256()
        with path.open("rb") as handle:
            for chunk in iter(lambda: handle.read(1024 * 1024), b""):
                digest.update(chunk)
    except (OSError, ValueError) as exc:
        raise RelocationError(f"cannot fingerprint attachment source: {path}") from exc
    return FileFingerprint(size=size, sha256=digest.hexdigest())


def _first_author(data: Mapping[str, Any]) -> str:
    creators = data.get("creators") or []
    if not isinstance(creators, list):
        return ""
    for creator in creators:
        if (
            not isinstance(creator, Mapping)
            or creator.get("creatorType", "author") != "author"
        ):
            continue
        if creator.get("name"):
            return str(creator["name"])
        return " ".join(
            str(creator.get(field) or "").strip()
            for field in ("firstName", "lastName")
            if str(creator.get(field) or "").strip()
        )
    return ""


def _year(data: Mapping[str, Any]) -> str:
    raw = str(data.get("date") or "").strip()
    return raw[:4] if raw[:4].isdigit() else ""


def _citekey(data: Mapping[str, Any]) -> str:
    if data.get("citationKey"):
        return str(data["citationKey"])
    extra = str(data.get("extra") or "")
    for line in extra.splitlines():
        if line.lower().startswith("citation key:"):
            return line.split(":", 1)[1].strip()
    return ""


def _resolve_source(
    binding: MetadataBinding, item: LocalItem, settings: RelocationSettings
) -> tuple[Path, str]:
    data = item.data
    link_mode = str(data.get("linkMode") or "").strip()
    raw_path = str(data.get("path") or "").strip()
    if link_mode not in _SUPPORTED_LINK_MODES:
        raise RelocationError(
            f"unsupported Zotero attachment linkMode: {link_mode or 'missing'}"
        )
    if not raw_path:
        if link_mode == "imported_file":
            # The Zotero 10 local API omits `path` for imported files; the
            # on-disk layout is always storage/<ATTACHMENT_KEY>/<filename>.
            filename = str(data.get("filename") or binding.filename or "").strip()
            if filename and Path(filename).name == filename:
                if settings.storage_root is None:
                    raise RelocationError(
                        "imported-file attachment requires zotero_relocation.storage_root for local resolution"
                    )
                return (
                    settings.storage_root / binding.attachment_key / filename,
                    "zotero-storage-filename",
                )
        raise RelocationError("Zotero attachment returned no path")
    if link_mode == "linked_file":
        if raw_path.startswith(ATTACHMENTS_PREFIX):
            relative = raw_path[len(ATTACHMENTS_PREFIX) :].strip()
            rel_path = PurePosixPath(relative)
            if (
                not relative
                or rel_path.is_absolute()
                or any(part in {"", ".", ".."} for part in rel_path.parts)
            ):
                raise RelocationError(
                    "base-directory-relative attachment path is unsafe"
                )
            return settings.root / Path(*rel_path.parts), "zotero-base-relative-path"
        path = Path(raw_path).expanduser()
        if not path.is_absolute():
            raise RelocationError(
                "linked-file attachment path must be absolute or attachments:-relative"
            )
        return path, "zotero-linked-path"
    if raw_path.startswith("storage:"):
        if settings.storage_root is None:
            raise RelocationError(
                "imported-file attachment requires zotero_relocation.storage_root for local resolution"
            )
        filename = raw_path.split(":", 1)[1]
        if not filename or Path(filename).name != filename:
            raise RelocationError("imported-file storage path has an unsafe filename")
        return (
            settings.storage_root / binding.attachment_key / filename,
            "zotero-storage-path",
        )
    path = Path(raw_path).expanduser()
    if not path.is_absolute():
        raise RelocationError(
            "imported-file attachment path must be storage: or absolute"
        )
    return path, "zotero-imported-absolute-path"


def _target_for(
    binding: MetadataBinding,
    item: LocalItem,
    source: Path,
    settings: RelocationSettings,
    context_data: Mapping[str, Any] | None = None,
) -> Path:
    # Naming context is normally the parent bibliographic item: attachment rows
    # often carry only a generic title like "PDF" and no creators/date.
    data = context_data if context_data is not None else item.data
    context = {
        "collection_path": binding.collection_name,
        "author": _first_author(data),
        "year": _year(data),
        "title": str(data.get("title") or binding.item_title),
        "citekey": _citekey(data),
        "item_type": str(data.get("itemType") or "attachment"),
    }
    rendered = render_alias_template(settings.path_template, context)
    components = [
        sanitize_title_stem(component, settings.max_component_bytes)
        for component in rendered.split("/")
        if component
    ]
    if not components:
        components = [
            sanitize_title_stem(context["title"], settings.max_component_bytes)
        ]
    name = components[-1]
    suffix = source.suffix or Path(binding.filename).suffix
    if suffix and not name.lower().endswith(suffix.lower()):
        name = f"{name}{suffix}"
    components[-1] = (
        sanitize_title_stem(
            Path(name).stem,
            settings.max_component_bytes - len(Path(name).suffix.encode("utf-8")),
        )
        + Path(name).suffix
    )
    relative = Path(*components)
    return _check_target_path(settings.root, relative)


def _stored_path(target: Path, settings: RelocationSettings) -> str:
    """Path written back to Zotero: absolute, or portable attachments:-relative to root.

    The relative form resolves against each device's own Linked Attachment Base
    Directory, so it is the only cross-device-safe representation; the root must
    match that base directory on every device.
    """
    if not settings.base_dir_relative:
        return str(target)
    relative = target.relative_to(settings.root)
    return ATTACHMENTS_PREFIX + relative.as_posix()


def _candidate_with_suffix(path: Path, number: int) -> Path:
    suffix = path.suffix
    stem = path.name[: -len(suffix)] if suffix else path.name
    return path.with_name(f"{stem} {number}{suffix}")


def _choose_target(
    candidate: Path,
    source: Path,
    source_fingerprint: FileFingerprint,
    settings: RelocationSettings,
    reserved: set[Path],
) -> tuple[Path, bool, bool]:
    source_absolute = _absolute_candidate(source)
    current = candidate
    for attempt in range(settings.max_collision_attempts + 1):
        current = _check_target_path(settings.root, current.relative_to(settings.root))
        if current in reserved:
            occupied = True
        else:
            occupied = current.exists()
        if not occupied:
            return current, False, False
        if current == source_absolute:
            return current, True, False
        if not current.is_file() or current.is_symlink():
            same_content = False
        else:
            same_content = _file_fingerprint(current) == source_fingerprint
        if same_content:
            return current, True, True
        if attempt == settings.max_collision_attempts:
            break
        current = _candidate_with_suffix(candidate, attempt + 2)
    raise RelocationError("target collision limit exceeded")


async def _template_context_data(
    adapter: AttachmentAdapter,
    binding: MetadataBinding,
    attachment_item: LocalItem,
) -> Mapping[str, Any]:
    """Prefer the parent bibliographic item's metadata for path templating."""
    if not binding.item_key:
        return attachment_item.data
    try:
        parent = await adapter.get_item(binding.item_key)
    except (KeyError, LocalWriteError, OSError, TypeError, ValueError) as exc:
        LOG.warning(
            "parent item %s unavailable for naming %s: %s",
            binding.item_key,
            binding.attachment_key,
            exc,
        )
        return attachment_item.data
    if str(parent.data.get("itemType") or "") == "attachment":
        return attachment_item.data
    return parent.data


async def build_plans(
    store: MetadataStore,
    adapter: AttachmentAdapter,
    settings: RelocationSettings,
    *,
    item_keys: set[str] | None = None,
    attachment_keys: set[str] | None = None,
) -> list[RelocationPlan]:
    bindings = store.bindings(item_keys=item_keys, attachment_keys=attachment_keys)
    plans: list[RelocationPlan] = []
    reserved: set[Path] = set()
    for binding in bindings:
        try:
            if not binding.item_key:
                raise RelocationError("metadata binding is missing parent item key")
            item = await adapter.get_item(binding.attachment_key)
            if str(item.data.get("itemType") or "") != "attachment":
                raise RelocationError(
                    "metadata attachment key does not identify an attachment"
                )
            parent_item = str(item.data.get("parentItem") or "").strip().upper()
            if binding.item_key and parent_item and parent_item != binding.item_key:
                raise RelocationError(
                    "metadata parent item does not match Zotero attachment"
                )
            source, resolution = _resolve_source(binding, item, settings)
            if not source.exists() or not source.is_file():
                raise RelocationError(
                    f"local attachment source is missing or not a file: {source}"
                )
            fingerprint = _file_fingerprint(source)
            context_data = await _template_context_data(adapter, binding, item)
            candidate = _target_for(binding, item, source, settings, context_data)
            target, target_exists, same_content = _choose_target(
                candidate, source, fingerprint, settings, reserved
            )
            reserved.add(target)
            status = "same_target" if target == _absolute_candidate(source) else "ready"
            if target_exists and same_content and status == "ready":
                status = "ready_existing_content"
            plans.append(
                RelocationPlan(
                    binding,
                    status,
                    source=source,
                    target=target,
                    source_fingerprint=fingerprint,
                    source_resolution=resolution,
                    target_exists=target_exists,
                    target_same_content=same_content,
                    stored_path=_stored_path(target, settings),
                    item=item,
                )
            )
        except (RelocationError, LocalWriteError, OSError) as exc:
            plans.append(
                RelocationPlan(binding, _error_status(str(exc)), reason=str(exc))
            )
    return plans


def _error_status(reason: str) -> str:
    lowered = reason.lower()
    if "storage_root" in lowered:
        return "missing-storage-root"
    if "missing" in lowered or "not a file" in lowered:
        return "missing-local-path"
    if "collision" in lowered:
        return "collision"
    if "unsupported" in lowered or "absolute" in lowered:
        return "blocked-by-policy"
    return "error-plan"


def _copy_verified(source: Path, target: Path, expected: FileFingerprint) -> bool:
    if target.exists():
        if target.is_symlink():
            raise RelocationError("refusing to overwrite a symlink target")
        if target.is_file() and _file_fingerprint(target) == expected:
            return False
        raise RelocationError(f"target appeared or changed during apply: {target}")
    target.parent.mkdir(parents=True, exist_ok=True)
    fd, raw_tmp = tempfile.mkstemp(
        prefix=f".{target.name}.", suffix=".tmp", dir=target.parent
    )
    tmp = Path(raw_tmp)
    try:
        with source.open("rb") as input_handle, os.fdopen(fd, "wb") as output_handle:
            shutil.copyfileobj(input_handle, output_handle, length=1024 * 1024)
            output_handle.flush()
            os.fsync(output_handle.fileno())
        if _file_fingerprint(tmp) != expected:
            raise RelocationError("copied attachment failed fingerprint verification")
        os.replace(tmp, target)
        return True
    except (OSError, ValueError) as exc:
        raise RelocationError(f"cannot copy attachment to target: {target}") from exc
    finally:
        if tmp.exists():
            tmp.unlink()


def _materialize_alias(
    project_root: Path,
    alias: Path,
    target: Path,
    *,
    force: bool,
    on_error: str,
) -> str:
    alias_path = _validate_alias_path(project_root, alias)
    project = project_root.resolve()
    for parent in [alias_path.parent, *alias_path.parent.parents]:
        if parent == project:
            break
        if parent.exists() and parent.is_symlink():
            raise RelocationError("source alias parent crosses an existing symlink")
    if alias_path.exists() or alias_path.is_symlink():
        if alias_path.is_symlink() and alias_path.resolve() == target.resolve():
            return "skipped"
        if alias_path.is_symlink() and force:
            alias_path.unlink()
        elif (
            alias_path.is_file()
            and not alias_path.is_symlink()
            and _file_fingerprint(alias_path) == _file_fingerprint(target)
        ):
            return "existing-copy"
        else:
            raise RelocationError(
                f"refusing to replace existing non-managed alias: {alias_path}"
            )
    alias_path.parent.mkdir(parents=True, exist_ok=True)
    try:
        alias_path.symlink_to(target)
        return "symlink"
    except OSError:
        if on_error == "metadata":
            return "metadata-only"
        try:
            if on_error == "copy":
                shutil.copy2(target, alias_path)
            else:
                os.link(target, alias_path)
        except OSError as fallback_exc:
            raise RelocationError(
                "alias symlink and configured fallback both failed"
            ) from fallback_exc
        return on_error


def _cleanup_source(
    store: MetadataStore,
    plan: RelocationPlan,
    settings: RelocationSettings,
) -> str:
    if not settings.delete_source:
        return "disabled"
    assert plan.source is not None
    if plan.target is not None and _absolute_candidate(
        plan.source
    ) == _absolute_candidate(plan.target):
        return "same-target"
    source = plan.source
    if source.is_symlink() or not source.is_file():
        raise RelocationError("refusing to delete a non-regular attachment source")
    source_resolved = source.resolve()
    if not any(
        _is_within(source_resolved, root) for root in settings.allowed_source_roots
    ):
        raise RelocationError("source is outside allowed_source_roots")
    if store.references_path(source, excluding=plan.binding.attachment_key):
        raise RelocationError("source is referenced by another metadata attachment")
    expected = plan.source_fingerprint
    if expected is None or _file_fingerprint(source) != expected:
        raise RelocationError("source changed after relocation; refusing cleanup")
    source.unlink()
    return "removed"


def _result_base(plan: RelocationPlan) -> dict[str, Any]:
    return {
        "item_key": plan.binding.item_key,
        "attachment_key": plan.binding.attachment_key,
        "title": plan.binding.item_title,
        "status": plan.status,
        "reason": plan.reason,
        "source": str(plan.source) if plan.source else "",
        "target": str(plan.target) if plan.target else "",
        "zotero_path": plan.stored_path,
    }


async def relocate(
    metadata_path: Path,
    project_root: Path,
    settings: RelocationSettings,
    adapter: AttachmentAdapter,
    *,
    apply: bool,
    item_keys: set[str] | None = None,
    attachment_keys: set[str] | None = None,
) -> RelocationReport:
    metadata = MetadataStore.load(metadata_path)
    plans = await build_plans(
        metadata,
        adapter,
        settings,
        item_keys=item_keys,
        attachment_keys=attachment_keys,
    )
    report = RelocationReport(applied=apply, plans=plans)
    if not apply:
        report.results = [_result_base(plan) for plan in plans]
        return report
    if not settings.enabled:
        raise RelocationError("zotero_relocation.enabled must be true before apply")

    for plan in plans:
        result = _result_base(plan)
        if plan.status not in {"ready", "ready_existing_content", "same_target"}:
            result["status"] = plan.status
            report.results.append(result)
            continue
        assert (
            plan.source is not None
            and plan.target is not None
            and plan.source_fingerprint is not None
        )
        created_target = False
        zotero_repointed = False
        try:
            if plan.status == "same_target":
                result["copy"] = "skipped"
            else:
                created_target = _copy_verified(
                    plan.source, plan.target, plan.source_fingerprint
                )
                result["copy"] = "created" if created_target else "existing-content"

            expected_parent = (
                str(plan.item.data.get("parentItem") or "") if plan.item else None
            )
            repoint = await adapter.repoint_attachment(
                plan.binding.attachment_key,
                plan.stored_path,
                expected_parent_item=expected_parent or None,
            )
            zotero_repointed = repoint.status != "skipped_current"
            result["zotero"] = repoint.status

            if settings.update_metadata:
                metadata.update_local_path(plan.binding.attachment_key, plan.target)
                metadata.write_atomic()
                result["metadata"] = "updated"
            else:
                result["metadata"] = "disabled"

            if settings.materialize_aliases:
                result["alias"] = _materialize_alias(
                    project_root,
                    plan.binding.source_alias,
                    plan.target,
                    force=True,
                    on_error=settings.on_symlink_error,
                )
            else:
                result["alias"] = "disabled"
            try:
                result["cleanup"] = _cleanup_source(metadata, plan, settings)
            except (RelocationError, OSError) as exc:
                result["cleanup"] = "pending"
                result["cleanup_reason"] = str(exc)
            result["status"] = "complete"
        except (RelocationError, LocalWriteError, OSError, ValueError) as exc:
            result["status"] = "error-after-zotero" if zotero_repointed else "error"
            result["reason"] = str(exc)
            if (
                created_target
                and not zotero_repointed
                and plan.target.exists()
                and not plan.target.is_symlink()
            ):
                try:
                    plan.target.unlink()
                    result["rollback"] = "target-removed"
                except OSError:
                    result["rollback"] = "target-cleanup-needed"
            report.results.append(result)
            continue
        report.results.append(result)
    return report


def report_to_manifest(report: RelocationReport) -> dict[str, Any]:
    return report.manifest()
