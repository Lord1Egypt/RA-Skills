#!/usr/bin/env python3
"""逐帧画面裁字幕区 → OCR → 去重合并成带时间戳的讲稿。

设计要点：
1. 这类知识讲解视频通常是**双层文字**结构——顶部是章节/得分点标题条，底部是口播字幕。
   两块都要，所以裁出来纵向拼接。
2. 暗底白字会让 OCR 引擎（按「深色字+浅色底」训练）识别率骤降，因此每帧同时输出
   「原图」和「反色」两个版本，OCR 后按识别出的中文字数自动择优，不靠猜亮暗。
   （若确认某平台不需要，可用 ``--variants n`` 只跑原图，速度翻倍。）
3. 同一句字幕会横跨多帧，按相似度去重合并。
4. OCR 后端可插拔（见 ``ocr_backends.py``）：Windows 用系统内置引擎，其他平台用
   tesseract，或者用 ``--backend none`` 只产出裁好的图交给具备视觉能力的 agent 直接读。

用法:
    python ocr_subtitles.py --dir <capture_frames 输出目录>
    python ocr_subtitles.py --dir <目录> --backend none     # 交给 agent 读图
    python ocr_subtitles.py --dir <目录> --top 0 --bottom 0.28

输出:
    <dir>/subtitles/*.jpg        裁剪图（_n 原图 / _i 反色）
    <dir>/ocr_raw.txt            OCR 原始输出
    <dir>/transcript.md          完整讲稿
    <dir>/transcript.json        结构化分段
    <dir>/manifest.md            backend=none 时的读图清单
"""
from __future__ import annotations

import argparse
import difflib
import json
import os
import re
import sys

from PIL import Image

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ocr_backends import ocr_images, resolve_backend  # noqa: E402

CJK = re.compile(r"[\u4e00-\u9fff]")
VARIANTS = {"both": ("n", "i"), "n": ("n",), "i": ("i",)}


def crop_subtitles(frames_meta, out_dir, top_ratio, bottom_ratio, scale, variants):
    sub_dir = os.path.join(out_dir, "subtitles")
    os.makedirs(sub_dir, exist_ok=True)
    mapping = {}
    suffixes = VARIANTS[variants]
    for fr in frames_meta["frames"]:
        src = fr["file"]
        if not os.path.exists(src):
            continue
        img = Image.open(src).convert("L")
        w, h = img.size
        parts = []
        if top_ratio > 0:
            parts.append(img.crop((0, 0, w, int(h * top_ratio))))
        if bottom_ratio > 0:
            parts.append(img.crop((0, int(h * (1 - bottom_ratio)), w, h)))
        if not parts:
            parts = [img]
        gap = 12
        total_h = sum(p.height for p in parts) + gap * (len(parts) - 1)
        canvas = Image.new("L", (w, total_h), 0)
        y = 0
        for p in parts:
            canvas.paste(p, (0, y))
            y += p.height + gap
        if scale > 1:
            canvas = canvas.resize((canvas.width * scale, canvas.height * scale),
                                   Image.LANCZOS)
        stem = os.path.splitext(os.path.basename(src))[0]
        if "n" in suffixes:
            canvas.save(os.path.join(sub_dir, f"{stem}_n.jpg"), quality=95)
        if "i" in suffixes:
            canvas.point(lambda v: 255 - v).save(
                os.path.join(sub_dir, f"{stem}_i.jpg"), quality=95)
        mapping[stem] = fr["t"]
    return sub_dir, mapping


def run_ocr(sub_dir, out_dir, backend="auto", tess_lang="chi_sim+eng"):
    """调用可插拔后端识别 ``sub_dir`` 下所有 jpg，返回 [(文件名, 文本)]。"""
    names = sorted(n for n in os.listdir(sub_dir) if n.lower().endswith(".jpg"))
    pairs_map, used = ocr_images([os.path.join(sub_dir, n) for n in names],
                                 backend=backend, tess_lang=tess_lang)
    pairs = []
    for n in names:
        text = (pairs_map.get(n) or "").replace("\r", " ").replace("\n", " ").strip()
        pairs.append((n, text))
    with open(os.path.join(out_dir, "ocr_raw.txt"), "w", encoding="utf-8") as f:
        for n, t in pairs:
            f.write(f"{n}|{t}\n")
    return pairs, used


def normalize(s: str) -> str:
    s = s.replace(" ", "").replace("　", "")
    return "".join(ch for ch in s if ch.isalnum() or CJK.match(ch))


def pick_best_variants(pairs, mapping):
    """同一帧的 _n / _i 两个版本，取识别出中文字更多的那个。"""
    best = {}
    for name, text in pairs:
        stem = re.sub(r"_[ni]\.jpg$", "", name)
        if stem not in mapping:
            continue
        score = len(CJK.findall(text))
        cur = best.get(stem)
        if cur is None or score > cur["score"]:
            best[stem] = {"score": score, "text": text}
    return best


def build_transcript(best, mapping, threshold=0.80):
    items = []
    for stem, info in best.items():
        clean = normalize(info["text"])
        if len(clean) < 2:
            continue
        items.append({"t": mapping.get(stem), "stem": stem,
                      "text": info["text"], "clean": clean})
    items.sort(key=lambda x: (x["t"] is None, x["t"] or 0))

    merged = []
    for it in items:
        if merged:
            prev = merged[-1]
            ratio = difflib.SequenceMatcher(None, prev["clean"], it["clean"]).ratio()
            if ratio > threshold:
                if len(it["clean"]) > len(prev["clean"]):
                    prev["text"], prev["clean"] = it["text"], it["clean"]
                prev["end"] = it["t"]
                continue
        merged.append({"start": it["t"], "end": it["t"], "text": it["text"],
                       "clean": it["clean"], "stem": it["stem"]})
    return merged


def fmt(t):
    if t is None:
        return "??:??"
    return f"{int(t)//60:02d}:{int(t)%60:02d}"


def write_manifest(out_dir, meta, mapping, sub_dir, used):
    """backend=none 时输出读图清单，让具备视觉能力的 agent 直接读字幕图。"""
    lines = ["# 读图清单（OCR 后端：none）", "",
             "本目录下的字幕图已按时间戳命名，请**直接读取这些图片**获取字幕文字：", "",
             f"- 时长：{fmt(meta.get('duration'))}",
             f"- 采样间隔：{meta.get('interval')} 秒",
             f"- 字幕图目录：`{sub_dir}`",
             "- 命名规则：`<毫秒>.jpg`，如 `0120000_n.jpg` = 第 120 秒的原图版本",
             "- 每张图纵向拼接了「顶部标题条 + 底部口播字幕」，读图时两块都要看", "",
             "| 时间 | 字幕图 |", "| --- | --- |"]
    for stem in sorted(mapping, key=lambda s: mapping[s]):
        t = mapping[stem]
        cand = os.path.join(sub_dir, f"{stem}_n.jpg")
        if not os.path.exists(cand):
            cand = os.path.join(sub_dir, f"{stem}_i.jpg")
        lines.append(f"| {fmt(t)} | `{cand}` |")
    path = os.path.join(out_dir, "manifest.md")
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
    return path


def write_outputs(out_dir, merged, meta, used):
    with open(os.path.join(out_dir, "transcript.json"), "w", encoding="utf-8") as f:
        json.dump({"platform": meta.get("platform"), "video_id": meta.get("video_id"),
                   "duration": meta.get("duration"), "interval": meta.get("interval"),
                   "ocr_backend": used, "segments": merged},
                  f, ensure_ascii=False, indent=1)
    lines = ["# 视频逐句讲稿（画面字幕 OCR）", "",
             f"- 平台：{meta.get('platform') or '未知'}",
             f"- 视频 ID：{meta.get('video_id') or '—'}",
             f"- 时长：{fmt(meta.get('duration'))}",
             f"- 采样间隔：{meta.get('interval')} 秒",
             f"- OCR 后端：{used}",
             f"- 去重后字幕条数：{len(merged)}", "", "---", ""]
    for m in merged:
        lines.append(f"**[{fmt(m['start'])}]** {m['text']}")
        lines.append("")
    path = os.path.join(out_dir, "transcript.md")
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    return path


def main():
    ap = argparse.ArgumentParser(description="画面字幕 OCR 并合并讲稿")
    ap.add_argument("--dir", required=True, help="capture_frames 的输出目录")
    ap.add_argument("--top", type=float, default=0.22, help="顶部标题条裁剪比例（默认 0.22）")
    ap.add_argument("--bottom", type=float, default=0.24, help="底部字幕裁剪比例（默认 0.24）")
    ap.add_argument("--scale", type=int, default=2, help="放大倍数（默认 2）")
    ap.add_argument("--variants", choices=list(VARIANTS), default="both",
                    help="输出变体：both=原图+反色（默认，最稳）、n=只原图（快一倍）")
    ap.add_argument("--backend", default="auto",
                    help="OCR 后端：auto|winrt|tesseract|none（默认 auto）")
    ap.add_argument("--tess-lang", default="chi_sim+eng", help="tesseract 语言（默认 chi_sim+eng）")
    ap.add_argument("--skip-crop", action="store_true", help="复用已有 subtitles 目录")
    args = ap.parse_args()

    with open(os.path.join(args.dir, "frames.json"), encoding="utf-8") as f:
        meta = json.load(f)

    sub_dir = os.path.join(args.dir, "subtitles")
    mapping = {os.path.splitext(os.path.basename(fr["file"]))[0]: fr["t"]
               for fr in meta["frames"]}
    if not args.skip_crop:
        sub_dir, mapping = crop_subtitles(meta, args.dir, args.top, args.bottom,
                                          args.scale, args.variants)
        print(f"[info] 裁剪完成 {len(mapping)} 帧 ×{len(VARIANTS[args.variants])} 版本 → {sub_dir}",
              file=sys.stderr)

    resolved, why = resolve_backend(args.backend)
    print(f"[info] OCR 后端: {resolved}（{why}）", file=sys.stderr)

    if resolved == "none":
        path = write_manifest(args.dir, meta, mapping, sub_dir, resolved)
        print(f"[info] 未做 OCR，已输出读图清单 → {path}", file=sys.stderr)
        print(path)
        return

    pairs, used = run_ocr(sub_dir, args.dir, backend=args.backend,
                          tess_lang=args.tess_lang)
    print(f"[info] OCR 返回 {len(pairs)} 条", file=sys.stderr)

    best = pick_best_variants(pairs, mapping)
    empty = [k for k, v in best.items() if v["score"] == 0]
    if empty:
        print(f"[warn] {len(empty)} 帧未识别出中文（示例：{empty[:3]}）", file=sys.stderr)
    merged = build_transcript(best, mapping)
    print(f"[info] 去重后 {len(merged)} 条字幕", file=sys.stderr)
    print(write_outputs(args.dir, merged, meta, used))


if __name__ == "__main__":
    main()
