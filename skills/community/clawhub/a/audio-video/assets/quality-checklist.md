# Audio/Video Output Quality Checklist

Use this checklist before delivering any encoded file. Run each verification command and confirm expected values.

## Pre-Encode Checklist

- [ ] Input probed with `ffprobe` — know source codec, resolution, fps, duration
- [ ] Output directory exists and has write permissions
- [ ] Sufficient disk space (estimate: bitrate × duration ÷ 8)
- [ ] Codec is available in your ffmpeg build (`ffmpeg -encoders 2>&1 | grep <codec>` on macOS/Linux; `ffmpeg -encoders 2>&1 | Select-String <codec>` on Windows PowerShell)
- [ ] Correct pixel format for codec (`yuv420p` for H.264 in MP4)

## Post-Encode Verification

### 1. File exists and is non-zero
```bash
ffprobe -v error -show_entries format=size -of default=noprint_wrappers=1:nokey=1 "output.mp4"
# Prints file size in bytes; errors if file is missing or empty
```

### 2. No corrupt packets
```bash
ffmpeg -v error -i "output.mp4" -f null - 2>&1
# Expected: no output (silence = clean)
# Note: 2>&1 works on macOS/Linux. On Windows PowerShell use: ffmpeg ... 2>&1 (same syntax in PS); on cmd.exe: 2>&1
```

### 3. Duration matches expected
```bash
ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 "output.mp4"
# Check against input duration
```

### 4. All expected streams present
```bash
ffprobe -v error -show_entries stream=index,codec_type,codec_name -of csv "output.mp4"
# Verify: video + audio (+ subtitles if added)
```

### 5. Resolution correct
```bash
ffprobe -v error -select_streams v:0 -show_entries stream=width,height -of csv=p=0 "output.mp4"
```

### 6. Frame rate correct
```bash
ffprobe -v error -select_streams v:0 -show_entries stream=r_frame_rate -of default=noprint_wrappers=1:nokey=1 "output.mp4"
```

### 7. File size within target (if applicable)
```bash
ffprobe -v error -show_entries format=size -of default=noprint_wrappers=1:nokey=1 "output.mp4"
# Prints size in bytes
```

### 8. Playable (spot check — requires video player)
```bash
# macOS
open "output.mp4"
# Linux
mpv "output.mp4" 2>/dev/null || vlc "output.mp4"
# Note: 2>/dev/null is Linux/macOS only; on Windows omit it or use 2>NUL
# Windows
start "output.mp4"
```

### 9. Web MP4: moov atom at front
```bash
ffprobe -v quiet -show_entries format_tags=major_brand -of default "output.mp4"
# Confirm -movflags +faststart was used if needed
```

### 10. Audio levels acceptable (peak < 0dBFS)
```bash
ffmpeg -i "output.mp4" -af volumedetect -f null - 2>&1 | grep -E "mean_volume|max_volume"
# max_volume should be ≤ -0.1 dB (not clipping)
# Note: grep is not available on Windows — use PowerShell: ffmpeg ... 2>&1 | Select-String "mean_volume|max_volume"
```

## Quality Severity Levels

### 🔴 Critical (must fix before delivery)
- File is corrupt or zero bytes
- Missing video or audio streams
- Duration is wrong (>2s off for short clips, >5s for long)
- Codec incompatible with target platform

### 🟡 Warning (fix if possible)
- File size >20% larger than target
- Audio peaks at 0dBFS (potential clipping)
- Rotation metadata not handled (phone videos)
- Missing `-movflags +faststart` for web delivery

### 🟢 Info (acceptable for most use cases)
- Slight frame rate variation (29.97 vs 30)
- Minor timestamp gaps in non-broadcast content
- Using default metadata (no title/artist tags)
