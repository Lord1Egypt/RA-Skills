"""Find exact word onsets / silent cut points.

usage:
  python envelope.py <audio16k.wav> <t0> <t1> [step=0.02]     -> prints time:dB pairs
  python envelope.py <audio16k.wav> words <segments.json> <t0> <t1>   -> prints whisper words in range
Speech is roughly > -25 dB, room tone < -40 dB. Cut inside a dip; a word's onset is where dB jumps.
"""
import json, subprocess, sys, os
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from render import FFMPEG

wav = sys.argv[1]
if sys.argv[2] == "words":
    segs = json.load(open(sys.argv[3])); t0, t1 = float(sys.argv[4]), float(sys.argv[5])
    print(" ".join(f"{w['start']:.2f}:{w['word'].strip()}" for s in segs for w in s.get("words", []) if t0 <= w["start"] <= t1))
    sys.exit()
pcm = subprocess.run([FFMPEG, "-v", "error", "-i", wav, "-ac", "1", "-ar", "16000", "-f", "f32le", "-"], capture_output=True, check=True).stdout
a = np.frombuffer(pcm, np.float32)
t0, t1 = float(sys.argv[2]), float(sys.argv[3]); st = float(sys.argv[4]) if len(sys.argv) > 4 else 0.02
out = []
t = t0
while t < t1:
    s = a[int(t * 16000):int((t + st) * 16000)]
    out.append(f"{t:.2f}:{20 * np.log10(np.sqrt(np.mean(s ** 2)) + 1e-6):.0f}")
    t += st
print(" ".join(out))
