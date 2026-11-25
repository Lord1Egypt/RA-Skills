"""Bundled api-to-typemcp engine entry point.

Staged deterministic commands:
  inspect  — parse a supplied local structured spec and print a summary
  manifest — build a secret-free normalized manifest with canonical digest
  approve  — issue a single-use digest-bound approval receipt
  generate — render a TypeMCP project after receipt validation (Task 3 gate)
"""

from __future__ import annotations

import argparse
import json
import shutil
import sys
from pathlib import Path

# ---------------------------------------------------------------------------
# Module resolution — allow running as `python3 scripts/api_to_typemcp.py`
# or from the repository root.
# ---------------------------------------------------------------------------
SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

import intake  # noqa: E402
import structured_specs  # noqa: E402
import manifest as manifest_mod  # noqa: E402
import approval  # noqa: E402
import agent_clients  # noqa: E402
import install_mcp  # noqa: E402
import install_plan  # noqa: E402
import render  # noqa: E402
from swagger_ui import MAX_SWAGGER_UI_BYTES, SwaggerUIError, extract_spec_reference  # noqa: E402


def _emit(payload: dict) -> None:
    json.dump(payload, sys.stdout, indent=2, sort_keys=True)
    sys.stdout.write("\n")


def _safe_error(message: str) -> None:
    sys.stderr.write(f"error: {message}\n")
    raise SystemExit(2)


# ---------------------------------------------------------------------------
# Output-target safety
# ---------------------------------------------------------------------------

def _validate_output_target(output: str, replace: bool) -> Path:
    """Validate the generation output directory.

    Rules:
    - Must exist (no implicit creation of arbitrary paths).
    - Must be empty unless ``replace`` is True.
    - Must not be a symlink (escape prevention).
    - Resolved path must not contain ``..`` components relative to cwd.
    """
    p = Path(output)

    # Reject paths with parent-directory components before resolution.
    if ".." in p.parts:
        _safe_error(f"output path must not contain '..': {output}")

    if not p.exists():
        _safe_error(f"output directory does not exist: {output}")

    if not p.is_dir():
        _safe_error(f"output path is not a directory: {output}")

    # Symlink escape: resolve and compare.
    resolved = p.resolve()
    if p.is_symlink() or resolved != p.absolute():
        if p.is_symlink():
            _safe_error(
                f"output directory is a symlink; refusing to follow it for safety: {output}"
            )

    if not replace and any(p.iterdir()):
        _safe_error(
            f"output directory is non-empty: {output}. "
            "Pass --replace to overwrite existing content."
        )

    return resolved


# ---------------------------------------------------------------------------
# Commands
# ---------------------------------------------------------------------------

def _cmd_inspect(args: argparse.Namespace) -> None:
    # Swagger UI discovery is deliberately bounded to the supplied HTML. It
    # reports only a config reference; callers must separately supply the
    # structured spec and the CLI never fetches it.
    candidate = Path(args.file)
    if candidate.suffix.lower() in {".html", ".htm"} and candidate.is_file():
        try:
            if candidate.stat().st_size > MAX_SWAGGER_UI_BYTES:
                raise intake.IntakeError(
                    f"Swagger UI input exceeds {MAX_SWAGGER_UI_BYTES} byte limit"
                )
            content = candidate.read_text(encoding="utf-8")
            discovery = extract_spec_reference(content)
        except (OSError, UnicodeDecodeError) as exc:
            raise intake.IntakeError("input must be UTF-8 text") from exc
        except SwaggerUIError as exc:
            raise intake.IntakeError(str(exc)) from exc
        if discovery is not None:
            _emit({
                "source": {"kind": discovery["source_kind"], "descriptor": "local-swagger-ui"},
                "spec_url": discovery["spec_url"],
            })
            return

    _path, document, descriptor = intake.load_supplied_source(args.file, base_url=args.base_url)
    m = structured_specs.build_manifest(document, descriptor)

    # Detect source kind from the document itself.
    if "openapi" in document:
        kind = "openapi"
    elif "swagger" in document:
        kind = "swagger"
    else:
        kind = "unknown"

    _emit({
        "source": {"kind": kind, "descriptor": descriptor},
        "api_version": document.get("openapi") or document.get("swagger", ""),
        "title": document.get("info", {}).get("title", ""),
        "version": document.get("info", {}).get("version", ""),
        "operationCount": len(m.get("operations", [])),
    })


def _cmd_manifest(args: argparse.Namespace) -> None:
    _path, document, descriptor = intake.load_supplied_source(args.file, base_url=args.base_url)
    m = structured_specs.build_manifest(document, descriptor)
    if args.json:
        _emit(m)
    else:
        _emit({
            "manifest_digest": m["manifest_digest"],
            "operation_count": len(m["operations"]),
            "warnings": m.get("warnings", []),
        })


def _cmd_approve(args: argparse.Namespace) -> None:
    # Compute current digest to verify the caller's stated digest matches.
    _path, document, descriptor = intake.load_supplied_source(args.file, base_url=args.base_url)
    m = structured_specs.build_manifest(document, descriptor)
    current_digest = m["digest"]

    if args.manifest_digest != current_digest:
        _safe_error(
            f"provided digest {args.manifest_digest} does not match current "
            f"manifest digest {current_digest}; refusing to approve"
        )

    receipt_path = approval.issue_receipt(current_digest)
    _emit({
        "status": "approved",
        "manifest_digest": current_digest,
        "receipt": str(receipt_path),
    })


def _cmd_generate(args: argparse.Namespace) -> None:
    # Build manifest to get current digest.
    _path, document, descriptor = intake.load_supplied_source(args.file, base_url=args.base_url)
    m = structured_specs.build_manifest(document, descriptor)
    current_digest = m["digest"]

    # Structured specs require explicit digest confirmation on the generate
    # command line so the operator proves they reviewed the exact manifest.
    if args.confirm_manifest_digest != current_digest:
        _safe_error(
            f"confirmation digest {args.confirm_manifest_digest} does not match "
            f"current manifest digest {current_digest}; the manifest has changed"
        )

    # Reject local output-target mistakes before consuming the single-use
    # approval receipt, so the operator can correct a path and retry.
    output_dir = _validate_output_target(args.output, args.replace)

    # Validate the isolated-state approval receipt (single-use, HMAC-bound).
    try:
        approval.validate_and_consume_receipt(current_digest)
    except approval.ApprovalError as exc:
        _safe_error(str(exc))

    # Render the full TypeMCP stdio project.
    written: list[str] = []
    try:
        written = render.render_project(m, output_dir)
    except Exception as exc:
        _safe_error(f"render failed: {type(exc).__name__}")

    _emit({
        "status": "generated",
        "manifest_digest": current_digest,
        "output": str(output_dir),
        "files": written,
        "file_count": len(written),
    })

def _install_context(args: argparse.Namespace) -> tuple[agent_clients.McpServerSpec, install_plan.InstallPlan]:
    project = Path(args.project)
    home = Path(args.home).expanduser()
    selected = tuple(item.strip() for item in args.targets.split(",") if item.strip())
    spec = agent_clients.server_spec_from_project(project, server_name=args.server_name)
    detected = agent_clients.detect_clients(home=home, project=project, which=shutil.which)
    detected_ids = {client.id for client in detected}
    unknown = sorted(set(selected) - detected_ids)
    if unknown:
        _safe_error("requested agent target is not detected: " + ", ".join(unknown))
    try:
        plan = install_plan.build_plan(spec, selected=selected, home=home)
    except (agent_clients.AgentClientError, install_plan.InstallPlanError) as exc:
        _safe_error(str(exc))
    return spec, plan


def _cmd_install_plan(args: argparse.Namespace) -> None:
    _spec, plan = _install_context(args)
    _emit({"status": "review-required", "mode_prompt": "project-only-or-install", "plan_digest": plan.digest, "plan": plan.to_public_dict()})


def _cmd_install_approve(args: argparse.Namespace) -> None:
    receipt = approval.issue_receipt(args.plan_digest)
    _emit({"status": "install-approved", "plan_digest": args.plan_digest, "receipt": str(receipt)})


def _cmd_install_export(args: argparse.Namespace) -> None:
    try:
        spec = agent_clients.server_spec_from_project(Path(args.project), server_name=args.server_name)
        output = install_plan.write_portable_export(Path(args.project), spec)
    except (agent_clients.AgentClientError, install_plan.InstallPlanError) as exc:
        _safe_error(str(exc))
    _emit({"status": "portable-exported", "output": str(output), "mutated_agent_config": False})


def _cmd_install_apply(args: argparse.Namespace) -> None:
    spec, plan = _install_context(args)
    if args.confirm_plan_digest != plan.digest:
        _safe_error("confirmation digest does not match the current installation plan")
    try:
        results = install_mcp.apply_native_plan(plan, spec)
    except install_mcp.InstallError as exc:
        _safe_error(str(exc))
    _emit({"status": "installed", "plan_digest": plan.digest, "targets": [{"client_id": result.client_id, "config_path": str(result.config_path), "backup_path": str(result.backup_path), "status": result.status} for result in results]})


# ---------------------------------------------------------------------------
# CLI wiring
# ---------------------------------------------------------------------------

def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="api_to_typemcp",
        description="Bundled api-to-typemcp engine (deterministic, local-only).",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    # inspect
    p_inspect = sub.add_parser("inspect", help="Summarize a local structured spec.")
    p_inspect.add_argument("--file", required=True, help="Path to supplied local JSON/YAML/Markdown/HTML input.")
    p_inspect.add_argument("--base-url", help="Required explicit http(s) base URL for Markdown/HTML input.")
    p_inspect.add_argument("--json", action="store_true", help="Emit full JSON output.")

    # manifest
    p_manifest = sub.add_parser("manifest", help="Build a normalized manifest.")
    p_manifest.add_argument("--file", required=True, help="Path to supplied local input.")
    p_manifest.add_argument("--base-url", help="Required explicit http(s) base URL for Markdown/HTML input.")
    p_manifest.add_argument("--json", action="store_true", help="Emit the full manifest JSON.")

    # approve
    p_approve = sub.add_parser("approve", help="Issue an approval receipt for the current digest.")
    p_approve.add_argument("--file", required=True, help="Path to supplied local input.")
    p_approve.add_argument("--base-url", help="Required explicit http(s) base URL for Markdown/HTML input.")
    p_approve.add_argument(
        "--manifest-digest",
        required=True,
        help="Exact canonical digest to approve (must match current state).",
    )

    # generate
    p_generate = sub.add_parser("generate", help="Generate a TypeMCP project (Task 3 gate).")
    p_generate.add_argument("--file", required=True, help="Path to supplied local input.")
    p_generate.add_argument("--base-url", help="Required explicit http(s) base URL for Markdown/HTML input.")
    p_generate.add_argument("--output", required=True, help="Output directory (must exist and be empty unless --replace).")
    p_generate.add_argument("--replace", action="store_true", help="Allow writing into a non-empty output directory.")
    p_generate.add_argument(
        "--confirm-manifest-digest",
        required=True,
        help="Explicit confirmation of the current manifest digest.",
    )

    def add_install_context(command: argparse.ArgumentParser) -> None:
        command.add_argument("--project", required=True, help="Verified generated project directory.")
        command.add_argument("--home", default=str(Path.home()), help="Explicit agent-home directory; defaults to the current home.")
        command.add_argument("--targets", required=True, help="Comma-separated detected native targets.")
        command.add_argument("--server-name", default="api-mcp", help="Safe MCP server name for this project.")

    p_install_plan = sub.add_parser("install-plan", help="Read-only agent detection and secret-free install preview.")
    add_install_context(p_install_plan)

    p_install_approve = sub.add_parser("install-approve", help="Issue a one-time receipt for an exact reviewed install plan.")
    p_install_approve.add_argument("--plan-digest", required=True, help="Exact digest emitted by install-plan.")

    p_install_export = sub.add_parser("install-export", help="Write portable mcpServers JSON without changing agent settings.")
    p_install_export.add_argument("--project", required=True, help="Verified generated project directory.")
    p_install_export.add_argument("--server-name", default="api-mcp", help="Safe MCP server name for this project.")

    p_install_apply = sub.add_parser("install-apply", help="Apply an approved unchanged JSON-native install plan.")
    add_install_context(p_install_apply)
    p_install_apply.add_argument("--confirm-plan-digest", required=True, help="Exact digest emitted by install-plan and approved separately.")

    return parser


def main(argv: list[str] | None = None) -> None:
    parser = _build_parser()
    args = parser.parse_args(argv)

    try:
        if args.command == "inspect":
            _cmd_inspect(args)
        elif args.command == "manifest":
            _cmd_manifest(args)
        elif args.command == "approve":
            _cmd_approve(args)
        elif args.command == "generate":
            _cmd_generate(args)
        elif args.command == "install-plan":
            _cmd_install_plan(args)
        elif args.command == "install-approve":
            _cmd_install_approve(args)
        elif args.command == "install-export":
            _cmd_install_export(args)
        elif args.command == "install-apply":
            _cmd_install_apply(args)
    except intake.IntakeError as exc:
        _safe_error(str(exc))
    except structured_specs.StructuredSpecError as exc:
        _safe_error(str(exc))
    except approval.ApprovalError as exc:
        _safe_error(str(exc))
    except SystemExit:
        raise
    except Exception as exc:  # pragma: no cover — last-resort safety net
        _safe_error(f"unexpected internal error: {type(exc).__name__}")


if __name__ == "__main__":
    main()
