"""Labelled contact sheet of a video, for reviewing takes, framing, and finished edits.

usage: python contact_sheet.py <video> <out.jpg> (--every SECONDS | --times t1,t2,...) [--cols 4] [--width 480]
"""
import argparse, os, subprocess, sys, tempfile
from PIL import Image, ImageDraw
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from render import FFMPEG, FFPROBE

ap = argparse.ArgumentParser()
ap.add_argument("video"); ap.add_argument("out")
ap.add_argument("--every", type=float); ap.add_argument("--times")
ap.add_argument("--cols", type=int, default=4); ap.add_argument("--width", type=int, default=480)
a = ap.parse_args()
if a.times:
    ts = [float(x) for x in a.times.split(",")]
else:
    dur = float(subprocess.run([FFPROBE, "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", a.video],
                               capture_output=True, text=True).stdout)
    ts = [i * a.every for i in range(int(dur // a.every) + 1)]
tmp = tempfile.mkdtemp()
ims = []
for k, t in enumerate(ts):
    p = os.path.join(tmp, f"{k}.jpg")
    subprocess.run([FFMPEG, "-v", "error", "-y", "-ss", str(t), "-i", a.video, "-frames:v", "1", "-vf", f"scale={a.width}:-2", p])
    if os.path.exists(p):
        im = Image.open(p).convert("RGB"); d = ImageDraw.Draw(im)
        d.text((6, 4), f"{int(t // 60)}:{t % 60:05.2f}", fill=(255, 255, 0)); ims.append(im)
w, h = ims[0].size
rows = (len(ims) + a.cols - 1) // a.cols
sheet = Image.new("RGB", (w * a.cols, h * rows))
for k, im in enumerate(ims):
    sheet.paste(im, ((k % a.cols) * w, (k // a.cols) * h))
sheet.save(a.out, quality=85)
print(a.out, len(ims), "frames")
