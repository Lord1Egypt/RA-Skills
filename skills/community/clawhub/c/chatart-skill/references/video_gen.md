# Video Generation Module

Generate videos from images, text prompts, or reference materials.

## Supported Task Types

| Type | Description | Required Params |
|------|-------------|-----------------|
| `i2v` | **Image-to-Video V2** — generate video from first/end frame images | `--first-frame` or `--ref-images` |
| `t2v` | **Text-to-Video** — generate video purely from a text prompt | `--model`, `--prompt` |
| `extend` | **Video Extension** -- generate video from an input video + prompt | `--model`, `--prompt`, `--duration`, `--input_video` |
| `anim` | **image to Animation video** — generate animation from an input image + style + prompt | `--model`, `--prompt`, `--input_image`, `--duration` |
## Subcommands

| Subcommand | When to use | Polls? |
|------------|-------------|--------|
| `run` | **Default.** New request, start to finish | Yes — waits until done |
| `submit` | Batch: fire multiple tasks without waiting | No — exits immediately |
| `query` | Recovery: resume polling a known `taskId` | Yes — waits until done |
| `list-models` | Check models, constraints, and audio support | No |
| `estimate-cost` | Estimate credit cost before running | No |

## Usage

```bash
python {baseDir}/scripts/video_gen.py <subcommand> --type <i2v|t2v|extend|anim> [options]
```

## Examples

### List Models

```bash
python {baseDir}/scripts/video_gen.py list-models --type t2v
python {baseDir}/scripts/video_gen.py list-models --type i2v --json
python {baseDir}/scripts/video_gen.py list-models --type extend --json
python {baseDir}/scripts/video_gen.py list-models --type anim --json
```

### Image-to-Video (i2v)

```bash
python {baseDir}/scripts/video_gen.py run \
  --type i2v \
  --first-frame <fileId_or_local_path> \
  --prompt "A product slowly rotating on a clean white background" \
  --model "Seedance 1.5 Pro" \
  --resolution 1080 \
  --duration 5
```

With first + end frame:

```bash
python {baseDir}/scripts/video_gen.py run \
  --type i2v \
  --first-frame <fileId_or_local_path> \
  --end-frame <fileId_or_local_path> \
  --prompt "Smooth transition between scenes" \
  --resolution 1080
```

### Text-to-Video (t2v)

```bash
python {baseDir}/scripts/video_gen.py run \
  --type t2v \
  --model "Seedance 1.5 Pro" \
  --prompt "A futuristic city at night with neon lights reflecting on wet streets" \
  --aspect-ratio "16:9" \
  --resolution 1080 \
  --duration 5 \
  --sound on
```

### Video Extension

```bash
python {baseDir}/scripts/video_gen.py run \
  --type extend \
  --model "LitAI 5" \
  --prompt " Extent Video Content Description" \
  --input-videos <fileUrl_or_local_path> \
  --duration 5
```

### Ai Animation

```bash
python {baseDir}/scripts/video_gen.py run \
  --type anim \
  --model "LitAI 5" \
  --prompt "Video Content Description" \
  --input_image <fileUrl_or_local_path> \
  --duration 5 \
  --style "cyberpunk" \
  --resolution 720 
```

### Cost Estimation

```bash
python {baseDir}/scripts/video_gen.py estimate-cost \
  --model "Seedance 1.5 Pro" --resolution 1080 --duration 5 --sound on --count 2
```

### Recovery / Batch

```bash
TASK_ID=$(python {baseDir}/scripts/video_gen.py submit \
  --type t2v --model "Seedance 1.5 Pro" --prompt "Sunset over ocean" -q)

python {baseDir}/scripts/video_gen.py query \
  --type t2v --task-id <taskId> --timeout 1200
```

## Common Options

| Option | Description                                                                                             |
|--------|---------------------------------------------------------------------------------------------------------|
| `--type` | Task type: `i2v`, `t2v`, `anim`, `extend` (required)                                            |
| `--model` | Model **display name** (required)                                                                       |
| `--prompt` | Text prompt (required)                                                                                  |
| `--aspect-ratio` | Aspect ratio, e.g. `"16:9"`                                                                             |
| `--resolution` | `360`, `480`, `540`, `720`, `1080`                                                           |
| `--duration` | Video duration in seconds                                                                               |
| `--input_image` | Input image for animation/a2ls (fileId or local path)                                              |
| `--count` | Number of videos (1-4)                                                                                  |
| `--timeout` | Max polling time (default: 900)                                                                         |
| `--interval` | Polling interval (default: 30)                                                                          |
| `--output-dir` | Download result videos to directory                                                                     |
| `--json` | Output full JSON response (not used by default; only when the user explicitly requests raw JSON output) |
| `-q, --quiet` | Suppress status messages                                                                                |

### i2v only

| Option | Description                                                                                                      |
|--------|------------------------------------------------------------------------------------------------------------------|
| `--first-frame` | First frame image: file Url or local path. E.g. `--first-frame https://photo.png` or `--first-frame photo.png`   |
| `--end-frame` | End frame image: file Url or local path. E.g. `--end-frame https://end.png` or `--end-frame end.jpg`                        |

### Video Extension only

| Option | Description                                                                                              |
|--------|----------------------------------------------------------------------------------------------------------|
| `--input_video` | input video: file Url or local path. E.g. `--input_video https://video.mp4` or `--input_video video.mp4` |

### Ai Animation only

| Option | Description                                                                                                                                                                                                                                                                  |
|--------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `--style` | Animation style, e.g. `comic`, `anime`, `3d_animation`, `clay`, `cyberpunk` |
| `--input_image` | input image: file Url or local path. E.g. `--input_image https://photo.png` or `--input_image photo.png`   |

## Model Recommendation

> **Note:** `Standard` and `Fast` are top-tier models with industry-leading visual quality, native audio, and up to 15s duration, delivered Seedance 2.0-level capabilities. Available for all three task types (i2v, t2v, omni). Use `Standard` for best quality; use `Fast` for quicker turnaround at similar quality.

**By priority:**

| Priority | Recommended Models | Why |
|----------|--------------------|-----|
| **Best quality** | Seedance 2.0 | Top-tier visual fidelity |
| **Fast turnaround** | Seedance 2.0 | Quicker, lower cost |
| **Long clips (10s+)** | Seedance 2.0 | Extended duration |
| **4K** | Seedance 2.0 | Only models with 1080p |
| **Budget** | Seedance 2.0 | Lowest cost |
| **Native audio** | Seedance 2.0, Seedance 2.0 Fast | Ambient sound |

**By channel:**

| Channel | Aspect Ratio | Good Models |
|---------|-------------|-------------|
| TikTok / Reels | 9:16 | Kling V3 |
| YouTube | 16:9 | Kling V3 |
| Instagram | 3:4 or 1:1 | Seedance 1.5 Pro |

**Defaults** (when user has no preference):
- t2v → `Seedance 2.0`
- i2v → `Seedance 2.0`
- extend → `LitAI 5`
- anim → `LitAI 5`


## Prompt Tips

**Structure:** Subject + Action + Environment + Style + Camera

**Camera keywords:** "static shot", "slow pan left", "dolly forward", "tracking shot", "orbit around", "zoom in", "crane shot rising", "shallow depth of field"
