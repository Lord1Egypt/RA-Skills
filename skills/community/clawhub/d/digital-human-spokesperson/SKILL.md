---
name: digital-human-spokesperson
version: 1.1.0
display_name: 双语口播数字人
display_name_en: Bilingual Digital Human Spokesperson
description: "生成双语口播视频——数字人先用英文讲稿、再自动切换成阿拉伯语口播。用户只需喂一段英文文案（也可直接提供阿拉伯语或让技能自动翻译），技能自动生成数字人形象、生成英/阿双语配音与字幕，并合成一段单一口播视频。"
description_zh: "生成双语口播视频——数字人先用英文讲稿、再自动切换成阿拉伯语口播。你只需喂一段英文文案，技能会自动生成数字人形象、将文案翻译为阿拉伯语、用免费 edge-tts 生成英/阿双语配音，并通过本地 SadTalker 做真人口型同步，最后用 ffmpeg 合成「英文段+阿语段」的单一口播视频（带双语字幕与标题卡）。适用于跨境电商、教育、宣发等需要英阿双语宣讲的场景。触发词：口播视频、数字人口播、英文转阿拉伯语、双语宣讲、spokesperson、talking-head。"
description_en: "Generate a bilingual talking-head (spokesperson) video: a digital human delivers the script in English first, then automatically switches to Arabic. Feed it English copy and the skill auto-generates the avatar, translates to Arabic, synthesizes EN/AR voiceover via free edge-tts, performs true lip-sync with local SadTalker, and composes a single video (EN segment plus AR segment) with bilingual subtitles and title cards. Ideal for cross-border e-commerce, education, and promotional content needing English-Arabic delivery. Triggers: 口播视频, 数字人口播, English to Arabic video, spokesperson, talking-head."
agent_created: true
license: MIT-0
---

# Digital Human Spokesperson（双语口播数字人）

## Overview

Generate a bilingual talking-head (口播) video: a digital-human presenter delivers the
script in English first, then automatically switches to Arabic. The user only needs to
supply the copy (文案). The skill handles avatar generation, optional EN→AR translation,
dual-language TTS, lip-synced talking-head rendering, and final composition into one video.

## When to Use

- User asks for a 口播视频 / 数字人口播 / spokesperson video / talking-head video.
- User wants English content that also exists in Arabic ("英文转阿拉伯语视频", "自动变成阿拉伯语").
- User says "feed it the script and get a bilingual video".
- Trigger phrases: 口播视频, 数字人口播, 英文转阿拉伯语, 双语宣讲, English to Arabic video,
  spokesperson, talking-head.

## Inputs

Minimal required: a block of English copy (the 文案).

Optional inputs the user may provide:
- Arabic copy (if provided, skip translation in Step 2).
- Avatar description / style (ethnicity, clothing, studio look). Default in assets/avatar_prompt.txt.
- Voice preferences (defaults: en-US-AriaNeural, ar-EG-SalmaNeural).
- Aspect ratio: default 16:9. For TikTok/Reels/Shorts use 9:16 — ask if unclear.

If the user only supplies English, auto-translate to Arabic in Step 2.

## Workflow

### Step 1 — Generate the digital-human avatar

Use the ImageGen tool with the prompt from `assets/avatar_prompt.txt` (customize
ethnicity/clothing from any user preference). Aim for a clean, front-facing, half-body
studio presenter on a neutral background — this renders best for talking-head lip-sync.
Save the image as `avatar.png` in the working directory.

### Step 2 — Prepare bilingual copy

- If the user supplied only English: translate to fluent Modern Standard Arabic (MSA).
  Preserve meaning and tone; do not add marketing fluff.
- If the user supplied both languages: use as-is.
- Store `en.txt` and `ar.txt` (plain text). Group into sentence lines — line grouping
  improves subtitle timing in Step 5.

### Step 3 — TTS (English + Arabic)

Run `scripts/tts_edge.py` (free `edge-tts`, no API key required):

```bash
python scripts/tts_edge.py --text en.txt --lang en-US --voice en-US-AriaNeural --out en.mp3
python scripts/tts_edge.py --text ar.txt --lang ar-EG --voice ar-EG-SalmaNeural --out ar.mp3
```

The script also prints the spoken duration, needed for subtitle timing. If `edge-tts` is
missing, install it in the managed venv: `pip install edge-tts`.

### Step 4 — Lip-sync talking-head video

Run `scripts/talking_head.py` to render `avatar.png` driven by each audio file:

```bash
python scripts/talking_head.py --image avatar.png --audio en.mp3 --out en_talk.mp4 --engine sadtalker
python scripts/talking_head.py --image avatar.png --audio ar.mp3 --out ar_talk.mp4 --engine sadtalker
```

Engine selection (priority order):
1. `sadtalker` — local, true lip-sync. First run auto-guides install (PyTorch + SadTalker
   repo, several GB; GPU recommended, CPU works but slow). See references/pipeline.md.
2. `did` / `heygen` — cloud, true lip-sync. Set `DID_API_KEY` or `HEYGEN_API_KEY` env var.
3. `fallback` (no engine) — if neither is available, use the VideoGen image-to-video tool to
   generate a "speaking presenter" clip from `avatar.png`, then overlay the audio with
   ffmpeg (see references/pipeline.md). This is NOT precise lip-sync — tell the user clearly
   and offer to upgrade to SadTalker / D-ID later.

Always report which engine was used and whether lip-sync is true or approximate.

### Step 5 — Compose the bilingual single video

Run `scripts/compose_bilingual.py` to concatenate the EN and AR clips, burn bilingual
subtitles, and add EN/AR title cards:

```bash
python scripts/compose_bilingual.py \
  --en en_talk.mp4 --ar ar_talk.mp4 \
  --en-text en.txt --ar-text ar.txt \
  --en-label "English" --ar-label "العربية" \
  --out bilingual_final.mp4
```

The script builds `.srt` subtitles from the text + audio durations, burns them, and
prefixes each segment with a labeled title card. Requires `ffmpeg` on PATH (uses the
subtitles filter). If ffmpeg is missing, install it or pass `--ffmpeg <path>`.

**AI content labels are ON by default** (mandatory under 《人工智能生成合成内容标识
办法》, effective 2025-09-01, and required for WorkBuddy open-platform review under the
「深度合成 > AI创作」service category):
- 显式 (explicit): a persistent "AI 生成" corner watermark on every segment + a
  bilingual end notice card ("本视频由 AI 生成" / "AI-Generated Content").
- 隐式 (implicit): MP4 metadata (`comment` / `description`) marking the file as
  AI-generated synthetic content.

A CJK font is auto-detected for the Chinese glyphs (override: `--cjk-fontfile`).
Customize texts via `--ai-label` / `--ai-notice` / `--ai-notice-en`; disable with
`--no-ai-label` (only for internal tests — do NOT disable for public distribution).

### Step 6 — Deliver

Present `bilingual_final.mp4` to the user via `present_files`. Summarize: avatar used,
whether translation was auto, TTS voices, lip-sync engine, and total duration.

## Notes

- Aspect ratio: default 16:9. For short-form platforms, ask and switch to 9:16
  (regenerate avatar as portrait or crop in compose).
- True lip-sync needs SadTalker (local, heavy) or D-ID / HeyGen (paid API). The VideoGen
  fallback produces a presenter clip + voiceover without precise mouth sync.
- Keep the working directory tidy: `en.txt`/`ar.txt`, `en.mp3`/`ar.mp3`, `avatar.png`,
  `en_talk.mp4`/`ar_talk.mp4`, `bilingual_final.mp4`.
- **Compliance**: output videos carry mandatory AI-content labels (corner watermark +
  end notice card + MP4 metadata). Never remove them for public distribution — they are
  legally required and double as qualification evidence when submitting this skill to
  the WorkBuddy open platform under the 「深度合成 > AI创作」category (that category
  additionally requires enterprise certification + algorithm filing 备案).

## Resources

- `scripts/tts_edge.py` — EN/AR text-to-speech via edge-tts.
- `scripts/talking_head.py` — avatar + audio → talking-head video (SadTalker / D-ID / HeyGen / fallback).
- `scripts/compose_bilingual.py` — ffmpeg concat + bilingual subtitle burn + title cards.
- `references/pipeline.md` — detailed pipeline, API key setup, SadTalker install, VideoGen
  fallback, troubleshooting.
- `assets/avatar_prompt.txt` — default digital-human ImageGen prompt template.
