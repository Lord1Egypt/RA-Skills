"""One process runner for the skill scripts.

Safe because there is a single ``subprocess.run`` and ``shell`` is off, so
the shell never parses the command. The executable is only ``git``, ``tar``,
or this Python interpreter. ``python`` means ``sys.executable``, the same
interpreter that launched the caller. Every argument is a string with no
NUL. Git's first argument has to be one of the subcommands these scripts
use. A patch or a tar archive is stdin, not an argument.
"""

import subprocess
import sys

_GIT_COMMANDS = frozenset({
    "add",
    "apply",
    "archive",
    "commit",
    "diff",
    "log",
    "ls-files",
    "reset",
    "rev-parse",
    "status",
})
_TOOLS = frozenset({"git", "tar", "python"})


def run_git(args, *, cwd, stdin=None, text=True, capture_output=True):
    """Run git in ``cwd``. ``args`` is the list after the executable."""
    if cwd is None:
        sys.exit("refusing to run git without a working directory")
    return _run("git", args, cwd=cwd, stdin=stdin, text=text, capture_output=capture_output)


def run_tool(name, args, *, cwd=None, stdin=None, text=False, capture_output=False):
    """Run tar or this Python interpreter. ``args`` is the list after the executable."""
    if name == "git":
        sys.exit("use run_git for git")
    return _run(name, args, cwd=cwd, stdin=stdin, text=text, capture_output=capture_output)


def _run(name, args, *, cwd, stdin, text, capture_output):
    if name not in _TOOLS:
        sys.exit(f"refusing executable {name!r}")
    if name == "git":
        if not isinstance(args, list) or not args or args[0] not in _GIT_COMMANDS:
            sys.exit("refusing a git command that is not one of the fixed forms")
    elif name == "tar":
        if not isinstance(args, list) or not args or args[0] != "-x":
            sys.exit("refusing a tar command that is not extract")
    elif not isinstance(args, list) or not args:
        sys.exit("refusing a command with no arguments")
    if any(not isinstance(item, str) or "\0" in item for item in args):
        sys.exit("refusing a command argument that is not plain text")
    if text:
        if stdin is not None and not isinstance(stdin, str):
            sys.exit("refusing stdin that is not text")
    elif stdin is not None and not isinstance(stdin, (bytes, bytearray)):
        sys.exit("refusing stdin that is not bytes")
    executable = sys.executable if name == "python" else name
    return subprocess.run(
        [executable, *args],
        shell=False,
        cwd=cwd,
        check=True,
        text=text,
        capture_output=capture_output,
        input=None if stdin is None else stdin,
    )
