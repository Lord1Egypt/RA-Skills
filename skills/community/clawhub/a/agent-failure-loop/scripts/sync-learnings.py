#!/usr/bin/env python3
"""
sync-learnings.py — failures/ → .learnings/ 구조화 동기화

failures/ 디렉토리의 원시 실패 기록을 파싱하여
.learnings/ 디렉토리에 유형별·패턴별로 구조화된 분석 결과를 생성한다.

Usage:
    python3 sync-learnings.py [--failures-dir PATH] [--learnings-dir PATH] [--dry-run]

Requires: Python 3.8+ (표준 라이브러리만 사용)
"""

import argparse
import hashlib
import json
import os
import re
import sys
from collections import Counter, defaultdict
from datetime import datetime, timedelta
from pathlib import Path

# ── 설정 ────────────────────────────────────────────────────────────────────

DEFAULT_FAILURES_DIR = "memory/failures"
DEFAULT_LEARNINGS_DIR = ".learnings"

FAILURE_TYPES = {"ERROR", "CORRECTION", "RETRY_EXCEEDED", "MISUNDERSTAND"}

# 실패 기록 파싱 정규식
ENTRY_HEADER_RE = re.compile(
    r"^##\s+(\d{2}:\d{2})\s*-\s*\[(\w+)\]\s*(.+)$", re.MULTILINE
)
FIELD_RE = re.compile(r"^-\s+\*\*(\w+?):\*\*\s*(.+)$", re.MULTILINE)


# ── 파싱 ────────────────────────────────────────────────────────────────────


def parse_failure_file(filepath: Path) -> list[dict]:
    """하나의 failures/YYYY-MM-DD.md 파일을 파싱하여 엔트리 리스트를 반환한다."""
    text = filepath.read_text(encoding="utf-8")
    date_str = filepath.stem  # YYYY-MM-DD

    entries = []
    # 헤더 위치 기준으로 분할
    headers = list(ENTRY_HEADER_RE.finditer(text))

    for i, match in enumerate(headers):
        time_str = match.group(1)
        failure_type = match.group(2).upper()
        title = match.group(3).strip()

        # 이 엔트리의 본문 범위
        start = match.end()
        end = headers[i + 1].start() if i + 1 < len(headers) else len(text)
        body = text[start:end]

        # 필드 추출
        fields = {}
        for field_match in FIELD_RE.finditer(body):
            key = field_match.group(1).lower()
            value = field_match.group(2).strip()
            fields[key] = value

        # 유형 검증
        if failure_type not in FAILURE_TYPES:
            failure_type = "ERROR"  # fallback

        entry = {
            "date": date_str,
            "time": time_str,
            "type": failure_type,
            "title": title,
            "situation": fields.get("상황", fields.get("situation", "")),
            "cause": fields.get("원인", fields.get("cause", "")),
            "lesson": fields.get("교훈", fields.get("lesson", "")),
            "count": fields.get("누적", fields.get("count", "")),
            "raw_body": body.strip(),
        }

        # 패턴 키 생성 (유형 + 원인 해시로 유사 실패 그룹핑)
        cause_normalized = re.sub(r"\s+", " ", entry["cause"].lower().strip())
        pattern_key = f"{failure_type}:{hashlib.md5(cause_normalized.encode()).hexdigest()[:8]}"
        entry["pattern_key"] = pattern_key

        entries.append(entry)

    return entries


def scan_all_failures(failures_dir: Path) -> list[dict]:
    """failures/ 디렉토리 전체를 스캔하여 모든 엔트리를 반환한다."""
    all_entries = []
    if not failures_dir.exists():
        print(f"[WARN] failures 디렉토리 없음: {failures_dir}")
        return all_entries

    for f in sorted(failures_dir.glob("*.md")):
        if re.match(r"\d{4}-\d{2}-\d{2}\.md$", f.name):
            try:
                entries = parse_failure_file(f)
                all_entries.extend(entries)
            except Exception as e:
                print(f"[WARN] 파싱 실패 {f.name}: {e}")

    return all_entries


# ── 분석 ────────────────────────────────────────────────────────────────────


def analyze_patterns(entries: list[dict]) -> dict:
    """패턴별 그룹핑 + 통계 분석."""
    by_pattern = defaultdict(list)
    by_type = Counter()
    by_date = Counter()

    for e in entries:
        by_pattern[e["pattern_key"]].append(e)
        by_type[e["type"]] += 1
        by_date[e["date"]] += 1

    # 반복 패턴 감지 (3회 이상)
    repeated = {
        k: v for k, v in by_pattern.items() if len(v) >= 3
    }

    return {
        "total_entries": len(entries),
        "by_type": dict(by_type),
        "by_date": dict(by_date),
        "patterns": {
            k: {
                "count": len(v),
                "type": v[0]["type"],
                "first_seen": v[0]["date"],
                "last_seen": v[-1]["date"],
                "representative_title": v[0]["title"],
                "representative_cause": v[0]["cause"],
                "representative_lesson": v[0]["lesson"],
                "all_titles": [e["title"] for e in v],
            }
            for k, v in by_pattern.items()
        },
        "repeated_patterns": {
            k: {
                "count": len(v),
                "type": v[0]["type"],
                "titles": [e["title"] for e in v],
                "cause": v[0]["cause"],
                "lesson": v[0]["lesson"],
                "dates": [e["date"] for e in v],
            }
            for k, v in repeated.items()
        },
    }


# ── 출력 (learnings/) ──────────────────────────────────────────────────────


def write_learnings(analysis: dict, learnings_dir: Path, dry_run: bool = False):
    """분석 결과를 .learnings/ 디렉토리에 구조화하여 기록한다."""
    learnings_dir.mkdir(parents=True, exist_ok=True)

    # 1. summary.json — 전체 요약 (머신 리더블)
    summary_path = learnings_dir / "summary.json"
    summary_data = {
        "last_sync": datetime.now().isoformat(),
        "total_failures": analysis["total_entries"],
        "by_type": analysis["by_type"],
        "repeated_pattern_count": len(analysis["repeated_patterns"]),
        "patterns": {
            k: {"count": v["count"], "type": v["type"]}
            for k, v in analysis["patterns"].items()
        },
    }

    if dry_run:
        print(f"[DRY-RUN] Would write: {summary_path}")
        print(json.dumps(summary_data, indent=2, ensure_ascii=False)[:500])
    else:
        summary_path.write_text(
            json.dumps(summary_data, indent=2, ensure_ascii=False),
            encoding="utf-8",
        )
        print(f"[OK] {summary_path}")

    # 2. repeated-patterns.md — 반복 패턴 분석 (사람 리더블)
    repeated_path = learnings_dir / "repeated-patterns.md"
    lines = [
        "# Repeated Failure Patterns",
        "",
        f"> Last sync: {datetime.now().strftime('%Y-%m-%d %H:%M')}",
        f"> Total failures analyzed: {analysis['total_entries']}",
        f"> Repeated patterns (≥3): {len(analysis['repeated_patterns'])}",
        "",
    ]

    if not analysis["repeated_patterns"]:
        lines.append("No repeated patterns detected yet. Keep recording failures.")
    else:
        for key, pat in sorted(
            analysis["repeated_patterns"].items(),
            key=lambda x: x[1]["count"],
            reverse=True,
        ):
            lines.extend([
                f"## [{pat['type']}] {pat['titles'][0]} ({pat['count']}회)",
                "",
                f"- **Pattern Key:** `{key}`",
                f"- **Count:** {pat['count']}",
                f"- **Type:** {pat['type']}",
                f"- **First:** {pat['dates'][0]} → **Last:** {pat['dates'][-1]}",
                f"- **Cause:** {pat['cause']}",
                f"- **Lesson:** {pat['lesson']}",
                "",
                "### All occurrences:",
                "",
            ])
            for i, title in enumerate(pat["titles"]):
                lines.append(f"{i+1}. [{pat['dates'][i]}] {title}")
            lines.extend(["", "---", ""])

    content = "\n".join(lines)
    if dry_run:
        print(f"[DRY-RUN] Would write: {repeated_path}")
        print(content[:500])
    else:
        repeated_path.write_text(content, encoding="utf-8")
        print(f"[OK] {repeated_path}")

    # 3. by-type/ 디렉토리 — 유형별 상세
    by_type_dir = learnings_dir / "by-type"
    by_type_dir.mkdir(parents=True, exist_ok=True)

    for ftype in FAILURE_TYPES:
        type_patterns = {
            k: v for k, v in analysis["patterns"].items()
            if v["type"] == ftype
        }
        if not type_patterns:
            continue

        type_path = by_type_dir / f"{ftype.lower()}.md"
        type_lines = [
            f"# {ftype} Failures",
            "",
            f"Total patterns: {len(type_patterns)}",
            f"Total occurrences: {sum(p['count'] for p in type_patterns.values())}",
            "",
        ]
        for key, pat in sorted(
            type_patterns.items(), key=lambda x: x[1]["count"], reverse=True
        ):
            type_lines.extend([
                f"## {pat['representative_title']} ({pat['count']}회)",
                "",
                f"- **Cause:** {pat['representative_cause']}",
                f"- **Lesson:** {pat['representative_lesson']}",
                f"- **Period:** {pat['first_seen']} ~ {pat['last_seen']}",
                "",
            ])

        if dry_run:
            print(f"[DRY-RUN] Would write: {type_path}")
        else:
            type_path.write_text("\n".join(type_lines), encoding="utf-8")
            print(f"[OK] {type_path}")

    # 4. promotable.json — 승격 후보 목록 (auto-promote.py 입력)
    promotable_path = learnings_dir / "promotable.json"
    promotable = []
    for key, pat in analysis["repeated_patterns"].items():
        promotable.append({
            "pattern_key": key,
            "type": pat["type"],
            "count": pat["count"],
            "title": pat["titles"][0],
            "cause": pat["cause"],
            "lesson": pat["lesson"],
            "first_seen": pat["dates"][0],
            "last_seen": pat["dates"][-1],
            "suggested_rule": pat["lesson"],
        })

    if dry_run:
        print(f"[DRY-RUN] Would write: {promotable_path}")
    else:
        promotable_path.write_text(
            json.dumps(promotable, indent=2, ensure_ascii=False),
            encoding="utf-8",
        )
        print(f"[OK] {promotable_path} ({len(promotable)} candidates)")

    return len(analysis["repeated_patterns"])


# ── CLI ─────────────────────────────────────────────────────────────────────


def main():
    parser = argparse.ArgumentParser(
        description="Sync failures/ → .learnings/ (structured analysis)"
    )
    parser.add_argument(
        "--failures-dir",
        default=os.environ.get("AFL_FAILURES_DIR", DEFAULT_FAILURES_DIR),
        help=f"failures 디렉토리 경로 (default: {DEFAULT_FAILURES_DIR})",
    )
    parser.add_argument(
        "--learnings-dir",
        default=os.environ.get("AFL_LEARNINGS_DIR", DEFAULT_LEARNINGS_DIR),
        help=f"learnings 디렉토리 경로 (default: {DEFAULT_LEARNINGS_DIR})",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="실제 파일 쓰기 없이 미리보기",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="JSON 형식으로 요약 출력",
    )
    args = parser.parse_args()

    failures_dir = Path(args.failures_dir)
    learnings_dir = Path(args.learnings_dir)

    print(f"[sync-learnings] Scanning: {failures_dir}")
    entries = scan_all_failures(failures_dir)
    print(f"[sync-learnings] Found {len(entries)} failure entries")

    if not entries:
        print("[sync-learnings] No entries to process. Done.")
        sys.exit(0)

    analysis = analyze_patterns(entries)

    if args.json:
        print(json.dumps(analysis, indent=2, ensure_ascii=False))
        sys.exit(0)

    repeated_count = write_learnings(analysis, learnings_dir, dry_run=args.dry_run)

    print(f"\n[sync-learnings] Done. {repeated_count} repeated patterns found.")
    if repeated_count > 0:
        print("[sync-learnings] Run auto-promote.py to promote rules automatically.")


if __name__ == "__main__":
    main()
