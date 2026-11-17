---
name: "article-to-video"
version: "1.0.0"
description: "Converts articles (docx/pdf/txt/md) to narrated videos with AI-generated visuals and TTS voiceover. Invoke when user asks to convert article/document to video, mentions 文章转视频, or needs text-to-video with narration."
author: "unique-memory"
homepage: "https://github.com/unique-memory/article-to-video"
---

# Article to Video

Convert articles in Word (.docx), PDF (.pdf), Text (.txt), or Markdown (.md) format into narrated videos with AI-generated visuals, TTS voiceover, subtitles, background music, and scene transitions.

## When to Use

- User says "把这篇文章转为视频" / "convert this article to video"
- User uploads a .docx/.pdf/.txt/.md file and wants a video version
- User mentions "文章转视频" / "article to video" / "文字转视频"
- User wants to create a narrated video from a document with voiceover

## Workflow Overview

The pipeline has 5 stages, each handled by a dedicated Python script:

```
[Document] → ① parse_doc.py → scenes.json
                              ↓
                   ② generate_tts.py → audio + timing.json
                              ↓
              ③ create_slides.py (or GenerateImage) → images
                              ↓
                ④ assemble_video.py → final MP4 + SRT
                              ↓
                         ⑤ Output: video.mp4 + subtitle.srt
```

## Stage 1: Document Parsing (`scripts/parse_doc.py`)

Parses the input document into a structured JSON of scenes.

**Supported formats:**
- `.docx` → `python-docx` (paragraphs with heading levels)
- `.pdf` → `pdfplumber` (page-by-page text extraction, table detection)
- `.txt` → direct read, split by blank lines
- `.md` → `markdown` library, preserve heading hierarchy

**Output format (`scenes.json`):**
```json
{
  "title": "Article Title",
  "scenes": [
    {
      "index": 0,
      "heading": "Section Title",
      "level": 1,
      "narration": "Clean text suitable for TTS reading...",
      "slide_text": "Key points for visual display...",
      "image_prompt": "Description for AI image generation...",
      "char_count": 250
    }
  ],
  "total_chars": 5000,
  "estimated_duration_sec": 1000
}
```

**Usage:**
```bash
python scripts/parse_doc.py --input article.docx --output scenes.json
```

**Key logic:**
- Split by headings (H1/H2) into scenes
- For each scene: extract narration text (clean markdown/HTML), generate slide text (key points), create image prompt
- Estimate duration: Chinese ~4.5 chars/sec, English ~2.8 words/sec
- Handle complex content: tables → text summary, code blocks → formatted text, formulas → description

**Content type auto-detection:**
The parser automatically detects the document's content type using keyword analysis, and stores it in `scenes.json` as `content_type`. This drives visual style and BGM selection in later stages.

| Content Type | Description | Auto Theme | Ken Burns |
|---|---|---|---|
| `finance` | 金融/投资报告 | ocean (deep blue + gold) | slow |
| `business` | 商业/管理 | default (purple) | normal |
| `technology` | 科技/IT | dark (black + cyan) | fast |
| `science` | 科学/研究 | ocean (deep blue) | slow |
| `education` | 教育/教程 | warm (dark + orange) | normal |
| `news` | 新闻/资讯 | light (white + red) | fast |
| `lifestyle` | 生活/随笔 | warm (dark + orange) | normal |
| `default` | 通用 | default | normal |

Override with `--content-type technology`.

## Stage 2: TTS Generation (`scripts/generate_tts.py`)

Converts narration text to speech with retry and fallback.

**Primary engine:** `edge-tts` (free, high quality, multi-voice Chinese support)
**Fallback chain:** edge-tts → gTTS → pyttsx3 (offline)

**Key features:**
- Retry with exponential backoff on 429 rate limit (2^n seconds, max 3 retries)
- 1-3 second delay between scenes to avoid throttling
- Precise duration measurement via `ffprobe`/`ffmpeg -i` after generation
- Caching: text SHA256 hash → skip regeneration if cached
- Output: `scene_NN.mp3` + `timing.json` (with actual measured durations)

**Voice Profiles (new):**
Use `--profile` to apply a preset combination of voice + rate + pitch + volume:

```bash
python scripts/generate_tts.py --scenes scenes.json --outdir ./audio --profile professional
```

| Profile | Voice | Rate | Pitch | Best For |
|---|---|---|---|---|
| `professional` | Yunyang (男声播音) | +0% | +0Hz | 商务报告、金融分析 |
| `casual` | Xiaoxiao (女声亲切) | +10% | +2Hz | 博客文章、生活分享 |
| `energetic` | Yunxi (男声活力) | +15% | +5Hz | 科技资讯、产品发布 |
| `documentary` | Yunjian (男声解说) | -5% | -2Hz | 历史人文、深度报道 |
| `warm` | Xiaoyi (女声温柔) | -5% | +0Hz | 教育课程、情感故事 |

**Available voices (Chinese):**
- `zh-CN-XiaoxiaoNeural` - 女声，亲切自然 (default)
- `zh-CN-YunxiNeural` - 男声，年轻活力
- `zh-CN-YunyangNeural` - 男声，专业播音
- `zh-CN-XiaoyiNeural` - 女声，温柔甜美
- `zh-CN-YunjianNeural` - 男声，体育解说

## Stage 3: Visual Generation (`scripts/create_slides.py`)

Two modes for generating scene visuals:

**Mode A - Template slides (default, fast):**
Renders HTML templates to PNG images using the built-in `slide.html` template.
- Title slides with gradient backgrounds
- Content slides with bullet points
- Quote/highlight slides
- Configurable color themes and fonts
- **Auto-selects theme based on content_type** (with optional `--theme` override)

**Mode B - AI image generation (optional, higher quality):**
Uses the `GenerateImage` tool or `Seedream` plugin to create custom illustrations.
- **Content-type-aware prompts**: Each scene's `image_prompt` is automatically adapted based on the detected content type (e.g. finance → financial infographic style, technology → futuristic cyberpunk aesthetic)
- In AI mode, the pipeline generates `ai_image_requests.json` — a manifest of all image generation requests with prompts, output paths, and dimensions
- Template slides are generated as fallback — if AI generation fails, the template slide remains
- The AI agent reads the manifest and calls GenerateImage for each request

**AI Image Style Mapping:**
| Content Type | Artistic Style | Color Mood |
|---|---|---|
| `finance` | Financial infographic, corporate | Deep blue + gold |
| `business` | Corporate illustration, minimalist | Purple + white |
| `technology` | Futuristic tech, digital cyberpunk | Dark + neon cyan/purple |
| `science` | Scientific illustration, precise | Deep blue + teal |
| `education` | Warm educational, friendly | Orange + soft blue |
| `news` | Editorial news, impactful | White + red/blue |
| `lifestyle` | Lifestyle photography, natural | Soft warm tones |

**Usage (template mode):**
```bash
python scripts/create_slides.py --scenes scenes.json --outdir ./slides --mode template
```

**Usage (AI mode):**
The skill instructions below describe how to use GenerateImage for this stage.

## Stage 4: Video Assembly (`scripts/assemble_video.py`)

Combines images + audio into final video using FFmpeg.

**Pipeline:**
1. For each scene: create video clip from image + audio (with Ken Burns zoom + pan effect)
2. Add crossfade transitions between scenes (xfade filter)
3. Mix background music with narration (amix filter, BGM at -15dB)
4. Burn subtitles into video (optional)
5. Concatenate all scene clips → final MP4

**Key features:**
- Ken Burns effect: `zoompan` filter with **zoom + pan** for cinematic camera movement. Pan direction (right/left/down/up) is deterministically selected per scene via filename hash, ensuring varied but reproducible movement. Pan range is configurable per speed preset (slow: 60px, normal: 80px, fast: 100px).
- **Ken Burns speed adapts to content type** (slow for finance, fast for tech)
- Scene transitions: `xfade` filter (fade, dissolve, slideleft)
- **BGM auto-selection**: picks BGM from `assets/bgm/<style>/` based on content type
- **BGM style override**: use `--bgm-style` to force a specific BGM style (e.g. `--bgm-style cinematic`)
- **Style-specific BGM volume**: each BGM style has its own volume level (e.g. corporate: -18dB, cinematic: -12dB)
- **Random selection**: when multiple audio files exist in a style directory, one is randomly selected
- Background music: `amix` with automatic ducking
- Subtitle burning: SRT → `subtitles` filter with Chinese font (FontSize=12, no background box, 20px from bottom)
- **Extended timeout**: FFmpeg operations use 1800s timeout for long videos (20+ min), with `fast` preset and CRF 24 for subtitle burning and concatenation
- Windows-safe: all temp files use ASCII-only short names
- Disk space check before starting
- Progress tracking via JSON file

**Usage:**
```bash
# BGM auto-selected based on content type (with style-specific volume)
python scripts/assemble_video.py \
  --slides ./slides \
  --audio ./audio \
  --timing ./audio/timing.json \
  --output final_video.mp4 \
  --resolution 1920x1080 \
  --transition fade

# Override BGM style (ignores content type mapping)
python scripts/assemble_video.py \
  --slides ./slides \
  --audio ./audio \
  --timing ./audio/timing.json \
  --output final_video.mp4 \
  --bgm-style cinematic \
  --resolution 1920x1080

# Or specify BGM file manually
python scripts/assemble_video.py \
  --slides ./slides \
  --audio ./audio \
  --timing ./audio/timing.json \
  --output final_video.mp4 \
  --bgm ./assets/bgm/corporate/track01.mp3 \
  --resolution 1920x1080
```

## BGM Library Management (`scripts/bgm_manager.py`)

Manage background music files in the `assets/bgm/<style>/` directory structure.

**BGM Styles:**
| Style | Directory | Volume | Best For |
|---|---|---|---|
| `corporate` | corporate/ | -18dB | 商务、金融、新闻 |
| `acoustic` | acoustic/ | -15dB | 生活、随笔 |
| `electronic` | electronic/ | -20dB | 科技、产品发布 |
| `cinematic` | cinematic/ | -12dB | 科学、纪录片 |
| `soft` | soft/ | -16dB | 教育、儿童 |

**Commands:**
```bash
# List all BGM files
python scripts/bgm_manager.py list

# List files in a specific style
python scripts/bgm_manager.py list --style corporate

# Upload (copy) audio file to a style directory
python scripts/bgm_manager.py upload --file music.mp3 --style corporate
python scripts/bgm_manager.py upload --file music.mp3 --style corporate --name track01

# Remove a BGM file
python scripts/bgm_manager.py remove --style corporate --file track01.mp3

# Validate an audio file before uploading
python scripts/bgm_manager.py validate --file music.mp3

# Show BGM configuration summary
python scripts/bgm_manager.py info
```

**Upload validation:**
- Supported formats: `.mp3`, `.m4a`, `.wav`
- Minimum file size: 10KB
- Minimum audio duration: 5 seconds (verified via ffprobe)
- ASCII-safe filenames (spaces replaced with underscores)

## Stage 5: Output

Final deliverables:
- `final_video.mp4` - The complete narrated video
- `subtitle.srt` - Subtitle file (also burned into video)
- `thumbnail.jpg` - Video thumbnail (first scene frame)

## Complete Usage Example

```bash
# Step 1: Parse document (auto-detects content type)
python scripts/parse_doc.py --input article.docx --output scenes.json
# Or manually specify: --content-type technology

# Step 2: Generate TTS audio (use voice profile or individual settings)
python scripts/generate_tts.py --scenes scenes.json --outdir ./audio --profile professional
# Or: --voice zh-CN-XiaoxiaoNeural --rate +0% --pitch +0Hz

# Step 3: Generate slide images (auto-selects theme from content type)
python scripts/create_slides.py --scenes scenes.json --outdir ./slides --mode template
# Or override: --theme dark

# Step 4: Assemble final video (auto-selects BGM from content type)
python scripts/assemble_video.py \
  --slides ./slides \
  --audio ./audio \
  --timing ./audio/timing.json \
  --output final_video.mp4 \
  --resolution 1920x1080
```

## Configuration

All defaults are in `scripts/config.py`. Key options:

| Option | Default | Description |
|--------|---------|-------------|
| `voice` | `zh-CN-XiaoxiaoNeural` | TTS voice |
| `--profile` | (none) | Voice profile preset (professional/casual/energetic/documentary/warm) |
| `--content-type` | auto | Override content type detection (finance/business/technology/...) |
| `--bgm-style` | auto | Override BGM style (corporate/acoustic/electronic/cinematic/soft) |
| `resolution` | `1920x1080` | Output video resolution |
| `transition` | `fade` | Scene transition type |
| `bgm_volume` | style-specific | Background music volume (per-style: corporate -18dB, cinematic -12dB, etc.) |
| `narration_volume` | `-3dB` | Narration volume |
| `ken_burns` | `True` | Enable Ken Burns zoom + pan effect |
| `ken_burns_speed` | auto | Ken Burns speed (slow/normal/fast) — auto from content type |
| `ken_burns_pan_range` | 60/80/100 | Pan range in pixels per speed (slow/normal/fast) |
| `bgm_auto_select` | `True` | Auto-select BGM from content type |
| `bgm_random` | `True` | Randomly select from multiple BGM files in style directory |
| `ai_image_size` | `landscape_16_9` | AI image generation size preset |
| `subtitle` | `True` | Burn subtitles into video |
| `subtitle_font` | `Microsoft YaHei` | Subtitle font family |
| `subtitle_font_size` | `12` | Subtitle font size (ASS FontSize) |
| `subtitle_border_style` | `1` | ASS BorderStyle (1=outline only, 3=background box) |
| `subtitle_margin_v` | `20` | Subtitle vertical margin from bottom (pixels) |
| `tts_delay` | `2.0` | Seconds between TTS calls (anti-throttle) |
| `tts_max_retries` | `3` | Max retry on 429 errors |

## Platform Presets

| Platform | Resolution | Aspect |
|----------|-----------|--------|
| YouTube/B站 | 1920x1080 | 16:9 |
| 抖音/TikTok | 1080x1920 | 9:16 |
| 小红书 | 1080x1440 | 3:4 |

## Important Notes

- **Windows paths**: All temp files use ASCII-only names (scene_001, scene_002...) to avoid FFmpeg/edge-tts path encoding issues
- **FFmpeg**: Uses `imageio-ffmpeg` which bundles a full FFmpeg binary with all codecs (PNG decode, H.264 encode, AAC/MP3 audio). No separate system FFmpeg installation required. The config auto-detects the bundled binary.
- **Chinese font**: Subtitle burning uses "Microsoft YaHei" font family (must be installed on system). Change in config if unavailable
- **Disk space**: Video generation needs ~5x document size in temp space. Script checks before starting
- **Long documents**: Documents >10,000 chars are split into batches. Each batch generates independently, then concatenated
- **Breakpoint resume**: Progress is saved to `progress.json`. Re-running skips completed scenes

## Error Handling

- TTS 429 → exponential backoff retry, then fallback to gTTS, then pyttsx3
- Image generation failure → fallback to template text card
- FFmpeg error → check disk space, temp file cleanup, retry once
- Document parse error → report format-specific error message with fix suggestion
