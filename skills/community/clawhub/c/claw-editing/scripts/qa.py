"""QA a finished video before handing it over.

usage: python qa.py <output.mp4> <qa_dir> [--source SRC --edl edl.json] [--times t1,t2,...]

Reports: stream durations + frame counts, integrated loudness / true peak, a transcript of the
finished video (read it: doubled words or half-words mean a bad splice), audio sync vs the source
for every segment (needs --source and the edl.json written by edit.py; want ~0 ms lag),
and a contact sheet at --times (put a time inside every graphic and either side of every cut).
"""
import argparse, json, os, subprocess, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from render import FFMPEG, FFPROBE

ap = argparse.ArgumentParser()
ap.add_argument("video"); ap.add_argument("qa_dir")
ap.add_argument("--source"); ap.add_argument("--edl"); ap.add_argument("--times")
a = ap.parse_args()
os.makedirs(a.qa_dir, exist_ok=True)

print(subprocess.run([FFPROBE, "-v", "error", "-count_packets", "-show_entries",
                      "stream=index,codec_type,codec_name,nb_read_packets,duration,r_frame_rate:stream_disposition=attached_pic",
                      "-of", "compact", a.video], capture_output=True, text=True).stdout)
lo = subprocess.run([FFMPEG, "-hide_banner", "-nostats", "-i", a.video, "-map", "0:a", "-af", "ebur128=peak=true", "-f", "null", "-"],
                    capture_output=True, text=True).stderr
print("loudness:", " | ".join(l.strip() for l in lo.splitlines() if l.strip().startswith(("I:", "Peak:"))))


def pcm16k(path):
    b = subprocess.run([FFMPEG, "-v", "error", "-i", path, "-map", "0:a", "-ac", "1", "-ar", "16000", "-f", "f32le", "-"],
                       capture_output=True, check=True).stdout
    return np.frombuffer(b, np.float32)


fin = pcm16k(a.video)
if a.source and a.edl:
    src = pcm16k(a.source)
    edl = json.load(open(a.edl))
    from fractions import Fraction
    fps = float(Fraction(edl["fps"]))
    th = edl.get("thumbnail_frames", 0)
    for s in edl["segments"]:
        t_out = (s["at"] + th) / fps + 0.3
        t_src = s["f_in"] / fps + 0.3
        n = min(16000, int(s["n"] / fps * 16000) - 8000)
        if n < 4000:
            continue
        x = fin[int(t_out * 16000):int(t_out * 16000) + n]
        best = None
        for lag in range(-160, 161):
            y = src[int(t_src * 16000) + lag:int(t_src * 16000) + lag + n]
            c = float(np.dot(x, y) / (np.linalg.norm(x) * np.linalg.norm(y) + 1e-9))
            if best is None or c > best[1]:
                best = (lag, c)
        print(f"sync {s['name']:<16} lag {best[0] / 16:+.2f} ms  corr {best[1]:.3f}")

from asr import transcribe
with open(os.path.join(a.qa_dir, "final_transcript.txt"), "w") as f:
    for s in transcribe(fin, words=False):
        f.write(f"{s['start']:8.2f} {s['text'].strip()}\n")
print(open(os.path.join(a.qa_dir, "final_transcript.txt")).read())

if a.times:
    subprocess.run([sys.executable, os.path.join(HERE, "contact_sheet.py"), a.video, os.path.join(a.qa_dir, "contact-sheet.jpg"),
                    "--times", a.times], check=True)
