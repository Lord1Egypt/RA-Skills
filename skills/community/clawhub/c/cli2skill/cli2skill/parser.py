"""Parse CLI --help output into structured command metadata."""
from __future__ import annotations
import re
import subprocess
import sys
from dataclasses import dataclass, field


@dataclass
class Argument:
    name: str
    description: str = ""
    required: bool = True
    default: str | None = None


@dataclass
class Option:
    flags: str          # e.g. "-k, --top-k"
    description: str = ""
    default: str | None = None
    value_type: str = ""


@dataclass
class Command:
    name: str
    description: str = ""
    arguments: list[Argument] = field(default_factory=list)
    options: list[Option] = field(default_factory=list)


@dataclass
class CLIMetadata:
    name: str
    description: str = ""
    commands: list[Command] = field(default_factory=list)
    global_options: list[Option] = field(default_factory=list)


def run_help(executable: str, args: list[str] | None = None) -> str:
    """Run `executable --help` and capture stdout+stderr."""
    # Support multi-word executables like "python script.py"
    cmd = executable.split() + (args or []) + ["--help"]
    try:
        result = subprocess.run(
            cmd, capture_output=True, text=True, timeout=10,
        )
        return result.stdout or result.stderr
    except FileNotFoundError:
        print(f"Error: '{executable}' not found in PATH", file=sys.stderr)
        sys.exit(1)
    except subprocess.TimeoutExpired:
        print(f"Error: '{executable} --help' timed out", file=sys.stderr)
        sys.exit(1)


def parse_help_text(name: str, text: str) -> CLIMetadata:
    """Parse generic --help output into CLIMetadata."""
    meta = CLIMetadata(name=name)

    lines = text.strip().splitlines()

    # Extract top-level description (first non-empty line before section headers)
    section_headers = ("usage", "options", "commands", "positional",
                       "core commands", "additional commands", "flags",
                       "available commands", "subcommands", "github actions")
    desc_lines = []
    for line in lines:
        lower = line.strip().lower()
        if any(lower.startswith(h) for h in section_headers):
            break
        if line.strip():
            desc_lines.append(line.strip())
    meta.description = " ".join(desc_lines[:2])  # Keep first 2 lines max

    # Extract subcommands — support multiple formats:
    # Format A (argparse):  "  command_name   description text"
    # Format B (cobra/gh):  "  name:          description text" or "name:  desc"
    # Format C (section):   lines under COMMANDS/CORE COMMANDS/etc headers
    in_commands = False
    for line in lines:
        lower = line.strip().lower()
        if any(lower.startswith(h) for h in (
            "commands", "subcommands", "positional arguments",
            "core commands", "additional commands", "available commands",
            "alias commands", "github actions commands",
        )):
            in_commands = True
            continue
        # Section break: empty line after a non-command section header
        if in_commands:
            # Stop on known non-command sections
            if any(lower.startswith(h) for h in (
                "options", "flags", "help topics", "learn more",
                "examples", "environment",
            )):
                in_commands = False
                continue
            # Skip empty/header lines but don't break
            if not line.strip():
                continue
            # Format B: "  name:  description" (Cobra style)
            m = re.match(r"^\s{2,}([\w][\w-]*):\s+(.+)$", line)
            if m:
                meta.commands.append(Command(
                    name=m.group(1), description=m.group(2).strip(),
                ))
                continue
            # Format A: "  command_name   description text" (argparse)
            m = re.match(r"^\s{2,}(\w[\w-]*)\s{2,}(.+)$", line)
            if m:
                meta.commands.append(Command(
                    name=m.group(1), description=m.group(2).strip(),
                ))
                continue

    # Extract options
    in_options = False
    for line in lines:
        lower = line.strip().lower()
        if lower.startswith(("options:", "flags:", "optional arguments:")):
            in_options = True
            continue
        if in_options:
            if not line.strip():
                in_options = False
                continue
            # Match "  -f, --flag VALUE   description (default: X)"
            m = re.match(
                r"^\s{2,}(-[\w,\s-]+(?:\s+\w+)?)\s{2,}(.+)$", line,
            )
            if m:
                flags = m.group(1).strip()
                desc = m.group(2).strip()
                default = None
                dm = re.search(r"\(default[:\s]+([^)]+)\)", desc, re.I)
                if dm:
                    default = dm.group(1).strip()
                meta.global_options.append(Option(
                    flags=flags, description=desc, default=default,
                ))

    return meta


def parse_subcommand_help(executable: str, meta: CLIMetadata) -> CLIMetadata:
    """Enrich commands by running `executable subcommand --help` for each."""
    for cmd in meta.commands:
        text = run_help(executable, [cmd.name])
        # Parse options specific to this subcommand
        in_options = False
        for line in text.splitlines():
            lower = line.strip().lower()
            if lower.startswith(("options:", "flags:", "optional arguments:")):
                in_options = True
                continue
            if in_options:
                if not line.strip():
                    in_options = False
                    continue
                m = re.match(
                    r"^\s{2,}(-[\w,\s-]+(?:\s+\w+)?)\s{2,}(.+)$", line,
                )
                if m:
                    flags = m.group(1).strip()
                    desc = m.group(2).strip()
                    default = None
                    dm = re.search(r"\(default[:\s]+([^)]+)\)", desc, re.I)
                    if dm:
                        default = dm.group(1).strip()
                    cmd.options.append(Option(
                        flags=flags, description=desc, default=default,
                    ))

        # Parse positional arguments
        in_positional = False
        for line in text.splitlines():
            lower = line.strip().lower()
            if lower.startswith("positional arguments:"):
                in_positional = True
                continue
            if in_positional:
                if not line.strip() or line.strip().lower().startswith(("options:", "flags:")):
                    in_positional = False
                    continue
                m = re.match(r"^\s{2,}(\w[\w-]*)\s{2,}(.+)$", line)
                if m:
                    cmd.arguments.append(Argument(
                        name=m.group(1), description=m.group(2).strip(),
                    ))

    return meta
