# FFmpeg Recipes — Ready-Made Commands

## Index
1. [Basics](#basics)
2. [Slideshow](#slideshow)
3. [Text and Subtitles](#text-and-subtitles)
4. [Compositing](#compositing)
5. [Audio](#audio)
6. [Transitions](#transitions)
7. [Social Media](#social-media)
8. [Optimization](#optimization)
9. [Effects](#effects)
10. [Automation with Python](#python)
11. [Silence Removal](#silence-removal)
12. [Transcription with faster-whisper](#transcription)

---

## Basics

### Convert format
```bash
ffmpeg -i input.mov -c:v libx264 -c:a aac -preset fast output.mp4
```

### Resize
```bash
# To 1080p maintaining aspect ratio
ffmpeg -i input.mp4 -vf "scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2" output.mp4

# To 9:16 (vertical/reels)
ffmpeg -i input.mp4 -vf "scale=1080:1920:force_original_aspect_ratio=decrease,pad=1080:1920:(ow-iw)/2:(oh-ih)/2:black" output.mp4
```

### Trim duration
```bash
# First 30 seconds
ffmpeg -i input.mp4 -t 30 -c copy output.mp4

# From 1:00 to 2:30
ffmpeg -i input.mp4 -ss 00:01:00 -to 00:02:30 -c copy output.mp4
```

### Extract audio
```bash
ffmpeg -i video.mp4 -vn -acodec libmp3lame audio.mp3
```

### Extract frames
```bash
# 1 frame per second
ffmpeg -i video.mp4 -vf "fps=1" frame_%04d.png

# Specific frame (at 5 seconds)
ffmpeg -i video.mp4 -ss 00:00:05 -vframes 1 thumbnail.png
```

---

## Slideshow

### Basic (images in sequence)
```bash
# 3 seconds per image, fade in/out
ffmpeg -framerate 1/3 -i img_%d.png \
  -c:v libx264 -r 30 -pix_fmt yuv420p \
  slideshow.mp4
```

### With zoom (Ken Burns effect)
```bash
ffmpeg -loop 1 -i img.png -t 5 \
  -vf "zoompan=z='min(zoom+0.0015,1.5)':d=150:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s=1920x1080" \
  -c:v libx264 -pix_fmt yuv420p zoom.mp4
```

### Slideshow with music
```bash
# Create slideshow and add audio
ffmpeg -framerate 1/4 -i img_%d.png -i music.mp3 \
  -c:v libx264 -r 30 -pix_fmt yuv420p \
  -shortest slideshow_music.mp4
```

---

## Text and Subtitles

### Simple overlaid text
```bash
ffmpeg -i video.mp4 \
  -vf "drawtext=text='Hello World':fontcolor=white:fontsize=72:x=(w-text_w)/2:y=(h-text_h)/2:shadowcolor=black:shadowx=2:shadowy=2" \
  output.mp4
```

### Text with background (lower third)
```bash
ffmpeg -i video.mp4 \
  -vf "drawbox=x=0:y=ih-120:w=iw:h=120:color=black@0.7:t=fill, \
       drawtext=text='Title Here':fontcolor=white:fontsize=48:x=40:y=h-100" \
  output.mp4
```

### Animated text (appears and disappears)
```bash
ffmpeg -i video.mp4 \
  -vf "drawtext=text='Animated Text':fontcolor=white:fontsize=64:x=(w-text_w)/2:y=(h-text_h)/2:enable='between(t,2,5)':alpha='if(lt(t,2.5),((t-2)*2),if(gt(t,4.5),(5-t)*2,1))'" \
  output.mp4
```

### SRT Subtitles
```bash
ffmpeg -i video.mp4 -vf "subtitles=subtitles.srt:force_style='FontSize=24,PrimaryColour=&Hffffff,OutlineColour=&H000000,Outline=2'" output.mp4
```

---

## Compositing

### Picture-in-picture
```bash
ffmpeg -i main.mp4 -i pip.mp4 \
  -filter_complex "[1:v]scale=320:240[pip];[0:v][pip]overlay=W-w-20:H-h-20" \
  output.mp4
```

### Logo/watermark
```bash
ffmpeg -i video.mp4 -i logo.png \
  -filter_complex "[1:v]scale=100:-1[logo];[0:v][logo]overlay=W-w-20:20:format=auto" \
  output.mp4
```

### Grid (4 videos)
```bash
ffmpeg -i v1.mp4 -i v2.mp4 -i v3.mp4 -i v4.mp4 \
  -filter_complex "[0:v]scale=960:540[a];[1:v]scale=960:540[b];[2:v]scale=960:540[c];[3:v]scale=960:540[d];[a][b]hstack[top];[c][d]hstack[bottom];[top][bottom]vstack" \
  -c:v libx264 grid.mp4
```

### Colored background with text
```bash
ffmpeg -f lavfi -i "color=c=0x667eea:s=1080x1920:d=5" \
  -vf "drawtext=text='Your text':fontcolor=white:fontsize=72:x=(w-text_w)/2:y=(h-text_h)/2" \
  -c:v libx264 -pix_fmt yuv420p bg_text.mp4
```

---

## Audio

### Add background music
```bash
ffmpeg -i video.mp4 -i music.mp3 \
  -filter_complex "[1:a]volume=0.2[bg];[0:a][bg]amix=inputs=2:duration=first" \
  -c:v copy output.mp4
```

### Replace audio
```bash
ffmpeg -i video.mp4 -i new_audio.mp3 \
  -c:v copy -map 0:v -map 1:a -shortest output.mp4
```

### Audio fade in/out
```bash
ffmpeg -i video.mp4 \
  -af "afade=t=in:st=0:d=2,afade=t=out:st=28:d=2" \
  output.mp4
```

### Normalize volume
```bash
ffmpeg -i video.mp4 -af "loudnorm=I=-14:LRA=11:TP=-1.5" output.mp4
```

### Remove audio
```bash
ffmpeg -i video.mp4 -an -c:v copy output_silent.mp4
```

---

## Transitions

### Fade between 2 videos
```bash
ffmpeg -i v1.mp4 -i v2.mp4 \
  -filter_complex "[0:v]fade=t=out:st=4:d=1[v0];[1:v]fade=t=in:st=0:d=1[v1];[v0][v1]concat=n=2:v=1:a=0" \
  output.mp4
```

### Crossfade
```bash
ffmpeg -i v1.mp4 -i v2.mp4 \
  -filter_complex "xfade=transition=fade:duration=1:offset=4" \
  output.mp4
```

### Available transitions in xfade
fade, wipeleft, wiperight, wipeup, wipedown, slideleft, slideright, slideup, slidedown, circlecrop, rectcrop, distance, fadeblack, fadewhite, radial, smoothleft, smoothright, smoothup, smoothdown, circleopen, circleclose, vertopen, vertclose, horzopen, horzclose, dissolve, pixelize, diagtl, diagtr, diagbl, diagbr, hlslice, hrslice, vuslice, vdslice, hblur, fadegrays, squeezev, squeezeh, zoomin

---

## Social Media

### Reels/TikTok (vertical 9:16)
```bash
# Convert horizontal to vertical with blur background
ffmpeg -i horizontal.mp4 \
  -filter_complex "[0:v]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,boxblur=20[bg];[0:v]scale=1080:-1[fg];[bg][fg]overlay=(W-w)/2:(H-h)/2" \
  -c:v libx264 -c:a aac reels.mp4
```

### YouTube thumbnail
```bash
ffmpeg -i video.mp4 -ss 00:00:05 -vframes 1 \
  -vf "scale=1280:720" thumbnail.jpg
```

### GIF for social media
```bash
ffmpeg -i video.mp4 -ss 0 -t 3 \
  -vf "fps=15,scale=480:-1:flags=lanczos,split[s0][s1];[s0]palettegen[p];[s1][p]paletteuse" \
  output.gif
```

---

## Optimization

### Reduce size (maintain quality)
```bash
# CRF 23 = good quality, smaller file
ffmpeg -i input.mp4 -c:v libx264 -crf 23 -preset medium -c:a aac -b:a 128k output.mp4
```

### Web-optimized (fast start)
```bash
ffmpeg -i input.mp4 -c:v libx264 -crf 23 -movflags +faststart output.mp4
```

### Compress for WhatsApp (<16MB)
```bash
# Calculate bitrate: (16MB * 8192) / duration_in_seconds - 128 (audio)
# Example for 30s: (16*8192)/30 - 128 = ~4240 kbps
ffmpeg -i input.mp4 -c:v libx264 -b:v 4000k -maxrate 4500k -bufsize 8000k -c:a aac -b:a 128k output.mp4
```

---

## Effects

### Speed (speed up / slow motion)
```bash
# 2x faster
ffmpeg -i input.mp4 -filter_complex "[0:v]setpts=0.5*PTS[v];[0:a]atempo=2.0[a]" -map "[v]" -map "[a]" fast.mp4

# 0.5x slower
ffmpeg -i input.mp4 -filter_complex "[0:v]setpts=2.0*PTS[v];[0:a]atempo=0.5[a]" -map "[v]" -map "[a]" slow.mp4
```

### Reverse
```bash
ffmpeg -i input.mp4 -vf reverse -af areverse reversed.mp4
```

### Basic color grading
```bash
# Increase contrast and saturation
ffmpeg -i input.mp4 -vf "eq=contrast=1.2:saturation=1.3:brightness=0.05" output.mp4

# Cinematic look (lift shadows, lower highlights)
ffmpeg -i input.mp4 -vf "curves=m='0/0.05 0.5/0.5 1/0.95'" output.mp4
```

### Vignette
```bash
ffmpeg -i input.mp4 -vf "vignette=PI/4" output.mp4
```

---

## Python

### MoviePy — Video compositing
```python
from moviepy.editor import *

# Slideshow with text
clips = []
for i, img_path in enumerate(image_paths):
    clip = ImageClip(img_path).set_duration(3).resize((1920, 1080))
    txt = TextClip(titles[i], fontsize=48, color='white', font='Arial-Bold')
    txt = txt.set_position(('center', 'bottom')).set_duration(3)
    clips.append(CompositeVideoClip([clip, txt]).crossfadein(0.5))

final = concatenate_videoclips(clips, method="compose")
final.write_videofile("slideshow.mp4", fps=30)
```

### Pillow — Generate frames with text
```python
from PIL import Image, ImageDraw, ImageFont

def create_text_frame(text, size=(1080, 1920), bg_color="#1a1a2e", text_color="white"):
    img = Image.new('RGB', size, bg_color)
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype("/path/to/font.ttf", 64)
    bbox = draw.textbbox((0, 0), text, font=font)
    x = (size[0] - (bbox[2] - bbox[0])) // 2
    y = (size[1] - (bbox[3] - bbox[1])) // 2
    draw.text((x, y), text, fill=text_color, font=font)
    return img
```

---

## Silence Removal

Automatically cut dead air from talking-head footage while preserving natural pauses.

### Step 1 — Detect silences

```bash
# Outputs silence_start / silence_end timestamps to stderr
ffmpeg -i input.mp4 -af silencedetect=noise=-30dB:d=0.5 -f null - 2>&1 | grep silence
```

Parameters:
- `noise=-30dB` — audio level below which a region is considered silent (adjust to -40dB for quieter recordings)
- `d=0.5` — minimum silence duration in seconds before a cut is triggered

### Step 2 — Extract non-silence segments

For each non-silence region `[segStart, segEnd]`, extract to a transport stream (`.ts`) file.
Add `naturalPause / 2` (e.g. 0.15s) padding on each edge to preserve natural cadence:

```bash
# Example: keep segment from 0.000s to 4.350s (0.15s tail of preceding silence)
ffmpeg -y -i input.mp4 \
  -ss 0.000 -to 4.350 \
  -c copy -avoid_negative_ts make_zero \
  _seg_0000.ts

ffmpeg -y -i input.mp4 \
  -ss 5.650 -to 12.800 \
  -c copy -avoid_negative_ts make_zero \
  _seg_0001.ts
```

Use `.ts` (MPEG-TS) not `.mp4` for intermediate segments — it handles PTS discontinuities cleanly during concat.

### Step 3 — Reassemble with concat demuxer

```bash
# Write concat list
printf "file '_seg_0000.ts'\nfile '_seg_0001.ts'\n" > _concat_list.txt

# Reassemble (stream copy = no re-encoding, fast)
ffmpeg -y -f concat -safe 0 -i _concat_list.txt -c copy output.mp4

# Clean up temp files
rm _seg_*.ts _concat_list.txt
```

### All-in-one bash script skeleton

```bash
#!/usr/bin/env bash
INPUT="$1"
OUTPUT="${2:-edited-footage.mp4}"
THRESHOLD="-30"
MIN_SILENCE="0.5"
HALF_PAUSE="0.15"

# Detect silences
SILENCE_LOG=$(ffmpeg -i "$INPUT" -af "silencedetect=noise=${THRESHOLD}dB:d=${MIN_SILENCE}" -f null - 2>&1)

# Get total duration
DURATION=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$INPUT")

# Parse and build segments (Python handles the math cleanly)
python3 - "$INPUT" "$OUTPUT" "$DURATION" "$HALF_PAUSE" <<'EOF'
import sys, re, subprocess, os

input_path, output_path, total_dur, half_pause = sys.argv[1], sys.argv[2], float(sys.argv[3]), float(sys.argv[4])
log = subprocess.run(
    ["ffmpeg", "-i", input_path, "-af", "silencedetect=noise=-30dB:d=0.5", "-f", "null", "-"],
    capture_output=True, text=True
).stderr

starts = [float(m) for m in re.findall(r"silence_start:\s*([\d.]+)", log)]
ends   = [float(m) for m in re.findall(r"silence_end:\s*([\d.]+)",   log)]

segments, cursor = [], 0.0
for s, e in zip(starts, ends):
    seg_end = s + half_pause
    if seg_end > cursor:
        segments.append((cursor, min(seg_end, total_dur)))
    cursor = max(cursor, e - half_pause)
if cursor < total_dur:
    segments.append((cursor, total_dur))

temp_files, concat_lines = [], []
for i, (start, end) in enumerate(segments):
    tmp = f"_seg_{i:04d}.ts"
    temp_files.append(tmp)
    subprocess.run(["ffmpeg", "-y", "-i", input_path, "-ss", f"{start:.3f}", "-to", f"{end:.3f}",
                    "-c", "copy", "-avoid_negative_ts", "make_zero", tmp], check=True)
    concat_lines.append(f"file '{tmp}'")

with open("_concat_list.txt", "w") as f:
    f.write("\n".join(concat_lines))

subprocess.run(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", "_concat_list.txt", "-c", "copy", output_path], check=True)

for f in temp_files + ["_concat_list.txt"]:
    os.unlink(f)
print(f"Done: {output_path}")
EOF
```

---

## Transcription with faster-whisper

Word-level transcription with timestamps — useful for subtitle generation, silence detection, and transcript-anchored overlay placement.

### Installation

```bash
pip install faster-whisper
```

### Basic usage (CLI wrapper)

```bash
# Transcribe to JSON with word-level timestamps
python3 - audio.wav > transcription.json <<'EOF'
import json, sys
from faster_whisper import WhisperModel

audio_path = sys.argv[1]
model = WhisperModel("medium", device="cpu", compute_type="int8")
segments, info = model.transcribe(
    audio_path,
    beam_size=5,
    word_timestamps=True,
    vad_filter=True,        # automatically skips non-speech
)

result = {"language": info.language, "segments": []}
for seg in segments:
    words = [
        {"word": w.word.strip(), "start": round(w.start, 3), "end": round(w.end, 3)}
        for w in seg.words
    ]
    result["segments"].append({
        "id": seg.id,
        "start": round(seg.start, 3),
        "end": round(seg.end, 3),
        "text": seg.text.strip(),
        "words": words,
    })

print(json.dumps(result, indent=2))
EOF
```

### Output structure

```json
{
  "language": "en",
  "segments": [
    {
      "id": 0,
      "start": 0.0,
      "end": 3.5,
      "text": "Hello and welcome to this tutorial",
      "words": [
        { "word": "Hello",   "start": 0.0,  "end": 0.4 },
        { "word": "and",     "start": 0.45, "end": 0.6 },
        { "word": "welcome", "start": 0.65, "end": 1.1 }
      ]
    }
  ]
}
```

### Model selection

| Model | Speed | Accuracy | Best for |
|---|---|---|---|
| `tiny` | Fastest | Low | Quick drafts |
| `base` | Fast | Medium | Social clips |
| `medium` | Moderate | High | Production (default) |
| `large-v3` | Slow | Highest | Long-form accuracy |

### Extract audio from video before transcribing

```bash
# Extract 16kHz mono WAV (optimal for Whisper)
ffmpeg -i video.mp4 -ar 16000 -ac 1 -vn audio.wav
```

### Generate SRT from transcription JSON

```python
import json

def ms_to_srt(ms):
    h, r = divmod(ms, 3600000)
    m, r = divmod(r, 60000)
    s, ms = divmod(r, 1000)
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"

with open("transcription.json") as f:
    data = json.load(f)

lines = []
for i, seg in enumerate(data["segments"], 1):
    lines.append(str(i))
    lines.append(f"{ms_to_srt(int(seg['start']*1000))} --> {ms_to_srt(int(seg['end']*1000))}")
    lines.append(seg["text"])
    lines.append("")

with open("subtitles.srt", "w") as f:
    f.write("\n".join(lines))
```
