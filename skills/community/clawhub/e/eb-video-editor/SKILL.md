---
name: video-editor
description: "Edits existing videos using ffmpeg and Python. Use ALWAYS when the user wants to edit a video, cut a video, join videos, add subtitles, add music, remove audio, resize a video, convert format, compress a video, extract audio, extract frames, add a watermark, make a timelapse, slow motion, speed up, reverse, add a transition, crop, rotate, adjust brightness/contrast, color grading, generate a GIF, generate a thumbnail, or any manipulation of an existing video file. Also activates when the user mentions: ffmpeg, moviepy, cutting a clip, joining clips, captioning a video, or processing a video."
metadata:
  author: EmersonBraun
  version: "1.1.0"
---

# Video Editor — Video Editing via Code

You are an expert in video editing and manipulation using ffmpeg and Python. You receive existing videos and apply transformations, cuts, compositions, and effects.

## Principles

1. **Understand before editing** — Analyze the input video (resolution, codec, duration, fps, audio) before any operation
2. **Preserve quality** — Use `-c copy` whenever possible (no re-encoding). Re-encode only when necessary (filters, resize, compositing)
3. **Non-destructive** — Never overwrite the original. Always generate a new file
4. **Batch-friendly** — Scripts should work for 1 or 100 videos

## First Step: Analyze the Video

Always start by analyzing the input video:

```bash
# Full video info
ffprobe -v quiet -print_format json -show_format -show_streams input.mp4

# Quick summary
ffprobe -v quiet -show_entries format=duration,size,bit_rate:stream=codec_name,width,height,r_frame_rate,channels -of compact input.mp4
```

Essential information:
- **Resolution**: width x height
- **Codec**: h264, h265, vp9, av1
- **FPS**: frames per second
- **Duration**: in seconds
- **Bitrate**: quality
- **Audio**: codec, sample rate, channels

## Common Operations

### Trim
```bash
# Without re-encoding (fast, keyframe-accurate)
ffmpeg -ss 00:01:00 -to 00:02:30 -i input.mp4 -c copy output.mp4

# With re-encoding (frame-accurate)
ffmpeg -i input.mp4 -ss 00:01:00 -to 00:02:30 -c:v libx264 -c:a aac output.mp4
```

### Concatenate (Join Videos)
```bash
# Create list
echo "file 'v1.mp4'" > list.txt
echo "file 'v2.mp4'" >> list.txt
echo "file 'v3.mp4'" >> list.txt

# Concatenate (same resolution/codec)
ffmpeg -f concat -safe 0 -i list.txt -c copy output.mp4

# Concatenate (different resolutions)
ffmpeg -i v1.mp4 -i v2.mp4 \
  -filter_complex "[0:v]scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080[v0];[1:v]scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080[v1];[v0][v1]concat=n=2:v=1:a=0" \
  output.mp4
```

### Resize
```bash
# Specific resolution
ffmpeg -i input.mp4 -vf "scale=1280:720" -c:a copy output.mp4

# Maintain aspect ratio (width 1080, proportional height)
ffmpeg -i input.mp4 -vf "scale=1080:-2" -c:a copy output.mp4

# Fit in box without distorting
ffmpeg -i input.mp4 -vf "scale=1080:1920:force_original_aspect_ratio=decrease,pad=1080:1920:(ow-iw)/2:(oh-ih)/2:black" output.mp4
```

### Crop (Crop Area)
```bash
# Crop center 1080x1080 from 1920x1080 video
ffmpeg -i input.mp4 -vf "crop=1080:1080:(iw-1080)/2:(ih-1080)/2" output.mp4

# Crop with automatic black border detection
ffmpeg -i input.mp4 -vf "cropdetect" -f null - 2>&1 | tail -5
```

### Rotate
```bash
# 90 degrees clockwise
ffmpeg -i input.mp4 -vf "transpose=1" output.mp4

# 90 degrees counter-clockwise
ffmpeg -i input.mp4 -vf "transpose=2" output.mp4

# 180 degrees
ffmpeg -i input.mp4 -vf "transpose=1,transpose=1" output.mp4
```

### Format Conversion
```bash
# MP4 to WebM (VP9)
ffmpeg -i input.mp4 -c:v libvpx-vp9 -crf 30 -c:a libopus output.webm

# MOV to MP4
ffmpeg -i input.mov -c:v libx264 -c:a aac -preset fast output.mp4

# MP4 to GIF
ffmpeg -i input.mp4 -vf "fps=15,scale=480:-1:flags=lanczos,split[s0][s1];[s0]palettegen[p];[s1][p]paletteuse" output.gif
```

### Compression
```bash
# Good quality, smaller file (CRF 23 = default, 28 = more compressed)
ffmpeg -i input.mp4 -c:v libx264 -crf 23 -preset medium -c:a aac -b:a 128k output.mp4

# For WhatsApp (max 16MB)
# Formula: target_bitrate = (16 * 8192 / duration_seconds) - 128
ffmpeg -i input.mp4 -c:v libx264 -b:v 3000k -maxrate 3500k -bufsize 7000k -c:a aac -b:a 128k -movflags +faststart output.mp4

# 2-pass (best quality/size)
ffmpeg -i input.mp4 -c:v libx264 -b:v 2000k -pass 1 -f null /dev/null
ffmpeg -i input.mp4 -c:v libx264 -b:v 2000k -pass 2 -c:a aac output.mp4
```

## Audio Editing

### Add background music
```bash
ffmpeg -i video.mp4 -i music.mp3 \
  -filter_complex "[1:a]volume=0.2[bg];[0:a][bg]amix=inputs=2:duration=first[out]" \
  -map 0:v -map "[out]" -c:v copy -c:a aac output.mp4
```

### Replace entire audio
```bash
ffmpeg -i video.mp4 -i new_audio.mp3 -c:v copy -map 0:v -map 1:a -shortest output.mp4
```

### Remove audio
```bash
ffmpeg -i video.mp4 -an -c:v copy silent.mp4
```

### Extract audio
```bash
ffmpeg -i video.mp4 -vn -c:a libmp3lame -q:a 2 audio.mp3
```

### Normalize volume
```bash
ffmpeg -i video.mp4 -af "loudnorm=I=-14:LRA=11:TP=-1.5" -c:v copy output.mp4
```

## Subtitles and Text

### Add embedded SRT subtitles
```bash
# Soft subtitles (player shows/hides)
ffmpeg -i video.mp4 -i subs.srt -c copy -c:s mov_text output.mp4

# Hard subtitles (burned-in, always visible)
ffmpeg -i video.mp4 -vf "subtitles=subs.srt:force_style='FontSize=24,PrimaryColour=&Hffffff,OutlineColour=&H000000,Outline=2,MarginV=40'" output.mp4
```

### Generate SRT with Whisper
```bash
pip install openai-whisper
whisper video.mp4 --model base --output_format srt --language pt
```

### Overlaid text
```bash
ffmpeg -i video.mp4 \
  -vf "drawtext=text='Title':fontcolor=white:fontsize=64:x=(w-text_w)/2:y=50:shadowcolor=black:shadowx=3:shadowy=3" \
  output.mp4
```

## Effects and Adjustments

### Speed
```bash
# 2x faster
ffmpeg -i input.mp4 -filter_complex "[0:v]setpts=0.5*PTS[v];[0:a]atempo=2.0[a]" -map "[v]" -map "[a]" fast.mp4

# 0.5x slower
ffmpeg -i input.mp4 -filter_complex "[0:v]setpts=2.0*PTS[v];[0:a]atempo=0.5[a]" -map "[v]" -map "[a]" slow.mp4
```

### Color Grading
```bash
# Brightness, contrast, saturation
ffmpeg -i input.mp4 -vf "eq=brightness=0.05:contrast=1.2:saturation=1.3" output.mp4

# Cinematic (crush blacks, roll highlights)
ffmpeg -i input.mp4 -vf "curves=m='0/0.05 0.5/0.5 1/0.95'" output.mp4

# Black and white
ffmpeg -i input.mp4 -vf "hue=s=0" output.mp4
```

### Stabilization
```bash
# Step 1: Analyze
ffmpeg -i shaky.mp4 -vf vidstabdetect -f null -

# Step 2: Apply
ffmpeg -i shaky.mp4 -vf vidstabtransform=smoothing=10:input=transforms.trf output.mp4
```

### Watermark/Logo
```bash
ffmpeg -i video.mp4 -i logo.png \
  -filter_complex "[1:v]scale=80:-1,format=rgba,colorchannelmixer=aa=0.5[logo];[0:v][logo]overlay=W-w-20:20" \
  output.mp4
```

## Batch Processing

### Convert all MOV to MP4
```bash
for f in *.mov; do
  ffmpeg -i "$f" -c:v libx264 -c:a aac -preset fast "${f%.mov}.mp4"
done
```

### Generate thumbnails for all videos
```bash
for f in *.mp4; do
  ffmpeg -i "$f" -ss 00:00:05 -vframes 1 "thumb_${f%.mp4}.jpg"
done
```

### Resize all to 1080p
```bash
for f in *.mp4; do
  ffmpeg -i "$f" -vf "scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2" -c:a copy "1080p_$f"
done
```

## Editing Workflow

1. **Analyze** — `ffprobe` on the input video
2. **Plan** — List the required operations in order
3. **Chain filters** — Combine operations in a single command when possible (avoids multiple re-encodings)
4. **Execute** — Run the command
5. **Verify** — `ffprobe` on the output, confirm quality
6. **Optimize** — Adjust CRF, bitrate, resolution if needed

## Performance Tips

- Use `-c copy` whenever possible (no re-encoding = instant)
- Use `-preset ultrafast` for quick tests, `-preset slow` for final output
- `-movflags +faststart` for web videos (loads faster)
- For batch processing, use GNU `parallel` to process multiple videos simultaneously
- Hardware acceleration: `-hwaccel auto` (uses GPU if available)

---

## Overlay Compositing

Use `filter_complex` to composite multiple video layers onto a base, with per-overlay time-gating and position control.

### Multiple overlays with time-gating

Each overlay layer is activated only within its time window using `enable='between(t,start,end)'`:

```bash
ffmpeg -y \
  -i base-footage.mp4 \
  -i overlay-01.mov \
  -i overlay-02.mov \
  -i overlay-03.mov \
  -filter_complex "
    [0:v]copy[base];
    [1:v]setpts=PTS-STARTPTS[o0];
    [base][o0]overlay=0:800:enable='between(t,5.0,12.5)'[v0];
    [2:v]setpts=PTS-STARTPTS[o1];
    [v0][o1]overlay=540:0:enable='between(t,14.0,22.0)'[v1];
    [3:v]setpts=PTS-STARTPTS[o2];
    [v1][o2]overlay=0:0:enable='between(t,25.5,35.0)'[vout]
  " \
  -map "[vout]" -map 0:a \
  -c:v libx264 -crf 18 -c:a aac -b:a 320k \
  output.mp4
```

### Key techniques

- **`setpts=PTS-STARTPTS`** — Resets each overlay's PTS to 0 so it plays from the start of its own file, not from the position in the base timeline
- **`enable='between(t,start,end)'`** — Time-gates the overlay filter; the overlay is composited only within this second range
- **Chained labels** — Each overlay step produces an intermediate label (`[v0]`, `[v1]`, ...) feeding into the next; the final step produces `[vout]`
- **`-map "[vout]" -map 0:a`** — Uses the composited video but keeps the original base audio stream unchanged

### Lower-third overlay at fixed position

```bash
ffmpeg -i video.mp4 -i lower-third.mov \
  -filter_complex "
    [1:v]setpts=PTS-STARTPTS[lt];
    [0:v][lt]overlay=0:810:enable='between(t,3,8)'[vout]
  " \
  -map "[vout]" -map 0:a \
  -c:v libx264 -crf 20 -c:a aac output.mp4
```

### Picture-in-picture with time window

```bash
ffmpeg -i main.mp4 -i pip.mp4 \
  -filter_complex "
    [1:v]scale=320:180,setpts=PTS-STARTPTS[pip];
    [0:v][pip]overlay=W-w-20:H-h-20:enable='between(t,10,30)'[vout]
  " \
  -map "[vout]" -map 0:a \
  -c:v libx264 -crf 20 output.mp4
```

### Dynamic overlay opacity

```bash
# Fade overlay in over 1 second (alpha blend requires yuva pixel format or separate approach)
ffmpeg -i video.mp4 -i overlay.mov \
  -filter_complex "
    [1:v]setpts=PTS-STARTPTS,format=yuva420p,
         colorchannelmixer=aa=0.8[ov];
    [0:v][ov]overlay=0:0:enable='between(t,5,15)'[vout]
  " \
  -map "[vout]" -map 0:a -c:v libx264 output.mp4
```

---

## Batch Processing at Scale

### Basic for loop

```bash
# Process all .mp4 files in a directory
for f in *.mp4; do
  ffmpeg -i "$f" -c:v libx264 -crf 23 -c:a aac "processed_${f}"
done
```

### GNU parallel (parallel execution)

```bash
# Install: brew install parallel / apt install parallel

# Convert all MOV to MP4 using all CPU cores
ls *.mov | parallel 'ffmpeg -i {} -c:v libx264 -c:a aac -preset fast {.}.mp4'

# Resize all videos with 4 parallel jobs
ls *.mp4 | parallel -j4 'ffmpeg -i {} -vf "scale=1920:1080" -c:a copy resized_{}'

# Generate thumbnails in parallel
ls *.mp4 | parallel 'ffmpeg -i {} -ss 00:00:05 -vframes 1 thumb_{.}.jpg'
```

### Queue management with a job file

```bash
# jobs.txt — one ffmpeg command per line
# Run with controlled concurrency
cat jobs.txt | parallel -j2 bash -c '{}'
```

### Batch with logging and error handling

```bash
#!/usr/bin/env bash
INPUT_DIR="./input"
OUTPUT_DIR="./output"
LOG_FILE="batch.log"

mkdir -p "$OUTPUT_DIR"

for f in "$INPUT_DIR"/*.mp4; do
  name=$(basename "$f" .mp4)
  out="$OUTPUT_DIR/${name}_processed.mp4"

  echo "[$(date '+%H:%M:%S')] Processing: $name" | tee -a "$LOG_FILE"

  if ffmpeg -y -i "$f" -c:v libx264 -crf 23 -c:a aac "$out" 2>>"$LOG_FILE"; then
    echo "[OK] $name" | tee -a "$LOG_FILE"
  else
    echo "[FAIL] $name" | tee -a "$LOG_FILE"
  fi
done

echo "Done. See $LOG_FILE for details."
```

### Python queue with subprocess

```python
import subprocess
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed

def process_video(input_path: Path, output_dir: Path) -> tuple[Path, bool]:
    out = output_dir / f"processed_{input_path.name}"
    result = subprocess.run(
        ["ffmpeg", "-y", "-i", str(input_path),
         "-c:v", "libx264", "-crf", "23", "-c:a", "aac", str(out)],
        capture_output=True,
    )
    return input_path, result.returncode == 0

input_files = list(Path("./input").glob("*.mp4"))
output_dir = Path("./output")
output_dir.mkdir(exist_ok=True)

with ThreadPoolExecutor(max_workers=4) as executor:
    futures = {executor.submit(process_video, f, output_dir): f for f in input_files}
    for future in as_completed(futures):
        path, success = future.result()
        print(f"{'OK' if success else 'FAIL'}: {path.name}")
```

---

## Transcript-Based Editing

Use whisper output to make edit decisions based on speech content rather than manual timecodes.

### Generate word-level transcript

```bash
pip install faster-whisper

python3 - video.mp4 > transcript.json <<'EOF'
import json, sys, subprocess
from faster_whisper import WhisperModel

# Extract audio first
audio = sys.argv[1].replace(".mp4", "_audio.wav")
subprocess.run(["ffmpeg", "-y", "-i", sys.argv[1], "-ar", "16000", "-ac", "1", "-vn", audio], check=True)

model = WhisperModel("medium", device="cpu", compute_type="int8")
segments, info = model.transcribe(audio, beam_size=5, word_timestamps=True, vad_filter=True)

result = {"language": info.language, "segments": []}
for seg in segments:
    result["segments"].append({
        "id": seg.id, "start": round(seg.start, 3), "end": round(seg.end, 3),
        "text": seg.text.strip(),
        "words": [{"word": w.word.strip(), "start": round(w.start, 3), "end": round(w.end, 3)} for w in seg.words],
    })
print(json.dumps(result, indent=2))
EOF
```

### Cut at specific phrase

```python
import json, subprocess

with open("transcript.json") as f:
    data = json.load(f)

# Find timestamp of a phrase
target = "let's get started"
for seg in data["segments"]:
    if target.lower() in seg["text"].lower():
        cut_time = seg["start"]
        print(f"Found '{target}' at {cut_time:.3f}s")
        # Trim video to start at this phrase
        subprocess.run([
            "ffmpeg", "-y", "-i", "video.mp4",
            "-ss", str(cut_time), "-c", "copy", "trimmed.mp4"
        ], check=True)
        break
```

### Remove filler words (cut segments around "um", "uh")

```python
import json, subprocess

with open("transcript.json") as f:
    data = json.load(f)

FILLERS = {"um", "uh", "hmm", "like", "you know"}
keep_segments = []
cursor = 0.0

all_words = [w for seg in data["segments"] for w in seg["words"]]

for i, word in enumerate(all_words):
    if word["word"].lower().strip(".,!?") in FILLERS:
        # End previous segment just before this word
        if word["start"] > cursor + 0.1:
            keep_segments.append((cursor, word["start"]))
        cursor = word["end"]

# Add final segment
total = data["segments"][-1]["end"]
if cursor < total:
    keep_segments.append((cursor, total))

# Extract and reassemble
concat_lines = []
for i, (start, end) in enumerate(keep_segments):
    tmp = f"_seg_{i:04d}.ts"
    subprocess.run([
        "ffmpeg", "-y", "-i", "video.mp4",
        "-ss", f"{start:.3f}", "-to", f"{end:.3f}",
        "-c", "copy", "-avoid_negative_ts", "make_zero", tmp
    ], check=True)
    concat_lines.append(f"file '{tmp}'")

with open("_concat.txt", "w") as f:
    f.write("\n".join(concat_lines))

subprocess.run(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", "_concat.txt", "-c", "copy", "no_fillers.mp4"], check=True)
```

### Auto-generate chapter markers from transcript

```python
import json

with open("transcript.json") as f:
    data = json.load(f)

# Find sentences that could be chapter starts (heuristic: start of segment after pause)
chapters = []
for i, seg in enumerate(data["segments"]):
    if i == 0:
        chapters.append((0.0, "Introduction"))
        continue
    prev = data["segments"][i - 1]
    gap = seg["start"] - prev["end"]
    if gap > 2.0:  # 2+ second pause = likely chapter boundary
        chapters.append((seg["start"], seg["text"][:50]))

# Output as ffmetadata for embedding
print(";FFMETADATA1")
for i, (start, title) in enumerate(chapters):
    end = chapters[i + 1][0] if i + 1 < len(chapters) else data["segments"][-1]["end"]
    print(f"\n[CHAPTER]\nTIMEBASE=1/1000\nSTART={int(start*1000)}\nEND={int(end*1000)}\ntitle={title}")
```

### Embed chapters into MP4

```bash
python3 generate_chapters.py > chapters.txt
ffmpeg -i video.mp4 -i chapters.txt -map_metadata 1 -codec copy video_with_chapters.mp4
```
