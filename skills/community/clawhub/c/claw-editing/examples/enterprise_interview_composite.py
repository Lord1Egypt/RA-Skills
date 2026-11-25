# Worked example from the original project. Paths are placeholders: point them at your files.
"""Composite the OpenClaw-style graphics onto 'What is OpenClaw enterprise.mov'.

- Base: What is OpenClaw enterprise.mov (picture + audio untouched; audio stream-copied).
- Frames 185-565 (6.17-18.83 s) are replaced with the matching frames of
  Kevin & Graham OCE.mov (clean frame = frame - 180) to remove the old name tags.
- v3: thumbnail.png is held for THUMB frames before everything (first frame = thumbnail)
  and thumbnail.jpg is embedded as cover art.
- Old title card (0-6 s) and old end card (from 1344.17 s) are covered by the new opaque cards.
"""
import json, subprocess, sys
from render import FFMPEG as FF  # run with PYTHONPATH={baseDir}/scripts
BASE = "/path/to/What is OpenClaw enterprise.mov"
CLEAN = "/path/to/Kevin & Graham OCE.mov"
CLIPS = "/path/to/OpenClaw Enterprise Edit/Motion Graphics/clips"
P0, P1, SHIFT = 185, 566, 180
EDIT = "/path/to/OpenClaw Enterprise Edit"
THUMB = 30   # 1.0 s
tl = json.load(open("timeline_ent.json"))
args = [FF, "-v", "error", "-stats", "-y", "-i", BASE, "-i", CLEAN]
fc = [f"[1:v]fps=30,trim=start_frame={P0 - SHIFT}:end_frame={P1 - SHIFT},setpts=PTS-STARTPTS+{P0}/30/TB[patch]",
      "[0:v][patch]overlay=eof_action=pass:repeatlast=0[b0]"]
last = "b0"
for k, (name, (start, dur)) in enumerate(sorted(tl.items(), key=lambda kv: kv[1][0]), 2):
    args += ["-i", f"{CLIPS}/{name}.mov"]
    f0 = round(start * 30)
    fc.append(f"[{k}:v]setpts=PTS-STARTPTS+{f0}/30/TB[g{k}]")
    fc.append(f"[{last}][g{k}]overlay=eof_action=pass:format=yuv444:repeatlast=0[v{k}]")
    last = f"v{k}"
fc.append(f"[{last}]format=yuv420p[body]")
n_in = len(tl) + 2
args += ["-loop", "1", "-framerate", "30", "-t", f"{THUMB / 30}", "-i", f"{EDIT}/thumbnail.png", "-i", f"{EDIT}/thumbnail.jpg"]
fc.append(f"[{n_in}:v]format=yuv420p,setsar=1[th]")
fc.append("[th][body]concat=n=2:v=1:a=0[out]")
fc.append(f"aevalsrc=0|0:d={THUMB / 30}:s=44100,aformat=sample_fmts=fltp:channel_layouts=stereo[sil]")
fc.append("[0:a]aformat=sample_fmts=fltp:sample_rates=44100:channel_layouts=stereo[a0]")
fc.append("[sil][a0]concat=n=2:v=0:a=1[aout]")
args += ["-filter_complex", ";".join(fc), "-map", "[out]", "-map", "[aout]", "-map", f"{n_in + 1}:v", "-frames:v:0", str(40415 + THUMB),
         "-c:v:0", "libx264", "-preset", "medium", "-crf", "16", "-profile:v:0", "high", "-r:v:0", "30",
         "-colorspace", "bt709", "-color_primaries", "bt709", "-color_trc", "bt709", "-color_range", "tv",
         "-c:a", "aac", "-b:a", "192k", "-c:v:1", "mjpeg", "-disposition:v:1", "attached_pic", "-movflags", "+faststart", sys.argv[1]]
subprocess.run(args, check=True)
