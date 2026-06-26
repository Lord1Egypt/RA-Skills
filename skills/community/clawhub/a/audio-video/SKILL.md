---
name: audio-video
description: "Expert audio/video processing with ffmpeg and ffprobe. Use when the user needs to convert, compress, edit, analyze, stream, or process any audio or video file. Triggers on: transcode, convert video, compress video, extract audio, trim clip, merge files, add subtitles, change bitrate, generate thumbnail, probe media, HLS stream, audio normalization, video filter, codec, fps, resolution, aspect ratio, waveform, spectrogram, ffmpeg, ffprobe, stabilize video, video stabilization, shaky footage, 360 video, VR video, equirectangular, cubemap, v360, HDR, tone mapping, HDR to SDR, bt2020, smpte2084, color space, SRT streaming, low latency stream, multi-destination stream, tee muxer, restream, DVR recording, rolling window, repair video, corrupt video, VFR to CFR, variable frame rate, fix sync, metadata, chapter markers, cover art, strip metadata, embed chapters, SMPTE bars, test signal, packet analysis, encoding benchmark."
metadata:
  tools: ffmpeg, ffprobe
  platforms: macOS, Linux, Windows
---

# Audio/Video Processing Skill

You are an expert audio/video engineer with deep mastery of **ffmpeg** and **ffprobe**. You produce correct, efficient, copy-safe shell commands with clear explanations.

This skill covers a wide range of audio/video tasks organized by sections below. To know only the features offered by this skill (without knowing the specific commands), read the [features.md](./assets/features.md) which is also organized by sections. `features.md` also mentions several use-cases for which different sections of this skill can be used.

---

## STEP 0 — Tool Availability Check (ALWAYS RUN FIRST)

Before generating any commands, verify the required tools are installed. Run or instruct the agent to run:

```bash
ffmpeg -version 2>&1 | head -1
ffprobe -version 2>&1 | head -1
```

> **Windows**: Run these in PowerShell. `head` is not available — use `ffmpeg -version` and read the first line manually, or pipe to `Select-Object -First 1`.

### If ffmpeg/ffprobe is NOT installed:

**Stop immediately** and provide platform-specific installation instructions:

#### macOS
```bash
# Option 1: Homebrew (recommended)
brew install ffmpeg

# Note: Homebrew removed --with-* option flags. The default formula includes
# the most common codecs. For a build with more codecs (libfdk-aac, etc.):
#   brew tap homebrew-ffmpeg/ffmpeg && brew install homebrew-ffmpeg/ffmpeg/ffmpeg
# See: https://formulae.brew.sh/formula/ffmpeg

# Verify
ffmpeg -version
```

#### Linux (Ubuntu/Debian)
```bash
sudo apt update && sudo apt install -y ffmpeg

# Or for latest static build:
wget https://johnvansickle.com/ffmpeg/releases/ffmpeg-release-amd64-static.tar.xz
tar xf ffmpeg-release-amd64-static.tar.xz
FFDIR=$(find . -maxdepth 1 -type d -name 'ffmpeg-*-static' | head -n1)
sudo mv "$FFDIR/ffmpeg" "$FFDIR/ffprobe" /usr/local/bin/
```

#### Linux (RHEL/Fedora/CentOS)
```bash
sudo dnf install -y ffmpeg ffmpeg-devel
# Or via RPM Fusion:
sudo dnf install -y https://download1.rpmfusion.org/free/fedora/rpmfusion-free-release-$(rpm -E %fedora).noarch.rpm
sudo dnf install -y ffmpeg
```

#### Windows
```powershell
# Option 1: winget
winget install Gyan.FFmpeg

# Option 2: Chocolatey
choco install ffmpeg

# Option 3: Scoop
scoop install ffmpeg

# Option 4: Manual — download from https://www.gyan.dev/ffmpeg/builds/
# Extract and add to PATH
```

#### Docker (any platform)
```bash
# macOS / Linux
docker run --rm -v "$(pwd):/work" -w /work jrottenberg/ffmpeg:latest \
  -i input.mp4 output.mp4

# Windows PowerShell
docker run --rm -v "${PWD}:/work" -w /work jrottenberg/ffmpeg:latest `
  -i input.mp4 output.mp4
```

> **Do not proceed with any other steps until ffmpeg is confirmed installed.**

---

## STEP 1 — Media Analysis (Always Probe Before Processing)

Always inspect input files before building commands. Load `references/ffprobe-analysis.md` for full probe patterns.

### Quick probe
```bash
# Full JSON output — machine-readable, use for scripting
ffprobe -v quiet -print_format json -show_format -show_streams "input.mp4"

# Human-readable summary
ffprobe -v error -show_entries format=filename,duration,size,bit_rate \
  -show_entries stream=index,codec_name,codec_type,width,height,r_frame_rate,bit_rate,sample_rate,channels \
  -of default=noprint_wrappers=1 "input.mp4"

# Human-readable full metadata summary
ffprobe -v quiet -print_format json -show_format -show_streams "input.mp4" | python3 -m json.tool
```

### Key facts to extract before any operation:
- **Video**: codec, resolution (WxH), fps, bitrate, pixel format, color space
- **Audio**: codec, sample rate, channels, bitrate, layout (stereo/5.1/etc.)
- **Container**: format, duration, total size, nb_streams
- **Subtitles/attachments**: subtitle streams, embedded fonts

---

## STEP 2 — Command Construction Rules

Load `references/ffmpeg-flags.md` for the complete flag reference.

### Universal Safety Rules

1. **Never overwrite without explicit `-y` flag** — use `-n` to skip existing files by default
2. **Always specify `-map` for multi-stream operations** — prevents silent stream loss
3. **Prefer `-c copy` (stream copy) when no re-encoding is needed** — faster, lossless
4. **Use `-crf` for quality-based encoding, `-b:v` for bitrate-based** — never both together
5. **Validate output**: run `ffprobe` on output to confirm expected streams
6. **Use `-progress pipe:1`** for scriptable progress tracking
7. **Set `-loglevel warning`** in production scripts to suppress info spam
8. **Always use `-movflags +faststart`** for web MP4s (moves moov atom to front)
9. **Quote all file paths** — spaces and special characters will break commands
10. **Use `-ss` before `-i` for fast seek** (keyframe seek), after `-i` for accurate seek

### Command Template
```bash
ffmpeg \
  [global options] \
  [input options] -i "input_file" \
  [output options] \
  "output_file"
```

---

## SECTION A — Format Conversion & Transcoding

Load `references/codecs-containers.md` for codec compatibility matrix.

### A1. Video Transcoding

#### MP4 → High-quality H.264 (universal compatibility)
```bash
ffmpeg -i "input.mov" \
  -c:v libx264 -crf 23 -preset slow \
  -c:a aac -b:a 192k \
  -movflags +faststart \
  "output.mp4"
```
> `crf 18-28`: lower = better quality/larger file. `preset`: ultrafast→veryslow (speed vs compression).

#### H.265/HEVC (better compression, modern devices)
```bash
ffmpeg -i "input.mp4" \
  -c:v libx265 -crf 28 -preset slow \
  -c:a aac -b:a 128k \
  -tag:v hvc1 \
  "output_h265.mp4"
```
> `-tag:v hvc1` required for Apple device compatibility.

#### AV1 (best compression, slowest encode)
```bash
ffmpeg -i "input.mp4" \
  -c:v libaom-av1 -crf 30 -b:v 0 \
  -strict experimental \
  -c:a libopus -b:a 128k \
  "output.webm"
```

#### VP9 / WebM (web-optimized, royalty-free)
```bash
ffmpeg -i "input.mp4" \
  -c:v libvpx-vp9 -crf 30 -b:v 0 \
  -c:a libopus -b:a 128k \
  "output.webm"
```

#### Hardware-accelerated encoding (macOS VideoToolbox)
```bash
ffmpeg -i "input.mp4" \
  -c:v h264_videotoolbox -b:v 5M \
  -c:a aac -b:a 192k \
  "output_fast.mp4"
```

#### Hardware-accelerated encoding (NVIDIA NVENC)
```bash
ffmpeg -i "input.mp4" \
  -c:v h264_nvenc -preset p6 -cq 23 \
  -c:a aac -b:a 192k \
  "output_nvenc.mp4"
```

#### Hardware-accelerated encoding (Intel QSV)
```bash
ffmpeg -i "input.mp4" \
  -c:v h264_qsv -global_quality 23 \
  -c:a aac -b:a 192k \
  "output_qsv.mp4"
```

### A2. Container Remuxing (No Re-encoding)
```bash
# MP4 → MKV (stream copy, instant)
ffmpeg -i "input.mp4" -c copy "output.mkv"

# MKV → MP4 (stream copy, may fail if codec incompatible)
ffmpeg -i "input.mkv" -c copy -movflags +faststart "output.mp4"

# MOV → MP4
ffmpeg -i "input.mov" -c copy -movflags +faststart "output.mp4"
```

### A3. Image Sequence → Video
```bash
# PNG sequence at 24fps
ffmpeg -framerate 24 -i "frame_%04d.png" \
  -c:v libx264 -crf 18 -pix_fmt yuv420p \
  "output.mp4"

# With audio
ffmpeg -framerate 24 -i "frame_%04d.png" -i "audio.wav" \
  -c:v libx264 -crf 18 -pix_fmt yuv420p \
  -c:a aac -b:a 192k \
  -shortest "output.mp4"
```

### A4. Video → Image Sequence
```bash
# Extract all frames
ffmpeg -i "input.mp4" "frames/frame_%04d.png"

# Extract at specific fps (1 frame per second)
ffmpeg -i "input.mp4" -vf fps=1 "frames/frame_%04d.jpg"

# Extract keyframes only
# Note: -vsync vfr is deprecated since ffmpeg 5.1; use -fps_mode vfr on newer builds
ffmpeg -i "input.mp4" -vf "select=eq(pict_type\,I)" -fps_mode vfr "keyframe_%04d.jpg"
```

---

## SECTION B — Audio Processing


### B1. Audio Extraction
```bash
# Extract audio as AAC (from MP4, keep original codec quality)
ffmpeg -i "input.mp4" -c:a copy -vn "audio.aac"

# Extract as MP3
ffmpeg -i "input.mp4" -c:a libmp3lame -q:a 2 -vn "audio.mp3"

# Extract as FLAC (lossless)
ffmpeg -i "input.mp4" -c:a flac -vn "audio.flac"

# Extract as WAV (PCM, uncompressed)
ffmpeg -i "input.mp4" -c:a pcm_s16le -vn "audio.wav"

# Extract as Opus (best quality/size ratio)
ffmpeg -i "input.mp4" -c:a libopus -b:a 128k -vn "audio.opus"
```

### B2. Audio Conversion
```bash
# MP3 → WAV
ffmpeg -i "input.mp3" "output.wav"

# WAV → AAC (for iOS/web)
ffmpeg -i "input.wav" -c:a aac -b:a 256k "output.m4a"

# Multi-channel → stereo downmix
ffmpeg -i "input_surround.ac3" -ac 2 "output_stereo.mp3"

# Sample rate conversion
ffmpeg -i "input_48k.wav" -ar 44100 "output_44k.wav"
```

### B3. Audio Normalization (EBU R128 Loudness)
```bash
# Two-pass loudnorm (broadcast standard, recommended)
# Pass 1: Measure
ffmpeg -i "input.mp3" \
  -af loudnorm=I=-23:TP=-1.5:LRA=11:print_format=json \
  -f null - 2>&1 | tail -n 20
# Note: tail -n 20 is required (not tail -20); tail is not available on Windows (use PowerShell: ... | Select-Object -Last 20)

# Pass 2: Apply measured values (replace measured_* with Pass 1 output)
ffmpeg -i "input.mp3" \
  -af "loudnorm=I=-23:TP=-1.5:LRA=11:measured_I=-18.2:measured_TP=-0.5:measured_LRA=8.3:measured_thresh=-28.5:offset=0.5:linear=true" \
  "output_normalized.mp3"
```

### B4. Audio Filters
```bash
# Volume adjustment (+6dB)
ffmpeg -i "input.mp3" -af "volume=6dB" "output_louder.mp3"

# High-pass filter (remove low rumble below 80Hz)
ffmpeg -i "input.mp3" -af "highpass=f=80" "output.mp3"

# Low-pass filter (remove high frequencies above 8kHz)
ffmpeg -i "input.mp3" -af "lowpass=f=8000" "output.mp3"

# Noise reduction (non-local means denoising)
ffmpeg -i "input.wav" -af "anlmdn=s=7:p=0.002:r=0.002:m=15" "output.wav"

# Dynamic range compression
ffmpeg -i "input.mp3" \
  -af "acompressor=threshold=-20dB:ratio=4:attack=5:release=50:makeup=2dB" \
  "output_compressed.mp3"

# Stereo to mono
ffmpeg -i "input_stereo.mp3" -ac 1 "output_mono.mp3"

# Audio fade in/out
ffmpeg -i "input.mp3" \
  -af "afade=t=in:st=0:d=3,afade=t=out:st=57:d=3" \
  "output_faded.mp3"
```

### B5. Advanced Audio Processing
```bash
# Trim silence (remove leading/trailing silence)
ffmpeg -i "input.wav" -af "silenceremove=start_periods=1:start_silence=0.1:start_threshold=0.01:stop_periods=-1:stop_silence=0.1:stop_threshold=0.01" "output.wav"

# Speed change (pitch preserved using atempo, supports 0.5–2.0 range)
ffmpeg -i "input.wav" -af "atempo=1.5" "output.wav"

# Pitch shift (without tempo change, shift up by 2 semitones)
ffmpeg -i "input.wav" -af "asetrate=44100*1.122,aresample=44100,atempo=0.891" "output.wav"

# Generate waveform data (stats/loudness info)
ffprobe -v quiet -of json -show_streams "input.wav"
ffmpeg -i "input.wav" -af "astats" -f null - 2>&1

# Generate spectrogram PNG
ffmpeg -i "input.wav" -lavfi "showspectrumpic=s=1024x512:mode=combined" -update 1 "spectrogram.png"
```

---

## SECTION C — Video Editing


### C1. Trimming & Cutting
```bash
# Fast trim (keyframe-accurate, stream copy — may be slightly imprecise at start)
ffmpeg -ss 00:01:30 -to 00:03:00 -i "input.mp4" -c copy "clip.mp4"

# Frame-accurate trim (re-encodes, precise)
ffmpeg -i "input.mp4" -ss 00:01:30 -to 00:03:00 \
  -c:v libx264 -crf 23 -c:a aac \
  "clip_accurate.mp4"

# Cut by duration
ffmpeg -ss 00:01:30 -t 90 -i "input.mp4" -c copy "clip_90s.mp4"

# Remove a section (e.g., remove 00:10 to 00:20)
ffmpeg -i "input.mp4" \
  -vf "select='not(between(t,10,20))',setpts=N/FRAME_RATE/TB" \
  -af "aselect='not(between(t,10,20))',asetpts=N/SR/TB" \
  "output_removed_section.mp4"
```

### C2. Concatenation
```bash
# Concat same-codec files (no re-encode, fastest)
# Create filelist.txt:
printf "file '%s'\n" *.mp4 > filelist.txt
# Or manually:
cat > filelist.txt << 'EOF'
file 'part1.mp4'
file 'part2.mp4'
file 'part3.mp4'
EOF

ffmpeg -f concat -safe 0 -i filelist.txt -c copy "output.mp4"

# Concat with re-encode (different codecs/resolutions)
ffmpeg -i "part1.mp4" -i "part2.mp4" \
  -filter_complex "[0:v][0:a][1:v][1:a]concat=n=2:v=1:a=1[v][a]" \
  -map "[v]" -map "[a]" \
  -c:v libx264 -crf 23 -c:a aac \
  "output.mp4"
```

### C3. Scaling & Resolution
```bash
# Scale to 1920x1080, maintain aspect ratio (pad with black)
ffmpeg -i "input.mp4" \
  -vf "scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2" \
  -c:v libx264 -crf 23 -c:a copy \
  "output_1080p.mp4"

# Scale to width 1280, auto height (preserve aspect ratio)
ffmpeg -i "input.mp4" -vf "scale=1280:-2" -c:v libx264 -crf 23 "output.mp4"

# Scale to 50% of original
ffmpeg -i "input.mp4" -vf "scale=iw/2:ih/2" "output_half.mp4"

# Scale for specific platform targets
# 4K UHD
ffmpeg -i "input.mp4" -vf "scale=3840:2160:flags=lanczos" -c:v libx265 -crf 28 "output_4k.mp4"
# 720p
ffmpeg -i "input.mp4" -vf "scale=-2:720" -c:v libx264 -crf 23 "output_720p.mp4"
# 480p
ffmpeg -i "input.mp4" -vf "scale=-2:480" -c:v libx264 -crf 23 "output_480p.mp4"
```

### C4. Frame Rate Conversion
```bash
# Change to 30fps (duplicate/drop frames)
ffmpeg -i "input.mp4" -vf fps=30 -c:v libx264 -crf 23 "output_30fps.mp4"

# Smooth slow-motion via frame interpolation (minterpolate)
ffmpeg -i "input.mp4" \
  -vf "minterpolate=fps=60:mi_mode=mci:mc_mode=aobmc:me_mode=bidir:vsbmc=1" \
  -c:v libx264 -crf 23 \
  "output_60fps_smooth.mp4"
```

### C5. Rotation & Flipping
```bash
# Rotate 90° clockwise
ffmpeg -i "input.mp4" -vf "transpose=1" -c:a copy "output_rotated.mp4"
# transpose: 0=90°CCW+vflip, 1=90°CW, 2=90°CCW, 3=90°CW+vflip

# Rotate 180° (faster alternative: vflip,hflip — same result without two transpose passes)
ffmpeg -i "input.mp4" -vf "vflip,hflip" -c:a copy "output_180.mp4"

# Flip horizontal (mirror)
ffmpeg -i "input.mp4" -vf hflip -c:a copy "output_mirrored.mp4"

# Flip vertical
ffmpeg -i "input.mp4" -vf vflip -c:a copy "output_vflip.mp4"

# Auto-rotate from metadata (fix phone videos)
# ffmpeg enables autorotate by default when re-encoding — simply re-encode without -noautorotate
# Setting rotate=0 in metadata only clears the flag; it does NOT physically rotate the video
ffmpeg -i "input.mp4" -c:v libx264 -crf 23 -c:a copy \
  "output_autorotate.mp4"
```

### C6. Cropping
```bash
# Crop to 1280x720 starting at (100,50)
ffmpeg -i "input.mp4" -vf "crop=1280:720:100:50" -c:a copy "output_cropped.mp4"

# Crop center 1:1 square
ffmpeg -i "input.mp4" \
  -vf "crop=min(iw\,ih):min(iw\,ih):(iw-min(iw\,ih))/2:(ih-min(iw\,ih))/2" \
  -c:a copy "output_square.mp4"

# Auto-detect and remove black bars
# Note: grep is not available on Windows — use: ffmpeg ... 2>&1 | Select-String crop  (PowerShell)
ffmpeg -i "input.mp4" -vf "cropdetect=24:16:0" -f null - 2>&1 | grep crop
# Then apply the detected crop value:
ffmpeg -i "input.mp4" -vf "crop=1920:800:0:140" -c:a copy "output_cropped.mp4"
```

### C7. Overlays & Watermarks
```bash
# Add image watermark (bottom-right, 10px margin)
ffmpeg -i "input.mp4" -i "watermark.png" \
  -filter_complex "overlay=W-w-10:H-h-10" \
  -c:a copy "output_watermarked.mp4"

# Add text watermark
ffmpeg -i "input.mp4" \
  -vf "drawtext=text='© 2024 MyBrand':fontcolor=white:fontsize=24:x=10:y=10:alpha=0.8" \
  -c:a copy "output_text.mp4"

# Animated overlay with fade
ffmpeg -i "input.mp4" -i "logo.png" \
  -filter_complex "overlay=10:10:enable='between(t,2,8)'" \
  -c:a copy "output_timed_overlay.mp4"

# Picture-in-Picture (PiP)
ffmpeg -i "main.mp4" -i "pip.mp4" \
  -filter_complex "[1:v]scale=320:180[pip];[0:v][pip]overlay=W-w-10:H-h-10" \
  -c:a copy "output_pip.mp4"
```

### C8. Color Correction & Grading
```bash
# Brightness, contrast, saturation
ffmpeg -i "input.mp4" \
  -vf "eq=brightness=0.06:contrast=1.2:saturation=1.5:gamma=1.0" \
  -c:a copy "output_color.mp4"

# LUT (Look-Up Table) color grading
ffmpeg -i "input.mp4" \
  -vf "lut3d=file='film_emulation.cube'" \
  -c:a copy "output_graded.mp4"

# Curves adjustment (S-curve for punch)
ffmpeg -i "input.mp4" \
  -vf "curves=r='0/0 0.5/0.6 1/1':g='0/0 0.5/0.52 1/1':b='0/0 0.5/0.44 1/1'" \
  -c:a copy "output_curves.mp4"

# Hue/saturation shift
ffmpeg -i "input.mp4" \
  -vf "hue=h=30:s=1.2" \
  -c:a copy "output_hue.mp4"
```

---

## SECTION D — Subtitles & Captions


### D1. Subtitle Operations
```bash
# Burn subtitles into video (hard subtitles)
ffmpeg -i "input.mp4" -vf "subtitles=subs.srt" -c:a copy "output_burned.mp4"

# Add SRT as soft subtitle track (selectable, not burned)
ffmpeg -i "input.mp4" -i "subs.srt" \
  -c copy -c:s mov_text \
  -metadata:s:s:0 language=eng \
  "output_soft_subs.mp4"

# Add ASS/SSA subtitles to MKV
ffmpeg -i "input.mkv" -i "subs.ass" \
  -c copy -c:s copy \
  "output.mkv"

# Extract subtitle track
ffmpeg -i "input.mkv" -map 0:s:0 "subtitles.srt"

# Convert SRT → ASS
ffmpeg -i "subs.srt" "subs.ass"
```

---

## SECTION E — Thumbnails & Screenshots

### E1. Thumbnail Generation
```bash
# Single thumbnail at specific timestamp
ffmpeg -i "input.mp4" -ss 00:00:05 -vframes 1 "thumbnail.jpg"

# High-quality thumbnail (PNG)
ffmpeg -i "input.mp4" -ss 00:00:05 -vframes 1 -q:v 2 "thumbnail.png"

# Thumbnail at best frame (highest quality scene)
ffmpeg -i "input.mp4" -vf "thumbnail,scale=640:-1" -vframes 1 "best_thumb.jpg"

# Sprite sheet / contact sheet (multiple thumbnails in a grid)
ffmpeg -i "input.mp4" \
  -vf "fps=1/10,scale=160:90,tile=10x10" \
  -vframes 1 \
  "sprite_sheet.jpg"

# Thumbnail every 10 seconds
ffmpeg -i "input.mp4" -vf "fps=1/10,scale=320:-1" "thumbs/thumb_%04d.jpg"
```

---

## SECTION F — Streaming & Adaptive Bitrate


### F1. HLS (HTTP Live Streaming)
```bash
# Generate HLS segments with master playlist
ffmpeg -i "input.mp4" \
  -c:v libx264 -crf 23 -preset fast \
  -c:a aac -b:a 128k \
  -hls_time 6 \
  -hls_playlist_type vod \
  -hls_segment_filename "hls/segment_%03d.ts" \
  "hls/playlist.m3u8"

# Multi-bitrate HLS (ABR ladder)
ffmpeg -i "input.mp4" \
  -filter_complex \
    "[0:v]split=3[v1][v2][v3]; \
     [v1]scale=-2:1080[v1out]; \
     [v2]scale=-2:720[v2out]; \
     [v3]scale=-2:480[v3out]" \
  -map "[v1out]" -c:v:0 libx264 -b:v:0 5000k \
  -map "[v2out]" -c:v:1 libx264 -b:v:1 2800k \
  -map "[v3out]" -c:v:2 libx264 -b:v:2 1400k \
  -map 0:a -c:a aac -b:a 128k \
  -var_stream_map "v:0,a:0 v:1,a:1 v:2,a:2" \
  -master_pl_name "master.m3u8" \
  -hls_time 6 -hls_list_size 0 \
  -hls_segment_filename "hls/%v/segment_%03d.ts" \
  "hls/%v/playlist.m3u8"
```

### F2. DASH (Dynamic Adaptive Streaming over HTTP)
```bash
ffmpeg -i "input.mp4" \
  -c:v libx264 -crf 23 -preset fast \
  -c:a aac -b:a 128k \
  -f dash \
  -seg_duration 4 \
  -use_template 1 \
  -use_timeline 1 \
  "dash/manifest.mpd"
```

### F3. RTMP Live Streaming
```bash
# Stream to RTMP endpoint (YouTube, Twitch, etc.)
ffmpeg -re -i "input.mp4" \
  -c:v libx264 -preset veryfast -b:v 4500k -maxrate 4500k -bufsize 9000k \
  -pix_fmt yuv420p -g 60 \
  -c:a aac -b:a 160k -ar 44100 \
  -f flv "rtmp://live.twitch.tv/app/YOUR_STREAM_KEY"

# Screen capture + stream (macOS)
ffmpeg \
  -f avfoundation -framerate 30 -i "1:0" \
  -c:v libx264 -preset veryfast -b:v 4500k \
  -c:a aac -b:a 160k \
  -f flv "rtmp://YOUR_RTMP_ENDPOINT"
```

---

## SECTION G — Screen & Webcam Capture

### G1. Screen Recording
```bash
# macOS (AVFoundation) — list devices first
ffmpeg -f avfoundation -list_devices true -i ""

# Record screen (device 1) with audio (device 0)
ffmpeg -f avfoundation -framerate 30 -i "1:0" \
  -c:v libx264 -preset ultrafast -crf 18 \
  -c:a aac -b:a 192k \
  "screen_recording.mp4"

# Linux (x11grab + PulseAudio)
ffmpeg -f x11grab -r 30 -s 1920x1080 -i :0.0+0,0 \
  -f pulse -ac 2 -i default \
  -c:v libx264 -preset ultrafast -crf 18 \
  "screen_recording.mp4"
# Note: -f pulse is PulseAudio. On modern Linux (Ubuntu 22.04+, PipeWire):
# replace -f pulse -i default  with  -f pipewire -i default
# or use pactl to find the correct PipeWire source name

# Windows (gdigrab)
ffmpeg -f gdigrab -framerate 30 -i desktop \
  -c:v libx264 -preset ultrafast -crf 18 \
  "screen_recording.mp4"
```

### G2. Webcam Capture
```bash
# macOS
ffmpeg -f avfoundation -framerate 30 -video_size 1280x720 -i "0" \
  -c:v libx264 -crf 23 "webcam.mp4"

# Linux (v4l2)
ffmpeg -f v4l2 -framerate 30 -video_size 1280x720 -i /dev/video0 \
  -c:v libx264 -crf 23 "webcam.mp4"

# Windows (dshow)
ffmpeg -f dshow -i video="Integrated Camera" \
  -c:v libx264 -crf 23 "webcam.mp4"
```

---

## SECTION H — GIF & Animated Images

### H1. Video → GIF (High Quality)
```bash
# Two-pass high-quality GIF (palette generation)
# Pass 1: Generate optimal palette
ffmpeg -i "input.mp4" \
  -vf "fps=15,scale=480:-1:flags=lanczos,palettegen=stats_mode=diff" \
  -y "palette.png"

# Pass 2: Apply palette
ffmpeg -i "input.mp4" -i "palette.png" \
  -filter_complex "fps=15,scale=480:-1:flags=lanczos[x];[x][1:v]paletteuse=dither=bayer:bayer_scale=5:diff_mode=rectangle" \
  -y "output.gif"
```

### H2. GIF → Video
```bash
ffmpeg -i "input.gif" -c:v libx264 -pix_fmt yuv420p -movflags +faststart "output.mp4"
```

### H3. WebP Animation
```bash
ffmpeg -i "input.mp4" -vf "fps=24,scale=480:-1:flags=lanczos" \
  -loop 0 -preset default -an -fps_mode passthrough \
  "output.webp"
# Note: -vsync 0 is deprecated since ffmpeg 5.1; use -fps_mode passthrough
```

---

## SECTION I — Batch Processing & Scripting

### I1. Batch Convert (Shell)
```bash
# Convert all .mov files to .mp4 (bash/zsh — macOS/Linux only)
for f in *.mov; do
  ffmpeg -i "$f" \
    -c:v libx264 -crf 23 -preset slow \
    -c:a aac -b:a 192k \
    -movflags +faststart \
    "${f%.mov}.mp4" \
    && echo "Done: $f" || echo "FAILED: $f"
done

# Windows PowerShell equivalent:
# Get-ChildItem *.mov | ForEach-Object {
#   ffmpeg -i $_.FullName -c:v libx264 -crf 23 -preset slow -c:a aac -b:a 192k -movflags +faststart "$($_.BaseName).mp4"
# }

# Parallel batch (GNU parallel, 4 jobs) — avoids issues with spaces in filenames
printf '%s\n' *.mov | parallel -j4 'ffmpeg -i {} -c:v libx264 -crf 23 {.}.mp4'
```

### I2. Progress Monitoring
```bash
# Machine-readable progress output
ffmpeg -i "input.mp4" \
  -c:v libx264 -crf 23 \
  -progress pipe:1 -nostats \
  "output.mp4" 2>/dev/null
# Note: 2>/dev/null suppresses stderr on macOS/Linux. On Windows use: 2>NUL

# Duration-aware progress percentage (bash/zsh — macOS/Linux)
DURATION=$(ffprobe -v error -show_entries format=duration \
  -of default=noprint_wrappers=1:nokey=1 "input.mp4")
ffmpeg -i "input.mp4" -c:v libx264 -crf 23 \
  -progress pipe:1 "output.mp4" 2>/dev/null | \
  python3 -c "
import sys, re
dur = float('$DURATION')
for line in sys.stdin:
    m = re.match(r'out_time_ms=(\d+)', line)
    if m:
        print(f'\r{int(m.group(1))/1000000/dur*100:.1f}%', end='', flush=True)
"
```

### I3. Two-Pass Encoding (Precise Bitrate Control)
```bash
# Pass 1 (analysis only)
ffmpeg -y -i "input.mp4" \
  -c:v libx264 -b:v 2M -pass 1 -an -f null -

# Pass 2 (encode with target bitrate)
ffmpeg -i "input.mp4" \
  -c:v libx264 -b:v 2M -pass 2 \
  -c:a aac -b:a 192k \
  "output_2pass.mp4"
```

---

## SECTION J — Advanced Filtergraphs

### J1. Complex Filter Examples
```bash
# Side-by-side video comparison
ffmpeg -i "original.mp4" -i "processed.mp4" \
  -filter_complex "[0:v][1:v]hstack=inputs=2[v]" \
  -map "[v]" -c:v libx264 -crf 23 \
  "comparison.mp4"

# Stack videos vertically
ffmpeg -i "top.mp4" -i "bottom.mp4" \
  -filter_complex "[0:v][1:v]vstack=inputs=2[v]" \
  -map "[v]" -c:v libx264 -crf 23 \
  "stacked.mp4"

# 2x2 grid layout
ffmpeg -i "v1.mp4" -i "v2.mp4" -i "v3.mp4" -i "v4.mp4" \
  -filter_complex \
    "[0:v][1:v]hstack[top]; \
     [2:v][3:v]hstack[bottom]; \
     [top][bottom]vstack[v]" \
  -map "[v]" -c:v libx264 -crf 23 \
  "grid_2x2.mp4"

# Zoom/Pan (Ken Burns effect)
ffmpeg -i "photo.jpg" -t 10 \
  -vf "zoompan=z='min(zoom+0.0015,1.5)':d=250:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)',scale=1280:720" \
  -c:v libx264 -crf 23 \
  "ken_burns.mp4"

# Vignette effect
ffmpeg -i "input.mp4" \
  -vf "vignette=PI/4:eval=frame" \
  -c:a copy "output_vignette.mp4"

# Blur (useful for privacy/background)
ffmpeg -i "input.mp4" \
  -vf "boxblur=10:1" \
  -c:a copy "output_blurred.mp4"

# Selective blur (blur a region, keep rest sharp)
ffmpeg -i "input.mp4" \
  -filter_complex \
    "[0:v]crop=200:200:100:100,boxblur=10[blurred]; \
     [0:v][blurred]overlay=100:100[v]" \
  -map "[v]" -c:a copy "output_region_blur.mp4"
```

### J2. Audio/Video Sync Repair
```bash
# Fix audio delay (audio is 500ms late)
ffmpeg -i "input.mp4" -itsoffset -0.5 -i "input.mp4" \
  -map 1:v -map 0:a -c copy "output_synced.mp4"

# Add audio delay (audio is 500ms early)
ffmpeg -i "input.mp4" -itsoffset 0.5 -i "input.mp4" \
  -map 0:v -map 1:a -c copy "output_synced.mp4"
```

---

## SECTION K — Quality Analysis & Verification

### K1. Quality Metrics
```bash
# PSNR (Peak Signal-to-Noise Ratio) — higher is better
ffmpeg -i "original.mp4" -i "compressed.mp4" \
  -lavfi psnr="stats_file=psnr.log" -f null -

# SSIM (Structural Similarity Index) — closer to 1.0 is better
ffmpeg -i "original.mp4" -i "compressed.mp4" \
  -lavfi ssim="stats_file=ssim.log" -f null -

# VMAF (Netflix perceptual quality — industry standard)
ffmpeg -i "original.mp4" -i "compressed.mp4" \
  -lavfi libvmaf="log_fmt=json:log_path=vmaf.json:n_threads=4" \
  -f null -
```

### K2. Output Validation Checklist

After every encode, verify:

```bash
# Check output is valid and playable
ffprobe -v error -show_entries \
  format=duration,size,bit_rate \
  -show_entries stream=codec_name,codec_type,width,height,r_frame_rate,bit_rate \
  -of default=noprint_wrappers=1 "output.mp4"

# Confirm stream count matches expectation
ffprobe -v error -show_entries stream=index,codec_type -of csv "output.mp4"

# Verify no corrupt packets
ffmpeg -v error -i "output.mp4" -f null - 2>&1 | head -n 20
```

---

## SECTION L — Platform-Specific Presets

### L1. Web (HTML5 video)
```bash
ffmpeg -i "input.mp4" \
  -c:v libx264 -crf 23 -preset slow \
  -c:a aac -b:a 128k \
  -pix_fmt yuv420p \
  -movflags +faststart \
  -profile:v high -level 4.0 \
  "web.mp4"
```

### L2. YouTube Upload
```bash
ffmpeg -i "input.mp4" \
  -c:v libx264 -crf 18 -preset slow \
  -c:a aac -b:a 384k -ar 48000 \
  -pix_fmt yuv420p \
  -r 29.97 \
  -movflags +faststart \
  "youtube_upload.mp4"
```

### L3. Instagram / TikTok (Vertical 9:16)
```bash
ffmpeg -i "input.mp4" \
  -vf "scale=1080:1920:force_original_aspect_ratio=decrease,pad=1080:1920:(ow-iw)/2:(oh-ih)/2:black" \
  -c:v libx264 -crf 23 -preset slow \
  -c:a aac -b:a 192k \
  -t 60 \
  "instagram_reel.mp4"
```

### L4. Apple ProRes (Post-production)
```bash
ffmpeg -i "input.mp4" \
  -c:v prores_ks -profile:v 3 \
  -c:a pcm_s16le \
  "output_prores.mov"
# Profiles: 0=Proxy, 1=LT, 2=Standard, 3=HQ, 4=4444, 5=4444XQ
```

### L5. Discord / Messaging (8MB limit)
```bash
# Calculate target bitrate for 8MB / duration
DURATION=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "input.mp4")
TARGET_KBPS=$(python3 -c "print(int(8*1024*8 / $DURATION - 128))")
ffmpeg -i "input.mp4" \
  -c:v libx264 -b:v "${TARGET_KBPS}k" -pass 1 -an -f null - && \
ffmpeg -i "input.mp4" \
  -c:v libx264 -b:v "${TARGET_KBPS}k" -pass 2 \
  -c:a aac -b:a 128k \
  "discord_clip.mp4"
```

---

## SECTION M — Video Stabilization

Stabilize shaky footage from handheld cameras, drones, or action cameras. Uses a two-pass approach: pass 1 analyzes motion, pass 2 applies correction.

### Check libvidstab availability

```bash
ffmpeg -filters 2>&1 | grep vidstab
# Should show: vidstabdetect, vidstabtransform
```

**If not available:** Install a full-featured ffmpeg build.
- macOS: `brew install ffmpeg-full` or `brew install ffmpeg --with-libvidstab`
- Linux: `sudo apt install ffmpeg` (Ubuntu 20.04+ includes libvidstab)
- Windows: Download from https://www.gyan.dev/ffmpeg/builds/ (full build includes libvidstab)

### Pass 1 — Detect motion (analyze shakiness)
```bash
# shakiness: 1 (low) to 10 (high). accuracy: 1-15, higher = better but slower.
ffmpeg -i input.mp4 -vf vidstabdetect=shakiness=5:accuracy=15:result=transforms.trf -f null -
```

### Pass 2 — Apply stabilization
```bash
# smoothing: number of frames to average (higher = smoother but more crop). zoom: extra zoom to hide black borders.
ffmpeg -i input.mp4 \
  -vf "vidstabtransform=input=transforms.trf:zoom=1:smoothing=30,unsharp=5:5:0.8:3:3:0.4" \
  -c:v libx264 -crf 18 -c:a copy stabilized.mp4
```

### One-liner (both passes)
```bash
ffmpeg -i input.mp4 -vf vidstabdetect=shakiness=5:accuracy=15:result=transforms.trf -f null - && \
ffmpeg -i input.mp4 -vf "vidstabtransform=input=transforms.trf:zoom=1:smoothing=30,unsharp=5:5:0.8:3:3:0.4" \
  -c:v libx264 -crf 18 -c:a copy stabilized.mp4
```

### Windows (PowerShell)
```powershell
ffmpeg -i input.mp4 -vf vidstabdetect=shakiness=5:accuracy=15:result=transforms.trf -f null NUL
ffmpeg -i input.mp4 -vf "vidstabtransform=input=transforms.trf:zoom=1:smoothing=30,unsharp=5:5:0.8:3:3:0.4" -c:v libx264 -crf 18 -c:a copy stabilized.mp4
```

### Parameter tuning
| Goal | Settings |
|------|----------|
| Mild stabilization | `shakiness=3:smoothing=10` |
| Heavy stabilization | `shakiness=8:smoothing=50:zoom=5` |
| Preserve full frame | `zoom=0` (black borders may appear) |
| Action cam footage | `shakiness=10:accuracy=15:smoothing=30:zoom=2` |

---

## SECTION N — 360° / VR Video

Handle 360° footage from cameras like GoPro Max, Insta360, Ricoh Theta. Convert between projections and inject spherical metadata so platforms (YouTube VR, Facebook 360) recognize the video correctly.

### Check v360 filter availability
```bash
ffmpeg -filters 2>&1 | grep v360
```

### Convert equirectangular → cubemap (3x2 layout)
```bash
# Input must be 2:1 aspect ratio (e.g. 3840x1920)
ffmpeg -i input_360.mp4 -vf "v360=equirect:c3x2" -c:v libx264 -crf 18 -c:a copy cubemap.mp4
```

### Convert cubemap → equirectangular
```bash
ffmpeg -i cubemap.mp4 -vf "v360=c3x2:equirect" -c:v libx264 -crf 18 -c:a copy equirect.mp4
```

### Inject spherical metadata (YouTube VR / Facebook 360)
```bash
# Inject metadata so platforms recognize as 360° video
ffmpeg -i input_360.mp4 -c copy \
  -metadata:s:v:0 spherical-video=equirectangular \
  output_360.mp4
```

> **Note:** For full YouTube VR compliance, use Google's [spatial-media tool](https://github.com/google/spatial-media) after encoding to inject the proper XMP metadata atom. FFmpeg metadata injection is a best-effort fallback.

### Reframe / extract a flat view from 360° video
```bash
# Extract a flat 1920x1080 view from equirectangular (yaw=0, pitch=0, fov=90)
ffmpeg -i input_360.mp4 \
  -vf "v360=equirect:flat:yaw=0:pitch=0:roll=0:h_fov=90:v_fov=90:w=1920:h=1080" \
  -c:v libx264 -crf 18 -c:a copy flat_view.mp4
```

### macOS / Linux / Windows
The `v360` filter works identically on all platforms — no platform-specific flags needed.

---

## SECTION O — HDR / Color Science

Handle HDR10 content from modern phones (iPhone, Android) and cameras. Convert HDR to SDR for web delivery, or tag files with correct color metadata.

### Check color filters availability
```bash
ffmpeg -filters 2>&1 | grep -E "zscale|colorspace|tonemap"
```

> **If zscale is missing:** Install with `--enable-libzimg`. macOS: `brew install ffmpeg-full`. Linux: `sudo apt install ffmpeg` (20.04+). Windows: use full build from gyan.dev.

### HDR10 → SDR tone mapping (real HDR source required)
```bash
# Use this when input is a genuine HDR10 file (bt2020/smpte2084 color space)
# Pass 1: verify input is HDR
ffprobe -v quiet -select_streams v:0 -show_entries stream=color_space,color_transfer,color_primaries -of default input.mp4

# Pass 2: tone map to SDR
ffmpeg -i input_hdr10.mp4 \
  -vf "zscale=t=linear:npl=100,format=gbrpf32le,zscale=p=bt709,tonemap=tonemap=hable:desat=0,zscale=t=bt709:m=bt709:r=tv,format=yuv420p" \
  -c:v libx264 -crf 18 -c:a copy sdr_output.mp4
```

### Colorspace conversion (SDR bt2020 → bt709)
```bash
# For files tagged bt2020 but not true HDR (common from some Android phones)
ffmpeg -i input.mp4 \
  -vf "colorspace=bt709:iall=bt2020:fast=1" \
  -c:v libx264 -crf 18 -c:a copy bt709_output.mp4
```

### Encode HDR10 output (for archival/editing)
```bash
# Encode to HDR10 with proper metadata
ffmpeg -i input.mp4 \
  -vf "format=yuv420p10le" \
  -c:v libx265 \
  -x265-params "colorprim=bt2020:transfer=smpte2084:colormatrix=bt2020nc:hdr-opt=1:repeat-headers=1:master-display=G(13250,34500)B(7500,3000)R(34000,16000)WP(15635,16450)L(10000000,1):max-cll=1000,400" \
  -c:a copy hdr10_output.mp4
```

### Tag existing file with correct color metadata (no re-encode)
```bash
ffmpeg -i input.mp4 -c copy \
  -color_primaries bt2020 \
  -color_trc smpte2084 \
  -colorspace bt2020nc \
  tagged_hdr10.mp4
```

### Tone mapping algorithm comparison
| Algorithm | Description | Best for |
|-----------|-------------|----------|
| `hable` | Filmic, preserves highlights | General use |
| `reinhard` | Simple, global | Fast previews |
| `mobius` | Smooth, natural | Skin tones |
| `clip` | Hard clip at white | Technical use |

### Windows / Linux / macOS
Commands are identical across platforms. Ensure ffmpeg is built with `--enable-libzimg`.

---

## SECTION P — Advanced Streaming

### SRT (Secure Reliable Transport) — low-latency streaming

SRT handles packet loss and network jitter, making it ideal for unstable connections (cellular, satellite, long-distance contribution).

```bash
# Check SRT support
ffmpeg -protocols 2>&1 | grep srt

# Send stream via SRT (caller mode)
ffmpeg -re -i input.mp4 -c:v libx264 -b:v 4000k -c:a aac -b:a 128k \
  -f mpegts "srt://receiver_ip:port?pkt_size=1316"

# Receive SRT stream and save
ffmpeg -i "srt://0.0.0.0:port?mode=listener" -c copy output.mp4

# SRT with latency tuning (default 120ms, increase for unreliable links)
ffmpeg -re -i input.mp4 -c:v libx264 -b:v 4000k -c:a aac \
  -f mpegts "srt://receiver_ip:port?pkt_size=1316&latency=500000"
```

> **Windows:** Same commands work in PowerShell. SRT is included in full ffmpeg builds from gyan.dev.

### Multi-endpoint restreaming (tee muxer)

Stream to YouTube, Twitch, and Facebook simultaneously from one ffmpeg process:

```bash
ffmpeg -re -i input.mp4 \
  -c:v libx264 -b:v 4500k -maxrate 4500k -bufsize 9000k \
  -c:a aac -b:a 128k -ar 44100 \
  -f tee \
  "[f=flv]rtmp://a.rtmp.youtube.com/live2/YOUR_YOUTUBE_KEY|\
[f=flv]rtmp://live.twitch.tv/app/YOUR_TWITCH_KEY|\
[f=flv]rtmps://live-api-s.facebook.com:443/rtmp/YOUR_FB_KEY"
```

### Rolling window DVR recording

Continuous loop recording — keeps only the last N segments (useful for security cameras, broadcast monitoring):

```bash
# Record in 60-second segments, keep only last 10 (10 minutes of rolling buffer)
# segment_wrap=10 means segment_000 through segment_009, then wraps back
ffmpeg -i input_stream_or_device \
  -c:v libx264 -b:v 2000k -c:a aac \
  -f segment \
  -segment_time 60 \
  -segment_wrap 10 \
  -reset_timestamps 1 \
  dvr_segment_%03d.ts

# macOS screen capture rolling DVR
ffmpeg -f avfoundation -i "1:0" \
  -c:v libx264 -b:v 2000k -c:a aac \
  -f segment -segment_time 60 -segment_wrap 10 -reset_timestamps 1 \
  dvr_%03d.ts

# Linux screen capture rolling DVR
ffmpeg -f x11grab -r 30 -i :0.0 -f pulse -i default \
  -c:v libx264 -b:v 2000k -c:a aac \
  -f segment -segment_time 60 -segment_wrap 10 -reset_timestamps 1 \
  dvr_%03d.ts

# Windows screen capture rolling DVR (PowerShell)
ffmpeg -f gdigrab -framerate 30 -i desktop -f dshow -i audio="Microphone" `
  -c:v libx264 -b:v 2000k -c:a aac `
  -f segment -segment_time 60 -segment_wrap 10 -reset_timestamps 1 `
  dvr_%03d.ts
```

---

## SECTION Q — Repair & Recovery

### Recover from corrupt or truncated files
```bash
# Attempt recovery — ignore errors and discard corrupt packets
ffmpeg -i corrupt_input.mp4 \
  -c copy \
  -err_detect ignore_err \
  -fflags +discardcorrupt \
  recovered.mp4

# Increase probe size for files with missing moov atom or bad headers
ffmpeg -analyzeduration 100M -probesize 100M \
  -i corrupt_input.mp4 -c copy recovered.mp4

# Fix files that won't open at all (try forcing container format)
ffmpeg -f mp4 -i corrupt_input.mp4 -c copy recovered.mp4
# or for MKV:
ffmpeg -f matroska -i corrupt_input.mkv -c copy recovered.mkv
```

### VFR → CFR conversion (fix audio sync drift)

Variable frame rate (VFR) footage — common from phones and screen recorders — causes audio sync drift in editing software. Convert to constant frame rate (CFR):

```bash
# Convert to CFR at 30fps (re-encodes video)
ffmpeg -i input_vfr.mp4 -vsync cfr -r 30 -c:v libx264 -crf 18 -c:a copy cfr_output.mp4

# Detect if input is VFR first
ffprobe -v quiet -select_streams v:0 \
  -show_entries stream=r_frame_rate,avg_frame_rate \
  -of default input.mp4
# If r_frame_rate != avg_frame_rate → VFR confirmed
```

### Fix audio/video sync offset
```bash
# Audio is N seconds late (positive = delay audio, negative = advance audio)
ffmpeg -i input.mp4 -itsoffset 0.5 -i input.mp4 \
  -map 0:v -map 1:a -c copy sync_fixed.mp4

# Simpler: shift audio stream only
ffmpeg -i input.mp4 -c:v copy -af "adelay=500|500" sync_fixed.mp4
# 500 = 500ms delay on both channels
```

### Rebuild broken index / moov atom
```bash
# Re-mux to fix index (fast, no quality loss)
ffmpeg -i input.mp4 -c copy -movflags +faststart fixed.mp4
```

### Windows / Linux / macOS
All recovery commands are platform-independent. On Windows PowerShell, use backtick `` ` `` for line continuation instead of `\`.

---

## SECTION R — Metadata Management

### Embed key/value metadata tags
```bash
# Add title, artist, year, comment
ffmpeg -i input.mp4 \
  -metadata title="My Video" \
  -metadata artist="Author Name" \
  -metadata year="2025" \
  -metadata comment="Description here" \
  -c copy tagged.mp4

# Audio files: embed standard ID3-style tags
ffmpeg -i input.mp3 \
  -metadata title="Song Title" \
  -metadata artist="Artist" \
  -metadata album="Album" \
  -metadata track="1" \
  -c copy tagged.mp3
```

### Strip all metadata (privacy)
```bash
# Remove all metadata from file
ffmpeg -i input.mp4 -map_metadata -1 -c copy stripped.mp4

# Verify metadata is gone
ffprobe -v quiet -show_format -of json stripped.mp4 | python3 -c "import sys,json; d=json.load(sys.stdin); print(d['format'].get('tags', 'No tags — CLEAN'))"
```

### Add chapter markers
```bash
# Step 1: Create a chapters metadata file (chapters.txt)
cat > chapters.txt << 'EOF'
;FFMETADATA1
[CHAPTER]
TIMEBASE=1/1000
START=0
END=60000
title=Introduction

[CHAPTER]
TIMEBASE=1/1000
START=60000
END=300000
title=Main Content

[CHAPTER]
TIMEBASE=1/1000
START=300000
END=600000
title=Conclusion
EOF

# Step 2: Embed chapters into the video
ffmpeg -i input.mp4 -i chapters.txt -map_metadata 1 -c copy chaptered.mp4

# Verify chapters
ffprobe -v quiet -show_chapters chaptered.mp4
```

> **Windows (PowerShell):** Write chapters.txt manually with a text editor, then run the ffmpeg step 2 command.

### Embed cover art into audio file (MP3, M4A, AAC)
```bash
# Embed cover art into MP3
ffmpeg -i input.mp3 -i cover.jpg \
  -map 0 -map 1 \
  -c copy -id3v2_version 3 \
  -metadata:s:v title="Album cover" \
  -metadata:s:v comment="Cover (front)" \
  output_with_cover.mp3

# Embed cover art into M4A/AAC
ffmpeg -i input.m4a -i cover.jpg \
  -map 0 -map 1 \
  -c copy -disposition:v:0 attached_pic \
  output_with_cover.m4a
```

### Multi-language audio/subtitle track management
```bash
# Add language tag to existing track
ffmpeg -i input.mp4 -c copy \
  -metadata:s:a:0 language=eng \
  -metadata:s:a:1 language=spa \
  tagged_lang.mp4

# Extract specific language track
ffmpeg -i input.mp4 -map 0:a:0 -c copy english_audio.aac

# Remove a specific stream (e.g. remove second audio track)
ffmpeg -i input.mp4 -map 0 -map -0:a:1 -c copy removed_track.mp4
```

### Read all metadata
```bash
ffprobe -v quiet -show_format -show_streams -of json input.mp4 | python3 -c "
import sys, json
d = json.load(sys.stdin)
print('=== Format Tags ===')
for k, v in d['format'].get('tags', {}).items():
    print(f'  {k}: {v}')
for i, s in enumerate(d['streams']):
    print(f'=== Stream {i} ({s[\"codec_type\"]}) Tags ===')
    for k, v in s.get('tags', {}).items():
        print(f'  {k}: {v}')
"
```

---

## SECTION S — Testing & Debugging

### Generate SMPTE color bars + tone (calibration signal)
```bash
# Standard SMPTE color bars with 1kHz test tone — use to verify encoding pipeline
ffmpeg -f lavfi -i "smptebars=duration=10:size=1920x1080:rate=30" \
       -f lavfi -i "sine=frequency=1000:duration=10" \
       -c:v libx264 -crf 18 -c:a aac \
       smpte_bars.mp4

# SMPTE HDBars (HD version)
ffmpeg -f lavfi -i "smptehdbars=duration=10:size=1920x1080:rate=30" \
       -f lavfi -i "sine=frequency=1000:duration=10" \
       -c:v libx264 -crf 18 -c:a aac \
       smpte_hdbars.mp4

# Windows PowerShell — identical commands
```

### Packet-level analysis (find corruption, missing keyframes)
```bash
# List all video packets with PTS, DTS, size, flags
ffprobe -v quiet -select_streams v:0 \
  -show_packets -of json input.mp4 | python3 -c "
import sys, json
d = json.load(sys.stdin)
pkts = d['packets']
keyframes = [p for p in pkts if p['flags'] in ('K_', 'K')]
print(f'Total packets : {len(pkts)}')
print(f'Keyframes     : {len(keyframes)}')
print(f'Duration span : {pkts[0][\"pts_time\"]}s → {pkts[-1][\"pts_time\"]}s')
gaps = [(pkts[i]['pts_time'], pkts[i+1]['pts_time']) for i in range(len(pkts)-1)
        if float(pkts[i+1]['pts_time']) - float(pkts[i]['pts_time']) > 0.1]
if gaps: print(f'Gaps detected : {gaps[:5]}')
else: print('No gaps detected')
"

# Detect corrupt packets
ffmpeg -v error -i input.mp4 -f null - 2>&1 | grep -E "corrupt|invalid|error"

# Windows PowerShell
ffmpeg -v error -i input.mp4 -f null NUL 2>&1 | Select-String -Pattern "corrupt|invalid|error"
```

### Encoding benchmark (compare presets)
```bash
# Benchmark H.264 presets — measures encode speed and output size
python3 - << 'EOF'
import subprocess, time, os

input_file = "input.mp4"   # change to your file
presets = ["ultrafast", "fast", "medium", "slow"]
results = []

for preset in presets:
    out = f"bench_{preset}.mp4"
    start = time.time()
    subprocess.run([
        "ffmpeg", "-y", "-i", input_file,
        "-c:v", "libx264", "-preset", preset, "-crf", "23",
        "-an", out
    ], capture_output=True)
    elapsed = time.time() - start
    size_mb = os.path.getsize(out) / 1024 / 1024
    results.append((preset, elapsed, size_mb))
    os.remove(out)

print(f"{'Preset':<12} {'Time (s)':<12} {'Size (MB)':<10}")
print("-" * 36)
for preset, t, s in results:
    print(f"{preset:<12} {t:<12.1f} {s:<10.2f}")
EOF
```

### Bit stream filter debugging
```bash
# Dump raw H.264 NAL units for inspection
ffmpeg -i input.mp4 -c:v copy -bsf:v trace_headers -f null - 2>&1 | head -50

# Check if MP4 is streamable (moov atom position)
ffprobe -v quiet -show_format -of json input.mp4 | python3 -c "
import sys, json
d = json.load(sys.stdin)
print('Format:', d['format']['format_name'])
print('Duration:', d['format'].get('duration', 'unknown'), 's')
print('Bitrate:', int(d['format'].get('bit_rate', 0)) // 1000, 'kbps')
"

# Measure actual encode speed on your hardware
ffmpeg -benchmark -i input.mp4 -c:v libx264 -preset medium -an -f null - 2>&1 | grep bench
```

---

## STEP 3 — Output Review

After generating any command, always:

1. **Explain what each flag does** — never leave flags unexplained
2. **State the expected output** — codec, resolution, duration, approximate file size
3. **Flag potential issues** — codec availability, platform support, quality trade-offs
4. **Provide the validation command** — so the agent/user can confirm success
5. **Suggest optimizations** — if a faster or better approach exists, mention it

---

## Quick Decision Reference

| Goal | Recommended Approach |
|------|---------------------|
| Change container, same codec | `-c copy` remux |
| Reduce file size | H.265/CRF 28 or VP9 |
| Maximum compatibility | H.264/AAC in MP4 |
| Professional editing | ProRes or DNxHD |
| Web streaming | H.264 + `-movflags +faststart` |
| Lossless archival | FFV1 + FLAC in MKV |
| Audio podcast | MP3 VBR q:a 2 or AAC 192k |
| Thumbnails fast | `-ss` before `-i`, `-vframes 1` |
| Analyze file | `ffprobe -print_format json` |
| Fix rotation | `transpose` filter |
| Precise cut | Re-encode with accurate `-ss` after `-i` |
| Fast cut (slight imprecision OK) | `-ss` before `-i` + `-c copy` |

---

## Common Error Diagnosis

| Error | Likely Cause | Fix |
|-------|-------------|-----|
| `Encoder not found` | Codec not compiled into ffmpeg | Install full ffmpeg build |
| `Invalid option -crf` | Using `-crf` with copy or incompatible codec | Remove `-crf`, use `-b:v` |
| `moov atom not found` | Corrupt/truncated input | Use `-analyzeduration 100M -probesize 100M` |
| `No audio/video stream` | Wrong `-map` or stream missing | Check streams with `ffprobe`, fix `-map` |
| `Output file is empty` | Missing output path or filter error | Check filtergraph syntax, verify paths |
| `Trailing option(s) found` | Flag order wrong | Move input flags before `-i` |
| `Unable to find a suitable output format` | Missing output extension | Add correct extension to output file |
| `Conversion failed!` | See preceding error lines | Run with `-loglevel debug` for full trace |

---

## References

- `references/ffprobe-analysis.md` — Complete ffprobe query patterns and JSON parsing
- `references/codecs-containers.md` — Codec compatibility matrix and container guide
- `references/ffmpeg-flags.md` — Complete flag reference with defaults and ranges
- `assets/platform-presets.md` — Ready-to-use presets for 20+ platforms
- `assets/quality-checklist.md` — Pre-release quality verification checklist
- `assets/features.md` — Feature overview and capability descriptions
