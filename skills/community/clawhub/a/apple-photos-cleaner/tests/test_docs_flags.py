#!/usr/bin/env python3
"""
Docs-vs-CLI audit (ROADMAP T0.5).

Agents learn the CLI from SKILL.md, so a documented flag that a script doesn't
accept is a guaranteed failed command. Each script's real flags come from its
own `--help` (which exits before touching any database), so this needs no
refactoring of the scripts and stays true to what users actually run.
"""

import argparse
import importlib
import re
import subprocess
import sys
from functools import cache
from pathlib import Path
from unittest.mock import patch

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
SCRIPTS_DIR = REPO_ROOT / "scripts"
COMMAND_DOCS = sorted(p.relative_to(REPO_ROOT).as_posix() for p in (REPO_ROOT / "references" / "commands").glob("*.md"))
DOCS = ["SKILL.md", "README.md", "references/workflows.md", *COMMAND_DOCS]

SCRIPT_NAMES = sorted(p.stem for p in SCRIPTS_DIR.glob("[a-z]*.py"))
FLAG = re.compile(r"(?<![\w-])(--[a-z][a-z0-9-]*)")
SCRIPT_REF = re.compile(r"\b(" + "|".join(SCRIPT_NAMES) + r")\.py\b")


@cache
def cli_flags(script: str) -> frozenset[str]:
    """Long options from the script's --help, excluding its examples epilog."""
    result = subprocess.run(
        [sys.executable, str(SCRIPTS_DIR / f"{script}.py"), "--help"],
        capture_output=True,
        text=True,
        check=True,
        cwd=REPO_ROOT,
    )
    options = re.split(r"\n(?:examples|Examples):", result.stdout)[0]
    return frozenset(FLAG.findall(options))


def logical_lines(text: str):
    """Yield (line_number, line), joining shell `\\` continuations."""
    lines = text.splitlines()
    i = 0
    while i < len(lines):
        start, line = i + 1, lines[i]
        while line.rstrip().endswith("\\") and i + 1 < len(lines):
            i += 1
            line = line.rstrip()[:-1] + " " + lines[i]
        yield start, line
        i += 1


def documented_script_flags(doc: str) -> list[tuple[int, str, str]]:
    """(line, script, flag) for each flag that follows a `<script>.py` mention on the same line."""
    found = []
    for lineno, line in logical_lines((REPO_ROOT / doc).read_text(encoding="utf-8")):
        refs = list(SCRIPT_REF.finditer(line))
        for k, ref in enumerate(refs):
            segment_end = refs[k + 1].start() if k + 1 < len(refs) else len(line)
            found.extend((lineno, ref[1], flag) for flag in FLAG.findall(line[ref.end() : segment_end]))
    return found


def test_every_script_has_help():
    assert SCRIPT_NAMES, "no scripts found"
    for script in SCRIPT_NAMES:
        assert "--help" in cli_flags(script), script


@pytest.mark.parametrize("doc", DOCS)
def test_documented_flags_exist_on_their_script(doc):
    missing = [
        f"{doc}:{lineno}: {script}.py {flag}"
        for lineno, script, flag in documented_script_flags(doc)
        if flag not in cli_flags(script)
    ]
    assert not missing, "Documented flags the script doesn't accept:\n" + "\n".join(missing)


@pytest.mark.parametrize("doc", DOCS)
def test_every_mentioned_flag_exists_somewhere(doc):
    """Catches flags in prose and tables that don't name a script on the same line."""
    known = frozenset().union(*(cli_flags(s) for s in SCRIPT_NAMES))
    unknown = [
        f"{doc}:{lineno}: {flag}"
        for lineno, line in logical_lines((REPO_ROOT / doc).read_text(encoding="utf-8"))
        for flag in FLAG.findall(line)
        if flag not in known
    ]
    assert not unknown, "Flags no script defines:\n" + "\n".join(unknown)


def test_extractor_finds_documented_usage():
    """Guard the guard: if parsing silently finds nothing, the tests above pass vacuously."""
    flags = [flag for doc in DOCS for flag in documented_script_flags(doc)]
    assert len(flags) > 40
    assert ("cleanup_executor", "--execute") in {(s, f) for _, s, f in flags}


# ── Documented defaults ──────────────────────────────────────────────────────

OPTION_DEFAULT = re.compile(r"^- `(--[a-z][a-z0-9-]*)[^`]*` — .*?\(default: ([^,)]+)")


class _ParserCapturedError(Exception):
    def __init__(self, parser: argparse.ArgumentParser):
        self.parser = parser


@cache
def cli_defaults(script: str) -> dict[str, object]:
    """Each long option's real default, read from the parser main() builds (stops before parsing)."""
    module = importlib.import_module(script)

    def capture(parser, *args, **kwargs):
        raise _ParserCapturedError(parser)

    with patch.object(argparse.ArgumentParser, "parse_args", capture), pytest.raises(_ParserCapturedError) as caught:
        module.main()
    return {
        option: action.default
        for action in caught.value.parser._actions
        for option in action.option_strings
        if option.startswith("--")
    }


def documented_defaults() -> list[tuple[str, str, str, str]]:
    """(location, script, flag, documented default) from each references/commands/<script>.md option list."""
    found = []
    for doc in COMMAND_DOCS:
        script = Path(doc).stem
        for lineno, line in enumerate((REPO_ROOT / doc).read_text(encoding="utf-8").splitlines(), start=1):
            if match := OPTION_DEFAULT.match(line):
                found.append((f"{doc}:{lineno}", script, match[1], match[2].strip()))
    return found


def same_default(documented: str, actual: object) -> bool:
    if isinstance(actual, bool) or actual is None:
        return False
    if isinstance(actual, (int, float)):
        try:
            return float(documented) == float(actual)
        except ValueError:
            return False
    return documented == str(actual)


def test_documented_defaults_match_argparse():
    documented = documented_defaults()
    assert len(documented) >= 20, "default extraction found too little; the parser above is broken"
    wrong = [
        f"{where}: {script}.py {flag} documented {doc!r}, actual {cli_defaults(script).get(flag)!r}"
        for where, script, flag, doc in documented
        if not same_default(doc, cli_defaults(script).get(flag))
    ]
    assert not wrong, "Documented defaults that don't match the code:\n" + "\n".join(wrong)
