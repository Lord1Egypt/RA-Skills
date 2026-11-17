#!/usr/bin/env python3
"""CLI entry: inventory by default; deep analyze only with explicit --conv."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from analyze import analyze_conversation
from core import load_config, redact_path
from inventory import format_inventory_text, inventory_conversations, resolve_target
from load_export import load_input
from quality_gate import assert_no_default_max_group, gate_deep, gate_inventory
from report_builder import ALLOWED_FORMATS, write_reports

HELP_EPILOG = """
示例:
  python3 scripts/run.py -i export.jsonl
  python3 scripts/run.py -i export.jsonl --conv 1
  python3 scripts/run.py -i export.jsonl --conv 1 --person 于先生 --owner-alias '群主'

无导出文件时请先自备数据（本 skill 不登录 IM）:
  references/how-to-get-exports.md
"""



def _public_paths(paths: dict) -> dict:
    """CLI/JSON 对外只暴露脱敏路径，避免把本机 output 绝对路径打进管道。"""
    out = {}
    for k, v in (paths or {}).items():
        out[k] = redact_path(str(v))
    return out

def main(argv=None) -> int:
    p = argparse.ArgumentParser(
        description="Douyin Chat Insight — 用户自备导出 → inventory → 点选深挖 → 单页报告",
        epilog=HELP_EPILOG,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    p.add_argument("--version", action="version", version="douyin-chat-insight 0.1.3")
    p.add_argument("--input", "-i", required=True, type=Path, help="导出文件或目录")
    p.add_argument("--conv", help="会话编号(#1)/名称/id；深挖必填")
    p.add_argument("--person", help="只看某人发言（昵称模糊匹配）")
    p.add_argument("--deep", action="store_true", help="显式深挖（仍必须 --conv）")
    p.add_argument("--inventory-only", action="store_true", help="只出概况")
    p.add_argument("--output-dir", "-o", type=Path, help="报告目录")
    p.add_argument("--config", type=Path)
    p.add_argument("--owner-alias", action="append", default=[], help="临时群主别名")
    p.add_argument("--formats", default="html,md,json", help="html,md,json 逗号分隔")
    p.add_argument("--json", action="store_true", help="stdout 打印 JSON")
    args = p.parse_args(argv)

    cfg = load_config(args.config)
    if args.owner_alias:
        aliases = list(cfg.get("owner_aliases") or [])
        for a in args.owner_alias:
            if a not in aliases:
                aliases.append(a)
        cfg["owner_aliases"] = aliases

    try:
        convs = load_input(args.input)
    except FileNotFoundError as e:
        print(f"ERROR: 找不到输入路径 — {e}", file=sys.stderr)
        print("提示: 请传入已存在的导出文件/目录。如何自备导出见 references/how-to-get-exports.md", file=sys.stderr)
        return 2
    except PermissionError as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return 2
    except ValueError as e:
        print(f"ERROR: 无法解析导出 — {e}", file=sys.stderr)
        print("支持: ChatLab JSONL / JSON 数组 / 纯文本「昵称: 内容」。见 references/input-formats.md", file=sys.stderr)
        return 2
    except Exception as e:
        print(f"ERROR: 读取失败 — {type(e).__name__}: {e}", file=sys.stderr)
        return 2

    inv = inventory_conversations(convs, cfg)
    ok, msgs = gate_inventory(inv)
    warns = [m for m in msgs if m.startswith("WARN:")]
    errs = [m for m in msgs if not m.startswith("WARN:")]
    for wmsg in warns:
        print(wmsg, file=sys.stderr)
    if not ok:
        print("QUALITY_GATE_FAIL:", "; ".join(errs), file=sys.stderr)
        return 2

    if args.person and not args.conv and not args.inventory_only:
        # person alone implies deep but still needs conv — fail early with inventory
        pass
    want_deep = bool(args.deep or args.conv or args.person)
    if args.inventory_only:
        want_deep = False

    formats = [x.strip().lower() for x in args.formats.split(",") if x.strip()]
    bad = [f for f in formats if f not in ALLOWED_FORMATS]
    if bad:
        print(f"ERROR: 不支持的格式 {bad}；允许: {sorted(ALLOWED_FORMATS)}", file=sys.stderr)
        return 2
    if not formats:
        formats = ["html", "md", "json"]

    if not want_deep:
        out_dir = Path(args.output_dir or cfg.get("output_dir") or "output/douyin-chat-insight")
        try:
            paths = write_reports(inv, out_dir, formats)
        except OSError as e:
            print(f"ERROR: 无法写入报告目录 {out_dir}: {e}", file=sys.stderr)
            return 2
        if args.json:
            print(json.dumps({**inv, "report_paths": _public_paths(paths)}, ensure_ascii=False, indent=2))
        else:
            print(format_inventory_text(inv))
            print("报告:", _public_paths(paths))
        return 0

    try:
        assert_no_default_max_group(True, bool(args.conv))
        target = resolve_target(convs, conv=args.conv, person=args.person)
    except ValueError as e:
        print(f"ERROR: {e}", file=sys.stderr)
        print(format_inventory_text(inv), file=sys.stderr)
        return 2

    try:
        result = analyze_conversation(target, cfg, person=args.person)
    except ValueError as e:
        print(f"ERROR: {e}", file=sys.stderr)
        print("提示: 检查 --person 是否匹配，或导出是否仅有系统/卡片消息。", file=sys.stderr)
        return 2

    ok, errs = gate_deep(result)
    if not ok:
        print("QUALITY_GATE_FAIL:", "; ".join(errs), file=sys.stderr)
        return 2

    out_dir = Path(args.output_dir or cfg.get("output_dir") or "output/douyin-chat-insight")
    try:
        paths = write_reports(result, out_dir, formats)
    except OSError as e:
        print(f"ERROR: 无法写入报告目录 {out_dir}: {e}", file=sys.stderr)
        return 2
    if args.json:
        print(json.dumps({**result, "report_paths": _public_paths(paths)}, ensure_ascii=False, indent=2))
    else:
        print(f"深挖完成: {target.name}")
        print(
            f"硬事实: {len(result['blocks']['hard_facts'])} | "
            f"矛盾: {len(result['blocks']['open_contradictions'])} | "
            f"需求原话: {len(result['blocks']['demand_quotes'])} | "
            f"动作: {len(result['blocks']['actions'])}"
        )
        for k, v in _public_paths(paths).items():
            print(f"  {k}: {v}")
        # 本机打开仍可用真实路径（仅人类终端第二行提示，不进 JSON）
        real = paths.get("html") or paths.get("md") or next(iter(paths.values()), "")
        if real:
            print(f"（本机打开: {real}）")
        print("请打开 HTML/MD 按质量清单终审后再对外使用。")
        print("（启发式草稿 ≠ 终审定论）")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
