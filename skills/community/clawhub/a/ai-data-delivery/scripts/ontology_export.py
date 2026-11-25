#!/usr/bin/env python3
"""Export a verified semantic snapshot to OGS 1.1, or audit a real round trip."""
import argparse
import json
import os
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from workbench.ogs_export import audit_roundtrip, export_ogs
from workbench.semantic_package import MAX_PACKAGE_BYTES, PackageError


class Parser(argparse.ArgumentParser):
    def error(self, message):
        raise PackageError("INVALID_INPUT", message)


def _read(path):
    path = Path(path)
    if path.stat().st_size > MAX_PACKAGE_BYTES:
        raise PackageError("INPUT_TOO_LARGE", "OGS input exceeds 64 MiB")
    def unique(pairs):
        out = {}
        for key, value in pairs:
            if key in out:
                raise ValueError("Duplicate JSON key: " + key)
            out[key] = value
        return out
    return json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=unique,
                      parse_constant=lambda x: (_ for _ in ()).throw(ValueError(x)))


def _write_pair(outputs):
    paths = [Path(path) for path, _ in outputs]
    if len({str(path.resolve()).casefold() for path in paths}) != len(paths):
        raise PackageError("INVALID_INPUT", "Model and report must use different paths")
    for path in paths:
        if path.exists():
            raise PackageError("OUTPUT_EXISTS", "Output already exists; select a new path", path=str(path))
        if not path.parent.is_dir():
            raise PackageError("OUTPUT_DIRECTORY_MISSING", "Output parent does not exist", path=str(path.parent))
    created = []
    try:
        for path, (_, value) in zip(paths, outputs):
            with path.open("x", encoding="utf-8", newline="\n") as stream:
                created.append(path)
                json.dump(value, stream, ensure_ascii=False, indent=2, allow_nan=False)
                stream.write("\n")
                stream.flush()
                os.fsync(stream.fileno())
    except (OSError, ValueError):
        for path in created:
            try:
                path.unlink()
            except OSError:
                pass
        raise


def main(argv=None):
    try:
        parser = Parser(description=__doc__)
        parser.add_argument("--package", help="Explicit semantic ZIP/directory for export")
        sub = parser.add_subparsers(dest="command", required=True, parser_class=Parser)
        export = sub.add_parser("export", help="Generate a new-design projection plus coverage report; no database writes")
        export.add_argument("--out", required=True)
        export.add_argument("--report", required=True)
        audit = sub.add_parser("audit", help="Compare original export with an actual converted OGS JSON")
        audit.add_argument("--original", required=True)
        audit.add_argument("--returned", required=True)
        args = parser.parse_args(argv)
        if args.command == "export":
            if not args.package:
                raise PackageError("INVALID_INPUT", "export requires --package")
            model, result = export_ogs(args.package)
            _write_pair([(args.out, model), (args.report, result)])
            result = {"status": result["status"], "snapshot_id": result["snapshot_id"],
                      "native_nodes": result["native_nodes"], "native_relationships": result["native_relationships"],
                      "out": str(Path(args.out).resolve()), "report": str(Path(args.report).resolve()),
                      "database_import_ready": False}
        else:
            if args.package:
                raise PackageError("INVALID_INPUT", "audit takes --original/--returned, not --package")
            result = audit_roundtrip(_read(args.original), _read(args.returned))
        print(json.dumps(result, ensure_ascii=False, allow_nan=False))
        return 1 if result.get("status") == "changed_or_lost" else 0
    except (PackageError, OSError, ValueError, RecursionError) as exc:
        error = exc.as_dict() if isinstance(exc, PackageError) else {"code": "INVALID_INPUT", "message": str(exc)}
        print(json.dumps({"status": "error", "error": error}, ensure_ascii=False))
        return 2


if __name__ == "__main__":
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    raise SystemExit(main())
