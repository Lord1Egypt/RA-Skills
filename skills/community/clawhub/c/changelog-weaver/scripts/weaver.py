#!/usr/bin/env python3
"""
Changelog Weaver — parse git history into structured changelog data.

Reads git log for a specified tag/commit range, parses Conventional Commits,
classifies by type, deduplicates similar commits, and outputs structured JSON
ready for AI-powered semantic rewriting.

Usage:
    # Collect commits between two tags
    python3 scripts/weaver.py collect --from v2.3.0 --to v2.4.0

    # Collect commits since last tag
    python3 scripts/weaver.py collect --from-latest-tag

    # Collect commits from a date range
    python3 scripts/weaver.py collect --since "2026-06-01" --until "2026-06-15"

    # Output as JSON (for AI processing)
    python3 scripts/weaver.py collect --from v2.3.0 --to HEAD -o commits.json

    # Generate changelog preview directly
    python3 scripts/weaver.py generate --input commits.json --format changelog

    # List available formats
    python3 scripts/weaver.py formats
"""

import argparse
import json
import re
import subprocess
import sys
from collections import defaultdict
from datetime import datetime
from pathlib import Path

# ─── Conventional Commit Patterns ───

CC_PATTERN = re.compile(
    r'^(?P<type>build|chore|ci|docs|feat|fix|perf|refactor|style|test|revert|security|deps)'
    r'(?:\((?P<scope>[^)]*)\))?'
    r'(?P<breaking>!)?:\s*(?P<description>.+)$',
    re.IGNORECASE
)

BREAKING_FOOTER = re.compile(
    r'^BREAKING[-\s]CHANGE:\s*(?P<detail>.+)$',
    re.IGNORECASE | re.MULTILINE
)

MERGE_PATTERN = re.compile(r'^Merge\s+(pull\s+request\s+)?#?\d+', re.IGNORECASE)
REF_PATTERN = re.compile(r'(?:#|GH-)(\d+)')

# ─── Classification ───

TYPE_LABELS = {
    "feat":     {"category": "Features",       "emoji": "✨"},
    "fix":      {"category": "Bug Fixes",      "emoji": "🐛"},
    "perf":     {"category": "Performance",    "emoji": "⚡"},
    "refactor": {"category": "Refactoring",    "emoji": "♻️"},
    "docs":     {"category": "Documentation",  "emoji": "📝"},
    "style":    {"category": "Styling",        "emoji": "💄"},
    "test":     {"category": "Tests",          "emoji": "✅"},
    "chore":    {"category": "Chores",         "emoji": "🔧"},
    "build":    {"category": "Build System",   "emoji": "📦"},
    "ci":       {"category": "CI/CD",          "emoji": "🔄"},
    "revert":   {"category": "Reverts",        "emoji": "⏪"},
    "security": {"category": "Security",       "emoji": "🔒"},
    "deps":     {"category": "Dependencies",   "emoji": "⬆️"},
    "breaking": {"category": "Breaking Changes","emoji": "⚠️"},
}

CATEGORY_ORDER = [
    "breaking", "feat", "fix", "perf", "security",
    "refactor", "style", "test", "build", "ci",
    "docs", "deps", "chore", "revert",
]


def run_git(repo_path: str, args: list) -> str:
    """Run a git command and return stdout."""
    try:
        result = subprocess.run(
            ["git", "-C", repo_path] + args,
            capture_output=True, text=True, timeout=30,
        )
        if result.returncode != 0:
            print(f"[WARN] git {' '.join(args)} failed: {result.stderr.strip()}",
                  file=sys.stderr)
            return ""
        return result.stdout.strip()
    except FileNotFoundError:
        print("[ERROR] git not found. Is git installed?", file=sys.stderr)
        sys.exit(1)
    except subprocess.TimeoutExpired:
        print("[ERROR] git command timed out", file=sys.stderr)
        return ""


def collect_commits(repo_path: str, from_ref: str = None, to_ref: str = "HEAD",
                    since: str = None, until: str = None,
                    max_count: int = 500, include_merges: bool = False) -> list:
    """Collect commits from a git repository within the specified range."""
    fmt = "%H%n%an%n%ae%n%aI%n%s%n%b%n---COMMIT_END---"
    git_args = ["log", f"--format={fmt}", f"--max-count={max_count}"]

    if not include_merges:
        git_args.append("--no-merges")

    if since:
        git_args.append(f"--since={since}")
    if until:
        git_args.append(f"--until={until}")

    if from_ref and to_ref:
        git_args.append(f"{from_ref}..{to_ref}")
    elif from_ref:
        git_args.append(f"{from_ref}..HEAD")
    elif to_ref and to_ref != "HEAD":
        git_args.append(to_ref)

    raw = run_git(repo_path, git_args)
    if not raw:
        return []

    commits = []
    for block in raw.split("---COMMIT_END---"):
        block = block.strip()
        if not block:
            continue
        lines = block.split("\n", 5)
        if len(lines) < 5:
            continue

        hash_short = lines[0][:8]
        author = lines[1]
        email = lines[2]
        date = lines[3]
        subject = lines[4]
        body = lines[5] if len(lines) > 5 else ""

        cc_match = CC_PATTERN.match(subject)
        if cc_match:
            commit_type = cc_match.group("type").lower()
            scope = cc_match.group("scope") or ""
            has_breaking = bool(cc_match.group("breaking"))
            description = cc_match.group("description").strip()
        else:
            commit_type = "other"
            scope = ""
            has_breaking = False
            description = subject.strip()

        breaking_detail = ""
        if not has_breaking:
            bm = BREAKING_FOOTER.search(body)
            if bm:
                has_breaking = True
                breaking_detail = bm.group("detail").strip()

        refs = REF_PATTERN.findall(subject + " " + body)

        commits.append({
            "hash": lines[0],
            "hash_short": hash_short,
            "author": author,
            "email": email,
            "date": date,
            "subject": subject,
            "body": body.strip(),
            "type": commit_type,
            "scope": scope,
            "breaking": has_breaking,
            "breaking_detail": breaking_detail,
            "description": description,
            "references": list(set(refs)),
        })

    return commits


def collect_from_latest_tag(repo_path: str, max_count: int = 500) -> list:
    """Collect commits since the most recent tag."""
    latest_tag = run_git(repo_path, ["describe", "--tags", "--abbrev=0"])
    if not latest_tag:
        print("[WARN] No tags found. Collecting all commits.", file=sys.stderr)
        return collect_commits(repo_path, max_count=max_count)

    print(f"[INFO] Latest tag: {latest_tag}", file=sys.stderr)
    return collect_commits(repo_path, from_ref=latest_tag, max_count=max_count)


def deduplicate_commits(commits: list, similarity_threshold: float = 0.7) -> list:
    """Merge adjacent commits of the same type with high description overlap."""
    if len(commits) <= 1:
        return commits

    def tokenize(text: str) -> set:
        return set(re.findall(r'\w+', text.lower()))

    def similarity(a: str, b: str) -> float:
        tokens_a = tokenize(a)
        tokens_b = tokenize(b)
        if not tokens_a or not tokens_b:
            return 0.0
        intersection = tokens_a & tokens_b
        return len(intersection) / min(len(tokens_a), len(tokens_b))

    merged = []
    skip = set()

    for i, commit in enumerate(commits):
        if i in skip:
            continue

        group = [commit]
        for j in range(i + 1, min(i + 10, len(commits))):
            if j in skip:
                continue
            if commits[j]["type"] == commit["type"]:
                sim = similarity(commit["description"], commits[j]["description"])
                if sim >= similarity_threshold:
                    group.append(commits[j])
                    skip.add(j)

        if len(group) == 1:
            merged.append(commit)
        else:
            base = group[0].copy()
            all_refs = set()
            all_authors = set()
            for g in group:
                all_refs.update(g["references"])
                all_authors.add(g["author"])
            base["references"] = sorted(all_refs)
            base["authors"] = sorted(all_authors)
            base["count"] = len(group)
            merged.append(base)

    return merged


def group_by_category(commits: list) -> dict:
    """Group commits by Conventional Commit category."""
    grouped = defaultdict(list)
    for c in commits:
        if c.get("breaking"):
            grouped["breaking"].append(c)
        grouped[c["type"]].append(c)

    ordered = {}
    for cat in CATEGORY_ORDER:
        if cat in grouped:
            ordered[cat] = grouped[cat]
    for cat in grouped:
        if cat not in ordered:
            ordered[cat] = grouped[cat]
    return ordered


def compute_stats(commits: list, grouped: dict) -> dict:
    """Compute summary statistics."""
    contributors = sorted(set(c["author"] for c in commits))
    type_counts = {cat: len(entries) for cat, entries in grouped.items()}
    return {
        "total_commits": len(commits),
        "total_contributors": len(contributors),
        "contributors": contributors,
        "type_counts": type_counts,
        "breaking_changes": sum(1 for c in commits if c.get("breaking")),
        "date_range": {
            "first": commits[-1]["date"] if commits else None,
            "last": commits[0]["date"] if commits else None,
        },
    }


def to_json(commits: list, grouped: dict, stats: dict,
            version: str = None, date: str = None, repo_path: str = None) -> dict:
    """Build a structured JSON payload for AI-powered rewriting."""
    payload = {
        "meta": {
            "version": version or "unreleased",
            "date": date or datetime.now().strftime("%Y-%m-%d"),
            "generated_at": datetime.now().isoformat(),
            "generator": "changelog-weaver",
        },
        "stats": stats,
        "categories": {},
    }

    for cat, entries in grouped.items():
        label = TYPE_LABELS.get(cat, {"category": cat.capitalize(), "emoji": "📌"})
        payload["categories"][cat] = {
            "label": label["category"],
            "emoji": label["emoji"],
            "count": len(entries),
            "entries": [
                {
                    "hash": e["hash_short"],
                    "description": e["description"],
                    "scope": e.get("scope", ""),
                    "breaking": e.get("breaking", False),
                    "breaking_detail": e.get("breaking_detail", ""),
                    "author": e["author"],
                    "references": e.get("references", []),
                    "original_subject": e["subject"],
                    "count": e.get("count", 1),
                }
                for e in entries
            ],
        }

    if repo_path:
        try:
            repo_url = run_git(repo_path, ["config", "--get", "remote.origin.url"])
            if repo_url:
                payload["meta"]["repo_url"] = repo_url.strip()
        except Exception:
            pass

    return payload


def to_changelog_md(commits: list, grouped: dict, stats: dict,
                    version: str = None, date: str = None,
                    repo_url: str = None, ai_rewrites: dict = None) -> str:
    """Generate CHANGELOG.md in Keep a Changelog format."""
    date = date or datetime.now().strftime("%Y-%m-%d")
    version = version or "Unreleased"

    lines = ["# Changelog", ""]
    lines.append(f"## [{version}] - {date}")
    lines.append("")

    for cat in CATEGORY_ORDER:
        entries = grouped.get(cat, [])
        if not entries:
            continue
        label = TYPE_LABELS.get(cat, {"category": cat.capitalize(), "emoji": "📌"})
        lines.append(f"### {label['emoji']} {label['category']}")
        lines.append("")

        for e in entries:
            desc = (ai_rewrites or {}).get(e["hash_short"], e["description"])
            refs_str = ""
            if e.get("references"):
                refs_str = " (" + ", ".join(f"#{r}" for r in e["references"]) + ")"
            author_str = f" — @{e['author']}" if e.get("author") else ""
            count_note = f" ({e['count']} commits)" if e.get("count", 1) > 1 else ""
            lines.append(f"- {desc}{refs_str}{count_note}{author_str}")
            if e.get("breaking") and e.get("breaking_detail"):
                lines.append(f"  - **BREAKING:** {e['breaking_detail']}")
        lines.append("")

    if stats.get("contributors"):
        lines.append("### 🙏 Contributors")
        lines.append("")
        lines.append(", ".join(f"@{c}" for c in stats["contributors"]))
        lines.append("")

    return "\n".join(lines)


def to_release_notes(commits: list, grouped: dict, stats: dict,
                     version: str = None, date: str = None,
                     repo_url: str = None, ai_rewrites: dict = None) -> str:
    """Generate a GitHub Release body."""
    date = date or datetime.now().strftime("%Y-%m-%d")
    version = version or "Unreleased"

    lines = [f"## 🚀 Release {version}", ""]
    breaking_count = stats.get("breaking_changes", 0)
    lines.append(f"**{stats['total_commits']} commits** by "
                 f"**{stats['total_contributors']} contributors**")
    if breaking_count:
        lines.append(f" — ⚠️ includes **{breaking_count} breaking change(s)**")
    lines.append("")

    for cat in CATEGORY_ORDER:
        entries = grouped.get(cat, [])
        if not entries:
            continue
        label = TYPE_LABELS.get(cat, {"category": cat.capitalize(), "emoji": "📌"})
        lines.append(f"### {label['emoji']} {label['category']}")
        lines.append("")
        for e in entries:
            desc = (ai_rewrites or {}).get(e["hash_short"], e["description"])
            refs = ""
            if e.get("references"):
                refs = " (" + ", ".join(f"#{r}" for r in e["references"]) + ")"
            lines.append(f"- {desc}{refs} by @{e['author']} in `{e['hash_short']}`")
            if e.get("breaking") and e.get("breaking_detail"):
                lines.append(f"  > ⚠️ **BREAKING CHANGE:** {e['breaking_detail']}")
        lines.append("")

    if stats.get("contributors"):
        lines.append("### 🙏 New Contributors")
        lines.append("")
        lines.append("Thanks to all contributors for this release!")
        lines.append("")
        lines.append("**Full Changelog**: [compare link]")
        lines.append("")

    return "\n".join(lines)


def to_plain_text(commits: list, grouped: dict, stats: dict,
                  version: str = None, date: str = None,
                  ai_rewrites: dict = None, platform: str = "generic") -> str:
    """Generate plain text release notes for messaging platforms."""
    date = date or datetime.now().strftime("%Y-%m-%d")
    version = version or "Unreleased"

    lines = [f"📦 {version} 发布通知 ({date})", ""]

    for cat in CATEGORY_ORDER:
        entries = grouped.get(cat, [])
        if not entries:
            continue
        label = TYPE_LABELS.get(cat, {"category": cat.capitalize(), "emoji": "•"})
        if platform in ("feishu", "dingtalk"):
            lines.append(f"【{label['category']}】")
        else:
            lines.append(f"{label['emoji']} {label['category']}")
        for e in entries[:5]:
            desc = (ai_rewrites or {}).get(e["hash_short"], e["description"])
            lines.append(f"  • {desc}")
        if len(entries) > 5:
            lines.append(f"  ... and {len(entries) - 5} more changes")
        lines.append("")

    if stats.get("contributors"):
        lines.append(f"👥 贡献者: {', '.join(stats['contributors'][:8])}")
        if len(stats["contributors"]) > 8:
            lines.append(f"   ... 及其他 {len(stats['contributors']) - 8} 位贡献者")
    lines.append("")

    return "\n".join(lines)


# ─── CLI ───

def cmd_collect(args):
    """CLI handler for the 'collect' subcommand."""
    repo = args.repo or "."

    if args.from_latest_tag:
        commits = collect_from_latest_tag(repo, max_count=args.max_count)
    elif args.from_ref or args.since:
        commits = collect_commits(
            repo, from_ref=args.from_ref, to_ref=args.to or "HEAD",
            since=args.since, until=args.until,
            max_count=args.max_count, include_merges=args.include_merges,
        )
    else:
        print("[ERROR] Specify --from/--since/--from-latest-tag", file=sys.stderr)
        sys.exit(1)

    if not commits:
        print("[INFO] No commits found in the specified range.", file=sys.stderr)
        sys.exit(0)

    if not args.no_dedup:
        commits = deduplicate_commits(commits)

    grouped = group_by_category(commits)
    stats = compute_stats(commits, grouped)
    payload = to_json(commits, grouped, stats, version=args.version, repo_path=repo)
    output = json.dumps(payload, indent=2, ensure_ascii=False)

    if args.output:
        Path(args.output).parent.mkdir(parents=True, exist_ok=True)
        Path(args.output).write_text(output)
        print(f"[OK] Structured changelog data saved to: {args.output}", file=sys.stderr)
    else:
        print(output)

    print(f"\n[SUMMARY] {stats['total_commits']} commits, "
          f"{stats['total_contributors']} contributors, "
          f"{stats['breaking_changes']} breaking changes", file=sys.stderr)
    for cat in CATEGORY_ORDER:
        count = stats["type_counts"].get(cat, 0)
        if count > 0:
            label = TYPE_LABELS.get(cat, {"category": cat, "emoji": "•"})
            print(f"  {label['emoji']} {label['category']}: {count}", file=sys.stderr)


def cmd_generate(args):
    """CLI handler for the 'generate' subcommand."""
    if args.input:
        payload = json.loads(Path(args.input).read_text())
    else:
        print("[ERROR] --input required for generate", file=sys.stderr)
        sys.exit(1)

    meta = payload.get("meta", {})
    stats = payload.get("stats", {})
    categories_raw = payload.get("categories", {})

    grouped = {}
    commits = []
    ai_rewrites = payload.get("ai_rewrites", {})

    for cat_name, cat_data in categories_raw.items():
        entries = cat_data.get("entries", [])
        grouped[cat_name] = []
        for entry in entries:
            commit = {
                "hash_short": entry.get("hash", ""),
                "description": entry.get("description", ""),
                "author": entry.get("author", ""),
                "references": entry.get("references", []),
                "breaking": entry.get("breaking", False),
                "breaking_detail": entry.get("breaking_detail", ""),
                "scope": entry.get("scope", ""),
                "count": entry.get("count", 1),
            }
            grouped[cat_name].append(commit)
            commits.append(commit)

    version = meta.get("version", "Unreleased")
    date = meta.get("date", datetime.now().strftime("%Y-%m-%d"))
    repo_url = meta.get("repo_url", "")

    if args.format == "changelog":
        output = to_changelog_md(commits, grouped, stats, version, date,
                                 repo_url, ai_rewrites)
    elif args.format == "release":
        output = to_release_notes(commits, grouped, stats, version, date,
                                  repo_url, ai_rewrites)
    elif args.format == "plain":
        output = to_plain_text(commits, grouped, stats, version, date,
                               ai_rewrites, platform=args.platform or "generic")
    elif args.format == "json":
        output = json.dumps(payload, indent=2, ensure_ascii=False)
    else:
        print(f"[ERROR] Unknown format: {args.format}", file=sys.stderr)
        sys.exit(1)

    if args.output:
        Path(args.output).parent.mkdir(parents=True, exist_ok=True)
        Path(args.output).write_text(output)
        print(f"[OK] Generated {args.format} saved to: {args.output}", file=sys.stderr)
    else:
        print(output)


def cmd_formats(args):
    """List available output formats."""
    print("Available output formats:")
    print()
    print("  changelog    CHANGELOG.md (Keep a Changelog format)")
    print("  release      GitHub/GitLab Release body")
    print("  plain        Plain text (飞书/钉钉/企业微信)")
    print("  json         Structured JSON for CI/CD pipelines")
    print()
    print("Usage:")
    print("  weaver.py generate -i commits.json -f changelog")
    print("  weaver.py generate -i commits.json -f release")
    print("  weaver.py generate -i commits.json -f plain -p feishu")
    print("  weaver.py generate -i commits.json -f json")


def main():
    parser = argparse.ArgumentParser(
        description="Changelog Weaver — structured changelog data from git history"
    )
    subparsers = parser.add_subparsers(dest="command", help="Sub-commands")

    # collect
    p = subparsers.add_parser("collect", help="Collect commits from git")
    p.add_argument("--repo", "-r", default=".", help="Path to git repo")
    p.add_argument("--from", dest="from_ref", help="Starting ref")
    p.add_argument("--to", dest="to", default="HEAD", help="Ending ref")
    p.add_argument("--since", help="Start date (YYYY-MM-DD)")
    p.add_argument("--until", help="End date (YYYY-MM-DD)")
    p.add_argument("--from-latest-tag", action="store_true", help="Since latest tag")
    p.add_argument("--version", help="Version string")
    p.add_argument("--max-count", type=int, default=500)
    p.add_argument("--include-merges", action="store_true")
    p.add_argument("--no-dedup", action="store_true")
    p.add_argument("--output", "-o", help="Save JSON to file")

    # generate
    g = subparsers.add_parser("generate", help="Generate changelog from JSON")
    g.add_argument("--input", "-i", required=True, help="Input JSON from collect")
    g.add_argument("--format", "-f", choices=["changelog","release","plain","json"],
                   default="changelog")
    g.add_argument("--platform", "-p", choices=["generic","feishu","dingtalk","slack"],
                   default="generic")
    g.add_argument("--output", "-o", help="Save to file")

    # formats
    subparsers.add_parser("formats", help="List available output formats")

    args = parser.parse_args()

    if args.command == "collect":
        cmd_collect(args)
    elif args.command == "generate":
        cmd_generate(args)
    elif args.command == "formats":
        cmd_formats(args)
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
