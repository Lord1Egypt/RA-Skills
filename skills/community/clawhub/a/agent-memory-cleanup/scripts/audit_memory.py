#!/usr/bin/env python3
"""Deterministic audit/proposal engine for agent memory markdown files."""

from __future__ import annotations

import argparse
import difflib
import hashlib
import json
import re
import shutil
import sys
import tempfile
from dataclasses import asdict, dataclass
from datetime import datetime
from pathlib import Path
from typing import Any, Iterable


RULES_PATH = Path(__file__).resolve().parent.parent / "references" / "default-rules.json"


@dataclass
class MemoryFinding:
    file: str
    line: int
    classification: str
    reason: str
    text: str


@dataclass
class CleanupProposal:
    original_redacted: str
    proposed_markdown: str
    diff: str
    changed: bool


@dataclass
class FileReport:
    path: str
    exists: bool
    bytes: int = 0
    sha256: str | None = None
    status: str = "missing"
    findings: list[MemoryFinding] | None = None
    proposal: CleanupProposal | None = None
    backup_path: str | None = None
    updated: bool = False
    error: str | None = None


class RuleConfig:
    def __init__(self, data: dict[str, Any]) -> None:
        self.data = data
        self.thresholds = data.get("thresholds", {})
        self.likely_memory_names = {name.lower() for name in data.get("likely_memory_names", [])}
        self.allowed_memory_extensions = {ext.lower() for ext in data.get("allowed_memory_extensions", [".md", ".txt", ".json"])}
        self.blocked_memory_extensions = {ext.lower() for ext in data.get("blocked_memory_extensions", [".db", ".sqlite", ".bin"])}
        self.project_policy_names = {name.lower() for name in data.get("project_policy_names", [])}
        self.search_roots = data.get("search_roots", [".", ".codex", ".claude"])
        self.keep_re = self._compile(data.get("keep_patterns", []))
        self.remove_re = self._compile(data.get("remove_patterns", []))
        self.secret_re = self._compile(data.get("secret_patterns", []))
        self.task_state_re = self._compile(data.get("task_state_patterns", []))
        self.conflict_rules = data.get("conflict_rules", [])
        self.intervention_triggers = data.get("intervention_triggers", {})
        self.condense_rewrites = data.get("condense_rewrites", [])
        self.secret_instruction = data.get(
            "secret_instruction",
            "Do not store secrets, tokens, passwords, or credentials in memory files",
        )

    @classmethod
    def load(cls, path: Path | None = None) -> "RuleConfig":
        rules_path = path or RULES_PATH
        return cls(json.loads(rules_path.read_text(encoding="utf-8")))

    @staticmethod
    def _compile(patterns: Iterable[str]) -> list[re.Pattern[str]]:
        return [re.compile(pattern, re.IGNORECASE) for pattern in patterns]

    def threshold(self, name: str, default: float) -> float:
        value = self.thresholds.get(name, default)
        return float(value)


class MemoryAuditor:
    def __init__(self, rules: RuleConfig) -> None:
        self.rules = rules
        self._seen_normalized: list[str] = []

    def discover_paths(self, base: Path) -> list[Path]:
        candidates: list[Path] = []
        for root_name in self.rules.search_roots:
            root = base / root_name
            if not root.exists() or not root.is_dir():
                continue
            for path in root.iterdir():
                if path.is_file() and self.is_allowed_memory_path(path) and path.name.lower() in self.rules.likely_memory_names:
                    candidates.append(path)
        return sorted(set(candidates))

    def is_allowed_memory_path(self, path: Path) -> bool:
        suffix = path.suffix.lower()
        if suffix in self.rules.blocked_memory_extensions:
            return False
        return suffix in self.rules.allowed_memory_extensions

    def audit_paths(self, paths: list[Path], build_proposals: bool = True) -> list[FileReport]:
        return [self.audit_file(path, build_proposal=build_proposals) for path in paths]

    def audit_candidate(
        self,
        text: str,
        label: str = "<candidate-memory-update>",
        build_proposal: bool = True,
    ) -> FileReport:
        findings = self.classify_text(Path(label), f"- {text}\n")
        redacted = self.redact_text(text)
        proposal = None
        if build_proposal:
            proposed = self.build_proposed_memory(findings)
            proposal = CleanupProposal(
                original_redacted=redacted,
                proposed_markdown=proposed,
                diff=self.build_diff(Path(label), redacted + "\n", proposed),
                changed=True,
            )
        return FileReport(
            path=label,
            exists=True,
            bytes=len(text.encode("utf-8", errors="replace")),
            sha256=hashlib.sha256(text.encode("utf-8", errors="replace")).hexdigest(),
            status="candidate: pre-write lint",
            findings=findings,
            proposal=proposal,
        )

    def audit_file(self, path: Path, build_proposal: bool = True) -> FileReport:
        if not path.exists():
            return FileReport(path=str(path), exists=False)
        size = path.stat().st_size
        if path.name.lower() in self.rules.project_policy_names:
            return FileReport(
                path=str(path),
                exists=True,
                bytes=size,
                status="skipped: project policy file, not user memory by default",
                findings=[],
            )
        if not self.is_allowed_memory_path(path):
            return FileReport(
                path=str(path),
                exists=True,
                bytes=size,
                status="skipped: unsupported memory file extension",
                findings=[],
            )

        raw = path.read_text(encoding="utf-8", errors="replace")
        findings = self.classify_text(path, raw)
        status = self.status_for_size(size)
        has_cleanup_issue = any(finding.classification != "keep" for finding in findings)
        proposal = None
        if build_proposal:
            proposed = self.build_proposed_memory(findings) if has_cleanup_issue or status != "ok" else raw
            redacted_raw = self.redact_text(raw)
            diff = self.build_diff(path, redacted_raw, proposed)
            proposal = CleanupProposal(
                original_redacted=redacted_raw,
                proposed_markdown=proposed,
                diff=diff,
                changed=redacted_raw != proposed,
            )

        return FileReport(
            path=str(path),
            exists=True,
            bytes=size,
            sha256=hashlib.sha256(raw.encode("utf-8", errors="replace")).hexdigest(),
            status=status,
            findings=findings,
            proposal=proposal,
        )

    def classify_text(self, path: Path, raw: str) -> list[MemoryFinding]:
        findings: list[MemoryFinding] = []
        for line, unit in self.split_units(raw):
            classification, reason, redacted = self.classify_unit(unit)
            key = self.normalize(redacted)
            if key:
                self._seen_normalized.append(key)
            findings.append(
                MemoryFinding(
                    file=str(path),
                    line=line,
                    classification=classification,
                    reason=reason,
                    text=redacted,
                )
            )
        return findings

    def split_units(self, text: str) -> list[tuple[int, str]]:
        units: list[tuple[int, str]] = []
        paragraph: list[str] = []
        paragraph_start = 1

        def flush() -> None:
            nonlocal paragraph, paragraph_start
            if paragraph:
                units.append((paragraph_start, " ".join(line.strip() for line in paragraph).strip()))
                paragraph = []

        for index, raw_line in enumerate(text.splitlines(), start=1):
            line = raw_line.strip()
            if not line:
                flush()
                paragraph_start = index + 1
                continue
            if line.startswith("#"):
                flush()
                paragraph_start = index + 1
                continue
            if re.match(r"^[-*+]\s+", line) or re.match(r"^\d+[.)]\s+", line):
                flush()
                cleaned = re.sub(r"^([-*+]|\d+[.)])\s+", "", line).strip()
                units.append((index, cleaned))
                paragraph_start = index + 1
                continue
            if not paragraph:
                paragraph_start = index
            paragraph.append(line)
        flush()
        return [(line, unit) for line, unit in units if unit]

    def classify_unit(self, text: str) -> tuple[str, str, str]:
        redacted = self.redact_text(text)
        normalized = self.normalize(redacted)

        if self.has_secret(text):
            return "remove", "contains a suspected secret or credential", redacted
        if self.is_duplicate(normalized):
            return "condense", "duplicate of an earlier memory item", redacted

        remove_match = self.matches(self.rules.remove_re, redacted)
        keep_match = self.matches(self.rules.keep_re, redacted)

        if remove_match and keep_match:
            return "condense", "mixes durable preference/context with transient task detail", redacted
        if remove_match:
            return "remove", "looks task-specific, stale, or operational", redacted
        if keep_match:
            return "keep", "looks durable and globally useful", redacted
        if len(redacted) > 240:
            return "flag", "long memory item may contain mixed or stale details", redacted
        return "flag", "unclear whether this is durable global memory", redacted

    @staticmethod
    def matches(patterns: list[re.Pattern[str]], text: str) -> bool:
        return any(pattern.search(text) for pattern in patterns)

    def has_secret(self, text: str) -> bool:
        return self.matches(self.rules.secret_re, text)

    def is_task_state(self, text: str) -> bool:
        return self.matches(self.rules.task_state_re, text)

    def redact_text(self, text: str) -> str:
        redacted = text
        for pattern in self.rules.secret_re:
            redacted = pattern.sub("[REDACTED_SECRET]", redacted)
        return redacted

    @staticmethod
    def normalize(text: str) -> str:
        text = text.lower().strip()
        text = re.sub(r"`[^`]+`", "`x`", text)
        text = re.sub(r"\b20\d{2}[-/]\d{1,2}[-/]\d{1,2}\b", "<date>", text)
        text = re.sub(r"\b\d+\b", "<num>", text)
        text = re.sub(r"[^a-z0-9\u4e00-\u9fff<>]+", " ", text)
        return re.sub(r"\s+", " ", text).strip()

    def is_duplicate(self, normalized: str) -> bool:
        if not normalized:
            return False
        if normalized in self._seen_normalized:
            return True
        min_length = int(self.rules.threshold("fuzzy_duplicate_min_length", 28))
        ratio = self.rules.threshold("fuzzy_duplicate_ratio", 0.72)
        if len(normalized) < min_length:
            return False
        return any(difflib.SequenceMatcher(None, normalized, item).ratio() >= ratio for item in self._seen_normalized)

    def status_for_size(self, size: int) -> str:
        if size >= self.rules.threshold("critical_bytes", 40960):
            return "critical: over 40KB, cleanup should be prioritized"
        if size >= self.rules.threshold("cleanup_bytes", 20480):
            return "cleanup recommended: over 20KB"
        if size >= self.rules.threshold("audit_bytes", 8192):
            return "audit recommended: over 8KB"
        return "ok"

    def canonicalize_keep(self, text: str) -> str:
        text = self.redact_text(text).strip()
        text = re.sub(r"\s+", " ", text)
        return text.rstrip(".")

    def append_unique(self, items: list[str], item: str) -> None:
        key = self.normalize(item)
        existing = [self.normalize(value) for value in items]
        if item and not self.is_duplicate_against(key, existing):
            items.append(item)

    def is_duplicate_against(self, normalized: str, existing: list[str]) -> bool:
        if not normalized:
            return False
        if normalized in existing:
            return True
        min_length = int(self.rules.threshold("fuzzy_duplicate_min_length", 28))
        ratio = self.rules.threshold("fuzzy_duplicate_ratio", 0.72)
        if len(normalized) < min_length:
            return False
        return any(difflib.SequenceMatcher(None, normalized, item).ratio() >= ratio for item in existing)

    def rewrite_condensed_item(self, text: str) -> str | None:
        lower = text.lower()
        for rule in self.rules.condense_rewrites:
            needles = [value.lower() for value in rule.get("when_contains_any", [])]
            if any(needle in lower for needle in needles):
                return rule.get("rewrite")
        if "prefer" in lower or "concise" in lower or "direct" in lower:
            return self.canonicalize_keep(text)
        return None

    def build_proposed_memory(self, findings: list[MemoryFinding]) -> str:
        keeps: list[str] = []
        instructions: list[str] = []
        review: list[str] = []
        secret_found = False

        for finding in findings:
            if finding.reason.startswith("contains a suspected secret"):
                secret_found = True
            if finding.classification == "keep":
                self.append_unique(keeps, self.canonicalize_keep(finding.text))
            elif finding.classification == "condense":
                rewritten = self.rewrite_condensed_item(finding.text)
                if rewritten:
                    self.append_unique(keeps, rewritten)
                else:
                    review.append(f"{finding.text} ({finding.reason})")
            elif finding.classification == "flag":
                review.append(f"{finding.text} ({finding.reason})")

        if secret_found:
            instructions.append(self.rules.secret_instruction)

        lines = ["# User Memory", ""]
        if keeps:
            lines.append("## Global Preferences")
            for item in keeps:
                lines.append(f"- {item}.")
            lines.append("")
        if instructions:
            lines.append("## Agent Instructions")
            for item in instructions:
                lines.append(f"- {item}.")
            lines.append("")
        if review:
            lines.append("## Review Needed")
            for item in review:
                lines.append(f"- {item}")
            lines.append("")
        return "\n".join(lines).rstrip() + "\n"

    @staticmethod
    def build_diff(path: Path, original_redacted: str, proposed: str) -> str:
        return "".join(
            difflib.unified_diff(
                original_redacted.splitlines(keepends=True),
                proposed.splitlines(keepends=True),
                fromfile=str(path),
                tofile=f"{path} (proposed)",
            )
        )


class BackupWriter:
    def apply(self, report: FileReport) -> None:
        if not report.exists or not report.proposal:
            return
        path = Path(report.path)
        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        backup = path.with_name(f"{path.name}.bak-{timestamp}")
        tmp_path: Path | None = None
        try:
            shutil.copy2(path, backup)
        except OSError as exc:
            report.error = f"backup failed: {exc}"
            return
        try:
            with tempfile.NamedTemporaryFile(
                "w",
                encoding="utf-8",
                dir=str(path.parent),
                prefix=f".{path.name}.",
                suffix=".tmp",
                delete=False,
            ) as tmp_file:
                tmp_file.write(report.proposal.proposed_markdown)
                tmp_file.flush()
                tmp_path = Path(tmp_file.name)
            tmp_path.replace(path)
        except OSError as exc:
            report.error = f"atomic write failed after backup: {exc}"
            if tmp_path and tmp_path.exists():
                try:
                    tmp_path.unlink()
                except OSError:
                    pass
            return
        report.backup_path = str(backup)
        report.updated = True


class ReportRenderer:
    @staticmethod
    def markdown(reports: list[FileReport], include_diff: bool, mode: str = "audit-only") -> str:
        lines = ["## Memory Cleanup Report", ""]
        lines.append("Files reviewed:")
        for report in reports:
            lines.append(f"- {report.path} - {report.status} - {report.bytes} bytes")
        lines.append("")

        for classification, title in [
            ("keep", "Kept"),
            ("condense", "Condensed"),
            ("remove", "Removed"),
            ("flag", "Needs review"),
        ]:
            lines.append(f"{title}:")
            matches = [
                finding
                for report in reports
                for finding in (report.findings or [])
                if finding.classification == classification
            ]
            if matches:
                for finding in matches:
                    lines.append(f"- {finding.file}:{finding.line} - {finding.reason}: {finding.text}")
            else:
                lines.append("- None")
            lines.append("")

        lines.append("Recommended next step:")
        has_findings = any(report.findings for report in reports)
        has_cleanup_issue = any(
            finding.classification != "keep"
            for report in reports
            for finding in (report.findings or [])
        )
        if mode == "apply-approved" and any(report.updated for report in reports):
            lines.append("- Cleanup has been applied after approval. Review updated files and keep backups until satisfied.")
        elif any(report.status.startswith("critical") for report in reports):
            lines.append("- Apply approved cleanup after reviewing flagged items; file size is in the critical range.")
        elif has_cleanup_issue:
            lines.append("- Review the proposed cleanup and apply only after user approval.")
        elif has_findings:
            lines.append("- No cleanup needed. The reviewed memory appears durable and low-risk.")
        else:
            lines.append("- No memory files found. Provide explicit memory paths or run from an agent config workspace.")
        lines.append("")

        if include_diff:
            for report in reports:
                if report.proposal and report.proposal.diff:
                    lines.append(f"Diff for {report.path}:")
                    lines.append("```diff")
                    lines.append(report.proposal.diff.rstrip())
                    lines.append("```")
                    lines.append("")

        if mode == "apply-approved":
            updated = [report for report in reports if report.updated]
            if updated:
                lines.append("Backups created:")
                for report in updated:
                    lines.append(f"- {report.backup_path}")
                lines.append("")
                lines.append("Files updated:")
                for report in updated:
                    lines.append(f"- {report.path}")
                lines.append("")
            errors = [report for report in reports if report.error]
            if errors:
                lines.append("Errors:")
                for report in errors:
                    lines.append(f"- {report.path}: {report.error}")
                lines.append("")

        return "\n".join(lines).rstrip() + "\n"


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Audit agent memory markdown files.")
    parser.add_argument("paths", nargs="*", help="Memory files to audit. If omitted, scan likely files in the current workspace.")
    parser.add_argument(
        "--mode",
        choices=["audit-only", "propose-patch", "apply-approved"],
        default="audit-only",
        help="Execution mode. Only apply-approved writes files.",
    )
    parser.add_argument("--rules", help="Optional path to a JSON rules file.")
    parser.add_argument("--json", action="store_true", help="Emit JSON instead of markdown.")
    parser.add_argument("--summary-json", action="store_true", help="Emit compact machine-readable summary JSON.")
    parser.add_argument("--candidate", help="Lint a proposed memory entry before writing it to global memory.")
    parser.add_argument("--include-diff", action="store_true", help="Include unified diffs in markdown output.")
    parser.add_argument("--output", help="Write report to this path instead of stdout.")
    parser.add_argument("--write-proposed", help="Write the first proposed cleaned memory to this path.")
    return parser.parse_args(argv)


def compact_summary(reports: list[FileReport], rules: RuleConfig) -> dict[str, Any]:
    counts: dict[str, int] = {"keep": 0, "condense": 0, "remove": 0, "flag": 0}
    secret_count = 0
    task_state_count = 0
    all_text: list[str] = []
    for report in reports:
        for finding in report.findings or []:
            counts[finding.classification] = counts.get(finding.classification, 0) + 1
            if "suspected secret" in finding.reason:
                secret_count += 1
            if "task-specific" in finding.reason or "stale" in finding.reason or "operational" in finding.reason:
                task_state_count += 1
            all_text.append(finding.text.lower())
    total = sum(counts.values())
    polluted = counts.get("condense", 0) + counts.get("remove", 0) + counts.get("flag", 0)
    pollution_score = round(polluted / total, 4) if total else 0.0
    conflict_count, conflicts = detect_conflicts(all_text, rules)
    intervention = recommend_intervention(
        pollution_score=pollution_score,
        secret_count=secret_count,
        task_state_count=task_state_count,
        conflict_count=conflict_count,
        candidate=any(report.status.startswith("candidate") for report in reports),
        rules=rules,
    )
    return {
        "files": [
            {
                "path": report.path,
                "exists": report.exists,
                "bytes": report.bytes,
                "status": report.status,
                "changed": report_needs_cleanup(report),
                "updated": report.updated,
                "backup_path": report.backup_path,
                "error": report.error,
            }
            for report in reports
        ],
        "counts": counts,
        "quality": {
            "total_items": total,
            "polluted_items": polluted,
            "pollution_score": pollution_score,
            "secret_count": secret_count,
            "task_state_count": task_state_count,
            "conflict_count": conflict_count,
            "conflicts": conflicts,
            "intervention": intervention,
        },
    }


def report_needs_cleanup(report: FileReport) -> bool:
    if report.proposal:
        return report.proposal.changed
    if report.status != "ok" and not report.status.startswith("skipped"):
        return True
    return any(finding.classification != "keep" for finding in (report.findings or []))


def detect_conflicts(texts: list[str], rules: RuleConfig) -> tuple[int, list[str]]:
    joined = "\n".join(texts)
    conflicts: list[str] = []
    for rule in rules.conflict_rules:
        positive = any(term.lower() in joined for term in rule.get("positive", []))
        negative = any(term.lower() in joined for term in rule.get("negative", []))
        if positive and negative:
            conflicts.append(rule.get("name", "unnamed_conflict"))
    return len(conflicts), conflicts


def recommend_intervention(
    *,
    pollution_score: float,
    secret_count: int,
    task_state_count: int,
    conflict_count: int,
    candidate: bool,
    rules: RuleConfig,
) -> str:
    triggers = rules.intervention_triggers
    if secret_count > int(triggers.get("secret_count_gt", 0)):
        return "prompt_cleanup_now_secret_detected"
    if conflict_count > int(triggers.get("conflict_count_gt", 0)):
        return "prompt_user_review_conflicting_memory"
    if candidate and triggers.get("candidate_remove_or_flag", True) and task_state_count > int(triggers.get("task_state_count_gt", 0)):
        return "do_not_write_candidate_to_global_memory"
    if pollution_score >= float(triggers.get("pollution_cleanup_ratio", rules.threshold("pollution_cleanup_ratio", 0.35))):
        return "prompt_cleanup_recommended"
    if pollution_score >= float(triggers.get("pollution_notice_ratio", rules.threshold("pollution_notice_ratio", 0.2))):
        return "prompt_audit_recommended"
    return "no_intervention_needed"


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    rules = RuleConfig.load(Path(args.rules) if args.rules else None)
    auditor = MemoryAuditor(rules)
    paths = [Path(path).expanduser() for path in args.paths]
    if not paths:
        paths = auditor.discover_paths(Path.cwd())

    build_proposals = not (
        args.summary_json
        and args.mode == "audit-only"
        and not args.include_diff
        and not args.write_proposed
    )

    reports = auditor.audit_paths(paths, build_proposals=build_proposals)
    if args.candidate:
        reports.append(auditor.audit_candidate(args.candidate, build_proposal=build_proposals))

    if args.write_proposed:
        first = next((report for report in reports if report.proposal), None)
        if first and first.proposal:
            Path(args.write_proposed).write_text(first.proposal.proposed_markdown, encoding="utf-8")

    if args.mode == "apply-approved":
        writer = BackupWriter()
        for report in reports:
            writer.apply(report)

    if args.summary_json:
        payload = json.dumps(compact_summary(reports, rules), indent=2, ensure_ascii=False)
    elif args.json:
        payload = json.dumps([asdict(report) for report in reports], indent=2, ensure_ascii=False)
    else:
        include_diff = args.include_diff or args.mode in {"propose-patch", "apply-approved"}
        payload = ReportRenderer.markdown(reports, include_diff=include_diff, mode=args.mode)

    if args.output:
        Path(args.output).write_text(payload, encoding="utf-8")
    else:
        sys.stdout.write(payload)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
