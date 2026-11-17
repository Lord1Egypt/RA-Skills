# -*- coding: utf-8 -*-
"""scam-radar tests/ 快照治理工具（与 scripts/radar_check.py 配套）。

用法（在 tests/ 目录下）：
    python regen_snapshots.py            # 重生成全部快照（脚本改动后跑）
    python regen_snapshots.py --verify   # 不改文件，只把当前脚本输出与快照对比，报漂移

约定：scripts/radar_check.py 任何改动（哪怕只是文案）→ 跑 regenerate；
verify 非零退出 = 快照已漂移，先 review 差异再重生成，不要盲跑覆盖。
"""
import argparse
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
SCRIPT = HERE.parent / "scripts" / "radar_check.py"

# (args, 输出快照列表)
JOBS = [
    (["--input", str(HERE / "case_full.json")], ["report_full.md", "report_case_full.md"]),
    (["--input", str(HERE / "case_partial.json")], ["report_partial.md", "report_case_partial.md"]),
    (["--input", str(HERE / "case_clean.json")], ["report_clean.md", "report_case_clean.md"]),
    (["--input", str(HERE / "case_crypto.json")], ["report_crypto.md", "report_case_crypto.md"]),
    (["--scenario", "stockgroup"], ["report_s_stockgroup.md"]),
    (["--scenario", "cheapcourse"], ["report_s_cheapcourse.md"]),
    (["--scenario", "unknownapp"], ["report_s_unknownapp.md"]),
    (["--scenario", "insurancemixed"], ["report_s_insurancemixed.md"]),
]


def _run_case(script, args):
    return subprocess.run(
        [sys.executable, "-X", "utf8", str(script)] + args,
        capture_output=True, text=True, encoding="utf-8", errors="replace")


def regen():
    drifted = []
    for args, outs in JOBS:
        generate = _run_case(SCRIPT, args)
        if generate.returncode != 0:
            drifted.append(f"脚本运行失败 rc={generate.returncode} args={args}")
            print(f"!! 脚本失败 rc={generate.returncode} {args}")
            continue
        if "COMPLIANCE" in (generate.stderr or ""):
            drifted.append(f"合规告警 args={args}")
            print(f"!! 合规告警 {args}：{generate.stderr.strip()[:120]}")
        for out in outs:
            (HERE / out).write_text(generate.stdout, encoding="utf-8", newline="\n")
            again = _run_case(SCRIPT, args)
            if again.stdout != generate.stdout:
                drifted.append(f"{out} 连续两次生成不一致（脚本含随机性？）")
                print(f"!! 非确定性 {out}")
            else:
                print(f"OK {out}")
    print("regenerate 完成" + (f"，但有 {len(drifted)} 项问题：{drifted}" if drifted else "，0 项问题"))
    return 1 if drifted else 0


def verify():
    bad = []
    for args, outs in JOBS:
        r = _run_case(SCRIPT, args)
        if r.returncode != 0:
            bad.append(f"{outs[0]}: 脚本 rc={r.returncode}")
            continue
        for out in outs:
            stored = (HERE / out).read_text(encoding="utf-8").replace("\r\n", "\n").strip()
            if r.stdout.replace("\r\n", "\n").strip() != stored:
                bad.append(out)
                print(f"漂移  {out}")
            else:
                print(f"一致  {out}")
    print("verify " + ("全部一致" if not bad else f"发现 {len(bad)} 处漂移：{bad}"))
    return 0 if not bad else 1


def main():
    ap = argparse.ArgumentParser(description="scam-radar 快照治理（regenerate / verify）")
    ap.add_argument("--verify", action="store_true", help="只验证不覆盖")
    a = ap.parse_args()
    sys.exit(verify() if a.verify else regen())


if __name__ == "__main__":
    main()
