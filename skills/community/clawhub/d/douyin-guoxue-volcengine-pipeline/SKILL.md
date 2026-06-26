---
name: douyin-guoxue-volcengine-pipeline
description: Create and publish Chinese metaphysics / guoxue / I Ching short videos for Douyin using a verified multi-shot pipeline: Volcengine image generation + Volcengine video generation + Edge TTS dubbing + ffmpeg stitching + Douyin publish + backend verification. Use when the user wants 国学/易经/卦象/乾卦/坤卦/泰卦 style short videos, especially when they want 3-second shot changes instead of a single looping shot, AI-assisted visual generation, or a reusable Douyin production workflow. 中文：用于抖音国学/易经/卦象短视频的多镜头生产发布流程，包含火山文生图、火山图生视频、Edge TTS 配音、ffmpeg 合成、抖音发布和后台回查。适用于“做一条乾卦/坤卦/泰卦视频”“3秒换镜头”“国学短视频自动生成并发布”等请求。
---

# douyin-guoxue-volcengine-pipeline

Use this skill to run a **production-tested Douyin guoxue pipeline**.

## Core workflow

1. Load Volcengine env from `C:\Users\Lenovo\.openclaw\workspace\.volcengine_config`
2. Generate **3 vertical keyframes** with `volcengine-image-studio`
3. Turn each keyframe into a **5s motion shot** with `volcengine-video-studio`
4. Stitch 3 shots into a ~15s vertical cut with `ffmpeg`
5. Generate Chinese voiceover with `edge-tts`
6. Mix voice + BGM + subtitles
7. Publish through `skills/douyin-publisher/scripts/publish.py`
8. Verify in Douyin creator backend after publish

## Hard rules

- Do **not** use a single still image as the full video when the user wants a stronger result
- Prefer **3 shots**; use about **3-5s per shot**
- Always keep output **9:16 vertical**
- Always do a **backend verification** after publish; do not trust script success text alone
- When publishing AI-generated work, use the publish flow that goes through:
  - `发文助手`
  - `自主声明`
  - `添加声明`
  - `内容由AI生成`

## Current validated local components

- Volcengine image script: `skills/volcengine-image-studio/scripts/generate_image.py`
- Volcengine video script: `skills/volcengine-video-studio/scripts/generate_video.py`
- Douyin publish script: `skills/douyin-publisher/scripts/publish.py`
- Volcengine env file: `.volcengine_config`
- Typical BGM asset: `generated/guoxue-douyin/final-cuts/guofeng-lite-bgm.wav`

## Fast execution pattern

### 1. Load config into current process

PowerShell:

```powershell
$cfg = Get-Content .\.volcengine_config
foreach($line in $cfg){ if($line -match '^\s*([A-Z0-9_]+)=(.*)$'){ [Environment]::SetEnvironmentVariable($matches[1], $matches[2], 'Process') } }
[Environment]::SetEnvironmentVariable('VOLCENGINE_VIDEO_MODEL','doubao-seedance-1-0-pro-fast-251015','Process')
```

### 2. Generate 3 keyframes

Use thematic prompts for shot 1 / shot 2 / shot 3. Keep style consistent:
- Song-dynasty aesthetics
- Eastern negative space
- cinematic light
- no cartoon
- no modern city unless requested

### 3. Generate 3 motion shots

For each generated keyframe:

```powershell
py -3.11 .\skills\volcengine-video-studio\scripts\generate_video.py "<motion prompt>" --image <cover> --ratio 9:16 --duration 5 --download-dir <dir>
```

### 4. Voiceover

```powershell
edge-tts --voice zh-CN-XiaoxiaoNeural --file <script.txt> --write-media <voice.mp3>
```

Recommended voices:
- `zh-CN-XiaoxiaoNeural` — warm / calm / female
- `zh-CN-YunxiNeural` — male / composed / explanatory

### 5. Final assembly

Use ffmpeg to:
- trim each shot to ~4.8-4.9s
- concat 3 shots
- burn title / line subtitles
- mix voice + low-volume BGM

### 6. Publish and verify

Publish with `py -3.11 skills/douyin-publisher/scripts/publish.py ...`

Then **must** open creator manage page and confirm the new item appears in the list.

## Suggested directory pattern

Store runs under:

```text
generated/guoxue-douyin/<theme>-volcengine/
```

Example themes:
- `qian-gua-volcengine`
- `kun-gua-volcengine`
- `tai-gua-volcengine`

## Read next when needed

- For prompt structure and reusable shot patterns, read `references/prompt-patterns.md`
- For publishing / verification / AI declaration notes, read `references/publish-notes.md`
