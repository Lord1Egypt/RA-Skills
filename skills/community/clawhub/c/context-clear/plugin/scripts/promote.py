#!/usr/bin/env python3
"""
promote.py — 晋升评分 + 候选报告（纯文件系统）

条件（任一满足即晋升候选）：
  7天内引用 ≥ 3 次
  14天内引用 ≥ 5 次
  总引用 ≥ 8 次
  用户标记（user_marked = true）

输出：promote_report.md
用途：子 session 读取报告，按分类人工处理
"""

import json, math, os, time, sys
from pathlib import Path

STATE_DIR = Path(os.environ.get("OPENCLAW_STATE_DIR", Path.home() / ".openclaw"))
FS_BASE = STATE_DIR / "memory_fs"
REFCOUNT = STATE_DIR / "refcount.json"
REPORT = STATE_DIR / "promote_report.md"


def load_refcount() -> dict:
    if REFCOUNT.exists():
        return json.loads(REFCOUNT.read_text(encoding="utf-8"))
    return {}


def save_refcount(data: dict):
    REFCOUNT.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def classify(rel_path: str, entry: dict) -> str:
    """基于路径和内容猜测分类"""
    low = rel_path.lower()
    tags = entry.get("tags", [])

    if any(t in low for t in ["skill", "skill", "retrospect", "protocol"]):
        return "skill"
    if any(t in ["skill", "retrospect"] for t in tags):
        return "skill"
    if any(t in low for t in ["pref", "preference", "user"]):
        return "preference"
    if entry.get("user_marked"):
        return "preference"
    return "unknown"


def promote(dry_run=True):
    now = int(time.time())
    refcount = load_refcount()

    # 标记已摘要化的 gist 文件，跳过引用计数（gist 已非原文）
    for rel, entry in refcount.items():
        if entry.get("summarized"):
            continue
        # 滚动 7 天计数
        count_7d = sum(1 for ts in entry.get("timestamps", []) if now - ts < 7 * 86400)

        # 晋升条件
        if (entry.get("user_marked") and count_7d >= 1) or \
           (count_7d >= 3) or \
           (now - entry.get("created", now) < 14 * 86400 and count_7d >= 5) or \
           (entry.get("total", 0) >= 8):
            entry["_candidate"] = True
        else:
            entry["_candidate"] = False

    candidates = [(rel, e) for rel, e in refcount.items() if e.get("_candidate")]

    # 生成报告
    lines = ["# 晋升候选清单\n"]
    lines.append(f"> 统计时间: {time.strftime('%Y-%m-%d %H:%M')}\n")
    lines.append(f"> 候选数: {len(candidates)}\n\n")

    if not candidates:
        lines.append("_无晋升候选_\n")
    else:
        lines.append("| 文件 | 总引用 | 7d引用 | 用户标记 | 建议分类 |")
        lines.append("|------|--------|--------|----------|----------|")
        for rel, entry in candidates:
            count_7d = sum(1 for ts in entry.get("timestamps", []) if now - ts < 7 * 86400)
            cat = classify(rel, entry)
            labels = {"skill": "📐 Skill → retro", "preference": "👤 偏好 → MEMORY", "unknown": "📄 需判定"}
            lines.append(
                f"| {Path(rel).name} "
                f"| {entry.get('total', 0)} "
                f"| {count_7d} "
                f"| {'⭐' if entry.get('user_marked') else ''} "
                f"| {labels.get(cat, '')} |"
            )

    lines.append("\n---\n")
    lines.append("**处理流程：**\n")
    lines.append("1. Skill 类 → spawn 子 session 读本文 → 搬至 `skills/<skill>/docs/retrospect.md`")
    lines.append("2. 偏好类 → spawn 子 session 读原文 → 提取关键信息至 `MEMORY.md`")
    lines.append("3. 需判定 → 主 session 扫一眼后分类\n")
    lines.append("**标记说明：**\n")
    lines.append("- 已标记 `pending` 的条目等待处理")
    lines.append("- 处理完后从 refcount.json 删除该条目或标记 `promoted: true`\n")

    REPORT.write_text('\n'.join(lines), encoding='utf-8')

    # 标记候选（dry_run 模式下不修改 refcount）
    if not dry_run:
        for rel, entry in candidates:
            entry["status"] = "pending_promote"
        save_refcount(refcount)

    return REPORT


if __name__ == "__main__":
    dry = "--apply" not in sys.argv
    path = promote(dry_run=dry)
    print(f"📋 晋升报告: {path}")
    print(f"   候选数: {len([k for k, v in load_refcount().items() if v.get('_candidate')])}")
    if dry:
        print("   ℹ️  预览模式，加 --apply 标记候选")
