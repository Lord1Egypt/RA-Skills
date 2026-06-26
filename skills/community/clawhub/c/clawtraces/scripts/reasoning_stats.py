#!/usr/bin/env python3
# FILE_META
# INPUT:  .openai.json files
# OUTPUT: table of reasoning_content coverage per session
# POS:    skill scripts — utility, standalone
# MISSION: Analyze reasoning content usage ratios across trajectories.
"""Calculate reasoning_content ratio for all OpenAI format trajectory files.

Reads .openai.json files from output directory and reports reasoning ratio.

Usage:
    python reasoning_stats.py [--output-dir PATH]
"""

import argparse
import json
import os
import glob
import sys


sys.path.insert(0, os.path.dirname(__file__))
from lib.paths import get_default_output_dir

DEFAULT_OUTPUT_DIR = get_default_output_dir()


def calc_reasoning_ratio(oai_data: dict) -> dict:
    """Calculate reasoning ratio for a single OpenAI trajectory.

    Denominator = pure text assistant (no tool_calls) + assistant with tool_calls AND reasoning_content
    Numerator = all assistant messages with non-empty reasoning_content

    Returns dict with stats.
    """
    total_asst = 0
    total_tool_calls = 0
    pure_text_asst = 0
    has_rc_with_tc = 0
    has_rc_pure_text = 0

    for m in oai_data.get("messages", []):
        if m.get("role") != "assistant":
            continue
        total_asst += 1

        tc = m.get("tool_calls", [])
        has_tc = len(tc) > 0
        total_tool_calls += len(tc)

        rc = m.get("reasoning_content", "")
        has_rc = isinstance(rc, str) and rc.strip() != ""

        if has_tc:
            if has_rc:
                has_rc_with_tc += 1
        else:
            pure_text_asst += 1
            if has_rc:
                has_rc_pure_text += 1

    numerator = has_rc_pure_text + has_rc_with_tc
    denominator = pure_text_asst + has_rc_with_tc
    ratio = numerator / denominator if denominator > 0 else 0

    return {
        "total_asst": total_asst,
        "total_tool_calls": total_tool_calls,
        "numerator": numerator,
        "denominator": denominator,
        "ratio": ratio,
    }


def main():
    parser = argparse.ArgumentParser(description="Calculate reasoning ratio for OpenAI trajectories")
    parser.add_argument("--output-dir", "-o", default=DEFAULT_OUTPUT_DIR, help="Directory with .openai.json files")
    args = parser.parse_args()

    output_dir = os.path.expanduser(args.output_dir)
    oai_files = sorted(glob.glob(os.path.join(output_dir, "*.openai.json")))

    if not oai_files:
        print("No .openai.json files found.", file=sys.stderr)
        sys.exit(1)

    rows = []
    for oai_path in oai_files:
        sid = os.path.basename(oai_path).replace(".openai.json", "")

        with open(oai_path, "r", encoding="utf-8") as f:
            oai_data = json.load(f)

        # Get title from stats if available
        stats_path = os.path.join(output_dir, f"{sid}.stats.json")
        title = ""
        turns = 0
        if os.path.exists(stats_path):
            with open(stats_path, "r", encoding="utf-8") as f:
                stats = json.load(f)
            title = stats.get("title", "")
            turns = stats.get("turns", 0)

        if not title:
            title = "(无标题)"

        result = calc_reasoning_ratio(oai_data)
        rows.append({
            "sid": sid,
            "title": title,
            "turns": turns,
            **result,
        })

    # Print table
    print(f"| 序号 | session_id | 标题 | 轮次 | 工具调用 | 带reasoning | 总条数(排除纯tool) | 比例 |")
    print(f"|------|-----------|------|------|---------|------------|-------------------|------|")

    for i, r in enumerate(rows, 1):
        ratio_str = f"{r['ratio']:.0%}" if r["denominator"] > 0 else "N/A"
        mark = "✓" if r["ratio"] >= 0.5 else "✗"
        print(f"| {i:2d} | {r['sid']} | {r['title']} | {r['turns']} | {r['total_tool_calls']} | {r['numerator']} | {r['denominator']} | {ratio_str} {mark} |")

    pass_count = sum(1 for r in rows if r["ratio"] >= 0.5)
    avg_ratio = sum(r["ratio"] for r in rows) / len(rows) if rows else 0
    print(f"\nPASS(>=50%): {pass_count}/{len(rows)}  平均: {avg_ratio:.0%}")


if __name__ == "__main__":
    main()
