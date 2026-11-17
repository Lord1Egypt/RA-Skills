#!/usr/bin/env python3
"""
Echo Map 子技能 CLI — 功能三：真实经历 → DND 冒险映射

职责（确定性部分）：
  anonymize  把真实姓名 / 机构名 / 地名替换为 DND 幻想名（防隐私泄露）
  normalize  把 LLM 起草的映射草稿（模组 JSON）按 mapping_dict 规范化，
             执行脱敏、补全输出契约（chronicle_note），校验核心字段

语义映射（人物→种族/职业/阵营、冲突→反派/怪物/CR 等）由 LLM 完成；
本脚本只做「脱敏 + 结构化兜底」，强制不泄露真实身份。

用法：
  # 1) 生成脱敏字典并改写经历文本
  python echo_map.py anonymize --names "张三 李四" --places "上海 甲公司" \
                               --story experience.txt --out experience_anon.txt

  # 2) 规范化 LLM 起草的模组 JSON（脱敏 + 补全契约）
  python echo_map.py normalize --draft draft_module.json \
                               --names "张三 李四" --places "上海 甲公司" --out final.json
"""

import argparse
import json
import os
import sys
from pathlib import Path

SKILL_SCRIPTS = Path(__file__).resolve().parent.parent.parent / "scripts"
sys.path.insert(0, str(SKILL_SCRIPTS))

DATA_DIR = os.environ.get("DND_LENS_DATA") or (Path(__file__).resolve().parent.parent.parent / "data")
MAP_DICT = DATA_DIR / "mapping_dict.json"

# 输出契约（复用功能二模组 JSON + chronicle_note）
OUTPUT_KEYS = [
    "title", "pitch", "level_range", "type", "premise",
    "factions", "npcs", "locations", "acts", "rewards",
    "timeline", "hooks_for_current_campaign", "chronicle_note",
]


def load_dict():
    with open(MAP_DICT, encoding="utf-8") as f:
        return json.load(f)


def flat(items):
    """把 ['张三 李四', '王五'] 这类（中文名常无空格、整串传入）展平为 ['张三','李四','王五']。"""
    out = []
    for it in (items or []):
        out += str(it).split()
    return out


def build_alias_map(names, places, mdict):
    """构造 真实名 → 幻想名 的稳定映射。"""
    alias = {}
    npool = mdict["anonymize"]["name_pool"]
    ppool = mdict["anonymize"]["place_pool"]
    for i, n in enumerate(names):
        alias[n] = npool[i % len(npool)]
    for i, p in enumerate(places):
        alias[p] = ppool[i % len(ppool)]
    return alias


def apply_alias(text, alias):
    for real, fan in alias.items():
        if real:
            text = text.replace(real, fan)
    return text


# ---------------------------------------------------------------------------
def cmd_anonymize(args):
    mdict = load_dict()
    names = flat(args.names)
    places = flat(args.places)
    alias = build_alias_map(names, places, mdict)

    print("# 脱敏映射字典")
    for real, fan in alias.items():
        print(f"  {real}  →  {fan}")
    print()

    if args.story:
        src = Path(args.story)
        if not src.exists():
            print(f"[错误] 故事文件不存在: {src}")
            return
        text = src.read_text(encoding="utf-8")
        anon = apply_alias(text, alias)
        if args.out:
            Path(args.out).write_text(anon, encoding="utf-8")
            print(f"已写入脱敏后文本：{args.out}")
        else:
            print("# 脱敏后文本\n")
            print(anon)
    else:
        print("（未提供 --story，仅输出映射字典）")


# ---------------------------------------------------------------------------
def cmd_normalize(args):
    mdict = load_dict()
    names = flat(args.names)
    places = flat(args.places)
    alias = build_alias_map(names, places, mdict)

    # 读草稿
    if args.draft:
        draft = json.loads(Path(args.draft).read_text(encoding="utf-8"))
    else:
        draft = json.load(sys.stdin)

    # 脱敏：遍历所有字符串值做替换
    def scrub(obj):
        if isinstance(obj, str):
            return apply_alias(obj, alias)
        if isinstance(obj, list):
            return [scrub(x) for x in obj]
        if isinstance(obj, dict):
            return {k: scrub(v) for k, v in obj.items()}
        return obj

    draft = scrub(draft)

    # 补全输出契约
    missing = [k for k in ("title", "premise", "npcs", "acts") if k not in draft]
    if missing:
        print(f"[警告] 草稿缺少核心字段：{missing}（以下功能二契约不完整）")
    if "chronicle_note" not in draft:
        draft["chronicle_note"] = "（请补一段『这段经历在费伦编年史中可记为何事』的注记）"

    # 附注：本映射遵循的字典版本与脱敏规则
    draft["_meta"] = {
        "generated_by": "echo-map",
        "mapping_dict_version": mdict.get("version"),
        "anonymized": bool(alias),
        "privacy_note": mdict["anonymize"]["rule"],
    }

    out = json.dumps(draft, ensure_ascii=False, indent=2)
    if args.out:
        Path(args.out).write_text(out, encoding="utf-8")
        print(f"已写入规范化模组 JSON：{args.out}")
    else:
        print(out)


# ---------------------------------------------------------------------------
def main():
    p = argparse.ArgumentParser(description="Echo Map 子技能 CLI（功能三）")
    sub = p.add_subparsers(dest="cmd", required=True)

    a = sub.add_parser("anonymize", help="脱敏：真实名→幻想名")
    a.add_argument("--names", nargs="*", default=[], help="真实人名列表")
    a.add_argument("--places", nargs="*", default=[], help="真实地名/机构名列表")
    a.add_argument("--story", help="原始经历文本文件（可选，改写后输出）")
    a.add_argument("--out", help="输出文件（默认打印到屏幕）")
    a.set_defaults(func=cmd_anonymize)

    n = sub.add_parser("normalize", help="规范化 LLM 草稿（脱敏+补全契约）")
    n.add_argument("--draft", help="LLM 起草的模组 JSON 文件（或管道输入）")
    n.add_argument("--names", nargs="*", default=[], help="需脱敏的真实人名")
    n.add_argument("--places", nargs="*", default=[], help="需脱敏的真实地名/机构名")
    n.add_argument("--out", help="输出文件（默认打印）")
    n.set_defaults(func=cmd_normalize)

    args = p.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
