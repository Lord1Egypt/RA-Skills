#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
回填历史图片的「出图 API」标签 backfill_api.py

背景：早期出图没有把 api / model 写回 提示词.json，样图库只能显示「未标注」。
本脚本按**图片尺寸规格**反推渠道，把标签补回去，并标 `api_estimated: true`（样图库显示为「推定」）：

  1536x1024 / 1024x1536 → newapi · gpt-image-2-c      （NewAPI 中转的固定两档）
  1152x2048 / 2048x1152 → ark    · doubao-seedream-5-0-pro-260628 （Ark 2K 档）
  其它尺寸               → 跳过，保持「未标注」（不猜）

规则：
  · 只补**没有 api 字段**的行；已标注的不动（除非 --force）
  · 同时校验行内 `size` 与实际图片尺寸：不一致就跳过并打印（避免误标）
  · 出图时间用图片文件的 mtime（回填的时间，仅作参考，标 estimated）

用法：
  python3 scripts/backfill_api.py            # 预览，不写盘
  python3 scripts/backfill_api.py --apply    # 写入 提示词.json
"""
import argparse
import glob
import json
import os
import time

SKILL_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTPUT_ROOT = os.path.join(SKILL_ROOT, "assets", "output")
PROMPTS = os.path.join(OUTPUT_ROOT, "提示词.json")
IMG_ROOT = os.path.join(OUTPUT_ROOT, "图片")
IMG_EXTS = (".png", ".jpg", ".jpeg", ".webp")

SIZE_MAP = {
    "1536x1024": ("newapi", "gpt-image-2-c"),
    "1024x1536": ("newapi", "gpt-image-2-c"),
    "1152x2048": ("ark", "doubao-seedream-5-0-pro-260628"),
    "2048x1152": ("ark", "doubao-seedream-5-0-pro-260628"),
}


def image_size(path):
    with open(path, "rb") as f:
        head = f.read(32)
    if head[:8] == b"\x89PNG\r\n\x1a\n":
        import struct
        w, h = struct.unpack(">II", head[16:24])
        return int(w), int(h)
    if head[:2] == b"\xff\xd8":
        # JPEG：交给 PIL（本机一般都有）；没有就跳过
        try:
            from PIL import Image
            with Image.open(path) as im:
                return im.size
        except Exception:  # noqa: BLE001
            return 0, 0
    try:
        from PIL import Image
        with Image.open(path) as im:
            return im.size
    except Exception:  # noqa: BLE001
        return 0, 0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true", help="真正写入（默认只预览）")
    ap.add_argument("--force", action="store_true", help="已有 api 字段的行也覆盖")
    args = ap.parse_args()

    with open(PROMPTS, "r", encoding="utf-8") as f:
        data = json.load(f)
    rows = data["rows"]
    by_id = {str(r.get("id")): r for r in rows}

    files = [p for p in glob.glob(os.path.join(IMG_ROOT, "*"))
             if p.lower().endswith(IMG_EXTS)]
    filled, skipped, unknown = [], [], []
    for path in sorted(files):
        stem = os.path.splitext(os.path.basename(path))[0]
        r = by_id.get(stem)
        if not r:
            unknown.append((stem, "无提示词行"))
            continue
        if r.get("api") and not args.force:
            continue
        w, h = image_size(path)
        if not w:
            unknown.append((stem, "读不出尺寸"))
            continue
        dim = f"{w}x{h}"
        row_size = str(r.get("size") or "").strip()
        if row_size and row_size != dim:
            skipped.append((stem, f"行内 size={row_size} 与图片 {dim} 不一致"))
            continue
        hit = SIZE_MAP.get(dim)
        if not hit:
            skipped.append((stem, f"尺寸 {dim} 不在已知规格里"))
            continue
        api, model = hit
        ts = time.strftime("%Y-%m-%d %H:%M", time.localtime(os.path.getmtime(path)))
        filled.append({
            "id": stem, "api": api, "model": model,
            "api_at": ts, "api_size": dim, "api_estimated": True,
        })
        if args.apply:
            r.update(api=api, model=model, api_at=ts, api_size=dim, api_estimated=True)

    for x in filled:
        print(f"[补] {x['id'][:44]:46s} {x['api']:6s} {x['model']:32s} {x['api_at']}")
    for stem, why in skipped:
        print(f"[跳过] {stem[:44]:46s} {why}")
    for stem, why in unknown:
        print(f"[忽略] {stem[:44]:46s} {why}")

    print(f"\n[汇总] 可补 {len(filled)} 张 · 跳过 {len(skipped)} · 忽略 {len(unknown)}")
    if not args.apply:
        print("[预览] 未写盘。确认无误后加 --apply")
        return 0
    with open(PROMPTS, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        f.write("\n")
    print(f"[写入] {PROMPTS}")
    print("[下一步] python3 scripts/gallery.py   # 刷新样图库标签")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
