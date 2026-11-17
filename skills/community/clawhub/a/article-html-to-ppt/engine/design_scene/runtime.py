"""Portable bounded processes, optional OS isolation, and real rendering."""
from __future__ import annotations

import importlib.metadata
import json
import os
import platform
import re
import shutil
import signal
import subprocess
import sys
from pathlib import Path

from .store import DesignError, Store, digest

CODE_ROOT = Path(__file__).resolve().parents[2]


def find_tool(name):
    path = shutil.which(name)
    if path:
        if os.name == "nt" and name == "soffice" and Path(path).with_suffix(".com").is_file():
            path = str(Path(path).with_suffix(".com"))
        return str(Path(path).absolute())
    if name == "soffice":
        candidates = [Path("/Applications/LibreOffice.app/Contents/MacOS/soffice")]
        if os.name == "nt":
            candidates = [Path(os.environ[key]) / "LibreOffice/program/soffice.com"
                          for key in ("ProgramFiles", "ProgramFiles(x86)") if key in os.environ]
        return next((str(p) for p in candidates if p.is_file()), None)
    return None


def select_isolation(requested="auto"):
    if requested not in {"auto", "host", "macos"}:
        raise DesignError("UNKNOWN_ISOLATION_MODE")
    available = platform.system() == "Darwin" and bool(shutil.which("sandbox-exec"))
    if requested == "macos" and not available:
        raise DesignError("OS_SANDBOX_UNAVAILABLE: macos requires Darwin and sandbox-exec; use host for local execution")
    return ("macos" if available else "host") if requested == "auto" else requested


def execution_capabilities():
    mode = select_isolation()
    return {"default_mode": mode, "available_modes": ["host", "macos"] if mode == "macos" else ["host"],
            "host_can_deliver": True, "os_isolation_required_by_default": False,
            "strict_os_isolation_available": mode == "macos",
            "filesystem": "windows_locked_handles" if os.name == "nt" else "posix_dir_fd",
            "posix_resource_limits": os.name == "posix"}


def run_process(args, *, cwd, timeout=120, env=None, capture_stderr=False):
    """No shell; terminate the process tree after a bounded wait."""
    options = ({"creationflags": subprocess.CREATE_NEW_PROCESS_GROUP} if os.name == "nt"
               else {"start_new_session": True})
    p = subprocess.Popen(args, cwd=cwd, env=env, stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE, **options)
    try:
        out, err = p.communicate(timeout=timeout)
    except subprocess.TimeoutExpired as exc:
        if os.name == "nt":
            killer = Path(os.environ.get("SystemRoot", "C:/Windows")) / "System32/taskkill.exe"
            try:
                subprocess.run([str(killer), "/PID", str(p.pid), "/T", "/F"],
                               stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=10)
            except (OSError, subprocess.TimeoutExpired):
                pass
            if p.poll() is None:
                p.kill()
        else:
            try:
                os.killpg(p.pid, signal.SIGKILL)
            except ProcessLookupError:
                pass
        try:
            p.communicate(timeout=10)
        except subprocess.TimeoutExpired:
            # An escaped descendant must not leave our pipe drain unbounded.
            p.stdout.close()
            p.stderr.close()
        raise DesignError("PROCESS_TIMEOUT") from exc
    if p.returncode:
        raise DesignError(f"PROCESS_FAILED ({Path(args[0]).name}): {(err or out).decode('utf-8', 'replace')[-1800:]}")
    return (out + (b"\n" + err if capture_stderr else b"")).decode("utf-8", "replace").strip()


def clean_environment(stage):
    # Deliberately do not forward API keys, proxies, Python hooks, or user env.
    paths = [str(Path(sys.executable).parent)]
    paths += [str(Path(p).parent) for name in ("soffice", "pdftoppm", "fc-match") if (p := find_tool(name))]
    paths += [p for p in os.defpath.split(os.pathsep) if os.path.isabs(p)]
    if os.name != "nt":
        paths += ["/usr/local/bin", "/opt/homebrew/bin"]
    env = {"PATH": os.pathsep.join(dict.fromkeys(paths)), "LANG": "en_US.UTF-8", "PYTHONUTF8": "1",
           "PYTHONDONTWRITEBYTECODE": "1", "PYTHONPATH": str(CODE_ROOT),
           "TMPDIR": str(stage / "tmp"), "TMP": str(stage / "tmp"), "TEMP": str(stage / "tmp"),
           "XDG_CACHE_HOME": str(stage / "cache"),
           "XDG_CONFIG_HOME": str(stage / "config")}
    # Keep the real home identity; do not point HOME at a fake user directory.
    # Seatbelt still denies reads/writes there except explicit trusted libraries.
    for key in ("HOME", "USER", "LOGNAME", "SystemRoot", "WINDIR", "USERPROFILE", "APPDATA",
                "LOCALAPPDATA", "ProgramFiles", "ProgramFiles(x86)"):
        if key in os.environ:
            env[key] = os.environ[key]
    return env


def sandbox_command(args, stage, mode):
    mode = select_isolation(mode)
    if mode == "host":
        return args
    roots = {"/System", "/Library", "/usr", "/opt", "/bin", "/sbin", "/Applications", "/private/etc",
             "/private/var/db/dyld", "/private/var/db/timezone", "/private/preboot/Cryptexes",
             str(CODE_ROOT / "engine"), str(stage)}
    # The package directories are trusted installed dependencies, not task data.
    roots.update(str(Path(p).resolve()) for p in sys.path if p and ("site-packages" in p or "lib/python" in p))
    # dyld's libignition and descriptor-relative Store both open ancestor
    # directories. Permit those directories themselves, never their subtrees.
    literals = {"/", "/dev/null", "/dev/urandom", "/dev/random", "/etc", "/tmp", "/var"}
    for root in roots:
        literals.update(str(p) for p in Path(root).parents)
    reads = " ".join(f"(subpath {json.dumps(p)})" for p in sorted(roots))
    reads += " " + " ".join(f"(literal {json.dumps(p)})" for p in sorted(literals))
    profile = f"(version 1)(allow default)(deny network*)(deny file-read*)(deny file-write*)(allow file-read-metadata)(allow file-read* {reads})(allow file-read* file-write* (subpath {json.dumps(str(stage))}))(allow file-write* (literal \"/dev/null\"))"
    # LibreOffice's per-profile single-instance IPC is a local Unix socket.
    # Restrict it to this private build directory; all IP networking stays denied.
    if not re.fullmatch(r"[\w /.-]+", str(stage)):
        raise DesignError("SANDBOX_PATH_UNSUPPORTED: use letters, numbers, spaces, dots, dashes or underscores")
    # SBPL regex literals do not use JSON's backslash-unescaping rules. Avoid
    # backslashes entirely so a literal dot stays a literal dot in Seatbelt.
    pipe_pattern = json.dumps("^(" + str(stage).replace(".", "[.]") + r"/|[.]/)OSL_PIPE_[0-9]+_SingleOfficeIPC_[0-9a-f]+$", ensure_ascii=False)
    profile += f"(allow network-bind network-inbound (local unix-socket (path-regex #{pipe_pattern})))(allow network-outbound (remote unix-socket (path-regex #{pipe_pattern})))"
    return ["/usr/bin/sandbox-exec", "-p", profile, *args]


def renderer_identity():
    code = {}
    for p in sorted((CODE_ROOT / "engine" / "design_scene").glob("*.py")):
        code[p.name] = digest(p.read_bytes())
    tools = {}
    for name in ("soffice", "pdftoppm", "fc-match"):
        path = find_tool(name)
        tools[name] = digest(Path(path).resolve().read_bytes()) if path else None
    if Path("/Applications/LibreOffice.app/Contents/MacOS/soffice").is_file():
        tools["libreoffice_binary"] = digest(Path("/Applications/LibreOffice.app/Contents/MacOS/soffice").read_bytes())
    return {"code": code, "python": platform.python_version(), "platform": platform.platform(), "tools": tools,
            "dependencies": {p: importlib.metadata.version(p) for p in ("python-pptx", "Pillow", "jsonschema", "lxml")}}


def fonts_for(task):
    from .contract import walk
    families = set()
    for page in task["scene"]["pages"]:
        for n, *_ in walk(page["nodes"]):
            if "font" in n:
                families.add(n["font"]["family"])
            families.update(s["font"]["family"] for s in n.get("spans", []))
    result = []
    matcher = find_tool("fc-match")
    for family in sorted(families):
        if not matcher:
            result.append({"requested": family, "status": "unverified"})
            continue
        try:
            found = run_process([matcher, "-f", "%{family}\n%{file}", family], cwd=CODE_ROOT, timeout=10)
            name, path = found.split("\n", 1)
            result.append({"requested": family, "matched": name,
                           "sha256": digest(Path(path).read_bytes()),
                           "status": "matched" if family.casefold() in [s.strip().casefold() for s in name.split(",")] else "substituted"})
        except (OSError, DesignError, ValueError):
            result.append({"requested": family, "status": "unverified"})
    return result


def launch_worker(stage, *, isolation="auto", preview=True, timeout=180):
    with Store(stage) as store:
        # Create private work directories using the same no-symlink boundary.
        for directory in ("tmp", "cache", "config", "lo-profile"):
            store.write(directory + "/.owner", b"pptsmith", exclusive=True)
    args = [sys.executable, "-B", "-m", "engine.design_scene.worker", str(stage)]
    if preview:
        args.append("--preview")
    command = sandbox_command(args, stage, isolation)
    return run_process(command, cwd=stage, timeout=timeout, env=clean_environment(stage))


def real_preview(stage, task):
    soffice, poppler = find_tool("soffice"), find_tool("pdftoppm")
    if not soffice or not poppler:
        return {"status": "unavailable", "reason": "LIBREOFFICE_OR_POPPLER_UNAVAILABLE", "pages": []}
    try:
        profile_arg = "-env:UserInstallation=" + (stage / "lo-profile").as_uri()
        lo_version = run_process([soffice, profile_arg, "--version"], cwd=stage, timeout=15)
        # A relative socket directory keeps sockaddr_un below its path limit,
        # even when the authorized task lives in a deeply nested worktree.
        conversion_log = run_process([soffice, profile_arg, "-env:OSL_SOCKET_PATH=.",
                     "--headless", "--convert-to", "pdf", "--outdir", str(stage), str(stage / "deck.pptx")], cwd=stage, capture_stderr=True)
        with Store(stage) as store:
            store.write("conversion.log", conversion_log.encode("utf-8"), exclusive=True)
            if not (stage / "deck.pdf").is_file():
                raise DesignError("RENDER_PDF_MISSING: " + conversion_log[-1800:])
            store.read("deck.pdf")
        dpi = min(144, 1920 * 72 / max(task["canvas"]["width"], task["canvas"]["height"]))
        run_process([poppler, "-r", str(dpi), "-png", str(stage / "deck.pdf"), str(stage / "preview")], cwd=stage)
        images = sorted(stage.glob("preview-*.png"), key=lambda p: int(p.stem.split("-")[-1]))
        if len(images) != len(task["scene"]["pages"]):
            raise DesignError("REAL_RENDER_PAGE_COUNT_MISMATCH")
        from .store import decode_image
        pages = []
        with Store(stage) as store:
            for p, page in zip(images, task["scene"]["pages"]):
                data = store.read(p.name)
                im = decode_image(data)
                if abs(im.width / im.height / (task["canvas"]["width"] / task["canvas"]["height"]) - 1) > .01:
                    raise DesignError("REAL_RENDER_ASPECT_MISMATCH")
                pages.append({"page_id": page["id"], "file": p.name, "sha256": digest(data), "width": im.width, "height": im.height})
        return {"status": "passed", "engine": "LibreOffice", "version": lo_version,
                "path": "PPTX → PDF → PNG", "dpi": dpi, "pages": pages}
    except (DesignError, OSError) as exc:
        return {"status": "failed", "reason": str(exc), "pages": []}
