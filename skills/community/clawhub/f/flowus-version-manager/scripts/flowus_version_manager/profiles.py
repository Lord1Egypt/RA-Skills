"""Private shared configuration. Cloud data is never executable client configuration."""
from __future__ import annotations

import copy
import json
import re
import uuid
from urllib.parse import urlsplit

from . import __version__
from .common import Conflict, GateError, ManagerError, atomic_json, config_template, digest, stable_id
from .store import FIELDS, FlowUsStore, plain, rich

KIND = "flowus-version-manager/profile"
SETTINGS = {"vault_id", "business_parent_id", "approval_parent_id", "approval_probe_id",
            "databases", "view_pages", "inbox_page_id", "rules", "governance_mode"}
TARGETS = SETTINGS - {"rules"}
RULE_KEYS = {"categories", "continuous_categories", "continuous_keywords", "title_aliases",
             "business_terms", "extension_categories", "category_defaults", "ambiguous_names"}
DATABASES = {"documents", "versions", "events", "proposals", "approvals"}
VIEWS = {"latest", "history", "review"}
MAX_PROFILE = 256 * 1024


def root_id(value):
    if not isinstance(value, str):
        raise ManagerError("A FlowUs root page ID or URL is required")
    if "://" in value:
        parsed = urlsplit(value)
        if (parsed.scheme != "https" or parsed.hostname not in {"flowus.cn", "www.flowus.cn", "flowus.app"}
                or parsed.username or parsed.password or parsed.query or parsed.port not in (None, 443)):
            raise ManagerError("Use a plain HTTPS FlowUs page URL without credentials or query parameters")
        value = parsed.path.rstrip("/").rsplit("/", 1)[-1]
    try:
        return str(uuid.UUID(value))
    except (ValueError, AttributeError):
        raise ManagerError("Invalid FlowUs page ID") from None


def _identifier(value, *, optional=False):
    if optional and value == "":
        return
    if not isinstance(value, str) or root_id(value) != value:
        raise GateError("Shared configuration contains an invalid resource ID")


def _strings(values):
    if (not isinstance(values, list) or len(values) > 1000
            or any(not isinstance(v, str) or len(v) > 1000 for v in values)):
        raise GateError("Rule lists must contain bounded text values")


def _decode(text):
    def unique(pairs):
        value = {}
        for key, item in pairs:
            if key in value:
                raise GateError("Duplicate JSON keys in shared configuration")
            value[key] = item
        return value
    return json.loads(text, object_pairs_hook=unique)


def validate_rules(rules):
    if not isinstance(rules, dict) or set(rules) - RULE_KEYS:
        raise GateError("Unknown shared rule fields; credentials and client settings are not allowed")
    for key in RULE_KEYS - {"categories", "extension_categories", "title_aliases", "category_defaults"}:
        if key in rules:
            _strings(rules[key])
    for key in ("categories", "extension_categories", "title_aliases"):
        rows = rules.get(key, [])
        if not isinstance(rows, list) or len(rows) > 1000:
            raise GateError("Invalid shared rule collection")
        allowed = ({"contains", "equals", "title"} if key == "title_aliases" else
                   {"name", "title", "keywords", "extensions", "lifecycle", "retention"})
        for row in rows:
            if not isinstance(row, dict) or set(row) - allowed:
                raise GateError("Unknown shared rule entry fields")
            required = {"title"} if key == "title_aliases" else {"name", "title"}
            if not required <= set(row):
                raise GateError("Shared rule entry is missing its name or title")
            for field, value in row.items():
                if field in {"contains", "equals", "keywords", "extensions"}:
                    _strings(value)
                elif not isinstance(value, str) or len(value) > 1000:
                    raise GateError("Invalid shared rule text")
    defaults = rules.get("category_defaults", {})
    if not isinstance(defaults, dict) or len(defaults) > 1000:
        raise GateError("Invalid category defaults")
    for key, row in defaults.items():
        if (not isinstance(key, str) or not isinstance(row, dict)
                or set(row) - {"project", "file_type", "stage", "lifecycle"}
                or any(not isinstance(v, str) or len(v) > 1000 for v in row.values())):
            raise GateError("Invalid category default fields")


def validate_profile(profile, root):
    if not isinstance(profile, dict) or set(profile) != {
            "kind", "profile_schema_version", "config_version", "minimum_tool_version", "settings"}:
        raise GateError("Unknown profile fields or incomplete shared configuration")
    if profile["kind"] != KIND or type(profile["profile_schema_version"]) is not int or profile["profile_schema_version"] != 1:
        raise GateError("Unsupported shared configuration schema")
    if type(profile["config_version"]) is not int or profile["config_version"] < 1:
        raise GateError("Invalid shared configuration version")
    minimum = profile["minimum_tool_version"]
    if not isinstance(minimum, str) or not re.fullmatch(r"\d+\.\d+\.\d+", minimum):
        raise GateError("Invalid minimum tool version")
    if tuple(map(int, __version__.split("."))) < tuple(map(int, minimum.split("."))):
        raise GateError("Upgrade the skill before connecting to this profile")
    settings = profile["settings"]
    if not isinstance(settings, dict) or set(settings) != SETTINGS:
        raise GateError("Unknown shared settings; client state must remain local")
    for name in ("vault_id", "business_parent_id", "inbox_page_id", "approval_parent_id", "approval_probe_id"):
        _identifier(settings[name], optional=name.startswith("approval_"))
    if settings["business_parent_id"] != root:
        raise GateError("Profile belongs to a different root page")
    for key, names in (("databases", DATABASES), ("view_pages", VIEWS)):
        mapping = settings[key]
        if not isinstance(mapping, dict) or set(mapping) != names:
            raise GateError("Shared database or catalog mapping is incomplete")
        for value in mapping.values():
            _identifier(value)
        if len(set(mapping.values())) != len(mapping):
            raise GateError("Shared resources must use distinct IDs")
    if settings["governance_mode"] not in {"trusted_client", "isolated_approval"}:
        raise GateError("Unknown shared governance mode")
    if settings["governance_mode"] == "isolated_approval" and (
            not settings["approval_parent_id"] or not settings["approval_probe_id"]
            or settings["approval_parent_id"] == root):
        raise GateError("Isolated approval configuration must retain its separate parent and probe")
    validate_rules(settings["rules"])
    if len(json.dumps(profile, ensure_ascii=False).encode()) > MAX_PROFILE:
        raise GateError("Shared configuration exceeds its size limit")
    return profile


def export_profile(config, version=1):
    settings = {key: copy.deepcopy(config.get(key, "")) for key in SETTINGS}
    profile = {"kind": KIND, "profile_schema_version": 1, "config_version": version,
               "minimum_tool_version": "0.4.0", "settings": settings}
    return validate_profile(profile, config["business_parent_id"])


def children(writer, page):
    rows, cursor, seen = [], None, set()
    while True:
        path = f"/blocks/{page}/children?page_size=100"
        if cursor:
            from urllib.parse import quote
            path += "&start_cursor=" + quote(cursor, safe="")
        data, _ = writer.request("GET", path)
        rows.extend(data.get("results", []))
        if len(rows) > 2000:
            raise GateError("Page discovery exceeds its bound")
        if not data.get("has_more"):
            return rows
        cursor = data.get("next_cursor")
        if not isinstance(cursor, str) or not cursor or cursor in seen:
            raise GateError("Invalid page discovery cursor")
        seen.add(cursor)


def discover(writer, root, *, required=True):
    """Only traverse child pages within two levels; never inspect document databases."""
    queue, seen, found = [(root, 0)], set(), []
    while queue:
        page, depth = queue.pop(0)
        if page in seen:
            raise GateError("Cyclic or duplicate page discovery")
        seen.add(page)
        if len(seen) > 40:
            raise GateError("Too many child pages for bounded profile discovery")
        versions = []
        for block in children(writer, page):
            if block.get("type") == "code":
                text = plain(block.get("code", {}).get("rich_text"))
                if KIND in text:
                    if len(text.encode()) > MAX_PROFILE:
                        raise GateError("Shared configuration block exceeds its size limit")
                    try:
                        profile = validate_profile(_decode(text), root)
                    except ValueError:
                        raise GateError("Shared configuration is not valid JSON") from None
                    versions.append((profile, block["id"]))
            if depth < 2 and block.get("type") == "child_page":
                queue.append((block["id"], depth + 1))
        if versions:
            latest = max(p["config_version"] for p, _ in versions)
            active = [(p, b) for p, b in versions if p["config_version"] == latest]
            if len(active) != 1:
                raise Conflict("Multiple active profile revisions; reconcile before continuing")
            found.append((active[0][0], page, active[0][1]))
    if len(found) > 1:
        raise Conflict("Multiple shared configuration pages; choose a single authoritative profile")
    if not found:
        if required:
            raise GateError("No shared profile found; publish the existing configuration first, never provision a new library")
        return None
    return found[0]


def validate_resources(config, writer):
    store = FlowUsStore(config, writer=writer)
    for name, identifier in config["databases"].items():
        data, _ = store.client(name).request("GET", "/databases/" + identifier)
        expected = {"Name": "title", "ApprovalCode": "rich_text", "Decision": "select"} if name == "approvals" else FIELDS
        if data.get("id") != identifier or any(data.get("properties", {}).get(k, {}).get("type") != v for k, v in expected.items()):
            raise GateError("Configured database structure is incompatible")
        ancestor = data.get("parent", {})
        expected_root = config["approval_parent_id"] if name == "approvals" and config["governance_mode"] == "isolated_approval" else config["business_parent_id"]
        visited = set()
        while ancestor.get("page_id") != expected_root:
            parent = ancestor.get("page_id")
            if not parent or parent in visited or len(visited) >= 8:
                raise GateError("Configured database is outside the authorized root")
            visited.add(parent)
            page, _ = writer.request("GET", "/pages/" + parent)
            ancestor = page.get("parent", {})
    for identifier in [config["inbox_page_id"], *config["view_pages"].values()]:
        page, _ = writer.request("GET", "/pages/" + identifier)
        if page.get("id") != identifier or page.get("parent", {}).get("page_id") != config["business_parent_id"]:
            raise GateError("Configured inbox or catalog is outside the authorized root")


def _reference(profile, root, page, block):
    return {"root_id": root, "page_id": page, "block_id": block,
            "config_version": profile["config_version"], "fingerprint": digest(profile)}


def pull(config, path, writer, *, dry_run=False):
    previous = config.get("remote_profile")
    if not previous:
        raise GateError("No remote profile binding; use connect or config push first")
    root = root_id(previous["root_id"])
    profile, page, block = discover(writer, root)
    settings = profile["settings"]
    if any(config.get(k, "") != settings[k] for k in TARGETS) or page != previous["page_id"]:
        raise Conflict("Shared targets or governance changed; explicitly reconnect after human review")
    if profile["config_version"] < previous["config_version"]:
        raise Conflict("Shared configuration was rolled back; review before reconnecting")
    changed = digest(profile) != previous["fingerprint"]
    result = {"status": "changed" if changed else "current", "config_version": profile["config_version"], "dry_run": dry_run}
    if not dry_run:
        config["rules"] = copy.deepcopy(settings["rules"])
        config["remote_profile"] = _reference(profile, root, page, block)
        if path:
            atomic_json(path, config)
    return result


def connect(path, root, transport, *, agent_id=None, writer=None, dry_run=False, replace=False, existing=None, rest_auth=None):
    root = root_id(root)
    if transport not in {"rest", "mcp_relay"}:
        raise ManagerError("Choose an explicit connection transport")
    config = config_template()
    if agent_id is not None and (not isinstance(agent_id, str) or not agent_id.strip() or len(agent_id) > 200):
        raise ManagerError("Client agent ID must be nonblank text of at most 200 characters")
    config.update(transport=transport, agent_id=agent_id or "client-" + str(uuid.uuid4()))
    config["rest_auth"] = rest_auth or ((existing or {}).get("rest_auth", "environment") if transport == "rest" else "environment")
    from .common import rest_auth_mode
    rest_auth_mode(config)
    if existing is not None:
        config["network_mode"] = existing.get("network_mode", "system")
    writer = writer or FlowUsStore(config).writer
    page, _ = writer.request("GET", "/pages/" + root)
    if page.get("id") != root:
        raise GateError("Root page is not accessible")
    profile, profile_page, block = discover(writer, root)
    config.update(copy.deepcopy(profile["settings"]))
    rest_auth_mode(config)
    if transport == "mcp_relay" and config["governance_mode"] != "trusted_client":
        raise GateError("MCP relay requires the explicitly configured trusted-client mode")
    validate_resources(config, writer)
    config["remote_profile"] = _reference(profile, root, profile_page, block)
    if existing is not None:
        same = (all(existing.get(k, "") == config[k] for k in TARGETS)
                and existing.get("transport", "rest") == transport
                and existing.get("rest_auth", "environment") == config["rest_auth"])
        if not same and not replace:
            raise Conflict("Existing local binding differs; review the target and use connect --replace explicitly")
        config["agent_id"] = agent_id or existing["agent_id"]
        config["network_mode"] = existing.get("network_mode", "system")
        # Reconnection always requires independent write verification, even on the same machine.
    if not dry_run:
        if path.exists():
            atomic_json(path.with_name(path.name + ".before-connect-" + str(uuid.uuid4())), existing)
        atomic_json(path, config, exclusive=not path.exists())
    return {"status": "read_ready", "writes_enabled": False, "dry_run": dry_run,
            "config_version": profile["config_version"], "root_id": root,
            "next": "Run doctor --verify-writes using this client's identity before writing"}


def push(manager, path, *, dry_run=False):
    config, writer = manager.config, manager.store.writer
    root = root_id(config["business_parent_id"])
    current = discover(writer, root, required=False)
    previous = config.get("remote_profile")
    pending = config.get("pending_profile_push")
    if current and pending:
        active, page, block = current
        if (pending.get("fingerprint") == digest(active) and pending.get("page_id") == page
                and active["settings"] == export_profile(config)["settings"]):
            if dry_run:
                return {"status": "would_recover", "config_version": active["config_version"], "dry_run": True}
            manager.guard()
            config["remote_profile"] = _reference(active, root, page, block)
            manager.event(stable_id(config["vault_id"], "profile", digest(active)), "config_published",
                          {"config_version": active["config_version"], "fingerprint": digest(active)})
            config.pop("pending_profile_push", None)
            config.pop("pending_profile_publish", None)
            atomic_json(path, config)
            return {"status": "recovered", "config_version": active["config_version"], "page_id": page}
    if current:
        old, page, _ = current
        if not previous or previous["fingerprint"] != digest(old) or previous["page_id"] != page:
            raise Conflict("Remote profile changed; pull and review before publishing local rules")
        if any(old["settings"][key] != config.get(key, "") for key in TARGETS):
            raise Conflict("Changing shared targets requires explicit rebinding, not config push")
        version = old["config_version"] + 1
    else:
        if previous:
            raise Conflict("Previously bound profile is missing; do not silently recreate it")
        version = 1
    profile = export_profile(config, version)
    validate_resources(config, writer)
    if current and old["settings"] == profile["settings"]:
        if not dry_run and config.pop("pending_profile_publish", False):
            atomic_json(path, config)
        return {"status": "unchanged", "config_version": old["config_version"], "dry_run": dry_run}
    if dry_run:
        return {"status": "would_publish", "config_version": version, "dry_run": True}
    manager.guard()
    from .layout import ensure_page
    backend = ensure_page(config, path, writer, "backend", root, "AI 后台（按需查看）")
    if not current:
        page = ensure_page(config, path, writer, "profile", backend, "资料库配置")
        if discover(writer, root, required=False):
            raise Conflict("Another client published a profile; pull before retrying")
    elif digest(discover(writer, root)[0]) != digest(old):
        raise Conflict("Profile changed before publication")
    config["pending_profile_push"] = {"page_id": page, "fingerprint": digest(profile), "config_version": version}
    atomic_json(path, config)
    # Append immutable revisions instead of overwriting a block without conditional-update support.
    writer.request("PATCH", f"/blocks/{page}/children", {"children": [
        {"object": "block", "type": "code", "code": {"language": "json", "rich_text": rich(json.dumps(profile, ensure_ascii=False, indent=2))}}]})
    active, actual_page, block = discover(writer, root)
    if actual_page != page or digest(active) != digest(profile):
        raise Conflict("Concurrent profile publication; reconcile the active revision")
    config["remote_profile"] = _reference(profile, root, page, block)
    manager.event(stable_id(config["vault_id"], "profile", digest(profile)), "config_published",
                  {"config_version": version, "fingerprint": digest(profile)})
    config.pop("pending_profile_push", None)
    config.pop("pending_profile_publish", None)
    atomic_json(path, config)
    return {"status": "published", "config_version": version, "page_id": page}
