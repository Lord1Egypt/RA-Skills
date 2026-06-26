#!/usr/bin/env python3
"""
每日复盘与自我提升脚本
记录任务纠正 → 分析规律 → 生成成长报告
"""

import argparse
import json
import os
import sys
from dataclasses import dataclass, asdict
from datetime import datetime
from pathlib import Path


MEMORY_DIR = Path.home() / ".qclaw" / "memory"
HOT_FILE = MEMORY_DIR / "memory.md"
COLD_DIR = MEMORY_DIR / "archive"


@dataclass
class Reflection:
    timestamp: str
    context: str
    what_happened: str
    lesson: str
    severity: int  # 1=轻微, 5=严重
    tags: list[str]


def ensure_dirs():
    MEMORY_DIR.mkdir(parents=True, exist_ok=True)
    COLD_DIR.mkdir(parents=True, exist_ok=True)


def load_hot_memory() -> list[Reflection]:
    """加载热记忆"""
    if not HOT_FILE.exists():
        return []

    reflections = []
    current: dict = {}
    in_block = False

    for line in HOT_FILE.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line.startswith("**CONTEXT:**"):
            in_block = True
            current = {"context": line.replace("**CONTEXT:**", "").strip()}
        elif in_block:
            if line.startswith("**"):
                key = line.replace("**", "").split(":")[0].lower()
                val = line.split(":", 1)[-1].strip()
                current[key] = val
            elif line == "---":
                if all(k in current for k in ["context", "reflection", "lesson"]):
                    reflections.append(Reflection(
                        timestamp=current.get("timestamp", ""),
                        context=current.get("context", ""),
                        what_happened=current.get("reflection", ""),
                        lesson=current.get("lesson", ""),
                        severity=int(current.get("severity", 3)),
                        tags=[t.strip() for t in current.get("tags", "").split(",") if t.strip()]
                    ))
                current = {}
                in_block = False

    return reflections


def record_reflection(
    context: str,
    what_happened: str,
    lesson: str,
    severity: int = 3,
    tags: list[str] = None,
) -> Reflection:
    """记录一次纠正"""
    ensure_dirs()

    ref = Reflection(
        timestamp=datetime.now().strftime("%Y-%m-%d %H:%M"),
        context=context,
        what_happened=what_happened,
        lesson=lesson,
        severity=max(1, min(5, severity)),
        tags=tags or [],
    )

    entry = (
        f"\n---\n"
        f"**CONTEXT:** {ref.context}\n"
        f"**TIMESTAMP:** {ref.timestamp}\n"
        f"**REFLECTION:** {ref.what_happened}\n"
        f"**LESSON:** {ref.lesson}\n"
        f"**SEVERITY:** {ref.severity}\n"
        f"**TAGS:** {', '.join(ref.tags)}\n"
    )

    HOT_FILE.write_text(HOT_FILE.read_text(encoding="utf-8") + entry, encoding="utf-8")
    return ref


def analyze_patterns(reflections: list[Reflection]) -> dict:
    """分析纠正规律"""
    if not reflections:
        return {}

    # 按标签统计
    tag_count = {}
    for r in reflections:
        for tag in r.tags:
            tag_count[tag] = tag_count.get(tag, 0) + 1

    # 按严重程度统计
    severity_dist = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}
    for r in reflections:
        severity_dist[r.severity] = severity_dist.get(r.severity, 0) + 1

    # 高频教训（出现多次）
    lesson_count = {}
    for r in reflections:
        key = r.lesson[:50]
        lesson_count[key] = lesson_count.get(key, 0) + 1

    recurring = [k for k, v in lesson_count.items() if v >= 2]

    return {
        "total_reflections": len(reflections),
        "tag_distribution": dict(sorted(tag_count.items(), key=lambda x: -x[1])[:10]),
        "severity_distribution": severity_dist,
        "recurring_lessons": recurring,
    }


def generate_report(reflections: list[Reflection], patterns: dict) -> str:
    """生成复盘报告"""
    if not reflections:
        return "📭 暂无记录。运行 `reflect.py --add` 记录你的第一次复盘吧！"

    latest = reflections[-1]
    report_lines = [
        f"# 📊 自我复盘报告",
        f"生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M')}",
        f"",
        f"## 📈 总体统计",
        f"- 总复盘次数: **{patterns['total_reflections']}**",
        f"- 最新记录: **{latest.timestamp}** | 场景: {latest.context}",
        f"",
        f"## 🏷️ 高频问题领域",
    ]

    for tag, count in list(patterns["tag_distribution"].items())[:5]:
        bar = "█" * count
        report_lines.append(f"- {tag}: {bar} ({count}次)")

    report_lines += [
        f"",
        f"## ⚠️ 严重程度分布",
        f"- 🔵 轻微(1-2): {patterns['severity_distribution'][1] + patterns['severity_distribution'][2]} 次",
        f"- 🟡 一般(3):   {patterns['severity_distribution'][3]} 次",
        f"- 🔴 严重(4-5): {patterns['severity_distribution'][4] + patterns['severity_distribution'][5]} 次",
    ]

    if patterns["recurring_lessons"]:
        report_lines += [
            f"",
            f"## ♻️ 反复出现的问题（需重点关注）",
        ]
        for lesson in patterns["recurring_lessons"]:
            report_lines.append(f"- ⚠️ {lesson}")

    report_lines += [
        f"",
        f"## 💡 最新教训",
        f"> {latest.lesson}",
        f"",
        f"---",
        f"*由 automation-skill 自动生成*",
    ]

    return "\n".join(report_lines)


# ── CLI ──────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="自我复盘与成长记录工具")
    sub = parser.add_subparsers(dest="cmd")

    # 记录
    add_p = sub.add_parser("add", help="记录一次复盘")
    add_p.add_argument("-c", "--context", required=True, help="任务/场景描述")
    add_p.add_argument("-w", "--what", required=True, help="发生了什么/哪里做错了")
    add_p.add_argument("-l", "--lesson", required=True, help="下次如何改进")
    add_p.add_argument("-s", "--severity", type=int, default=3, choices=[1,2,3,4,5], help="严重程度 1-5")
    add_p.add_argument("-t", "--tags", nargs="*", default=[], help="标签")

    # 报告
    report_p = sub.add_parser("report", help="生成复盘报告")
    report_p.add_argument("-o", "--output", help="输出文件路径")

    # 统计
    sub.add_parser("stats", help="显示统计信息")

    # 列出
    list_p = sub.add_parser("list", help="列出最近 N 条记录")
    list_p.add_argument("-n", "--num", type=int, default=10, help="显示数量")

    args = parser.parse_args()

    if args.cmd == "add":
        ref = record_reflection(args.context, args.what, args.lesson, args.severity, args.tags)
        print(f"✅ 已记录: [{ref.timestamp}] {ref.context}")
        print(f"   → {ref.lesson}")

    elif args.cmd == "report":
        refs = load_hot_memory()
        pats = analyze_patterns(refs)
        report = generate_report(refs, pats)
        print(report)
        if args.output:
            Path(args.output).write_text(report, encoding="utf-8")
            print(f"\n📄 已保存到: {args.output}")

    elif args.cmd == "stats":
        refs = load_hot_memory()
        pats = analyze_patterns(refs)
        print(f"📊 统计信息")
        print(f"  总记录: {pats['total_reflections']}")
        print(f"  标签分布: {pats['tag_distribution']}")
        print(f"  严重程度: {pats['severity_distribution']}")

    elif args.cmd == "list":
        refs = load_hot_memory()
        for r in refs[-args.num:]:
            print(f"\n[{r.timestamp}] {r.context} {'⚠️' * r.severity}")
            print(f"  {r.what_happened}")
            print(f"  → {r.lesson}")

    else:
        parser.print_help()

    return 0


if __name__ == "__main__":
    sys.exit(main() or 0)
