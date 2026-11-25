# Worked example from the original project. Paths are placeholders: point them at your files.
"""OpenClaw 10.1 short: cut C0519.MP4 to the six feature passages and add graphics.

Steps: (1) frame-accurate cut of picture + raw audio, (2) speech cleanup and
loudness (high-pass, light denoise with latency compensation, two-pass loudnorm
to -16 LUFS), (3) composite graphics and mux.
"""
import json, os, subprocess, sys
import numpy as np

from render import FFMPEG as FF  # run with PYTHONPATH={baseDir}/scripts
SRC = "/path/to/release videos/10.1/C0519.MP4"
PROJ = "/path/to/release videos/10.1"
CLIPS = PROJ + "/Motion Graphics/clips"
WORK = sys.argv[1]
OUT = sys.argv[2]
FPS = 60000 / 1001
SR = 48000

# source passages (seconds), cut points chosen in silence
SEGS = [
    ("A intro", 60.86, 65.70),     # "OpenClaw just updated to 10.1, and here's a few features..."
    ("D together", 246.90, 253.96),  # "...all go together. We've got better skill discovery, we've got richer MCP applications,"
    ("E rest", 272.50, 276.46),    # "External backups, conversation snooze, and better offline continuity."
    ("F mac+close", 433.30, 445.02),  # "...the Mac setup is now even simpler... So go update to 10.1..."
]
LEAD = 180          # frames of title card before footage

os.makedirs(WORK, exist_ok=True)
segs = []
pos = LEAD
for name, a, b in SEGS:
    fi, fo = round(a * FPS), round(b * FPS)
    segs.append(dict(name=name, f_in=fi, n=fo - fi, at=pos))
    pos += fo - fi
FOOT_END = pos
S = {s["name"][0]: s for s in segs}
OUTRO_AT = FOOT_END - 18
TOTAL = OUTRO_AT + round(3.3033 * FPS)
PLACE = [
    ("intro-title", 0),
    ("card-01-05-features", S["D"]["at"] + round((249.60 - 246.90) * FPS)),
    ("lt-06-mac-setup", S["F"]["at"] + round(3.3 * FPS)),
    ("lt-07-cta", S["F"]["at"] + round(7.75 * FPS)),
    ("outro-foundation", OUTRO_AT),
]


def run(args):
    subprocess.run([FF, "-v", "error", "-y"] + args, check=True)


# ---- 1. cut ----
base, raw = f"{WORK}/base.mov", f"{WORK}/raw.wav"
if not os.path.exists(base):
    args, fc = [], []
    for k, s in enumerate(segs):
        args += ["-ss", f"{s['f_in'] / FPS:.6f}", "-i", SRC]
        d = s["n"] / FPS
        fc.append(f"[{k}:v]trim=end_frame={s['n']},setpts=PTS-STARTPTS[v{k}]")
        fc.append(f"[{k}:a]atrim=end_sample={round(d * SR)},asetpts=PTS-STARTPTS,"
                  f"afade=t=in:d=0.008,afade=t=out:st={d - 0.008:.6f}:d=0.008[a{k}]")
    fc.append("".join(f"[v{k}][a{k}]" for k in range(len(segs))) + f"concat=n={len(segs)}:v=1:a=1[v][a]")
    run(args + ["-filter_complex", ";".join(fc), "-map", "[v]", "-c:v", "prores_ks", "-profile:v", "3",
                "-colorspace", "bt709", "-color_primaries", "bt709", "-color_trc", "bt709", base,
                "-map", "[a]", "-c:a", "pcm_s24le", raw])


# ---- 2. audio ----
def rd(p):
    """mono float32 at the native rate, decoded by ffmpeg"""
    b = subprocess.run([FF, "-v", "error", "-i", p, "-ac", "1", "-f", "f32le", "-"], capture_output=True, check=True).stdout
    return np.frombuffer(b, np.float32)


def lag(a, b, maxlag=4800):
    """samples by which b lags a"""
    n = min(len(a), len(b))
    A = np.fft.rfft(a[:n], 2 * n)
    B = np.fft.rfft(b[:n], 2 * n)
    c = np.fft.irfft(np.conj(A) * B)
    c = np.concatenate([c[-maxlag:], c[:maxlag + 1]])
    return int(np.argmax(c)) - maxlag


clean = f"{WORK}/clean.wav"
run(["-i", raw, "-af", "highpass=f=75,afftdn=nr=6:nf=-45", "-c:a", "pcm_s24le", f"{WORK}/den.wav"])
L = lag(rd(raw), rd(f"{WORK}/den.wav"))
print("denoiser latency (samples):", L)
comp = f"atrim=start_sample={L},asetpts=PTS-STARTPTS," if L > 0 else ""
m = subprocess.run([FF, "-hide_banner", "-i", f"{WORK}/den.wav", "-af", comp + "loudnorm=I=-16:TP=-2:LRA=11:print_format=json",
                    "-f", "null", "-"], capture_output=True, text=True).stderr
mj = json.loads(m[m.rindex("{"):m.rindex("}") + 1])
ln = (f"loudnorm=I=-16:TP=-2:LRA=11:measured_I={mj['input_i']}:measured_TP={mj['input_tp']}:"
      f"measured_LRA={mj['input_lra']}:measured_thresh={mj['input_thresh']}:offset={mj['target_offset']}:linear=true")
run(["-i", f"{WORK}/den.wav", "-af", comp + ln + f",aresample={SR}", "-c:a", "pcm_s24le", clean])
L2 = lag(rd(raw), rd(clean))
print("residual lag after compensation (samples):", L2)

# ---- 3. composite ----
args = ["-i", base, "-i", clean]
fc = [f"[0:v]tpad=start={LEAD}:stop={TOTAL - FOOT_END}:color=black[v0]",
      f"aevalsrc=0|0:d={LEAD / FPS:.6f}:s={SR},aformat=sample_fmts=fltp:channel_layouts=stereo[sil]",
      f"[1:a]aformat=sample_fmts=fltp:sample_rates={SR}:channel_layouts=stereo[sp]",
      f"[sil][sp]concat=n=2:v=0:a=1,apad=whole_dur={TOTAL / FPS:.6f}[a]"]
last = "v0"
for k, (name, f0) in enumerate(PLACE, 2):
    args += ["-i", f"{CLIPS}/{name}.mov"]
    fc.append(f"[{k}:v]setpts=PTS-STARTPTS+{f0 / FPS:.6f}/TB[g{k}]")
    fc.append(f"[{last}][g{k}]overlay=eof_action=pass:format=yuv444:repeatlast=0[v{k}]")
    last = f"v{k}"
fc.append(f"[{last}]format=yuv420p[out]")
run(args + ["-filter_complex", ";".join(fc), "-map", "[out]", "-map", "[a]", "-frames:v", str(TOTAL),
            "-c:v", "libx264", "-preset", "slow", "-crf", "14", "-profile:v", "high",
            "-colorspace", "bt709", "-color_primaries", "bt709", "-color_trc", "bt709", "-color_range", "tv",
            "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart",
            "-metadata", "title=OpenClaw 10.1 update", OUT])
json.dump({"fps": "60000/1001", "lead_frames": LEAD, "total_frames": TOTAL, "segments": segs,
           "placement_frames": PLACE, "denoiser_latency_samples": L, "residual_lag_samples": L2},
          open(f"{WORK}/edl.json", "w"), indent=1)
print("total frames", TOTAL, "=", round(TOTAL / FPS, 3), "s")
