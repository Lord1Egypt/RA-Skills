#!/usr/bin/env python3
"""Read an explicitly supplied semantic ZIP/directory; no project or network access."""
import argparse
import json
import os
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from workbench.semantic_package import PackageError, read_package


class Parser(argparse.ArgumentParser):
    def error(self, message):
        raise PackageError("INVALID_INPUT", message)


def make_parser():
    p = Parser(description=__doc__)
    p.add_argument("--package", required=True, help="Explicit ZIP file or extracted package directory")
    p.add_argument("--full-scope", action="store_true", help="Include full package-wide ID lists and verify issues even for large models; place before the command")
    commands = p.add_subparsers(dest="command", required=True, parser_class=Parser)
    commands.add_parser("verify", help="Verify bytes, references, states and evidence, not business truth")
    commands.add_parser("describe", help="Discover read-only tools and execution boundaries")
    brief = commands.add_parser("brief", help="Question package: context, blockers and evidence pointers in one read; no execution")
    brief.add_argument("--limit", type=int, default=50)
    brief.add_argument("--offset", type=int, default=0)
    brief.add_argument("--expected-snapshot", help="Caller reference only; no freshness authority")
    control = commands.add_parser("control", help="Read the snapshot-bound query control; never generate SQL or authorize execution")
    control.add_argument("--scenario", dest="scenario_id")
    control.add_argument("--expected-snapshot", help="Caller-supplied reference detects mismatch; not an authority or freshness proof")
    task = commands.add_parser("task", help="Read the question explicitly included in this snapshot; never execute it")
    task.add_argument("--detail", choices=["summary", "full"], default="summary")
    task.add_argument("--limit", type=int, default=50)
    task.add_argument("--offset", type=int, default=0)
    resolve = commands.add_parser("resolve", help="Find question-related candidates, or read context for explicitly selected IDs; never answer or execute")
    resolve.add_argument("--question", required=True)
    resolve.add_argument("--id", action="append", dest="ids")
    resolve.add_argument("--intent", choices=["explain", "calculate", "query", "act"], default="explain")
    resolve.add_argument("--domain")
    resolve.add_argument("--scope", help="Exact scope string, or a JSON object subset; not authorization")
    resolve.add_argument("--as-of")
    resolve.add_argument("--limit", type=int, default=50)
    resolve.add_argument("--offset", type=int, default=0)
    resolve.add_argument("--detail", choices=["summary", "full"], default="full")
    context = commands.add_parser("context", help="Read required definitions, scopes, dependencies, evidence and gaps together")
    context.add_argument("--id", required=True, action="append", dest="ids")
    context.add_argument("--intent", choices=["explain", "calculate", "query", "act"], default="explain")
    context.add_argument("--as-of")
    context.add_argument("--limit", type=int, default=100)
    context.add_argument("--offset", type=int, default=0)
    context.add_argument("--detail", choices=["summary", "full"], default="full")
    search = commands.add_parser("search", help="Find definitions; multiple matches remain ambiguous")
    search.add_argument("--query", required=True)
    search.add_argument("--domain")
    search.add_argument("--kind")
    search.add_argument("--scope", help="Exact scope string, or a JSON object subset")
    search.add_argument("--as-of", help="Business date YYYY-MM-DD; absence never means today")
    search.add_argument("--limit", type=int, default=50)
    search.add_argument("--offset", type=int, default=0)
    get = commands.add_parser("get", help="Read by stable ID, following explicit merge redirects")
    get.add_argument("--id", required=True)
    get.add_argument("--as-of")
    sources = commands.add_parser("sources", help="Read exact evidence excerpts and locations")
    sources.add_argument("--id", required=True, action="append", dest="ids")
    sources.add_argument("--limit", type=int, default=100)
    sources.add_argument("--offset", type=int, default=0)
    neighbors = commands.add_parser("neighbors", help="Traverse declared edges without inventing reverse facts")
    neighbors.add_argument("--id", required=True)
    neighbors.add_argument("--direction", choices=["in", "out", "both"], default="both")
    neighbors.add_argument("--depth", type=int, default=1)
    neighbors.add_argument("--relation-type", action="append", default=[])
    neighbors.add_argument("--limit", type=int, default=100)
    neighbors.add_argument("--offset", type=int, default=0)
    neighbors.add_argument("--as-of")
    path = commands.add_parser("path", help="Trace one directed definition path with evidence pointers and remaining gaps")
    path.add_argument("--from-id", required=True)
    path.add_argument("--to-id", required=True)
    path.add_argument("--as-of", help="Business date YYYY-MM-DD")
    path.add_argument("--max-depth", type=int, default=12, help="Maximum hops (0–32, default 12)")
    export = commands.add_parser("export", help="Create a new dependency-closed subgraph ZIP")
    export.add_argument("--id", required=True, action="append", dest="ids")
    export.add_argument("--out", required=True)
    export.add_argument("--draft", action="store_true", default=None)
    export.add_argument("--include-execution", action="store_true", default=None)
    viewer = commands.add_parser("graph-view", help="Save an offline 3D view of a verified package")
    viewer.add_argument("--out", required=True)
    viewer.add_argument("--language", choices=["en", "zh"], default="en")
    scope = viewer.add_mutually_exclusive_group()
    scope.add_argument("--id", help="Object or relationship ID")
    scope.add_argument("--all", action="store_true", help="All active objects in this package")
    viewer.add_argument("--all-neighbors", action="store_true", help="Include every direct neighbor of --id")
    return p


def main(argv=None):
    package = None
    try:
        args = make_parser().parse_args(argv)
        package = read_package(args.package)
        package.compact_cli = not args.full_scope
        if args.command == "graph-view":
            from workbench.graph_view import projection, save_html
            data = projection(package.model["assets"], package.manifest["source_revision"], args.id, args.all,
                              all_neighbors=args.all_neighbors)
            result = {"snapshot_id": package.manifest["snapshot_id"], **save_html(data, args.out, args.language)}
        elif args.command == "verify":
            result = package.verify()
        elif args.command == "describe":
            result = package.describe()
        elif args.command == "brief":
            result = package.brief(limit=args.limit, offset=args.offset, expected_snapshot=args.expected_snapshot)
        elif args.command == "control":
            result = package.control(scenario_id=args.scenario_id, expected_snapshot=args.expected_snapshot)
        elif args.command == "task":
            result = package.task(detail=args.detail, limit=args.limit, offset=args.offset)
        elif args.command == "context":
            result = package.context(args.ids, intent=args.intent, as_of=args.as_of, limit=args.limit, offset=args.offset, detail=args.detail)
        elif args.command in {"search", "resolve"}:
            scope = args.scope
            if scope and scope.lstrip().startswith("{"):
                try:
                    scope = json.loads(scope)
                except ValueError as exc:
                    raise PackageError("INVALID_INPUT", "--scope 不是有效 JSON 对象") from exc
            if args.command == "resolve":
                result = package.resolve(args.question, asset_ids=args.ids, intent=args.intent, domain=args.domain,
                                         scope=scope, as_of=args.as_of, limit=args.limit, offset=args.offset, detail=args.detail)
            else:
                result = package.search(args.query, domain=args.domain, kind=args.kind, scope=scope,
                                        as_of=args.as_of, limit=args.limit, offset=args.offset)
        elif args.command == "get":
            result = package.get(args.id, as_of=args.as_of)
        elif args.command == "sources":
            result = package.sources(args.ids, limit=args.limit, offset=args.offset)
        elif args.command == "neighbors":
            result = package.neighbors(args.id, direction=args.direction, depth=args.depth,
                                       relation_types=args.relation_type, limit=args.limit, offset=args.offset,
                                       as_of=args.as_of)
        elif args.command == "path":
            result = package.path(args.from_id, args.to_id, as_of=args.as_of, max_depth=args.max_depth)
        elif args.command == "export":
            output = Path(args.out)
            if output.exists():
                raise PackageError("OUTPUT_EXISTS", "输出文件已存在；固定快照不覆盖，请选择新文件", path=str(output))
            if not output.parent.is_dir():
                raise PackageError("OUTPUT_DIRECTORY_MISSING", "输出目录不存在，请先创建目录", path=str(output.parent))
            content, manifest = package.export(args.ids, draft=args.draft, include_execution=args.include_execution)
            created_by_call = False
            try:
                with output.open("xb") as stream:
                    created_by_call = True
                    stream.write(content)
                    stream.flush()
                    os.fsync(stream.fileno())
            except FileExistsError as exc:
                raise PackageError("OUTPUT_EXISTS", "输出文件已存在；没有覆盖", path=str(output)) from exc
            except OSError:
                # This call exclusively created the file; a failed partial artifact is not a publication.
                if created_by_call:
                    try:
                        output.unlink()
                    except OSError:
                        pass
                raise
            result = {"status": "exported", "snapshot_id": manifest["snapshot_id"],
                      "parent_snapshot_id": package.manifest["snapshot_id"], "scope": manifest["scope"],
                      "complete": manifest["complete"], "draft": manifest["draft"], "output": str(output.resolve()),
                      "is_latest": "unknown_offline"}
        print(json.dumps(result, ensure_ascii=False, allow_nan=False))
        return 0
    except (PackageError, OSError, ValueError) as exc:
        error = exc.as_dict() if isinstance(exc, PackageError) else {"code": "IO_ERROR" if isinstance(exc, OSError) else "INVALID_INPUT", "message": str(exc)}
        result = {"status": "error", "complete": False, "error": error}
        if package is not None:
            result.update(snapshot_id=package.manifest["snapshot_id"], scope=package.reader_scope())
        print(json.dumps(result, ensure_ascii=False, allow_nan=False))
        return 2


if __name__ == "__main__":
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    raise SystemExit(main())
