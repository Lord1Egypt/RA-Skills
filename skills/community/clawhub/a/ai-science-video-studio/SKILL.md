---
name: ai-science-video-studio
description: "AI科普视频全流程自动化制作技能。将数字人形象（Google Flow / SadTalker）、AI语音克隆（F5-TTS MLX）、Pillow内容幻灯片、逐字卡拉OK字幕（Pillow + FFmpeg）、以及专业级音视频QA整合为8阶段自动化流水线。覆盖：脚本策划 → 数字人生成 → TTS语音克隆 → 幻灯片渲染 → 字幕渲染 → 音频修复 → 最终合成（FFmpeg xfade + acrossfade + alimiter）→ 专业QA审查。触发词：AI科普视频、制作科普视频、做个AI讲解视频、生成科技短视频。**推荐硬件：Mac mini M系列 16GB内存**，利用Apple Silicon MLX加速语音克隆和本地渲染。"
agent_created: true
---

# AI Science Video Studio — AI科普视频自动化制作技能

## Overview

Full pipeline for producing explainer / educational videos that combine a digital human
avatar (intro/outro) with animated content slides (body), voice-narrated by a cloned
personal voice (F5-TTS MLX), with karaoke-style subtitles throughout.

The pipeline follows an 8-stage workflow:

```
Script Planning → Digital Human → TTS Voice → Content Slides
    → Subtitles → Audio Repair → Final Compositing → QA Review
```

Default configuration is tuned for 1280×720 (16:9), 24fps, CRF 20 encoding, a single
presenter avatar, and Mandarin Chinese narration. All parameters are adjustable.

---

## When to Use This Skill

Trigger on any of the following intents:

- User asks to create an "AI科普" (AI science explainer) video
- User wants an educational/explainer video with digital human + slides format
- User mentions combining a talking avatar with content slides
- User needs the full pipeline: script → voice clone → slides → subtitles → compositing
- User says "做一个讲解视频", "生成科普视频", "制作AI讲解类视频"

Do NOT use this skill for:
- Pure short films / drama without educational content → use `ai-short-film-studio`
- Only SadTalker PiP compositing without slides → use `sadtalker-pip-compositing`
- Only Google Flow video generation → use `google-flow-automation`

---

## Pipeline Stages

### Stage 1: Script Planning

Create a `script.json` file defining the video structure with exactly 5 paragraphs:

```json
{
  "intro":      { "type": "digital_human", "engine": "google_flow", "duration": 10, "narration": "开场旁白...", "flow_prompt": "..." },
  "content_1":  { "type": "slides",        "engine": "pillow",      "duration": 30, "narration": "正文第一段旁白..." },
  "content_2":  { "type": "slides",        "engine": "pillow",      "duration": 25, "narration": "正文第二段旁白..." },
  "content_3":  { "type": "slides",        "engine": "pillow",      "duration": 29, "narration": "正文第三段旁白..." },
  "outro":      { "type": "digital_human", "engine": "google_flow", "duration": 10, "narration": "结尾旁白...", "flow_prompt": "..." }
}
```

**Rules:**
- intro and outro use `digital_human` type (talking avatar)
- content segments use `slides` type (animated content screens)
- Each segment must specify: type, engine, duration (seconds), narration text
- Narration text should be ≤15 seconds worth of speech per segment (~60 Chinese characters)
- Duration field is the target video length (not TTS length — TTS naturally sets the pace)

For detailed script format specification, see `references/script_format.md`.

---

### Stage 2: Digital Human Generation (Intro & Outro)

Two approaches are available. Prefer Google Flow for standalone talking-head segments;
use SadTalker for picture-in-picture overlay on content slides.

#### Option A: Google Flow CDP Automation

Use the `google-flow-automation` skill to generate intro/outro videos:

1. Launch Chrome with remote debugging on port 9222
2. Navigate to labs.google/fx/tools/flow
3. Upload avatar reference image
4. Enter the Chinese prompt from script.json
5. Wait ~3-5 minutes for 10-second video generation
6. Download as `intro.mp4` and `outro.mp4`

**Key parameters:**
- Avatar: upload the user's preferred reference image (portrait photo)
- Prompt: in Chinese, describe the scene and delivery style
- Model: Omni Flash, 16:9 aspect ratio, 10s duration
- Account: the user's Google account credentials (handled by Chrome profile)

#### Option B: SadTalker MPS (for PiP on content)

Use the `sadtalker-pip-compositing` skill when the digital human should appear as a
circular picture-in-picture overlay on content slides.

**Steps:**
1. Run `scripts/fix_sadtalker_numpy.py` for numpy 2.x compatibility
2. Extract avatar image + TTS audio
3. Run SadTalker 3-stage inference with `device='mps'`
4. Create circular mask (120×120) with PIL
5. FFmpeg overlay onto content at bottom-left corner

**PiP Parameters:**
| Parameter | Value |
|-----------|-------|
| Size | 120×120 (final) |
| Position | bottom-left, 20px margin |
| Mask | PIL circular, radius 60px |
| Overlay | `overlay=20:H-h-20:shortest=1` |

---

### Stage 3: Voice Generation (TTS)

#### Primary: F5-TTS MLX Voice Cloning

Use F5-TTS MLX on Apple Silicon for personal voice cloning:

```python
from f5_tts_mlx.generate import generate

# For content narration (MUST use estimate_duration=True!)
audio = generate(
    text="旁白文本...",
    ref_audio_path="/path/to/ref_voice.mp3",
    ref_audio_text="参考音频的文本内容",
    steps=64,
    cfg_strength=2.5,
    speed=1.0,
    estimate_duration=True,  # CRITICAL for Chinese!
)
```

**CRITICAL — `estimate_duration=True`:**
Without this parameter, F5-TTS generates extremely short audio for Chinese text
(0.5-0.9 seconds per sentence). With it, the model estimates target duration and
generates properly-length audio.

**Parameter table:**
| Parameter | Intro/Outro | Content |
|-----------|-------------|---------|
| steps | 64 | 64 |
| cfg_strength | 2.5 | 2.5 |
| speed | 0.45 | 1.0 |
| estimate_duration | No | **Yes** (critical!) |

**Post-processing:**
After generation, compute the actual-vs-target duration ratio and apply `atempo`
to fine-tune timing:

```bash
# Example: actual 11.98s, target 10.0s → atempo=1.198
ffmpeg -i generated.wav -filter:a "atempo=1.198" output.wav
```

#### Fallback: edge-tts

When F5-TTS is unavailable or produces garbled output:

```bash
edge-tts --voice zh-CN-YunxiNeural --text "旁白文本" --write-media output.wav
```

**Voice selection:**
| Purpose | Voice |
|---------|-------|
| Content narration (male) | zh-CN-YunxiNeural |
| Patch/correction (female) | zh-CN-XiaoxiaoNeural |

---

### Stage 4: Content Slide Rendering

Render animated content slides using Pillow frame-by-frame rendering + FFmpeg pipe.

Use `scripts/render_slides.py` as the template. The script should:

1. Accept narration text split into lines
2. Render each frame with progressively "typed" text (one new line per frame)
3. Use terminal/IDE aesthetic: dark background (#1a1a2e), green/white text, monospace font
4. Output 1280×720, 24fps PNG frames via FFmpeg pipe
5. Sync frame count to the TTS audio duration

**Key rendering parameters:**
- Resolution: 1280×720
- Frame rate: 24fps
- Background: dark (#1a1a2e or pure black for terminal look)
- Text: green (#00ff41) for code, white for explanatory text
- Font: SF Mono or Menlo for code sections; STHeiti for Chinese text

The script is at `scripts/render_slides.py`. Customize the content per video topic
while keeping the rendering engine intact.

---

### Stage 5: Subtitle Rendering

Generate karaoke-style subtitles as transparent PNG frames overlayed on the final video.

The process:
```
Audio (.wav)
  → Whisper small/medium transcription
  → Word-level timestamps (segments + words)
  → Text correction mapping (fix Whisper mis-transcriptions)
  → Pillow frame-by-frame PNG rendering (transparent BG)
  → FFmpeg overlay onto video
```

Use `scripts/render_subtitles.py` as the rendering engine.

**Subtitle style specification (intro and outro MUST match):**
| Property | Value |
|----------|-------|
| Font | STHeiti Medium (macOS: `/System/Library/Fonts/STHeiti Medium.ttc`) |
| Size | 44px |
| Spoken text color | Orange (#FF6B2B) |
| Unspoken text color | White (#FFFFFF) |
| Outline | 2px black |
| Background bar | Semi-transparent black `rgba(0,0,0,160)` |
| Display mode | Per-sentence (each sentence appears and disappears independently) |
| Highlight mode | Word-by-word (karaoke-style progressive highlight) |

**Text correction mapping:**
Always maintain a correction dictionary to fix Whisper mis-transcriptions of
technical terms and proper names:

```python
corrections = {
    "材领": "才林",
    "Anthropy": "Anthropic",
    "Cloud Code": "Claude Code",
}
```

**CRITICAL — Consistency rule:** Intro and outro subtitles MUST use the exact
same rendering engine (Pillow) with identical style properties. Never mix Pillow
and ASS/other formats — FFmpeg on macOS lacks libass support.

---

### Stage 6: Audio Repair

Common audio issues and their fixes. Run `scripts/audio_analyzer.py` for automated
detection before proceeding.

| Issue | Symptom | Root Cause | Fix |
|-------|---------|------------|-----|
| Right channel dropout | Crunching noise at specific timestamps | Source right channel flickers 20+ times | `channelmap=FL-FL|FL-FR` (duplicate L→R) |
| Silence gaps | Sudden "click" in music | AI-generated BGM has gaps (100-400ms) | 250ms fade-out/in at each gap boundary |
| Audio truncation | Sound stops abruptly | Segment extracted from wrong time range | Use original source file, re-extract |
| Channel mismatch | Concat fails or silent segments | Mono vs stereo mismatch | Unify all to 48000Hz stereo |
| Clipping | Peak near 32768 (16-bit max) | Volume stacking at concatenation points | `alimiter` with `limit=-0.9dB` |
| TTS mispronunciation | Garbled Chinese characters | TTS engine multi-phoneme errors | Re-generate with F5-TTS or edge-tts patch |

**Channel fix command:**
```bash
ffmpeg -i input.wav -af "channelmap=map=FL-FL|FL-FR" -ar 48000 -ac 2 output.wav
```

**Gap smoothing approach:**
For each audio gap >80ms detected by `scripts/audio_analyzer.py`:
```bash
# Split at gap, apply fade-out/fade-in, re-concatenate
ffmpeg -i audio.wav -af "afade=t=out:st=GAP_START-0.25:d=0.25,afade=t=in:st=GAP_END:d=0.25" patched.wav
```

---

### Stage 7: Final Compositing

Assemble all segments with professional transitions using FFmpeg.

**Compositing order:**
```
intro.mp4 → content_1.mp4 → content_2.mp4 → content_3.mp4 → outro.mp4
```

Use `scripts/compose_final.py` for automated assembly.

**Encoding parameters:**
| Parameter | Value | Rationale |
|-----------|-------|-----------|
| Codec | libx264 | Maximum compatibility |
| Resolution | 1280×720 | 16:9 standard |
| Frame rate | 24fps | Cinematic feel |
| Rate control | CRF 20 | High-quality unified encoding |
| Pixel format | yuv420p | Universal compatibility |
| Audio codec | AAC 192kbps | 48000Hz stereo |
| Limiter | alimiter limit=-0.9dB | Prevent clipping |

**Transition effects:**
- Video: `xfade=transition=fade:duration=0.5:offset=<time>` (cross-fade, eliminates hard cuts)
- Audio: `acrossfade=d=0.5:curve=tri` (triangular cross-fade, smooth audio joins)

**Pre-compositing checklist:**
1. All segments re-encoded to CRF 20 (unified quality)
2. All audio normalized to 48000Hz stereo
3. Subtitle overlays applied to each segment
4. Transitions prepared: 0.5s offset for each segment boundary

---

### Stage 8: Professional QA Review

Run a systematic quality review before delivering the final video.

**QA dimensions and inspection methods:**
| Dimension | Check | Method |
|-----------|-------|--------|
| Video transitions | Hard cuts at boundaries? | Extract transition zone, frame-by-frame review |
| Video encoding | Consistent bitrate across segments? | `ffprobe` bitrate check |
| Audio artifacts | Noise, pops, silence gaps? | Second-by-second mean/peak analysis |
| Audio joins | Smooth at concatenation points? | Acrossfade spectral analysis |
| Audio clipping | Peaks near 32768? | Peak detection (>32000 = danger) |
| Subtitle sync | Subtitles aligned with speech? | Whisper word-level timestamp verification |
| Subtitle consistency | Intro and outro styles match? | Visual comparison of 7 style properties |
| Pronunciation | Chinese pronunciation accurate? | Whisper transcription cross-validation |

**Verification commands:**
```bash
# Audio per-second analysis
python3 scripts/audio_analyzer.py output.mp4

# Video quality check
ffprobe -v error -select_streams v:0 \
  -show_entries stream=codec_name,width,height,r_frame_rate,bit_rate \
  output.mp4

# Subtitle sync verification
whisper model small --language zh output.mp4
```

For the complete QA checklist, see `references/qa_checklist.md`.

---

## File Naming Convention

```
AI科普第{N}期_{主题}_v{N}.mp4
```

Example: `AI科普第一期_SadTalker画中画_v11.mp4`

**Intermediate files:**
| File | Purpose |
|------|---------|
| `content_video.mp4` / `content_with_pip_v{N}.mp4` | Content with optional PiP |
| `sadtalker_output.mp4` / `intro.mp4` / `outro.mp4` | Digital human outputs |
| `content_audio.wav` / `ref_audio_24k.wav` | Audio files |
| `subs_s{N}/frame_{N}.png` | Subtitle frames |
| `build_v{N}.py` / `build_v{N}_fixed.py` | Build scripts |
| `merge_final.sh` / `concat_v{N}.txt` | Merge scripts |

---

## Quality Targets

| Metric | Target |
|--------|--------|
| Video resolution | 1280×720 (16:9) |
| Frame rate | 24fps |
| Video bitrate | CRF 20 (~200-400 kbps) |
| Audio sample rate | 48000Hz stereo |
| Audio bitrate | AAC 192kbps |
| Audio peak | < -0.9dB (no clipping) |
| Segment transition | 0.5s xfade + acrossfade |
| Subtitle alignment | Whisper word-level timestamps |

---

## Critical Pitfalls

For the complete pitfalls reference, see `references/pitfalls.md`. Key highlights:

1. **F5-TTS Chinese too short**: Always set `estimate_duration=True` for Chinese content narration. Without it, audio is only 0.5-0.9s per sentence.

2. **Alpha channel compositing**: When using `alphamerge`, the human RGBA video is the color source (first input), and the circular mask PNG is the alpha (second input). Reversing them produces a white circle with no human visible.

3. **Concat format mismatch**: Different segments may have different sample rates (16000 vs 48000Hz) or channel counts (mono vs stereo). Unify all segments to 48000Hz stereo before concatenation.

4. **Subtitle rendering engine inconsistency**: Always use Pillow for both intro and outro subtitles. FFmpeg on macOS lacks libass, making ASS-subtitle filters unavailable.

5. **AI-generated BGM gaps**: Google Flow's AI-generated background music may contain silence gaps (100-400ms). Smooth them with 250ms crossfades at each gap boundary.

---

## Bundled Resources

### Scripts

- `scripts/render_slides.py` — Pillow-based content slide frame renderer (1280×720, dark IDE theme, progressive text reveal)
- `scripts/render_subtitles.py` — Karaoke-style subtitle PNG renderer (word-by-word orange highlight, transparent BG, STHeiti 44px)
- `scripts/compose_final.py` — End-to-end FFmpeg compositing (xfade + acrossfade + alimiter + CRF20 unified encoding)
- `scripts/audio_analyzer.py` — Audio QA analysis tool (second-by-second mean/peak detection, gap finder, clipping detector)

### References

- `references/script_format.md` — Complete script.json format specification and examples
- `references/qa_checklist.md` — Detailed 8-dimension QA review checklist
- `references/pitfalls.md` — Comprehensive list of known pitfalls with root causes and fixes
