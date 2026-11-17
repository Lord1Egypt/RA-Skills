#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
输出目录 · 生成人读版 `提示词.md` export_md.py

支持两种布局：
  ① 合并库：`assets/output/提示词.json` → `assets/output/提示词.md`（每条带批次 tag）
  ② 旧的多项目：`assets/output/<项目>/提示词.json` → 同目录 `提示词.md`

提示词本体**独立成块、无标题无围栏**，可整段复制。零依赖。

用法：
  python3 scripts/export_md.py                 # 自动识别布局
  python3 scripts/export_md.py --project 01-全库样图
"""
import argparse
import json
import os
import time

SKILL_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STYLES_DIR = os.path.join(SKILL_ROOT, "styles")
OUTPUT_ROOT = os.path.join(SKILL_ROOT, "assets", "output")
IMG_EXTS = (".png", ".jpg", ".jpeg", ".webp")


def card_map():
    m = {}
    for name in sorted(os.listdir(STYLES_DIR)):
        if name.endswith(".md") and name[:2].isdigit():
            m[name[:-3]] = name
    return m


def image_map(root):
    found = {}
    for dirpath, _d, files in os.walk(root):
        for fn in files:
            stem, ext = os.path.splitext(fn)
            if ext.lower() in IMG_EXTS:
                found.setdefault(stem, os.path.join(dirpath, fn))
    return found


def write_md(out_path, title, subtitle, rows, imgs, cards, project_of, group_by_project):
    lines = [f"# {title}", "", subtitle, ""]
    lines.append("## 目录")
    lines.append("")
    current = None
    for i, r in enumerate(rows, 1):
        proj = project_of(r)
        if group_by_project and proj != current:
            current = proj
            lines.append("")
            lines.append(f"### {proj}")
            lines.append("")
        mark = "✅" if r.get("id") in imgs else "⏳"
        lines.append(f"{i}. {mark} `{r.get('id')}` · {r.get('size', '')}")
    lines += ["", "---", ""]
    for r in rows:
        rid = r.get("id", "")
        kind = r.get("kind", "")
        card = cards.get(kind)
        meta = [r.get("size", "")]
        if group_by_project:
            meta.insert(0, f"批次 `{project_of(r)}`")
        if card:
            meta.append(f"风格卡 `styles/{card}`")
        if r.get("api"):
            label = {"ark": "ARK", "newapi": "NewAPI", "tool": "宿主工具"}.get(r["api"], r["api"])
            model = (r.get("model") or "").replace("doubao-", "").replace("-260628", "")
            est = "（推定）" if r.get("api_estimated") else ""
            meta.append(f"出图 `{label}{(' · ' + model) if model else ''}{est}`"
                        + (f" · {r['api_at']}" if r.get("api_at") else ""))
        if rid not in imgs:
            meta.append("**待出**")
        lines.append(f"## {rid}")
        lines.append("")
        lines.append(" · ".join(x for x in meta if x))
        lines.append("")
        lines.append(r.get("prompt", "").strip())
        lines.append("")
        lines.append("---")
        lines.append("")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines).rstrip() + "\n")
    print(f"[+] {out_path}  ({len(rows)} 条)")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--project", default="")
    args = ap.parse_args()

    cards = card_map()
    root_pj = os.path.join(OUTPUT_ROOT, "提示词.json")

    # ① 合并库
    if os.path.isfile(root_pj) and not args.project:
        data = json.load(open(root_pj, "r", encoding="utf-8"))
        rows = data.get("rows", [])
        imgs = image_map(OUTPUT_ROOT)
        done = sum(1 for r in rows if r.get("id") in imgs)
        subtitle = (f"> 共 **{len(rows)}** 条提示词 / **{done}** 张成图"
                    f"{'' if done == len(rows) else f' / **{len(rows) - done}** 张待出'} · "
                    f"生成于 {time.strftime('%Y-%m-%d %H:%M')}\n>\n"
                    f"> 出图：`python3 scripts/generate.py --project . --dry-run`（免费预览）→ 加 `--yes` 出一张")
        write_md(os.path.join(OUTPUT_ROOT, "提示词.md"), "提示词总表（合并库）", subtitle,
                 rows, imgs, cards, lambda r: r.get("project", "合并库"), True)
        return 0

    # ② 旧的多项目
    projects = sorted(
        d for d in os.listdir(OUTPUT_ROOT)
        if os.path.isdir(os.path.join(OUTPUT_ROOT, d)) and not d.startswith("_")
        and os.path.isfile(os.path.join(OUTPUT_ROOT, d, "提示词.json"))
    )
    if args.project:
        projects = [p for p in projects if p == args.project]
    for project in projects:
        path = os.path.join(OUTPUT_ROOT, project)
        data = json.load(open(os.path.join(path, "提示词.json"), "r", encoding="utf-8"))
        rows = data.get("rows", [])
        imgs = image_map(path)
        done = sum(1 for r in rows if r.get("id") in imgs)
        subtitle = (f"> 共 **{len(rows)}** 条提示词 / **{done}** 张成图"
                    f"{'' if done == len(rows) else f' / **{len(rows) - done}** 张待出'} · "
                    f"生成于 {time.strftime('%Y-%m-%d %H:%M')}\n>\n"
                    f"> 出图：`python3 scripts/generate.py --project {project} --dry-run`"
                    f"（免费预览）→ 加 `--yes` 出一张")
        write_md(os.path.join(path, "提示词.md"), project, subtitle,
                 rows, imgs, cards, lambda r, p=project: p, False)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
