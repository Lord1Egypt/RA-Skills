"""Add graphics to an already-edited video without re-cutting it (interviews, podcasts).

usage: python composite.py plan.json

plan.json:
{
  "base": "/path/What is OpenClaw enterprise.mov",      # untouched; picture + audio come from here
  "output": "/path/What is OpenClaw Enterprise - v2.mp4",
  "clips_dir": "/path/Motion Graphics/clips",
  "fps": "30",
  "total_frames": 40415,                                # base video's frame count (ffprobe -count_packets)
  "overlays": [ {"clip": "intro-title", "at": 0.0}, ... ],      # seconds on the base timeline
  "patches": [                                          # optional: swap in clean frames to hide old burned-in overlays
      {"source": "/path/clean.mov", "from_frame": 185, "to_frame": 566, "source_offset_frames": -180}
  ],
  "thumbnail": "/path/thumbnail.png"                    # optional: 1 s first frame + cover art (audio re-encoded)
}
Without a thumbnail the audio is stream-copied (bit-identical).
"""
import json, os, subprocess, sys
from fractions import Fraction
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from render import FFMPEG

p = json.load(open(sys.argv[1]))
FR = Fraction(p.get("fps", "30")); FPS = float(FR)
assert os.path.abspath(p["output"]) != os.path.abspath(p["base"]), "refusing to overwrite the base video"
args = [FFMPEG, "-v", "error", "-stats", "-y", "-i", p["base"]]
fc, last, k = [], "0:v", 1
for i, pa in enumerate(p.get("patches", [])):
    args += ["-i", pa["source"]]
    s0 = pa["from_frame"] + pa["source_offset_frames"]; s1 = pa["to_frame"] + pa["source_offset_frames"]
    fc.append(f"[{k}:v]fps={FR},trim=start_frame={s0}:end_frame={s1},setpts=PTS-STARTPTS+{pa['from_frame']}/{FPS}/TB[pt{i}]")
    fc.append(f"[{last}][pt{i}]overlay=eof_action=pass:repeatlast=0[pb{i}]")
    last, k = f"pb{i}", k + 1
for o in sorted(p["overlays"], key=lambda o: o["at"]):
    args += ["-i", f"{p['clips_dir']}/{o['clip']}.mov"]
    fc.append(f"[{k}:v]setpts=PTS-STARTPTS+{round(o['at'] * FPS)}/{FPS}/TB[g{k}]")
    fc.append(f"[{last}][g{k}]overlay=eof_action=pass:format=yuv444:repeatlast=0[v{k}]")
    last, k = f"v{k}", k + 1
thumb = p.get("thumbnail")
TH = round(FPS) if thumb else 0
if thumb:
    args += ["-loop", "1", "-framerate", str(FR), "-t", f"{TH / FPS:.6f}", "-i", thumb, "-i", thumb]
    fc.append(f"[{last}]format=yuv420p[body]")
    fc.append(f"[{k}:v]scale=1920:1080,format=yuv420p,setsar=1[th]")
    fc.append("[th][body]concat=n=2:v=1:a=0[out]")
    fc.append(f"aevalsrc=0|0:d={TH / FPS:.6f}:s=48000,aformat=sample_fmts=fltp:channel_layouts=stereo[sil]")
    fc.append("[0:a]aformat=sample_fmts=fltp:sample_rates=48000:channel_layouts=stereo[a0]")
    fc.append("[sil][a0]concat=n=2:v=0:a=1[aout]")
    amap, acodec = ["-map", "[aout]", "-map", f"{k + 1}:v"], ["-c:a", "aac", "-b:a", "192k", "-c:v:1", "mjpeg", "-pix_fmt:v:1", "yuvj420p", "-disposition:v:1", "attached_pic"]
else:
    fc.append(f"[{last}]format=yuv420p[out]")
    amap, acodec = ["-map", "0:a"], ["-c:a", "copy"]
args += ["-filter_complex", ";".join(fc), "-map", "[out]"] + amap + ["-frames:v:0", str(p["total_frames"] + TH),
         "-c:v:0", "libx264", "-preset", "medium", "-crf", "16", "-profile:v:0", "high", "-r:v:0", str(FR),
         "-colorspace:v:0", "bt709", "-color_primaries:v:0", "bt709", "-color_trc:v:0", "bt709", "-color_range:v:0", "tv"] + acodec + \
        ["-movflags", "+faststart", p["output"]]
subprocess.run(args, check=True)
print("wrote", p["output"])
