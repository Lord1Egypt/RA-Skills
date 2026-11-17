#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""studio.py - 企业技能工程台统一 CLI 入口（薄 harness）

把全部子脚本收为一个入口，降低使用摩擦：
  - 统一子命令：`studio review ...` 而非记住十几个文件路径
  - 参数透传：每个子命令的其余参数直接交给底层脚本（含 --help）
  - 统一解释器：用当前 python 运行，无需手动激活
  - 新增 `studio gate`：发布前卡点，同时跑【安全体检 + 移植体检】

设计原则（贴合本技能"厚技能+薄 harness"）：
  智能封装在各子脚本里，studio.py 只做"发现+分发"。

用法：
  studio -h                        # 列出全部子命令
  studio review .                  # 审查当前技能
  studio review . --json          # 审查并输出 JSON
  studio cross-platform . --platform codex   # 移植体检
  studio gate . --platform codex   # 发布前卡点：安全+移植 双体检
  studio maturity --answers a.json
  studio compose --spec wf.json
  studio portal --skills-dir ../..
  studio usage report --log usage.jsonl
  studio <子命令> --help           # 看底层脚本帮助
"""

import argparse
import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))

# 子命令 -> 底层脚本（统一放置于 scripts/ 同目录）
SCRIPTS = {
    "review":          "review_checklist.py",
    "upgrade":         "upgrade_skill.py",
    "maturity":        "maturity_assess.py",
    "lifecycle":       "lifecycle_track.py",
    "roi":             "roi_filter.py",
    "evolution":       "evolution_log.py",
    "dupe":            "dupe_check.py",
    "training":        "training_pack.py",
    "cross-platform":  "cross_platform_check.py",
    "compose":         "compose.py",
    "eval":            "eval_gen.py",
    "portal":          "portal.py",
    "usage":           "usage_tracker.py",
    "update":          "update_skill.py",
    "audit":           "skillsec_audit.py",
}

# 一句话说明，用于 `studio -h` 的帮助
HELP = {
    "review":         "审查技能（安全8/CISO5/质量5/厚技能/事务安全/AI安全）",
    "upgrade":        "个人技能 -> 企业级技能升级器",
    "maturity":       "体系成熟度自测（L0-L4，含 Agentic 维度）",
    "lifecycle":      "生命周期注册表追踪 + 弃用候选",
    "roi":            "ROI 筛选（频次/时长/成本门槛 -> BUILD/HOLD）",
    "evolution":      "维护 Evolution Log 条目",
    "dupe":           "技能重名/功能重叠检测（查重复用）",
    "training":       "生成培训推广包四件套骨架",
    "cross-platform": "跨平台适配合规检查",
    "compose":        "生成多技能编排器骨架",
    "eval":           "生成评测套件（应触发/不应/边界）",
    "portal":         "技能库 -> 门户目录/README/HTML",
    "usage":          "成本/计量追踪（半自动 usage 日志）",
    "update":          "自更新：检查/应用本技能自身更新（--check/--apply/--backup/--dry-run）",
    "audit":           "技能安全审计（SkillSec 16 类，方法论借鉴 NVIDIA SkillSpector）",
}


def build_parser():
    p = argparse.ArgumentParser(
        prog="studio",
        description="企业技能工程台统一 CLI（薄 harness 调度各子脚本）",
    )
    sub = p.add_subparsers(dest="cmd", required=True, metavar="<子命令>")

    for name, script in SCRIPTS.items():
        sp = sub.add_parser(name, help=HELP.get(name, f"运行 {script}"))
        sp.add_argument(
            "rest",
            nargs=argparse.REMAINDER,
            help=f"透传给 {script} 的参数（可加 --help 查看）",
        )
    # 特殊子命令：gate（发布前双体检，非简单透传）
    gp = sub.add_parser("gate", help="发布前卡点：安全体检 + 移植体检 同时跑")
    gp.add_argument("--skill", required=True, help="目标技能目录（含 SKILL.md）")
    gp.add_argument("--platform", help="仅针对某平台做移植体检：" + "/".join(
        ["workbuddy", "claude-code", "codex", "cursor", "loong", "hermes"]))
    gp.add_argument("--json", action="store_true", help="输出 JSON（含两段原始报告）")
    return p


def build_gate_parser():
    """gate 子命令专用 parser（普通子命令走 argv 切片透传，不走此 parser）。"""
    gp = argparse.ArgumentParser(
        prog="studio gate",
        description="发布前卡点：安全体检 + 移植体检 同时跑",
    )
    gp.add_argument("--skill", required=True, help="目标技能目录（含 SKILL.md）")
    gp.add_argument("--platform", help="仅针对某平台做移植体检：" + "/".join(
        ["workbuddy", "claude-code", "codex", "cursor", "loong", "hermes"]))
    gp.add_argument("--json", action="store_true", help="输出 JSON（含两段原始报告）")
    return gp


def run_gate(skill, platform, as_json):
    """发布前卡点：同时跑安全体检(review) + 移植体检(cross-platform)。
    返回码：2=BLOCK（任一未通过），0=PASS。"""
    review = os.path.join(HERE, "review_checklist.py")
    cross = os.path.join(HERE, "cross_platform_check.py")
    if not os.path.isdir(skill):
        sys.stderr.write(f"[studio] 目录不存在: {skill}\n")
        return 2
    if not os.path.isfile(os.path.join(skill, "SKILL.md")):
        sys.stderr.write(f"[studio] 目录内无 SKILL.md: {skill}\n")
        return 2

    r1 = subprocess.run([sys.executable, review, skill], capture_output=True, text=True)
    cargs = [sys.executable, cross, "--skill", skill]
    if platform:
        cargs += ["--platform", platform]
    r2 = subprocess.run(cargs, capture_output=True, text=True)

    review_block = (r1.returncode == 1)   # review 返回 1 = 存在 FAIL
    cross_block = (r2.returncode == 2)     # cross 返回 2 = BLOCK
    block = review_block or cross_block

    if as_json:
        payload = {
            "skill": skill,
            "platform": platform,
            "security": {"returncode": r1.returncode, "report": r1.stdout.strip()},
            "portability": {"returncode": r2.returncode, "report": r2.stdout.strip()},
            "verdict": "BLOCK" if block else "PASS",
        }
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    else:
        print("=" * 64)
        print("技能发布前卡点 —— 安全体检 + 移植体检")
        print(f"目标技能: {skill}")
        if platform:
            print(f"目标平台: {platform}")
        print("=" * 64)
        print("\n—— [1/2] 安全体检（review_checklist） ——")
        print(r1.stdout.strip() or r1.stderr.strip())
        print("\n—— [2/2] 移植体检（cross_platform_check） ——")
        print(r2.stdout.strip() or r2.stderr.strip())
        print("\n" + "=" * 64)
        if block:
            reasons = []
            if review_block:
                reasons.append("安全体检存在 FAIL")
            if cross_block:
                reasons.append("移植体检 BLOCK")
            print("结论: ❌ BLOCK —— " + "；".join(reasons))
        else:
            print("结论: ✅ PASS —— 安全与移植体检均通过，可发布/移植。")
        print("=" * 64)
    return 2 if block else 0


def main(argv=None):
    # 薄 harness：子命令之后全部参数原样切片透传底层脚本，避免 argparse
    # 子命令 + REMAINDER 在首个 `-` 选项上的解析坑（薄 harness 不该再解析一次）。
    raw = sys.argv[1:] if argv is None else list(argv)
    if not raw:
        build_parser().print_help()
        return 2
    cmd = raw[0]
    if cmd in ("-h", "--help"):
        build_parser().print_help()
        return 0
    rest = raw[1:]
    if cmd == "gate":
        try:
            a = build_gate_parser().parse_args(rest)
        except SystemExit:
            return 2
        return run_gate(a.skill, a.platform, a.json)
    if cmd not in SCRIPTS:
        sys.stderr.write(f"[studio] 未知子命令: {cmd}\n")
        return 2
    target = os.path.join(HERE, SCRIPTS[cmd])
    if not os.path.isfile(target):
        sys.stderr.write(f"[studio] 未找到底层脚本: {target}\n")
        return 2
    cmdline = [sys.executable, target] + rest
    try:
        r = subprocess.run(cmdline)
    except KeyboardInterrupt:
        return 130
    return r.returncode


if __name__ == "__main__":
    sys.exit(main())
