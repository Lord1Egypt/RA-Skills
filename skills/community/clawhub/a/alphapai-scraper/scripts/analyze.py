#!/usr/bin/env python3
"""
AlphaPai report generator.
"""

from __future__ import annotations

import argparse
import glob
import json
import os
import subprocess
from datetime import datetime
from pathlib import Path
from typing import Any

from common import (
    build_run_stamp,
    choose_output_extension,
    ensure_runtime_dirs,
    load_settings,
)


FALLBACK_SECTORS = {
    "AI / 算力": ["AI", "算力", "GPU", "芯片", "英伟达", "华为", "昇腾", "大模型", "Agent", "LLM"],
    "新能源": ["新能源", "光伏", "储能", "电池", "风电", "充电", "宁德", "比亚迪"],
    "科技硬件": ["半导体", "PCB", "光模块", "服务器", "苹果", "小米", "面板"],
    "消费": ["消费", "零售", "电商", "白酒", "餐饮", "品牌"],
    "医药": ["医药", "创新药", "CXO", "生物", "医疗器械"],
    "宏观 / 政策": ["政策", "央行", "关税", "利率", "财政", "出口"],
}

DELTA_KEYWORDS = [
    "加单",
    "涨价",
    "提价",
    "公告",
    "中标",
    "订单",
    "扩产",
    "回购",
    "业绩",
    "突破",
    "更新",
    "变化",
]


def extract_semantic_lines(content: str) -> list[str]:
    lines: list[str] = []
    for raw_line in content.splitlines():
        line = raw_line.strip()
        if not line:
            continue
        if line.startswith("#"):
            continue
        if line.startswith("- 抓取时间:") or line.startswith("- 窗口:") or line.startswith("- 篇数:"):
            continue
        if line.startswith("- 时间:") or line.startswith("- 来源:"):
            continue
        line = line.lstrip("-").strip()
        if not line or line.startswith("`") or len(line) < 4:
            continue
        lines.append(line)
    return lines


def load_latest_raw_file(settings: dict[str, Any], specific_file: str | None = None) -> str | None:
    if specific_file and os.path.exists(specific_file):
        return specific_file
    runtime_dirs = ensure_runtime_dirs(settings)
    files = glob.glob(str(runtime_dirs["raw_dir"] / "*.*"))
    if not files:
        return None
    files.sort(key=os.path.getmtime, reverse=True)
    return files[0]


def build_prompt(content: str, lookback_hours: float, settings: dict[str, Any]) -> str:
    target_length = int(settings["ai"]["target_length_chars"])
    custom_requirements = str(settings["ai"].get("custom_requirements") or "").strip()
    custom_block = ""
    if custom_requirements:
        custom_block = f"\n额外格式要求：\n{custom_requirements}\n"
    return f"""你是一位擅长二级市场信息提炼的研究员，请把 Alpha派最近 {lookback_hours:g} 小时评论整理成一份适合手机阅读的中文摘要。

必须遵守以下格式和要求：
1. 总字数控制在 {target_length - 100} 到 {target_length + 150} 字。
2. 第一段必须是“今日结论”，用 2-3 句总结市场最重要的增量信息。
3. 第二部分必须是“边际变化 / 增量信息 TOP5”，只写真正的新变化，例如加单、涨价、公告、订单、政策、业绩、预期差。
4. 第三部分按“行业”或“股票标的”做清晰分类，优先使用最有信息量的一种分组方式。
5. 每个要点不超过 2 行，适合手机阅读。
6. 重要股票、公司、行业关键词请加粗。
7. 最后一部分必须写“情绪温度计”，只能从“偏热 / 中性 / 偏冷”中选一个，并给一句解释。
8. 如果原文里有明显噪声、传闻或重复信息，请单独放到“待验证”。
{custom_block}

建议输出骨架：
# Alpha派摘要
## 今日结论
## 边际变化 / 增量信息 TOP5
## 行业 / 标的脉络
## 情绪温度计
## 待验证

下面是原文：

{content}
"""


def run_ai_analysis(prompt: str, settings: dict[str, Any]) -> str | None:
    model = settings["ai"]["model"]
    try:
        result = subprocess.run(
            [
                "openclaw",
                "agent",
                "--message",
                prompt,
                "--model",
                model,
            ],
            capture_output=True,
            text=True,
            timeout=180,
        )
    except Exception:
        return None

    if result.returncode == 0 and result.stdout.strip():
        return result.stdout.strip()
    return None


def fallback_analysis(content: str, lookback_hours: float) -> str:
    lines = extract_semantic_lines(content)
    deltas: list[str] = []
    sector_hits: dict[str, list[str]] = {key: [] for key in FALLBACK_SECTORS}
    unclassified: list[str] = []

    for line in lines:
        if any(keyword in line for keyword in DELTA_KEYWORDS) and line not in deltas:
            deltas.append(line[:120])
        matched = False
        for sector, keywords in FALLBACK_SECTORS.items():
            if any(keyword in line for keyword in keywords):
                snippet = line[:120]
                if snippet not in sector_hits[sector]:
                    sector_hits[sector].append(snippet)
                matched = True
        if not matched and len(unclassified) < 6:
            unclassified.append(line[:120])

    temperature = "中性"
    if len(deltas) >= 5:
        temperature = "偏热"
    elif len(deltas) <= 1:
        temperature = "偏冷"

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    report_lines = [
        f"# Alpha派摘要",
        "",
        f"- 生成时间: `{timestamp}`",
        f"- 覆盖窗口: 最近 `{lookback_hours:g}` 小时",
        "",
        "## 今日结论",
        f"最近 {lookback_hours:g} 小时内的评论里，市场关注点主要集中在边际变化最明确的板块和标的，信息密度最高的线索优先来自订单、价格、公告和政策催化。",
        "",
        "## 边际变化 / 增量信息 TOP5",
    ]
    for entry in deltas[:5]:
        report_lines.append(f"- {entry}")
    if not deltas:
        report_lines.append("- 暂未识别出足够明确的增量信号，建议回看原文确认。")

    report_lines.extend(["", "## 行业 / 标的脉络"])
    wrote_sector = False
    for sector, snippets in sector_hits.items():
        if not snippets:
            continue
        wrote_sector = True
        report_lines.append(f"### {sector}")
        for snippet in snippets[:3]:
            report_lines.append(f"- {snippet}")
        report_lines.append("")
    if not wrote_sector:
        for snippet in unclassified[:5]:
            report_lines.append(f"- {snippet}")
        report_lines.append("")

    report_lines.extend(
        [
            "## 情绪温度计",
            f"- {temperature}：评论中有 {len(deltas)} 条相对明确的增量线索，整体更偏交易驱动而非全面扩散。",
            "",
            "## 待验证",
            "- 规则引擎版本不会自动判断真假和强弱，正式使用时建议结合 AI 版摘要二次确认。",
        ]
    )
    return "\n".join(report_lines).strip() + "\n"


def generate_report(
    raw_file: str,
    settings: dict[str, Any],
    lookback_hours: float,
) -> dict[str, Any]:
    runtime_dirs = ensure_runtime_dirs(settings)
    report_ext = choose_output_extension(settings, "report_format")
    report_suffix = settings["output"]["report_suffix"]

    try:
        content = Path(raw_file).read_text(encoding="utf-8")
    except Exception as exc:
        return {"ok": False, "error": f"读取原文失败: {exc}"}

    max_input_chars = int(settings["ai"]["max_input_chars"])
    prompt = build_prompt(content[:max_input_chars], lookback_hours, settings)
    report = run_ai_analysis(prompt, settings)
    engine = "ai"
    if not report:
        report = fallback_analysis(content, lookback_hours)
        engine = "fallback"

    raw_stem = Path(raw_file).stem
    report_path = runtime_dirs["report_dir"] / f"{raw_stem}{report_suffix}.{report_ext}"
    report_path.write_text(report, encoding="utf-8")

    meta_path = runtime_dirs["runtime_dir"] / f"{raw_stem}_report.json"
    meta_path.write_text(
        json.dumps(
            {
                "generated_at": build_run_stamp(),
                "engine": engine,
                "raw_file": raw_file,
                "report_file": str(report_path),
                "lookback_hours": lookback_hours,
            },
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )

    return {
        "ok": True,
        "report_file": str(report_path),
        "engine": engine,
        "meta_file": str(meta_path),
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="AlphaPai report generator")
    parser.add_argument("raw_file", nargs="?", help="Path to raw file")
    parser.add_argument("--hours", type=float, default=None)
    parser.add_argument("--settings", help="Path to settings file")
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    settings = load_settings(args.settings)
    lookback_hours = (
        args.hours
        if args.hours is not None
        else float(settings["scrape"]["default_lookback_hours"])
    )
    raw_file = load_latest_raw_file(settings, args.raw_file)
    if not raw_file:
        print("未找到原文文件")
        return 1

    result = generate_report(raw_file, settings, lookback_hours)
    if result["ok"]:
        print(result["report_file"])
        return 0
    print(result["error"])
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
