"""Cut a raw recording into a finished OpenClaw video from a JSON edit plan.

usage: python edit.py plan.json

plan.json:
{
  "source": "/path/C0519.MP4",
  "output": "/path/OpenClaw 10.1 Update - v1.mp4",     # never the source; version the name
  "work": "/path/scratch/work",                         # intermediates (base.mov, wavs, edl.json)
  "clips_dir": "/path/Motion Graphics/clips",           # ProRes 4444 clips rendered with render.py/overlays.py
  "fps": "60000/1001",                                  # the source's r_frame_rate
  "lead_frames": 180,                                   # title card before footage (3.003 s at 59.94)
  "segments": [ {"name": "A intro", "in": 60.86, "out": 65.70}, ... ],   # source seconds, cut in silence
  "overlays": [                                         # clip = file stem in clips_dir
      {"clip": "intro-title", "at": 0},                 #   "at": output seconds, or
      {"clip": "card-01-05-features", "segment": "D", "offset": 2.70}   # segment name prefix + seconds in
  ],
  "outro": {"clip": "outro-foundation", "seconds": 3.3033, "overlap_frames": 18},
  "thumbnail": "/path/thumbnail.png",                   # optional: held 1 s as first frame + embedded cover art
  "audio": {"denoise": true, "lufs": -16}
}
Audio: 8 ms fades at every splice, 75 Hz high-pass, light afftdn (its latency is measured and removed),
two-pass loudnorm. Silent under the title/end cards. Writes <work>/edl.json with the final placement.
"""
import json, os, subprocess, sys
from fractions import Fraction
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from render import FFMPEG

plan = json.load(open(sys.argv[1]))
SRC, OUT, WORK, CLIPS = plan["source"], plan["output"], plan["work"], plan["clips_dir"]
FR = Fraction(plan.get("fps", "60000/1001"))
FPS = float(FR)
SR = 48000
LEAD = int(plan.get("lead_frames", round(3.0 * FPS)))
assert os.path.abspath(OUT) != os.path.abspath(SRC), "refusing to overwrite the source"
os.makedirs(WORK, exist_ok=True)


def run(args):
    subprocess.run([FFMPEG, "-v", "error", "-y"] + args, check=True)


segs, pos = [], LEAD
for sg in plan["segments"]:
    fi, fo = round(sg["in"] * FPS), round(sg["out"] * FPS)
    segs.append(dict(name=sg["name"], f_in=fi, n=fo - fi, at=pos))
    pos += fo - fi
FOOT_END = pos
outro = plan.get("outro")
OUTRO_AT = FOOT_END - (outro.get("overlap_frames", 18) if outro else 0)
TOTAL = OUTRO_AT + (round(outro["seconds"] * FPS) if outro else 0)
TOTAL = max(TOTAL, FOOT_END)


def seg_at(prefix):
    for s in segs:
        if s["name"].split()[0] == prefix or s["name"] == prefix:
            return s["at"]
    raise KeyError(prefix)


place = []
for o in plan.get("overlays", []):
    f0 = round(o["at"] * FPS) if "at" in o else seg_at(o["segment"]) + round(o.get("offset", 0) * FPS)
    place.append((o["clip"], f0))
if outro:
    place.append((outro["clip"], OUTRO_AT))

# ---- 1. cut picture + raw audio (frame-aligned; same -ss for both keeps sync) ----
base, raw = f"{WORK}/base.mov", f"{WORK}/raw.wav"
if not (os.path.exists(base) and os.path.exists(raw)):
    args, fc = [], []
    for k, s in enumerate(segs):
        d = s["n"] / FPS
        args += ["-ss", f"{s['f_in'] / FPS:.6f}", "-i", SRC]
        fc.append(f"[{k}:v]trim=end_frame={s['n']},setpts=PTS-STARTPTS[v{k}]")
        fc.append(f"[{k}:a]aresample={SR},atrim=end_sample={round(d * SR)},asetpts=PTS-STARTPTS,"
                  f"afade=t=in:d=0.008,afade=t=out:st={d - 0.008:.6f}:d=0.008[a{k}]")
    fc.append("".join(f"[v{k}][a{k}]" for k in range(len(segs))) + f"concat=n={len(segs)}:v=1:a=1[v][a]")
    run(args + ["-filter_complex", ";".join(fc), "-map", "[v]", "-c:v", "prores_ks", "-profile:v", "3",
                "-colorspace", "bt709", "-color_primaries", "bt709", "-color_trc", "bt709", base,
                "-map", "[a]", "-c:a", "pcm_s24le", raw])


# ---- 2. audio cleanup ----
def rd(p):
    b = subprocess.run([FFMPEG, "-v", "error", "-i", p, "-ac", "1", "-f", "f32le", "-"], capture_output=True, check=True).stdout
    return np.frombuffer(b, np.float32)


def lag(a, b, maxlag=4800):
    n = min(len(a), len(b))
    c = np.fft.irfft(np.conj(np.fft.rfft(a[:n], 2 * n)) * np.fft.rfft(b[:n], 2 * n))
    c = np.concatenate([c[-maxlag:], c[:maxlag + 1]])
    return int(np.argmax(c)) - maxlag


ac = plan.get("audio", {})
lufs = ac.get("lufs", -16)
clean = f"{WORK}/clean.wav"
src_for_ln = raw
L = 0
if ac.get("denoise", True):
    run(["-i", raw, "-af", "highpass=f=75,afftdn=nr=6:nf=-45", "-c:a", "pcm_s24le", f"{WORK}/den.wav"])
    L = lag(rd(raw), rd(f"{WORK}/den.wav"))
    src_for_ln = f"{WORK}/den.wav"
comp = f"atrim=start_sample={L},asetpts=PTS-STARTPTS," if L > 0 else ""
m = subprocess.run([FFMPEG, "-hide_banner", "-i", src_for_ln, "-af", comp + f"loudnorm=I={lufs}:TP=-2:LRA=11:print_format=json",
                    "-f", "null", "-"], capture_output=True, text=True).stderr
mj = json.loads(m[m.rindex("{"):m.rindex("}") + 1])
ln = (f"loudnorm=I={lufs}:TP=-2:LRA=11:measured_I={mj['input_i']}:measured_TP={mj['input_tp']}:"
      f"measured_LRA={mj['input_lra']}:measured_thresh={mj['input_thresh']}:offset={mj['target_offset']}:linear=true")
run(["-i", src_for_ln, "-af", comp + ln + f",aresample={SR}", "-c:a", "pcm_s24le", clean])
L2 = lag(rd(raw), rd(clean))
print(f"denoiser latency {L} samples removed; residual lag {L2} samples (want 0)")

# ---- 3. composite + mux ----
thumb = plan.get("thumbnail")
TH = round(FPS) if thumb else 0
args = ["-i", base, "-i", clean]
AF = f"aformat=sample_fmts=fltp:sample_rates={SR}:channel_layouts=stereo"
fc = [f"[0:v]tpad=start={LEAD}:stop={TOTAL - FOOT_END}:color=black[v0]",
      # leading silence via concat: this ffmpeg build drops adelay when apad follows it
      f"aevalsrc=0|0:d={(LEAD + TH) / FPS:.6f}:s={SR},{AF}[sil]",
      f"[1:a]{AF}[sp]",
      f"[sil][sp]concat=n=2:v=0:a=1,apad=whole_dur={(TOTAL + TH) / FPS:.6f}[a]"]
last = "v0"
for k, (name, f0) in enumerate(place, 2):
    args += ["-i", f"{CLIPS}/{name}.mov"]
    fc.append(f"[{k}:v]setpts=PTS-STARTPTS+{f0 / FPS:.6f}/TB[g{k}]")
    fc.append(f"[{last}][g{k}]overlay=eof_action=pass:format=yuv444:repeatlast=0[v{k}]")
    last = f"v{k}"
fc.append(f"[{last}]format=yuv420p[body]")
maps = ["-map", "[out]", "-map", "[a]"]
extra = []
if thumb:
    n = len(place) + 2
    args += ["-loop", "1", "-framerate", str(FR), "-t", f"{TH / FPS:.6f}", "-i", thumb, "-i", thumb]
    fc.append(f"[{n}:v]scale=1920:1080,format=yuv420p,setsar=1[th]")
    fc.append("[th][body]concat=n=2:v=1:a=0[out]")
    maps += ["-map", f"{n + 1}:v"]
    extra = ["-c:v:1", "mjpeg", "-pix_fmt:v:1", "yuvj420p", "-disposition:v:1", "attached_pic"]
else:
    fc[-1] = f"[{last}]format=yuv420p[out]"
run(args + ["-filter_complex", ";".join(fc)] + maps + ["-frames:v:0", str(TOTAL + TH),
            "-c:v:0", "libx264", "-preset", "slow", "-crf", "14", "-profile:v:0", "high", "-r:v:0", str(FR),
            "-colorspace:v:0", "bt709", "-color_primaries:v:0", "bt709", "-color_trc:v:0", "bt709", "-color_range:v:0", "tv",
            "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart"] + extra + [OUT])
json.dump({"fps": str(FR), "lead_frames": LEAD, "thumbnail_frames": TH, "total_frames": TOTAL + TH,
           "segments": segs, "placement_frames": place, "denoiser_latency_samples": L, "residual_lag_samples": L2},
          open(f"{WORK}/edl.json", "w"), indent=1)
print("wrote", OUT, f"({(TOTAL + TH) / FPS:.3f} s)")
