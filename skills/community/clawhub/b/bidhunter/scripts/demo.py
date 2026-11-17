#!/usr/bin/env python3
"""
demo.py - Generate a sample report from bundled demo data (BidHunter v1.5, A7).

Lets a new user SEE the actual output (verdict + score + calendar) before
configuring their own rules. No network, no external data.

Usage:
  python3 demo.py                # full sample report (text)
  python3 demo.py --summary      # top-5 essence
  python3 demo.py --calendar     # also show bid calendar from sample
"""
import os
import sys
import argparse
import subprocess

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SAMPLES = os.path.join(SCRIPT_DIR, "samples")
RULES = os.path.join(SAMPLES, "demo_rules.json")
CACHE = os.path.join(SAMPLES, "demo_cache.jsonl")
QUAL = os.path.join(SAMPLES, "demo_qual.jsonl")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--summary", action="store_true")
    ap.add_argument("--calendar", action="store_true")
    args = ap.parse_args()

    py = sys.executable
    # qualify
    r = subprocess.run([py, os.path.join(SCRIPT_DIR, "qual_check.py"), CACHE, RULES],
                       stdout=open(QUAL, "w", encoding="utf-8"), stderr=subprocess.DEVNULL)
    if r.returncode != 0:
        print("demo qualify failed", file=sys.stderr)
        sys.exit(1)

    # text report
    cmd = [py, os.path.join(SCRIPT_DIR, "report_text.py"), QUAL, "DEMO"]
    if args.summary:
        cmd.append("--summary")
    out = subprocess.run(cmd, capture_output=True, text=True)
    print(out.stdout)

    if args.calendar:
        print()
        cal = subprocess.run([py, os.path.join(SCRIPT_DIR, "calendar.py"), QUAL, "--days", "30"],
                             capture_output=True, text=True)
        print(cal.stdout)

    print("\n—" * 24)
    print("✅ 以上为示例效果。配置你自己的规则：")
    print("   1) 复制 scripts/samples/demo_rules.json → 你的 qual_rules.json")
    print("   2) 按营业执照改 entities / red_alerts / region_priority")
    print("   3) 运行 python3 doctor.py 自检，再 bash pipeline.sh 跑真实采集")


if __name__ == "__main__":
    main()
