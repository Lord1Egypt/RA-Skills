#!/usr/bin/env python3
"""
auto-promote.py — 반복 실패 패턴을 자동으로 규칙 파일에 승격

.learnings/promotable.json 에서 승격 후보를 읽어
지정된 대상 파일(AGENTS.md, CLAUDE.md, .cursorrules 등)에
자가 개선 규칙을 자동 추가한다.

Usage:
    python3 auto-promote.py [--learnings-dir PATH] [--target PATH] [--format FORMAT] [--dry-run]

Formats:
    agents-md   — AGENTS.md 테이블 포맷 (default)
    claude-md   — CLAUDE.md 규칙 포맷
    cursorrules — .cursorrules 포맷
    plain       — 범용 마크다운 규칙 리스트

Requires: Python 3.8+ (표준 라이브러리만 사용)
"""

import argparse
import json
import os
import re
import sys
from datetime import datetime
from pathlib import Path

# ── 설정 ────────────────────────────────────────────────────────────────────

DEFAULT_LEARNINGS_DIR = ".learnings"
DEFAULT_TARGET = "AGENTS.md"
DEFAULT_FORMAT = "agents-md"
DEFAULT_MIN_COUNT = 3  # 최소 반복 횟수

# 이미 승격된 규칙 추적 파일
PROMOTED_LOG = ".learnings/promoted.json"

# ── 포맷터 ──────────────────────────────────────────────────────────────────


def format_agents_md_row(item: dict, today: str) -> str:
    """AGENTS.md 자가 개선 규칙 테이블 행 포맷."""
    rule = item["suggested_rule"]
    type_code = item["type"]
    count = item["count"]
    title = item["title"]
    return f"| {today} | {rule} | [{type_code}] {count}회 반복 — {title} |"


def format_claude_md_rule(item: dict) -> str:
    """CLAUDE.md 규칙 포맷 (Claude Code 호환)."""
    return f"- **{item['type']}**: {item['suggested_rule']} (반복 {item['count']}회, 원인: {item['cause']})"


def format_cursorrules(item: dict) -> str:
    """.cursorrules 포맷 (Cursor IDE 호환)."""
    return f"- {item['suggested_rule']}"


def format_plain(item: dict, today: str) -> str:
    """범용 마크다운 규칙."""
    return (
        f"### [{item['type']}] {item['title']}\n"
        f"- **Rule:** {item['suggested_rule']}\n"
        f"- **Count:** {item['count']}회\n"
        f"- **Promoted:** {today}\n"
    )


FORMATTERS = {
    "agents-md": format_agents_md_row,
    "claude-md": format_claude_md_rule,
    "cursorrules": format_cursorrules,
    "plain": format_plain,
}


# ── 승격 로직 ───────────────────────────────────────────────────────────────


def load_promoted(learnings_dir: Path) -> set:
    """이미 승격된 패턴 키를 로드한다."""
    promoted_path = learnings_dir / "promoted.json"
    if promoted_path.exists():
        try:
            data = json.loads(promoted_path.read_text(encoding="utf-8"))
            return set(data.get("promoted_keys", []))
        except (json.JSONDecodeError, KeyError):
            return set()
    return set()


def save_promoted(learnings_dir: Path, promoted_keys: set):
    """승격 완료된 패턴 키를 저장한다."""
    promoted_path = learnings_dir / "promoted.json"
    data = {
        "last_updated": datetime.now().isoformat(),
        "promoted_keys": sorted(promoted_keys),
    }
    promoted_path.write_text(
        json.dumps(data, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )


def load_promotable(learnings_dir: Path) -> list[dict]:
    """승격 후보를 로드한다."""
    promotable_path = learnings_dir / "promotable.json"
    if not promotable_path.exists():
        print(f"[WARN] promotable.json 없음: {promotable_path}")
        print("[HINT] 먼저 sync-learnings.py 를 실행하세요.")
        return []

    try:
        return json.loads(promotable_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        print(f"[ERROR] promotable.json 파싱 실패: {e}")
        return []


def find_insertion_point_agents_md(content: str) -> int | None:
    """AGENTS.md에서 자가 개선 규칙 테이블의 마지막 행 위치를 찾는다."""
    # "현재 등록된 자가 개선 규칙" 섹션의 테이블 끝을 찾음
    marker = "현재 등록된 자가 개선 규칙"
    idx = content.find(marker)
    if idx == -1:
        return None

    # 테이블 헤더(|---|) 이후의 마지막 | 행을 찾음
    table_start = content.find("|---", idx)
    if table_start == -1:
        return None

    # 테이블 행들의 끝을 찾음
    pos = table_start
    last_row_end = table_start
    for line in content[table_start:].split("\n"):
        pos += len(line) + 1
        if line.strip().startswith("|") and line.strip().endswith("|"):
            last_row_end = idx + (pos - len(line) - 1) + len(line)
        elif line.strip() and not line.strip().startswith("|"):
            break

    return last_row_end


def find_insertion_point_claude_md(content: str) -> int | None:
    """CLAUDE.md에서 규칙 삽입 위치를 찾는다."""
    # "Rules" 또는 "자가 개선" 섹션 끝
    for marker in ["## Rules", "## Self-Improvement", "## 자가 개선"]:
        idx = content.find(marker)
        if idx != -1:
            # 다음 ## 섹션 직전
            next_section = content.find("\n## ", idx + len(marker))
            if next_section != -1:
                return next_section
            return len(content)
    return None


def insert_rules_into_file(
    target_path: Path,
    rules_text: str,
    fmt: str,
    dry_run: bool = False,
) -> bool:
    """대상 파일에 규칙을 삽입한다."""
    if not target_path.exists():
        print(f"[WARN] 대상 파일 없음: {target_path}")
        if fmt == "plain":
            # plain 포맷은 새 파일 생성 허용
            if dry_run:
                print(f"[DRY-RUN] Would create: {target_path}")
                return True
            target_path.parent.mkdir(parents=True, exist_ok=True)
            target_path.write_text(
                f"# Auto-Promoted Rules\n\n{rules_text}\n",
                encoding="utf-8",
            )
            print(f"[OK] Created: {target_path}")
            return True
        return False

    content = target_path.read_text(encoding="utf-8")

    if fmt == "agents-md":
        insert_pos = find_insertion_point_agents_md(content)
    elif fmt == "claude-md":
        insert_pos = find_insertion_point_claude_md(content)
    else:
        insert_pos = len(content)  # 파일 끝에 추가

    if insert_pos is None:
        print(f"[WARN] 삽입 위치를 찾을 수 없음. 파일 끝에 추가합니다.")
        insert_pos = len(content)

    new_content = content[:insert_pos] + "\n" + rules_text + "\n" + content[insert_pos:]

    if dry_run:
        print(f"[DRY-RUN] Would update: {target_path}")
        print(f"[DRY-RUN] Inserting at position {insert_pos}:")
        print(rules_text[:500])
        return True

    target_path.write_text(new_content, encoding="utf-8")
    print(f"[OK] Updated: {target_path}")
    return True


# ── 메인 ────────────────────────────────────────────────────────────────────


def main():
    parser = argparse.ArgumentParser(
        description="Auto-promote repeated failure patterns to rule files"
    )
    parser.add_argument(
        "--learnings-dir",
        default=os.environ.get("AFL_LEARNINGS_DIR", DEFAULT_LEARNINGS_DIR),
        help=f"learnings 디렉토리 (default: {DEFAULT_LEARNINGS_DIR})",
    )
    parser.add_argument(
        "--target",
        default=os.environ.get("AFL_TARGET_FILE", DEFAULT_TARGET),
        help=f"승격 대상 파일 (default: {DEFAULT_TARGET})",
    )
    parser.add_argument(
        "--format",
        choices=FORMATTERS.keys(),
        default=os.environ.get("AFL_FORMAT", DEFAULT_FORMAT),
        help=f"출력 포맷 (default: {DEFAULT_FORMAT})",
    )
    parser.add_argument(
        "--min-count",
        type=int,
        default=int(os.environ.get("AFL_MIN_COUNT", DEFAULT_MIN_COUNT)),
        help=f"최소 반복 횟수 (default: {DEFAULT_MIN_COUNT})",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="실제 파일 수정 없이 미리보기",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="이미 승격된 패턴도 다시 승격",
    )
    args = parser.parse_args()

    learnings_dir = Path(args.learnings_dir)
    target_path = Path(args.target)
    today = datetime.now().strftime("%Y-%m-%d")

    # 1. 승격 후보 로드
    candidates = load_promotable(learnings_dir)
    if not candidates:
        print("[auto-promote] No candidates. Run sync-learnings.py first.")
        sys.exit(0)

    # 2. 이미 승격된 키 로드
    promoted_keys = load_promoted(learnings_dir) if not args.force else set()

    # 3. 미승격 + min_count 이상 필터
    new_candidates = [
        c for c in candidates
        if c["pattern_key"] not in promoted_keys and c["count"] >= args.min_count
    ]

    if not new_candidates:
        print(f"[auto-promote] No new candidates (min_count={args.min_count}).")
        sys.exit(0)

    print(f"[auto-promote] {len(new_candidates)} new rules to promote")

    # 4. 포맷팅
    formatter = FORMATTERS[args.format]
    formatted_rules = []
    for item in new_candidates:
        if args.format in ("agents-md", "plain"):
            formatted_rules.append(formatter(item, today))
        else:
            formatted_rules.append(formatter(item))

    rules_text = "\n".join(formatted_rules)

    # 5. 삽입
    success = insert_rules_into_file(target_path, rules_text, args.format, args.dry_run)

    if success and not args.dry_run:
        # 승격 완료 기록
        for c in new_candidates:
            promoted_keys.add(c["pattern_key"])
        save_promoted(learnings_dir, promoted_keys)
        print(f"[auto-promote] Promoted {len(new_candidates)} rules to {target_path}")
    elif success:
        print(f"[DRY-RUN] Would promote {len(new_candidates)} rules")

    # 6. 요약 출력
    print("\n--- Promoted Rules ---")
    for item in new_candidates:
        print(f"  [{item['type']}] {item['title']} ({item['count']}x) → {item['suggested_rule'][:80]}")


if __name__ == "__main__":
    main()
