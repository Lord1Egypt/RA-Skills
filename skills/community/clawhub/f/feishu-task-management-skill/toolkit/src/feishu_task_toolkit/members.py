from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .config import ToolkitPaths, load_json, write_json
from .http import FeishuHttpClient


def _candidate_key(member: dict[str, Any]) -> str:
    return member.get("open_id") or member.get("user_id") or member.get("email") or ""


def _dedupe(values: list[str]) -> list[str]:
    seen: set[str] = set()
    output: list[str] = []
    for value in values:
        if not value or value in seen:
            continue
        seen.add(value)
        output.append(value)
    return output


def normalize_member(record: dict[str, Any]) -> dict[str, Any]:
    department_ids = record.get("department_ids") or []
    departments = record.get("departments") or []
    return {
        "open_id": record.get("open_id", ""),
        "user_id": record.get("user_id", ""),
        "name": record.get("name", ""),
        "en_name": record.get("en_name", ""),
        "nickname": record.get("nickname", ""),
        "email": record.get("email", ""),
        "mobile": record.get("mobile", ""),
        "department_ids": _dedupe(list(department_ids)),
        "departments": _dedupe(list(departments)),
        "status": record.get("status", "active"),
    }


def build_member_table(
    scope_users: list[dict[str, Any]],
    department_users: dict[str, list[dict[str, Any]]],
    generated_at: str | None = None,
) -> dict[str, Any]:
    merged: dict[str, dict[str, Any]] = {}
    all_records = list(scope_users)
    for records in department_users.values():
        all_records.extend(records)

    for raw in all_records:
        member = normalize_member(raw)
        key = _candidate_key(member)
        if not key:
            continue
        existing = merged.get(key)
        if not existing:
            merged[key] = member
            continue
        existing["department_ids"] = _dedupe(existing["department_ids"] + member["department_ids"])
        existing["departments"] = _dedupe(existing["departments"] + member["departments"])
        for field in ("user_id", "name", "en_name", "nickname", "email", "mobile", "status"):
            if not existing.get(field) and member.get(field):
                existing[field] = member[field]

    items = sorted(merged.values(), key=lambda item: (item["name"], item["open_id"], item["user_id"]))
    return {
        "version": 1,
        "generated_at": generated_at or datetime.now(timezone.utc).isoformat(),
        "member_count": len(items),
        "members": items,
    }


@dataclass
class MemberDirectory:
    members: list[dict[str, Any]]
    aliases: dict[str, str]

    @staticmethod
    def load_aliases(path: Path) -> dict[str, str]:
        payload = load_json(path, {})
        if not isinstance(payload, dict):
            raise ValueError("alias file must be a JSON object")
        return {str(key): str(value) for key, value in payload.items()}

    @classmethod
    def from_paths(cls, paths: ToolkitPaths) -> "MemberDirectory":
        member_payload = load_json(paths.members_file, {"members": []})
        members = member_payload.get("members", [])
        aliases = cls.load_aliases(paths.alias_file)
        return cls(members=members, aliases=aliases)

    def resolve(self, query: str) -> dict[str, Any]:
        lookup = query.strip()
        if not lookup:
            return {"status": "not_found", "query": query, "candidates": []}

        alias_target = self.aliases.get(lookup)
        if alias_target:
            member = self._find_by_exact_id(alias_target)
            if member:
                return {"status": "matched", "query": query, "member": member, "source": "alias"}

        exact_matches = self._exact_matches(lookup)
        if len(exact_matches) == 1:
            return {"status": "matched", "query": query, "member": exact_matches[0], "source": "exact"}
        if len(exact_matches) > 1:
            return {"status": "ambiguous", "query": query, "candidates": [self._candidate_view(item) for item in exact_matches]}

        fuzzy_matches = self._fuzzy_matches(lookup)
        if len(fuzzy_matches) == 1:
            return {"status": "matched", "query": query, "member": fuzzy_matches[0], "source": "fuzzy"}
        if len(fuzzy_matches) > 1:
            return {"status": "ambiguous", "query": query, "candidates": [self._candidate_view(item) for item in fuzzy_matches]}

        return {"status": "not_found", "query": query, "candidates": []}

    def validate_aliases(self) -> list[dict[str, str]]:
        invalid: list[dict[str, str]] = []
        for alias, target in sorted(self.aliases.items()):
            if not self._find_by_exact_id(target):
                invalid.append({"alias": alias, "target": target})
        return invalid

    def _find_by_exact_id(self, identity: str) -> dict[str, Any] | None:
        for member in self.members:
            if identity in {member.get("open_id"), member.get("user_id"), member.get("email"), member.get("mobile")}:
                return member
        return None

    def _exact_matches(self, lookup: str) -> list[dict[str, Any]]:
        lowered = lookup.casefold()
        matches = []
        for member in self.members:
            fields = [
                member.get("open_id", ""),
                member.get("user_id", ""),
                member.get("name", ""),
                member.get("en_name", ""),
                member.get("nickname", ""),
                member.get("email", ""),
                member.get("mobile", ""),
            ]
            if any(value and value.casefold() == lowered for value in fields):
                matches.append(member)
        return self._unique(matches)

    def _fuzzy_matches(self, lookup: str) -> list[dict[str, Any]]:
        lowered = lookup.casefold()
        matches = []
        for member in self.members:
            fields = [member.get("name", ""), member.get("en_name", ""), member.get("nickname", ""), member.get("email", "")]
            if any(lowered in value.casefold() for value in fields if value):
                matches.append(member)
        return self._unique(matches)

    def _unique(self, matches: list[dict[str, Any]]) -> list[dict[str, Any]]:
        unique: dict[str, dict[str, Any]] = {}
        for member in matches:
            unique[_candidate_key(member)] = member
        return list(unique.values())

    def _candidate_view(self, member: dict[str, Any]) -> dict[str, Any]:
        return {
            "open_id": member.get("open_id", ""),
            "name": member.get("name", ""),
            "email": member.get("email", ""),
            "departments": member.get("departments", []),
        }


def _scope_stub(open_id: str) -> dict[str, Any]:
    return {
        "open_id": open_id,
        "user_id": "",
        "name": "",
        "en_name": "",
        "nickname": "",
        "email": "",
        "mobile": "",
        "department_ids": [],
        "departments": [],
        "status": "active",
    }


def fetch_scope_users(client: FeishuHttpClient, user_ids: list[str]) -> list[dict[str, Any]]:
    items: list[dict[str, Any]] = []
    for open_id in user_ids:
        payload = client.request(
            "GET",
            f"/contact/v3/users/{open_id}",
            params={
                "user_id_type": "open_id",
                "department_id_type": "open_department_id",
            },
        )
        user = payload.get("user", {})
        items.append(
            {
                "open_id": user.get("open_id", open_id),
                "user_id": user.get("user_id", ""),
                "name": user.get("name", ""),
                "en_name": user.get("en_name", ""),
                "nickname": user.get("nickname", ""),
                "email": user.get("email", ""),
                "mobile": user.get("mobile", ""),
                "department_ids": user.get("department_ids", []),
                "departments": user.get("departments", []),
                "status": "active" if user.get("status") in (None, True) else str(user.get("status")),
            }
        )
    return items


def _extract_user_items(payload: dict[str, Any]) -> list[dict[str, Any]]:
    for key in ("items", "users", "user_list"):
        value = payload.get(key)
        if isinstance(value, list):
            return value
    return []


def _build_sync_warnings(member_table: dict[str, Any], scope: dict[str, list[str]]) -> list[dict[str, str]]:
    warnings: list[dict[str, str]] = []
    members = member_table.get("members", [])
    if members and all(not (item.get("name") or item.get("email") or item.get("mobile")) for item in members):
        warnings.append(
            {
                "code": "sparse_user_profiles",
                "message": (
                    "The current contact permissions expose only identifier fields for synced users. "
                    "Check the app's contact-field permissions if you expect names or emails."
                ),
            }
        )
    if scope.get("user_ids") and not scope.get("department_ids"):
        warnings.append(
            {
                "code": "direct_user_scope_only",
                "message": (
                    "The authorized contact scope contains direct users only and no departments. "
                    "Member sync can enrich only the fields returned by the single-user detail API."
                ),
            }
        )
    return warnings


def fetch_authorized_scope(client: FeishuHttpClient) -> dict[str, list[str]]:
    department_ids: list[str] = []
    user_ids: list[str] = []
    page_token = None
    while True:
        payload = client.request(
            "GET",
            "/contact/v3/scopes",
            params={
                "department_id_type": "open_department_id",
                "user_id_type": "open_id",
                "page_size": 50,
                "page_token": page_token,
            },
        )
        department_ids.extend(payload.get("department_ids", []))
        user_ids.extend(payload.get("user_ids", []))
        if not payload.get("has_more"):
            break
        page_token = payload.get("page_token")
        if not page_token:
            break
    return {"department_ids": _dedupe(department_ids), "user_ids": _dedupe(user_ids)}


def fetch_department_users(client: FeishuHttpClient, department_id: str) -> list[dict[str, Any]]:
    items: list[dict[str, Any]] = []
    page_token = None
    while True:
        payload = client.request(
            "GET",
            "/contact/v3/users/find_by_department",
            params={
                "department_id": department_id,
                "department_id_type": "open_department_id",
                "user_id_type": "open_id",
                "page_size": 50,
                "page_token": page_token,
            },
        )
        raw_items = _extract_user_items(payload)
        for raw in raw_items:
            department_ids = raw.get("department_ids") or [department_id]
            items.append(
                {
                    "open_id": raw.get("open_id", ""),
                    "user_id": raw.get("user_id", ""),
                    "name": raw.get("name", ""),
                    "en_name": raw.get("en_name", ""),
                    "nickname": raw.get("nickname", ""),
                    "email": raw.get("email", ""),
                    "mobile": raw.get("mobile", ""),
                    "department_ids": department_ids,
                    "departments": raw.get("departments", []),
                    "status": "active" if raw.get("status") in (None, True) else str(raw.get("status")),
                }
            )
        if not payload.get("has_more"):
            break
        page_token = payload.get("page_token")
        if not page_token:
            break
    return items


def sync_members(client: FeishuHttpClient, paths: ToolkitPaths) -> dict[str, Any]:
    paths.ensure()
    scope = fetch_authorized_scope(client)
    department_payload: dict[str, list[dict[str, Any]]] = {}
    for department_id in scope["department_ids"]:
        department_payload[department_id] = fetch_department_users(client, department_id)
    scope_users = fetch_scope_users(client, scope["user_ids"]) if scope["user_ids"] else []
    detailed_scope_ids = {item.get("open_id", "") for item in scope_users}
    for open_id in scope["user_ids"]:
        if open_id not in detailed_scope_ids:
            scope_users.append(_scope_stub(open_id))
    member_table = build_member_table(scope_users=scope_users, department_users=department_payload)
    warnings = _build_sync_warnings(member_table, scope)
    sync_meta = {
        "version": 1,
        "synced_at": member_table["generated_at"],
        "scope_department_ids": scope["department_ids"],
        "scope_user_ids": scope["user_ids"],
        "member_count": member_table["member_count"],
        "department_count": len(scope["department_ids"]),
        "warnings": warnings,
    }
    write_json(paths.members_file, member_table)
    write_json(paths.sync_meta_file, sync_meta)
    return {"members": member_table, "sync_meta": sync_meta}
