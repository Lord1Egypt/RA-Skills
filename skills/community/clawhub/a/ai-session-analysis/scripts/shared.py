"""Shared utilities for AI session analysis scripts."""

from pathlib import Path


def strip_home_prefix(dirname):
    """Strip the HOME-derived prefix from a Claude Code project directory name.

    Claude Code encodes the project path in directory names like:
      -Users-qute-Program-SkillFab
    This strips the HOME portion, leaving:
      Program-SkillFab
    Works generically for any user on any OS.
    """
    sanitized = str(Path.home()).replace("\\", "/").lstrip("/").replace("/", "-")
    home_prefix = "-" + sanitized
    if dirname.startswith(home_prefix):
        return dirname[len(home_prefix):]
    return dirname


def classify_shell_cmd(cmd):
    """Categorize a shell command string. Pure string matching, no execution."""
    if not cmd:
        return "(empty)"
    if "git " in cmd or cmd.strip() == "git":
        return "git"
    if any(kw in cmd for kw in ["rg ", "grep ", "find ", "mdfind "]):
        return "grep/find"
    if any(kw in cmd for kw in ["npm ", "yarn ", "pnpm ", "npx "]):
        return "npm/yarn"
    if any(kw in cmd for kw in ["python", "pip ", "pytest"]):
        return "python"
    if any(kw in cmd for kw in ["cat ", "head ", "tail ", "sed ", "awk "]):
        return "view/read"
    if "ls " in cmd or cmd.strip() == "ls":
        return "ls"
    if "cd " in cmd or "pwd" == cmd.strip():
        return "cd/pwd"
    if any(kw in cmd for kw in ["curl ", "wget "]):
        return "network"
    if any(kw in cmd for kw in ["rm ", "cp ", "mv ", "mkdir ", "touch "]):
        return "fs_ops"
    return "other"
