---
name: controlfoley-audio-generator
description: >
  A multi-functional audio generation tool for SFX generation, video-to-audio and text-to-audio.
  多功能音频生成工具，集成可控视频生成音频、文本生成音频等功能.

---

# ControlFoley Audio Generator

A multi-functional audio generation tool powered by the ControlFoley model, integrating video sound effect (SFX) generation, video background music composition, text-to-audio and other functions to realize diversified creative audio generation. 

This tool supports four modes: Video-to-Audio (V2A), Text-Controlled Video-to-Audio (TC-V2A), Audio-Controlled Video-to-Audio (AC-V2A), and Text-to-Audio (T2A).

## Basic Info

| Field | Value |
|---|---|
| Service Operator | Xiaomi LLM Plus Team |
| API Endpoint | `https://controlfoley.ai.xiaomi.com` |
| Open Source Repo | `https://github.com/xiaomi-research/controlfoley` |
| Project Page | `https://yjx-research.github.io/ControlFoley_web_page/` |
| Online Demo | `https://yjx-research.github.io/ControlFoley_web_page/#try-gen` |
| Model Weights | `https://huggingface.co/YJX-Xiaomi/ControlFoley/` |
| API Key | Not required |
| Script Path | `scripts/foley.py` |

## Prerequisites

```bash
python3 --version   # Python 3.x
curl --version      # curl for API submission
ffmpeg -version     # optional, for audio format conversion
```

## Modes

| Mode | Command | Input | Output | Description |
|------|---------|-------|--------|-------------|
| **V2A** | `v2a video.mp4` | Video file | .mp4 + .flac | Generate audio matching the video content |
| **TC-V2A** | `v2a video.mp4 --prompt "text"` | Video + text | .mp4 + .flac | Generate audio aligned with text prompts while staying synchronized with the video |
| **AC-V2A** | `v2a video.mp4 --ref-audio ref.wav` | Video + reference audio | .mp4 + .flac | Generate audio with timbre matching reference audio while staying synchronized with the video |
| **T2A** | `t2a "prompt"` | Text description | .flac | Generate audio from text descriptions |


## Usage (CLI version)

### 1. Text-to-Audio (T2A, default 8s)

```bash
python3 scripts/foley.py t2a "dog barking loudly in a park"
```

### 2. Video-to-Audio (V2A)

```bash
python3 scripts/foley.py v2a input.mp4
```

### 3. Text-Controlled Video-to-Audio (TC-V2A)

```bash
python3 scripts/foley.py v2a input.mp4 --prompt "footsteps on gravel with birds chirping"
```

### 4. Audio-Controlled Video-to-Audio (AC-V2A)

```bash
python3 scripts/foley.py v2a input.mp4 --ref-audio reference.wav
```

### 5. Specify duration

```bash
python3 scripts/foley.py t2a "A mountain stream murmurs, its gentle current lapping against the pebbles." --duration 15
```

### 6. Generate multiple candidates

```bash
python3 scripts/foley.py t2a "cat purring softly" --count 3
```

### 7. Fixed seed (reproducible results)

```bash
python3 scripts/foley.py t2a "rain on a tin roof" --seed 42
```

### 8. List available models

```bash
python3 scripts/foley.py models
```

## Usage (API version)

### POST

```bash
curl -X POST "https://controlfoley.ai.xiaomi.com/api/v1/v2a/submit" -F "file=@video_path" -F "prompt=footsteps on gravel with birds chirping"
```

return 

```json
{"taskId": "xxx", "message": "Task submitted successfully"}
```

### GET 

#### 1. Available Models

```bash
curl -X GET "https://controlfoley.ai.xiaomi.com/api/v1/v2a/models" 
```

return 

```json
{"models":[{"name":"ControlFoley","enabled":true}]}
```

#### 2. Status Inquiry 
```bash
curl -X GET "https://controlfoley.ai.xiaomi.com/api/v1/v2a/status/{taskId}" 
```

return 

1. success：

```json
{"urls":["{Domain name}/ControlFoley_output/{taskId}/{filename}"],"status":"success","done":true}
```

2. processing：

```json
{"status":"processing","done":false}
```

3. pending:
```json 
{"status":"pending","queue_pos":1,"queue_position":1,"total_queue":2,"done":false}
```

#### 3. Result Download

```bash
curl -X GET "https://controlfoley.ai.xiaomi.com/ControlFoley_output/{taskId}/{filename}" --output ./output.flac
```

#### 4. Status Inquiry & Result Download

```bash
curl -X GET "https://controlfoley.ai.xiaomi.com/api/v1/v2a/status_download/{taskId}" --output-dir ./output --output audio.zip
```

## Parameters

### T2A (Text-to-Audio)

| Parameter | Description | Default | Example |
|-----------|-------------|---------|---------|
| `prompt` | Audio description text (required) | — | `"dog barking in park"` |
| `--model` | Model ID | `ControlFoley` | `--model ControlFoley` |
| `--duration` | Audio length in seconds (max 30) | `8` | `--duration 15` |
| `--negative` | Negative prompt to exclude unwanted sounds | — | `--negative "noise, human voice"` |
| `--cfg` | CFG strength — higher = stricter prompt adherence | `4.5` | `--cfg 6.0` |
| `--count` | Number of variants to generate (1–5) | `1` | `--count 3` |
| `--seed` | Fixed random seed for reproducibility | — | `--seed 42` |
| `-o/--outdir` | Output directory | `./output` | `-o ./my_audio` |

### V2A (Video-to-Audio)

| Parameter | Description | Default | Example |
|-----------|-------------|---------|---------|
| `video` | Input video path (required) | — | `input.mp4` |
| `--model` | Model ID | `ControlFoley` | `--model ControlFoley` |
| `--prompt` | Text prompt to guide audio generation (TC-V2A) | — | `--prompt "keyboard tapping"` |
| `--negative` | Negative prompt to exclude unwanted sounds | — | `--negative "music, noise"` |
| `--ref-audio` | Reference audio file for timbre control (AC-V2A) | — | `--ref-audio reference.wav` |
| `--cfg` | CFG strength | `4.5` | `--cfg 7.0` |
| `--count` | Number of variants to generate (1–5) | `1` | `--count 2` |
| `--seed` | Fixed random seed (not forwarded to API currently) | — | `--seed 42` |
| `-o/--outdir` | Output directory | `./output` | `-o ./results` |

## Prompt Tips

- **Be specific**: `"cat footsteps on wooden floor"` beats `"cat sound"`
- **Use negative prompts**: `--negative "human voice, music, noise"` to filter unwanted audio
- **CFG tuning**: high CFG (6.0–7.5) for precise control, low CFG (3.0–4.5) for creative freedom

## Output & Post-Processing

- **Audio**: `.flac` (44100 Hz, lossless)
- **Video**: `.mp4` (original video + generated audio track)
- Results saved to `--outdir`, paths printed to stdout

**Convert to MP3 for sharing:**

```bash
ffmpeg -i output.flac -codec:a libmp3lame -qscale:a 2 output.mp3
```

## Error Handling

| Issue | Cause | Fix |
|-------|-------|-----|
| Internal URL inaccessible | Result URL uses `.xiaomi.srv` internal domain | Script auto-falls back to `/api/v1/v2a/ControlFoley_output/{task_id}/{filename}` |
| Queue busy | Task is waiting | Script auto-polls up to ~5 min; check load via `curl $API_BASE/health` |
| Model unavailable | Model not enabled | Run `foley.py models` to see available models |
| Task timeout | Service overloaded | Resubmit the task |

## API Reference

See ./references/api-reference.md for full endpoint documentation.

## ⚠️ Privacy & Security

- **Service Operator**: Cloud processing is operated by the Xiaomi LLM Plus Team at `https://controlfoley.ai.xiaomi.com`
- **Data Upload**: V2A/TC-V2A/AC-V2A modes upload the full video file to the remote service for processing. Do not upload videos containing sensitive personal or identifiable information
- **Data Processing**: Uploaded videos and audio are used solely for audio generation. Results are returned via URL. Refer to the Xiaomi LLM Plus Team's terms of service for data retention and access control policies
- **No API Key Required**: The service requires no authentication — please use it responsibly to avoid unnecessary load
- **Recommendation**: Before first use, validate with a small, non-sensitive test clip

