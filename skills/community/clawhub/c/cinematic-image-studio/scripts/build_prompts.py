#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
风格库 · 提示词装配器 build_prompts.py

把「一张风格卡（styles/0N-*.md）」+「一条测试主体变量」合成为一条 **14 节电影级提示词**，
并写进项目的 `提示词.json`（`rows`）。**固定节逐字照抄风格卡**，保证同风格成系列。

零依赖。用法：
  python3 scripts/build_prompts.py --project 01-全库样图 --vars <变量.json> [--replace]
  # --replace：已有同 id 的行用新值覆盖；否则跳过已存在的 id

变量.json 结构（每风格一条）：
  [
    {"card": "05-温馨亲子绘本.md", "id": "05-温馨亲子绘本-暖光窗前母子共读", "kind": "05-温馨亲子绘本",
     "size": "1536x1024", "ratio": "16:9",
     "subject": "…", "near": "无", "mid": "…", "far": "…", "global": "…",
     "composition": "…", "lens": "…", "extra_negative": "…"}
  ]
"""
import argparse
import json
import os
import re
import sys

SKILL_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STYLES_DIR = os.path.join(SKILL_ROOT, "styles")

# 14 节标准序 + 可选【装饰】（只有卡里写了才输出，如 03-中式美学）
NODE_ORDER = ["主体", "次要元素·近景", "次要元素·中景", "次要元素·远景", "全局",
              "构图", "光影", "色彩", "影像质感", "装饰", "背景", "镜头", "风格", "画幅"]

VAR_KEY = {"主体": "subject", "次要元素·近景": "near", "次要元素·中景": "mid",
           "次要元素·远景": "far", "全局": "global", "构图": "composition", "镜头": "lens"}

GENERIC_NEG = [
    "日式动漫", "美式漫画", "卡通", "Q版", "3D渲染", "CG塑料感", "矢量插画",
    "文字", "字幕", "水印", "Logo", "签名", "题款", "落款", "印章", "二维码", "可读文字",
    "人物融合", "人物残缺", "多余人物", "手指畸形", "五官错位", "多余肢体",
    "主体被裁切", "构图失衡", "画面塞满", "模糊", "噪点", "过曝", "欠曝",
]


def read_card(card_name):
    path = os.path.join(STYLES_DIR, card_name)
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def extract_fixed_nodes(text):
    """从「★固定节」代码块抽取 {节名: 文本}。"""
    m = re.search(r"★固定节[^\n]*\n+```[^\n]*\n(.*?)\n```", text, re.S)
    if not m:
        return {}
    block = m.group(1)
    nodes = {}
    for name, body in re.findall(r"【([^】]+)】\s*(.*?)(?=【|$)", block, re.S):
        nodes[name.strip()] = " ".join(body.split())
    return nodes


def extract_owner_negative(text):
    m = re.search(r"★专属负向[^\n]*\n+```[^\n]*\n(.*?)\n```", text, re.S)
    if not m:
        return []
    raw = m.group(1)
    items = []
    for line in raw.splitlines():
        line = line.strip()
        if not line or line.startswith("【"):
            continue
        for tok in re.split(r"[、,，;；]", line):
            tok = tok.strip()
            if tok:
                items.append(tok)
    return items


def dedup(seq):
    seen, out = set(), []
    for x in seq:
        if x not in seen:
            seen.add(x)
            out.append(x)
    return out


def build_prompt(v):
    text = read_card(v["card"])
    nodes = extract_fixed_nodes(text)
    if not nodes:
        sys.exit(f"[FAIL] 未从 {v['card']} 抽到固定节")
    ratio = v.get("ratio") or "16:9"
    nodes["画幅"] = ratio

    def node(key, default="无"):
        return v.get(VAR_KEY.get(key, key)) or default

    parts = []
    for name in NODE_ORDER:
        if name in VAR_KEY:
            parts.append(f"【{name}】{node(name)}")
        elif name == "画幅":
            parts.append(f"【{name}】{ratio}")
        else:
            if name in nodes:
                parts.append(f"【{name}】{nodes[name]}")
    # 卡片里出现、但不在标准序里的固定节（例如 【装饰】已在 NODE_ORDER；其余补到最后）
    for name, body in nodes.items():
        if name not in NODE_ORDER:
            parts.append(f"【{name}】{body}")

    # 负向 = 风格专属 + 变量补充 + 通用（去重）
    neg = dedup(extract_owner_negative(text)
                + [x.strip() for x in (v.get("extra_negative") or "").split("、") if x.strip()]
                + GENERIC_NEG)
    prompt = "\n".join(parts) + "\n\n【负向】" + "、".join(neg)
    return prompt


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--project", required=True)
    ap.add_argument("--vars", required=True, help="变量.json 路径")
    ap.add_argument("--prompts", default="提示词.json")
    ap.add_argument("--replace", action="store_true")
    args = ap.parse_args()

    proj = os.path.join(SKILL_ROOT, "assets", "output", args.project)
    prompts_path = os.path.join(proj, args.prompts)
    with open(args.vars, "r", encoding="utf-8") as f:
        variables = json.load(f)

    data = {"style": args.project, "rows": []}
    if os.path.isfile(prompts_path):
        with open(prompts_path, "r", encoding="utf-8") as f:
            data = json.load(f)
    rows = data.get("rows", [])
    by_id = {r.get("id"): r for r in rows}

    added = 0
    for v in variables:
        rid = v["id"]
        if rid in by_id and not args.replace:
            print(f"[skip] {rid}（已存在）")
            continue
        row = {"id": rid, "kind": v["kind"], "size": v.get("size") or "1536x1024",
               "prompt": build_prompt(v), "refs": v.get("refs", [])}
        if rid in by_id:
            by_id[rid].update(row)
        else:
            rows.append(row)
            by_id[rid] = row
        added += 1
        print(f"[+ ] {rid} ← {v['card']}")

    data["rows"] = rows
    os.makedirs(proj, exist_ok=True)
    with open(prompts_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"[完成] 新增/覆盖 {added} 行，共 {len(rows)} 行 → {prompts_path}")


if __name__ == "__main__":
    main()
