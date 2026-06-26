---
name: douyin-video-analysis
description: 抖音视频分析流水线：输入抖音链接后，自动/半自动抓取页面信息与音频、转写口播、总结内容、提取有用信息与对应证据、进行批判性思维分析，并把转写与分析结果写入 Obsidian。 / Analyze a Douyin video from a shared URL by extracting page metadata, capturing audio when possible, transcribing speech into readable text, summarizing content, extracting useful information plus evidence, applying critical analysis, and saving both transcript and analysis into Obsidian.
---

# Douyin Video Analysis

Use this skill when the user gives a Douyin video URL and wants:
- the real video topic/content extracted
- the title and hook analyzed
- audio downloaded from the page if possible
- audio transcribed into readable Chinese text
- critical thinking analysis of the script/content
- results saved into Obsidian notes

## Scope

This skill is for **analysis and note capture**, not reposting or bulk scraping.

## Inputs

Expected user input:
- a Douyin short URL or full video URL
- optional analysis focus, such as:
  - whether the copy is AI-generated
  - title strategy
  - persuasion methods
  - logical flaws / manipulation / exaggeration

## Output contract

Produce:
1. short status update in chat
2. transcript note in Obsidian
3. analysis note in Obsidian
4. final chat summary with note paths

## Workflow

### 1. Resolve the real video page
- Open the Douyin URL in Chrome if needed.
- Extract:
  - canonical video URL
  - title
  - description
  - account name
  - visible chapter points / page text
- Be explicit about what came from page metadata vs full transcript.

### 2. Extract media URLs if possible
- Prefer reading browser performance resources from the actual loaded page.
- Capture candidate audio/video stream URLs.
- If direct download gets 403, retry with browser-derived headers/cookies when available.
- Save temporary files under `/tmp/douyin_transcribe/`.

### 3. Transcribe audio
- Prefer a local/offline path.
- Current practical path on this machine:
  - Python venv in `/tmp/douyin_transcribe/venv`
  - `mlx-whisper`
- First pass:
  - use a smaller model to get a usable draft quickly
- If needed:
  - do a second pass or manual cleanup for readability
- Clearly label transcript status:
  - raw machine transcript
  - cleaned readable version
  - final polished version

### 4. Summarize before criticizing
Before any critical-thinking judgment, always do these two steps:

#### A. Content summary
- produce a concise summary of what the video actually says
- separate hook / core claim / support / conclusion
- avoid mixing your judgment into the summary

#### B. Useful information + evidence extraction
List the video's actually useful information and pair each item with the evidence the video itself provides.
For each item, give an initial confidence judgment:
- high
- medium
- low

This prevents the analysis from becoming pure attitude.

### 5. Analyze critically
Always cover, unless the user narrows scope:
- what the video is actually saying
- whether the title/hook exaggerates or distorts the case
- whether the script appears AI-generated / AI-assisted / human-written
- emotional triggers used
- hidden assumptions
- survivorship bias / overgeneralization / false lessons
- what is genuinely useful vs what is manipulative or shallow

### 6. Save into Obsidian
Default destination:
- transcript note → `OpenClaw/Inbox/YYYY-MM-DD 抖音视频口播转写 - <topic>.md`
- analysis note → `OpenClaw/Inbox/YYYY-MM-DD 抖音视频分析 - <topic>.md`

Include:
- source URL
- canonical URL
- account name if available
- what was directly obtained vs inferred
- transcript quality warning if imperfect

## Response rules

- Never pretend a full transcript was obtained if only page metadata was captured.
- If only metadata is available, say so plainly.
- Distinguish between:
  - page title/description analysis
  - full script analysis
- Prefer usefulness over theatrical certainty.

## Local implementation notes

### Useful browser path
- Probe browser bridge
- Use macOS Chrome bridge to:
  - open the page
  - evaluate page JS
  - inspect visible text
  - inspect `performance.getEntriesByType("resource")`

### Useful temporary files
- `/tmp/douyin_transcribe/audio*.mp4`
- `/tmp/douyin_transcribe/venv`

### Suggested helper scripts

#### A. Grab page and audio

```bash
python3 /Users/bobzhong/.openclaw/workspace/skills/douyin-video-analysis/helpers/douyin_grab.py '<douyin-url>'
```

It will:
- open the Douyin page in Chrome
- fetch page metadata from the loaded Chrome tab
- extract candidate media URLs
- attempt authenticated audio download via curl with copied headers/cookies
- return JSON containing canonical URL, title, body preview, audio URL, and local audio path

#### B. Transcribe and create notes

```bash
python3 /Users/bobzhong/.openclaw/workspace/skills/douyin-video-analysis/helpers/transcribe_and_note.py \
  --audio-file /tmp/douyin_transcribe/audio_latest.mp4 \
  --title '<video-title>' \
  --source-url '<shared-url>' \
  --page-url '<canonical-url>' \
  --account '<creator>' \
  --topic '<short-topic>'
```

It will:
- transcribe the local audio with `mlx-whisper`
- create a transcript note in Obsidian
- create an analysis-note skeleton in Obsidian
- return both note paths as JSON

## Limits

- Some videos may block direct media download.
- Machine transcripts may contain proper noun and number errors.
- Large-model transcription may be slow; start fast, then refine if needed.

## When done
Tell the user:
- whether transcript is metadata-only / rough transcript / cleaned transcript
- where the notes were saved
- whether further cleanup would materially improve the analysis
