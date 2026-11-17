#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""audit_agent_responsiveness.py —— 「重活外派 · 随时应答」机制体检（跨平台）。

检查什么
    1. 探测本机有哪些受支持的 Agent 环境（Hermes / Claude Code）；
    2. 逐个落地目标核对：规则块是否存在、是否被标记包裹、是否置顶、内容是否与当前模板一致；
    3. 探测不到任何受支持平台时，如实输出「未检测到支持的平台」，**不假报通过**。

诚实边界
    * 只报告文件层面能核实的**事实**（存在 / 位置 / 内容是否一致），不臆测运行时生效情况。
    * 探测不到的路径一律标为「未探测到」，绝不当成通过。

用法
    python3 audit_agent_responsiveness.py
    python3 audit_agent_responsiveness.py --json
    python3 audit_agent_responsiveness.py --hermes-home /tmp/fake-hermes --claude-home /tmp/fake-claude

退出码
    0  全部目标通过（且至少检查到一个目标）
    1  有目标不通过
    2  未检测到任何受支持的平台（无法判定，不算通过）
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))  # 允许与落地器同目录导入

from provision_agent_responsiveness import (  # noqa: E402
    EXPORT_FILE_NAME,
    LEGACY_MARK,
    RULES_END,
    RULES_START,
    discover,
    extract_block,
    load_rules,
    norm,
)

TOP_POSITION_LIMIT = 800  # 规则块起始位置超过这个字符数就算「太靠后」


def _reconfigure_stdout() -> None:
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")  # type: ignore[attr-defined]
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")  # type: ignore[attr-defined]
    except Exception:  # noqa: BLE001
        pass


def check_target(path_str: str, block: str) -> dict:
    """核实单个目标的文件层面事实。返回 dict（不修改任何文件）。"""
    path = Path(path_str)
    rec = {"path": str(path), "exists": path.is_file(), "has_block": False, "top": False,
           "position": None, "up_to_date": False, "legacy": False, "note": ""}
    if not rec["exists"]:
        rec["note"] = "文件不存在"
        return rec
    try:
        text = path.read_text(encoding="utf-8")
    except OSError as exc:
        rec["note"] = "读取失败：%s" % exc
        return rec
    flat = text.replace("\r\n", "\n").replace("\r", "\n")
    rec["legacy"] = LEGACY_MARK in flat
    if RULES_START not in flat or RULES_END not in flat:
        rec["note"] = "未找到规则块标记（旧版规则块或从未安装）"
        return rec
    rec["has_block"] = True
    rec["position"] = flat.find(RULES_START)
    rec["top"] = rec["position"] <= max(TOP_POSITION_LIMIT, len(flat) // 3)
    existing = extract_block(text) or ""
    rec["up_to_date"] = norm(existing) == norm(block)
    if not rec["up_to_date"]:
        rec["note"] = "内容与当前模板不一致（模板已升级，建议重跑落地器 --apply）"
    return rec


def run(args: argparse.Namespace) -> int:
    script_file = Path(__file__).resolve()
    block, block_source = load_rules(script_file)

    ns = argparse.Namespace(
        hermes_home=args.hermes_home,
        claude_home=args.claude_home,
        out="",
        export=False,
        dry_run=True,
        json_output=False,
    )
    targets, platforms = discover(ns)

    results = []
    for t in targets:
        rec = check_target(t["path"], block)
        rec["platform"] = t["platform"]
        rec["scope"] = t["scope"]
        results.append(rec)

    def _ok(r: dict) -> bool:
        return bool(r["has_block"] and r["top"] and r["up_to_date"])

    passed = [r for r in results if _ok(r)]
    failed = [r for r in results if not _ok(r)]

    export_path = Path.cwd() / EXPORT_FILE_NAME
    export_info = {"path": str(export_path), "exists": export_path.is_file()}

    # 探测不到任何受支持平台：如实说明，不当通过
    if not targets:
        if args.json_output:
            sys.stdout.write(json.dumps({
                "supportedPlatformFound": False,
                "platforms": platforms,
                "targets": [],
                "exportedRulesFile": export_info,
                "verdict": "未检测到支持的平台",
            }, ensure_ascii=False, indent=2) + "\n")
        else:
            print("未检测到支持的平台（Hermes / Claude Code 均未探测到）——无法判定，本次不计通过。")
            print("")
            print("探测过的位置：")
            for p in platforms:
                print("  - %s：%s（%s）" % (p["platform"], p["detail"], "已探测" if p["detected"] else "不存在"))
            print("")
            print("这类平台请走「导出可粘贴规则块」路径：")
            print("  1) 运行 provision_agent_responsiveness.py --apply --export")
            print("     会在 %s 生成一份规则块（默认 ./%s）" % (export_path, EXPORT_FILE_NAME))
            print("  2) 把该文件内容粘到你的系统提示 / 自定义指令 / 项目规则里，即生效。")
        return 2

    if args.json_output:
        sys.stdout.write(json.dumps({
            "supportedPlatformFound": True,
            "rulesSource": block_source,
            "platforms": platforms,
            "targets": results,
            "exportedRulesFile": export_info,
            "verdict": "全部通过" if not failed else "%d 项不通过" % len(failed),
        }, ensure_ascii=False, indent=2) + "\n")
        return 0 if not failed else 1

    print("重活外派 · 随时应答 —— 机制体检")
    print("规则块模板来源：%s" % block_source)
    print("")
    print("① 平台探测")
    for p in platforms:
        print("  %-12s %s  %s" % (p["platform"], "✅ 探测到" if p["detected"] else "— 未探测到", (p.get("detail") or p["root"])))
    print("")
    print("② 落地目标检查")
    header = ("目标", "规则块", "置顶", "内容最新", "结论")
    print("  %-52s %-8s %-6s %-9s %s" % header)
    print("  " + "-" * 88)
    for r in results:
        verdict = "✅ 通过" if r in passed else "❌ 不通过"
        print("  %-52s %-8s %-6s %-9s %s" % (
            _short(r["path"], 50),
            "✅" if r["has_block"] else "❌",
            ("✅" if r["top"] else "⚠️ 靠后") if r["has_block"] else "—",
            "✅" if r["up_to_date"] else "❌",
            verdict,
        ))
        if r["note"]:
            print("       └ %s" % r["note"])
        if r["legacy"] and not r["has_block"]:
            print("       └ 检测到 v1.0 版规则块（无标记包裹）：请手工替换或删除后重跑落地器")
    print("")
    print("③ 可粘贴规则块（非受支持平台的兜底路径）")
    print("  %s：%s" % (export_path, "已存在" if export_info["exists"] else "未生成"))
    print("")
    print("合计：%d/%d 项通过" % (len(passed), len(results)))
    if failed:
        print("未通过项：")
        for r in failed:
            print("  - %s（%s）" % (r["path"], r["note"] or "规则块缺失 / 未置顶 / 非最新"))
        print("修复：provision_agent_responsiveness.py --apply")
    return 0 if not failed else 1


def _short(text: str, limit: int) -> str:
    return text if len(text) <= limit else "…" + text[-(limit - 1):]


def build_parser() -> argparse.ArgumentParser:
    ap = argparse.ArgumentParser(
        prog="audit_agent_responsiveness.py",
        description="跨平台体检「重活外派 · 随时应答」规则块是否已落地且为最新。",
    )
    ap.add_argument("--json", dest="json_output", action="store_true", help="以 JSON 输出")
    ap.add_argument("--hermes-home", default="", help="覆盖 Hermes 主目录")
    ap.add_argument("--claude-home", default="", help="覆盖 Claude Code 配置目录")
    return ap


def main(argv: list[str] | None = None) -> int:
    _reconfigure_stdout()
    args = build_parser().parse_args(argv)
    return run(args)


if __name__ == "__main__":
    sys.exit(main())
