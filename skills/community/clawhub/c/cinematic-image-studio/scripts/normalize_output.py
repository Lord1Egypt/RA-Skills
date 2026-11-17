#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
输出目录 · 命名规范化 normalize_output.py

把 `assets/output/<项目>/` 里的 kind / id / 目录名 / 图片名统一到**风格卡文件名**：

  规则一：kind = 风格卡文件名去掉 `.md`（如 `18-敦煌金彩·壁画圣像`）
  规则二：id   = kind + '-' + 主体（如 `18-敦煌金彩·壁画圣像-观世音圣像`）
  规则三：图片落点 = `图片/<kind>/<id>.<ext>`

默认 **dry-run**，只打印将发生的改名；确认后加 `--apply` 真正执行。
零依赖。

用法：
  python3 scripts/normalize_output.py                 # 预览全部项目
  python3 scripts/normalize_output.py --project 01-全库样图
  python3 scripts/normalize_output.py --apply         # 执行
"""
import argparse
import json
import os
import re
import shutil
import sys

SKILL_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STYLES_DIR = os.path.join(SKILL_ROOT, "styles")
OUTPUT_ROOT = os.path.join(SKILL_ROOT, "assets", "output")
IMG_EXTS = (".png", ".jpg", ".jpeg", ".webp")


def load_cards():
    """编号 -> 风格卡文件名（去 .md）"""
    cards = {}
    for name in sorted(os.listdir(STYLES_DIR)):
        if not re.match(r"^\d\d-.*\.md$", name):
            continue
        cards[name[:2]] = name[:-3]
    return cards


def split_subject(old_id, old_kind):
    """从旧 id 里剥出「主体」。"""
    # ① id 以旧 kind 开头
    if old_id.startswith(old_kind + "-"):
        return old_id[len(old_kind) + 1:]
    # ② 去掉编号，再试旧 kind 去掉编号后的样子
    m = re.match(r"^\d\d-(.*)$", old_id)
    if m:
        rest = m.group(1)
        style_part = re.sub(r"^\d\d-", "", old_kind)
        if rest.startswith(style_part + "-"):
            return rest[len(style_part) + 1:]
        if "-" in rest:
            return rest.split("-", 1)[1]
        return rest
    # ③ 无编号 id（如 `天庭仙境-墨青主仙起舞`）：去掉最前面一截风格名
    if "-" in old_id:
        return old_id.split("-", 1)[1]
    return old_id


def iter_projects(only=None):
    for name in sorted(os.listdir(OUTPUT_ROOT)):
        path = os.path.join(OUTPUT_ROOT, name)
        if not os.path.isdir(path) or name.startswith("_"):
            continue
        if only and name != only:
            continue
        pj = os.path.join(path, "提示词.json")
        if os.path.isfile(pj):
            yield name, path, pj


def plan_project(project, path, pj, cards):
    with open(pj, "r", encoding="utf-8") as f:
        data = json.load(f)
    rows = data.get("rows", [])
    plan = []
    for row in rows:
        old_kind = row.get("kind", "")
        old_id = row.get("id", "")
        m = re.match(r"^(\d\d)-", old_kind)
        if m and m.group(1) in cards:
            new_kind = cards[m.group(1)]
        else:
            # 无编号的风格（个别变体项目）：编号取自项目名或 id
            pm = re.match(r"^(\d\d)-", project)
            if pm and pm.group(1) in cards:
                new_kind = cards[pm.group(1)]
            else:
                new_kind = old_kind
        subject = split_subject(old_id, old_kind)
        if new_kind == old_kind and old_id.startswith(new_kind + "-"):
            subject = old_id[len(new_kind) + 1:]
        new_id = new_kind + "-" + subject
        plan.append({"row": row, "old_kind": old_kind, "old_id": old_id,
                     "new_kind": new_kind, "new_id": new_id})
    return data, plan


def find_image(project_path, image_id):
    """按 id 找现有图片（任意子目录 / 后缀）。"""
    for dirpath, _dirnames, filenames in os.walk(project_path):
        for fn in filenames:
            stem, ext = os.path.splitext(fn)
            if stem == image_id and ext.lower() in IMG_EXTS:
                return os.path.join(dirpath, fn)
    return None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--project", default="", help="只处理某个项目")
    ap.add_argument("--apply", action="store_true", help="真正执行（默认只预览）")
    args = ap.parse_args()

    cards = load_cards()
    total_renames = 0
    for project, path, pj in iter_projects(args.project or None):
        data, plan = plan_project(project, path, pj, cards)
        if not plan:
            continue
        print(f"\n=== {project}")
        changes = 0
        for item in plan:
            row = item["row"]
            old_kind, old_id = item["old_kind"], item["old_id"]
            new_kind, new_id = item["new_kind"], item["new_id"]
            src = find_image(path, old_id)
            if not src:
                note = "（缺图，仅改 json）"
            else:
                note = ""
            if old_kind == new_kind and old_id == new_id and (
                    not src or os.path.basename(os.path.dirname(src)) == new_kind):
                continue
            changes += 1
            print(f"  {old_kind} | {old_id}")
            print(f"   → {new_kind} | {new_id} {note}")
            if not args.apply:
                continue
            if src:
                dst_dir = os.path.join(path, "图片", new_kind)
                os.makedirs(dst_dir, exist_ok=True)
                dst = os.path.join(dst_dir, new_id + os.path.splitext(src)[1])
                if os.path.abspath(src) != os.path.abspath(dst):
                    shutil.move(src, dst)
            row["kind"] = new_kind
            row["id"] = new_id
        if args.apply and changes:
            # 清掉空的旧目录
            img_root = os.path.join(path, "图片")
            if os.path.isdir(img_root):
                for d in sorted(os.listdir(img_root)):
                    dp = os.path.join(img_root, d)
                    if os.path.isdir(dp) and not os.listdir(dp):
                        os.rmdir(dp)
            data["style"] = project
            with open(pj, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"  [{changes} 处{'已执行' if args.apply else '待执行'}]")
        total_renames += changes
    print(f"\n[完成] 共 {total_renames} 处{'变更' if args.apply else '待变更（加 --apply 执行）'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
