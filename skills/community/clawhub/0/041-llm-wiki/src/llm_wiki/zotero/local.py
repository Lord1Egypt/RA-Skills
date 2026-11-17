"""Restricted Zotero 10 local-API writer with verified mutations.

Reads remain MCP-backed for normal collection workflows. This module is the
explicitly authorized temporary write path documented in the Zotero integration
protocol. It only talks to loopback, discovers the live Zotero server ID, guards
writes by item version, retries 412 conflicts with bounded exponential backoff,
and verifies every accepted PATCH with a fresh GET. Reciprocal Related-item
writes are compensated: if the second direction fails, the first direction's
addition is rolled back so no asymmetric residue is left behind.
"""

from __future__ import annotations

import asyncio
import json
import os
import re
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from pathlib import Path, PurePosixPath
from typing import Any
from urllib.parse import urlparse

import httpx

from ..agent_logger import get_logger

LOG = get_logger("zotero_local")

DEFAULT_BASE_URL = "http://127.0.0.1:23119"
DEFAULT_USER_PREFIX = "users/0"
_LOOPBACK_HOSTS = {"127.0.0.1", "localhost", "::1"}
_ITEM_KEY_RE = re.compile(r"^[A-Z0-9]{8}$")
_MAX_WRITE_TIMEOUT = 60.0
_MAX_AUTH_TIMEOUT = 300.0
_RELATION_PREDICATE = "dc:relation"
_DEFAULT_RETRY_DELAYS = (0.5, 1.0, 2.0)
# Zotero's portable linked-file form: a POSIX-relative path resolved against the
# per-device Linked Attachment Base Directory.  This is the only cross-device-safe
# representation; absolute paths break on any machine with a different root.
ATTACHMENTS_PREFIX = "attachments:"


def _validate_attachment_target(target: str) -> str:
    """Validate a linked-file target: absolute local path or portable attachments: form."""
    value = str(target or "").strip()
    if not value:
        raise LocalWriteError("attachment target path must not be empty")
    if value.startswith(ATTACHMENTS_PREFIX):
        relative = value[len(ATTACHMENTS_PREFIX) :]
        parts = PurePosixPath(relative).parts
        if (
            not relative
            or "\\" in relative
            or PurePosixPath(relative).is_absolute()
            or any(part in {"", ".", ".."} for part in parts)
        ):
            raise LocalWriteError(
                "attachments: target must be a safe POSIX-relative path"
            )
        return value
    if not os.path.isabs(value):
        raise LocalWriteError(
            "attachment target path must be absolute or attachments:-relative"
        )
    return value


class LocalWriteError(RuntimeError):
    """Raised when a local Zotero write cannot be completed or verified."""


@dataclass(frozen=True)
class LocalItem:
    """One local API item response with the real Zotero library identity."""

    key: str
    version: int
    data: dict[str, Any]
    library_type: str = ""
    library_id: str = ""

    @property
    def uri(self) -> str:
        if not self.library_id or self.library_type not in {"user", "group"}:
            raise LocalWriteError(
                f"item {self.key} returned no usable library identity; cannot build a relation URI"
            )
        segment = "users" if self.library_type == "user" else "groups"
        return f"http://zotero.org/{segment}/{self.library_id}/items/{self.key}"


@dataclass(frozen=True)
class LocalMutationResult:
    """Verified result of one safe item mutation."""

    item_key: str
    status: str
    attempts: int
    changed_fields: tuple[str, ...] = ()


@dataclass(frozen=True)
class RelationAudit:
    """Observed state of a reviewed reciprocal Related-item pair."""

    source_key: str
    target_key: str
    source_has_target: bool
    target_has_source: bool

    @property
    def reciprocal(self) -> bool:
        return self.source_has_target and self.target_has_source


@dataclass(frozen=True)
class RelationWriteResult:
    """Verified result of ensuring one reciprocal Related-item pair."""

    source_key: str
    target_key: str
    changed_items: tuple[str, ...]


@dataclass(frozen=True)
class AttachmentRepointResult:
    """Verified result of changing an attachment to a linked-file path."""

    item_key: str
    status: str
    attempts: int
    before_link_mode: str
    before_path: str
    target_path: str


@dataclass(frozen=True)
class _MutationExpectation:
    baseline_tags: tuple[dict[str, Any], ...]
    add_tags: frozenset[str]
    remove_tags: frozenset[str]
    extra_keys: Mapping[str, str]
    fields: Mapping[str, Any]


def _validate_loopback(base_url: str) -> None:
    """The local key is unscoped, so it must never leave loopback HTTP."""
    parsed = urlparse(base_url)
    host = (parsed.hostname or "").strip().lower()
    if parsed.scheme != "http" or host not in _LOOPBACK_HOSTS:
        raise LocalWriteError(
            f"local write base_url must use loopback HTTP, got {base_url!r}"
        )


def _validate_timeout(timeout: float, maximum: float) -> float:
    value = float(timeout)
    if value <= 0 or value > maximum:
        raise LocalWriteError(f"timeout must be > 0 and <= {maximum:g} seconds")
    return value


def _validate_item_key(item_key: str) -> str:
    key = str(item_key or "").strip().upper()
    if not _ITEM_KEY_RE.fullmatch(key):
        raise LocalWriteError("Zotero item key must be exactly 8 ASCII letters/digits")
    return key


def _tag_name(raw: Any) -> str:
    return str(raw.get("tag") if isinstance(raw, Mapping) else raw).strip()


def _tag_objects(raw_tags: Any) -> list[dict[str, Any]]:
    """Normalize tags while retaining every metadata field on existing objects."""
    tags: list[dict[str, Any]] = []
    for raw in raw_tags or []:
        name = _tag_name(raw)
        if not name:
            continue
        if isinstance(raw, Mapping):
            obj = dict(raw)
            obj["tag"] = name
        else:
            obj = {"tag": name}
        tags.append(obj)
    return tags


def _tag_names(raw_tags: Any) -> list[str]:
    return [_tag_name(raw) for raw in raw_tags or [] if _tag_name(raw)]


def _merge_tag_objects(
    raw_tags: Any,
    add_tags: Sequence[str],
    remove_tags: Sequence[str],
) -> list[dict[str, Any]]:
    remove = {str(tag).strip() for tag in remove_tags if str(tag).strip()}
    merged = [tag for tag in _tag_objects(raw_tags) if tag["tag"] not in remove]
    names = {tag["tag"] for tag in merged}
    for name in sorted({str(tag).strip() for tag in add_tags if str(tag).strip()}):
        if name not in names:
            merged.append({"tag": name})
            names.add(name)
    return merged


def _upsert_extra_lines(extra: str, set_keys: Mapping[str, str]) -> str:
    """Upsert managed Key: Value lines while preserving unrelated lines."""
    remaining = dict(set_keys)
    out: list[str] = []
    for line in str(extra or "").splitlines():
        if ":" in line:
            key = line.split(":", 1)[0].strip()
            if key in set_keys:
                if key in remaining:
                    out.append(f"{key}: {remaining.pop(key)}")
                continue
        out.append(line)
    for key, value in remaining.items():
        out.append(f"{key}: {value}")
    return "\n".join(out)


def _extra_keys(extra: str) -> dict[str, str]:
    parsed: dict[str, str] = {}
    for line in str(extra or "").splitlines():
        if ":" in line:
            key, value = line.split(":", 1)
            parsed[key.strip()] = value.strip()
    return parsed


def _relation_values(relations: Any, predicate: str = _RELATION_PREDICATE) -> list[str]:
    if not isinstance(relations, Mapping):
        return []
    raw = relations.get(predicate) or []
    if isinstance(raw, str):
        raw = [raw]
    return [str(value).strip() for value in raw if str(value).strip()]


def _relations_with_uri(relations: Any, uri: str) -> dict[str, Any]:
    out = dict(relations) if isinstance(relations, Mapping) else {}
    values = _relation_values(out)
    if uri not in values:
        values.append(uri)
    out[_RELATION_PREDICATE] = values
    return out


class LocalZoteroWriter:
    """Async loopback writer for incremental, verified Zotero mutations."""

    def __init__(
        self,
        api_key: str = "",
        *,
        base_url: str = DEFAULT_BASE_URL,
        user_prefix: str = DEFAULT_USER_PREFIX,
        timeout: float = 20.0,
        http: httpx.AsyncClient | None = None,
        retry_delays: Sequence[float] | None = None,
    ) -> None:
        _validate_loopback(base_url)
        self._api_key = str(api_key or "")
        self._base_url = base_url.rstrip("/")
        self._prefix = user_prefix.strip("/")
        self._timeout = _validate_timeout(timeout, _MAX_WRITE_TIMEOUT)
        self._http = http
        self._owns_http = http is None
        self._server_id_cache: str | None = None
        delays = tuple(
            float(d)
            for d in (
                retry_delays if retry_delays is not None else _DEFAULT_RETRY_DELAYS
            )
        )
        if any(d < 0 for d in delays):
            raise LocalWriteError("retry_delays must be non-negative seconds")
        self._retry_delays = delays

    @property
    def _max_attempts(self) -> int:
        return 1 + len(self._retry_delays)

    async def _backoff_before_retry(self, attempt: int) -> None:
        """Sleep the configured delay before retry number `attempt` (1-based)."""
        delay = self._retry_delays[attempt - 1]
        if delay:
            LOG.info("backing off %.2fs before retry %d", delay, attempt)
            await asyncio.sleep(delay)

    async def _client(self) -> httpx.AsyncClient:
        if self._http is None:
            self._http = httpx.AsyncClient(timeout=httpx.Timeout(self._timeout))
        return self._http

    async def aclose(self) -> None:
        if self._owns_http and self._http is not None:
            await self._http.aclose()
            self._http = None

    async def _server_id(self, *, refresh: bool = False) -> str:
        if refresh:
            self._server_id_cache = None
        if self._server_id_cache is None:
            client = await self._client()
            try:
                resp = await client.get(f"{self._base_url}/api/")
            except httpx.HTTPError as exc:
                raise LocalWriteError("cannot reach the Zotero loopback API") from exc
            if resp.status_code != 200:
                raise LocalWriteError(f"local API discovery -> HTTP {resp.status_code}")
            server_id = resp.headers.get("Zotero-Server-ID")
            if not server_id:
                raise LocalWriteError(
                    "local API did not return a Zotero-Server-ID header"
                )
            self._server_id_cache = server_id
        return self._server_id_cache

    async def get_item(self, item_key: str) -> LocalItem:
        key = _validate_item_key(item_key)
        client = await self._client()
        try:
            resp = await client.get(f"{self._base_url}/api/{self._prefix}/items/{key}")
        except httpx.HTTPError as exc:
            raise LocalWriteError(f"GET item {key} failed") from exc
        if resp.status_code != 200:
            raise LocalWriteError(f"GET item {key} -> HTTP {resp.status_code}")
        try:
            payload = resp.json() or {}
        except ValueError as exc:
            raise LocalWriteError(f"GET item {key} returned invalid JSON") from exc
        data = dict(payload.get("data") or {})
        version = payload.get("version", data.get("version"))
        if not isinstance(version, int):
            raise LocalWriteError(f"item {key} returned no integer version")
        library = payload.get("library") or {}
        return LocalItem(
            key=key,
            version=version,
            data=data,
            library_type=str(library.get("type") or "").strip(),
            library_id=str(library.get("id") or "").strip(),
        )

    async def _get_item(self, item_key: str) -> tuple[int, dict[str, Any]]:
        item = await self.get_item(item_key)
        return item.version, item.data

    async def _patch_item_once(
        self,
        item_key: str,
        patch: Mapping[str, Any],
        version: int,
    ) -> bool:
        if not self._api_key:
            raise LocalWriteError("local write authorization is required before PATCH")
        client = await self._client()
        server_id = await self._server_id(refresh=True)
        try:
            resp = await client.patch(
                f"{self._base_url}/api/{self._prefix}/items/{item_key}",
                json=dict(patch),
                headers={
                    "Zotero-Server-ID": server_id,
                    "Zotero-API-Key": self._api_key,
                    "If-Unmodified-Since-Version": str(version),
                    "Content-Type": "application/json",
                },
            )
        except httpx.HTTPError as exc:
            raise LocalWriteError(f"PATCH item {item_key} failed") from exc
        if resp.status_code == 412:
            return False
        if resp.status_code >= 400:
            detail = resp.text.strip().replace("\n", " ")[:300]
            if self._api_key:
                detail = detail.replace(self._api_key, "<redacted>")
            raise LocalWriteError(
                f"PATCH item {item_key} -> HTTP {resp.status_code}: {detail or 'no body'}"
            )
        return True

    @staticmethod
    def _build_mutation(
        data: Mapping[str, Any],
        *,
        set_keys: Mapping[str, str],
        add_tags: Sequence[str],
        remove_tags: Sequence[str],
        fields: Mapping[str, Any],
    ) -> tuple[dict[str, Any], _MutationExpectation]:
        patch: dict[str, Any] = {}
        baseline_tags = tuple(_tag_objects(data.get("tags")))
        current_names = set(_tag_names(data.get("tags")))
        add = frozenset(add_tags)
        remove = frozenset(remove_tags)
        if (add - current_names) or (remove & current_names):
            patch["tags"] = _merge_tag_objects(data.get("tags"), add, remove)

        current_extra = str(data.get("extra") or "")
        updated_extra = _upsert_extra_lines(current_extra, set_keys)
        if set_keys and updated_extra != current_extra:
            patch["extra"] = updated_extra

        changed_fields: dict[str, Any] = {}
        for key, value in fields.items():
            if data.get(key) != value:
                patch[key] = value
                changed_fields[key] = value

        expectation = _MutationExpectation(
            baseline_tags=baseline_tags,
            add_tags=add,
            remove_tags=remove,
            extra_keys=dict(set_keys),
            fields=changed_fields,
        )
        return patch, expectation

    @staticmethod
    def _verify_mutation(item: LocalItem, expectation: _MutationExpectation) -> None:
        current_objects = _tag_objects(item.data.get("tags"))
        current_names = {tag["tag"] for tag in current_objects}
        if (
            expectation.add_tags - current_names
            or expectation.remove_tags & current_names
        ):
            raise LocalWriteError(
                f"verification failed for item {item.key}: tag delta did not persist"
            )
        for old in expectation.baseline_tags:
            if old["tag"] not in expectation.remove_tags and old not in current_objects:
                raise LocalWriteError(
                    f"verification failed for item {item.key}: existing tag metadata changed"
                )

        parsed_extra = _extra_keys(str(item.data.get("extra") or ""))
        for key, value in expectation.extra_keys.items():
            if parsed_extra.get(key) != value:
                raise LocalWriteError(
                    f"verification failed for item {item.key}: Extra key {key!r} did not persist"
                )
        for key, value in expectation.fields.items():
            if item.data.get(key) != value:
                raise LocalWriteError(
                    f"verification failed for item {item.key}: field {key!r} did not persist"
                )

    async def write_safe_mutation(
        self,
        item_key: str,
        *,
        set_keys: Mapping[str, Any] | None = None,
        add_tags=(),
        remove_tags=(),
        fields: Mapping[str, Any] | None = None,
    ) -> LocalMutationResult:
        """GET, delta, versioned PATCH, GET, and exact verification.

        412 conflicts are retried from a fresh GET with bounded exponential
        backoff so concurrent unrelated tag and Extra updates are retained.
        """
        key = _validate_item_key(item_key)
        normalized_keys = {
            str(name): str(value)
            for name, value in (set_keys or {}).items()
            if value is not None
        }
        add = tuple(sorted({str(tag).strip() for tag in add_tags if str(tag).strip()}))
        remove = tuple(
            sorted({str(tag).strip() for tag in remove_tags if str(tag).strip()})
        )
        field_updates = {str(name): value for name, value in (fields or {}).items()}
        if not (normalized_keys or add or remove or field_updates):
            return LocalMutationResult(key, "skipped_current", 0)

        for attempt in range(1, self._max_attempts + 1):
            before = await self.get_item(key)
            patch, expectation = self._build_mutation(
                before.data,
                set_keys=normalized_keys,
                add_tags=add,
                remove_tags=remove,
                fields=field_updates,
            )
            if not patch:
                return LocalMutationResult(key, "skipped_current", attempt - 1)

            LOG.info(
                "local write %s: tags +%d -%d, set_keys=%d, fields=%s",
                key,
                len(add),
                len(remove),
                len(normalized_keys),
                sorted(field_updates),
            )
            accepted = await self._patch_item_once(key, patch, before.version)
            if not accepted:
                if attempt <= len(self._retry_delays):
                    LOG.warning(
                        "local write %s hit a version conflict (attempt %d); backing off",
                        key,
                        attempt,
                    )
                    await self._backoff_before_retry(attempt)
                    continue
                raise LocalWriteError(
                    f"PATCH item {key} conflicted {attempt} times; no further retry attempted"
                )

            after = await self.get_item(key)
            self._verify_mutation(after, expectation)
            return LocalMutationResult(
                key,
                "updated_verified",
                attempt,
                tuple(sorted(patch)),
            )

        raise LocalWriteError(f"PATCH item {key} did not complete")

    async def audit_relation_pair(
        self, source_key: str, target_key: str
    ) -> RelationAudit:
        source = await self.get_item(source_key)
        target = await self.get_item(target_key)
        if source.key == target.key:
            raise LocalWriteError("a Zotero item cannot be related to itself")
        if (
            source.library_type != target.library_type
            or source.library_id != target.library_id
            or not source.library_id
        ):
            raise LocalWriteError(
                "reviewed Related items must belong to the same real Zotero library"
            )
        return RelationAudit(
            source_key=source.key,
            target_key=target.key,
            source_has_target=target.uri
            in _relation_values(source.data.get("relations")),
            target_has_source=source.uri
            in _relation_values(target.data.get("relations")),
        )

    async def _ensure_relation_direction(self, item_key: str, related_uri: str) -> bool:
        for attempt in range(1, self._max_attempts + 1):
            item = await self.get_item(item_key)
            if related_uri in _relation_values(item.data.get("relations")):
                return False
            patch = {
                "relations": _relations_with_uri(
                    item.data.get("relations"), related_uri
                )
            }
            accepted = await self._patch_item_once(item.key, patch, item.version)
            if not accepted:
                if attempt <= len(self._retry_delays):
                    await self._backoff_before_retry(attempt)
                    continue
                raise LocalWriteError(
                    f"PATCH item {item.key} relation conflicted {attempt} times; "
                    "no further retry attempted"
                )
            verified = await self.get_item(item.key)
            if related_uri not in _relation_values(verified.data.get("relations")):
                raise LocalWriteError(
                    f"verification failed for item {item.key}: Related-item direction did not persist"
                )
            return True
        return False

    async def _remove_relation_direction(self, item_key: str, related_uri: str) -> None:
        """补偿回滚:移除同一次 ensure_relation_pair 调用刚写入的单向关联。

        仅用于事务补偿,不移除预先存在的关联——若 URI 在首次 GET 时就不在,
        直接返回。
        """
        for attempt in range(1, self._max_attempts + 1):
            item = await self.get_item(item_key)
            values = _relation_values(item.data.get("relations"))
            if related_uri not in values:
                return
            relations = dict(item.data.get("relations") or {})
            remaining = [value for value in values if value != related_uri]
            if remaining:
                relations[_RELATION_PREDICATE] = remaining
            else:
                relations.pop(_RELATION_PREDICATE, None)
            accepted = await self._patch_item_once(
                item.key, {"relations": relations}, item.version
            )
            if not accepted:
                if attempt <= len(self._retry_delays):
                    await self._backoff_before_retry(attempt)
                    continue
                raise LocalWriteError(
                    f"compensation failed for item {item.key}: relation removal conflicted "
                    f"{attempt} times"
                )
            verified = await self.get_item(item.key)
            if related_uri in _relation_values(verified.data.get("relations")):
                raise LocalWriteError(
                    f"compensation verification failed for item {item.key}: "
                    "Related-item removal did not persist"
                )
            return

    async def ensure_relation_pair(
        self,
        source_key: str,
        target_key: str,
    ) -> RelationWriteResult:
        """Ensure a user-reviewed reciprocal Related-item pair.

        The only removal this method may perform is compensating rollback: if
        the second direction fails after the first was written, the just-added
        relation on the source is removed so no asymmetric residue remains.
        """
        source = await self.get_item(source_key)
        target = await self.get_item(target_key)
        if source.key == target.key:
            raise LocalWriteError("a Zotero item cannot be related to itself")
        if (
            source.library_type != target.library_type
            or source.library_id != target.library_id
            or not source.library_id
        ):
            raise LocalWriteError(
                "reviewed Related items must belong to the same real Zotero library"
            )

        changed: list[str] = []
        source_changed = False
        if target.uri not in _relation_values(
            source.data.get("relations")
        ) and await self._ensure_relation_direction(source.key, target.uri):
            changed.append(source.key)
            source_changed = True
        try:
            if source.uri not in _relation_values(
                target.data.get("relations")
            ) and await self._ensure_relation_direction(target.key, source.uri):
                changed.append(target.key)
        except Exception as exc:
            if source_changed:
                LOG.warning(
                    "second relation direction failed for %s/%s; compensating %s",
                    source.key,
                    target.key,
                    source.key,
                )
                try:
                    await self._remove_relation_direction(source.key, target.uri)
                except LocalWriteError as compensation_exc:
                    raise LocalWriteError(
                        f"Related-item pair {source.key}/{target.key} failed ({exc}); "
                        f"compensation also failed ({compensation_exc}); "
                        "asymmetric relation residue requires manual cleanup"
                    ) from exc
            raise

        audit = await self.audit_relation_pair(source.key, target.key)
        if not audit.reciprocal:
            raise LocalWriteError(
                f"verification failed for Related-item pair {source.key}/{target.key}"
            )
        return RelationWriteResult(source.key, target.key, tuple(changed))

    async def repoint_attachment(
        self,
        item_key: str,
        target_path: str,
        *,
        expected_parent_item: str | None = None,
    ) -> AttachmentRepointResult:
        """Convert one attachment to a linked-file path and verify invariants.

        This deliberately exposes a narrower mutation than ``write_safe_mutation``:
        only attachment ``linkMode`` and ``path`` may change.  The method keeps the
        original item key and verifies the attachment identity and parent after the
        versioned PATCH.  It never creates, deletes, or re-keys Zotero items.
        """
        key = _validate_item_key(item_key)
        target = _validate_attachment_target(target_path)

        before = await self.get_item(key)
        if str(before.data.get("itemType") or "") != "attachment":
            raise LocalWriteError(f"item {key} is not a Zotero attachment")
        data_key = str(before.data.get("key") or key).strip().upper()
        if data_key != key:
            raise LocalWriteError(f"attachment {key} returned a different item key")
        parent_before = str(before.data.get("parentItem") or "").strip().upper()
        expected_parent = (
            str(expected_parent_item).strip().upper()
            if expected_parent_item is not None
            else None
        )
        if expected_parent is not None and parent_before != expected_parent:
            raise LocalWriteError(f"attachment {key} parent item changed before write")

        before_link_mode = str(before.data.get("linkMode") or "")
        before_path = str(before.data.get("path") or "")
        if before_link_mode == "linked_file" and before_path == target:
            return AttachmentRepointResult(
                key, "skipped_current", 0, before_link_mode, before_path, target
            )

        mutation = await self.write_safe_mutation(
            key,
            fields={"linkMode": "linked_file", "path": target},
        )
        after = await self.get_item(key)
        if str(after.data.get("itemType") or "") != "attachment":
            raise LocalWriteError(
                f"verification failed for attachment {key}: item type changed"
            )
        if str(after.data.get("key") or key).strip().upper() != key:
            raise LocalWriteError(
                f"verification failed for attachment {key}: item key changed"
            )
        if (
            expected_parent is not None
            and str(after.data.get("parentItem") or "").strip().upper()
            != expected_parent
        ):
            raise LocalWriteError(
                f"verification failed for attachment {key}: parent item changed"
            )
        if (
            str(after.data.get("linkMode") or "") != "linked_file"
            or str(after.data.get("path") or "") != target
        ):
            raise LocalWriteError(
                f"verification failed for attachment {key}: linked path did not persist"
            )

        for field in (
            "parentItem",
            "filename",
            "contentType",
            "charset",
            "relations",
            "tags",
            "extra",
        ):
            if field in before.data and after.data.get(field) != before.data.get(field):
                raise LocalWriteError(
                    f"verification failed for attachment {key}: protected field {field!r} changed"
                )
        return AttachmentRepointResult(
            key,
            mutation.status,
            mutation.attempts,
            before_link_mode,
            before_path,
            target,
        )

    @classmethod
    def from_store(cls, store_path, **kwargs) -> LocalZoteroWriter:
        return cls(load_local_key(store_path), **kwargs)


async def authorize_local(
    app_name: str,
    store_path=None,
    *,
    base_url: str = DEFAULT_BASE_URL,
    timeout: float = 180.0,
    http: httpx.AsyncClient | None = None,
) -> str:
    """Request a Zotero local key, optionally persisting it under private var.

    Passing store_path=None keeps the key only in the current process. The key
    is returned to the caller but is never logged or included in errors.
    """
    base = base_url.rstrip("/")
    _validate_loopback(base)
    bounded_timeout = _validate_timeout(timeout, _MAX_AUTH_TIMEOUT)
    app = str(app_name or "").strip()
    if not app or len(app) > 100:
        raise LocalWriteError("authorization app name must contain 1-100 characters")
    client = (
        http
        if http is not None
        else httpx.AsyncClient(timeout=httpx.Timeout(bounded_timeout))
    )
    try:
        try:
            resp = await client.get(f"{base}/api/")
        except httpx.HTTPError as exc:
            raise LocalWriteError("cannot reach the Zotero loopback API") from exc
        if resp.status_code != 200:
            raise LocalWriteError(f"local API discovery -> HTTP {resp.status_code}")
        server_id = resp.headers.get("Zotero-Server-ID")
        if not server_id:
            raise LocalWriteError("local API did not return a Zotero-Server-ID header")

        try:
            resp = await client.post(
                f"{base}/api/local/authorize",
                json={"appName": app},
                headers={
                    "Zotero-Server-ID": server_id,
                    "Content-Type": "application/json",
                },
            )
        except httpx.HTTPError as exc:
            raise LocalWriteError("local authorization request failed") from exc
        if resp.status_code >= 400:
            raise LocalWriteError(f"authorize -> HTTP {resp.status_code}")
        try:
            key = str((resp.json() or {}).get("key") or "")
        except ValueError as exc:
            raise LocalWriteError("authorization returned invalid JSON") from exc
        if not key:
            raise LocalWriteError(
                "authorization returned no key (the dialog may have been denied)"
            )

        if store_path is not None:
            private_path = Path(store_path)
            private_path.parent.mkdir(parents=True, exist_ok=True)
            fd = os.open(private_path, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
            try:
                payload = json.dumps({"app_name": app, "key": key}, indent=2) + "\n"
                os.write(fd, payload.encode("utf-8"))
            finally:
                os.close(fd)
            os.chmod(private_path, 0o600)
            LOG.info("stored local write authorization in private var state")
        else:
            LOG.info("obtained process-memory-only local write authorization")
        return key
    finally:
        if http is None:
            await client.aclose()


def load_local_key(store_path) -> str:
    """Read a reusable local key from the gitignored private store."""
    private_path = Path(store_path)
    try:
        data = json.loads(private_path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise LocalWriteError(
            "no stored local write key; run agent-bridge.py zotero-local-auth first "
            "or use process-memory authorization"
        ) from exc
    except (OSError, ValueError, TypeError) as exc:
        raise LocalWriteError("stored local write authorization is unreadable") from exc
    key = str(data.get("key") or "")
    if not key:
        raise LocalWriteError(
            "stored local write authorization contains no key; authorize again"
        )
    return key
