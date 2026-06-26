#!/usr/bin/env python3
"""Read-only BMA retention audit for aged OpenClaw memory archives."""
from __future__ import annotations

import argparse
import datetime as dt
import json
import re
from pathlib import Path

HIGH_PATTERNS = {
    "decision": r"\bDecision\b|决定|确认|选择|方案|架构|原则",
    "preference": r"Preference|偏好|喜欢|不喜欢|希望|以后|默认",
    "failure": r"FAILURE|CORRECTION|失败|教训|根因|修复|回滚|bug|Bug",
    "config": r"配置|config|openclaw\.json|cron|schema|doctor|Gateway|gateway",
    "runbook": r"runbook|workflow|流程|步骤|操作手册|复用",
    "project": r"项目|project|OpenCortex|memory-wiki|active-memory|lossless|qmd|BMA",
    "external": r"GitHub|ClawHub|邮件|日历|commit|PR|issue|发布|对外",
}
LOW_PATTERNS = {
    "empty": r"无新内容|无新日志|nothing to do|no new|HEARTBEAT_OK",
    "dreaming": r"dream|Dream|梦|DREAMS|dreaming|Light Sleep|REM Sleep",
    "tool_dump": r"Command exited|Process exited|stdout|stderr|tool result|日志片段",
    "transient": r"当前状态|临时|暂时|snapshot|status|检查通过|正常运行",
}
DATE_RE = re.compile(r"(20\d{2}-\d{2}-\d{2})")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Audit aged memory archive files without modifying them.")
    parser.add_argument("--workspace", default=".", help="OpenClaw workspace path")
    parser.add_argument("--older-than-days", type=int, default=30, help="Only scan files older than this many days")
    parser.add_argument("--archive-dir", default="memory/archive", help="Archive directory relative to workspace")
    parser.add_argument("--report-dir", default="memory-archive/reports", help="Report directory relative to workspace; kept outside memory/ by default")
    parser.add_argument("--limit", type=int, default=0, help="Optional max files to inspect")
    return parser.parse_args()


def infer_file_date(path: Path) -> dt.date | None:
    match = DATE_RE.search(path.name)
    if not match:
        return None
    try:
        return dt.date.fromisoformat(match.group(1))
    except ValueError:
        return None


def count_matches(text: str, patterns: dict[str, str]) -> dict[str, int]:
    return {name: len(re.findall(pattern, text, flags=re.IGNORECASE)) for name, pattern in patterns.items()}


def classify(score: int, high_total: int, low_total: int) -> str:
    if high_total >= 6 and score >= 6:
        return "retain-summary"
    if low_total >= 8 and high_total <= 2:
        return "cold-archive-only"
    if score <= 0:
        return "cold-archive-only"
    return "review-manual"


def excerpt(text: str, max_chars: int = 360) -> str:
    compact = re.sub(r"\s+", " ", text).strip()
    return compact[:max_chars] + ("…" if len(compact) > max_chars else "")


def audit_file(path: Path, workspace: Path, today: dt.date) -> dict:
    text = path.read_text(encoding="utf-8", errors="replace")
    high = count_matches(text, HIGH_PATTERNS)
    low = count_matches(text, LOW_PATTERNS)
    high_total = sum(high.values())
    low_total = sum(low.values())
    score = high_total * 2 - low_total
    file_date = infer_file_date(path)
    age_days = (today - file_date).days if file_date else None
    return {
        "path": str(path.relative_to(workspace)),
        "date": file_date.isoformat() if file_date else None,
        "ageDays": age_days,
        "bytes": path.stat().st_size,
        "lines": text.count("\n") + 1,
        "score": score,
        "bucket": classify(score, high_total, low_total),
        "highSignals": {k: v for k, v in high.items() if v},
        "lowSignals": {k: v for k, v in low.items() if v},
        "excerpt": excerpt(text),
        "futureColdPath": str(Path("memory-archive") / path.relative_to(workspace / "memory")),
    }


def render_report(results: list[dict], args: argparse.Namespace, today: dt.date) -> str:
    by_bucket: dict[str, list[dict]] = {}
    for item in results:
        by_bucket.setdefault(item["bucket"], []).append(item)
    lines = [
        f"# BMA Retention Audit — {today.isoformat()}",
        "",
        "Read-only audit. No source files were modified.",
        "",
        "## Parameters",
        f"- workspace: `{Path(args.workspace).resolve()}`",
        f"- archive dir: `{args.archive_dir}`",
        f"- report dir: `{args.report_dir}`",
        f"- older than days: `{args.older_than_days}`",
        f"- inspected files: {len(results)}",
        "",
        "## Summary",
    ]
    for bucket in ["retain-summary", "review-manual", "cold-archive-only"]:
        lines.append(f"- {bucket}: {len(by_bucket.get(bucket, []))}")
    lines.append("")
    for bucket in ["retain-summary", "review-manual", "cold-archive-only"]:
        items = sorted(by_bucket.get(bucket, []), key=lambda x: (-x["score"], x["path"]))
        lines.extend([f"## {bucket}", ""])
        if not items:
            lines.extend(["_None._", ""])
            continue
        for item in items[:50]:
            lines.extend([
                f"### `{item['path']}`",
                f"- date: {item['date']} / age: {item['ageDays']} days / score: {item['score']}",
                f"- size: {item['bytes']} bytes / lines: {item['lines']}",
                f"- future cold path: `{item['futureColdPath']}`",
                f"- high signals: `{json.dumps(item['highSignals'], ensure_ascii=False)}`",
                f"- low signals: `{json.dumps(item['lowSignals'], ensure_ascii=False)}`",
                f"- excerpt: {item['excerpt']}",
                "",
            ])
    return "\n".join(lines)


def main() -> int:
    args = parse_args()
    workspace = Path(args.workspace).expanduser().resolve()
    archive = (workspace / args.archive_dir).resolve()
    today = dt.datetime.now().date()
    cutoff = today - dt.timedelta(days=args.older_than_days)
    if not archive.exists():
        raise SystemExit(f"archive dir not found: {archive}")
    candidates = []
    for path in sorted(archive.rglob("*.md")):
        file_date = infer_file_date(path)
        if not file_date or file_date > cutoff:
            continue
        candidates.append(path)
    if args.limit and args.limit > 0:
        candidates = candidates[: args.limit]
    results = [audit_file(path, workspace, today) for path in candidates]
    reports_dir = (workspace / args.report_dir).resolve()
    try:
        reports_dir.relative_to(workspace / "memory")
    except ValueError:
        pass
    else:
        raise SystemExit("report-dir must not be inside memory/ because memory/ is indexed by memory-wiki indexDailyNotes")
    reports_dir.mkdir(parents=True, exist_ok=True)
    report_path = reports_dir / f"bma-retention-audit-{today.isoformat()}.md"
    report_path.write_text(render_report(results, args, today), encoding="utf-8")
    print(f"BMA retention audit complete: {report_path}")
    print(f"inspected={len(results)}")
    counts = {}
    for item in results:
        counts[item["bucket"]] = counts.get(item["bucket"], 0) + 1
    print(json.dumps(counts, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
