#!/usr/bin/env python3
"""cli-hub — CLI Registry — unified management for external CLI tools.

Reads/writes lightweight JSON registry entries. Powers the cli-hub AgentSkill.
Compatible with OpenClaw, Claude Code, Codex CLI, Cursor, Aider.

Usage:
    python3 cli-registry.py register <name> [--binary <bin>] [--desc <text>]
    python3 cli-registry.py list [--format json]
    python3 cli-registry.py lookup <name>
    python3 cli-registry.py discover [--scan-path <dir>]
    python3 cli-registry.py remove <name>
    python3 cli-registry.py help <name>
    python3 cli-registry.py search <keyword...>
    python3 cli-registry.py --version
"""

import json
import os
import re
import sys
import argparse
import subprocess
from datetime import datetime
from pathlib import Path

VERSION = "1.2.0"
REGISTRY_DIR = Path.home() / ".openclaw" / "cli-registry"
SKILLS_DIR = Path.home() / ".agents" / "skills"
KEYWORD_INDEX_PATH = REGISTRY_DIR / ".keywords.json"

# ── P0: Knowledge base ──────────────────────────────────────────
# Built-in descriptions, keywords, and categories.
# Priority: built-in desc > --help summary > "External CLI: <name>"

KNOWN_CLI_KB = {
    # ── data processing ──
    "jq": {
        "desc": "Lightweight command-line JSON processor — filter, transform, and query JSON data",
        "keywords": ["json", "filter", "transform", "query", "parse", "extract", "select", "map", "reduce"],
        "category": "data-processing",
    },
    "yq": {
        "desc": "YAML/JSON/XML processor — jq wrapper for YAML with similar syntax",
        "keywords": ["yaml", "json", "xml", "filter", "transform", "query", "parse", "convert"],
        "category": "data-processing",
    },
    "sed": {
        "desc": "Stream editor for filtering and transforming text",
        "keywords": ["text", "filter", "replace", "substitute", "transform", "stream", "edit"],
        "category": "text-processing",
    },
    "awk": {
        "desc": "Pattern scanning and text processing language",
        "keywords": ["text", "pattern", "scan", "column", "field", "parse", "report", "transform"],
        "category": "text-processing",
    },
    "grep": {
        "desc": "Print lines matching a pattern — search text with regex",
        "keywords": ["search", "text", "regex", "pattern", "match", "find", "grep", "filter"],
        "category": "text-processing",
    },
    "rg": {
        "desc": "ripgrep — recursively search directories for regex patterns (fast grep alternative)",
        "keywords": ["search", "text", "regex", "pattern", "match", "find", "grep", "ripgrep", "recursive"],
        "category": "text-processing",
    },
    "fd": {
        "desc": "Simple, fast file search — find entries in the filesystem (find alternative)",
        "keywords": ["search", "file", "find", "locate", "filesystem", "directory"],
        "category": "file-management",
    },
    "find": {
        "desc": "Search for files in a directory hierarchy",
        "keywords": ["search", "file", "find", "locate", "filesystem", "directory", "recursive"],
        "category": "file-management",
    },
    "xargs": {
        "desc": "Build and execute command lines from standard input",
        "keywords": ["pipe", "batch", "execute", "argument", "stdin", "parallel"],
        "category": "text-processing",
    },
    "wc": {
        "desc": "Print newline, word, and byte counts for each file",
        "keywords": ["count", "lines", "words", "bytes", "file", "statistics"],
        "category": "text-processing",
    },
    "sort": {
        "desc": "Sort lines of text files",
        "keywords": ["sort", "order", "lines", "text", "alphabetical", "numeric"],
        "category": "text-processing",
    },
    "uniq": {
        "desc": "Report or omit repeated lines",
        "keywords": ["unique", "duplicate", "lines", "text", "count", "filter"],
        "category": "text-processing",
    },
    "cut": {
        "desc": "Remove sections from each line of files — extract columns",
        "keywords": ["columns", "fields", "delimiter", "extract", "text", "csv"],
        "category": "text-processing",
    },

    # ── version control ──
    "git": {
        "desc": "Fast, scalable, distributed revision control system",
        "keywords": ["version", "control", "commit", "branch", "merge", "clone", "push", "pull", "diff"],
        "category": "version-control",
    },
    "gh": {
        "desc": "GitHub CLI — manage repositories, PRs, issues from the terminal",
        "keywords": ["github", "pr", "pull request", "issue", "repo", "repository", "release", "gist", "codespace"],
        "category": "version-control",
    },

    # ── containers ──
    "docker": {
        "desc": "Container platform — build, run, and manage containers",
        "keywords": ["container", "image", "docker", "build", "run", "compose", "deploy", "registry"],
        "category": "containers",
    },
    "kubectl": {
        "desc": "Kubernetes CLI — deploy and manage containerized applications on clusters",
        "keywords": ["kubernetes", "k8s", "cluster", "deploy", "pod", "service", "container", "orchestration"],
        "category": "containers",
    },
    "helm": {
        "desc": "Kubernetes package manager — install and manage Helm charts",
        "keywords": ["kubernetes", "k8s", "chart", "package", "deploy", "install", "template"],
        "category": "containers",
    },

    # ── networking ──
    "curl": {
        "desc": "Transfer data from or to a server — HTTP/HTTPS/FTP/Gopher client",
        "keywords": ["http", "https", "download", "api", "request", "rest", "web", "url", "ftp", "post", "get"],
        "category": "networking",
    },
    "wget": {
        "desc": "Non-interactive network downloader — retrieve files via HTTP/HTTPS/FTP",
        "keywords": ["download", "http", "https", "ftp", "mirror", "recursive", "web", "file"],
        "category": "networking",
    },
    "ssh": {
        "desc": "OpenSSH remote login client — securely connect to remote machines",
        "keywords": ["ssh", "remote", "login", "shell", "secure", "tunnel", "connect", "key"],
        "category": "networking",
    },
    "scp": {
        "desc": "Secure copy — transfer files between hosts over SSH",
        "keywords": ["copy", "transfer", "remote", "secure", "file", "ssh"],
        "category": "networking",
    },
    "rsync": {
        "desc": "Fast, versatile file copying tool — sync directories locally and remotely",
        "keywords": ["sync", "copy", "backup", "mirror", "transfer", "remote", "incremental"],
        "category": "networking",
    },
    "ping": {
        "desc": "Send ICMP ECHO_REQUEST to test network connectivity",
        "keywords": ["network", "connectivity", "latency", "test", "ping", "icmp"],
        "category": "networking",
    },
    "dig": {
        "desc": "DNS lookup utility — query DNS name servers",
        "keywords": ["dns", "domain", "lookup", "query", "nameserver", "resolve", "record"],
        "category": "networking",
    },
    "ss": {
        "desc": "Socket statistics — dump socket information (netstat replacement)",
        "keywords": ["socket", "network", "port", "connection", "tcp", "udp", "listen"],
        "category": "networking",
    },
    "ip": {
        "desc": "Show/manipulate routing, devices, policy routing, and tunnels",
        "keywords": ["network", "route", "interface", "address", "tunnel", "link", "ip"],
        "category": "networking",
    },

    # ── media ──
    "ffmpeg": {
        "desc": "Complete solution for recording, converting, and streaming audio/video",
        "keywords": ["video", "audio", "convert", "encode", "decode", "media", "stream", "compress", "transcode"],
        "category": "media",
    },
    "convert": {
        "desc": "ImageMagick — convert between image formats, resize, apply effects",
        "keywords": ["image", "convert", "resize", "format", "png", "jpg", "gif", "crop", "rotate"],
        "category": "media",
    },

    # ── languages / runtimes ──
    "python3": {
        "desc": "Python 3 interpreter and scripting language",
        "keywords": ["python", "script", "programming", "language", "interpreter", "run"],
        "category": "languages",
    },
    "node": {
        "desc": "Node.js JavaScript runtime — run JavaScript outside the browser",
        "keywords": ["javascript", "js", "node", "runtime", "server", "script", "npm"],
        "category": "languages",
    },
    "npm": {
        "desc": "Node.js package manager — install and manage JavaScript packages",
        "keywords": ["package", "install", "node", "javascript", "dependency", "module", "registry"],
        "category": "languages",
    },
    "pnpm": {
        "desc": "Fast, disk-space efficient package manager for Node.js",
        "keywords": ["package", "install", "node", "javascript", "dependency", "fast"],
        "category": "languages",
    },
    "yarn": {
        "desc": "Fast, reliable, and secure dependency management for JavaScript",
        "keywords": ["package", "install", "node", "javascript", "dependency", "yarn"],
        "category": "languages",
    },
    "bun": {
        "desc": "All-in-one JavaScript runtime — bundler, test runner, package manager",
        "keywords": ["javascript", "runtime", "bundler", "test", "package", "fast"],
        "category": "languages",
    },
    "cargo": {
        "desc": "Rust package manager and build tool",
        "keywords": ["rust", "package", "build", "compile", "dependency", "project"],
        "category": "languages",
    },
    "go": {
        "desc": "Go programming language — compile, build, and run Go programs",
        "keywords": ["go", "golang", "compile", "build", "run", "format", "module"],
        "category": "languages",
    },
    "rustc": {
        "desc": "Rust compiler — compile Rust source code",
        "keywords": ["rust", "compile", "build", "language", "binary"],
        "category": "languages",
    },
    "make": {
        "desc": "GNU make — build automation tool",
        "keywords": ["build", "compile", "automation", "makefile", "target", "dependency"],
        "category": "build",
    },
    "cmake": {
        "desc": "Cross-platform build system generator",
        "keywords": ["build", "compile", "cmake", "makefile", "project", "configure"],
        "category": "build",
    },
    "gcc": {
        "desc": "GNU C compiler — compile C programs",
        "keywords": ["c", "compile", "build", "gcc", "linker", "binary"],
        "category": "build",
    },

    # ── databases ──
    "sqlite3": {
        "desc": "SQLite CLI — manage SQLite databases from the command line",
        "keywords": ["sql", "database", "sqlite", "query", "table", "select", "insert", "db"],
        "category": "databases",
    },
    "psql": {
        "desc": "PostgreSQL interactive terminal — query and manage PostgreSQL databases",
        "keywords": ["sql", "database", "postgresql", "postgres", "query", "table", "select", "psql"],
        "category": "databases",
    },

    # ── cloud ──
    "aws": {
        "desc": "AWS CLI — manage Amazon Web Services from the command line",
        "keywords": ["aws", "amazon", "cloud", "s3", "ec2", "lambda", "iam", "deploy"],
        "category": "cloud",
    },
    "gcloud": {
        "desc": "Google Cloud CLI — manage Google Cloud Platform resources",
        "keywords": ["google", "cloud", "gcp", "compute", "storage", "deploy", "iam"],
        "category": "cloud",
    },
    "az": {
        "desc": "Azure CLI — manage Microsoft Azure resources",
        "keywords": ["azure", "microsoft", "cloud", "vm", "storage", "deploy", "resource"],
        "category": "cloud",
    },
    "terraform": {
        "desc": "Infrastructure as Code — define and provision cloud infrastructure",
        "keywords": ["infrastructure", "iac", "cloud", "provision", "deploy", "state", "plan", "apply"],
        "category": "cloud",
    },

    # ── system ──
    "systemctl": {
        "desc": "Control the systemd system and service manager",
        "keywords": ["systemd", "service", "daemon", "start", "stop", "restart", "status", "enable"],
        "category": "system",
    },
    "journalctl": {
        "desc": "Query the systemd journal — view and filter logs",
        "keywords": ["log", "journal", "systemd", "debug", "error", "service", "boot"],
        "category": "system",
    },
    "htop": {
        "desc": "Interactive process viewer — monitor system resources",
        "keywords": ["process", "cpu", "memory", "monitor", "system", "resource", "interactive"],
        "category": "system",
    },
    "ncdu": {
        "desc": "NCurses Disk Usage — interactive disk usage analyzer",
        "keywords": ["disk", "usage", "space", "file", "directory", "size", "interactive"],
        "category": "system",
    },

    # ── compression / archive ──
    "tar": {
        "desc": "Tape archiver — create and extract archive files",
        "keywords": ["archive", "compress", "extract", "tar", "gz", "backup", "bundle"],
        "category": "archives",
    },
    "gzip": {
        "desc": "Compress or decompress files using Lempel-Ziv coding",
        "keywords": ["compress", "decompress", "gz", "file", "zip"],
        "category": "archives",
    },
    "unzip": {
        "desc": "List, test, and extract compressed files in a ZIP archive",
        "keywords": ["unzip", "extract", "archive", "zip", "decompress"],
        "category": "archives",
    },
    "zip": {
        "desc": "Package and compress files into a ZIP archive",
        "keywords": ["zip", "compress", "archive", "package", "bundle"],
        "category": "archives",
    },

    # ── other tools ──
    "fzf": {
        "desc": "Command-line fuzzy finder — filter lists interactively",
        "keywords": ["fuzzy", "find", "filter", "interactive", "search", "select", "picker", "menu"],
        "category": "interactive",
    },
    "bat": {
        "desc": "cat clone with syntax highlighting and Git integration",
        "keywords": ["view", "cat", "syntax", "highlight", "file", "preview", "pager"],
        "category": "file-management",
    },
    "eza": {
        "desc": "Modern replacement for ls — list files with colors and icons",
        "keywords": ["list", "directory", "file", "ls", "tree", "color"],
        "category": "file-management",
    },
    "opencli": {
        "desc": "OpenClaw CLI — manage the OpenClaw AI agent gateway",
        "keywords": ["openclaw", "agent", "ai", "gateway", "skill", "plugin"],
        "category": "ai-tools",
    },
    "code": {
        "desc": "Visual Studio Code editor — open files, folders, and manage extensions",
        "keywords": ["editor", "code", "vscode", "ide", "file", "diff", "extension"],
        "category": "editors",
    },
    "mihomo": {
        "desc": "Clash meta kernel — proxy and network routing (official skill exists)",
        "keywords": ["proxy", "mihomo", "clash", "vpn", "node", "routing", "network", "switch"],
        "category": "networking",
    },
    "mmx": {
        "desc": "MiniMax multimodal AI toolkit — generate images, video, music, documents",
        "keywords": ["ai", "minimax", "generate", "image", "video", "music", "document", "multimodal"],
        "category": "ai-tools",
    },
}

# Common shell/Unix utilities to skip during PATH scanning
UNIX_BASICS = {
    "[", "alias", "apt", "apt-get", "arch", "bash", "bg", "bind", "builtin",
    "bunzip2", "bzcat", "bzip2", "cal", "case", "cat", "cd", "chgrp",
    "chmod", "chown", "clear", "cmp", "comm", "command", "compgen", "cp",
    "cpio", "csplit", "cut", "dash", "date", "dd", "declare", "df", "diff",
    "dir", "dircolors", "dirname", "dirs", "dmidecode", "dmesg", "done",
    "dpkg", "du", "echo", "ed", "egrep", "elif", "else", "enable", "env",
    "eval", "exec", "exit", "expand", "export", "expr", "factor", "false",
    "fc", "fg", "fgrep", "fi", "file", "findmnt", "fmt", "fold", "for",
    "free", "function", "getopt", "getopts", "groups", "gunzip", "gzip",
    "hash", "head", "history", "hostid", "hostname", "id", "if", "info",
    "install", "jobs", "join", "kill", "ld", "ldd", "less", "let", "link",
    "ln", "local", "locale", "logger", "login", "logname", "logout", "lp",
    "ls", "lscpu", "lsblk", "lsof", "man", "mapfile", "md5sum", "mkdir",
    "mkfifo", "mknod", "mktemp", "more", "mount", "mpstat", "mv", "namei",
    "newgrp", "nice", "nl", "nohup", "nproc", "od", "paste", "pip", "pip3",
    "popd", "pr", "printenv", "printf", "ps", "pushd", "pwd", "python",
    "read", "readarray", "readlink", "realpath", "rename", "renice", "rev",
    "rm", "rmdir", "run-parts", "sdiff", "select", "seq", "set", "sh",
    "sha1sum", "sha256sum", "shift", "shopt", "shred", "shuf", "sleep",
    "sort", "source", "split", "stat", "stdbuf", "strings", "strip", "stty",
    "su", "sudo", "sum", "suspend", "sync", "tac", "tail", "tee", "test",
    "time", "timeout", "times", "touch", "tput", "tr", "trap", "true",
    "truncate", "tset", "tsort", "tty", "type", "typeset", "ulimit",
    "umask", "umount", "unalias", "uname", "unexpand", "uniq", "unlink",
    "unset", "until", "updatedb", "uptime", "users", "vi", "vim", "wait",
    "wall", "watch", "w", "whatis", "whereis", "which", "while", "who",
    "whoami", "write", "xdg-open", "yes", "zcat", "zless", "zmore",
}

# Flattened set of known binary names (for quick lookup in discover)
_KNOWN_BINARIES = set(KNOWN_CLI_KB.keys())


# ── helpers ────────────────────────────────────────────────────

def _run(cmd, timeout=10):
    try:
        r = subprocess.run(
            cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            universal_newlines=True, timeout=timeout
        )
        return r.returncode, r.stdout, r.stderr
    except FileNotFoundError:
        return -1, "", "binary not found: {}".format(cmd[0])
    except subprocess.TimeoutExpired:
        return -2, "", "timed out"


def _whereis(binary):
    return subprocess.call(["which", binary],
                           stdout=subprocess.DEVNULL,
                           stderr=subprocess.DEVNULL) == 0


def _find_official_skill(name):
    for root in [SKILLS_DIR, Path.home() / ".openclaw" / "skills"]:
        sp = root / name / "SKILL.md"
        if sp.is_file():
            with open(sp, encoding="utf-8") as fh:
                head = fh.read(500)
            if head.startswith("---") and "name:" in head:
                return str(sp)
    return None


# ── help extraction ─────────────────────────────────────────────

def _fetch_help_text(binary, subcommand=None):
    """Get help text trying --help, -h, help, man, bare invocation."""
    if subcommand:
        attempts = [
            [binary, subcommand, "-h"],
            [binary, subcommand, "--help"],
            [binary, "help", subcommand],
        ]
    else:
        attempts = [
            [binary, "--help"],
            [binary, "-h"],
            [binary, "help"],
        ]

    for cmd in attempts:
        code, out, err = _run(cmd, timeout=15)
        output = (out + err).strip()
        if len(output) > 80:
            return output

    # man page fallback
    code, out, err = _run(["man", binary], timeout=10)
    if len(out.strip()) > 80:
        return out.strip()[:16384]

    # bare invocation
    code, out, err = _run([binary], timeout=10)
    output = (out + err).strip()
    return output if output else ""


def _fetch_version(binary):
    """Extract version from --version output.

    Handles: "git version 2.17.1", "gh version 2.92.0",
    "curl 7.58.0", "v22.14.0", "Python 3.6.9", "mihomo-cli v2.8.1"
    """
    try:
        code, out, err = _run([binary, "--version"], timeout=5)
        output = (out + err).strip()
        if not output:
            code, out, err = _run([binary, "-V"], timeout=5)
            output = (out + err).strip()
        if output:
            m = re.search(r'\d+\.\d+(?:\.\d+)?(?:[a-z]\d*)?', output)
            if m:
                return m.group(0)
    except Exception:
        pass
    return None


# ── P1: Smart summary extraction ────────────────────────────────

def _extract_summary(text):
    """Extract a one-line tool description from --help output.

    Strategy (first to succeed wins):
      1. Find the NAME / DESCRIPTION section heading and grab the next line
      2. Find the first sentence after the usage block
      3. Find the first substantial non-flag line
    Returns None if nothing useful found.
    """
    if not text or len(text) < 20:
        return None

    lines = [l.strip() for l in text.split("\n")]

    # Strategy 1: NAME or DESCRIPTION section
    in_target = False
    for i, line in enumerate(lines):
        lo = line.lower().rstrip(":")
        if lo in ("name", "description", "overview"):
            in_target = True
            continue
        if in_target and len(line) > 15 and not line.startswith("-"):
            # Grab up to the next blank or heading
            parts = []
            for j in range(i, min(i + 8, len(lines))):
                l2 = lines[j].strip()
                if not l2 or l2.endswith(":") or l2.startswith("-"):
                    break
                parts.append(l2)
            if parts:
                return " ".join(parts)[:300]
            return line[:200]
        if in_target and (line == "" or line.startswith("-")):
            continue

    # Strategy 2: first sentence-like line after skipping usage/options blurb
    for i, line in enumerate(lines):
        if len(line) < 15:
            continue
        lo = line.lower()
        # Skip boilerplate
        if any(lo.startswith(w) for w in ("usage", "用法", "使い方", "usage:", "用法:", "使い方:")):
            continue
        if lo.startswith("-") and ("--" in line or "-" in line[:3]):
            continue
        # Look for a substantive line
        if re.match(r'^[A-Z]', line) and len(line) > 20:
            # Stop at next blank or flag line
            return line[:300]

    # Strategy 3: any substantial non-flag line
    for line in lines:
        if len(line) > 20 and not line.startswith("-") and not line.startswith("#"):
            return line[:200]

    return None


def _clean_help_raw(text):
    """Prepare help text for LLM consumption.

    - Strip version/copyright headers
    - Remove excessive blank lines
    - Keep first 5000 chars (the useful part is always at the top)
    """
    lines = text.split("\n")
    cleaned = []
    skip_header = True
    for line in lines:
        s = line.strip()
        # Skip version/copyright noise at the top
        if skip_header:
            if any(w in s.lower() for w in ("version", "copyright", "license",
                   "all rights reserved", "maintainer", "built on", "contributors")):
                continue
            if s and len(s) < 80 and not s.startswith("-"):
                skip_header = False
        cleaned.append(line)
    result = "\n".join(cleaned).strip()
    # Deduplicate blank lines
    import re as _re
    result = _re.sub(r'\n{3,}', '\n\n', result)
    return result[:5000]


def _format_commands_text(parsed_subs):
    """Build a compact command summary for LLM consumption."""
    if not parsed_subs:
        return ""
    lines = []
    for s in parsed_subs[:20]:
        name = s["name"]
        desc = s.get("desc", "")
        if desc:
            lines.append("{} — {}".format(name, desc))
        else:
            lines.append(name)
    return "\n".join(lines)


def _format_options_text(options):
    """Build a compact options summary for LLM consumption."""
    if not options:
        return ""
    lines = []
    for o in options[:15]:
        flag = o["flag"]
        aliases = ", ".join(o.get("aliases", []))
        label = "{} ({})".format(flag, aliases) if aliases else flag
        value = " <{}>".format(o["value"]) if o.get("value") else ""
        desc = o.get("desc", "")
        lines.append("{}{} — {}".format(label, value, desc))
    return "\n".join(lines)


def _extract_help(binary):
    """Extract structured help: usage, subcommands with options, global options."""
    text = _fetch_help_text(binary)
    if not text:
        return {"binary": binary, "help_raw": "{} — help unavailable".format(binary)}

    parsed_subs = _parse_subcommands(text)
    parsed_opts = _parse_options(text)

    result = {
        "binary": binary,
        "version": _fetch_version(binary),
        "help_raw": _clean_help_raw(text),
        "usage": _extract_usage(text),
        "summary": _extract_summary(text),
        "commands_text": _format_commands_text(parsed_subs),
        "options_text": _format_options_text(parsed_opts),
        "subcommands": {},
        "global_options": [],
    }

    top_subs = parsed_subs[:12]

    for s in top_subs:
        name = s["name"]
        sub_help = _fetch_help_text(binary, name)
        sub_info = {
            "desc": s["desc"],
            "usage": _extract_usage(sub_help) if sub_help else "",
            "options": _parse_options(sub_help) if sub_help else [],
        }
        result["subcommands"][name] = sub_info

    return result


def _extract_usage(text):
    """Extract usage line(s)."""
    lines = []
    in_usage = False
    for line in text.split("\n"):
        s = line.strip()
        if re.match(r'^(usage|用法|使用方式|使い方)\s*[:：]', s, re.I):
            in_usage = True
            continue
        if in_usage:
            if s == "" or re.match(r'^[A-Z][a-z]+(\s+[a-z]+)*\s*[:：]', s):
                break
            if len(s) > 5:
                lines.append(s)
    if not lines:
        for line in text.split("\n"):
            s = line.strip()
            if s and not s.startswith("#") and len(s) > 10:
                lines.append(s)
                break
    return "\n".join(lines[:5])


def _parse_subcommands(text):
    """Extract subcommands from indented help text."""
    subs = []
    seen = set()
    noise = {
        "or", "and", "the", "for", "see", "a", "an", "of", "to", "in",
        "usage", "options", "commands", "examples", "arguments", "flags",
        "help", "all", "on", "off", "yes", "no", "true", "false",
        "be", "is", "it", "if", "by", "at", "also", "note", "use",
        "after", "before", "with", "from", "into", "out", "up", "per",
    }
    for m in re.finditer(r'(?m)^\s{2,}([a-z][a-z0-9._-]{2,30})\s{2,}(.+)', text):
        name, desc = m.group(1), m.group(2).strip()[:150]
        name = name.rstrip("._")
        if name.lower() not in noise and name not in seen:
            seen.add(name)
            subs.append({"name": name, "desc": desc})
    return subs


def _parse_options(text):
    """Extract options/flags with types."""
    options = []
    seen = set()
    skip = {"-h", "--help", "-v", "--version", "-V"}
    for m in re.finditer(
        r'(?m)^\s{0,6}(-{1,2}[\w][\w-]*(?:,\s*-{1,2}[\w][\w-]*)?)'
        r'(?:\s+(?!-)\S+)?\s{2,}(.+)',
        text
    ):
        flag_group = m.group(1)
        desc = m.group(2).strip()[:120] if m.group(2) else ""
        flags = [f.strip() for f in flag_group.split(",")]
        primary = next((f for f in flags if f.startswith("--")), flags[0])
        if primary in skip:
            continue
        value = ""
        type_match = re.search(r'(?:<([^>]+)>|\[=?(.+?)\])', desc)
        if type_match:
            value = type_match.group(1) or type_match.group(2)
        if primary not in seen:
            seen.add(primary)
            options.append({
                "flag": primary,
                "aliases": [f for f in flags if f != primary],
                "value": value,
                "desc": desc[:100]
            })
    return options[:25]


# ── P2: Keyword index ───────────────────────────────────────────

def _build_keyword_index():
    """Build a reverse index: keyword → [tool names].

    Sources: built-in KNOWN_CLI_KB keywords, then fallback to description tokens.
    Stored as REGISTRY_DIR/.keywords.json.
    """
    index = {}

    # From knowledge base
    for name, kb in KNOWN_CLI_KB.items():
        for kw in kb.get("keywords", []):
            k = kw.lower()
            if k not in index:
                index[k] = []
            if name not in index[k]:
                index[k].append(name)

    # Supplement: extract keywords from registered tool descriptions
    for entry_path in sorted(REGISTRY_DIR.glob("*.json")):
        name = entry_path.stem
        if name.startswith("."):
            continue
        try:
            d = json.loads(entry_path.read_text(encoding="utf-8"))
        except Exception:
            continue
        desc = d.get("description", "")
        if not desc or desc.startswith("External CLI:"):
            continue
        # Tokenize description for additional keywords
        tokens = set(re.findall(r'[a-z0-9]{3,}', desc.lower()))
        noise = {"the", "and", "for", "with", "from", "into", "that", "this",
                 "tool", "command", "line", "cli", "external", "file"}
        for t in tokens - noise:
            if t not in index:
                index[t] = []
            if name not in index[t]:
                index[t].append(name)

    return index


def _save_keyword_index():
    """Save the keyword index to disk."""
    REGISTRY_DIR.mkdir(parents=True, exist_ok=True)
    index = _build_keyword_index()
    KEYWORD_INDEX_PATH.write_text(
        json.dumps(index, indent=2, ensure_ascii=False), encoding="utf-8")
    return len(index)


# ── commands ─────────────────────────────────────────────────────

def _resolve_description(name, help_text):
    """Resolve description with priority: KB > --help summary > fallback."""
    # P0: Built-in knowledge base
    kb = KNOWN_CLI_KB.get(name)
    if kb and kb.get("desc"):
        return kb["desc"]

    # P1: Smart extraction from --help
    summary = _extract_summary(help_text) if help_text else None
    if summary:
        return summary

    # Fallback
    return "External CLI: {}".format(name)


def _resolve_keywords(name):
    """Get keywords for a tool. Returns empty list if not in KB."""
    kb = KNOWN_CLI_KB.get(name)
    if kb:
        return kb.get("keywords", [])
    return []


def cmd_register(args):
    name = args.cli
    binary = args.binary or name
    desc = args.desc or ""

    if not args.force and not _whereis(binary):
        print("Warning: {} not found on PATH. Use --force to register anyway.".format(binary))

    official = _find_official_skill(name)
    info = _extract_help(binary)

    # P0+P1: smart description resolution
    description = desc or _resolve_description(name, info.get("help_raw", ""))

    # P0: keywords from knowledge base
    keywords = _resolve_keywords(name)

    entry = {
        "name": name,
        "binary": binary,
        "description": description,
        "official_skill": official,
        "registered_at": datetime.now().isoformat(),
        "keywords": keywords,
        "auto_discovered": info,
    }

    REGISTRY_DIR.mkdir(parents=True, exist_ok=True)
    path = REGISTRY_DIR / "{}.json".format(name)
    path.write_text(json.dumps(entry, indent=2, ensure_ascii=False), encoding="utf-8")

    print("Registered: {} -> {}".format(name, path))
    print("   {}".format(description[:80]))
    if official:
        print("   Official skill: {} (takes priority)".format(official))
    subs = info.get("subcommands", {})
    opts = info.get("global_options", [])
    print("   {} subcommands, {} options, {} keywords".format(
        len(subs), len(opts), len(keywords)))


def cmd_list(args):
    entries = [e for e in sorted(REGISTRY_DIR.glob("*.json")) if not e.name.startswith(".")]
    if not entries:
        print("No CLI tools registered.")
        print("Try: python3 cli-registry.py discover")
        return

    if args.format == "json":
        result = {}
        for e in entries:
            d = json.loads(e.read_text(encoding="utf-8"))
            ad = d.get("auto_discovered", {})
            result[d["name"]] = {
                "binary": d.get("binary"),
                "description": d.get("description"),
                "has_official_skill": bool(d.get("official_skill")),
                "subcommands": len(ad.get("subcommands", {})),
                "global_options": len(ad.get("global_options", [])),
                "keywords": d.get("keywords", []),
            }
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        header = "{:<18s} {:<13s} {:<8s} {:>4s} {:>4s} {:>3s}  {}".format(
            "NAME", "BINARY", "OFFICIAL", "SUBS", "OPTS", "KW", "DESCRIPTION")
        print(header)
        print("-" * 90)
        for e in entries:
            d = json.loads(e.read_text(encoding="utf-8"))
            official = "yes" if d.get("official_skill") else "-"
            ad = d.get("auto_discovered", {})
            subs = len(ad.get("subcommands", {}))
            opts = len(ad.get("global_options", []))
            kw_cnt = len(d.get("keywords", []))
            print("{:<18s} {:<13s} {:<8s} {:>4d} {:>4d} {:>3d}  {}".format(
                d["name"], d.get("binary", d["name"]),
                official, subs, opts, kw_cnt, d.get("description", "")[:35]))


def cmd_lookup(args):
    path = REGISTRY_DIR / "{}.json".format(args.cli)
    if not path.is_file():
        print("Not registered: {}".format(args.cli))
        print("  Try: python3 cli-registry.py register {}".format(args.cli))
        sys.exit(1)

    d = json.loads(path.read_text(encoding="utf-8"))

    print("# CLI: {}".format(d["name"]))
    print("Binary: {}".format(d.get("binary")))
    if d.get("description"):
        print("Description: {}".format(d["description"]))
    ad = d.get("auto_discovered", {})
    if ad.get("version"):
        print("Registered version: {}".format(ad["version"]))
        print("Official Skill: {} (takes priority)".format(d["official_skill"]))
    keywords = d.get("keywords", [])
    if keywords:
        print("Keywords: {}".format(", ".join(keywords)))

    ad = d.get("auto_discovered", {})

    summary = ad.get("summary")
    if summary:
        print("\n## Help Summary")
        print(summary)

    usage = ad.get("usage")
    if usage:
        print("\n## Usage")
        print("```")
        print(usage)
        print("```")

    globals_opts = ad.get("global_options", [])
    if globals_opts:
        print("\n## Global Options ({})".format(len(globals_opts)))
        for o in globals_opts[:10]:
            v = " <{}>".format(o["value"]) if o.get("value") else ""
            aliases = " ({})".format(", ".join(o["aliases"])) if o.get("aliases") else ""
            print("  {}{}  {} {}".format(o["flag"], v, o.get("desc", ""), aliases))

    subs = ad.get("subcommands", {})
    if subs:
        print("\n## Subcommands ({})".format(len(subs)))
        for name, info in subs.items():
            print("\n### {} — {}".format(name, info.get("desc", "")))
            sub_usage = info.get("usage")
            if sub_usage:
                print("  Usage: `{}`".format(sub_usage.split("\n")[0][:120]))
            sub_opts = info.get("options", [])
            if sub_opts:
                for o in sub_opts[:8]:
                    v = " <{}>".format(o["value"]) if o.get("value") else ""
                    print("    {} {}  {}".format(o["flag"], v, o.get("desc", "")[:60]))


def cmd_search(args):
    """Search registered tools by keyword."""
    keywords = [kw.lower() for kw in args.keyword]

    # Try to load the keyword index
    index = {}
    if KEYWORD_INDEX_PATH.is_file():
        try:
            index = json.loads(KEYWORD_INDEX_PATH.read_text(encoding="utf-8"))
        except Exception:
            pass

    # Also check individual registry entries
    hits = {}  # name → set of matched keywords

    # Search index
    for kw in keywords:
        matches = index.get(kw, [])
        for name in matches:
            if name not in hits:
                hits[name] = set()
            hits[name].add(kw)

    # Search entries directly (covers tools registered after last index build)
    for entry_path in sorted(REGISTRY_DIR.glob("*.json")):
        name = entry_path.stem
        if name.startswith("."):
            continue
        try:
            d = json.loads(entry_path.read_text(encoding="utf-8"))
        except Exception:
            continue

        # Check built-in keywords
        for kw in d.get("keywords", []):
            for qk in keywords:
                if qk in kw.lower():
                    if name not in hits:
                        hits[name] = set()
                    hits[name].add(qk)

        # Check description
        desc = d.get("description", "").lower()
        for qk in keywords:
            if qk in desc and name not in hits:
                hits[name] = set()
                hits[name].add(qk)

    if not hits:
        print("No tools found for: {}".format(", ".join(keywords)))
        print("Try: python3 cli-registry.py list")
        return

    # Sort by number of matched keywords (descending)
    sorted_hits = sorted(hits.items(), key=lambda x: len(x[1]), reverse=True)

    print("Search: {}".format(", ".join(keywords)))
    print("{:<18s} {:>4s}  {}".format("TOOL", "MATCH", "DESCRIPTION"))
    print("-" * 80)
    for name, matched in sorted_hits:
        entry_path = REGISTRY_DIR / "{}.json".format(name)
        desc = ""
        if entry_path.is_file():
            try:
                d = json.loads(entry_path.read_text(encoding="utf-8"))
                desc = d.get("description", "")[:55]
            except Exception:
                pass
        print("{:<18s} {:>4d}  {}".format(name, len(matched), desc))

    print("\n{} tools matched. Use 'lookup <name>' for details.".format(len(hits)))


def cmd_discover(args):
    count = 0

    # Phase 1: known list (from knowledge base)
    for binary in _KNOWN_BINARIES:
        if (REGISTRY_DIR / "{}.json".format(binary)).is_file():
            continue
        if _whereis(binary):
            print("Found: {} ...".format(binary), end=" ", flush=True)
            try:
                cmd_register(argparse.Namespace(
                    cli=binary, binary=binary, desc="", force=False))
                count += 1
            except Exception as exc:
                print("failed ({})".format(exc))

    # Phase 2: deep PATH scan
    if args.scan:
        print("\nScanning PATH for additional binaries...")
        seen = set(_KNOWN_BINARIES) | {
            e.stem for e in REGISTRY_DIR.glob("*.json")
        }
        for path_dir in os.environ.get("PATH", "").split(os.pathsep):
            d = Path(path_dir)
            if not d.is_dir():
                continue
            try:
                for entry in d.iterdir():
                    name = entry.name
                    if name in seen or name in UNIX_BASICS:
                        continue
                    if len(name) < 2 or len(name) > 30:
                        continue
                    if not re.match(r'^[a-z][a-z0-9._-]+$', name):
                        continue
                    if entry.is_file() and os.access(str(entry), os.X_OK):
                        seen.add(name)
                        print("Found: {} ...".format(name), end=" ", flush=True)
                        try:
                            cmd_register(argparse.Namespace(
                                cli=name, binary=str(entry), desc="", force=False))
                            count += 1
                        except Exception as exc:
                            print("failed ({})".format(exc))
            except PermissionError:
                continue

    # Phase 3: custom directory
    if args.scan_path:
        sp = Path(args.scan_path)
        if sp.is_dir():
            for f in sp.iterdir():
                if f.is_file() and os.access(str(f), os.X_OK):
                    name = f.name
                    if not (REGISTRY_DIR / "{}.json".format(name)).is_file():
                        print("Found: {} ...".format(name), end=" ", flush=True)
                        try:
                            cmd_register(argparse.Namespace(
                                cli=name, binary=str(f), desc="", force=False))
                            count += 1
                        except Exception as exc:
                            print("failed ({})".format(exc))

    # P2: Build keyword index after discovering
    if count > 0:
        kw_count = _save_keyword_index()
        print("\nKeyword index: {} terms".format(kw_count))

    print("\nRegistered {} new CLI tools.".format(count))


def cmd_remove(args):
    path = REGISTRY_DIR / "{}.json".format(args.cli)
    if path.is_file():
        path.unlink()
        print("Removed: {}".format(args.cli))
        # Rebuild keyword index
        _save_keyword_index()
    else:
        print("Not registered: {}".format(args.cli))


def cmd_help_cli(args):
    binary = args.cli
    p = REGISTRY_DIR / "{}.json".format(args.cli)
    if p.is_file():
        binary = json.loads(p.read_text(encoding="utf-8")).get("binary", binary)
    output = _fetch_help_text(binary)
    if output:
        print(output[:5000])
    else:
        print("No help output from {}".format(binary))


def cmd_check_stale(args):
    """Check for tools whose installed version differs from registry."""
    entries = [e for e in sorted(REGISTRY_DIR.glob("*.json")) if not e.name.startswith(".")]
    if not entries:
        print("No tools registered.")
        return

    stale = []
    current = 0
    for e in entries:
        try:
            d = json.loads(e.read_text(encoding="utf-8"))
        except Exception:
            continue
        name = d.get("name")
        binary = d.get("binary", name)
        ad = d.get("auto_discovered", {})
        registered_ver = ad.get("version")
        installed_ver = _fetch_version(binary)

        if installed_ver is None:
            continue

        current += 1
        if registered_ver and installed_ver != registered_ver:
            stale.append((name, registered_ver, installed_ver))

    print("{} tools with version info".format(current))
    if stale:
        print("{} stale (installed ≠ registered):\n".format(len(stale)))
        for name, old, new in stale:
            print("  {}: {} → {}".format(name, old, new))
        if args.update:
            print("\nRe-registering stale tools...")
            for name, old, new in stale:
                cmd_register(argparse.Namespace(
                    cli=name, binary=name, desc="", force=True))
            _save_keyword_index()
            print("Done.")
        else:
            print("\nDry run. Use --update to re-register.")
    else:
        print("All up to date.")

def main():
    parser = argparse.ArgumentParser(
        description="CLI Registry for cli-hub AgentSkill",
        prog="cli-registry")
    parser.add_argument("--version", action="version", version=VERSION)

    sub = parser.add_subparsers(dest="command")
    sub.required = True

    p = sub.add_parser("register", help="Register a CLI tool")
    p.add_argument("cli", help="CLI name")
    p.add_argument("--binary", help="Binary name if different")
    p.add_argument("--desc", help="Description (override auto-detection)")
    p.add_argument("--force", action="store_true",
                   help="Register even if binary not on PATH")

    p = sub.add_parser("list", help="List registered CLIs")
    p.add_argument("--format", default="table", choices=["table", "json"])

    p = sub.add_parser("lookup", help="Look up a CLI")
    p.add_argument("cli", help="CLI name")

    p = sub.add_parser("search", help="Search tools by keyword")
    p.add_argument("keyword", nargs="+", help="Keyword(s) to search for")

    p = sub.add_parser("discover", help="Auto-discover CLI binaries")
    p.add_argument("--scan", action="store_true",
                   help="Deep scan all PATH directories (slower, finds more)")
    p.add_argument("--scan-path", help="Extra directory to scan for executables")

    p = sub.add_parser("check-stale", help="Check for tools with updated versions")
    p.add_argument("--update", action="store_true",
                   help="Re-register tools whose version changed")

    p = sub.add_parser("remove", help="Remove from registry")
    p.add_argument("cli", help="CLI name")

    p = sub.add_parser("help", help="Fetch live --help output")
    p.add_argument("cli", help="CLI name or binary")

    args = parser.parse_args()
    {
        "register": cmd_register,
        "list": cmd_list,
        "lookup": cmd_lookup,
        "search": cmd_search,
        "discover": cmd_discover,
        "remove": cmd_remove,
        "help": cmd_help_cli,
        "check-stale": cmd_check_stale,
    }[args.command](args)


if __name__ == "__main__":
    main()
