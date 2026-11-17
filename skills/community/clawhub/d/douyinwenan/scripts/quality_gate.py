# -*- coding: utf-8 -*-
"""质量门禁统一入口 — 一键跑三项检查，输出结构化报告

用法:
  python quality_gate.py "文案文本"
  python quality_gate.py --file draft.txt
  python quality_gate.py --json "文案文本"

判定:
  PASS    — 三项全部通过
  WARN    — 有警告（AI味警告/夸大词），可发布但建议修改
  FAIL    — 有红线（AI味过重/违禁词/事实点未核验），必须修改
"""
import argparse
import json
import os
import subprocess
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))


def run(script, text):
    """调用子脚本，返回 (exit_code, parsed_json)"""
    cmd = [sys.executable, os.path.join(SCRIPT_DIR, script), "--json", text]
    try:
        proc = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", timeout=30)
        data = json.loads(proc.stdout) if proc.stdout.strip() else {}
        return proc.returncode, data
    except Exception as e:
        return 1, {"error": str(e)}


def main():
    parser = argparse.ArgumentParser(description="质量门禁")
    parser.add_argument("text", nargs="?", help="文案文本")
    parser.add_argument("--file", help="从文件读取")
    parser.add_argument("--json", action="store_true", help="输出 JSON")
    args = parser.parse_args()

    if args.file:
        with open(args.file, encoding="utf-8") as f:
            text = f.read()
    elif args.text:
        text = args.text
    else:
        print("用法: python quality_gate.py '文案' 或 --file draft.txt")
        sys.exit(1)

    tone_rc, tone = run("check_ai_tone.py", text)
    facts_rc, facts = run("verify_facts.py", text)
    comp_rc, comp = run("check_compliance.py", text)

    tone_score = tone.get("score", 0)
    fact_count = facts.get("count", 0)
    comp_total = comp.get("total", 0)
    comp_redline = (len(comp.get("absolute", [])) + len(comp.get("promise", []))
                    + len(comp.get("drain", [])))

    # 判定
    issues = []
    if tone_score < 85:
        issues.append(f"AI味得分 {tone_score}/100 (<85)")
    if comp_redline > 0:
        issues.append(f"违禁红线词 {comp_redline} 个")
    if fact_count == 0:
        issues.append("无数据支撑（传播力弱）")

    if issues:
        verdict = "FAIL" if (tone_score < 70 or comp_redline > 0) else "WARN"
    else:
        verdict = "PASS"

    report = {
        "verdict": verdict,
        "ai_tone_score": tone_score,
        "fact_points": fact_count,
        "compliance_redline": comp_redline,
        "compliance_total": comp_total,
        "issues": issues,
    }

    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        print("=== 质量门禁报告 ===")
        print(f"判定: {verdict}")
        print(f"AI味得分: {tone_score}/100")
        print(f"事实点: {fact_count} 个 (需人工核对)")
        print(f"违禁词: {comp_total} 个 (红线 {comp_redline})")
        if issues:
            print("问题:")
            for i in issues:
                print(f"  - {i}")
        else:
            print("全部通过。")
        print("\n提示: 事实点仍需人工核对来源，脚本不替代人工判断。")

    sys.exit(0 if verdict == "PASS" else 1)


if __name__ == "__main__":
    main()
