#!/usr/bin/env python3
"""Show every caption style on a frame of the user's own video, so they can pick one by eye.

    python3 scripts/styles.py job.json                 # first video, 9:16, a moment with speech
    python3 scripts/styles.py job.json --only speed --canvas source --styles pop,clean,highlight

Writes <out>/styles-<id>.jpg: one panel per style, the style's name on top. Uses the proofread
words when there are any, so the sample text is the user's own.
"""
import argparse, os, shutil, sys, tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from aclib import (CANVAS, FITS, STYLE_DIR, die, font_for, get_font, guard, joiner, load_job,  # noqa: E402
                   load_pillow, load_style, need_ffmpeg, probe, rel, selected, shape_check)
import fix  # noqa: E402
from render import Layout, chunks, draw_state, frame_at, geometry, place  # noqa: E402


def main():
    ap = argparse.ArgumentParser(description="Every caption style on one frame.")
    ap.add_argument("job")
    ap.add_argument("--only", help="video id (default: the first)")
    ap.add_argument("--canvas", default="9:16", help="source, 9:16, 4:5, 1:1 or 16:9")
    ap.add_argument("--fit", default="crop", help="crop, blur or pad")
    ap.add_argument("--styles", help="comma-separated presets (default: all)")
    ap.add_argument("--at", type=float, help="second to show (default: a third of the way in)")
    a = ap.parse_args()
    if a.canvas not in ("source",) + tuple(CANVAS):
        die(f"--canvas must be source, {', '.join(CANVAS)}")
    if a.fit not in FITS:
        die("--fit must be crop, blur or pad")
    need_ffmpeg()
    Image, ImageDraw, ImageFont = load_pillow()
    from PIL import ImageFilter
    job = load_job(a.job)
    v = selected(job, a.only)[0]
    data = fix.apply(job, v, quiet=True)
    words = data["words"]
    lang = data.get("language") or job.get("language") or "en"
    if not words:
        die("no words to show; transcribe first (or the video has no speech)")
    shape_check(lang)
    o = {"id": "styles", "canvas": a.canvas, "fit": a.fit}
    out_cfg = next((x for x in job["outputs"] if x.get("canvas", "source") == a.canvas), {})
    for k in ("focus_x", "position"):
        if out_cfg.get(k) is not None:
            o[k] = out_cfg[k]
    vf, W, H, band = geometry(dict(probe(v["file"]), file=v["file"]), o, v)
    names = a.styles.split(",") if a.styles else sorted(f[:-5] for f in os.listdir(STYLE_DIR) if f.endswith(".json"))
    # a moment a third of the way in (or at --at)
    k = len(words) // 3 if a.at is None else min(range(len(words)), key=lambda i: abs(words[i]["start"] - a.at))
    tmp = tempfile.mkdtemp(prefix="captions-styles-")
    try:
        fp = os.path.join(tmp, "frame.jpg")
        frame_at(v["file"], words[k]["start"] + 0.1, vf, fp)
        base = Image.open(fp).convert("RGBA")
        label_font = get_font(os.path.join(os.path.dirname(STYLE_DIR), "fonts", "Inter.ttf"), 24, "SemiBold")
        sample = joiner(lang).join(w["w"] for w in words)
        panels = []
        for name in names:
            st = load_style(name, base=job["_base"])
            st["position"], _ = place(st, v, o, W, H, band)
            fpath, _ = font_for(st["font"], lang, sample.upper() if st.get("uppercase") else sample, 80,
                                out_cfg.get("font_file") or job.get("font_file"), st.get("weight"))
            lay = Layout(st, W, H, lang, fpath)
            groups = chunks(words, lay)
            gi = next((i for i, g in enumerate(groups) if any(w is words[k] for w in g)), None)
            img = base
            if gi is not None:
                g = groups[gi]
                pos = next(i for i, w in enumerate(g) if w is words[k])
                active = pos if (st.get("active") or st.get("active_box")) else -1
                p = os.path.join(tmp, f"{name}.png")
                draw_state(p, lay, g, len(g), active, Image, ImageDraw, ImageFilter)  # reveal: the whole chunk
                img = Image.alpha_composite(base, Image.open(p).resize(base.size, Image.LANCZOS))
            img = img.convert("RGB")
            panel = Image.new("RGB", (img.width, img.height + 40), "#1b1b1f")
            panel.paste(img, (0, 40))
            ImageDraw.Draw(panel).text((10, 7), name, font=label_font, fill="#e8e8ea")
            panels.append(panel)
        cols = min(4, len(panels))
        rows = (len(panels) + cols - 1) // cols
        pw, phh = panels[0].size
        sheet = Image.new("RGB", (cols * pw + (cols + 1) * 12, rows * phh + (rows + 1) * 12), "#1b1b1f")
        for i, p in enumerate(panels):
            sheet.paste(p, (12 + (i % cols) * (pw + 12), 12 + (i // cols) * (phh + 12)))
        os.makedirs(job["out"], exist_ok=True)
        path = os.path.join(job["out"], f"styles-{v['id']}.jpg")
        sheet.save(path, quality=88)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    print(f"{len(panels)} styles on {v['id']} at {W}x{H} -> {rel(path)}")


if __name__ == "__main__":
    guard(main)
