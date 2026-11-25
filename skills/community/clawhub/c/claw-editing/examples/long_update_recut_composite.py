# Worked example from the original project. Paths are placeholders: point them at your files.
"""v3: new intro card, opening lines cut, section graphics shifted, new outro.

v1 output frames 485..10774 (from "There's been a lot of new stuff..." to the end
of the last spoken passage) are placed at frame 180, after the intro card.
"""
from render import FFMPEG
import json, subprocess, sys
D = "/path/to/project"
FF = FFMPEG
CLIPS = D + "/Motion Graphics v1/clips"
FPS = 60000 / 1001
SRC_IN, SRC_OUT = 485, 10775          # v1 frames kept [in, out)
LEAD = 180                             # footage starts here (3.003 s)
SHIFT = LEAD - SRC_IN                  # v1 frame -> v3 frame
BODY = SRC_OUT - SRC_IN
OUTRO_AT = LEAD + BODY - 18            # outro dissolves over the last 0.3 s of footage
OUTRO_N = round(3.3033 * FPS)
TOTAL = OUTRO_AT + OUTRO_N
AF = "aformat=sample_fmts=fltp:sample_rates=48000:channel_layouts=stereo"
tl = json.load(open("timeline.json"))
place = [("intro-title", 0)]
for name, (start, dur) in sorted(tl.items(), key=lambda kv: kv[1][0]):
    place.append((name, round(start * FPS) + SHIFT))
place.append(("outro-foundation", OUTRO_AT))
args = [FF, "-v", "error", "-y", "-i", D + "/OpenClaw Update - Final v1.mp4"]
fc = [f"[0:v]trim=start_frame={SRC_IN}:end_frame={SRC_OUT},setpts=PTS-STARTPTS,"
      f"tpad=start={LEAD}:stop={TOTAL - LEAD - BODY}:color=black[v0]",
      f"[0:a]atrim=start={SRC_IN / FPS:.6f}:end={SRC_OUT / FPS:.6f},asetpts=PTS-STARTPTS,"
      f"afade=t=in:d=0.015,afade=t=out:st={BODY / FPS - 0.02:.6f}:d=0.02,{AF}[body]",
      # leading silence via concat (adelay is dropped by this ffmpeg build when followed by apad)
      f"aevalsrc=0|0:d={LEAD / FPS:.6f}:s=48000,{AF}[sil]",
      f"[sil][body]concat=n=2:v=0:a=1,apad=whole_dur={TOTAL / FPS:.6f}[a]"]
last = "v0"
for k, (name, f0) in enumerate(place, 1):
    args += ["-i", f"{CLIPS}/{name}.mov"]
    fc.append(f"[{k}:v]setpts=PTS-STARTPTS+{f0 / FPS:.6f}/TB[g{k}]")
    fc.append(f"[{last}][g{k}]overlay=eof_action=pass:format=yuv444:repeatlast=0[v{k}]")
    last = f"v{k}"
fc.append(f"[{last}]format=yuv420p[out]")
args += ["-filter_complex", ";".join(fc), "-map", "[out]", "-map", "[a]", "-frames:v", str(TOTAL),
         "-c:v", "libx264", "-preset", "slow", "-crf", "14", "-profile:v", "high",
         "-colorspace", "bt709", "-color_primaries", "bt709", "-color_trc", "bt709", "-color_range", "tv",
         "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-movflags", "+faststart",
         "-metadata", "title=OpenClaw update and other features you should know", sys.argv[1]]
json.dump({"total_frames": TOTAL, "placement_frames": place}, open("timeline_v3.json", "w"), indent=1)
subprocess.run(args, check=True)
