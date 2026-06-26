# FFmpeg Static API Reference

Complete reference for using `ffmpeg-static` (npm) with full FFmpeg CLI capabilities.

---

## Package Overview

| Property | Value |
|----------|-------|
| npm package | `ffmpeg-static` |
| Provides | Absolute path to a statically-linked FFmpeg binary |
| Node.js usage | `require('ffmpeg-static')` → `string` (absolute path) |
| ffprobe companion | `ffprobe-static` (`require('ffprobe-static').path`) |
| Upstream FFmpeg docs | https://ffmpeg.org/ffmpeg.html |

---

## Binary Resolution (`scripts/resolve_ffmpeg.js`)

```js
const { resolveFfmpeg, resolveFfprobe } = require('./scripts/resolve_ffmpeg');
const ffmpegPath  = resolveFfmpeg();   // throws if not found
const ffprobePath = resolveFfprobe();  // throws if not found
```

**Resolution order:**
1. `FFMPEG_PATH` env var
2. System FFmpeg — found by walking `PATH` directories with `fs.accessSync` (no shell invocation)
3. `require('ffmpeg-static')` bundled binary

---

## FFmpeg CLI — Global Flags

| Flag | Description |
|------|-------------|
| `-y` | Overwrite output without prompting (required in non-interactive scripts) |
| `-n` | Never overwrite; exit if output exists |
| `-loglevel <level>` | `quiet`, `error`, `warning`, `info`, `verbose`, `debug` |
| `-progress pipe:1` | Write machine-readable progress to stdout |
| `-stats` | Print encoding statistics to stderr (default on) |
| `-nostats` | Suppress statistics |
| `-hide_banner` | Suppress version/build info banner |
| `-threads <n>` | CPU threads for encoding (0 = auto) |

---

## Input / Output Flags

| Flag | Scope | Description |
|------|-------|-------------|
| `-i <file\|url>` | Input | Specify input file or URL |
| `-f <format>` | Input/Output | Force container format |
| `-ss <time>` | Input (before -i) | Fast keyframe seek |
| `-ss <time>` | Output (after -i) | Accurate decode seek |
| `-to <time>` | Output | Stop at timestamp |
| `-t <duration>` | Input/Output | Duration limit |
| `-fs <size>` | Output | File size limit in bytes |
| `-map <spec>` | Output | Select streams: `-map 0` (all), `-map 0:v:0` (first video), `-map 0:a:0` (first audio) |

**Time format:** `HH:MM:SS.mmm` or decimal seconds (e.g. `90.5`).

---

## Video Encoding Flags

| Flag | Description |
|------|-------------|
| `-c:v <codec>` | Video codec (`libx264`, `libx265`, `libvpx-vp9`, `copy`) |
| `-crf <0-51>` | Constant Rate Factor (libx264/libx265); lower = better quality; 23 is default |
| `-b:v <bitrate>` | Target video bitrate (e.g. `2M`, `500k`) |
| `-preset <name>` | libx264/libx265 speed/compression trade-off: `ultrafast` → `veryslow` |
| `-tune <name>` | libx264 tuning: `film`, `animation`, `grain`, `zerolatency`, `fastdecode` |
| `-profile:v <p>` | H.264 profile: `baseline`, `main`, `high` |
| `-pix_fmt <fmt>` | Pixel format: `yuv420p` (broadest compatibility), `yuv444p`, `rgb24` |
| `-r <fps>` | Output frame rate |
| `-vf <filtergraph>` | Video filter chain |
| `-vn` | Disable video stream |
| `-g <n>` | GOP size (keyframe interval) |

---

## Audio Encoding Flags

| Flag | Description |
|------|-------------|
| `-c:a <codec>` | Audio codec (`aac`, `libmp3lame`, `libopus`, `flac`, `copy`) |
| `-b:a <bitrate>` | Audio bitrate (e.g. `192k`, `320k`) |
| `-q:a <0-9>` | VBR quality for libmp3lame/libvorbis; lower = better |
| `-ar <rate>` | Sample rate (e.g. `44100`, `48000`) |
| `-ac <channels>` | Channel count (1=mono, 2=stereo, 6=5.1) |
| `-af <filtergraph>` | Audio filter chain |
| `-an` | Disable audio stream |
| `-vol <n>` | Volume (256 = 100%) |

---

## Video Filters (`-vf`)

| Filter | Example | Effect |
|--------|---------|--------|
| `scale` | `scale=1280:720` | Resize; use `-1` or `-2` to keep aspect ratio |
| `crop` | `crop=640:480:0:0` | Crop (w:h:x:y) |
| `fps` | `fps=30` | Force output frame rate |
| `transpose` | `transpose=1` | Rotate 90° clockwise |
| `hflip` / `vflip` | `hflip` | Mirror horizontal / vertical |
| `pad` | `pad=1920:1080:(ow-iw)/2:(oh-ih)/2` | Letterbox/pillarbox |
| `drawtext` | `drawtext=text='Hello':fontsize=24:x=10:y=10` | Burn in text overlay |
| `overlay` | `[0:v][1:v]overlay=10:10` | Composite two streams |
| `palettegen` + `paletteuse` | (two-pass) | High-quality GIF generation |
| `thumbnail` | `thumbnail=300` | Select representative frame every N frames |
| `setpts` | `setpts=0.5*PTS` | Speed up (0.5×) or slow down (2.0×) |

Chain filters with commas: `-vf "scale=1280:-2,fps=30"`

---

## Audio Filters (`-af`)

| Filter | Example | Effect |
|--------|---------|--------|
| `volume` | `volume=2.0` | Amplify / attenuate |
| `loudnorm` | `loudnorm=I=-16:TP=-1.5:LRA=11` | EBU R128 loudness normalization |
| `highpass` | `highpass=f=200` | High-pass filter |
| `lowpass` | `lowpass=f=3000` | Low-pass filter |
| `atempo` | `atempo=1.5` | Speed change (0.5–2.0 per pass) |
| `aresample` | `aresample=44100` | Resample |
| `pan` | `pan=stereo\|c0=c0\|c1=c1` | Channel routing |
| `silenceremove` | `silenceremove=1:0:-50dB` | Remove silence |

---

## Common Codec Reference

### Video Codecs

| Codec | Flag | Notes |
|-------|------|-------|
| H.264 | `libx264` | Universal compatibility; use `-crf 23 -preset fast` |
| H.265/HEVC | `libx265` | ~50% smaller than H.264; slower encode |
| VP9 | `libvpx-vp9` | Open; good for WebM/web delivery |
| AV1 | `libaom-av1` | Best compression; very slow encode |
| ProRes | `prores_ks` | Editing intermediate; large files |
| MJPEG | `mjpeg` | Per-frame JPEG; compatible with many editors |
| Stream copy | `copy` | No transcode; instant; preserves quality |

### Audio Codecs

| Codec | Flag | Notes |
|-------|------|-------|
| AAC | `aac` | Default for MP4; use `-b:a 128k`–`192k` |
| MP3 | `libmp3lame` | Ubiquitous; use `-q:a 2` for ~190 kbps VBR |
| Opus | `libopus` | Best at low bitrates; WebM/Ogg |
| FLAC | `flac` | Lossless; large files |
| PCM 16-bit | `pcm_s16le` | Uncompressed WAV |
| Stream copy | `copy` | Preserve original audio track |

---

## ffprobe — Media Inspection

```bash
ffprobe -v error -show_format -show_streams -of json input.mp4
```

### Get duration in seconds
```bash
ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 input.mp4
```

### List streams
```bash
ffprobe -v error -show_streams -of json input.mp4 | node -e "
  const d=JSON.parse(require('fs').readFileSync('/dev/stdin','utf8'));
  d.streams.forEach(s=>console.log(s.codec_type, s.codec_name, s.width||'', s.height||''));
"
```

### Node.js usage

See `templates/node_patterns.txt` for a copy-paste `probe()` / `getDuration()` implementation using `child_process.execFile` in your own project code.

---

## HLS / DASH Streaming

### HLS packaging
```bash
ffmpeg -i input.mp4 \
  -c:v libx264 -crf 23 -preset fast -g 48 -sc_threshold 0 \
  -c:a aac -b:a 128k \
  -f hls -hls_time 6 -hls_playlist_type vod \
  -hls_segment_filename 'segment_%03d.ts' \
  playlist.m3u8
```

### Multi-bitrate HLS (adaptive)
```bash
ffmpeg -i input.mp4 \
  -map 0:v -map 0:a -map 0:v -map 0:a \
  -c:v libx264 -c:a aac \
  -b:v:0 2M -b:v:1 500k -b:a:0 128k -b:a:1 96k \
  -var_stream_map "v:0,a:0 v:1,a:1" \
  -master_pl_name master.m3u8 \
  -f hls -hls_time 6 stream_%v/playlist.m3u8
```

---

## Hardware Acceleration (System FFmpeg Only)

Check available hwaccels:
```bash
ffmpeg -hwaccels
```

### NVIDIA NVENC
```bash
ffmpeg -i input.mp4 -c:v h264_nvenc -preset p4 -cq 23 output.mp4
```

### Intel QSV
```bash
ffmpeg -i input.mp4 -c:v h264_qsv -q 23 output.mp4
```

### AMD VAAPI (Linux)
```bash
ffmpeg -vaapi_device /dev/dri/renderD128 -i input.mp4 \
  -vf 'format=nv12,hwupload' -c:v h264_vaapi -qp 23 output.mp4
```

### Apple VideoToolbox (macOS)
```bash
ffmpeg -i input.mp4 -c:v h264_videotoolbox -q:v 60 output.mp4
```

> Hardware encoders are absent from the `ffmpeg-static` bundled binary. Ensure system FFmpeg is selected via `resolveFfmpeg()`.

---

## Node.js Integration Patterns

Copy-paste patterns for spawn, progress reporting, ffprobe, and fluent-ffmpeg are in `templates/node_patterns.txt`. Use `scripts/resolve_ffmpeg.js` to get the binary path, then invoke FFmpeg with `child_process.spawn` in your own project.

---

## Exit Codes

| Code | Meaning |
|------|---------|
| `0` | Success |
| `1` | General error (check stderr) |
| `127` | Binary not found (PATH / path resolution issue) |
| `130` | Interrupted by SIGINT (Ctrl+C) |

---

## Environment Variables

| Variable | Type | Description |
|----------|------|-------------|
| `FFMPEG_PATH` | string | Absolute path override for the ffmpeg binary |
| `FFPROBE_PATH` | string | Absolute path override for the ffprobe binary |
| `FFMPEG_STATIC_SKIP_BINARY_DOWNLOAD` | `"1"` | Skip binary download during `npm install` |

---

## Common Issues

| Symptom | Cause | Fix |
|---------|-------|-----|
| `Cannot find module 'ffmpeg-static'` | Package not installed | `npm install ffmpeg-static` |
| `EACCES: permission denied` on Linux/macOS | Binary not executable | `chmod +x $(node -e "process.stdout.write(require('ffmpeg-static'))")` |
| `Encoder libx264 not found` | Codec missing from bundled binary | Install system FFmpeg and set `FFMPEG_PATH` |
| `Unknown encoder 'h264_nvenc'` | No GPU encoder in bundled binary | Use system FFmpeg with CUDA support |
| Output file already exists, FFmpeg hangs | Missing `-y` flag | Add `-y` to args array |
| Very large output file | CRF too low or no rate control | Use `-crf 23` or set `-b:v` |
| Audio/video out of sync | Bad seek or missing `-async 1` | Use `-async 1` or re-mux with `-c copy` |
| `moov atom not found` | Truncated/corrupt input | Check source file; use `-err_detect ignore_err` cautiously |
