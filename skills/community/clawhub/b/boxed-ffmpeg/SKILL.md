---
name: boxed-ffmpeg
description: Audio/video information extraction, format conversion, and audio extraction using FFmpeg WASM sandbox.
---

# Boxed FFmpeg Skill

Run FFmpeg commands safely within a WASM sandbox for audio/video processing.

## Triggering

Use this skill when the user says:
- "ffmpeg", "media info", "get video information"
- "convert video", "change video format", "格式转换"
- "extract audio", "audio from video", "提取音频"
- "boxed-ffmpeg"

## ⚠️ Required Plugin

**This skill requires the `openclaw-wasm-sandbox` plugin version `>= 0.2.0`.**

```bash
openclaw plugins install clawhub:openclaw-wasm-sandbox
openclaw plugins update openclaw-wasm-sandbox
openclaw gateway restart
```

## ⚠️ WASM File Required

If the WASM file does not exist, download it first:

```javascript
wasm-sandbox-download({
  url: "https://raw.githubusercontent.com/guyoung/wasm-sandbox-openclaw-skills/main/boxed-ffmpeg/files/boxed-ffmpeg-component.wasm",
  output: "~/.openclaw/skills/boxed-ffmpeg/files/boxed-ffmpeg-component.wasm",
  resume: false,
  timeout: 120000
})
```

## Tool: wasm-sandbox-run

```javascript
wasm-sandbox-run({
  wasmFile: "~/.openclaw/skills/boxed-ffmpeg/files/boxed-ffmpeg-component.wasm",
  workDir: "<input-file-directory>",
  args: ["<COMMAND>", "<INPUT>", "<OUTPUT>"]
})
```

**Important:**
- `workDir` must be set to the directory containing the input file
- Input/output arguments are **filenames only** (no directory paths)

## Commands

| Command | Description | Arguments |
|---------|-------------|-----------|
| `info` | Get media file information | `<INPUT>` |
| `convert` | Convert video format | `<INPUT> <OUTPUT>` |
| `extract-audio` | Extract audio from video | `<INPUT> <OUTPUT>` |

## Examples

### Get Media Information
User says: "Get info about video.mp4" (file in workspace root)

```javascript
wasm-sandbox-run({
  wasmFile: "~/.openclaw/skills/boxed-ffmpeg/files/boxed-ffmpeg-component.wasm",
  workDir: "/home/user/.openclaw/workspace",
  args: ["info", "video.mp4"]
})
```

### Convert Video Format
User says: "Convert video.mp4 to AVI" (file in workspace root)

```javascript
wasm-sandbox-run({
  wasmFile: "~/.openclaw/skills/boxed-ffmpeg/files/boxed-ffmpeg-component.wasm",
  workDir: "/home/user/.openclaw/workspace",
  args: ["convert", "video.mp4", "video.avi"]
})
```

### Extract Audio from Video
User says: "Extract audio from video.mp4 as mp3" (file in workspace root)

```javascript
wasm-sandbox-run({
  wasmFile: "~/.openclaw/skills/boxed-ffmpeg/files/boxed-ffmpeg-component.wasm",
  workDir: "/home/user/.openclaw/workspace",
  args: ["extract-audio", "video.mp4", "audio.mp3"]
})
```

### Convert with Subdirectory
User says: "Convert videos/input.mp4 to videos/output.avi"

```javascript
wasm-sandbox-run({
  wasmFile: "~/.openclaw/skills/boxed-ffmpeg/files/boxed-ffmpeg-component.wasm",
  workDir: "/home/user/.openclaw/workspace/videos",
  args: ["convert", "input.mp4", "output.avi"]
})
```

## Important Notes

- **workDir is required** — must be the directory of the input file
- **Input/output are filenames only** — no paths, just names
- **Output file appears in workDir** after successful execution
- **No network access needed** — all processing is local
