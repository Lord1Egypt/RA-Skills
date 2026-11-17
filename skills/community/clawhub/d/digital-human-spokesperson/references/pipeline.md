# Bilingual Digital-Human Pipeline (reference)

Detailed notes for the `digital-human-spokesperson` skill. The SKILL.md is the
entry point; this file covers setup, API keys, fallback behavior, and troubleshooting.

## End-to-end pipeline

```
User copy (English)
   │
   ├─ Step 1  ImageGen  ──────────────► avatar.png  (digital-human still)
   ├─ Step 2  Translate EN → MSA AR ──► ar.txt
   ├─ Step 3  tts_edge.py (edge-tts) ─► en.mp3, ar.mp3  (+ .json durations)
   ├─ Step 4  talking_head.py         ─► en_talk.mp4, ar_talk.mp4
   └─ Step 5  compose_bilingual.py    ─► bilingual_final.mp4
```

## Step 1 — Avatar (ImageGen)

Use the prompt in `assets/avatar_prompt.txt`. For best talking-head results:
- Front-facing, eyes on camera, neutral/blurred studio background.
- Half-body (head + shoulders), even lighting, no extreme angles.
- Avoid heavy accessories, hats, or hands covering the face (SadTalker crops to face).

If the user wants a specific look (ethnicity, clothing, gender), edit the prompt.

## Step 2 — Translation

When only English is supplied, translate to Modern Standard Arabic (MSA). Keep
register appropriate for a spokesperson (clear, professional). Do not invent claims.

## Step 3 — TTS (edge-tts)

- Free, no API key. Installs in the managed venv: `pip install edge-tts`.
- Default voices: `en-US-AriaNeural`, `ar-EG-SalmaNeural`.
- Other good Arabic voices: `ar-SA-ZariyahNeural`, `ar-AE-FatimaNeural`.
- The script writes a `<name>.json` sidecar with `duration` (via ffprobe). If
  ffprobe is absent the duration is `null`; `compose_bilingual.py` then falls back
  to even splitting, which is acceptable.

## Step 4 — Lip-sync engine

### A. SadTalker (local, recommended true lip-sync)

Install once (heavy; GPU strongly recommended, CPU works but is slow):

```bash
git clone https://github.com/vinthony/SadTalker.git
cd SadTalker
pip install -r requirements.txt
pip install gfpgan facexlib
```

Then run `talking_head.py` with `--engine sadtalker --sadtalker-home <path>/SadTalker`
or set env `SADTALKER_HOME`. The script converts the audio to 16kHz mono WAV and
invokes `inference.py` with `--preprocess full --still --enhancer gfpgan`, then
copies the newest produced `.mp4` to `--out`.

Notes:
- SadTalker output resolution depends on the source image; `compose_bilingual.py`
  normalizes all clips to 1280x720, so this is fine.
- First run downloads GFPGAN / model checkpoints (~hundreds of MB).

### B. D-ID (cloud, true lip-sync, paid)

No local model needed. Set credentials (Bearer token OR key+secret):

```bash
export DID_TOKEN="<your-d-id-token>"          # Bearer auth
# or
export DID_KEY="<key>"; export DID_SECRET="<secret>"   # Basic auth
```

`--engine did` sends the local image + audio as base64 data URIs, polls until the
talk is `done`, and downloads the result. D-ID bills per second of video.

### C. HeyGen (cloud, true lip-sync, paid)

HeyGen needs public URLs for the image and audio (not local files). Host them
(e.g. any static host / object storage) and set:

```bash
export HEYGEN_API_KEY="<key>"
export HEYGEN_IMAGE_URL="https://.../avatar.png"
export HEYGEN_AUDIO_URL="https://.../en.mp3"
```

Then `--engine heygen`.

### D. Fallback (no lip-sync)

If no engine is available, `--engine fallback` uses ffmpeg to make a video from the
still avatar + audio with a subtle zoom (ken-burns). This is a real, always-works
output but the mouth does NOT move in sync. Always tell the user it is approximate
and offer to upgrade to SadTalker / D-ID.

### VideoGen fallback (alternative motion)

Instead of a static zoom, you can use the WorkBuddy **VideoGen** tool
(image-to-video) on `avatar.png` with a prompt like "a presenter speaking to
camera, slight natural movement" to get a moving clip, then overlay the TTS audio
with ffmpeg. Still not precise lip-sync, but more lively than a static image.

## Step 5 — Composition

`compose_bilingual.py`:
- Builds `.srt` subtitles with proportional timing (by character count across lines).
- Burns subtitles (`subtitles` filter) into each clip.
- Adds a 2s labeled title card ("English" / "العربية") before each segment using
  `drawtext` + silent `anullsrc` audio so concat has audio on every input.
- Applies the mandatory AI-content labels (《人工智能生成合成内容标识办法》):
  corner watermark "AI 生成" on every segment + 3s bilingual end notice card
  ("本视频由 AI 生成" / "AI-Generated Content") + MP4 `comment`/`description`
  metadata. On by default; `--no-ai-label` disables the visible ones (tests only).
- Normalizes resolution and `concat` filters all streams into one MP4.

### AI label flags

| Flag | Default | 作用 |
|---|---|---|
| `--ai-label` | `AI 生成` | 角标文字（显式） |
| `--ai-notice` | `本视频由 AI 生成` | 片尾卡中文行 |
| `--ai-notice-en` | `AI-Generated Content` | 片尾卡英文行 |
| `--label-card-dur` | `3.0` | 片尾卡秒数 |
| `--no-ai-label` | off | 关闭显式标识（仅内部测试用） |
| `--cjk-fontfile` | auto | 覆盖自动检测的中文字体（msyh.ttc 等） |

### Arabic font

libass usually finds an Arabic-capable system font on Windows (e.g. via Arial /
Segoe UI). If Arabic glyphs are missing/boxed, pass `--fontfile` to a TTF such as
**Noto Naskh Arabic** or **Amiri**:

```bash
python compose_bilingual.py ... --fontfile "C:/Fonts/NotoNaskhArabic-Regular.ttf"
```

### ffmpeg quirks hit in practice (2026-10-19, ffmpeg 6.0 gyan build)

- **Windows drive-letter colons break the `subtitles` filter filename** — quoting
  does NOT protect `C:` on this build (`'C:/...'` is parsed as filename `C` +
  `original_size=/Users/...` → `Invalid argument`). The script therefore burns
  subtitles with `cwd=work` + bare basename. Do not "simplify" this back to
  absolute paths.
- **ffprobe may be absent** (PASMStudio's ffmpeg bundle ships ffmpeg.exe only).
  `probe_duration` falls back to parsing `ffmpeg -i` stderr `Duration:`.

## Troubleshooting

| Symptom | Fix |
|---|---|
| `edge-tts` import error | `pip install edge-tts` in the managed venv |
| `ffmpeg not found` | Install ffmpeg; or pass `--ffmpeg <path>`; or use PASMStudio bundle at `%LOCALAPPDATA%\PASMStudio\bin\ffmpeg.exe` |
| SadTalker no `.mp4` | Check its stdout/stderr; ensure `--enhancer gfpgan` deps installed; verify image is a clear face |
| D-ID 401 | Wrong/unsigned token; check `DID_TOKEN` or `DID_KEY`/`DID_SECRET` |
| HeyGen needs URLs | Host image+audio publicly; set `HEYGEN_IMAGE_URL`/`HEYGEN_AUDIO_URL` |
| Arabic subtitles show boxes | Provide `--fontfile` with an Arabic TTF |
| Clips different sizes | Already handled by normalize scale in compose |

## Working-directory checklist

```
en.txt, ar.txt
en.mp3, ar.mp3  (+ en.json, ar.json)
avatar.png
en_talk.mp4, ar_talk.mp4
bilingual_final.mp4   <- deliver this
```
