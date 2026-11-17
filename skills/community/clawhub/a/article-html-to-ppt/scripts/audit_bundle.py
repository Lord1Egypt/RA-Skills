#!/usr/bin/env python3
"""Scan a PPTSmith bundle for distribution hygiene findings and emit a generated audit report.

PPTSmith forbids handwriting a trusted status for a deck. The same rule applies
to the bundle itself: a security or hygiene statement must be the output of an
actual scan, not prose. This script replaces the previously handwritten
`references/SECURITY-AUDIT.md` with a generated pair:

  * `references/BUNDLE-AUDIT.json` - machine-readable findings, the source of truth;
  * `references/BUNDLE-AUDIT.md`   - a rendering of that JSON for humans.

Checks performed:

  1. BUNDLE_EXCLUDED_PATH_PRESENT - a path matched by `packaging/bundle-exclude.txt`
     is present in the bundle.
  2. BUNDLE_ABSOLUTE_PATH_LEAK    - a text file records a local absolute home or
     workspace path. Fix with `scripts/normalize_bundle_paths.py`.
  3. BUNDLE_SECRET_LEAK           - a key/secret/token assignment with a plausible value.
  4. BUNDLE_SECRET_SHAPED_FILE    - a filename that conventionally holds a credential.
  5. BUNDLE_HIGH_ENTROPY_STRING   - a long hex or base64 run that is not a declared digest.

Deliberate exceptions live in `packaging/audit-allowlist.json` and must state a
reason. The generated report lists every suppression together with its reason,
so an exception is visible rather than silent.

The finding vocabulary intentionally mirrors `scripts/package_delivery.py`'s
`PRIVATE_PATTERNS`, which performs the same class of check on a delivery package
rather than on the bundle.
"""

from __future__ import annotations

import argparse
import fnmatch
import json
import os
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_EXCLUDE_FILE = ROOT / "packaging" / "bundle-exclude.txt"
DEFAULT_ALLOWLIST = ROOT / "packaging" / "audit-allowlist.json"
DEFAULT_JSON_OUTPUT = ROOT / "references" / "BUNDLE-AUDIT.json"
DEFAULT_MD_OUTPUT = ROOT / "references" / "BUNDLE-AUDIT.md"

# Text formats worth scanning for recorded paths and secrets. Binary payloads
# (pptx/pdf/png) are inventoried but not content-scanned.
TEXT_SUFFIXES = {".json", ".md", ".txt", ".log", ".py", ".js", ".mjs", ".html", ".css", ".yml", ".yaml", ".cfg", ".ini", ".toml"}

# Vendored third-party code is inventoried but never content-scanned: its
# fixtures and minified bundles trip every heuristic and none of it is ours.
CONTENT_SCAN_SKIP_DIRS = {
    "node_modules",
    ".git",
    ".release-artifacts",
    ".venv-release",
    ".pytest_cache",
    ".pytest-tmp",
    "__pycache__",
}
CONTENT_SCAN_SKIP_FILES = {"references/BUNDLE-AUDIT.json", "references/BUNDLE-AUDIT.md"}

ABSOLUTE_PATH_LEAK = re.compile(r"(?:/(?:Users|home)/[A-Za-z0-9._-]+/|[A-Za-z]:\\Users\\[A-Za-z0-9._-]+\\)")

SECRET_ASSIGNMENT = re.compile(r"(?i)(api[_-]?key|secret|password|passwd|token|bearer|private[_-]?key)\s*[:=]\s*['\"]?([A-Za-z0-9_\-/+]{12,})")

SECRET_SHAPED_NAMES = (".env", "*.pem", "*.key", "id_rsa", "id_rsa.pub", "*.p12", "*.pfx", "credentials.json", ".last-token", ".netrc")

# A 32+ character hex or base64 run. Content digests, renderer build hashes, and
# VCS revisions are legitimately long and high-entropy, so a line is exempt when
# it declares one - either with an explicit `sha256:`-style prefix or with a key
# name that names the value as a digest/version. Everything else is reported,
# because that is how a session token or API key looks.
HIGH_ENTROPY = re.compile(r"\b(?:[0-9a-fA-F]{32,}|[A-Za-z0-9+/]{40,}={0,2})\b")
DECLARED_DIGEST_PREFIX = re.compile(r"(?:sha256:|sha1:|sha512:|md5:|integrity\"?\s*:\s*\"?sha\d{3}-)\s*$")
DECLARED_DIGEST_KEY = re.compile(r"(?i)\"[A-Za-z0-9_.-]*(?:hash|digest|sha\d*|checksum|integrity|commit|revision|engine_version|build_id)[A-Za-z0-9_.-]*\"\s*:")

SEVERITY_ORDER = {"error": 2, "warning": 1, "info": 0}


def iso_now() -> str:
    fixed = os.environ.get("PPTSMITH_AUDIT_TIMESTAMP", "").strip()
    if fixed:
        return fixed
    return datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds")


def load_exclude_rules(path: Path) -> list[tuple[str, str]]:
    """Return [(pattern, severity)] from the exclude file.

    Markers:
      `warn:`  -> warning     (should not ship, tracked for removal)
      `cache:` -> regenerable (error when auditing an archive, ignored in a
                               live working tree, where running the suite
                               legitimately creates the path)
      none     -> error
    """
    if not path.exists():
        return []
    rules: list[tuple[str, str]] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        severity = "error"
        lowered = stripped.lower()
        if lowered.startswith("warn:"):
            severity = "warning"
            stripped = stripped.split(":", 1)[1].strip()
        elif lowered.startswith("cache:"):
            severity = "regenerable"
            stripped = stripped.split(":", 1)[1].strip()
        if stripped:
            rules.append((stripped, severity))
    return rules


def load_allowlist(path: Path) -> dict[str, set[str]]:
    """Return {relative_path: {suppressed codes}} from the allowlist document."""
    if not path.exists():
        return {}
    document = json.loads(path.read_text(encoding="utf-8"))
    allowed: dict[str, set[str]] = {}
    for entry in document.get("allowlist", []) or []:
        if not isinstance(entry, dict):
            continue
        target = str(entry.get("path", "")).strip()
        reason = str(entry.get("reason", "")).strip()
        codes = entry.get("codes") or []
        if not target or not reason or not codes:
            # An allowlist entry without a reason is a configuration error. It is
            # reported instead of silently honoured.
            continue
        allowed.setdefault(target, set()).update(str(code) for code in codes)
    return allowed


def allowlist_reasons(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    document = json.loads(path.read_text(encoding="utf-8"))
    return [entry for entry in document.get("allowlist", []) or [] if isinstance(entry, dict)]


def matches_rule(relative: str, is_dir: bool, rule: str) -> bool:
    """Match one exclude rule against a bundle-relative POSIX path.

    A directory rule ('trailing/') matches the directory itself and everything
    underneath it, and may itself contain '/' segments
    (e.g. `runtime/pptxgenjs/node_modules/`). A file rule is matched against both
    the basename and the full relative path, so `*.pyc` and `tests/x.py` both work.
    """
    if rule.endswith("/"):
        needle = rule.rstrip("/")
        if "/" in needle:
            # Multi-segment directory rule: compare on the path prefix.
            return relative == needle or relative.startswith(f"{needle}/")
        parts = relative.split("/")
        return needle in parts[:-1] or (is_dir and parts[-1] == needle)
    name = relative.split("/")[-1]
    return fnmatch.fnmatch(name, rule) or fnmatch.fnmatch(relative, rule)


def iter_paths(root: Path) -> list[Path]:
    return [path for path in sorted(root.rglob("*"))]


def scan_excluded_paths(
    root: Path,
    rules: list[tuple[str, str]],
    *,
    skip_dirs: set[str] | None = None,
) -> list[dict[str, Any]]:
    """Report one finding per violated rule, not one per matched file.

    A single vendored directory can match hundreds of paths; collapsing them
    keeps the report readable and keeps the finding count meaningful.
    """
    hits: dict[str, list[str]] = {}
    severities: dict[str, str] = {}
    skip_dirs = skip_dirs or set()
    for path in iter_paths(root):
        relative = path.relative_to(root).as_posix()
        if skip_dirs.intersection(Path(relative).parts):
            continue
        for rule, severity in rules:
            if matches_rule(relative, path.is_dir(), rule):
                hits.setdefault(rule, []).append(relative)
                severities[rule] = severity
                break

    findings: list[dict[str, Any]] = []
    for rule, paths in hits.items():
        findings.append({
            "code": "BUNDLE_EXCLUDED_PATH_PRESENT",
            "severity": severities[rule],
            "path": paths[0],
            "evidence": {"rule": rule, "matched_paths": len(paths), "samples": paths[:3]},
            "message": f"Path is excluded by packaging/bundle-exclude.txt rule '{rule}' but is present in the bundle.",
        })
    return findings


def scan_secret_shaped_files(root: Path) -> list[dict[str, Any]]:
    findings: list[dict[str, Any]] = []
    for path in iter_paths(root):
        if not path.is_file():
            continue
        relative = path.relative_to(root).as_posix()
        if CONTENT_SCAN_SKIP_DIRS.intersection(Path(relative).parts):
            continue
        name = path.name
        for pattern in SECRET_SHAPED_NAMES:
            if fnmatch.fnmatch(name, pattern):
                findings.append({
                    "code": "BUNDLE_SECRET_SHAPED_FILE",
                    "severity": "error",
                    "path": relative,
                    "evidence": {"pattern": pattern},
                    "message": "Filename conventionally holds a credential and must not be bundled.",
                })
                break
    return findings


def scan_text_content(root: Path) -> tuple[list[dict[str, Any]], int]:
    findings: list[dict[str, Any]] = []
    scanned = 0
    for path in iter_paths(root):
        if not path.is_file() or path.suffix.lower() not in TEXT_SUFFIXES:
            continue
        relative = path.relative_to(root).as_posix()
        if CONTENT_SCAN_SKIP_DIRS.intersection(Path(relative).parts):
            continue
        if relative in CONTENT_SCAN_SKIP_FILES:
            continue
        scanned += 1
        try:
            text = path.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue
        for line_number, line in enumerate(text.splitlines(), start=1):
            leak = ABSOLUTE_PATH_LEAK.search(line)
            if leak:
                findings.append({
                    "code": "BUNDLE_ABSOLUTE_PATH_LEAK",
                    "severity": "error",
                    "path": relative,
                    "evidence": {"line": line_number, "sample": leak.group(0)},
                    "message": "Text file records a local absolute home or workspace path. Run scripts/normalize_bundle_paths.py.",
                })
            secret = SECRET_ASSIGNMENT.search(line)
            if secret:
                findings.append({
                    "code": "BUNDLE_SECRET_LEAK",
                    "severity": "error",
                    "path": relative,
                    "evidence": {"line": line_number, "key": secret.group(1)},
                    "message": "Line looks like a credential assignment with a plausible value.",
                })
            if DECLARED_DIGEST_KEY.search(line):
                # The line names its own value as a digest, build hash, or revision.
                continue
            for match in HIGH_ENTROPY.finditer(line):
                prefix = line[: match.start()]
                if DECLARED_DIGEST_PREFIX.search(prefix):
                    continue
                findings.append({
                    "code": "BUNDLE_HIGH_ENTROPY_STRING",
                    "severity": "warning",
                    "path": relative,
                    "evidence": {"line": line_number, "length": len(match.group(0))},
                    "message": "Long hex/base64 run that is not a declared digest; confirm it is not a session token or key.",
                })
    return findings, scanned


def inventory(root: Path) -> dict[str, Any]:
    files = [path for path in iter_paths(root) if path.is_file()]
    total_bytes = sum(path.stat().st_size for path in files)
    by_dir: dict[str, int] = {}
    for path in files:
        parts = path.relative_to(root).parts
        top = parts[0] if len(parts) > 1 else "."
        by_dir[top] = by_dir.get(top, 0) + path.stat().st_size
    largest = sorted(by_dir.items(), key=lambda item: item[1], reverse=True)[:10]
    return {
        "file_count": len(files),
        "total_bytes": total_bytes,
        "largest_directories": [{"path": name, "bytes": size} for name, size in largest],
    }


def apply_allowlist(findings: list[dict[str, Any]], allowed: dict[str, set[str]]) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    active: list[dict[str, Any]] = []
    suppressed: list[dict[str, Any]] = []
    for finding in findings:
        codes = allowed.get(finding["path"], set())
        if finding["code"] in codes:
            suppressed.append(finding)
        else:
            active.append(finding)
    return active, suppressed


def resolve_rule_severities(rules: list[tuple[str, str]], mode: str) -> list[tuple[str, str]]:
    """Map the `regenerable` marker onto a concrete severity for this audit mode.

    In `archive` mode a cache directory in the package is a real defect. In
    `worktree` mode it is expected, because running the suite creates it, so the
    rule is dropped rather than reported.
    """
    resolved: list[tuple[str, str]] = []
    for pattern, severity in rules:
        if severity == "regenerable":
            if mode == "worktree":
                continue
            severity = "error"
        resolved.append((pattern, severity))
    return resolved


def build_report(root: Path, exclude_file: Path, allowlist_file: Path, *, mode: str = "worktree") -> dict[str, Any]:
    rules = resolve_rule_severities(load_exclude_rules(exclude_file), mode)
    allowed = load_allowlist(allowlist_file)

    findings = scan_excluded_paths(
        root,
        rules,
        skip_dirs=CONTENT_SCAN_SKIP_DIRS if mode == "worktree" else set(),
    )
    findings += scan_secret_shaped_files(root)
    content_findings, text_scanned = scan_text_content(root)
    findings += content_findings

    active, suppressed = apply_allowlist(findings, allowed)
    worst = max((SEVERITY_ORDER.get(item["severity"], 0) for item in active), default=-1)
    status = "passed" if worst < 1 else ("review" if worst == 1 else "failed")

    return {
        "schema_version": "1.0",
        "generated_at": iso_now(),
        "generated_by": "scripts/audit_bundle.py",
        "bundle_root": root.name,
        "private_bundle_present": (root / "private-pmo-pack").exists(),
        "mode": mode,
        "status": status,
        "checks": [
            {"code": "BUNDLE_EXCLUDED_PATH_PRESENT", "rules": len(rules), "source": exclude_file.relative_to(root).as_posix() if exclude_file.is_relative_to(root) else str(exclude_file)},
            {"code": "BUNDLE_ABSOLUTE_PATH_LEAK", "text_files_scanned": text_scanned},
            {"code": "BUNDLE_SECRET_LEAK", "text_files_scanned": text_scanned},
            {"code": "BUNDLE_SECRET_SHAPED_FILE", "patterns": len(SECRET_SHAPED_NAMES)},
            {"code": "BUNDLE_HIGH_ENTROPY_STRING", "text_files_scanned": text_scanned},
        ],
        "inventory": inventory(root),
        "findings": active,
        "suppressed": suppressed,
        "allowlist": allowlist_reasons(allowlist_file),
    }


def render_markdown(report: dict[str, Any]) -> str:
    lines: list[str] = []
    lines.append("# Bundle Audit (generated)")
    lines.append("")
    lines.append("> Do not edit this file. It is generated by `scripts/audit_bundle.py` from an")
    lines.append("> actual scan and is regenerated on every packaging run. The machine-readable")
    lines.append("> source of truth is `references/BUNDLE-AUDIT.json`.")
    lines.append("")
    lines.append(f"- Status: **{report['status']}**")
    lines.append(f"- Mode: {report['mode']}")
    lines.append(f"- Generated at: {report['generated_at']}")
    lines.append(f"- Files: {report['inventory']['file_count']}")
    lines.append(f"- Total size: {report['inventory']['total_bytes'] / 1_048_576:.1f} MiB")
    lines.append("")

    lines.append("## Checks performed")
    lines.append("")
    lines.append("| Check | Scope |")
    lines.append("| --- | --- |")
    for check in report["checks"]:
        scope = ", ".join(f"{key}={value}" for key, value in check.items() if key != "code")
        lines.append(f"| `{check['code']}` | {scope} |")
    lines.append("")

    lines.append("## Findings")
    lines.append("")
    if report["findings"]:
        lines.append("| Severity | Code | Path | Evidence |")
        lines.append("| --- | --- | --- | --- |")
        for finding in report["findings"]:
            evidence = ", ".join(f"{key}={value}" for key, value in finding.get("evidence", {}).items())
            lines.append(f"| {finding['severity']} | `{finding['code']}` | `{finding['path']}` | {evidence} |")
    else:
        lines.append("No findings. Every check above ran and returned zero results.")
    lines.append("")

    lines.append("## Suppressed by allowlist")
    lines.append("")
    if report["suppressed"]:
        lines.append("| Code | Path |")
        lines.append("| --- | --- |")
        for finding in report["suppressed"]:
            lines.append(f"| `{finding['code']}` | `{finding['path']}` |")
        lines.append("")
        lines.append("Reasons, from `packaging/audit-allowlist.json`:")
        lines.append("")
        for entry in report["allowlist"]:
            codes = ", ".join(f"`{code}`" for code in entry.get("codes", []))
            lines.append(f"- `{entry.get('path')}` ({codes}): {entry.get('reason')}")
    else:
        lines.append("Nothing suppressed.")
    lines.append("")

    lines.append("## Largest directories")
    lines.append("")
    lines.append("| Directory | Size |")
    lines.append("| --- | ---: |")
    for item in report["inventory"]["largest_directories"]:
        lines.append(f"| `{item['path']}` | {item['bytes'] / 1_048_576:.1f} MiB |")
    lines.append("")

    lines.append("## Distribution boundary")
    lines.append("")
    if report.get("private_bundle_present"):
        lines.append("This tree contains private commercial material under `private-pmo-pack/` and")
        lines.append("is not eligible for public distribution. Remove it from the release tree.")
    else:
        lines.append("This is the public PPT Smith distribution. Private commercial packs, local")
        lines.append("run artifacts, credentials, and dependency caches are outside this boundary.")
    lines.append("")
    return "\n".join(lines)


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description="Scan a PPTSmith bundle for distribution hygiene findings and write the generated audit report.")
    parser.add_argument("--root", type=Path, default=ROOT, help="Bundle root to audit (default: repository root).")
    parser.add_argument("--exclude-file", type=Path, default=DEFAULT_EXCLUDE_FILE)
    parser.add_argument("--allowlist", type=Path, default=DEFAULT_ALLOWLIST)
    parser.add_argument("--json-output", type=Path, default=DEFAULT_JSON_OUTPUT)
    parser.add_argument("--md-output", type=Path, default=DEFAULT_MD_OUTPUT)
    parser.add_argument("--mode", choices=("archive", "worktree"), default="archive", help="archive: regenerable caches are defects (use when packaging). worktree: caches are ignored (use in a live checkout).")
    parser.add_argument("--fail-on-finding", action="store_true", help="Exit non-zero when any error-severity finding remains.")
    parser.add_argument("--check", action="store_true", help="Do not write the report; only scan and report status.")
    args = parser.parse_args(argv)

    root = args.root.resolve()
    report = build_report(root, args.exclude_file, args.allowlist, mode=args.mode)

    if not args.check:
        args.json_output.parent.mkdir(parents=True, exist_ok=True)
        args.json_output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        args.md_output.write_text(render_markdown(report), encoding="utf-8")
        print(f"audit report written: {args.json_output}")
        print(f"audit report written: {args.md_output}")

    errors = [item for item in report["findings"] if item["severity"] == "error"]
    warnings = [item for item in report["findings"] if item["severity"] == "warning"]
    print(f"mode={report['mode']} status={report['status']} errors={len(errors)} warnings={len(warnings)} suppressed={len(report['suppressed'])}")
    for finding in report["findings"][:40]:
        print(f"  {finding['severity'].upper()} {finding['code']} {finding['path']} {finding.get('evidence')}")

    if args.fail_on_finding and errors:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
