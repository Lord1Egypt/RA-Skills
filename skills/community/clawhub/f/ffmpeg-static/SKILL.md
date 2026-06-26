---
name: ffmpeg-static-skill
description: "FFmpeg operations via the ffmpeg-static npm package (bundled binary) with automatic fallback to a native system FFmpeg installation. Use for: video/audio transcoding, stream manipulation, thumbnail extraction, format conversion, and any FFmpeg pipeline from Node.js or shell scripts."
metadata:
  openclaw:
    requires:
      bins:
        - node
        - npm
      env: []
    install:
      - kind: npm
        package: ffmpeg-static
        global: false
    primaryEnv: ""
    emoji: "🎞️"
    homepage: https://github.com/eugeneware/ffmpeg-static
    os:
      - linux
      - macos
      - windows
---

# FFmpeg Static Skill

This skill wires **[ffmpeg-static](https://github.com/eugeneware/ffmpeg-static)** — a self-contained FFmpeg binary distributed as an npm package — into every assistant interaction. When a native system FFmpeg is also installed, the skill prefers the system binary (usually newer and GPU-capable); otherwise it falls back to the bundled one. All FFmpeg capabilities are available in both paths.

> **No PATH manipulation needed.** `require('ffmpeg-static')` returns the absolute path to the binary; scripts pass it directly to `child_process.spawn`.

---

## Security Notice

- `ffmpeg-static` downloads pre-built binaries from GitHub Releases during `npm install`. Verify the package on [npmjs.com/package/ffmpeg-static](https://www.npmjs.com/package/ffmpeg-static).
- Never pipe untrusted filenames or URLs into FFmpeg commands without validation — FFmpeg can read from URLs and arbitrary protocols.
- The bundled binary does **not** include GPU-accelerated encoders (nvenc, vaapi, videotoolbox). For hardware acceleration, use the system FFmpeg.

---

## Installation

### Minimum install (bundled FFmpeg binary only)
```bash
npm install ffmpeg-static
```

### Project install with ffprobe (recommended)
```bash
npm install ffmpeg-static ffprobe-static
```

### Verify the binary path
```bash
node -e "console.log(require('ffmpeg-static'))"
# e.g. /path/to/node_modules/ffmpeg-static/ffmpeg
```

### Check resolved binary (bundled vs. system)
```bash
node scripts/resolve_ffmpeg.js
```

---

## Binary Resolution Logic

The skill resolves the FFmpeg binary in this priority order:

1. **`FFMPEG_PATH` env var** — explicit override, always wins
2. **System FFmpeg** — found by walking `PATH` directories with `fs.accessSync`; preferred when present (newer codecs, hardware acceleration)
3. **Bundled binary** — `require('ffmpeg-static')` absolute path; guaranteed to exist after `npm install`

```js
// Canonical resolution — use this pattern in all scripts
const { resolveFfmpeg } = require('./scripts/resolve_ffmpeg');
const ffmpegPath = resolveFfmpeg(); // throws if none found
```

---

## Common Operations

### Transcode video to H.264/AAC MP4
```bash
$(node -e "process.stdout.write(require('ffmpeg-static'))") \
  -i input.mkv -c:v libx264 -crf 23 -preset fast \
  -c:a aac -b:a 128k output.mp4
```

### Extract thumbnail at timestamp
```bash
ffmpeg -ss 00:01:30 -i input.mp4 -frames:v 1 -q:v 2 thumb.jpg
```

### Convert audio to MP3
```bash
ffmpeg -i input.flac -q:a 2 output.mp3
```

### Extract audio stream only
```bash
ffmpeg -i input.mp4 -vn -c:a copy audio.aac
```

### Trim without re-encoding
```bash
ffmpeg -ss 00:00:10 -to 00:01:00 -i input.mp4 -c copy trimmed.mp4
```

### Concatenate files
```bash
ffmpeg -f concat -safe 0 -i filelist.txt -c copy output.mp4
```
`filelist.txt` format:
```
file '/abs/path/clip1.mp4'
file '/abs/path/clip2.mp4'
```

### Scale video (maintain aspect ratio)
```bash
ffmpeg -i input.mp4 -vf "scale=1280:-2" -c:a copy scaled.mp4
```

### Generate animated GIF
```bash
ffmpeg -i input.mp4 -vf "fps=10,scale=480:-1:flags=lanczos,split[s0][s1];[s0]palettegen[p];[s1][p]paletteuse" output.gif
```

### HLS stream packaging
```bash
ffmpeg -i input.mp4 -codec: copy -start_number 0 \
  -hls_time 10 -hls_list_size 0 -f hls output.m3u8
```

---

## Using From Node.js

Copy-paste patterns are in `templates/node_patterns.txt`. Key steps:

1. **Resolve the binary** using `scripts/resolve_ffmpeg.js` (pure `fs`, no shell calls)
2. **Spawn FFmpeg** in your own project code using Node's `child_process.spawn`
3. **Or use `fluent-ffmpeg`** — pass the resolved path via `ffmpeg.setFfmpegPath()`

```js
// In YOUR project (not inside the skill)
const { resolveFfmpeg } = require('ffmpeg-static-skill/scripts/resolve_ffmpeg');
const ffmpegBin = resolveFfmpeg(); // absolute path, ready to pass to spawn or fluent-ffmpeg
```

See `templates/node_patterns.txt` for ready-to-copy spawn, progress, ffprobe, and fluent-ffmpeg snippets.

---

## Environment Variables

| Variable | Effect |
|----------|--------|
| `FFMPEG_PATH` | Override binary path; takes precedence over system and bundled |
| `FFPROBE_PATH` | Override ffprobe binary path |
| `FFMPEG_STATIC_SKIP_BINARY_DOWNLOAD` | Set to `1` to skip download during `npm install` (use with system FFmpeg) |

---

## Best Practices

### 1. Always resolve the binary once at startup
Call `resolveFfmpeg()` once and cache the result — don't call `require('ffmpeg-static')` inline in hot paths.

### 2. Prefer `-c copy` when no re-encoding is needed
Stream copy (`-c copy`) is instantaneous and lossless. Only decode/encode when you actually need to change the codec or apply filters.

### 3. Use `-ss` before `-i` for fast seeking
`-ss 00:01:00 -i input.mp4` (before `-i`) uses keyframe seeking (fast). `-i input.mp4 -ss 00:01:00` (after `-i`) decodes from the start (accurate but slow for large files).

### 4. Always pass `-y` in non-interactive scripts
`-y` overwrites output without prompting. Without it, FFmpeg hangs waiting for stdin in CI or background processes.

### 5. Validate inputs before building command arrays
Never interpolate user-supplied strings directly into FFmpeg args. Always validate paths exist and are the expected media type using ffprobe first.

### 6. For hardware encoding, require system FFmpeg
Check `ffmpeg -hwaccels` at startup and gate hardware-accelerated paths on the system binary being active.

### 7. Set `-loglevel error` in production
Reduces stderr noise. Re-enable verbose logging (`-loglevel verbose`) when debugging a failed transcode.

---

## Supported Formats (Bundled Binary)

The bundled `ffmpeg-static` binary is compiled with a broad but fixed set of codecs. Key inclusions:

**Video:** H.264 (libx264), H.265 (libx265), VP8/VP9 (libvpx), AV1 (libaom-av1), MPEG-2/4, ProRes, DNxHD, Theora  
**Audio:** AAC (native + libfdk-aac where licensed), MP3 (libmp3lame), Opus (libopus), Vorbis, FLAC, PCM  
**Containers:** MP4, MKV, MOV, WebM, AVI, TS, HLS (m3u8), DASH, FLV, GIF, APNG  
**Images:** MJPEG, PNG, WebP (via lavf)

> Hardware encoders (nvenc, qsv, vaapi, videotoolbox) are **not** in the bundled binary. Use the system FFmpeg for GPU acceleration.

---

## Troubleshooting

| Symptom | Fix |
|---------|-----|
| `Cannot find module 'ffmpeg-static'` | Run `npm install ffmpeg-static` in the project root |
| Binary not executable on Linux/macOS | Run `chmod +x $(node -e "process.stdout.write(require('ffmpeg-static'))")` |
| `Encoder libx264 not found` | Bundled binary may lack the codec; install system FFmpeg (`apt install ffmpeg` / `brew install ffmpeg`) |
| `No such file or directory` on output | Ensure the output directory exists before running FFmpeg |
| Transcode hangs in CI | Add `-y` flag to overwrite without prompting |
| Progress not reported | Use `-progress pipe:1` to write progress data to stdout |
| Slow GIF generation | Use the two-pass palettegen approach (see example above) |
| `FFMPEG_STATIC_SKIP_BINARY_DOWNLOAD` ignored | Set the env var before running `npm install`, not after |
