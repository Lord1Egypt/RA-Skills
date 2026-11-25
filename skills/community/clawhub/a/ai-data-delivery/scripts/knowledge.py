#!/usr/bin/env python3
"""Local CLI: import structure, edit semantics, export a portable package.

Read a prepared task and propose against its source revision. Review/edit commands
record explicit operator decisions through the same guards as the workbench.
No LLM or automatic confirmation. Metadata commands use the configured catalog.
"""
import argparse
import base64
import json
import os
from pathlib import Path
import sys
import uuid
from urllib.parse import urlencode

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from workbench.store import Store, Conflict
from workbench.knowledge import KnowledgeService
from workbench.semantic_package import PackageError, bounded_warnings, scope_summary


class JsonArgumentParser(argparse.ArgumentParser):
    def error(self, message):
        print(json.dumps({"ok": False, "status": "argument_error", "error": message,
                          "hint": "Use COMMAND --help / 使用子命令 --help 查看参数"}, ensure_ascii=False))
        raise SystemExit(2)


def main(argv=None):
    parser = JsonArgumentParser(description=__doc__)
    parser.add_argument("--project", required=True)
    parser.add_argument("--full-output", action="store_true", help="Return the full import/export receipt including all asset IDs, issues and parser warnings; place before command")
    parser.add_argument("--revision", type=int)
    parser.add_argument("--progress", action="store_true", help="Emit stage events as JSON lines on stderr; stdout remains one JSON receipt")
    parser.add_argument("--language", choices=['en', 'zh'], default='en')
    parser.add_argument("--operation-id", help="Reuse this ID with identical input after an uncertain result")
    commands = parser.add_subparsers(dest="command", required=True)
    state = commands.add_parser("state", help="Read the current project and material/candidate status")
    state.add_argument("--summary", action="store_true", help="Compact identities, revisions and pending work")
    inspect = commands.add_parser("inspect", help="Inspect model dependency closure and authoring gaps; read only")
    inspect.add_argument("--id", action="append", dest="asset_ids")
    hints = commands.add_parser("relation-hints", help="Find relationship leads from current physical metadata; read only")
    hints.add_argument("--id", help="Show leads touching this dataset asset ID")
    hints.add_argument("--limit", type=int, default=20)
    hints.add_argument("--offset", type=int, default=0)
    connection = commands.add_parser("connect", help="Register a metadata-only connection; credentials use environment variable names")
    connection.add_argument("--file", required=True, help="Connection profile JSON, never a password or SQL")
    for command in ("scan", "regress"):
        item = commands.add_parser(command, help="Read selected catalog / check affected question contracts")
        item.add_argument("--connection", required=True)
        if command == "scan":
            item.add_argument("--seed-draft", action="store_true", help="Initialize an empty graph with physical drafts; never confirm business meaning")
            item.add_argument("--refresh-review", action="store_true", help="Explicitly regenerate unresolved candidates against current graph and a fresh catalog observation")
    if (Path(__file__).resolve().parents[1] / "workbench/semantic_demo.py").is_file():
        commands.add_parser("example", help="Prepare the source repository equipment exercise")
    scenario = commands.add_parser("scenario", help="Save a business question and selected knowledge, never confirm it")
    scenario.add_argument("--file", required=True, help="JSON scenario object; omit ID for a new question")
    check = commands.add_parser("check", help="Read current scenario context and gaps; no query, publication or answer validation")
    check.add_argument("--scenario", required=True)
    check.add_argument("--limit", type=int, default=50)
    check.add_argument("--offset", type=int, default=0)
    assess = commands.add_parser("assess", help="Record a local operator observation, evidence and checked fingerprint")
    assess.add_argument("--file", required=True, help="JSON with scenario_id, case_id, basis_fingerprint, outcome, observed, evidence, actor")
    impact = commands.add_parser("impact", help="Read registered source/definition changes and affected question paths")
    impact.add_argument("--scenario")
    handoff = commands.add_parser("handoff", help="Explicitly export a saved question with its dependency-closed semantic snapshot")
    handoff.add_argument("--scenario", required=True)
    handoff.add_argument("--out", required=True)
    handoff.add_argument("--draft", action="store_true")
    export = commands.add_parser("export", help="Export the model without a question or a running server")
    export.add_argument("--out", required=True)
    export.add_argument("--id", action="append", dest="asset_ids", help="Optional selected asset ID; repeat for multiple assets. Default: all active model assets")
    export.add_argument("--draft", action="store_true", help="Preserve draft status and unresolved gaps")
    export.add_argument("--include-execution", action="store_true", help="Also include existing execution declarations; does not authorize execution")
    material = commands.add_parser("import", help="Register material without overwriting the graph")
    material.add_argument("--file", required=True)
    material.add_argument("--encoding", choices=("utf-8-sig", "utf-16", "gb18030"), help="Text input encoding. Default: UTF-8 or UTF-16 BOM. Choose gb18030 for GBK exports.")
    material.add_argument("--domain", default="")
    material.add_argument("--scope", default="")
    material.add_argument("--effective-from", help="Declared start date for this source revision (YYYY-MM-DD)")
    material.add_argument("--effective-to", help="Declared end date for this source revision (YYYY-MM-DD)")
    material.add_argument("--source-id")
    material.add_argument("--source-key", help="Stable logical DDL source (e.g. fleet/prod). Reuse across schema versions or fresh projects.")
    material.add_argument("--distinct-source", action="store_true")
    material.add_argument("--seed-draft", action="store_true", help="DDL only: initialize an empty graph with editable physical drafts")
    task = commands.add_parser("task", help="Read material fragments and current graph for the selected host task")
    task.add_argument("--batch", required=True)
    task_scope = task.add_mutually_exclusive_group()
    task_scope.add_argument("--scenario", help="Optional saved business question guiding this material task")
    task_scope.add_argument("--id", action="append", dest="asset_ids", help="Select this asset and its required dependencies; repeat for several roots")
    task_scope.add_argument("--question", help="Find candidate identities for a question without saving it; select with --id")
    task_scope.add_argument("--all-assets", action="store_true", help="Explicitly include the entire project graph")
    task.add_argument("--limit", type=int, default=12, help="Candidate identities per page (1–100)")
    task.add_argument("--offset", type=int, default=0, help="First identity on the candidate page")
    task.add_argument("--compare-source", action="append", default=[], help="Include another material from this project for comparison (repeat its source ID)")
    task.add_argument("--action", choices=["prepare", "cancel", "resume"], default="prepare")
    proposal = commands.add_parser("propose", help="Submit evidence-linked candidate groups, never confirm them")
    proposal.add_argument("--batch", required=True)
    proposal.add_argument("--file", required=True)
    proposal.add_argument("--partial", action="store_true")
    review = commands.add_parser("review", help="Record an explicitly authorized operator decision; never auto-accept proposals")
    review.add_argument("--group", required=True)
    review.add_argument("--action", required=True, choices=["accept", "reject", "defer"])
    review.add_argument("--reason", required=True)
    review.add_argument("--assets", help="Optional JSON array of revised assets within this group")
    edit = commands.add_parser("edit", help="Maintain an asset through normal graph guards; draft unless explicitly confirmed")
    edit.add_argument("--file", required=True, help="Complete semantic asset object or atomic array; same-batch dependencies allowed")
    edit.add_argument("--confirm", action="store_true", help="Only when the operator has authorized confirmation")
    edit.add_argument("--expect-grain", help="Check one metric against an independently supplied counting grain before saving")
    retire = commands.add_parser("retire", help="Retire selected assets together and retain their identities and history. Requires --revision before retire.")
    targets = retire.add_mutually_exclusive_group(required=True)
    targets.add_argument("--id", action="append", dest="asset_ids", help="Asset to retire; repeat for a batch")
    targets.add_argument("--file", help="UTF-8 JSON array of asset IDs to retire atomically")
    retire.add_argument("--reason", required=True)
    separate = commands.add_parser("separate", help="Record why two same-name assets must keep distinct identities. Requires --revision before separate.")
    separate.add_argument("--left", required=True)
    separate.add_argument("--right", required=True)
    separate.add_argument("--reason", required=True)
    receipt = commands.add_parser("receipt", help="Read the durable result of an earlier operation")
    receipt.add_argument("id")
    picture = commands.add_parser("graph-image", help="Save a focused, read-only SVG of a project revision; no browser required")
    picture.add_argument("--id", help="Active asset to focus, including a relationship")
    picture.add_argument("--out", required=True, help="New local .svg file")
    viewer = commands.add_parser("graph-view", help="Save an offline 3D view of the changed objects and neighbors")
    viewer.add_argument("--out", required=True, help="New .html file")
    scope = viewer.add_mutually_exclusive_group()
    scope.add_argument("--id", help="Focus on this object or relationship")
    scope.add_argument("--all", action="store_true", help="Include the full active graph")
    viewer.add_argument("--all-neighbors", action="store_true", help="Include every direct neighbor of --id")
    args = parser.parse_args(argv)
    if args.command in {"state", "inspect", "relation-hints", "check", "impact", "receipt", "export", "handoff", "retire", "separate", "graph-image", "graph-view"} and not (Path(args.project) / "project.sqlite").is_file():
        print(json.dumps({"ok": False, "status": "project_not_found", "error": "No project.sqlite here; check --project or import a schema first / 未找到项目，请核对路径或先导入结构"}, ensure_ascii=False))
        return 2
    store = Store(args.project)
    def report(stage, **data):
        print(json.dumps({"stage": stage, **data}, ensure_ascii=False), file=sys.stderr, flush=True)
    service = KnowledgeService(store, progress=report if args.progress else None)
    operation_id = args.operation_id or uuid.uuid4().hex
    req = {"revision": store.read()["revision"] if args.revision is None else args.revision, "operation_id": operation_id}
    try:
        if args.progress:
            report("started", command=args.command)
        if args.command == "state":
            result = service.state()
            if args.summary:
                result = {"revision": result["revision"], "project_id": result["project_id"],
                          "assets": [{k: a.get(k) for k in ("id", "name", "kind", "status")} for a in result["assets"]],
                          "sources": [{"id": a["id"], "name": a.get("name"), "current_revision": a.get("current_revision"),
                                       "revisions": [r["revision"] for r in a.get("revisions", [])]} for a in result["sources"]],
                          "pending_groups": [{k: a.get(k) for k in ("id", "batch_id", "status")} for a in result["groups"] if a.get("status") not in {"accepted", "rejected"}],
                          "batches": [{k: a.get(k) for k in ("id", "sources", "status")} for a in result["batches"]]}
        elif args.command == "inspect":
            from workbench.authoring_inspect import inspect_model
            current = service.state()
            result = {"revision": current["revision"], **inspect_model(current["assets"], current["sources"], asset_ids=args.asset_ids)}
        elif args.command == "relation-hints":
            from workbench.knowledge import containers
            from workbench.relation_hints import relation_hints
            current = store.read(args.revision)
            semantic, knowledge = containers(current["document"])
            result = {"revision": current["revision"], **relation_hints(
                semantic["assets"], knowledge["sources"], args.id, args.limit, args.offset)}
            result["editor_argv_prefix"] = [sys.executable, str(Path(__file__).with_name("start.py")),
                                           "--project", str(Path(args.project).resolve()), "--language", args.language]
            result["editor_focus_argument"] = "--focus"
        elif args.command == "connect":
            result = service.metadata_connect({**req, "connection": json.loads(Path(args.file).read_text(encoding="utf-8-sig"))})
        elif args.command in {"scan", "regress"}:
            result = getattr(service, "metadata_" + args.command)({**req, "connection_id": args.connection,
                **({"refresh_review": args.refresh_review, "seed_draft": args.seed_draft} if args.command == "scan" else {})})
        elif args.command == "graph-view":
            from workbench.graph_view import project_view, save_html
            data = project_view(store.read(args.revision), args.id, args.all, all_neighbors=args.all_neighbors)
            result = save_html(data, args.out, args.language)
        elif args.command == "graph-image":
            from workbench.graph_image import render_graph
            path = Path(args.out)
            if path.suffix.lower() != ".svg":
                raise ValueError("Choose a .svg output file / 请选择 .svg 图像文件")
            svg, result = render_graph(store.read(args.revision), args.id, args.language)
            created = False
            try:
                with path.open("x", encoding="utf-8", newline="\n") as stream:
                    created = True
                    stream.write(svg)
            except OSError:
                if created:
                    path.unlink(missing_ok=True)
                raise
            result["output"] = str(path.resolve())
        elif args.command == "receipt":
            stored = store.operation(args.id)
            result = {"target_operation_id": args.id, "found": stored is not None, "receipt": stored}
        elif args.command == "impact":
            result = service.impact({"scenario_id": args.scenario})
        elif args.command == "assess":
            data = json.loads(Path(args.file).read_text(encoding="utf-8-sig"))
            result = service.scenario_assess({**data, **req})
        elif args.command in {"handoff", "export"}:
            path = Path(args.out)
            if path.exists() or not path.parent.is_dir():
                raise ValueError("Choose a new output file in an existing directory / 请在已有目录中指定新文件")
            if args.command == "handoff":
                scope = {"scenario_id": args.scenario}
            else:
                selected = args.asset_ids if args.asset_ids is not None else [a["id"] for a in service.state()["assets"] if a["status"] != "retired"]
                if not selected:
                    raise ValueError("No model assets to export / 当前没有可导出的模型资产")
                scope = {"asset_ids": selected, "include_execution": args.include_execution}
            result = service.publish({**req, **scope, "draft": args.draft})
            created = False
            try:
                with path.open("xb") as stream:
                    created = True
                    stream.write(service.download(result["result"]["snapshot_id"]))
                    stream.flush()
                    os.fsync(stream.fileno())
            except OSError:
                if created:
                    path.unlink(missing_ok=True)
                raise
            result["output"] = str(path.resolve())
            manifest = result["result"]["manifest"]
            if not args.full_output and len(manifest["scope"].get("included_ids", [])) > 100:
                from collections import Counter
                result["result"]["manifest"] = {**{k:v for k,v in manifest.items() if k not in ("scope", "issues")},
                    "scope": scope_summary(manifest["scope"]), "issue_count": len(manifest["issues"]),
                    "issue_counts": dict(Counter(i["code"] for i in manifest["issues"])),
                    "full_receipt_option": "--full-output"}
        elif args.command == "import":
            path = Path(args.file)
            result = service.import_material({**req, "filename": path.name, "content_base64": base64.b64encode(path.read_bytes()).decode(),
                "domain": args.domain, "scope": args.scope, "language": args.language, "source_id": args.source_id, "distinct_source": args.distinct_source,
                **({"options": {"encoding": args.encoding}} if args.encoding else {}),
                **{key: getattr(args, key) for key in ("effective_from", "effective_to") if getattr(args, key) is not None},
                **({"source_key": args.source_key} if args.source_key is not None else {}),
                "seed_draft": args.seed_draft})
        elif args.command == "task":
            result = service.task({**req, "batch_id": args.batch, "action": args.action, 'language': args.language,
                                   **({"compare_source_ids": args.compare_source} if args.compare_source else {}),
                                   **({"asset_ids": args.asset_ids} if args.asset_ids else {}),
                                   **({"question": args.question} if args.question is not None else {}),
                                   **({"all_assets": True} if args.all_assets else {}),
                                   **({"limit": args.limit} if args.limit != 12 else {}),
                                   **({"offset": args.offset} if args.offset else {}),
                                   "scenario_id": args.scenario})
        elif args.command == "scenario":
            result = service.scenario({**req, "scenario": json.loads(Path(args.file).read_text(encoding="utf-8-sig"))})
        elif args.command == "check":
            result = service.scenario_check({"revision": req["revision"], "scenario_id": args.scenario,
                                             "limit": args.limit, "offset": args.offset})
        elif args.command == "example":
            result = service.example(req)
        elif args.command == "review":
            assets = json.loads(Path(args.assets).read_text(encoding="utf-8-sig")) if args.assets else []
            if not isinstance(assets, list):
                raise ValueError("Revised assets must be a JSON array / 修订资产须为 JSON 数组")
            if not args.reason.strip():
                raise ValueError("Describe the operator decision / 请填写操作者的核对理由")
            result = service.review({**req, "group_id": args.group, "action": args.action, "reason": args.reason, "assets": assets})
        elif args.command == "separate":
            if args.revision is None:
                raise Conflict("Pass the revision you reviewed / 请提供核对时的修订号")
            result = service.separate({**req, "left_id": args.left, "right_id": args.right, "reason": args.reason.strip()})
        elif args.command == "retire":
            if args.revision is None:
                raise Conflict("Use --revision from the state you reviewed before retire / 停用前请提供核对时的项目修订号")
            ids = json.loads(Path(args.file).read_text(encoding="utf-8-sig")) if args.file else args.asset_ids
            result = service.retire({**req, "asset_ids": ids, "reason": args.reason})
        elif args.command == "edit":
            result = service.edit({**req, **({"create_only": True} if args.revision is None else {}),
                                   **({"expected_grain": args.expect_grain} if args.expect_grain is not None else {}),
                                   "asset": json.loads(Path(args.file).read_text(encoding="utf-8-sig")), "confirm": args.confirm})
        else:
            data = json.loads(Path(args.file).read_text(encoding="utf-8-sig"))
            groups = data if isinstance(data, list) else data.get("groups")
            result = service.propose({**req, "batch_id": args.batch, "groups": groups, "complete": not args.partial})
        if args.command in {"import", "scan"} and args.seed_draft:
            detail = result["result"]
            result = {"revision": result["revision"], "result": {
                **{k: detail[k] for k in ("source_id", "batch_id", "seeded", "status", "guidance") if k in detail},
                **bounded_warnings(detail.get("parsed", {}).get("warnings", []), full=args.full_output),
                "optional_editor_argv": [sys.executable, str(Path(__file__).with_name("start.py")), "--project", str(Path(args.project).resolve()), "--language", args.language]}}
            receipt = result["result"]
            seeded = receipt.get("seeded") or {}
            counts = seeded.get("counts", {})
            if counts.get("dataset") and counts.get("relation", 0) * 4 <= counts["dataset"]:
                receipt["optional_relation_hints_argv"] = [
                    sys.executable, str(Path(__file__).resolve()), "--project", str(Path(args.project).resolve()),
                    "--language", args.language, "relation-hints"]
            if not args.full_output and len(seeded.get("asset_ids", [])) > 100:
                receipt["seeded"] = {**{k:v for k,v in seeded.items() if k!="asset_ids"},
                                    "asset_id_count": len(seeded["asset_ids"]), "ids_omitted": True}
            if receipt.get("warnings_truncated") or (receipt.get("seeded") or {}).get("ids_omitted"):
                receipt["full_receipt_hint"] = "state for stored source details and asset IDs; --full-output before a command for verbose output"
        detail = result.get("result") if isinstance(result, dict) else None
        guidance = detail.get("guidance") if isinstance(detail, dict) else None
        if guidance and (guidance["changed_count"] or guidance["next_action"] != "none"):
            # The first write can share the event's guidance object; persisted replays do not.
            # Keep launch arguments in the response, outside the stored event.
            guidance = detail["guidance"] = dict(guidance)
            args_open = [sys.executable, str(Path(__file__).with_name("start.py")), "--project", str(Path(args.project).resolve()), "--language", args.language]
            focus = guidance["focus_id"]
            page = {"review_candidates": "review", "interpret_material": "knowledge", "repair_material": "knowledge"}.get(guidance["next_action"], "graph")
            if focus:
                args_open += ["--focus", focus]
            if page != "graph":
                args_open += ["--page", page]
            guidance["preview"] = {"revision": result["revision"], "launch_argv": args_open,
                                   "location": "/?" + urlencode({"lang": args.language, **({"focus": focus} if focus else {})}) + "#" + page}
            if guidance["changed_count"]:
                guidance["preview"]["graph_view_location"] = "/?" + urlencode({
                    "view": "3d", "lang": args.language, "revision": result["revision"]})
                guidance["preview"]["graph_view_argv_prefix"] = [
                    sys.executable, str(Path(__file__).resolve()), "--project", str(Path(args.project).resolve()),
                    "--revision", str(result["revision"]), "--language", args.language, "graph-view"]
                guidance["preview"]["graph_view_output_argument"] = "--out"
            if page == "graph" and guidance["changed_count"] and guidance["next_action"] != "none":
                guidance["preview"]["image_argv_prefix"] = [
                    sys.executable, str(Path(__file__).resolve()), "--project", str(Path(args.project).resolve()),
                    "--revision", str(result["revision"]), "--language", args.language, "graph-image",
                    *(["--id", focus] if focus else [])]
                guidance["preview"]["image_output_argument"] = "--out"
        if args.progress:
            report("completed", command=args.command, revision=result.get("revision"))
        print(json.dumps({"ok": True, "operation_id": operation_id, "result": result}, ensure_ascii=False, allow_nan=False))
        return 0
    except (ValueError, OSError, TypeError) as exc:
        if args.progress:
            report("failed", command=args.command)
        print(json.dumps({"ok": False, "operation_id": operation_id, "status": "conflict" if isinstance(exc, Conflict) else "error", "error": str(exc),
                          **({"details": exc.as_dict()} if isinstance(exc, PackageError) else {})}, ensure_ascii=False))
        return 2


if __name__ == "__main__":
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    raise SystemExit(main())
