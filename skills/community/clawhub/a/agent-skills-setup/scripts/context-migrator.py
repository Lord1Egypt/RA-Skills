#!/usr/bin/env python3
"""Safe profile-aware CLI for agent context migration."""

from __future__ import annotations

import argparse
import contextlib
import copy
import hashlib
import io
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

_SCRIPT_DIR = str(Path(__file__).resolve().parent)
if _SCRIPT_DIR not in sys.path:
    sys.path.insert(0, _SCRIPT_DIR)

from migration_core import (
    ADAPTER_VERSIONS,
    AUTOMATIC_MIGRATION_POLICIES,
    AUTOMATIC_OBJECT_TYPES,
    INVENTORY_ONLY_OBJECT_TYPES,
    KNOWN_COMMANDS,
    OPT_IN_WRITABLE_OBJECT_TYPES,
    PlanItem,
    Registry,
    apply_plan,
    atomic_write,
    build_plan,
    build_plan_document,
    choose_surface,
    emit_mcp_document,
    git_provenance,
    hash_path,
    json_sha256,
    load_plan_document,
    parse_mcp_document,
    path_state,
    paths_overlap,
    rollback_manifest,
    resolve_output_path,
    scope_matches,
    validate_plan_document,
    verify_manifest,
    _plan_hash_payload,
    _preview_plan_item,
)

from acb.bundle import (
    ACB_CHECKSUMS_NAME,
    ACB_OBJECTS_DIR,
    ACB_SCHEMA_VERSION,
    ACBError,
    ACBManifest,
    ACBSecretLeak,
    collect_reauth,
    collect_rebuild,
    collect_requirements,
    collect_source_objects,
    file_entry_mode,
    load_manifest,
    make_bundle_id,
    restore_bundle_objects,
    sign_bundle,
    verify_bundle,
    verify_bundle_signature,
    validate_path_containment,
    write_bundle,
)
from acb.key_security import (
    KeyFileCreationError,
    assert_created_key_file,
    create_key_file,
    discard_created_key_file,
)
from detect.probes import (
    InstallState,
    ProbeResult,
    probe_app_bundle,
    probe_binary,
    probe_file_signature,
)


SCRIPT_DIR = Path(__file__).resolve().parent
REGISTRY_PATH = SCRIPT_DIR.parent / "references" / "registry-v2.json"
LEGACY_SCRIPT = SCRIPT_DIR / "legacy-smart-ide-migration.sh"


def emit(value: Any, as_json: bool) -> None:
    if as_json:
        print(json.dumps(value, indent=2, sort_keys=True))
        return
    if isinstance(value, list):
        for row in value:
            print(json.dumps(row, sort_keys=True))
    elif isinstance(value, dict):
        print(json.dumps(value, indent=2, sort_keys=True))
    else:
        print(value)


def common_workspace(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--workspace", type=Path, default=Path.cwd())
    parser.add_argument("--registry", type=Path, default=REGISTRY_PATH)
    parser.add_argument("--json", action="store_true")


def create_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Inventory, plan, apply, verify, and roll back agent context migrations."
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    detect = subparsers.add_parser("detect")
    common_workspace(detect)
    detect.add_argument("--product")
    detect.add_argument("--profile")

    inventory = subparsers.add_parser("inventory")
    common_workspace(inventory)
    inventory.add_argument("--product")
    inventory.add_argument("--profile")

    plan = subparsers.add_parser("plan")
    common_workspace(plan)
    plan.add_argument("--source", required=True)
    plan.add_argument("--target", required=True)
    plan.add_argument(
        "--objects", default="skills,instructions,mcp", help="comma-separated surfaces"
    )
    plan.add_argument(
        "--scope", choices=("user", "project", "local", "all"), default="project"
    )
    plan.add_argument("--output", type=Path)

    migrate = subparsers.add_parser(
        "migrate",
        help="One-sentence migration: detect -> inventory -> plan -> apply -> verify.",
    )
    common_workspace(migrate)
    migrate.add_argument("--source", required=True, help="<product>/<profile>")
    migrate.add_argument("--target", required=True, help="<product>/<profile>")
    migrate.add_argument(
        "--objects",
        default="all-portable",
        help=(
            "Comma-separated object list, 'all-portable' (default), or "
            "'all-inventory' (also records forbidden/generated items)."
        ),
    )
    migrate.add_argument(
        "--scope",
        default="user,project",
        help="user, project, user+project, all (all requires --yes)",
    )
    migrate.add_argument(
        "--plan-only", action="store_true", help="Stop after planning."
    )
    migrate.add_argument("--plan-out", type=Path)
    migrate.add_argument("--manifest-out", type=Path)
    migrate.add_argument("--verify-out", type=Path)
    migrate.add_argument("--yes", action="store_true")
    migrate.add_argument(
        "--include",
        dest="include_lossy",
        choices=("lossy",),
        help="Also apply ready-lossy items.",
    )
    migrate.add_argument(
        "--accept-loss",
        dest="accept_loss",
        default="",
        help="Comma-separated plan indices to apply as lossy.",
    )
    migrate.add_argument(
        "--strict",
        action="store_true",
        help="Reject plans containing any non-ready item.",
    )

    migrate.add_argument(
        "--include-session",
        dest="include_session",
        action="store_true",
        help=(
            "Explicitly opt in to handoff/session transfer "
            "(whitelisted fields only: reviewed summary, git branch, "
            "selected file list, reviewed patch)."
        ),
    )
    migrate.add_argument(
        "--include-plugins",
        dest="include_plugins",
        action="store_true",
        help="Explicitly opt in to plugin package transfer.",
    )
    apply = subparsers.add_parser("apply")
    apply.add_argument("plan", type=Path)
    apply.add_argument("--registry", type=Path, default=REGISTRY_PATH)
    apply.add_argument("--manifest", type=Path)
    apply.add_argument(
        "--bundle",
        type=Path,
        help="Path to .acb bundle archive for bundle-backed restore plans.",
    )
    apply.add_argument("--yes", action="store_true")
    apply.add_argument("--json", action="store_true")
    apply.add_argument(
        "--apply-safe",
        dest="apply_safe",
        action="store_true",
        default=True,
        help="Apply ready and draft-disabled items; manifest the rest (default).",
    )
    apply.add_argument(
        "--no-apply-safe",
        dest="apply_safe",
        action="store_false",
        help="Disable safe apply; require every item to be ready.",
    )
    apply.add_argument(
        "--include",
        dest="include_lossy",
        choices=("lossy",),
        help="Include lossy items alongside ready items.",
    )
    apply.add_argument(
        "--accept-loss",
        dest="accept_loss",
        default="",
        help="Comma-separated plan indices to apply as lossy even without --include lossy.",
    )
    apply.add_argument(
        "--strict",
        action="store_true",
        help="Reject any plan containing a non-ready item (legacy semantics).",
    )

    apply.add_argument(
        "--include-session",
        dest="include_session",
        action="store_true",
        help=(
            "Explicitly opt in to handoff/session transfer for replayed "
            "plans (whitelisted fields only)."
        ),
    )
    apply.add_argument(
        "--include-plugins",
        dest="include_plugins",
        action="store_true",
        help="Explicitly opt in to plugin package transfer.",
    )
    verify = subparsers.add_parser("verify")
    verify.add_argument("--manifest", type=Path, required=True)
    verify.add_argument("--json", action="store_true")

    rollback = subparsers.add_parser("rollback")
    rollback.add_argument("--manifest", type=Path, required=True)
    rollback.add_argument("--yes", action="store_true")
    rollback.add_argument("--json", action="store_true")

    legacy = subparsers.add_parser(
        "legacy", help="run the explicit lookup and zero-write compatibility interface"
    )
    legacy.add_argument("legacy_args", nargs=argparse.REMAINDER)

    snapshot = subparsers.add_parser(
        "snapshot",
        help="Capture a portable Agent Context Bundle (ACB) of the current device.",
    )
    common_workspace(snapshot)
    snapshot.add_argument("--output", type=Path, help="Bundle output directory (default: <workspace>/device.acb).")
    snapshot.add_argument("--source", default="cline/ide")
    snapshot.add_argument("--target", default="forge/cli")
    snapshot.add_argument("--scope", default="user,project")
    snapshot.add_argument(
        "--objects",
        default="skills,instructions,mcp",
        help=(
            "Comma-separated list of object types to include in the snapshot "
            "(default: skills,instructions,mcp). Use 'plugins' with "
            "--include-plugins and 'handoff' with --include-session to round-trip "
            "those opt-in objects through an ACB."
        ),
    )
    snapshot.add_argument(
        "--include-plugins",
        action="store_true",
        help="Explicitly opt in to opaque plugin package capture.",
    )
    snapshot.add_argument(
        "--include-session",
        action="store_true",
        help="Explicitly opt in to reviewed handoff capture (portable fields only).",
    )
    snapshot.add_argument(
        "--all-installed",
        action="store_true",
        help="Snapshot all detected and installed products on this device.",
    )
    snapshot.add_argument(
        "--include-configured",
        action="store_true",
        help="Include products detected in configured-only state.",
    )
    snapshot.add_argument(
        "--include-compatibility",
        action="store_true",
        help="Include products detected in compatibility-only state.",
    )

    verify_bundle = subparsers.add_parser(
        "bundle-verify",
        help="Verify checksums and optional Ed25519 signature inside an ACB directory.",
    )
    verify_bundle.add_argument("bundle", type=Path)
    verify_bundle.add_argument(
        "--trusted-key",
        type=Path,
        help="Path to trusted Ed25519 public key file to verify bundle signature.",
    )
    verify_bundle.add_argument("--json", action="store_true", default=True)

    bundle_sign = subparsers.add_parser(
        "bundle-sign",
        help="Sign an ACB directory with an Ed25519 private key.",
    )
    bundle_sign.add_argument("bundle", type=Path)
    bundle_sign.add_argument(
        "--key",
        type=Path,
        required=True,
        help="Path to an owner-only Ed25519 private key (POSIX mode 600 or private Windows ACL).",
    )
    bundle_sign.add_argument(
        "--signer",
        default="local-operator",
        help="Identifier or name of the signer.",
    )
    bundle_sign.add_argument("--json", action="store_true", default=True)

    bundle_keygen = subparsers.add_parser(
        "bundle-keygen",
        help="Generate Ed25519 keypair for signing and verifying ACBs.",
    )
    bundle_keygen.add_argument(
        "--out-private",
        type=Path,
        required=True,
        help="New owner-only private key path (POSIX mode 600 or private Windows ACL).",
    )
    bundle_keygen.add_argument(
        "--out-public",
        type=Path,
        required=True,
        help="Destination path for public key file.",
    )
    bundle_keygen.add_argument("--json", action="store_true", default=True)

    restore = subparsers.add_parser(
        "restore",
        help="Verify an ACB and rebuild a local restore plan against the current device.",
    )
    common_workspace(restore)
    restore.add_argument("bundle", type=Path)
    restore.add_argument("--source", default="cline/ide")
    restore.add_argument("--target", default="forge/cli")
    restore.add_argument("--scope", default="user,project")
    restore.add_argument(
        "--objects",
        default="skills,instructions,mcp",
        help=(
            "Comma-separated list of object types to include in the restore "
            "plan (default: skills,instructions,mcp). Use 'plugins' with "
            "--include-plugins and 'handoff' with --include-session to round-trip "
            "those opt-in objects through an ACB."
        ),
    )
    restore.add_argument(
        "--all-installed",
        action="store_true",
        help="Restore context across all detected and installed target products.",
    )
    restore.add_argument(
        "--include-configured",
        action="store_true",
        help="Include target products detected in configured-only state.",
    )
    restore.add_argument(
        "--include-compatibility",
        action="store_true",
        help="Include target products detected in compatibility-only state.",
    )
    restore.add_argument(
        "--include-session",
        dest="include_session",
        action="store_true",
        help="Explicitly opt in to handoff/session transfer.",
    )
    restore.add_argument(
        "--include-plugins",
        dest="include_plugins",
        action="store_true",
        help="Explicitly opt in to plugin package transfer.",
    )
    restore.add_argument(
        "--trusted-key",
        type=Path,
        help="Path to trusted Ed25519 public key file to verify bundle signature.",
    )
    restore.add_argument("--plan-out", type=Path)
    restore.add_argument(
        "--plan-in",
        "--plan",
        dest="plan_in",
        type=Path,
        help="Replay a previously reviewed plan document.",
    )
    restore.add_argument("--manifest-out", type=Path)
    restore.add_argument("--apply-safe", action="store_true", default=True)
    restore.add_argument(
        "--no-apply-safe", dest="apply_safe", action="store_false"
    )
    restore.add_argument(
        "--include", dest="include_lossy", choices=("lossy",),
    )
    restore.add_argument("--strict", action="store_true")
    restore.add_argument("--yes", action="store_true")
    restore.add_argument(
        "--plan-only",
        action="store_true",
        help="Build and review restore plan without applying to target surfaces.",
    )
    restore.add_argument(
        "--restore-root",
        type=Path,
        help="Explicit destination tree for object extraction after approved apply.",
    )
    restore.add_argument(
        "--allow-noop",
        action="store_true",
        help="Allow restore to succeed with zero applied items (otherwise a bundle that resolves no eligible items is a hard failure).",
    )
    restore.add_argument(
        "--dry-run",
        action="store_true",
        help="Plan and stage objects/ without writing.",
    )

    doctor = subparsers.add_parser(
        "doctor",
        help="Inspect an ACB and surface missing executables / re-auth actions.",
    )
    doctor.add_argument("bundle", type=Path)
    doctor.add_argument("--json", action="store_true", default=True)
    return parser


def selector(product: str | None, profile: str | None) -> str | None:
    if not product:
        if profile:
            raise ValueError("--profile requires --product")
        return None
    return f"{product}/{profile}" if profile else product


def reject_legacy_write(argv: list[str]) -> None:
    """Enforce the legacy subcommand as strictly read-only.

    The guarantee is structural, not flag filtering (audit SDI-4 /
    AST4): only the documented read-only modes --print-path and
    --dry-run are allowed through to the legacy engine at all.  Any
    other invocation — with or without --yes — is refused here.
    """
    if "--yes" in argv or "-y" in argv:
        raise ValueError(
            "legacy writes are disabled; create a saved plan with 'plan --output', "
            "then apply that exact plan file"
        )
    if not argv or "--help" in argv or "-h" in argv:
        return
    readonly = "--print-path" in argv or "--dry-run" in argv
    if not readonly:
        raise ValueError(
            "legacy subcommand is read-only lookup compatibility only: "
            "pass --print-path <ide> <object> or --dry-run. "
            "Use 'plan' / 'apply' for migrations."
        )


def resolve_objects(value: str) -> list[str]:
    """Translate --objects shorthand into an explicit object list."""
    tokens = [token.strip() for token in value.split(",") if token.strip()]
    if not tokens:
        return ["skills", "instructions", "mcp"]
    if tokens == ["all-portable"]:
        return ["skills", "instructions", "mcp"]
    if tokens == ["all-inventory"]:
        return [
            "skills",
            "instructions",
            "mcp",
            *sorted(INVENTORY_ONLY_OBJECT_TYPES),
        ]
    return tokens


def default_workspace_migration_dir(workspace: Path) -> Path:
    return workspace / ".migration"


def validate_artifact_output(
    path: Path,
    registry: Registry,
    document: dict[str, Any],
    protected_paths: list[Path] | None = None,
) -> None:
    """Keep reports and extracted objects away from inputs and live surfaces."""
    protected = [registry.path, *(protected_paths or [])]
    for item in document.get("items", []):
        for side in ("source", "target"):
            surface = item.get(side)
            if isinstance(surface, dict) and surface.get("resolved_path"):
                protected.append(Path(surface["resolved_path"]))
    if any(paths_overlap(path, candidate) for candidate in protected):
        raise ValueError(f"artifact output overlaps an input or migration surface: {path}")


def _registry_profile_detections(
    registry: Registry,
    product: str | None = None,
    profile: str | None = None,
) -> list[ProbeResult]:
    """Use the same resolved profiles and probe precedence for every command."""
    if product:
        product, separator, selected_profile = product.partition("/")
        if separator:
            if profile and profile != selected_profile:
                raise ValueError("conflicting profiles in --product and --profile")
            profile = selected_profile
        registry.profile(f"{product}/{profile}" if profile else product)
        products = {product: registry.products[product]}
    else:
        products = registry.products
    priority = {
        state: index for index, state in enumerate((
            InstallState.NOT_DETECTED, InstallState.AMBIGUOUS, InstallState.LEGACY,
            InstallState.CLOUD_CONNECTED, InstallState.COMPATIBILITY_ONLY,
            InstallState.CONFIGURED_ONLY, InstallState.INSTALLED,
        ))
    }
    results: dict[tuple[str, str], ProbeResult] = {}
    for product_id, definition in products.items():
        if not product and definition.get("alias_of"):
            continue
        selectors = (
            [f"{product_id}/{profile}"] if product and profile
            else [f"{product_id}/{key}" for key in definition.get("profiles", {})]
            or [product_id]
        )
        for selector in selectors:
            resolved_product, resolved_profile, resolved = registry.profile(selector)
            if profile and not product and resolved_profile != profile:
                continue
            key = (resolved_product, resolved_profile)
            if key in results:
                continue
            best = ProbeResult(*key, InstallState.NOT_DETECTED, ())
            for probe in resolved.get("detection", []) or []:
                if not isinstance(probe, dict):
                    continue
                kind = probe.get("type")
                if kind == "binary":
                    command = probe.get("command") or []
                    if isinstance(command, str):
                        command = [command]
                    names = command[:1] if command else probe.get("binaries", [])
                    if isinstance(names, str):
                        names = [names]
                    result = probe_binary(
                        *key, names,
                        version_command=probe.get("version_command"),
                        require_version=len(command) > 1,
                    )
                elif kind == "file-signature":
                    paths = [
                        registry.resolve_path({"path": str(raw)})[0]
                        for raw in probe.get("paths", [])
                    ]
                    result = probe_file_signature(*key, paths, home=registry.home)
                elif kind == "app-bundle":
                    result = probe_app_bundle(
                        *key, darwin_bundle_id=probe.get("darwin_bundle_id"),
                        home=registry.home,
                    )
                else:
                    # Undeclared implementations cannot prove installation.
                    continue
                if priority[result.state] > priority[best.state]:
                    best = result
                if best.state is InstallState.INSTALLED:
                    break

            # Concrete project surfaces supply local evidence even when the
            # project's directory lives beneath HOME. Shared paths remain opt-in.
            if best.state is not InstallState.INSTALLED:
                for object_type in sorted(AUTOMATIC_OBJECT_TYPES):
                    for surface in registry.surfaces(f"{key[0]}/{key[1]}", object_type):
                        if surface.scope != "project":
                            continue
                        result = probe_file_signature(
                            *key, [surface.resolved_path], home=registry.home,
                        )
                        if (
                            surface.location_role != "canonical"
                            and result.state is not InstallState.NOT_DETECTED
                        ):
                            result = ProbeResult(*key, InstallState.COMPATIBILITY_ONLY, result.evidence)
                        if priority[result.state] > priority[best.state]:
                            best = result
                        if best.state is InstallState.INSTALLED:
                            break
                    if best.state is InstallState.INSTALLED:
                        break
            results[key] = best
    if profile and not results:
        raise ValueError(f"unknown profile: {profile}")
    return [results[key] for key in sorted(results)]


def _select_installed_profiles(
    registry: Registry,
    include_configured: bool = False,
    include_compatibility: bool = False,
) -> tuple[set[str], dict[str, str]]:
    accepted = {InstallState.INSTALLED}
    if include_configured:
        accepted.add(InstallState.CONFIGURED_ONLY)
    if include_compatibility:
        accepted.add(InstallState.COMPATIBILITY_ONLY)
    detections = _registry_profile_detections(registry)
    return (
        {f"{row.product}/{row.profile}" for row in detections if row.state in accepted},
        {f"{row.product}/{row.profile}": row.state.value for row in detections},
    )


def run_detection(args: argparse.Namespace) -> int:
    registry = Registry(args.registry, args.workspace.resolve())
    detections = _registry_profile_detections(registry, args.product, args.profile)
    emit(
        {
            "ok": True,
            "stage": "detect",
            "platform": sys.platform,
            "home": str(registry.home),
            "detections": [row.to_dict() for row in detections],
        },
        args.json,
    )
    return 0


def run_snapshot(args: argparse.Namespace) -> int:
    """Capture a portable ACB snapshot of the current device.

    Strict Snapshot Allowlist (audit P0-2):
    - Collects only the requested source product/profile and requested scope(s).
    - Collects only portable object types (skills, instructions, mcp) in the migration plan.
    - Strictly rejects forbidden-regenerate, never-migrate, session, chat, runtime,
      database, generated memory, and trust/credential stores.
    """
    workspace = args.workspace.resolve()
    registry = Registry(args.registry, workspace)
    bundle_root = resolve_output_path(args.output or workspace / "device.acb")
    all_installed = getattr(args, "all_installed", False) or args.source in ("auto", "all-installed")
    inventory_rows = registry.inventory(None if all_installed else args.source)
    detect_rows = [row for row in inventory_rows if row.get("exists")]

    requested_scopes = {
        s.strip().lower()
        for s in (args.scope or "user,project").split(",")
        if s.strip()
    }
    if "all" in requested_scopes:
        requested_scopes = {"user", "project", "local"}
    allowed_object_types = set(
        resolve_objects(getattr(args, "objects", "skills,instructions,mcp"))
    )
    for object_type, flag in (("plugins", "include_plugins"), ("handoff", "include_session")):
        if object_type in allowed_object_types and not getattr(args, flag, False):
            raise ValueError(
                f"snapshot {object_type} requires --{flag.replace('_', '-')}"
            )

    all_installed = getattr(args, "all_installed", False) or args.source in ("auto", "all-installed")
    source_product, source_profile = (
        (None, None)
        if all_installed
        else (args.source.split("/", 1) if "/" in args.source else (args.source, None))
    )

    if all_installed:
        detected_selectors, detection_status = _select_installed_profiles(
            registry,
            include_configured=getattr(args, "include_configured", False),
            include_compatibility=getattr(args, "include_compatibility", False),
        )

        plan_rows: list[dict[str, Any]] = []
        failed_products: list[dict[str, str]] = []
        for selector in sorted(detected_selectors):
            try:
                doc = build_plan_document(
                    registry,
                    selector,
                    selector,
                    sorted(allowed_object_types),
                    args.scope,
                )
                plan_rows.extend(doc.get("items", []))
            except Exception as error:
                # Audit P1-2: never silently swallow per-product plan build
                # failures. Capture and surface them so the snapshot summary
                # can report parse_failed / plan_failed per product.
                failed_products.append({"selector": selector, "error": str(error)})
                print(
                    f"WARNING: failed to build plan for {selector}: {error}",
                    file=sys.stderr,
                )
    else:
        src_sel = args.source or "cline/ide"
        document = build_plan_document(
            registry,
            src_sel,
            args.target or src_sel,
            sorted(allowed_object_types),
            args.scope,
        )
        plan_rows = document.get("items", [])
    installed_products_list = (
            sorted(detected_selectors)
            if all_installed
            else sorted({row["product"] for row in detect_rows})
        )
    inventory_summary = {
        "installed_products": installed_products_list,
        "surface_count": sum(
            1 for row in inventory_rows if row.get("object_type")
        ),
        "detection_status": detection_status if all_installed else {},
        "failed_products": failed_products if all_installed else [],
    }
    requested_scopes = {
        source["scope"] for item in plan_rows
        if (source := item.get("source")) and scope_matches(source["scope"], args.scope)
    }
    validate_artifact_output(bundle_root, registry, {"items": plan_rows})

    # Only include authorized, planned objects in manifest
    manifest_objects = []
    for item in plan_rows:
        surface_type = item.get("object_type", "")
        item_scope = (item.get("source") or {}).get("scope", "")
        if surface_type not in allowed_object_types:
            continue
        if requested_scopes and item_scope not in requested_scopes:
            continue
        manifest_objects.append(
            {
                "object_id": item.get("object_id", ""),
                "product": (item.get("source") or {}).get("product", ""),
                "profile": (item.get("source") or {}).get("profile", ""),
                "surface": surface_type,
                "scope": item_scope,
                "status": item.get("status", ""),
                "reason": item.get("reason", ""),
                "secret_status": "clean",
            }
        )

    manifest = ACBManifest(
        schema_version=ACB_SCHEMA_VERSION,
        bundle_id=make_bundle_id(),
        created_at=datetime.now(timezone.utc).isoformat(),
        source_platform={
            "system": sys.platform,
            "python": sys.version.split()[0],
        },
        inventory_summary=inventory_summary,
        objects=manifest_objects,
    )
    # Copy source files under objects/ using strict allowlist (audit P0-2 & 0.8.25).
    if not all_installed:
        source_product, source_profile, _ = registry.profile(args.source)
    else:
        source_product, source_profile = None, None

    collect_summary = {"captured": 0, "manual_rebuild": 0, "excluded_by_policy": 0, "parse_failed": 0, "secret_rejected": 0, "conflict": 0}
    object_file_modes: dict[str, int] = {}
    try:
        objects_dir_files, collect_summary, object_file_map = collect_source_objects(
            registry,
            inventory_rows,
            home=registry.home,
            workspace=workspace,
            source_product=source_product,
            source_profile=source_profile,
            allowed_scopes=requested_scopes,
            allowed_object_types=allowed_object_types,
            plan_items=plan_rows,
            include_plugins=bool(getattr(args, "include_plugins", False)),
            include_session=bool(getattr(args, "include_session", False)),
            object_file_modes=object_file_modes,
        )
    except ACBError as error:
        # Parse failure during object collection - emit failure with summary
        inventory_summary["collection_summary"] = collect_summary
        emit(
            {
                "ok": False,
                "stage": "snapshot",
                "error": str(error),
                "summary": inventory_summary,
            },
            args.json,
        )
        return 1

    # compatibility: source_product x target_product matrix sourced from
    # Registry v2 migration_policy and support_level. Audit P1-2: check
    # migration_policy (bidirectional-reviewed) rather than assuming
    # support_level == "bidirectional-reviewed".
    compatibility_products = sorted(registry.products.keys())
    compatibility_pairs: list[dict[str, str]] = []
    for src in compatibility_products:
        src_product = registry.products.get(src, {})
        src_default_profile = src_product.get("default_profile", "cli")
        for tgt in compatibility_products:
            if src == tgt:
                continue
            tgt_product = registry.products.get(tgt, {})
            tgt_default_profile = tgt_product.get("default_profile", "cli")
            try:
                # Silently resolve: the matrix walks every product pair, and
                # Registry._log_resolution would otherwise spam one alias line
                # per call (O(N^2) stderr noise during snapshot).
                buffer = io.StringIO()
                with contextlib.redirect_stderr(buffer):
                    src_profile_data = registry.profile(f"{src}/{src_default_profile}")
                    tgt_profile_data = registry.profile(f"{tgt}/{tgt_default_profile}")
            except Exception as error:
                print(f"WARNING: failed to get profile for compatibility pair {src}->{tgt}: {error}", file=sys.stderr)
                continue
            # profile() returns (resolved_product, resolved_profile, profile_data)
            src_profile = src_profile_data[2] if len(src_profile_data) > 2 else {}
            tgt_profile = tgt_profile_data[2] if len(tgt_profile_data) > 2 else {}
            src_policy = src_profile.get("migration_policy") or src_profile.get("support_level")
            tgt_policy = tgt_profile.get("migration_policy") or tgt_profile.get("support_level")
            if (
                (src_policy == "bidirectional-reviewed" or src_policy in AUTOMATIC_MIGRATION_POLICIES)
                and (tgt_policy == "bidirectional-reviewed" or tgt_policy in AUTOMATIC_MIGRATION_POLICIES)
            ):
                compatibility_pairs.append({
                    "source": src,
                    "target": tgt,
                    "supported": True,
                    "evidence": src_profile.get("evidence"),
                })
    compatibility = {
        "schema_version": 2,
        "matrix_kind": "source_x_target_bidirectional_reviewed",
        "products": compatibility_products,
        "pairs": compatibility_pairs,
    }

    requirements, requirements_summary = collect_requirements(
        inventory_rows, plan_rows, objects_dir_files=objects_dir_files
    )
    reauth = collect_reauth(plan_rows)
    rebuild = collect_rebuild(plan_rows)
    # secrets_required: each entry is a non-secret description of a
    # credential the user must re-supply on the target device. The name
    # is derived from the MCP server's command / package, not the
    # object_id. The shape is designed so doctor / human readers can
    # understand "what credential" without inspecting the bundle.
    secrets_required = []
    for action in reauth:
        obj_id = action.get("object_id", "")
        # Audit P1-7: surface credential names instead of object IDs.
        # Derive a stable, human-readable name from the package/command
        # when possible, falling back to the object_id only when no
        # better signal is available.
        package = (
            action.get("source", {}).get("package")
            or action.get("source", {}).get("command")
            or ""
        )
        if package:
            cred_name = f"{package}::credential"
        else:
            cred_name = obj_id or "unknown-credential"
        secrets_required.append({
            "name": cred_name,
            "used_by": [obj_id] if obj_id else [],
            "recommended_storage": "environment-or-keychain",
        })
    try:
        write_bundle(
            bundle_root=bundle_root,
            manifest=manifest,
            inventory_rows=inventory_rows,
            compatibility=compatibility,
            requirements=requirements,
            secrets_required=secrets_required,
            reauth=reauth,
            rebuild=rebuild,
            objects_dir_files=objects_dir_files,
            adapter_versions=ADAPTER_VERSIONS,
            object_file_map=object_file_map,
            object_file_modes=object_file_modes,
        )
    except ACBSecretLeak as error:
        print(f"ERROR: ACB secret leak: {error}", file=sys.stderr)
        return 1
    emit(
        {
            "ok": True,
            "stage": "snapshot",
            "bundle": str(bundle_root),
            "bundle_id": manifest.bundle_id,
            "manifest": str(bundle_root / "manifest.json"),
            "checksums": str(bundle_root / ACB_CHECKSUMS_NAME),
            "objects_dir": str(bundle_root / ACB_OBJECTS_DIR),
            "objects_captured": sum(bool(files) for files in object_file_map.values()),
            "files_captured": len(objects_dir_files),
            "detected": detect_rows[:50],
            "summary": inventory_summary,
            "collection_summary": collect_summary,
        },
        args.json,
    )
    return 0


def run_bundle_verify(args: argparse.Namespace) -> int:
    """Verify checksums and optional Ed25519 signature for an ACB."""
    bundle_path = args.bundle.resolve()
    errors = verify_bundle(bundle_path)
    trusted_key = getattr(args, "trusted_key", None)
    if trusted_key:
        sig_errors = verify_bundle_signature(bundle_path, trusted_key)
        errors.extend(sig_errors)
    emit(
        {
            "ok": not errors,
            "bundle": str(bundle_path),
            "errors": errors,
            "signature_verified": bool(trusted_key and not errors),
        },
        args.json,
    )
    return 0 if not errors else 1


def run_bundle_sign(args: argparse.Namespace) -> int:
    """Sign an ACB bundle with an Ed25519 private key."""
    bundle_path = args.bundle.resolve()
    try:
        sig_path = sign_bundle(bundle_path, args.key, signer=args.signer)
        emit(
            {
                "ok": True,
                "bundle": str(bundle_path),
                "signature": str(sig_path),
                "signer": args.signer,
            },
            args.json,
        )
        return 0
    except Exception as error:
        emit({"ok": False, "bundle": str(bundle_path), "error": str(error)}, args.json)
        return 1


def run_bundle_keygen(args: argparse.Namespace) -> int:
    """Generate Ed25519 keypair for signing and verifying ACBs."""
    outputs_requiring_review: list[str] = []
    cleanup_errors: list[str] = []
    try:
        from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
        from cryptography.hazmat.primitives import serialization
        priv = Ed25519PrivateKey.generate()
        priv_bytes = priv.private_bytes(
            encoding=serialization.Encoding.Raw,
            format=serialization.PrivateFormat.Raw,
            encryption_algorithm=serialization.NoEncryption(),
        )
        pub_bytes = priv.public_key().public_bytes(
            encoding=serialization.Encoding.Raw,
            format=serialization.PublicFormat.Raw,
        )
        out_priv = resolve_output_path(args.out_private)
        out_pub = resolve_output_path(args.out_public)
        if paths_overlap(out_priv, out_pub):
            raise ValueError("private and public key outputs must be distinct files")
        if out_priv.exists() or out_pub.exists():
            raise ValueError("key outputs already exist; choose new paths")
        out_priv.parent.mkdir(parents=True, exist_ok=True)
        out_pub.parent.mkdir(parents=True, exist_ok=True)
        written: list[tuple[Path, int]] = []
        try:
            for destination, data in ((out_priv, priv_bytes), (out_pub, pub_bytes)):
                descriptor = create_key_file(destination)
                written.append((destination, descriptor))
                pending = memoryview(data)
                while pending:
                    count = os.write(descriptor, pending)
                    if count <= 0:
                        raise OSError("key output write made no progress")
                    pending = pending[count:]
                os.fsync(descriptor)
            for destination, descriptor in written:
                assert_created_key_file(destination, descriptor)
        except BaseException:
            for destination, descriptor in written:
                try:
                    if not discard_created_key_file(descriptor):
                        outputs_requiring_review.append(str(destination))
                except Exception as cleanup_error:
                    outputs_requiring_review.append(str(destination))
                    cleanup_errors.append(str(cleanup_error))
            raise
        finally:
            for destination, descriptor in reversed(written):
                try:
                    os.close(descriptor)
                except OSError as close_error:
                    outputs_requiring_review.append(str(destination))
                    cleanup_errors.append(str(close_error))
        if cleanup_errors:
            raise OSError("closing generated key outputs failed")
        emit(
            {
                "ok": True,
                "private_key": str(out_priv),
                "public_key": str(out_pub),
            },
            args.json,
        )
        return 0
    except Exception as error:
        if isinstance(error, KeyFileCreationError):
            outputs_requiring_review.extend(error.outputs_requiring_review)
            cleanup_errors.extend(error.cleanup_errors)
        result: dict[str, Any] = {"ok": False, "error": str(error)}
        if outputs_requiring_review:
            result["outputs_requiring_review"] = list(dict.fromkeys(outputs_requiring_review))
        if cleanup_errors:
            result["cleanup_errors"] = cleanup_errors
        emit(result, args.json)
        return 1


def _detect_target_profiles_for_restore(
    target_registry: Registry,
    workspace: Path,
    include_configured: bool = False,
    include_compatibility: bool = False,
) -> tuple[set[str], dict[str, str]]:
    """Probe destination profiles with the same rules as detect and snapshot."""
    return _select_installed_profiles(target_registry, include_configured, include_compatibility)


def _safe_canonical(canonical: str) -> str:
    """Mirror ``acb.bundle._path_for_object``'s canonical transform.

    The snapshot stores captured files at
    ``objects/<obj_type>/<product>/<profile>/<scope>/<safe_canonical>/<rest>``.
    Replay must strip the metadata prefix and stage the rest under the same
    ``<safe_canonical>`` layout so a resolved_path can be rebuilt as
    ``<staging_root>/<safe_canonical>/<skill>/SKILL.md`` — matching the
    Process A staging that originally produced the plan.
    """
    safe = canonical.strip("/\\").replace("~", "home").replace("..", "_")
    safe = re.sub(r"[/\\:]+", "/", safe)
    return safe


def _merged_mcp_source_document(servers: list[Any]) -> tuple[str, list[dict[str, Any]]]:
    """Keep verified source fields inert in staging until loss-aware target emission."""
    rendered, report = emit_mcp_document(servers, "json:mcpServers")
    document = json.loads(rendered)
    for server in servers:
        fields = document["mcpServers"][server.name]
        fields.update(server.extra_fields)
        if server.args:
            fields["args"] = list(server.args)
        if server.env:
            fields["env"] = dict(server.env)
    return json.dumps(document, indent=2, sort_keys=True) + "\n", report.to_dict()["items"]


def _resolve_bundle_plan_sources(
    document: dict[str, Any],
    bundle_root: Path,
    staging_root: Path,
) -> list[Path]:
    """Re-stage plan sources from verified bundle objects (P0-1, v0.9.3).

    For every item carrying an ``acb_uri`` (``acb://<bundle-id>#<object-id>``),
    verify the bundle, look up the referenced manifest object, verify content
    hash, copy the object into a fresh ``staging_root/<object-id>/`` tree,
    and rewrite ``source.resolved_path`` to point at the freshly staged file.

    Items without an ``acb_uri`` are left untouched. The returned list
    contains the new staging root so the caller can clean it up.

    Raises:
        ValueError: bundle verification fails, the object is missing, or
            a content hash does not match.
    """
    objects_root = bundle_root / ACB_OBJECTS_DIR
    manifest = load_manifest(bundle_root)
    object_by_id: dict[str, dict[str, Any]] = {
        obj.get("object_id", ""): obj for obj in manifest.objects if obj.get("object_id")
    }

    # Verify the bundle once before staging anything. verify_bundle covers
    # closed-world file enumeration, manifest integrity, and per-object
    # secret/binary scans.
    errors = verify_bundle(bundle_root)
    if errors:
        raise ValueError(
            "bundle failed verification before plan replay: " + "; ".join(errors)
        )

    if staging_root.exists():
        shutil.rmtree(staging_root, ignore_errors=True)
    staging_root.mkdir(parents=True, exist_ok=True)

    def stage_source(item: dict[str, Any]) -> Path:
        acb_uri = item.get("acb_uri", "")
        src = item.get("source")
        if not isinstance(src, dict) or not isinstance(acb_uri, str):
            raise ValueError("bundle plan source must declare an acb_uri and surface")
        object_id = item.get("object_id", "")
        obj = object_by_id.get(object_id)
        if obj is None:
            raise ValueError(
                f"acb_uri {acb_uri} references unknown object_id {object_id}"
            )
        # Validate the URI matches the loaded bundle before doing any I/O.
        if not acb_uri.startswith("acb://"):
            raise ValueError(f"malformed acb_uri: {acb_uri}")
        uri_bundle, separator, uri_object = acb_uri[len("acb://"):].partition("#")
        if not separator or uri_object != object_id:
            raise ValueError(f"acb_uri object mismatch: {acb_uri}")
        if uri_bundle != manifest.bundle_id:
            raise ValueError(
                f"acb_uri bundle mismatch: uri={uri_bundle} bundle={manifest.bundle_id}"
            )
        for field in ("product", "profile", "scope"):
            if obj.get(field) != src.get(field):
                raise ValueError(f"bundle source {field} does not match manifest: {acb_uri}")
        if (obj.get("surface") or obj.get("object_type")) != src.get("object_type"):
            raise ValueError(f"bundle source object type does not match manifest: {acb_uri}")

        # The bundle stores files under objects/<obj_type>/<prod>/<prof>/<scope>/
        # <safe_canonical>/<rest> (see acb.bundle._path_for_object). We strip
        # that metadata prefix and give each object its own canonical tree
        # so shared paths from different products cannot overwrite each other.
        obj_prefix = (
            f"{src.get('object_type', '')}/{src.get('product', '')}/"
            f"{src.get('profile', '')}/{src.get('scope', '')}"
        )
        canonical_path = src.get("canonical_path", "") or src.get("path", "")
        safe_canonical = _safe_canonical(canonical_path)
        object_stage = validate_path_containment(object_id, staging_root)

        # Stage every declared file for this object under its isolated tree.
        staged_files: list[Path] = []
        for file_entry in obj.get("files", []):
            rel = file_entry.get("path", "")
            if not rel:
                continue
            rel_clean = (
                rel[len(ACB_OBJECTS_DIR) + 1:]
                if rel.startswith(ACB_OBJECTS_DIR + "/")
                else rel
            )
            prefix_with_sep = obj_prefix + "/"
            if rel_clean.startswith(prefix_with_sep):
                stripped = rel_clean[len(prefix_with_sep):]
            else:
                # Bundle predates the metadata-prefix convention: stage the
                # full rel_clean so the test still produces a usable tree.
                stripped = rel_clean
            src_file = validate_path_containment(rel_clean, objects_root)
            if not src_file.is_file() or src_file.is_symlink():
                raise ValueError(f"missing or symlinked object file: {rel}")
            expected_sha = file_entry.get("sha256", "")
            if expected_sha:
                actual_sha = hashlib.sha256(src_file.read_bytes()).hexdigest()
                if actual_sha != expected_sha:
                    raise ValueError(
                        f"object {object_id} file {rel} hash mismatch "
                        f"(expected {expected_sha[:12]}\u2026 got {actual_sha[:12]}\u2026)"
                    )
            tgt = validate_path_containment(stripped, object_stage)
            tgt.parent.mkdir(parents=True, exist_ok=True)
            tgt.write_bytes(src_file.read_bytes())
            mode = file_entry_mode(file_entry)
            if mode is not None:
                tgt.chmod(mode)
            staged_files.append(tgt)

        if not staged_files:
            raise ValueError(
                f"object {object_id} has no stageable files for replay"
            )

        # Rebind the exact reviewed file or child directory. An object can
        # contain multiple Skills; selecting its first SKILL.md loses the
        # identity of every later child and turns file sources into folders.
        boundary = object_stage / "home" if safe_canonical.startswith("home/") else object_stage
        try:
            relative_source = Path(src["resolved_path"]).relative_to(Path(src["boundary"]))
        except (KeyError, ValueError) as error:
            raise ValueError(f"invalid reviewed source boundary: {acb_uri}") from error
        source_path = validate_path_containment(relative_source, boundary)
        if not source_path.exists():
            raise ValueError(f"reviewed source is absent from bundle: {relative_source}")
        expected = item.get("source_state")
        if expected is not None and path_state(source_path) != expected:
            raise ValueError(f"bundle source changed after plan review: {relative_source}")
        src["resolved_path"] = str(source_path)
        src["boundary"] = str(boundary)
        return source_path

    resolved = 0
    for item in document.get("items", []):
        if not item.get("acb_uri") or not item.get("source"):
            continue
        merge_sources = item.get("acb_merge_sources")
        if merge_sources:
            servers_by_name: dict[str, Any] = {}
            for candidate in merge_sources:
                source_path = stage_source(candidate)
                for server in parse_mcp_document(
                    source_path.read_text(encoding="utf-8"),
                    candidate["source"]["source_format"],
                ):
                    servers_by_name.setdefault(server.name, server)
            names = item.get("acb_merge_server_names", [])
            if not isinstance(names, list) or any(name not in servers_by_name for name in names):
                raise ValueError("bundle MCP merge recipe names an absent server")
            rendered, _ = _merged_mcp_source_document(
                [servers_by_name[name] for name in names]
            )
            merged_file = staging_root / "mcp-merged" / f"{resolved}.json"
            atomic_write(merged_file, rendered)
            if path_state(merged_file) != item.get("source_state"):
                raise ValueError("bundle MCP merge changed after plan review")
            item["source"]["resolved_path"] = str(merged_file)
            item["source"]["boundary"] = str(merged_file.parent)
        else:
            stage_source(item)
        resolved += 1

    if resolved == 0 and any(item.get("acb_uri") for item in document.get("items", [])):
        # All items had acb_uri but none resolved: this is a hard error,
        # not a silent fallback. Forces operator attention on bad bundles.
        raise ValueError("plan declares acb_uri items but none resolved from bundle")

    return [staging_root]


def _build_all_installed_restore_items(
    source_registry: Registry,
    target_registry: Registry,
    bundle_source_selectors: list[str],
    target_detected_selectors: set[str],
    object_types: list[str],
    scope: str,
    staging_root: Path,
    bundle_id: str = "",
    bundle_objects: list[dict[str, Any]] | None = None,
) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, str]]]:
    """Build restore plan items with object-level identity, deduplication, and conflict tracking."""
    all_items: list[dict[str, Any]] = []
    dropped_losses: list[dict[str, Any]] = []
    seen_target_skills: dict[tuple[str, str], tuple[str, str]] = {}
    seen_target_files: dict[str, tuple[str, str]] = {}
    seen_target_plugins: dict[tuple[str, str], tuple[str, str]] = {}
    mcp_candidates_by_target: dict[str, list[tuple[dict[str, Any], str, str]]] = {}
    failed_targets: list[dict[str, str]] = []
    bundle_object_ids = {
        (obj.get("surface") or obj.get("object_type"), obj.get("product"), obj.get("profile"), obj.get("scope")): obj["object_id"]
        for obj in bundle_objects or [] if obj.get("files") and obj.get("object_id")
    }

    for tgt_selector in sorted(target_detected_selectors):
        for src_selector in bundle_source_selectors:
            try:
                doc = build_plan_document(
                    source_registry,
                    src_selector,
                    tgt_selector,
                    object_types,
                    scope,
                    target_registry=target_registry,
                )
                dropped_losses.extend(doc.get("loss_report", {}).get("items", []))
                for item in doc.get("items", []):
                    obj_type = item.get("object_type")
                    target_dict = item.get("target") or {}
                    source_dict = item.get("source") or {}
                    target_path = target_dict.get("resolved_path")
                    source_path_str = source_dict.get("resolved_path")
                    source_path = Path(source_path_str) if source_path_str else None

                    if not target_path or item.get("status") in {"invalid", "manual-rebuild"}:
                        continue

                    # P0-1 (0.9.3): attach a stable acb:// URI to every item so
                    # the plan document survives a cross-process replay. The
                    # object_id is already stable; the bundle_id is supplied
                    # by run_restore from the loaded manifest.
                    object_key = (obj_type, source_dict.get("product"), source_dict.get("profile"), source_dict.get("scope"))
                    if object_key in bundle_object_ids:
                        item["object_id"] = bundle_object_ids[object_key]
                    if bundle_id and item.get("object_id"):
                        item["acb_uri"] = f"acb://{bundle_id}#{item['object_id']}"

                    # Audit P0-1: Child-level skill conflict detection & deduplication (0.9.1)
                    if obj_type == "skills" and source_path and source_path.is_dir():
                        skill_subdirs = [
                            p for p in source_path.iterdir()
                            if p.is_dir() and (p / "SKILL.md").is_file()
                        ] if source_path.exists() else []

                        for skill_dir in skill_subdirs:
                            skill_name = skill_dir.name
                            skill_key = (target_path, skill_name)
                            skill_hash = hash_path(skill_dir)
                            child_target_path = str(Path(target_path) / skill_name)
                            child_source_path = str(skill_dir)

                            child_item = copy.deepcopy(item)
                            if child_item.get("source"):
                                child_item["source"]["resolved_path"] = child_source_path
                            if child_item.get("target"):
                                child_item["target"]["resolved_path"] = child_target_path
                            child_item["source_state"] = path_state(Path(child_source_path))
                            child_item["target_state"] = path_state(Path(child_target_path))

                            if skill_key in seen_target_skills:
                                prev_hash, prev_src = seen_target_skills[skill_key]
                                if skill_hash != prev_hash:
                                    conflict_msg = (
                                        f"Skill conflict on '{skill_name}': target {child_target_path} "
                                        f"already claimed by {prev_src} with differing content"
                                    )
                                    dropped_losses.append({
                                        "object_type": "skills",
                                        "field": skill_name,
                                        "reason": conflict_msg,
                                        "detail": None,
                                    })
                                    child_item["status"] = "conflict"
                                    child_item["reason"] = conflict_msg
                                    all_items.append(child_item)
                                # If skill_hash == prev_hash: identical deduplication (skip)
                            else:
                                seen_target_skills[skill_key] = (skill_hash, src_selector)
                                child_item["status"] = "ready"
                                all_items.append(child_item)

                    elif obj_type == "instructions":
                        target_path_obj = Path(target_path)
                        if target_dict.get("storage") == "file" or target_path_obj.suffix in (".md", ".json", ".txt"):
                            file_key = target_path
                            source_hash = hash_path(source_path) if (source_path and source_path.exists()) else ""
                            if file_key in seen_target_files:
                                prev_hash, prev_src = seen_target_files[file_key]
                                if source_hash == prev_hash:
                                    continue
                                else:
                                    item_copy = dict(item)
                                    item_copy["status"] = "conflict"
                                    item_copy["reason"] = (
                                        f"Instruction conflict: multiple sources ({prev_src}, {src_selector}) "
                                        f"target same file {target_path} with different content"
                                    )
                                    dropped_losses.append({
                                        "object_type": "instructions",
                                        "field": target_path,
                                        "reason": item_copy["reason"],
                                        "detail": None,
                                    })
                                    all_items.append(item_copy)
                            else:
                                seen_target_files[file_key] = (source_hash, src_selector)
                                all_items.append(item)
                        else:
                            all_items.append(item)

                    elif obj_type == "mcp":
                        mcp_candidates_by_target.setdefault(target_path, []).append(
                            (item, src_selector, source_path_str or "")
                        )

                    elif obj_type == "plugins":
                        pkg_name = source_path.name if source_path else "pkg"
                        plugin_key = (target_path, pkg_name)
                        source_hash = hash_path(source_path) if (source_path and source_path.exists()) else ""
                        if plugin_key in seen_target_plugins:
                            prev_hash, prev_src = seen_target_plugins[plugin_key]
                            if source_hash == prev_hash:
                                continue
                            else:
                                item_copy = dict(item)
                                item_copy["status"] = "conflict"
                                item_copy["reason"] = f"Plugin conflict: multiple sources ({prev_src}, {src_selector}) targeting {plugin_key}"
                                dropped_losses.append({
                                    "object_type": "plugins",
                                    "field": str(target_path),
                                    "reason": item_copy["reason"],
                                    "detail": None,
                                })
                                all_items.append(item_copy)
                        else:
                            seen_target_plugins[plugin_key] = (source_hash, src_selector)
                            all_items.append(item)

                    else:
                        all_items.append(item)

            except Exception as error:
                # Audit P1-2: never silently swallow per-target plan
                # build failures during all-installed restore. Surface
                # the failure so the restore summary can report it.
                failed_targets.append({
                    "source": src_selector,
                    "target": tgt_selector,
                    "error": str(error),
                })
                print(
                    f"WARNING: restore plan build failed for source={src_selector} target={tgt_selector}: {error}",
                    file=sys.stderr,
                )

    # Consolidate and merge multi-source MCP configs per target file (0.9.1)
    for target_path, candidates in sorted(mcp_candidates_by_target.items()):
        if len(candidates) == 1:
            all_items.append(candidates[0][0])
        else:
            hashes = [
                hash_path(Path(c[2])) for c in candidates
                if c[2] and Path(c[2]).is_file()
            ]
            if len(set(hashes)) == 1:
                all_items.append(candidates[0][0])
            else:
                seen_servers: dict[str, tuple[Any, str, dict[str, Any]]] = {}
                conflicting_servers: set[str] = set()
                for cand_item, cand_src, cand_path_str in candidates:
                    if not cand_path_str or not Path(cand_path_str).is_file():
                        continue
                    cand_path = Path(cand_path_str)
                    src_format = cand_item.get("source", {}).get("source_format", "json:mcpServers")
                    try:
                        text = cand_path.read_text(encoding="utf-8")
                        servers = parse_mcp_document(text, src_format)
                        for srv in servers:
                            if srv.name in seen_servers:
                                prev_srv, prev_src, _ = seen_servers[srv.name]
                                is_same = (
                                    srv.transport == prev_srv.transport
                                    and srv.command == prev_srv.command
                                    and srv.args == prev_srv.args
                                    and srv.env == prev_srv.env
                                    and srv.url == prev_srv.url
                                    and srv.headers == prev_srv.headers
                                    and srv.cwd == prev_srv.cwd
                                )
                                if not is_same:
                                    conflicting_servers.add(srv.name)
                                    conflict_msg = (
                                        f"MCP server conflict on '{srv.name}': differing command/args/transport "
                                        f"between {prev_src} and {cand_src}"
                                    )
                                    dropped_losses.append({
                                        "object_type": "mcp",
                                        "field": f"{srv.name}@{target_path}",
                                        "reason": conflict_msg,
                                        "detail": None,
                                    })
                            else:
                                seen_servers[srv.name] = (srv, cand_src, cand_item)
                    except Exception as error:
                        print(f"WARNING: failed to parse MCP document for {cand_src} ({cand_path_str}): {error}", file=sys.stderr)

                valid_servers = [
                    srv for name, (srv, _, _) in seen_servers.items()
                    if name not in conflicting_servers
                ]

                if valid_servers:
                    mcp_temp_dir = staging_root / "mcp-merged"
                    mcp_temp_dir.mkdir(parents=True, exist_ok=True)
                    merged_file = mcp_temp_dir / f"merged_mcp_{hashlib.sha256(target_path.encode()).hexdigest()[:8]}.json"
                    merged_text, merge_losses = _merged_mcp_source_document(valid_servers)
                    dropped_losses.extend(merge_losses)
                    atomic_write(merged_file, merged_text)

                    merged_item = copy.deepcopy(candidates[0][0])
                    merged_item["source"]["resolved_path"] = str(merged_file)
                    merged_item["source"]["boundary"] = str(mcp_temp_dir)
                    merged_item["source"]["source_format"] = "json:mcpServers"
                    merged_item["source_state"] = path_state(merged_file)
                    merged_item["target_state"] = path_state(Path(target_path))
                    merged_item["status"] = "ready-lossy" if merge_losses else "ready"
                    merged_item["reason"] = (
                        f"Merged {len(valid_servers)} MCP server(s) from multiple sources"
                        + ("; explicit loss acceptance required" if merge_losses else "")
                    )
                    merged_item["acb_merge_sources"] = [
                        {
                            "object_id": candidate[0].get("object_id"),
                            "acb_uri": candidate[0].get("acb_uri"),
                            "source": copy.deepcopy(candidate[0].get("source")),
                            "source_state": candidate[0].get("source_state"),
                        }
                        for candidate in candidates
                    ]
                    merged_item["acb_merge_server_names"] = [server.name for server in valid_servers]
                    all_items.append(merged_item)
                else:
                    conflict_item = copy.deepcopy(candidates[0][0])
                    conflict_item["status"] = "conflict"
                    conflict_item["reason"] = f"MCP conflict: all servers targeting {target_path} conflicted across sources"
                    conflict_item["source_state"] = path_state(Path(candidates[0][2])) if (candidates[0][2] and Path(candidates[0][2]).exists()) else None
                    conflict_item["target_state"] = path_state(Path(target_path))
                    all_items.append(conflict_item)

    for item in all_items:
        item["review_preview"] = _preview_plan_item(PlanItem.from_dict(item))
    unique_losses = {
        json.dumps(loss, sort_keys=True): loss for loss in dropped_losses
    }
    return all_items, list(unique_losses.values()), failed_targets


def _stage_bundle_source_registry(
    bundle_root: Path,
    target_registry: Registry,
    staging_root: Path,
    source_selector: str,
    scope: str,
    object_types: list[str],
) -> Registry:
    """Stage only the plan's bundle sources, independent of device overrides."""
    file_modes = {
        entry["path"]: file_entry_mode(entry)
        for obj in load_manifest(bundle_root).objects for entry in obj.get("files", [])
    }
    staged_home = staging_root / "home"
    staged_home.mkdir(parents=True, exist_ok=True)
    selected = None
    if source_selector not in ("auto", "all-installed"):
        product, profile, _ = target_registry.profile(source_selector)
        selected = (product, profile)
    objects_root = bundle_root / ACB_OBJECTS_DIR
    for source in sorted(objects_root.rglob("*")):
        if not source.is_file():
            continue
        parts = source.relative_to(objects_root).parts
        if len(parts) < 5:
            raise ValueError("bundle object has no product/profile/scope binding")
        object_type, product, profile, surface_scope = parts[:4]
        if object_type not in object_types or not scope_matches(surface_scope, scope):
            continue
        if selected is not None and selected != (product, profile):
            continue
        if parts[4] == "home":
            destination = validate_path_containment(Path(*parts[5:]), staged_home)
        else:
            boundary = staged_home if surface_scope in {"user", "shared-user"} else staging_root
            destination = validate_path_containment(Path(*parts[4:]), boundary)
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_bytes(source.read_bytes())
        mode = file_modes.get(f"{ACB_OBJECTS_DIR}/{source.relative_to(objects_root).as_posix()}")
        if mode is not None:
            destination.chmod(mode)
    return Registry(target_registry.path, staging_root, home=staged_home, portable_source=True)


def _bind_named_bundle_sources(
    document: dict[str, Any],
    bundle_root: Path,
    manifest: ACBManifest,
    *,
    bind_identity: bool = False,
) -> dict[str, Any]:
    """Bind named sources and return a staged-ID validation copy if needed."""
    identity = {
        "bundle_id": manifest.bundle_id,
        "manifest_sha256": hashlib.sha256(
            (bundle_root / "manifest.json").read_bytes()
        ).hexdigest(),
    }
    recorded_identity = document.get("bundle_source")
    if bind_identity:
        document["bundle_source"] = identity
    elif recorded_identity is not None and recorded_identity != identity:
        raise ValueError("bundle source identity does not match the reviewed plan")

    for item in document.get("items", []):
        source = item.get("source")
        source_state = item.get("source_state") or {}
        if not source or not source_state.get("exists"):
            if item.get("acb_uri"):
                raise ValueError("bundle source URI requires a captured source")
            continue
        object_id = item.get("object_id")
        strict_identity = not bind_identity and (
            recorded_identity is not None or item.get("acb_uri") is not None
        )
        if strict_identity:
            matches = [obj for obj in manifest.objects if obj.get("object_id") == object_id]
        else:
            matches = [
                obj for obj in manifest.objects
                if all(source.get(field) == obj.get(field) for field in ("product", "profile", "scope"))
                and source.get("object_type") == (obj.get("surface") or obj.get("object_type"))
            ]
            exact_matches = [obj for obj in matches if obj.get("object_id") == object_id]
            if exact_matches:
                matches = exact_matches
        if len(matches) != 1:
            raise ValueError(f"bundle source object identity is absent or ambiguous: {object_id}")
        obj = matches[0]
        captured_id = obj.get("object_id")
        if not isinstance(captured_id, str) or not captured_id:
            raise ValueError("bundle source object identity must be a non-empty string")
        for field in ("product", "profile", "scope"):
            if source.get(field) != obj.get(field):
                raise ValueError(f"bundle source {field} does not match the manifest")
        object_type = obj.get("surface") or obj.get("object_type")
        if source.get("object_type") != object_type or item.get("object_type") != object_type:
            raise ValueError("bundle source object type does not match the manifest")
        expected_uri = f"acb://{manifest.bundle_id}#{captured_id}"
        if bind_identity:
            item["object_id"] = captured_id
            item["acb_uri"] = expected_uri
        elif recorded_identity is not None or item.get("acb_uri") is not None:
            if item.get("acb_uri") != expected_uri:
                raise ValueError("bundle source URI does not match the manifest identity")

    if bind_identity:
        document["plan_sha256"] = json_sha256(_plan_hash_payload(document))
    # Environment overrides can give captured objects different IDs from the
    # portable Registry's canonical staging paths. Keep captured IDs in the
    # reviewed document while validating the freshly resolved named plan.
    execution_document = copy.deepcopy(document)
    for item in execution_document.get("items", []):
        if item.get("acb_uri") and item.get("source"):
            staged_item = PlanItem.from_dict({**item, "object_id": ""})
            item["object_id"] = staged_item.object_id
    return execution_document


def run_restore(args: argparse.Namespace) -> int:
    """Verify and rebuild a plan from an ACB on the current device.

    Dual-side Plan Architecture (audit P0-1 & P0-3):
    1. Restore source is ALWAYS the verified bundle. Local source installation on
       device B does not alter or replace bundle content.
    2. Bundle objects are staged into an isolated temporary source tree.
    3. Source surfaces are resolved from the staged source registry; target
       surfaces are resolved from the real destination registry on this device.
    4. The reviewed PlanDocument contains the real destination target paths,
       real pre-apply target states (evaluating exists -> replace vs create),
       real unified/semantic diffs against the destination, and real workspace.
    5. The hash of this exact document is locked as plan_sha256 and recorded in
       provenance upon apply.
    6. Executed target paths == reviewed plan target paths at all times.
    """
    bundle_root = args.bundle.resolve()
    errors = verify_bundle(bundle_root)
    trusted_key = getattr(args, "trusted_key", None)
    if trusted_key:
        sig_errors = verify_bundle_signature(bundle_root, trusted_key)
        errors.extend(sig_errors)
    if errors:
        emit({"ok": False, "stage": "verify", "errors": errors}, args.json)
        return 1
    manifest = load_manifest(bundle_root)
    workspace = args.workspace.resolve()
    target_registry = Registry(args.registry, workspace)
    all_installed = getattr(args, "all_installed", False) or args.target in ("auto", "all-installed")
    source_sel = args.source or "cline/ide"
    target_sel = args.target or "forge/cli"
    object_types = resolve_objects(getattr(args, "objects", "skills,instructions,mcp"))
    scope = args.scope
    plan_in = getattr(args, "plan_in", None)
    reviewed_document = load_plan_document(plan_in.resolve()) if plan_in else None
    if reviewed_document is not None:
        source_sel = reviewed_document["source"]
        target_sel = reviewed_document["target"]
        scope = reviewed_document["scope"]
        object_types = reviewed_document["objects"]
        all_installed = source_sel in ("auto", "all-installed") or target_sel in ("auto", "all-installed")
    detected = [row for row in target_registry.inventory(None if all_installed else target_sel) if row.get("exists")]
    have_bundle_objects = (bundle_root / ACB_OBJECTS_DIR).is_dir()

    # Optional object extraction into an explicit restore-root (audit #4:
    # opt-in; defaults OFF so we never imply a transaction landed there).
    restore_root = (
        resolve_output_path(args.restore_root) if args.restore_root else None
    )
    restore_result = (
        restore_bundle_objects(bundle_root, restore_root, dry_run=True)
        if restore_root is not None
        else None
    )

    temp_dir: str | None = None
    replay_staging_dirs: list[Path] = []
    try:
        temp_dir = tempfile.mkdtemp(prefix="acb-source-stage-")
        temp_source_dir = Path(temp_dir)
        source_registry = _stage_bundle_source_registry(
            bundle_root, target_registry, temp_source_dir,
            "all-installed" if all_installed else source_sel, scope, object_types,
        )
        if plan_in:
            document = reviewed_document
            # P0-1 (v0.9.3): replay path. Re-stage any acb:// items from
            # the verified bundle into a fresh temp dir before validation
            # so the resolved_path matches reality on a different process.
            # The replay staging must stay alive until apply_plan has read
            # each item's resolved_path (outer finally cleans it up).
            if (
                document.get("source") in ("all-installed", "auto")
                or document.get("target") in ("all-installed", "auto")
            ):
                replay_staging = Path(
                    tempfile.mkdtemp(prefix="acb-replay-stage-")
                )
                replay_staging_dirs.append(replay_staging)
                execution_document = copy.deepcopy(document)
                _resolve_bundle_plan_sources(
                    execution_document, bundle_root, replay_staging
                )
            else:
                execution_document = _bind_named_bundle_sources(
                    document, bundle_root, manifest
                )
            plan_items, _ = validate_plan_document(
                execution_document, target_registry, source_registry=source_registry
            )
        elif all_installed:
            target_detected_selectors, target_detection_status = (
                _detect_target_profiles_for_restore(
                    target_registry=target_registry,
                    workspace=workspace,
                    include_configured=getattr(args, "include_configured", False),
                    include_compatibility=getattr(args, "include_compatibility", False),
                )
            )

            bundle_source_selectors = sorted({
                f"{obj.get('product')}/{obj.get('profile')}"
                for obj in manifest.objects
                if obj.get("product") and obj.get("profile")
            })
            if not bundle_source_selectors:
                bundle_source_selectors = [source_sel] if source_sel else ["cline/ide"]

            all_items, dropped_losses, failed_targets = _build_all_installed_restore_items(
                source_registry=source_registry,
                target_registry=target_registry,
                bundle_source_selectors=bundle_source_selectors,
                target_detected_selectors=target_detected_selectors,
                object_types=object_types,
                scope=scope,
                staging_root=temp_source_dir,
                bundle_id=manifest.bundle_id,
                bundle_objects=manifest.objects,
            )

            document = {
                "schema_version": 1,
                "created_at": datetime.now(timezone.utc).isoformat(),
                "workspace": str(target_registry.workspace),
                "source": "all-installed",
                "source_profile": "all",
                "source_support_level": "bidirectional-reviewed",
                "target": "all-installed",
                "target_profile": "all",
                "target_support_level": "bidirectional-reviewed",
                "scope": scope,
                "objects": object_types,
                "registry_sha256": hash_path(target_registry.path),
                "adapter_versions": ADAPTER_VERSIONS,
                "git_provenance": git_provenance(target_registry.workspace),
                "items": all_items,
                "loss_report": {"dropped_fields": dropped_losses, "warnings": []},
                "rebuild_manifest": {
                    "credential_policy": "references-only; never include literal credentials",
                    "items": [],
                },
                "detection_status": target_detection_status,
                "failed_targets": failed_targets,
            }
            document["plan_sha256"] = json_sha256(_plan_hash_payload(document))
            plan_items, _ = validate_plan_document(
                document, target_registry, source_registry=source_registry
            )
        else:
            # Build dual-side plan: source=bundle (source_registry), target=destination device (target_registry)
            document = build_plan_document(
                source_registry,
                source_sel,
                target_sel,
                object_types,
                scope,
                target_registry=target_registry,
            )
            execution_document = _bind_named_bundle_sources(
                document, bundle_root, manifest, bind_identity=True
            )
            # Enforce TOCTOU state lock validation on the generated plan document
            plan_items, _ = validate_plan_document(
                execution_document, target_registry, source_registry=source_registry
            )

        # Preflight all artifact destinations before writing the first one.
        plan_out = resolve_output_path(args.plan_out) if args.plan_out else None
        manifest_out = resolve_output_path(args.manifest_out) if args.manifest_out else None
        outputs = [path for path in (plan_out, manifest_out, restore_root) if path is not None]
        for output in outputs:
            protected = [bundle_root, *(path for path in outputs if path != output)]
            if plan_in is not None:
                protected.append(plan_in)
            validate_artifact_output(output, target_registry, document, protected)
        if len(outputs) != len(set(outputs)):
            raise ValueError("restore artifact output paths must be distinct")
        args.manifest_out = manifest_out
        if plan_out is not None and not args.dry_run:
            atomic_write(
                plan_out,
                json.dumps(document, indent=2, sort_keys=True) + "\n",
            )

        plan_display = str(plan_out) if plan_out and not args.dry_run else (str(plan_in) if plan_in else None)

        if args.dry_run:
            # Zero-write guarantee for dry-run.
            emit(
                {
                    "ok": True,
                    "stage": "plan",
                    "bundle": str(bundle_root),
                    "bundle_id": manifest.bundle_id,
                    "plan": plan_display,
                    "plan_sha256": document["plan_sha256"],
                    "plan_document": document,
                    "restore": restore_result,
                    "dry_run": True,
                    "detected": detected[:50],
                    "failed_targets": document.get("failed_targets", []),
                },
                args.json,
            )
            return 0

        is_plan_only = getattr(args, "plan_only", False) or not args.yes
        if is_plan_only:
            emit(
                {
                    "ok": True,
                    "stage": "plan",
                    "bundle": str(bundle_root),
                    "bundle_id": manifest.bundle_id,
                    "plan": plan_display,
                    "plan_sha256": document["plan_sha256"],
                    "plan_document": document,
                    "restore": restore_result,
                    "detected": detected[:50],
                    "failed_targets": document.get("failed_targets", []),
                },
                args.json,
            )
            return 0

        # --no-apply-safe requires strict execution; it is not a preview switch.
        if have_bundle_objects and not any(
            item.status == "ready"
            or (item.status == "ready-lossy" and args.include_lossy == "lossy")
            or (item.status == "draft-disabled" and item.object_type in {"skills", "instructions", "mcp"})
            for item in plan_items
        ) and not getattr(args, "allow_noop", False):
            emit(
                {
                    "ok": False,
                    "stage": "apply",
                    "error": "restore resolved no eligible items; refusing silent no-op (use --allow-noop to override)",
                },
                args.json,
            )
            return 1
        return _apply_restore(
            plan_items, workspace, args, bundle_root, manifest,
            document, restore_result, detected,
        )
    finally:
        # The staged source tree (and any replay staging from --plan-in)
        # must stay alive until apply_plan has read it, so they are cleaned
        # up only here (audit #5: never leak to /tmp).
        for d in replay_staging_dirs:
            shutil.rmtree(d, ignore_errors=True)
        if temp_dir is not None and Path(temp_dir).exists():
            shutil.rmtree(temp_dir, ignore_errors=True)


def _apply_restore(
    plan_items: list,
    workspace: Path,
    args: argparse.Namespace,
    bundle_root: Path,
    manifest,
    document: dict,
    restore_result,
    detected,
) -> int:
    """Apply a resolved plan, verify it, and emit the result."""
    manifest_obj, manifest_path_out = apply_plan(
        plan_items, workspace, args.manifest_out,
        provenance={
            "bundle_path": str(bundle_root),
            "bundle_id": manifest.bundle_id,
            "plan_sha256": document["plan_sha256"],
            "registry_sha256": document["registry_sha256"],
            "adapter_versions": document["adapter_versions"],
        },
        apply_safe=args.apply_safe,
        include_lossy=(args.include_lossy == "lossy"),
        accept_loss_ids=set(),
        strict=args.strict or not args.apply_safe,
        allow_plugin_copy=bool(getattr(args, "include_plugins", False)),
        allow_session_handoff=bool(getattr(args, "include_session", False)),
    )
    verify_errors = verify_manifest(manifest_path_out)
    if not verify_errors and args.restore_root is not None:
        restore_result = restore_bundle_objects(
            bundle_root, args.restore_root, dry_run=False
        )
    emit(
        {
            "ok": not verify_errors,
            "stage": "verify",
            "bundle": str(bundle_root),
            "plan": str(args.plan_out or args.plan_in) if (args.plan_out or args.plan_in) else None,
            "plan_sha256": document["plan_sha256"],
            "manifest": str(manifest_path_out),
            "restore": restore_result,
            "stale_targets": [],
            "detected": detected[:50],
            "summary": manifest_obj.get("summary", {}),
            "errors": verify_errors,
            "failed_targets": document.get("failed_targets", []),
        },
        args.json,
    )
    return 0 if not verify_errors else 1


def run_doctor(args: argparse.Namespace) -> int:
    """Report recorded requirements and check executable presence only."""
    bundle_root = args.bundle.resolve()
    errors = verify_bundle(bundle_root)
    if errors:
        emit({"ok": False, "stage": "verify", "errors": errors}, args.json)
        return 1
    requirements = json.loads(
        (bundle_root / "requirements.json").read_text(encoding="utf-8")
    )
    reauth = json.loads((bundle_root / "reauth.json").read_text(encoding="utf-8"))
    rebuild = json.loads((bundle_root / "rebuild.json").read_text(encoding="utf-8"))
    missing_executables: list[str] = []
    executable_checks: list[dict[str, Any]] = []
    for binary in requirements.get("executables", []):
        found_on_path = shutil.which(binary) is not None
        executable_checks.append(
            {"executable": binary, "found_on_path": found_on_path}
        )
        if not found_on_path:
            missing_executables.append(binary)
    unresolved_requirements = {**requirements, "executables": missing_executables}
    emit(
        {
            "ok": not missing_executables,
            "bundle": str(bundle_root),
            "missing_executables": missing_executables,
            "requirements": requirements,
            "executable_checks": executable_checks,
            "unresolved_requirements": unresolved_requirements,
            "reauth_actions": reauth.get("items", []),
            "rebuild_actions": rebuild.get("items", []),
            "platform_notes": requirements.get("platform_notes", []),
        },
        args.json,
    )
    return 0 if not missing_executables else 1


def run_migrate(args: argparse.Namespace) -> int:
    """Orchestrate detect -> inventory -> plan -> apply -> verify."""
    workspace = args.workspace.resolve()
    registry = Registry(args.registry, workspace)

    # Inspect only the products named by this migration.
    selectors = {args.source, args.target}
    detect_rows = [
        row for named in sorted(selectors)
        for row in registry.inventory(named) if row.get("exists")
    ]

    # 2. Resolve --objects.
    object_types = resolve_objects(args.objects)

    # Reject unsupported automatic object types unless all-inventory.
    unsupported = sorted(
        set(object_types) - AUTOMATIC_OBJECT_TYPES - OPT_IN_WRITABLE_OBJECT_TYPES - INVENTORY_ONLY_OBJECT_TYPES
    )
    if unsupported:
        raise ValueError(
            "unsupported automatic objects: "
            + ", ".join(unsupported)
            + "; use --objects 'skills,instructions,mcp' or 'all-portable'"
        )
    # Previewing every scope does not authorize or require an apply.
    scope = args.scope.replace("+", ",")
    requested_scopes = [part.strip() for part in scope.split(",") if part.strip()]
    if not requested_scopes or any(part not in {"user", "project", "local", "all"} for part in requested_scopes):
        raise ValueError(f"unsupported scope: {args.scope}")
    if "all" in requested_scopes and len(requested_scopes) != 1:
        raise ValueError("--scope all cannot be combined with individual scopes")
    scope = ",".join(dict.fromkeys(requested_scopes))
    if scope == "all" and not args.plan_only and not args.yes:
        raise ValueError("--scope all requires --yes")

    # 4. plan
    document = build_plan_document(
        registry, args.source, args.target, object_types, scope,
    )

    # 5. save plan
    output_root = default_workspace_migration_dir(workspace)
    plan_out = resolve_output_path(args.plan_out or output_root / "migrate-plan.json")
    default_manifest_out = resolve_output_path(args.manifest_out or output_root / "migrate-manifest.json")
    verify_out = resolve_output_path(args.verify_out or output_root / "migrate-verify.json")
    artifacts = [plan_out] if args.plan_only else [plan_out, default_manifest_out, verify_out]
    for index, artifact in enumerate(artifacts):
        validate_artifact_output(artifact, registry, document, artifacts[:index])
    if not args.plan_only and default_manifest_out.exists():
        raise ValueError(f"manifest path already exists: {default_manifest_out}")
    plan_out.parent.mkdir(parents=True, exist_ok=True)
    atomic_write(
        plan_out,
        json.dumps(document, indent=2, sort_keys=True) + "\n",
    )

    if args.plan_only:
        emit(
            {
                "ok": True,
                "stage": "plan",
                "plan": str(plan_out),
                "plan_sha256": document["plan_sha256"],
                "detected": detect_rows,
            },
            args.json,
        )
        return 0

    # Validate the persisted artifact before applying it.
    document = load_plan_document(plan_out)
    plan_items, _ = validate_plan_document(document, registry)
    accept_loss_ids = {
        token.strip() for token in args.accept_loss.split(",") if token.strip()
    }
    manifest, manifest_path_out = apply_plan(
        plan_items,
        workspace,
        default_manifest_out,
        provenance={
            "plan_path": str(plan_out.resolve()),
            "plan_sha256": document["plan_sha256"],
            "registry_sha256": document["registry_sha256"],
            "adapter_versions": document["adapter_versions"],
            "git_provenance": document.get("git_provenance"),
        },
        apply_safe=True,
        include_lossy=(args.include_lossy == "lossy"),
        accept_loss_ids=accept_loss_ids,
        strict=args.strict,
        allow_plugin_copy=bool(getattr(args, "include_plugins", False)),
        allow_session_handoff=bool(getattr(args, "include_session", False)),
    )

    # 7. verify
    errors = verify_manifest(manifest_path_out)
    verify_out.parent.mkdir(parents=True, exist_ok=True)
    atomic_write(
        verify_out,
        json.dumps(
            {
                "ok": not errors,
                "errors": errors,
                "manifest": str(manifest_path_out),
                "plan": str(plan_out),
            },
            indent=2,
            sort_keys=True,
        )
        + "\n",
    )

    emit(
        {
            "ok": not errors,
            "stage": "verify",
            "plan": str(plan_out),
            "manifest": str(manifest_path_out),
            "verify": str(verify_out),
            "summary": manifest.get("summary", {}),
            "errors": errors,
            "detected": detect_rows,
        },
        args.json,
    )
    return 0 if not errors else 1


def run_legacy_cli(argv: list[str]) -> int:
    reject_legacy_write(argv)
    environment = dict(os.environ)
    environment["AGENT_SKILLS_SETUP_INTERNAL_LEGACY"] = "1"
    bash_exe = "bash"
    if os.name == "nt":
        # On Windows hosts PATH can resolve bare "bash" to the System32
        # WSL launcher, which is not an MSYS shell: its output carries
        # NUL bytes and its lookups return nothing. Prefer Git Bash.
        for candidate in (
            Path(os.environ.get("PROGRAMW6432", r"C:\Program Files")) / "Git" / "bin" / "bash.exe",
            Path(os.environ.get("ProgramFiles", r"C:\Program Files")) / "Git" / "usr" / "bin" / "bash.exe",
        ):
            if candidate.is_file():
                bash_exe = str(candidate)
                break
    completed = subprocess.run(
        [bash_exe, str(LEGACY_SCRIPT), *argv],
        check=False,
        env=environment,
    )
    return completed.returncode


def run_new_cli(argv: list[str]) -> int:
    args = create_parser().parse_args(argv)
    if args.command == "verify":
        errors = verify_manifest(args.manifest)
        result = {"ok": not errors, "errors": errors, "manifest": str(args.manifest)}
        emit(result, args.json)
        return 0 if not errors else 1
    if args.command == "rollback":
        if not args.yes:
            raise ValueError("rollback requires --yes")
        restored = rollback_manifest(args.manifest)
        emit({"ok": True, "restored": restored}, args.json)
        return 0

    if args.command == "apply":
        if not args.yes:
            raise ValueError("apply requires --yes after reviewing the saved plan")
        document = load_plan_document(args.plan)
        workspace_value = document.get("workspace")
        if not isinstance(workspace_value, str) or not Path(workspace_value).is_absolute():
            raise ValueError("plan workspace must be an absolute path")
        registry = Registry(args.registry, Path(workspace_value))

        source_registry = None
        temp_dir = None
        bundle_root = None
        try:
            if getattr(args, "bundle", None):
                bundle_root = args.bundle.resolve()
                errors = verify_bundle(bundle_root)
                if errors:
                    emit({"ok": False, "stage": "verify", "errors": errors}, args.json)
                    return 1
                temp_dir = tempfile.mkdtemp(prefix="acb-source-stage-")
                temp_source_dir = Path(temp_dir)
                source_registry = _stage_bundle_source_registry(
                    bundle_root, registry, temp_source_dir,
                    document["source"], document["scope"], document["objects"],
                )
                if document.get("source") in ("all-installed", "auto") or document.get("target") in ("all-installed", "auto"):
                    execution_document = copy.deepcopy(document)
                    _resolve_bundle_plan_sources(
                        execution_document, bundle_root, temp_source_dir / "replay"
                    )
                else:
                    execution_document = _bind_named_bundle_sources(
                        document, bundle_root, load_manifest(bundle_root)
                    )
            else:
                if document.get("bundle_source") is not None or any(
                    item.get("acb_uri") for item in document.get("items", [])
                ):
                    raise ValueError("bundle-backed plans require --bundle")
                execution_document = document

            plan_items, _ = validate_plan_document(
                execution_document, registry, source_registry=source_registry
            )
            accept_loss_ids = {
                token.strip()
                for token in args.accept_loss.split(",")
                if token.strip()
            }
            provenance = {
                "plan_path": str(args.plan.resolve()),
                "plan_sha256": document["plan_sha256"],
                "registry_sha256": document["registry_sha256"],
                "adapter_versions": document["adapter_versions"],
                "git_provenance": document.get("git_provenance"),
            }
            if bundle_root is not None:
                provenance["bundle_path"] = str(bundle_root)
            manifest, manifest_path = apply_plan(
                plan_items,
                registry.workspace,
                args.manifest,
                provenance=provenance,
                apply_safe=args.apply_safe,
                include_lossy=(args.include_lossy == "lossy"),
                accept_loss_ids=accept_loss_ids,
                strict=args.strict,
                allow_plugin_copy=bool(getattr(args, "include_plugins", False)),
                allow_session_handoff=bool(getattr(args, "include_session", False)),
            )
            emit(
                {
                    "ok": True,
                    "plan": str(args.plan),
                    "plan_sha256": document["plan_sha256"],
                    "manifest": str(manifest_path),
                    "changes": manifest["changes"],
                    "loss_report": manifest["loss_report"],
                },
                args.json,
            )
            return 0
        finally:
            if temp_dir is not None and Path(temp_dir).exists():
                shutil.rmtree(temp_dir, ignore_errors=True)

    if args.command == "migrate":
        if not getattr(args, "plan_only", False) and not args.yes:
            raise ValueError(
                "migrate requires --yes after specifying source/target/objects"
            )
        return run_migrate(args)

    if args.command == "snapshot":
        return run_snapshot(args)

    if args.command == "bundle-verify":
        return run_bundle_verify(args)

    if args.command == "bundle-sign":
        return run_bundle_sign(args)

    if args.command == "bundle-keygen":
        return run_bundle_keygen(args)

    if args.command == "restore":
        return run_restore(args)

    if args.command == "doctor":
        return run_doctor(args)

    registry = Registry(args.registry, args.workspace)
    if args.command in {"detect", "inventory"}:
        if args.command == "detect":
            return run_detection(args)
        selected = selector(args.product, args.profile)
        rows = registry.inventory(selected)
        emit(rows, args.json)
        return 0

    object_types = resolve_objects(args.objects)
    unsupported = sorted(
        set(object_types) - AUTOMATIC_OBJECT_TYPES - OPT_IN_WRITABLE_OBJECT_TYPES - INVENTORY_ONLY_OBJECT_TYPES
    )
    if unsupported:
        raise ValueError(f"unsupported automatic objects: {', '.join(unsupported)}")
    document = build_plan_document(
        registry,
        args.source,
        args.target,
        object_types,
        args.scope,
    )
    if args.output:
        output_path = args.output.resolve(strict=False)
        protected_paths = [args.registry.resolve(strict=False)]
        for item in document["items"]:
            for side in ("source", "target"):
                surface = item.get(side)
                if isinstance(surface, dict) and isinstance(
                    surface.get("resolved_path"), str
                ):
                    protected_paths.append(Path(surface["resolved_path"]))
        if any(paths_overlap(output_path, path) for path in protected_paths):
            raise ValueError(
                "plan output overlaps the Registry or a planned source/target "
                f"surface: {output_path}"
            )
        atomic_write(
            output_path,
            json.dumps(document, indent=2, sort_keys=True) + "\n",
        )
    emit(document, args.json)
    return 0


def main() -> int:
    argv = sys.argv[1:]
    if not argv or argv[0] in {"-h", "--help"}:
        create_parser().print_help()
        return 0
    if argv[0] == "legacy":
        try:
            return run_legacy_cli(argv[1:])
        except (OSError, ValueError, json.JSONDecodeError) as error:
            print(f"ERROR: {error}", file=sys.stderr)
            return 1
    if argv[0].startswith("-"):
        print(
            "ERROR: implicit legacy flags are disabled; use the explicit "
            "'legacy' subcommand for lookup or zero-write dry-run compatibility",
            file=sys.stderr,
        )
        return 2
    if argv[0] not in KNOWN_COMMANDS:
        print(f"ERROR: unknown command: {argv[0]}", file=sys.stderr)
        return 2
    try:
        return run_new_cli(argv)
    except (OSError, ValueError, json.JSONDecodeError) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
