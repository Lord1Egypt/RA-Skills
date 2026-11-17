#!/usr/bin/env python3
"""Measure always-loaded instruction context without exposing its contents.

Character-only estimation is the safe default. Exact token counts require an
explicit trusted loopback HTTP endpoint for the current run; inherited endpoint
settings are intentionally ignored. Reports name the files, sections and path
prefixes an operator needs in order to act, and redact the absolute workspace
path and the text of duplicated instruction lines unless --show-content is set.
"""

import argparse
import ipaddress
import json
import re
import sys
import urllib.request
from pathlib import Path
from urllib.parse import urlparse

DEFAULT_BOOTSTRAP = ["AGENTS.md", "MEMORY.md", "SECURITY.md", "SOUL.md", "USER.md", "IDENTITY.md"]
DEFAULT_PER_FILE_LIMIT = 20000
DEFAULT_TOTAL_LIMIT = 60000
FALLBACK_CHARS_PER_TOKEN = 4.5


def validate_loopback_url(url):
    if not url:
        return ""
    try:
        parsed = urlparse(url)
        _ = parsed.port
        address = ipaddress.ip_address(parsed.hostname or "")
    except (ValueError, TypeError):
        raise ValueError("tokenizer URL must use a literal loopback IP address")
    if parsed.scheme not in {"http", "https"}:
        raise ValueError("tokenizer URL scheme must be http or https")
    if not address.is_loopback or parsed.username or parsed.password or parsed.fragment:
        raise ValueError("tokenizer URL must be a credential-free loopback endpoint")
    return url


class Tokenizer:
    def __init__(self, url, model):
        self.url, self.model, self.ok = url, model, False
        self.opener = urllib.request.build_opener(urllib.request.ProxyHandler({}))
        if url:
            self.ok = self.count("probe") is not None

    def count(self, text):
        if not self.url:
            return None
        payload = json.dumps({"model": self.model, "content": text}).encode()
        request = urllib.request.Request(
            self.url,
            data=payload,
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        try:
            with self.opener.open(request, timeout=30) as response:
                if response.status < 200 or response.status >= 300:
                    return None
                body = response.read(8_000_000)
            return len(json.loads(body)["tokens"])
        except Exception:
            return None

    def estimate(self, text):
        count = self.count(text) if self.ok else None
        return (count, True) if count is not None else (round(len(text) / FALLBACK_CHARS_PER_TOKEN), False)


def sections(text):
    """Split Markdown into H2 sections as (name, body) pairs."""
    marks = [(match.group(1), match.start()) for match in re.finditer(r"^## (.+)$", text, re.M)]
    result = []
    for index, (name, start) in enumerate(marks):
        end = marks[index + 1][1] if index + 1 < len(marks) else len(text)
        result.append((name, text[start:end]))
    return result


def repeated_prefixes(text, min_len=10, min_count=3):
    """Find path-like prefixes repeated often enough to merit consolidation."""
    paths = re.findall(r"`?([A-Za-z0-9_.\-]+/[A-Za-z0-9_./\-]*)`?", text)
    prefixes = {}
    for path in paths:
        parts = path.split("/")
        for index in range(1, len(parts)):
            prefix = "/".join(parts[:index]) + "/"
            if len(prefix) >= min_len:
                prefixes[prefix] = prefixes.get(prefix, 0) + 1
    return sorted(
        ((prefix, count) for prefix, count in prefixes.items() if count >= min_count),
        key=lambda item: -item[1] * len(item[0]),
    )


def duplicate_lines(files):
    """Return locations for substantive duplicated lines."""
    seen = {}
    for name, text in files.items():
        for line_number, line in enumerate(text.splitlines(), 1):
            normalized = line.strip().lstrip("-*0123456789. ").strip()
            if len(normalized) < 25 or normalized.startswith(("#", "|", "```")):
                continue
            seen.setdefault(normalized, []).append((name, line_number))
    return [
        (line, locations)
        for line, locations in seen.items()
        if len({name for name, _ in locations}) > 1
    ]


def safe_file(workspace, name):
    relative = Path(name)
    if relative.is_absolute() or not relative.parts or ".." in relative.parts:
        raise ValueError("file names must be relative paths inside the workspace")
    candidate = workspace / relative
    current = workspace
    for part in relative.parts:
        current = current / part
        if current.is_symlink():
            raise ValueError("symlinked inputs are not allowed")
    if not candidate.exists():
        return None
    resolved = candidate.resolve(strict=True)
    try:
        resolved.relative_to(workspace)
    except ValueError:
        raise ValueError("input escapes the workspace")
    if not resolved.is_file():
        raise ValueError("input is not a regular file")
    return resolved


def visible(value, label, show_content):
    """Hide instruction-derived text and host identity unless asked."""
    return value if show_content else label


def identifier(value, label, show_content):
    """Names an operator must see to act on the report.

    Bootstrap file names and markdown headings are structure, not content, and
    the report cannot be acted on without them. Absolute paths and the text of
    instruction lines stay under `visible`.
    """
    return value


def main():
    parser = argparse.ArgumentParser(description="Audit the always-loaded context budget.")
    parser.add_argument("--workspace", default=".")
    parser.add_argument("--files", nargs="*", default=DEFAULT_BOOTSTRAP)
    parser.add_argument("--per-file-limit", type=int, default=DEFAULT_PER_FILE_LIMIT)
    parser.add_argument("--total-limit", type=int, default=DEFAULT_TOTAL_LIMIT)
    parser.add_argument("--tokenizer-url", default="")
    parser.add_argument("--tokenizer-model", default="")
    parser.add_argument("--sections", action="store_true", help="break each file down by H2 section")
    parser.add_argument("--json", action="store_true")
    parser.add_argument(
        "--show-content",
        action="store_true",
        help="also show the absolute workspace path and the text of duplicated lines; keep output local",
    )
    args = parser.parse_args()

    if args.per_file_limit <= 0 or args.total_limit <= 0:
        parser.error("limits must be positive")
    if len(set(args.files)) != len(args.files):
        parser.error("file names must be unique")
    try:
        tokenizer_url = validate_loopback_url(args.tokenizer_url)
    except ValueError as error:
        parser.error(str(error))
    try:
        workspace = Path(args.workspace).expanduser().resolve(strict=True)
    except OSError:
        parser.error("unable to resolve workspace" if not args.show_content else "unable to resolve workspace: %s" % args.workspace)
    if tokenizer_url and not args.tokenizer_model:
        parser.error("--tokenizer-model is required with --tokenizer-url")
    if not workspace.is_dir():
        parser.error("workspace must be a directory")

    tokenizer = Tokenizer(tokenizer_url, args.tokenizer_model)
    file_labels = {
        name: identifier(name, "<file-%d>" % index, args.show_content)
        for index, name in enumerate(args.files, 1)
    }
    report = {
        "workspace": str(workspace) if args.show_content else "<workspace>",
        "exact_tokens": False,
        "tokenizer_model": args.tokenizer_model if tokenizer_url else None,
        "files": [],
        "findings": [],
    }

    total_chars = total_tokens = 0
    all_exact = tokenizer.ok
    texts = {}
    for name in args.files:
        label = file_labels[name]
        try:
            file_path = safe_file(workspace, name)
        except ValueError as error:
            parser.error(str(error))
        if file_path is None:
            continue
        try:
            text = file_path.read_text(errors="replace")
        except OSError:
            parser.error("unable to read a selected input")
        texts[name] = text
        chars = len(text)
        tokens, exact = tokenizer.estimate(text)
        all_exact = all_exact and exact
        total_chars += chars
        total_tokens += tokens
        entry = {
            "file": label,
            "chars": chars,
            "tokens": tokens,
            "token_count": "exact" if exact else "estimated",
            "truncated": chars > args.per_file_limit,
        }
        if args.sections:
            section_entries = []
            for section_index, (section_name, body) in enumerate(sections(text), 1):
                section_tokens, section_exact = tokenizer.estimate(body)
                all_exact = all_exact and section_exact
                section_entries.append({
                    "name": identifier(section_name, "<section-%d>" % section_index, args.show_content),
                    "chars": len(body),
                    "tokens": section_tokens,
                    "token_count": "exact" if section_exact else "estimated",
                })
            entry["sections"] = section_entries
        report["files"].append(entry)
        if chars > args.per_file_limit:
            report["findings"].append(
                "%s exceeds the per-file limit by %d characters" % (label, chars - args.per_file_limit)
            )

    report["exact_tokens"] = bool(report["files"]) and all_exact
    report["total_chars"] = total_chars
    report["total_tokens"] = total_tokens
    if total_chars > args.total_limit:
        report["findings"].append(
            "the set exceeds the total limit by %d characters" % (total_chars - args.total_limit)
        )

    joined = "\n".join(texts.values())
    report["repeated_prefixes"] = [
        {
            "prefix": identifier(prefix, "<prefix-%d>" % index, args.show_content),
            "count": count,
            "chars": count * len(prefix),
        }
        for index, (prefix, count) in enumerate(repeated_prefixes(joined)[:8], 1)
    ]
    report["duplicate_lines"] = [
        {
            "line": visible(line, "<line-%d>" % index, args.show_content),
            "locations": [
                {"file": file_labels[name], "line": number}
                for name, number in locations
            ],
        }
        for index, (line, locations) in enumerate(duplicate_lines(texts)[:15], 1)
    ]

    if args.json:
        print(json.dumps(report, indent=2))
        return 0

    print("Always-loaded context budget — %s" % report["workspace"])
    if report["exact_tokens"]:
        print("(all token counts exact; tokenizer model: %s)" % report["tokenizer_model"])
    elif report["tokenizer_model"]:
        print("(some token counts estimated at %.1f chars/token; tokenizer model: %s)" % (FALLBACK_CHARS_PER_TOKEN, report["tokenizer_model"]))
    else:
        print("(all token counts estimated at %.1f chars/token)" % FALLBACK_CHARS_PER_TOKEN)
    print()
    print("%-16s %8s %8s  %s" % ("file", "chars", "tokens", ""))
    for entry in report["files"]:
        flag = "  TRUNCATED, %d chars dropped" % (entry["chars"] - args.per_file_limit) if entry["truncated"] else ""
        print("%-16s %8d %8d%s" % (entry["file"], entry["chars"], entry["tokens"], flag))
    print("%-16s %8d %8d" % ("TOTAL", total_chars, total_tokens))

    if report["repeated_prefixes"]:
        print("\nRepeated path prefixes:")
        for prefix in report["repeated_prefixes"]:
            print("  %-24s x%-3d = %d chars" % (prefix["prefix"], prefix["count"], prefix["chars"]))
    if report["duplicate_lines"]:
        print("\nLines duplicated across files:")
        for duplicate in report["duplicate_lines"]:
            places = ", ".join("%s:%d" % (item["file"], item["line"]) for item in duplicate["locations"])
            print("  %s in %s" % (duplicate["line"], places))
    if args.sections:
        print("\nPer-section cost:")
        for entry in report["files"]:
            print("\n  %s" % entry["file"])
            for section in sorted(entry.get("sections", []), key=lambda item: -item["tokens"])[:12]:
                print("    %-30s %6d ch %6d tok" % (section["name"], section["chars"], section["tokens"]))
    if report["findings"]:
        print("\nFindings:")
        for finding in report["findings"]:
            print("  - %s" % finding)
    return 0


if __name__ == "__main__":
    sys.exit(main())
