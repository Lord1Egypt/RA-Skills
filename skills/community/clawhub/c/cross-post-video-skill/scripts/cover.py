#!/usr/bin/env python3
"""Pick a cover for a vertical video: a sheet of frames to choose from, then the cover image.

    python3 scripts/cover.py clip.mp4                 # covers/clip-sheet.jpg: 12 frames with their times
    python3 scripts/cover.py clip.mp4 --first 3       # 12 frames from the first 3 seconds (the hook)
    python3 scripts/cover.py clip.mp4 --at 1.4        # covers/clip.jpg (the cover) + covers/clip-grid.jpg,
                                                      #   and covers/clip.json (which video, which second)

The dashed box on every frame is the middle 3:4 that Instagram's profile grid shows; keep the face
or the title inside it. clip-grid.jpg shows the cover as it appears full screen and in the grid.
Needs Pillow (pip install pillow) and ffmpeg. Files go in covers/ in the folder you run this from.
The files are named after the video (letters and digits of any script are kept); --id gives
another name. covers/<name>.json records the video and the second, so plan.py can print
"Cover frame: 1.4 s" on the plan and on every by-hand page.
"""
import argparse, os, subprocess, sys, tempfile

sys.dont_write_bytecode = True   # nothing is ever written into the skill's own folder
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from xplib import die, guard, need_ffmpeg, probe, reading, rel, slug, write_json  # noqa: E402


def pil():
    try:
        from PIL import Image, ImageDraw, ImageFont
    except ImportError:
        die("Pillow is missing: pip install pillow")
    return Image, ImageDraw, ImageFont


def font(size):
    _, _, ImageFont = pil()
    try:
        return ImageFont.load_default(size=size)
    except TypeError:  # Pillow before 10.1
        return ImageFont.load_default()


def frame(video, t, tmp, k):
    out = os.path.join(tmp, f"f{k}.jpg")
    r = subprocess.run(["ffmpeg", "-y", "-v", "error", "-ss", f"{t:.3f}", "-i", video, "-frames:v", "1",
                        "-q:v", "2", out], capture_output=True, text=True, encoding="utf-8", errors="replace")
    if r.returncode != 0 or not os.path.exists(out):
        return None
    return out


def grid_box(w, h):
    """The middle 3:4 of a frame (what Instagram's profile grid shows of a 9:16 cover)."""
    if w * 4 >= h * 3:  # already 3:4 or wider: the grid crops the sides instead
        bw = h * 3 / 4
        return ((w - bw) / 2, 0, (w + bw) / 2, h)
    bh = w * 4 / 3
    return (0, (h - bh) / 2, w, (h + bh) / 2)


def dashed(draw, box, colour, width):
    x0, y0, x1, y1 = box
    step = 14
    for x in range(int(x0), int(x1), step * 2):
        draw.line([(x, y0), (min(x + step, x1), y0)], fill=colour, width=width)
        draw.line([(x, y1 - 1), (min(x + step, x1), y1 - 1)], fill=colour, width=width)
    for y in range(int(y0), int(y1), step * 2):
        draw.line([(x0, y), (x0, min(y + step, y1))], fill=colour, width=width)
        draw.line([(x1 - 1, y), (x1 - 1, min(y + step, y1))], fill=colour, width=width)


def sheet(video, info, first, out):
    Image, ImageDraw, _ = pil()
    span = min(first, info["duration"]) if first else info["duration"]
    n = 12
    times = [round(min(span * (k + 0.5) / n, max(info["duration"] - 0.05, 0)), 2) for k in range(n)]
    tw = 270
    th = int(tw * info["height"] / info["width"] / 2) * 2
    cols, pad, label = 6, 10, 26
    page = Image.new("RGB", (cols * (tw + pad) + pad, 2 * (th + label + pad) + pad), (18, 18, 20))
    draw = ImageDraw.Draw(page)
    f = font(18)
    with tempfile.TemporaryDirectory() as tmp:
        got = 0
        for k, t in enumerate(times):
            p = frame(video, t, tmp, k)
            if not p:
                continue
            got += 1
            with Image.open(p) as im:
                im = im.convert("RGB").resize((tw, th))
            x = pad + (k % cols) * (tw + pad)
            y = pad + (k // cols) * (th + label + pad)
            page.paste(im, (x, y))
            b = grid_box(tw, th)
            dashed(draw, (x + b[0], y + b[1], x + b[2], y + b[3]), (255, 255, 255), 1)
            draw.text((x + 2, y + th + 3), f"{t:.2f} s", fill=(235, 235, 235), font=f)
        if not got:
            die("couldn't read any frame from this video")
    page.save(out, quality=88)


def cover(video, info, t, out, grid_out):
    Image, ImageDraw, _ = pil()
    if not 0 <= t <= info["duration"]:
        die(f"--at must be between 0 and {info['duration']:.1f} (the video's length in seconds)")
    with tempfile.TemporaryDirectory() as tmp:
        p = frame(video, min(t, max(info["duration"] - 0.05, 0)), tmp, 0)
        if not p:
            die(f"couldn't read a frame at {t} s")
        with Image.open(p) as im:
            im = im.convert("RGB")
    if im.width > 1080:
        im = im.resize((1080, int(1080 * im.height / im.width / 2) * 2))
    im.save(out, quality=92)
    # how it looks: full screen next to the profile-grid crop
    h = 640
    full = im.resize((int(h * im.width / im.height), h))
    b = grid_box(im.width, im.height)
    crop = im.crop(tuple(int(v) for v in b))
    crop = crop.resize((int(h * 0.75 * crop.width / crop.height), int(h * 0.75)))
    pad, label = 16, 30
    page = Image.new("RGB", (full.width + crop.width + pad * 3, h + label + pad * 2), (18, 18, 20))
    draw = ImageDraw.Draw(page)
    f = font(18)
    page.paste(full, (pad, pad + label))
    fb = grid_box(full.width, full.height)
    dashed(draw, (pad + fb[0], pad + label + fb[1], pad + fb[2], pad + label + fb[3]), (255, 255, 255), 2)
    page.paste(crop, (pad * 2 + full.width, pad + label))
    draw.text((pad, pad), "Full screen", fill=(235, 235, 235), font=f)
    draw.text((pad * 2 + full.width, pad), "Profile grid (3:4)", fill=(235, 235, 235), font=f)
    page.save(grid_out, quality=88)


def main():
    ap = argparse.ArgumentParser(description="Pick a cover frame for a video.")
    ap.add_argument("video")
    ap.add_argument("--at", type=float, help="the second to use as the cover")
    ap.add_argument("--first", type=float, help="sheet: only the first N seconds")
    ap.add_argument("--id", help="name for the files (default: the video's file name)")
    ap.add_argument("--dir", default="covers", help="folder for the files (default: covers)")
    a = ap.parse_args()
    reading(a.video)
    need_ffmpeg()
    info = probe(a.video)
    if not info["width"] or not info["height"]:
        die("couldn't read this video's size")
    if not info["duration"]:
        die("can't read this file's length; re-save it as MP4 first (check_video.py --fix), then pick the cover "
            "from the new file")
    if a.first is not None and a.first <= 0:
        die("--first must be more than 0 seconds")
    name = slug(a.id or os.path.splitext(os.path.basename(a.video))[0])
    if os.path.lexists(a.dir) and not os.path.isdir(a.dir):
        die(f"--dir {a.dir} is a file, not a folder; give a folder for the cover files")
    os.makedirs(a.dir, exist_ok=True)
    if a.at is None:
        out = os.path.join(a.dir, f"{name}-sheet.jpg")
        sheet(a.video, info, a.first, out)
        print(f"wrote {rel(out)}: 12 frames with their times. Pick one, then run again with --at <seconds>")
    else:
        out = os.path.join(a.dir, f"{name}.jpg")
        grid_out = os.path.join(a.dir, f"{name}-grid.jpg")
        cover(a.video, info, a.at, out, grid_out)
        note = os.path.join(a.dir, f"{name}.json")
        try:
            src = os.path.relpath(os.path.abspath(a.video), os.path.abspath(a.dir))
        except ValueError:   # another drive on Windows
            src = os.path.abspath(a.video)
        write_json(note, {"video": src.replace(os.sep, "/"), "at": round(a.at, 3)})
        print(f"wrote {rel(out)} (the cover, from {a.at:g} s), {rel(grid_out)} (how it looks full screen "
              f"and in the profile grid) and {rel(note)} (the second, for the plan)")


if __name__ == "__main__":
    guard(main)
