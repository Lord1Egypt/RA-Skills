#!/usr/bin/env python3
"""fcskill: run FreeCAD modelling requests from the command line.

    python3 fcskill.py run request.json        # file
    python3 fcskill.py run - < request.json    # stdin
    python3 fcskill.py run '{"steps": [...]}'  # inline JSON
    python3 fcskill.py describe [op ...]       # operation catalog (no FreeCAD needed)
    python3 fcskill.py doctor                  # check the FreeCAD installation

Prints one JSON object on stdout. Exit codes: 0 success, 1 the request
failed (see "error"), 2 environment or usage problem.

This launcher needs Python 3.12+ and only its standard library. The
modelling itself runs inside FreeCAD's own interpreter (FreeCADCmd), found
automatically or via FCSKILL_FREECAD, whatever its Python version.
"""

from __future__ import annotations

import sys

MIN_PYTHON = (3, 12)
if sys.version_info < MIN_PYTHON:  # checked before anything that could need a newer Python
    sys.stdout.write(
        '{"status": "error", "error": {"code": "PYTHON_VERSION", "message": "fcskill needs Python 3.12 or newer, '
        'this is %d.%d", "hint": "Run it with a newer python3 (e.g. python3.12); FreeCAD itself may keep its own '
        'Python."}}\n' % sys.version_info[:2]
    )
    sys.exit(2)

import argparse
import glob
import hashlib
import importlib.util
import json
import os
import shlex
import shutil
import signal
import subprocess
import tempfile
import time
import uuid
from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

from fcengine import __version__, catalog, doclock, errors, library, workspace  # noqa: E402

CMD_NAMES = ("freecadcmd", "FreeCADCmd", "freecad.cmd")
DEFAULT_TIMEOUT = 300


# ------------------------------------------------------------------ output


def _finite(obj: Any) -> Any:
    """Replace NaN/Infinity (not valid JSON) with null."""
    if isinstance(obj, float) and (obj != obj or obj in (float("inf"), float("-inf"))):
        return None
    if isinstance(obj, dict):
        return {k: _finite(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [_finite(v) for v in obj]
    return obj


def emit(resp: Dict[str, Any], pretty: bool) -> int:
    print(
        json.dumps(
            _finite(resp), indent=2 if pretty else None, separators=None if pretty else (",", ":"), allow_nan=False
        )
    )
    if resp.get("status") == "success":
        return 0
    code = (resp.get("error") or {}).get("code")
    return (
        2
        if code
        in (
            errors.FREECAD_NOT_FOUND,
            errors.FREECAD_CRASHED,
            errors.TIMEOUT,
            errors.DOCUMENT_BUSY,
            errors.FREECAD_VERSION,
            errors.LIBRARY_UNAVAILABLE,
        )
        else 1
    )


def env_error(
    code: str, message: str, hint: Optional[str] = None, details: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    return errors.error_response(errors.SkillError(code, message, hint, details), engine=__version__)


# ------------------------------------------------------------------ FreeCAD discovery


class Backend:
    def __init__(self, kind: str, cmd: Sequence[str] = (), source: str = "") -> None:
        self.kind = kind  # "python" (FreeCAD importable by this interpreter) | "subprocess" (FreeCADCmd)
        self.cmd = list(cmd)
        self.source = source

    @property
    def is_snap(self) -> bool:
        if not self.cmd:
            return False
        exe = shutil.which(self.cmd[0]) or self.cmd[0]
        return exe.startswith("/snap/") or os.path.realpath(exe).startswith("/snap/") or "/snap/bin/" in exe

    def describe(self) -> Dict[str, Any]:
        d: Dict[str, Any] = {"kind": self.kind, "source": self.source}
        if self.cmd:
            d["command"] = self.cmd
        if self.is_snap:
            d["snap"] = True
        return d


def _split(cmd: str) -> List[str]:
    return shlex.split(cmd, posix=(os.name != "nt"))


def _cmd_in_dir(d: str) -> Optional[str]:
    for sub in ("", "bin", os.path.join("..", "bin")):
        for name in CMD_NAMES:
            for ext in ("", ".exe"):
                p = os.path.normpath(os.path.join(d, sub, name + ext))
                if os.path.isfile(p) and os.access(p, os.X_OK):
                    return p
    return None


def _platform_candidates() -> List[str]:
    out: List[str] = []
    if sys.platform == "win32":
        roots = [os.environ.get(k) for k in ("ProgramFiles", "ProgramW6432", "ProgramFiles(x86)", "LOCALAPPDATA")]
        for r in filter(None, roots):
            for pattern in ("FreeCAD*", os.path.join("Programs", "FreeCAD*")):
                for d in sorted(glob.glob(os.path.join(r, pattern)), reverse=True):
                    out.append(os.path.join(d, "bin"))
    elif sys.platform == "darwin":
        for app in sorted(
            glob.glob("/Applications/FreeCAD*.app") + glob.glob(os.path.expanduser("~/Applications/FreeCAD*.app")),
            reverse=True,
        ):
            out += [os.path.join(app, "Contents", "Resources", "bin"), os.path.join(app, "Contents", "MacOS")]
    else:
        out += [
            "/usr/bin",
            "/usr/local/bin",
            "/snap/bin",
            "/usr/lib/freecad/bin",
            "/usr/lib/freecad-daily/bin",
            "/opt/freecad/bin",
        ]
    return out


def find_freecad(explicit: Optional[str]) -> Optional[Backend]:
    if explicit:
        if os.path.isdir(explicit):
            found = _cmd_in_dir(explicit)
            return Backend("subprocess", [found], "FCSKILL_FREECAD (directory)") if found else None
        return Backend("subprocess", _split(explicit), "FCSKILL_FREECAD")

    try:
        if importlib.util.find_spec("FreeCAD") is not None:
            # Still a separate process: a crash in the CAD kernel or a hang must not take the launcher with it.
            return Backend("python", [sys.executable], "python import")
    except (ImportError, ValueError):
        pass

    for name in CMD_NAMES:
        exe = shutil.which(name)
        if exe:
            return Backend("subprocess", [exe], "PATH")

    for d in _platform_candidates():
        found = _cmd_in_dir(d)
        if found:
            return Backend("subprocess", [found], "standard location")

    if shutil.which("flatpak"):
        for root in (
            "/var/lib/flatpak/app/org.freecad.FreeCAD",
            os.path.expanduser("~/.local/share/flatpak/app/org.freecad.FreeCAD"),
        ):
            if os.path.isdir(root):
                return Backend(
                    "subprocess", ["flatpak", "run", "--command=FreeCADCmd", "org.freecad.FreeCAD"], "flatpak"
                )
    return None


NOT_FOUND_HINT = (
    "Install FreeCAD 1.1 or newer (https://www.freecad.org/downloads.php), or point FCSKILL_FREECAD at its "
    "command-line executable, e.g. FCSKILL_FREECAD=/usr/bin/freecadcmd, "
    "FCSKILL_FREECAD='C:\\Program Files\\FreeCAD 1.1\\bin\\freecadcmd.exe', "
    "FCSKILL_FREECAD=/Applications/FreeCAD.app/Contents/Resources/bin/freecadcmd, or "
    "FCSKILL_FREECAD='/path/FreeCAD.AppImage freecadcmd'."
)


# ------------------------------------------------------------------ snap staging


def _snap_accessible(path: Path) -> bool:
    """Snap's 'home' interface allows non-hidden paths under $HOME only."""
    home = Path(os.path.realpath(os.path.expanduser("~")))
    real = Path(os.path.realpath(path))
    try:
        rel = real.relative_to(home)
    except ValueError:
        return False
    return not rel.parts or not rel.parts[0].startswith(".")


def _snap_common() -> Path:
    return Path(os.path.expanduser("~/snap/freecad/common/fcskill"))


def _stage_engine() -> Path:
    """Copy the engine where snap FreeCAD can read it; return its parent dir."""
    src = HERE / "fcengine"
    digest = hashlib.sha1()
    for f in sorted(src.rglob("*.py")):
        digest.update(f.relative_to(src).as_posix().encode())
        digest.update(f.read_bytes())
    dest_parent = _snap_common() / f"engine-{__version__}-{digest.hexdigest()[:10]}"
    if not (dest_parent / "fcengine").is_dir():
        tmp = dest_parent.with_name(dest_parent.name + f".tmp{os.getpid()}")
        shutil.copytree(src, tmp / "fcengine", ignore=shutil.ignore_patterns("__pycache__"))
        try:
            os.replace(tmp, dest_parent)
        except OSError:
            shutil.rmtree(tmp, ignore_errors=True)  # another process won the race
        # Drop copies of other engine versions; a running request keeps its
        # modules loaded, so removing its folder does not break it.
        for old in _snap_common().glob("engine-*"):
            if old != dest_parent and old.is_dir():
                shutil.rmtree(old, ignore_errors=True)
    return dest_parent


# ------------------------------------------------------------------ execution


def _doc_rel(request: Any) -> str:
    if isinstance(request, dict) and isinstance(request.get("doc"), str):
        return request["doc"]
    return "model.FCStd"


def _links_in(folder: str, names: List[str]) -> List[str]:
    """copytree filter: links are left out, so staging copies nothing from outside the folder."""
    return [n for n in names if os.path.islink(os.path.join(folder, n))]


def _run_tree(cmd: List[str], cwd: Path, timeout: float) -> "subprocess.CompletedProcess[bytes]":
    """Run FreeCAD; on timeout kill it together with its children (Gmsh, CalculiX), not just FreeCAD.

    FreeCAD starts with this process's environment, unchanged: the launcher neither copies nor edits it."""
    posix = os.name == "posix"
    kw: Dict[str, Any] = (
        {"start_new_session": True} if posix else {"creationflags": getattr(subprocess, "CREATE_NEW_PROCESS_GROUP", 0)}
    )
    proc = subprocess.Popen(
        cmd, cwd=str(cwd), stdin=subprocess.DEVNULL, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, **kw
    )
    try:
        out, _ = proc.communicate(timeout=timeout)
    except subprocess.TimeoutExpired:
        try:
            if posix:
                os.killpg(proc.pid, signal.SIGKILL)
            else:
                subprocess.run(
                    ["taskkill", "/F", "/T", "/PID", str(proc.pid)],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                    timeout=30,
                )
        except (OSError, subprocess.SubprocessError):
            pass
        proc.kill()
        proc.communicate()
        raise
    return subprocess.CompletedProcess(cmd, proc.returncode, out)


def run_subprocess(backend: Backend, request: Any, root: Path, timeout: float) -> Dict[str, Any]:
    staged_ws: Optional[Path] = None
    engine_parent = HERE
    if backend.is_snap:
        if not _snap_accessible(HERE):
            engine_parent = _stage_engine()
        io_dir = _snap_common() / "io" / uuid.uuid4().hex
        if not _snap_accessible(root):
            staged_ws = _snap_common() / "ws" / uuid.uuid4().hex
    else:
        io_dir = Path(tempfile.mkdtemp(prefix="fcskill-"))
    io_dir.mkdir(parents=True, exist_ok=True)

    run_root = root
    try:
        if staged_ws is not None:
            doc_rel = _doc_rel(request)
            real_doc = workspace.resolve(root, doc_rel)  # refuse escapes before copying anything
            staged_ws.mkdir(parents=True)
            if real_doc.exists():
                target = staged_ws / workspace.relative(root, real_doc)
                target.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(real_doc, target)
            for rel in workspace.request_inputs(request):  # imported files and fonts the request names
                src = workspace.resolve(root, rel)  # inside the workspace, or the request is refused
                if src.is_file():
                    target = staged_ws / workspace.relative(root, src)
                    target.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(src, target)
            # Downloaded library parts the request imports: real files only, from a cache not reached via links.
            parts = library.parts_folder(root) if library.library_refs(request) else None
            if parts is not None:
                shutil.copytree(parts, staged_ws / library.CACHE_DIR / "parts", ignore=_links_in)
            run_root = staged_ws

        req_file, resp_file = io_dir / "request.json", io_dir / "response.json"
        req_file.write_text(json.dumps(request), encoding="utf-8")
        boot = (
            f"import sys; sys.path.insert(0, {str(engine_parent)!r}); from fcengine.runner import main_from_files; "
            f"main_from_files({str(req_file)!r}, {str(resp_file)!r}, {str(run_root)!r})"
        )
        try:
            proc = _run_tree(backend.cmd + ["-c", boot], run_root, timeout)
        except subprocess.TimeoutExpired:
            return env_error(
                errors.TIMEOUT,
                f"FreeCAD did not finish within {timeout:.0f} s",
                hint="Split the request into smaller batches or raise --timeout. Very large arrays, fillets on "
                "complex shapes and fem_static with a fine mesh are slow.",
            )
        except OSError as e:
            return env_error(
                errors.FREECAD_NOT_FOUND, f"Cannot start FreeCAD ({backend.cmd[0]}): {e}", hint=NOT_FOUND_HINT
            )
        if not resp_file.exists():
            tail = proc.stdout.decode("utf-8", "replace")[-2000:] if proc.stdout else ""
            return env_error(
                errors.FREECAD_CRASHED,
                f"FreeCAD exited (code {proc.returncode}) without a response",
                hint="Run 'fcskill.py doctor'. If FreeCAD is a snap, keep the workspace inside your home directory.",
                details={"output_tail": tail, "command": backend.cmd},
            )
        resp = json.loads(resp_file.read_text(encoding="utf-8"))

        if staged_ws is not None and resp.get("status") == "success":
            for rel in resp.get("files_written", []):
                src = workspace.resolve(staged_ws, rel)  # both ends confined: nothing from or to outside
                dst = workspace.resolve(root, rel)
                dst.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(src, dst)
        return resp
    finally:
        shutil.rmtree(io_dir, ignore_errors=True)
        if staged_ws is not None:
            shutil.rmtree(staged_ws, ignore_errors=True)


def execute(request: Any, root: Path, explicit: Optional[str], timeout: float) -> Dict[str, Any]:
    backend = find_freecad(explicit)
    if backend is None:
        return env_error(errors.FREECAD_NOT_FOUND, "FreeCAD was not found", hint=NOT_FOUND_HINT)
    try:
        doc = workspace.resolve(root, _doc_rel(request))
        # One request per document at a time; waits up to the request timeout.
        with doclock.DocumentLock(doc, timeout):
            return run_subprocess(backend, request, root, timeout)
    except errors.SkillError as e:
        return errors.error_response(e, engine=__version__)


# ------------------------------------------------------------------ commands


def read_request(arg: Optional[str]) -> Any:
    if arg is None or arg == "-":
        if arg is None and sys.stdin.isatty():
            raise errors.SkillError(
                errors.INVALID_REQUEST, "No request given", hint="Pass a JSON file, '-' for stdin, or inline JSON."
            )
        text = sys.stdin.read()
    elif arg.lstrip().startswith("{"):
        text = arg
    else:
        path = Path(arg)
        if not path.is_file():
            raise errors.SkillError(errors.INVALID_REQUEST, f"Request file '{arg}' not found")
        text = path.read_text(encoding="utf-8-sig")  # tolerate a BOM (Windows Notepad)
    text = text.lstrip("\ufeff")
    try:
        return json.loads(text)
    except json.JSONDecodeError as e:
        raise errors.SkillError(
            errors.INVALID_JSON,
            f"Invalid JSON: {e}",
            hint="Write the request to a .json file and pass its path; this avoids shell quoting problems.",
        ) from None


def cmd_run(args: argparse.Namespace) -> int:
    try:
        request = read_request(args.request)
    except errors.SkillError as e:
        return emit(errors.error_response(e, engine=__version__), args.pretty)
    root = Path(args.workspace or os.environ.get("FCSKILL_WORKSPACE") or os.getcwd()).resolve()
    if not root.is_dir():
        return emit(
            env_error(
                errors.PATH_NOT_ALLOWED,
                f"Workspace '{root}' is not a directory",
                hint="Create the folder first, or pass an existing one with --workspace / FCSKILL_WORKSPACE.",
            ),
            args.pretty,
        )
    t0 = time.monotonic()
    refs = library.library_refs(request)
    if refs:  # downloaded here: FreeCAD's own Python may lack SSL, and the engine stays offline
        try:
            src = _library_source()
            index = library.load_index(root, src=src)
            for ref in refs:
                library.fetch(root, ref, index, src)
        except errors.SkillError as e:
            return emit(errors.error_response(e, engine=__version__), args.pretty)
    resp = execute(request, root, args.freecad or os.environ.get("FCSKILL_FREECAD"), args.timeout)
    resp["elapsed_s"] = round(time.monotonic() - t0, 2)
    return emit(resp, args.pretty)


def _library_source() -> "library.Source":
    """The parts library settings: a local clone (FCSKILL_LIBRARY) and the offline switch (FCSKILL_OFFLINE)."""
    return library.source(os.environ.get(library.ENV_LOCAL), os.environ.get(library.ENV_OFFLINE) == "1")


def cmd_library(args: argparse.Namespace) -> int:
    root = Path(args.workspace or os.environ.get("FCSKILL_WORKSPACE") or os.getcwd()).resolve()
    try:
        index = library.load_index(root, refresh=args.refresh, src=_library_source())
        if not args.query:
            return emit(
                {
                    "status": "success",
                    "source": index["source"],
                    "files": len(index["files"]),
                    "note": "Give keywords to search, e.g. 'library 608 bearing'.",
                },
                args.pretty,
            )
        matches = library.search(index, " ".join(args.query), args.limit)
    except errors.SkillError as e:
        return emit(errors.error_response(e, engine=__version__), args.pretty)
    resp: Dict[str, Any] = {
        "status": "success",
        "query": " ".join(args.query),
        "matches": matches,
        "license": library.LICENSE,
        "source": index["source"],
    }
    if matches:
        resp["next"] = (
            'Import with {"op": "import", "library": "<part>", "name": "...", "anchor": "center", '
            '"position": [x, y, z]}; pass the reported attribution on to the user.'
        )
    else:
        resp["hint"] = "No match: try fewer or broader keywords (e.g. 'bearing' instead of 'deep groove bearing 608')."
    return emit(resp, args.pretty)


def cmd_describe(args: argparse.Namespace) -> int:
    unknown = [n for n in args.ops if n not in catalog.OPS_BY_NAME]
    if unknown:
        emit(
            env_error(errors.UNKNOWN_OP, f"Unknown op(s): {unknown}", details={"ops": list(catalog.OPS_BY_NAME)}),
            args.pretty,
        )
        return 2  # usage error
    if args.markdown:
        from fcengine import docs

        sys.stdout.write(docs.operations_markdown(args.ops or None))
        return 0
    data = catalog.describe(args.ops or None)
    if not args.ops:  # compact index: one line per op
        data["ops"] = [
            {
                "op": o["op"],
                "category": o["category"],
                "summary": o["summary"],
                "params": {k: ("*" if v.get("required") else "") + v["type"] for k, v in o["params"].items()},
            }
            for o in data["ops"]
        ]
        data["note"] = "'*' marks required params. Run 'describe <op>' for full details."
    print(json.dumps(data, indent=2 if args.pretty else None))
    return 0


def cmd_doctor(args: argparse.Namespace) -> int:
    report: Dict[str, Any] = {"engine": __version__, "python": sys.version.split()[0], "platform": sys.platform}
    backend = find_freecad(args.freecad or os.environ.get("FCSKILL_FREECAD"))
    if backend is None:
        report.update(
            status="error",
            error={"code": errors.FREECAD_NOT_FOUND, "message": "FreeCAD was not found", "hint": NOT_FOUND_HINT},
        )
        return emit(report, True)
    report["backend"] = backend.describe()
    base = _snap_common() / "doctor" if backend.is_snap else Path(tempfile.mkdtemp(prefix="fcskill-doctor-"))
    base.mkdir(parents=True, exist_ok=True)
    probe = {
        "doc": "doctor.FCStd",
        "new": True,
        "steps": [
            {"op": "box", "name": "B", "length": 10, "width": 10, "height": 10},
            {"op": "cylinder", "name": "C", "radius": 2, "height": 12, "position": [5, 5, -1]},
            {
                "op": "cut",
                "name": "R",
                "base": "B",
                "tool": "C",
                "expect": {"volume": 1000 - 3.14159265 * 4 * 10, "volume_tolerance": 0.0001},
            },
            {"op": "export", "filename": "doctor.step"},
        ],
    }
    t0 = time.monotonic()
    try:
        resp = run_subprocess(backend, probe, base, args.timeout)
    finally:
        shutil.rmtree(base, ignore_errors=True)
    report["probe_seconds"] = round(time.monotonic() - t0, 2)
    if resp.get("status") == "success":
        report.update(
            status="success",
            freecad=resp.get("freecad"),
            message="FreeCAD works: modelled, verified and exported a test part.",
        )
    else:
        report.update(status="error", error=resp.get("error"))
    if backend.is_snap:
        report["note"] = (
            "FreeCAD is a snap: files outside your home directory or in hidden folders (e.g. ~/.openclaw) "
            "are staged through ~/snap/freecad/common automatically."
        )
    return emit(report, True)


def main(argv: Optional[List[str]] = None) -> int:
    argv = list(sys.argv[1:] if argv is None else argv)
    if argv and argv[0].lstrip().startswith("{"):
        argv = ["run"] + argv  # shorthand: fcskill.py '<json>'
    parser = argparse.ArgumentParser(prog="fcskill", description="FreeCAD modelling for AI agents.")
    parser.add_argument("--version", action="version", version=f"fcskill {__version__}")
    sub = parser.add_subparsers(dest="command")

    def common(p: argparse.ArgumentParser) -> None:
        p.add_argument("--freecad", help="FreeCAD command (default: $FCSKILL_FREECAD or auto-detect)")
        p.add_argument("--timeout", type=float, default=DEFAULT_TIMEOUT, help="seconds (default 300)")
        p.add_argument("--pretty", action="store_true", help="indent JSON output")

    p_run = sub.add_parser("run", help="execute a request")
    p_run.add_argument("request", nargs="?", help="JSON file, '-' for stdin, or inline JSON")
    p_run.add_argument(
        "--workspace", help="root directory for documents and exports (default: $FCSKILL_WORKSPACE or cwd)"
    )
    common(p_run)
    p_desc = sub.add_parser("describe", help="list operations and their parameters")
    p_desc.add_argument("ops", nargs="*")
    p_desc.add_argument("--markdown", action="store_true")
    p_desc.add_argument("--pretty", action="store_true")
    p_doc = sub.add_parser("doctor", help="check that FreeCAD works")
    common(p_doc)
    p_lib = sub.add_parser("library", help="search the official FreeCAD parts library")
    p_lib.add_argument("query", nargs="*", help="keywords, e.g. 608 bearing")
    p_lib.add_argument("--limit", type=int, default=10)
    p_lib.add_argument("--refresh", action="store_true", help="re-download the library index")
    p_lib.add_argument("--workspace", help="workspace holding the cache (default: $FCSKILL_WORKSPACE or cwd)")
    p_lib.add_argument("--pretty", action="store_true")

    args = parser.parse_args(argv)
    if args.command == "run":
        return cmd_run(args)
    if args.command == "describe":
        return cmd_describe(args)
    if args.command == "doctor":
        return cmd_doctor(args)
    if args.command == "library":
        return cmd_library(args)
    parser.print_help(sys.stderr)
    return 2


if __name__ == "__main__":
    sys.exit(main())
