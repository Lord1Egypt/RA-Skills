"""bootstrap.py — make this skill runnable, and say which interpreter to use.

Run this FIRST, before any other script. It is idempotent and safe to
re-run.

    python scripts/bootstrap.py

Creates the virtualenv (outside the skill folder, so it is never
published), installs the requirements, installs the browser, and verifies
the imports actually work. Then it prints the interpreter to use, e.g.

    interpreter: /home/you/.cache/art-harvest/venv/bin/python

Every other script in this skill expects that interpreter. An agent driving
this skill should read the path from this script's output and pass it to
subsequent commands rather than guessing or using a bare `python`, which
resolves to a system interpreter with no playwright installed.

Options:
    --check     report status only, change nothing
    --recreate  delete and rebuild the venv (after editing requirements)
    --browser   also install the bundled Chromium (slow, ~150MB). The
                --channel msedge default uses your installed Edge instead,
                so this is only needed for offline Chromium use.
"""
from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
VENV = Path.home() / ".cache" / "art-harvest" / "venv"
REQUIREMENTS = HERE / "requirements.txt"

# Import name -> what breaks without it.
NEEDED = {"playwright": "browser transport (browser.py needs this)",
          "PIL": "image verification and the 512px/20KB floors",
          "huggingface_hub": "publish.py --mode hf only"}


def venv_python(root: Path | None = None) -> Path:
    # Resolve VENV at call time, never as a default argument. A default is
    # bound once at import, so reassigning VENV (as the tests do) would be
    # silently ignored and the check would inspect the wrong directory.
    root = root or VENV
    if os.name == "nt":
        return root / "Scripts" / "python.exe"
    return root / "bin" / "python"


def venv_exists(root: Path | None = None) -> bool:
    return venv_python(root).exists()


def run(cmd: list[str], **kw) -> subprocess.CompletedProcess:
    try:
        return subprocess.run(cmd, capture_output=True, text=True, **kw)
    except FileNotFoundError as e:
        # A missing interpreter or tool is an answer, not a crash. Callers
        # branch on returncode, and an exception here escapes all of them.
        return subprocess.CompletedProcess(cmd, 127, "", str(e))


def imports_ok(py: Path, mod: str) -> bool:
    """Ask the interpreter directly, never parse `pip list`.

    A venv built by `uv` has no pip at all, so a pip-based check reports
    every dependency as MISSING on a perfectly good environment. That is
    worse than no check: it sends the user to reinstall what is already
    installed.
    """
    return run([str(py), "-c", f"import {mod}"]).returncode == 0


def pip_command(py: Path) -> tuple[list[str], str] | None:
    """Return (argv prefix, interpreter flag) for `install <packages>`.

    Every prefix already includes the `install` subcommand, so the caller
    only appends the package arguments. Tries pip first, then uv, then
    ensurepip — a venv created by `uv` has no pip at all, so a pip-only
    bootstrap fails on exactly the machines most likely to be current.

    The flag differs because uv wants `--python` AFTER its subcommand
    (`uv pip install --python X`) while pip needs no such flag. Getting
    that order wrong is an "unexpected argument" error.
    """
    if run([str(py), "-m", "pip", "--version"]).returncode == 0:
        return [str(py), "-m", "pip", "install"], ""
    uv = shutil.which("uv")
    if uv:
        return [uv, "pip", "install"], "--python"
    if run([str(py), "-m", "ensurepip", "--upgrade"]).returncode == 0:
        return [str(py), "-m", "pip", "install"], ""
    return None


def report() -> int:
    """Print status. Return 0 if the environment is usable."""
    print(f"venv path      : {VENV}")
    if not venv_exists():
        print("venv           : MISSING — run: python scripts/bootstrap.py")
        return 1
    py = venv_python()
    print(f"interpreter    : {py}")
    r = run([str(py), "-c", "import sys; print(sys.version.split()[0])"])
    print(f"python         : {r.stdout.strip() or '?'}")
    missing = []
    for mod, why in NEEDED.items():
        if imports_ok(py, mod):
            print(f"  {mod:<18} ok")
        else:
            state = "optional" if mod == "huggingface_hub" else "MISSING"
            print(f"  {mod:<18} {state} — {why}")
            if mod != "huggingface_hub":
                missing.append(mod)
    if missing:
        print("\nrun: python scripts/bootstrap.py")
        return 1
    print("\nready.")
    print(f"interpreter: {py}")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--check", action="store_true",
                    help="report status only, change nothing")
    ap.add_argument("--recreate", action="store_true",
                    help="delete and rebuild the venv")
    ap.add_argument("--browser", action="store_true",
                    help="also install bundled Chromium (slow)")
    args = ap.parse_args()

    if args.check:
        return report()

    if args.recreate and VENV.exists():
        print(f"removing {VENV}")
        import shutil
        shutil.rmtree(VENV, ignore_errors=True)

    if not venv_exists():
        print(f"creating venv at {VENV}")
        r = run([sys.executable, "-m", "venv", str(VENV)])
        if r.returncode or not venv_exists():
            print(r.stdout + r.stderr)
            print("\nCould not create the venv. On Debian/Ubuntu you may need"
                  "\n  sudo apt install python3-venv")
            return 1
    else:
        print(f"venv exists at {VENV}")

    py = venv_python()
    found = pip_command(py)
    if found is None:
        print("no pip, uv, or working ensurepip found; cannot install.")
        print("Install one of them, then re-run. e.g.")
        print("  python3 -m ensurepip --upgrade")
        print("  # or install uv:  curl -LsSf https://astral.sh/uv/install.sh | sh")
        return 1
    pip, flag = found
    cmd = pip + [flag, str(py)] if flag else pip
    print(f"\ninstalling requirements with {' '.join(cmd)}")
    r = run(cmd + ["-r", str(REQUIREMENTS)])
    print(r.stdout[-1200:] if r.returncode == 0 else (r.stdout + r.stderr)[-1600:])
    if r.returncode:
        print("\nrequirements failed to install")
        return 1

    if args.browser:
        print("\ninstalling bundled Chromium (this downloads ~150MB)")
        r = run([str(py), "-m", "playwright", "install", "chromium"])
        print((r.stdout + r.stderr)[-600:])
    else:
        print("\nskipping bundled Chromium. The default --channel msedge uses "
              "your\ninstalled Edge, which has the best bot-wall pass rate. "
              "Add --browser if you\nneed offline Chromium.")

    rc = report()
    if rc == 0:
        print("\nNext: use that interpreter for every other script, e.g.")
        print(f'  "{py}" scripts/harvest.py --probe --sources yandere,e621')
    return rc


if __name__ == "__main__":
    raise SystemExit(main())