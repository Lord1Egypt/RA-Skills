from __future__ import annotations

import argparse
import json
import os
import sys
import tempfile
from pathlib import Path

from . import __version__
from .archive import cloud_backup, cloud_restore, migrate
from .common import ManagerError, GateError, atomic_json, config_template, load_config, governance_mode, network_mode, transport_mode, credential_names, credential_value, rest_auth_mode
from .manager import Manager
from .rules import normalize_rules, safe_filename
from .setup import doctor, provision, download_preflight, error_details
from .store import FlowUsStore
from .transport import HTTP
from .views import after_write, refresh


def parser():
    p = argparse.ArgumentParser(description="FlowUs on-demand file version manager")
    p.add_argument("--version", action="version", version=__version__)
    p.add_argument("--config", type=Path, default=Path(os.environ.get("CVA_CONFIG", str(Path.home() / ".config/cloud-version-assistant/config.json"))))
    p.add_argument("--json", action="store_true", help="All command results are structured JSON")
    p.add_argument("--result-file", type=Path, help="Save the full private JSON result; stdout returns a compact receipt")
    p.add_argument("--prompt-credentials", action="store_true", help="Read required credentials privately with getpass; never save them")
    commands = p.add_subparsers(dest="command", required=True)
    init = commands.add_parser("init")
    mode = init.add_mutually_exclusive_group(required=True)
    mode.add_argument("--local", action="store_true", help="Create private configuration only; no network")
    mode.add_argument("--provision", action="store_true", help="Create cloud databases using the configured page roots")
    init.add_argument("--business-parent")
    init.add_argument("--approval-parent")
    init.add_argument("--rules", type=Path, help="Private business rules JSON; never packaged")
    init.add_argument("--governance-mode", choices=("trusted_client", "isolated_approval"),
                      help="Explicitly select the policy; changing it invalidates capability verification")
    init.add_argument("--network-mode", choices=("system", "direct"),
                      help="Select the tool's connection route explicitly; never changes system proxy settings")
    init.add_argument("--transport", choices=("rest", "mcp_relay"),
                      help="Select REST or the native MCP host relay; OAuth credentials remain in the MCP client")
    init.add_argument("--rest-auth", choices=("environment", "flowus_cli"))
    connect = commands.add_parser("connect", help="Connect to an existing library using only its root page")
    connect.add_argument("--root", required=True)
    connect.add_argument("--transport", choices=("rest", "mcp_relay"), required=True)
    connect.add_argument("--agent-id")
    connect.add_argument("--rest-auth", choices=("environment", "flowus_cli"))
    connect.add_argument("--replace", action="store_true", help="Explicitly replace a reviewed local binding; old config is backed up")
    connect.add_argument("--dry-run", action="store_true")
    shared = commands.add_parser("config", help="Publish or pull private shared configuration")
    shared.add_argument("action", choices=("push", "pull"))
    shared.add_argument("--dry-run", action="store_true")
    layout = commands.add_parser("layout", help="Organize the home and AI backend without replacing database records")
    layout.add_argument("--dry-run", action="store_true")
    layout.add_argument("--backup-dir", type=Path)
    check = commands.add_parser("doctor")
    check.add_argument("--offline", action="store_true")
    check.add_argument("--verify-writes", action="store_true", help="Use synthetic records to test real cloud capabilities")
    check.add_argument("--probe-block", help="GET-only attachment preflight before provisioning business databases")
    check.add_argument("--expected-sha256", help="Original hash for --probe-block; no signed URLs accepted")
    commands.add_parser("refresh", help="Refresh the generated latest/history/review catalogs")
    ingest = commands.add_parser("ingest")
    ingest.add_argument("paths", nargs="*", type=Path)
    ingest.add_argument("--cloud-inbox", action="store_true")
    for name in ("latest", "timeline"):
        commands.add_parser(name).add_argument("query", nargs="?", default="")
    commands.add_parser("ask").add_argument("question")
    note = commands.add_parser("note")
    note.add_argument("version_key")
    note.add_argument("--text", required=True)
    note.add_argument("--operation-id")
    proposal = commands.add_parser("propose")
    proposal.add_argument("action", choices=("replace_final", "merge", "reclassify", "reclassify_batch", "logical_delete"))
    proposal.add_argument("target", help="Document key")
    proposal.add_argument("--changes", default="{}", help="JSON object of version_key, destination, or category")
    approved = commands.add_parser("apply-approved")
    approved.add_argument("proposal_key", nargs="?")
    confirmed = commands.add_parser("apply-confirmed")
    confirmed.add_argument("proposal_key")
    confirmed.add_argument("--confirmation", required=True, type=Path,
                           help="Private JSON evidence quoting the actual human approval in the current chat")
    migration = commands.add_parser("migrate")
    migration.add_argument("vault", type=Path)
    migration.add_argument("--backup", type=Path)
    backup = commands.add_parser("backup")
    backup.add_argument("output", type=Path)
    restore = commands.add_parser("restore")
    restore.add_argument("backup", type=Path)
    for name in ("ingest", "note", "propose", "apply-approved", "apply-confirmed", "migrate", "backup", "restore", "refresh"):
        commands.choices[name].add_argument("--dry-run", action="store_true")
    return p


def inbox(manager, *, dry_run=False):
    page = manager.config.get("inbox_page_id")
    if not page:
        raise ManagerError("No cloud inbox configured; run init --provision")
    results = []
    summary = {"added": 0, "duplicates": 0, "needs_review": 0, "failed": 0}
    for block in manager.store.children(page):
        if block.get("type") != "file":
            continue
        if dry_run:
            results.append({"block_id": block["id"], "dry_run": True})
            continue
        try:
            manager.guard()
            info = block.get("file", {})
            if info.get("type") != "file":
                raise ManagerError("Inbox must contain internal downloadable FlowUs file blocks")
            content = manager.store.download_block(block)
            import hashlib
            operation = "inbox:" + block["id"] + ":" + hashlib.sha256(content).hexdigest()
            if manager.store.get("events", operation + ":inbox_processed"):
                summary["duplicates"] += 1
                continue
            from urllib.parse import unquote
            filename = safe_filename(info.get("name") or unquote(Path(info.get("file", {}).get("oss_name", "unnamed.bin")).name))
            with tempfile.TemporaryDirectory(prefix="cva-inbox-") as directory:
                path = Path(directory) / filename
                path.write_bytes(content)
                result = manager.ingest(path, source_ref="flowus:block:" + block["id"])
            manager.event(operation, "inbox_processed", result)
            summary[{"duplicate": "duplicates", "needs_review": "needs_review", "added": "added"}[result["outcome"]]] += 1
            results.append(result)
        except ManagerError as error:
            summary["failed"] += 1
            results.append({"block_id": block["id"], "status": "failed", "error": error.code, "message": str(error)})
            if isinstance(error, GateError):
                break
    return {"results": results, "summary": summary, "status": "partial_failure" if summary["failed"] else "completed",
            "source_blocks": "retained; processed blocks are skipped using operation records"}


def run(args):
    if args.command == "connect":
        from .profiles import connect
        existing = load_config(args.config) if args.config.exists() else None
        return connect(args.config, args.root, args.transport, agent_id=args.agent_id,
                       replace=args.replace, dry_run=args.dry_run, existing=existing, rest_auth=args.rest_auth)
    if args.command == "init":
        if args.local:
            config = load_config(args.config) if args.config.exists() else config_template()
        else:
            config = load_config(args.config)
        if args.business_parent:
            config["business_parent_id"] = args.business_parent
        if args.approval_parent:
            config["approval_parent_id"] = args.approval_parent
        if args.governance_mode:
            if governance_mode(config) != args.governance_mode:
                config.pop("capability_receipt", None)
            config["governance_mode"] = args.governance_mode
            config["tool_version"] = __version__
        if args.network_mode:
            if network_mode(config) != args.network_mode:
                config.pop("capability_receipt", None)
            config["network_mode"] = args.network_mode
            config["tool_version"] = __version__
        if args.transport:
            if transport_mode(config) != args.transport:
                config.pop("capability_receipt", None)
            config["transport"] = args.transport
            transport_mode(config)
            config["tool_version"] = __version__
        if args.rest_auth:
            config["rest_auth"] = args.rest_auth
            config.pop("capability_receipt", None)
        rest_auth_mode(config)
        if args.rules:
            config["rules"] = normalize_rules(json.loads(args.rules.read_text(encoding="utf-8")))
        if args.local:
            if args.config.exists():
                # Existing configuration is preserved unless specific fields were explicitly requested.
                if args.business_parent or args.approval_parent or args.rules or args.governance_mode or args.network_mode or args.transport or args.rest_auth:
                    atomic_json(args.config, config)
                return {"config": str(args.config.resolve()), "status": "updated" if
                        args.business_parent or args.approval_parent or args.rules or args.governance_mode or args.network_mode or args.transport or args.rest_auth
                        else "existing_config_preserved"}
            atomic_json(args.config, config, exclusive=True)
            return {"config": str(args.config.resolve()), "status": "created", "network": False}
        if args.business_parent or args.approval_parent or args.rules or args.governance_mode or args.network_mode or args.transport or args.rest_auth:
            atomic_json(args.config, config)
        if config.get("remote_profile"):
            raise GateError("Already connected to a shared library; do not provision another set of databases")
        return provision(config, args.config, FlowUsStore(config).writer)
    config = load_config(args.config)
    if args.command == "doctor":
        if bool(args.probe_block) != bool(args.expected_sha256):
            raise ManagerError("--probe-block and --expected-sha256 must be supplied together")
        if args.probe_block and (args.offline or args.verify_writes):
            raise ManagerError("Attachment preflight cannot be combined with --offline or --verify-writes")
    if args.command == "doctor" and args.offline:
        if args.verify_writes:
            raise ManagerError("--offline and --verify-writes are mutually exclusive")
        return {"config_valid": True, "network": False, "writes_enabled": False,
                "network_mode": network_mode(config),
                "transport": transport_mode(config),
                "governance_mode": governance_mode(config),
                "missing_environment": ([] if transport_mode(config) == "mcp_relay" or rest_auth_mode(config) == "flowus_cli" else
                                        [key for key in credential_names(config) if not credential_value(key)])}
    # A migration preview reads only the local vault, without requiring any cloud credentials.
    if args.command == "migrate" and args.dry_run:
        return migrate(None, args.vault, dry_run=True)
    store = FlowUsStore(config)
    from .profiles import pull, push
    if config.get("pending_profile_publish") and not (args.command == "config" and args.action == "push"):
        raise GateError("Restored rules await config push; preserve them before running another cloud task")
    if config.get("remote_profile") and args.command != "config":
        # One validated snapshot per command. Never fall back to stale rules on network failure.
        pull(config, None if getattr(args, "dry_run", False) else args.config, store.writer)
    manager = Manager(store, config)
    if args.command == "config":
        return (push(manager, args.config, dry_run=args.dry_run) if args.action == "push" else
                pull(config, args.config, store.writer, dry_run=args.dry_run))
    if args.command == "layout":
        from .layout import organize
        return organize(manager, args.config, backup_dir=args.backup_dir, dry_run=args.dry_run)
    if args.command == "refresh":
        return refresh(manager, dry_run=args.dry_run)
    if args.command == "doctor":
        if args.probe_block:
            return download_preflight(store, config, args.probe_block, args.expected_sha256)
        if args.verify_writes:
            config.pop("capability_receipt", None)
            atomic_json(args.config, config)
        try:
            result = doctor(store, config, verify_writes=args.verify_writes)
        except ManagerError as error:
            if args.verify_writes and "last_capability_report" in config:
                report = config["last_capability_report"]
                report.update(status="blocked", **error_details(error))
                stage = report.get("stage")
                if stage:
                    report["diagnostics"][stage] = {"status": "failed", **error_details(error)}
                return {**report, "writes_enabled": False}
            raise
        finally:
            if args.verify_writes:
                atomic_json(args.config, config)
        return result
    if args.command == "ingest":
        if args.cloud_inbox:
            if args.paths:
                raise ManagerError("Choose local paths or --cloud-inbox, not both")
            result = inbox(manager, dry_run=args.dry_run)
            return result if args.dry_run else after_write(manager, result)
        if not args.paths:
            raise ManagerError("Provide file paths or --cloud-inbox")
        paths = []
        for path in args.paths:
            if path.is_dir():
                paths.extend(p for p in path.rglob("*") if p.is_file() and not any(part.startswith(".") for part in p.relative_to(path).parts)
                             and p.name.lower() != "readme.txt")
            else:
                paths.append(path)
        results = []
        summary = {"added": 0, "duplicates": 0, "needs_review": 0, "failed": 0}
        for path in sorted(set(paths)):
            try:
                result = manager.ingest(path, dry_run=args.dry_run)
                if not args.dry_run:
                    field = {"duplicate": "duplicates", "needs_review": "needs_review", "added": "added"}[result["outcome"]]
                    summary[field] += 1
                results.append(result)
            except ManagerError as error:
                summary["failed"] += 1
                results.append({"source": str(path), "status": "failed", "error": error.code, "message": str(error)})
                if isinstance(error, GateError):
                    break
        result = {"results": results, "summary": summary, "dry_run": args.dry_run,
                  "status": "partial_failure" if summary["failed"] else "completed"}
        return result if args.dry_run or not any(summary[k] for k in ('added', 'duplicates', 'needs_review')) else after_write(manager, result)
    if args.command in ("latest", "timeline"):
        return getattr(manager, args.command)(args.query)
    if args.command == "ask":
        return manager.ask(args.question)
    if args.command == "note":
        return manager.note(args.version_key, args.text, args.operation_id, args.dry_run)
    if args.command == "propose":
        changes = json.loads(args.changes)
        if not isinstance(changes, dict):
            raise ManagerError("--changes must be a JSON object")
        return manager.propose(args.action, args.target, changes, dry_run=args.dry_run)
    if args.command == "apply-confirmed":
        if args.confirmation.stat().st_size > 65536:
            raise ManagerError("Confirmation evidence is too large")
        confirmation = json.loads(args.confirmation.read_text(encoding="utf-8"))
        result = manager.apply_confirmed(args.proposal_key, confirmation, dry_run=args.dry_run)
        return result if args.dry_run else after_write(manager, result)
    if args.command == "apply-approved":
        if args.proposal_key:
            return manager.apply_approved(args.proposal_key, dry_run=args.dry_run)
        results = []
        for proposal in store.list("proposals"):
            if proposal.data.get("status") != "pending":
                continue
            try:
                results.append(manager.apply_approved(proposal.key, dry_run=args.dry_run))
            except ManagerError as exc:
                results.append({"proposal_key": proposal.key, "status": "not_applied", "error": str(exc)})
        return results
    if args.command == "migrate":
        result = migrate(manager, args.vault, args.backup, dry_run=args.dry_run)
        return result if args.dry_run else after_write(manager, result)
    if args.command == "backup":
        return cloud_backup(manager, args.output, dry_run=args.dry_run)
    if args.command == "restore":
        result = cloud_restore(manager, args.backup, dry_run=args.dry_run)
        if not args.dry_run:
            atomic_json(args.config, config)
            if config.get("pending_profile_publish"):
                try:
                    result["shared_configuration"] = push(manager, args.config)
                except ManagerError as error:
                    result["shared_configuration"] = {"status": "needs_publish", "error": error.code,
                        "next": "Files are restored; preserve local rules and retry config push"}
        return result if args.dry_run else after_write(manager, result)


def main(argv=None):
    args = parser().parse_args(argv)
    def emit(payload, *, error=False):
        if args.result_file:
            atomic_json(args.result_file, payload)
            payload = {"ok": payload["ok"], "result_file": str(args.result_file.resolve())}
        print(json.dumps(payload, ensure_ascii=False, indent=2), file=sys.stderr if error else sys.stdout)
    try:
        offline = (args.command == "init" and args.local) or (args.command == "doctor" and args.offline) or (args.command == "migrate" and args.dry_run)
        if args.prompt_credentials and not offline:
            import getpass
            config = (config_template() if args.command == "connect" and not args.config.exists() else load_config(args.config))
            if args.command == "connect":
                config["transport"] = args.transport
            if args.command == "init" and args.governance_mode:
                config["governance_mode"] = args.governance_mode
            if args.command == "init" and args.transport:
                config["transport"] = args.transport
            if args.command in {"connect", "init"} and args.rest_auth:
                config["rest_auth"] = args.rest_auth
            keys = () if transport_mode(config) == "mcp_relay" or rest_auth_mode(config) == "flowus_cli" else credential_names(config, provision=args.command == "init")
            for key in keys:
                if not credential_value(key):
                    os.environ[key] = getpass.getpass(key + " (hidden, not saved): ")
        result = run(args)
        success = not (isinstance(result, dict) and result.get("status") in ("partial_failure", "blocked", "failed"))
        emit({"ok": success, "result": result})
        return 0 if success else 1
    except (ManagerError, OSError, ValueError, KeyError) as exc:
        # Never print request bodies, HTTP headers, environment values or stack traces.
        message = str(exc) if isinstance(exc, ManagerError) else f"Invalid input/configuration or local I/O ({type(exc).__name__})"
        try:
            emit({"ok": False, "error": getattr(exc, "code", "invalid_input"), "message": message}, error=True)
        except OSError:
            print(json.dumps({"ok": False, "error": "invalid_input", "message": "Cannot save private result file"}), file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
