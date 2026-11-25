"""Transcribe a video with word timestamps (Whisper large-v3-turbo; see asr.py).

usage: python transcribe.py <video> <outdir>
writes: <outdir>/audio16k.wav, segments.json (with words), transcript.txt ("start-end text" per line)
Word times can run 0.1-0.4 s early; confirm cut points and animation beats with envelope.py.
"""
import json, os, subprocess, sys
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from render import FFMPEG
from asr import transcribe

video, out = sys.argv[1], sys.argv[2]
os.makedirs(out, exist_ok=True)
wav = os.path.join(out, "audio16k.wav")
subprocess.run([FFMPEG, "-v", "error", "-y", "-i", video, "-vn", "-ac", "1", "-ar", "16000", wav], check=True)
pcm = subprocess.run([FFMPEG, "-v", "error", "-i", wav, "-f", "f32le", "-"], capture_output=True, check=True).stdout
a = np.frombuffer(pcm, np.float32)
segments = transcribe(a)
json.dump(segments, open(os.path.join(out, "segments.json"), "w"))
with open(os.path.join(out, "transcript.txt"), "w") as f:
    for s in segments:
        f.write(f"{s['start']:8.2f}-{s['end']:8.2f} {s['text'].strip()}\n")
print(open(os.path.join(out, "transcript.txt")).read())
