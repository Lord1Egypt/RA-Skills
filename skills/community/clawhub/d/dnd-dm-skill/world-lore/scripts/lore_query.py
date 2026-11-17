#!/usr/bin/env python3
"""
World Lore 子技能 CLI — 功能一：世界观对话 / 编年史检索

薄封装 lens_rag.WorldLens，提供：
  query  普通世界观查询（知识摘要，供 LLM 撰写叙述）
  pack   编年史素材打包（按 chronicle/event/location/faction/deity 分组，便于组装编年史）

路径：脚本位于 world-lore/scripts/，共享引擎在 skill 根 scripts/lens_rag.py
"""

import argparse
import json
import sys
from pathlib import Path

# 让脚本能 import 共享引擎 lens_rag
SKILL_SCRIPTS = Path(__file__).resolve().parent.parent.parent / "scripts"
sys.path.insert(0, str(SKILL_SCRIPTS))
from lens_rag import WorldLens, CHRONICLE_TYPES  # noqa: E402


def cmd_query(args):
    lens = WorldLens()
    cards = lens.search(" ".join(args.query), top_k=args.top_k, types=args.types)
    print(f"# 世界观查询：{' '.join(args.query)}")
    print(f"# 命中 {len(cards)} 张知识卡\n")
    print(lens.render(cards, with_body=not args.no_body))


def cmd_pack(args):
    """编年史素材打包：按类型分组，输出结构化知识包。"""
    lens = WorldLens()
    topic = " ".join(args.query)
    cards = lens.chronicle(topic, top_k=args.top_k)
    groups: dict[str, list] = {t: [] for t in CHRONICLE_TYPES}
    for c in cards:
        groups.setdefault(c.get("type"), []).append(c)
    print(f"# 编年史素材包：{topic or '(全量)'}")
    print(f"# 共 {len(cards)} 张\n")
    for t in CHRONICLE_TYPES:
        items = groups.get(t, [])
        if not items:
            continue
        print(f"## {t}（{len(items)}）")
        for c in items:
            src = c.get("source_file", "?")
            sec = c.get("source_section", "")
            line = f"- {c.get('title')} 〔{src}{('/'+sec) if sec else ''}〕"
            print(line)
        print()
    # 附原始 JSON 便于程序化使用
    if args.json:
        slim = [{k: c[k] for k in ("type", "title", "body", "source_file",
                                    "source_section", "tags", "_score") if k in c}
                for c in cards]
        print("<!-- JSON -->")
        print(json.dumps(slim, ensure_ascii=False, indent=2))


def main():
    p = argparse.ArgumentParser(description="World Lore 子技能 CLI（功能一）")
    sub = p.add_subparsers(dest="cmd", required=True)

    q = sub.add_parser("query", help="普通世界观查询")
    q.add_argument("query", nargs="+", help="检索词")
    q.add_argument("--top-k", type=int, default=6)
    q.add_argument("--types", nargs="+", help="限定类型")
    q.add_argument("--no-body", action="store_true")
    q.set_defaults(func=cmd_query)

    pk = sub.add_parser("pack", help="编年史素材打包（按类型分组）")
    pk.add_argument("query", nargs="*", help="主题词（可空）")
    pk.add_argument("--top-k", type=int, default=14)
    pk.add_argument("--json", action="store_true")
    pk.set_defaults(func=cmd_pack)

    args = p.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
