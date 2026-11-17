#!/usr/bin/env python3
"""forge_runbook.py — 成功路径脚本化（P1-5 / G10）。

把 S2 真机取证阶段验证过的命令（写在 references/*_evidence.md 的代码块里）
沉淀为**确定性可重跑的 runbook**，让"成功路径"不只是文档，而是程序：
  python scripts/forge_runbook.py init <技能目录>     # 扫描证据→生成 runbook.md + run_verified.py
  python scripts/forge_runbook.py list <技能目录>     # 列出已沉淀的步骤锚点

生成物：
  references/runbook.md    人类可读的成功路径目录（每步附证据来源）
  scripts/run_verified.py  按锚点执行某步（默认 --dry-run 安全，--exec 才真跑）

SKILL.md 动作段应改为锚点链接指向 run_verified.py（见 P2-4 最短化 + 锚点化）。
"""
import argparse
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))

# 证据文件里的代码块：```bash / ```shell / ```sh / ``` 含命令
CODE_FENCE = re.compile(r"```(?:bash|shell|sh|console|cmd)?\s*\n(.*?)```", re.S)
# 行内命令（以 $ 或 > 或 直接 python/xxx 开头，且像命令）
INLINE_CMD = re.compile(r"^\s*[\$>]\s*(.+)$")
# 锚点化：把命令首词/路径变成可读锚点
ANCHOR_CLEAN = re.compile(r"[^\w\-]+")


def _extract_commands(text):
    """从证据文本抽出命令列表（去提示符、去空行）。"""
    cmds = []
    for block in CODE_FENCE.findall(text):
        for line in block.splitlines():
            line = line.rstrip()
            if not line.strip():
                continue
            m = INLINE_CMD.match(line)
            if m:
                line = m.group(1)
            # 跳过纯输出行（无空格或明显是路径输出）
            if line.startswith(("#", "//")):
                continue
            cmds.append(line)
    return cmds


def _anchor_of(cmd, idx):
    """生成可读锚点：取命令前两个 token，清洗。"""
    toks = re.split(r"\s+", cmd.strip())
    head = toks[0] if toks else "step"
    head = head.replace("python", "").replace("scripts/", "").replace("./", "")
    head = head.replace("/", "-").replace("\\", "-")
    head = ANCHOR_CLEAN.sub("-", head).strip("-") or "step"
    return f"{idx:02d}-{head}"


def _scan_evidence(sd):
    """扫描 references/*_evidence.md，返回 [(锚点, 命令, 来源文件)]。"""
    ref = os.path.join(sd, "references")
    if not os.path.isdir(ref):
        return []
    out = []
    idx = 0
    for fn in sorted(os.listdir(ref)):
        if not fn.endswith("_evidence.md"):
            continue
        text = open(os.path.join(ref, fn), encoding="utf-8").read()
        for cmd in _extract_commands(text):
            idx += 1
            out.append((_anchor_of(cmd, idx), cmd, fn))
    return out


def cmd_init(sd):
    sd = os.path.abspath(os.path.expanduser(sd))
    steps = _scan_evidence(sd)
    if not steps:
        print(f"✗ 未从 references/*_evidence.md 扫到任何命令（先完成 S2 真机取证）")
        return 1
    # 写 runbook.md
    rb = os.path.join(sd, "references", "runbook.md")
    lines = ["# 成功路径 Runbook（由 forge_runbook.py 自动生成）", "",
             "> 本文件沉淀 S2 真机取证验证过的命令，按锚点可重跑（见 scripts/run_verified.py）。",
             "> 任何一步改动后，重跑本技能的自测以确认成功路径未退化。", ""]
    for anchor, cmd, src in steps:
        lines.append(f"## {anchor}")
        lines.append(f"- 来源证据: `references/{src}`")
        lines.append(f"- 命令: `{cmd}`")
        lines.append("")
    open(rb, "w", encoding="utf-8").write("\n".join(lines))
    # 写 run_verified.py
    rv = os.path.join(sd, "scripts", "run_verified.py")
    os.makedirs(os.path.dirname(rv), exist_ok=True)
    rv_content = _render_run_verified(steps, sd)
    open(rv, "w", encoding="utf-8").write(rv_content)
    print(f"✓ 生成 {len(steps)} 个成功路径步骤：")
    print(f"  - references/runbook.md")
    print(f"  - scripts/run_verified.py")
    print(f"  下一步：SKILL.md 动作段改为锚点链接 → run_verified.py <锚点>（见 P2-4）")
    return 0


def _render_run_verified(steps, sd):
    anchors = "\n".join(f'    "{a}": "{c}",' for a, c, _ in steps)
    return f'''#!/usr/bin/env python3
"""run_verified.py — 按锚点执行成功路径步骤（自动生成，勿手改）。

python scripts/run_verified.py --list          # 列出步骤
python scripts/run_verified.py <锚点>           # 默认 --dry-run 打印命令
python scripts/run_verified.py <锚点> --exec    # 真跑（在技能目录内）
"""
import argparse, os, subprocess, sys

STEPS = {{
{anchors}
}}

SKILL_DIR = r"{sd}"

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("anchor", nargs="?", help="步骤锚点")
    ap.add_argument("--list", action="store_true")
    ap.add_argument("--exec", action="store_true", help="真跑（默认仅打印）")
    args = ap.parse_args()
    if args.list or not args.anchor:
        for a in STEPS:
            print(a, "->", STEPS[a])
        return 0
    if args.anchor not in STEPS:
        print("✗ 未知锚点:", args.anchor); return 2
    cmd = STEPS[args.anchor]
    print(("EXEC " if args.exec else "DRY  ") + cmd)
    if args.exec:
        r = subprocess.run(cmd, shell=True, cwd=SKILL_DIR)
        return r.returncode
    return 0

if __name__ == "__main__":
    sys.exit(main())
'''


def cmd_list(sd):
    steps = _scan_evidence(os.path.abspath(os.path.expanduser(sd)))
    if not steps:
        print("（无已沉淀步骤）")
        return 0
    for anchor, cmd, src in steps:
        print(f"  {anchor}  <-  {cmd[:60]}")
    return 0


def main():
    ap = argparse.ArgumentParser(description="成功路径 runbook 生成")
    sub = ap.add_subparsers(dest="cmd", required=True)
    p_init = sub.add_parser("init"); p_init.add_argument("skill_dir")
    p_list = sub.add_parser("list"); p_list.add_argument("skill_dir")
    args = ap.parse_args()
    if args.cmd == "init":
        return cmd_init(args.skill_dir)
    if args.cmd == "list":
        return cmd_list(args.skill_dir)


if __name__ == "__main__":
    sys.exit(main())
