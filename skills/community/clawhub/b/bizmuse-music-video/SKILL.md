---
name: bizmuse-music-video
version: 1.1.4
description: Create complete AI music videos from local audio or public audio URLs with 1-7 reference images. Use for single-track or batch music video production, creative direction, task monitoring, and result downloads through the official BizMuse CLI.
allowed-tools:
  - Bash(command -v bizmuse)
  - Bash(bizmuse *)
  - Bash(npm install -g bizmuse-cli)
metadata:
  openclaw:
    requires:
      bins:
        - bizmuse
    install:
      - kind: node
        package: bizmuse-cli
        bins:
          - bizmuse
    homepage: https://bizmuse.ai/skill
---

# BizMuse Music Video

Create a complete AI music video from a finished song and visual references through [BizMuse AI](https://bizmuse.ai). This skill keeps the user focused on creative direction while the official BizMuse CLI handles uploads, generation, task monitoring, and result delivery.

## Capabilities

- Create one complete music video from a local audio file or direct public audio URL.
- Use 1-7 reference images to guide subject identity, wardrobe, setting, and visual style.
- Choose a vertical, landscape, or square delivery format.
- Select storytelling, singing, dancing, or abstract content direction.
- Submit a directory of audio files as a bounded-concurrency batch.
- Monitor asynchronous generation tasks and download completed video and cover files.

This skill only uses the BizMuse `one-click-ai-mv` workflow. It does not advertise unrelated image, video, music, or third-party model capabilities.

## Requirements

- Node.js 18 or newer.
- The `bizmuse-cli` package installed as the `bizmuse` command.
- A BizMuse account, API key, and sufficient generation credits.
- One supported audio source and 1-7 supported reference images.

Install the CLI when it is not already available:

```bash
npm install -g bizmuse-cli
```

Create an API key at [bizmuse.ai/settings/apikeys](https://bizmuse.ai/settings/apikeys), then configure it in the user's own terminal:

```bash
bizmuse auth set-api-key <key>
```

Never ask the user to paste an API key into chat. Never print, repeat, or store credentials in project files.

## Supported Inputs

### Audio

- Local `.mp3`, `.wav`, `.m4a`, or `.aac` file.
- Direct public HTTP or HTTPS audio URL.
- Duration from 10 to 180 seconds.
- Maximum local upload size of 20 MB.

Suno, YouTube, Udio, SoundCloud, and similar platform page URLs are not direct audio URLs. Ask the user to export or download the audio first.

### Reference Images

- 1-7 local `.jpg`, `.jpeg`, `.png`, or `.webp` files.
- Direct public HTTP or HTTPS image URLs.
- Maximum local upload size of 50 MB per image.

Use clear, well-lit references when subject consistency matters. Do not claim guaranteed face, wardrobe, or scene consistency.

## Creative Intake

Before submitting, confirm:

1. Audio source.
2. Reference image sources.
3. Subject and setting.
4. Visual era, palette, lighting, and camera language.
5. Aspect ratio: `9:16`, `16:9`, or `1:1`.
6. Resolution: `540p`, `720p`, or `1080p`.
7. Content mode: `storytelling`, `singing`, `dancing`, or `abstract`.

Use [references/prompts.md](references/prompts.md) when the user needs help developing a coherent visual direction.

## Single Music Video Workflow

Submit one music video with machine-readable output:

```bash
bizmuse mv run \
  --audio "song.mp3" \
  --image "artist.jpg" "stage.jpg" \
  --prompt "Night performance in Tokyo, neon reflections, cinematic camera movement" \
  --ratio 9:16 \
  --resolution 720p \
  --content-mode storytelling \
  --json
```

Retain the returned task ID. A submitted task is not a completed video.

Check progress no more frequently than every 30 seconds:

```bash
bizmuse task status <task-id> --json
```

Only request the final result after the task reports success:

```bash
bizmuse task result <task-id> --json
```

When the user requests local files, stream the completed video and optional cover to a directory:

```bash
bizmuse task result <task-id> --download "./bizmuse-output" --json
```

## Batch Workflow

Use batch mode only when the user provides a directory of separate audio files and wants the same references and creative direction applied to each file.

```bash
bizmuse mv batch \
  --dir "./songs" \
  --image "artist.jpg" "stage.jpg" \
  --prompt "Live performance with cinematic lighting and energetic camera movement" \
  --ratio 16:9 \
  --resolution 720p \
  --content-mode singing \
  --concurrency 2 \
  --output "./bizmuse-output" \
  --json
```

Concurrency must be between 1 and 5. Return the manifest path, submitted task IDs, and any per-file failures. Inspect each task independently before reporting completed media.

## Result Contract

Return a concise result in the user's preferred language:

- Task ID.
- Current or final status.
- Video URL when available.
- Cover URL when available.
- Download paths when requested.
- Batch manifest path and per-file failures when applicable.
- Actionable provider or account error without exposing credentials.

If a task is still running after 30 minutes, stop polling and return the task ID with a command the user can run later. Never invent a successful result or media URL.

## Cost and Privacy

BizMuse is an external paid service. Generation consumes account credits based on the selected output and source duration; current plans are listed at [bizmuse.ai/pricing](https://bizmuse.ai/pricing).

Audio, reference images, prompts, and generated media are sent to BizMuse to perform the requested generation. Confirm the user has the right to upload and process all supplied media. Do not upload unrelated files or private material that is not required for the requested video.

## Troubleshooting

- Read [references/setup.md](references/setup.md) for installation, authentication, and input requirements.
- Read [references/models.md](references/models.md) for the exact model and CLI controls exposed by this skill.
- Read [references/errors.md](references/errors.md) before retrying failed authentication, billing, upload, or provider operations.

- Product: [bizmuse.ai](https://bizmuse.ai)
- Documentation: [bizmuse.ai/skill](https://bizmuse.ai/skill)
- Source: [github.com/BizMuse-AI/skills](https://github.com/BizMuse-AI/skills)
