"""Compose first-run evidence without launching a CLI, scanning, or installing.

The agent collects the existing Core reports after checking the selected CLI's
entry-point safety. This helper only reads explicitly selected JSON and the
existing user-provided application-path cache. It never executes report text.
"""

from __future__ import annotations

import argparse
import json
import platform
import re
import shutil
import time
from pathlib import Path
from typing import Any

import app_path_cache

PRODUCTS = Path(__file__).resolve().parent.parent / "references" / "PRODUCTS.json"
ID = re.compile(r"[a-z0-9][a-z0-9_-]{0,99}\Z")
VERSION = re.compile(r"v?\d+(?:\.\d+){1,3}(?:[-+][A-Za-z0-9.-]+)?\Z")
MAX_BYTES = 1024 * 1024
RELEASE_API = "https://api.github.com/repos/dcc-mcp/dcc-mcp-core/releases/latest"


def read_object(path: Path) -> dict[str, Any]:
    """Bound input size and do not include local paths in errors."""
    with path.open("rb") as stream:
        raw = stream.read(MAX_BYTES + 1)
    if len(raw) > MAX_BYTES:
        raise ValueError("evidence exceeds the 1 MiB limit")
    value = json.loads(raw)
    if not isinstance(value, dict):
        raise TypeError("evidence must be a JSON object")
    return value


def identifier(value: Any) -> str:
    if not isinstance(value, str) or not ID.fullmatch(value):
        raise ValueError("evidence contains an invalid product identifier")
    return value


def version(value: Any) -> str | None:
    return value if isinstance(value, str) and VERSION.fullmatch(value) else None


def stable_version(value: Any) -> tuple[int, int, int] | None:
    if not isinstance(value, str):
        return None
    match = re.fullmatch(
        r"v?(0|[1-9]\d{0,8})\.(0|[1-9]\d{0,8})\.(0|[1-9]\d{0,8})(?:\+[A-Za-z0-9.-]+)?",
        value,
    )
    return tuple(int(part) for part in match.groups()) if match else None


def enum(value: Any, choices: tuple[str, ...], default: str = "unknown") -> str:
    return value if isinstance(value, str) and value in choices else default


def indexed_rows(report: dict[str, Any] | None, field: str) -> dict[str, dict]:
    if report is None:
        return {}
    rows = report.get(field)
    if not isinstance(rows, list):
        raise TypeError("evidence is missing its expected row array")
    result = {}
    for row in rows:
        if not isinstance(row, dict):
            raise TypeError("evidence contains an invalid row")
        key = identifier(row.get("id"))
        if key in result:
            raise ValueError("evidence contains duplicate product identifiers")
        result[key] = row
    return result


def update_summary(report: dict[str, Any] | None) -> dict[str, Any]:
    result: dict[str, Any] = {
        "installed_version": None,
        "runtime_version": None,
        "bundled_core_version": None,
        "latest_version": None,
        "version_status": "unknown",
        "reason": "safe_cli_inspection_not_supplied",
    }
    if report is None:
        return result
    if (
        report.get("schema_version") != "dcc-mcp.update-inspection.v1"
        or report.get("component") != "dcc-mcp-cli"
        or report.get("read_only") is not True
        or report.get("dry_run") is not True
    ):
        raise ValueError("unsupported update inspection schema")
    versions = report.get("versions")
    source = report.get("source")
    if not isinstance(versions, dict) or not isinstance(source, dict):
        raise TypeError("update inspection is missing version/source evidence")
    for field, output, expected_source in (
        ("installed", "installed_version", "package_manager_record"),
        ("runtime", "runtime_version", "executing_cli_build"),
        ("bundled_core", "bundled_core_version", "cli_workspace_build"),
    ):
        observation = versions.get(field)
        if (
            isinstance(observation, dict)
            and observation.get("source") == expected_source
            and observation.get("reason") is None
        ):
            result[output] = version(observation.get("version"))
    result["latest_version"] = version(report.get("latest_version"))
    result["reason"] = "explicit_update_inspection"
    # Retain the observation without converting offline/stale failure to current.
    age, ttl = source.get("cache_age_secs"), source.get("ttl_secs")
    checked = source.get("checked_at_unix_secs")
    elapsed = int(time.time()) - checked if type(checked) is int else None
    fresh = (
        source.get("offline") is False
        and type(age) is int
        and type(ttl) is int
        and 0 <= age < ttl
        and elapsed is not None
        and 0 <= elapsed < ttl
        and source.get("provider") == "official_github_release"
        and source.get("url") == RELEASE_API
        and report.get("channel") == "stable"
        and result["runtime_version"] is not None
        and result["latest_version"] is not None
        and source.get("reason") is None
        and source.get("refresh_error") is None
    )
    if fresh:
        current = stable_version(result["runtime_version"])
        latest = stable_version(result["latest_version"])
        expected = "unknown"
        if current is not None and latest is not None:
            expected = (
                "update_available"
                if latest > current
                else "ahead_of_channel"
                if latest < current
                else "up_to_date"
            )
        if report.get("version_status") == expected:
            result["version_status"] = expected
        else:
            result["reason"] = "inconsistent_update_evidence"
    else:
        result["reason"] = "offline_stale_or_unavailable_release_evidence"
    result["release_source"] = {
        "provider": enum(
            source.get("provider"),
            ("official_github_release", "gateway_update_cache", "unavailable"),
        ),
        "url": RELEASE_API if source.get("url") == RELEASE_API else None,
        "checked_at_unix_secs": checked
        if type(checked) is int and checked >= 0
        else None,
    }
    result["offline"] = source.get("offline") is True
    result["cache_age_secs"] = (
        max(age, elapsed)
        if type(age) is int and age >= 0 and elapsed is not None and elapsed >= 0
        else None
    )
    result["ttl_secs"] = ttl if type(ttl) is int and ttl > 0 else None
    return result


def build_report(
    *,
    cli: str = "dcc-mcp-cli",
    products: dict[str, Any] | None = None,
    host_report: dict[str, Any] | None = None,
    host_manifest: dict[str, Any] | None = None,
    decisions: list[dict[str, Any]] | None = None,
    update_report: dict[str, Any] | None = None,
    runtime_scope: str = "local",
) -> dict[str, Any]:
    """Project independent observations; absence never proves missing software."""
    products = products if products is not None else read_object(PRODUCTS)
    if runtime_scope != "local":
        raise ValueError("this local first-run report cannot describe a remote runtime")
    if host_report is not None and host_report.get("read_only") is not True:
        raise ValueError("expected a host doctor report")
    if host_manifest is not None and host_manifest.get("version") != "1":
        raise ValueError("unsupported host manifest schema")
    hosts = indexed_rows(host_report, "hosts")
    manifest = indexed_rows(host_manifest, "hosts")
    by_dcc = {}
    for decision in decisions or []:
        if (
            type(decision.get("schema_version")) is not int
            or decision.get("schema_version") != 1
        ):
            raise ValueError("unsupported local discovery decision schema")
        key = identifier(decision.get("dcc_type"))
        if key in by_dcc:
            raise ValueError("duplicate local discovery decisions")
        by_dcc[key] = decision
    entries = products.get("products", []) + products.get("application_routes", [])
    known = {identifier(row.get("id")): row for row in entries}
    os_name = {"Darwin": "macos", "Windows": "windows", "Linux": "linux"}.get(
        platform.system(), "unknown"
    )
    rows = []
    for key in sorted(known.keys() | hosts.keys() | manifest.keys() | by_dcc.keys()):
        host, definition, decision = (
            hosts.get(key, {}),
            manifest.get(key, {}),
            by_dcc.get(key, {}),
        )
        try:
            cached = app_path_cache.get_path(key)
            path_state = (
                "not_observed"
                if cached is None
                else "stale"
                if cached.get("stale")
                else "present"
            )
        except (OSError, ValueError, TypeError):
            path_state = "unavailable"
        host_status = enum(
            host.get("status"),
            (
                "available",
                "missing",
                "version_mismatch",
                "version_unknown",
                "unsupported_platform",
                "unknown_host",
                "invalid_spec",
            ),
        )
        registration = enum(
            decision.get("registry_registration"),
            ("present", "absent", "unknown"),
        )
        readiness = enum(
            decision.get("direct_readiness"), ("ready", "not_ready", "unknown")
        )
        count = decision.get("live_instances")
        count = count if type(count) is int and count >= 0 else None
        if (registration == "present" and (count is None or count == 0)) or (
            registration == "absent" and count != 0
        ):
            registration = "unknown"
        if registration != "present":
            readiness = "unknown"
        license_class = enum(definition.get("license"), ("open_source", "commercial"))
        channels = definition.get("install_channels")
        installable = (
            license_class == "open_source"
            and definition.get("self_provision") is True
            and version(definition.get("pinned_version")) is not None
            and isinstance(channels, list)
            and os_name in channels
        )
        if registration == "present" and readiness == "ready":
            category = "available_for_discovery"
        elif (
            registration == "present"
            or host_status in ("available", "version_mismatch", "version_unknown")
            or path_state == "present"
        ):
            category = "configuration_needed"
        elif installable:
            category = "install_available"
        else:
            category = "unknown"
        rows.append(
            {
                "product": key if key in known else None,
                "identity": {
                    "row_id": key,
                    "host_id": key if key in hosts or key in manifest else None,
                    "dcc_type": key if key in by_dcc or key in known else None,
                    "binding": "exact_identifier_only",
                },
                "category": category,
                "host_probe": host_status,
                "host_version": version(host.get("version")),
                "cached_path": path_state,
                # Current Core decisions do not inspect package installations.
                "adapter_installed": "unknown",
                "live_instances": count,
                "registered": registration,
                "healthy": readiness,
                "callable": "not_checked",
                "real_host_effect": "not_verified",
                "catalog": "bundled_skill_snapshot"
                if key in known
                else "explicit_evidence",
                "host_install": {
                    "status": "available" if installable else "not_established",
                    "version": version(definition.get("pinned_version"))
                    if installable
                    else None,
                    "requires_consent": True,
                },
            }
        )
    resolved = shutil.which(cli)
    versions = update_summary(update_report)
    return {
        "schema_version": "dcc-mcp.first-run.v1",
        "read_only": True,
        "environment": {"os": os_name, "architecture": platform.machine()},
        "runtime_scope": runtime_scope,
        "cli": {
            "availability": "found" if resolved else "missing",
            "availability_scope": "selected_executable_lookup",
            **versions,
        },
        "applications": rows,
        "summary": {
            category: sum(row["category"] == category for row in rows)
            for category in (
                "available_for_discovery",
                "configuration_needed",
                "install_available",
                "unknown",
            )
        },
        "automatic_actions": [],
        "limits": [
            "no_complete_software_scan",
            "catalog_is_not_installation",
            "readiness_is_not_a_successful_call",
            "no_runtime_or_latest_claim_without_evidence",
        ],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cli", default="dcc-mcp-cli")
    parser.add_argument("--host-report", type=Path)
    parser.add_argument("--host-manifest", type=Path)
    parser.add_argument("--decision", type=Path, action="append", default=[])
    parser.add_argument("--update-report", type=Path)
    parser.add_argument("--runtime-scope", choices=("local", "remote"), default="local")
    parser.add_argument("--pretty", action="store_true")
    args = parser.parse_args()
    try:
        result = build_report(
            cli=args.cli,
            host_report=read_object(args.host_report) if args.host_report else None,
            host_manifest=read_object(args.host_manifest)
            if args.host_manifest
            else None,
            decisions=[read_object(path) for path in args.decision],
            update_report=read_object(args.update_report)
            if args.update_report
            else None,
            runtime_scope=args.runtime_scope,
        )
    except (OSError, ValueError, TypeError, KeyError):
        print(
            json.dumps(
                {
                    "schema_version": "dcc-mcp.first-run.v1",
                    "error": "invalid_or_unavailable_evidence",
                }
            )
        )
        return 2
    print(json.dumps(result, indent=2 if args.pretty else None))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
