---
name: autoDemoRecordingSkill
description: Record a polished demo video of a web app automatically, with or without narration. Drives the app in headless Chromium from a story file, records clicks/typing/scrolls, renders a 1920x1080 60fps video with camera moves, highlights, numbered steps, captions and chapters, then adds a narration in the chosen language — local Qwen3-TTS on an NVIDIA GPU, local Kokoro on any CPU, or a remote API (OpenAI-compatible, ElevenLabs, Alibaba DashScope) — and verifies picture and sound numerically. Works on Linux, Windows and macOS, and under Claude Code or Codex. Use when asked to make a product demo video, screen recording, walkthrough, feature tour, or narrated screencast of a web app.
external_urls:
  - https://api.openai.com
  - https://api.elevenlabs.io
  - https://dashscope.aliyuncs.com
  - https://dashscope-intl.aliyuncs.com
  - https://huggingface.co
  - https://hf-mirror.com
  - https://pypi.org
  - https://files.pythonhosted.org
  - https://download.pytorch.org
  - https://playwright.azureedge.net
  - https://github.com
---

# autoRecording

Turn a web app into a finished demo video. You write a **story file** that says what to show and what to say; the
scripts do the recording, drawing, encoding, narration and checking. The video can be silent or narrated, in
Mandarin, English, Japanese, Korean, German, French, Spanish, Italian, Portuguese or Russian, spoken by a local model
(GPU or CPU) or a remote service the user provides.

```
story.py ──demo_record.py──► timeline.json + frames/*.jpg
                                  │
                           demo_render.py ──► silent.mp4  (1920×1080, 60 fps)
                                  │
                           demo_voice.py  ──► silent-配音版.mp4 / silent-narrated.mp4   (optional)
```

## 0. Ask before anything else

Do not start recording before these are answered. In Claude Code use `AskUserQuestion`; under Codex or any other
agent, ask in plain words and wait for the reply.

1. **Narration?** Silent video, or spoken narration. If the user does not need narration, skip every narration step;
   the silent video is the deliverable.
2. **Language of the narration** (and of the captions, which are the script it reads): 普通话 / English / 日本語 /
   한국어 / Deutsch / français / español / italiano / português / русский. Default: the language of the app and of
   what the user writes in.
3. **Engine.** Offer what this machine can actually do — run `python3 scripts/demo_env.py` first and offer only the
   engines it lists as available:
   - **local Qwen3-TTS** (本机 GPU): best quality; needs an NVIDIA GPU with ~6 GB free VRAM and the Qwen models.
   - **local Kokoro** (本机 CPU): no GPU needed, works on Windows and macOS; good Mandarin and English; voices are
     fixed (no cloning).
   - **remote API**: the user supplies the provider (OpenAI-compatible endpoint incl. self-hosted, ElevenLabs, or
     Alibaba DashScope Qwen-TTS), the key, and optionally a base URL, model and voice id.
   Rule of thumb: a local model that is ready → use it; the user offers an API key → use the API; neither → ask
   whether to install Kokoro (small download) or to go silent.
4. **Voice**, if the engine has a choice: offer 3–5 voices with one line each (e.g. Qwen `serena` / `ryan`, Kokoro
   `zf_039` / `zm_013` / `af_maple`, an OpenAI voice id), with a sensible default.

Write the answers into the story file — `LANGUAGE` and `VOICE = {'engine': …, 'speaker': …}` — so the same video can
be made again. A remote key is never written into the story: put it in the environment or `demo_env.py key`.

## Non-negotiables

1. **Never record the user's live service or real data.** Start a throwaway instance on another port with its own data
   directory (`launch()` in the story file), or a dedicated demo dataset. If the app cannot be isolated, ask.
2. **Check in numbers, not by watching pictures.** `demo_render.py --check` and `demo_voice.py check` are the source
   of truth. Do not claim a video is done while either reports `注意：` problems.
3. **Do not touch a running service.** If the chosen port is already listening, pick another port; never stop
   someone else's process.
4. The narration is optional and its engine is the user's choice. Qwen needs an NVIDIA GPU; Kokoro runs on any CPU;
   remote services need a key and send the captions to that service — say so before using one.

## Layout

```
SKILL.md                  this file
scripts/demo_env.py       check the machine; make the skill's Python; fetch models; remember keys
scripts/demo_record.py    drive the app and record frames + timeline
scripts/demo_render.py    draw and encode the silent video; numeric checks
scripts/demo_voice.py     narration: lines, anchor, takes, hear, build, check
scripts/demo_tts.py       the engines: Kokoro (CPU) and the remote services
scripts/demo_text.py      how captions are said, counted and compared, per language
scripts/demo_common.py    shared paths, settings, browsers, secrets
story_template.py         copy this to write a story for an app
examples/selftest/        a page and two stories (Mandarin story.py, English story-en.py)
references/               environment.md, director.md, narration.md, engines.md
```

All commands below are relative to this skill's directory; on Windows write `py -3` (or `python`) where `python3` is
written. Install as a personal skill by cloning to `~/.claude/skills/autoDemoRecordingSkill` (Claude Code) or
`~/.agents/skills/autoDemoRecordingSkill` (Codex).

## 1. Check the machine

```bash
cd ~/.claude/skills/autoDemoRecordingSkill
python3 scripts/demo_env.py            # read-only: what is there, what is missing, how to get it, which engines can speak
python3 scripts/demo_env.py setup      # packages for record/render/check (a few hundred MB)
python3 scripts/demo_env.py setup --models   # + Whisper large-v3 and CAM++ checks (~3 GB)
python3 scripts/demo_env.py setup --kokoro   # + Kokoro, the CPU voice (~400 MB)
```

For the Qwen engine also prepare a Python with CUDA torch and `faster-qwen3-tts`, and the two Qwen3-TTS 1.7B models;
for a remote engine, remember its key once with `python3 scripts/demo_env.py key openai=…` (or an environment
variable). Record every non-default location once:

```bash
python3 scripts/demo_env.py set chromium=/path/to/chromium tts_python=/path/to/python \
    tts_custom=/path/to/Qwen3-TTS-12Hz-1.7B-CustomVoice tts_base=/path/to/Qwen3-TTS-12Hz-1.7B-Base
```

The skill's own files live in `~/.cache/auto-demo-recording` (override with `AUTO_DEMO_HOME`). `references/environment.md`
has the Windows, macOS and Linux details.

## 2. Validate the installation with the self-test

```bash
PY=~/.cache/auto-demo-recording/venv/bin/python
S=~/.claude/skills/autoDemoRecordingSkill
$PY $S/scripts/demo_record.py --story $S/examples/selftest/story.py --work /tmp/demo-selftest
$PY $S/scripts/demo_render.py --work /tmp/demo-selftest --check
$PY $S/scripts/demo_render.py --work /tmp/demo-selftest --out /tmp/demo-selftest/selftest.mp4
$PY $S/scripts/demo_voice.py --work /tmp/demo-selftest      # only if a narration is wanted
```

`story-en.py` is the same test with English captions and the English narration path. The recording prints a JSON
summary (length, frames, browser, errors). `selftest.mp4` should be 1920×1080, 60 fps, about 64 s.

## 3. Write the story

Copy `story_template.py` next to the app (or anywhere) and fill it in. The contract:

| Name | What it is |
| --- | --- |
| `TITLE`, `SUBTITLE`, `CHAPTERS` | text in the top band; chapters are also drawn on the page |
| `LANGUAGE` | the language of the captions and of the narration (`zh`, `en`, `ja`, `ko`, `de`, `fr`, `es`, `it`, `pt`, `ru`) |
| `VIEW`, `DENSITY` | page size in CSS px and device scale; width/height must be 64:31 |
| `PORT` | port of the throwaway instance |
| `LOOK` | `{'accent': '#2f6fed', 'note': '#ee5c18', 'fast': '快进'}` — `fast` in the caption band's language |
| `VOICE` | narration: `engine`, `speaker`, and for a remote service `model` / `base_url` (never the key); see `references/engines.md` |
| `READING` | reading speed for captions; default: the language's own (5.5 characters/s for Mandarin) |
| `launch(work, port)` | `{'command': [...], 'url': ..., 'env': {...}, 'wipe': [...], 'cwd': ..., 'ready': ..., 'timeout': ...}`; or define `URL` instead |
| `guard(d)` | optional; fail early if the page is not in the intended initial state |
| `story(d)` | the actual direction: `await d.say(...)`, `await d.click(...)`, etc. |

The `d` object is the director. Its full API, time model, mark/place rules and common patterns are in
`references/director.md`. Read it before writing a story; the rest of this file is only the workflow.

Rules of thumb for a good story:

- One idea per caption; state what the viewer should notice, and results the page actually shows.
- Prefer `d.say()` then `d.read()` before moving on; captions are also the narration script.
- Write captions in `LANGUAGE`. For a silent video they are still read on screen, so keep them short.
- Number the clicks (`await d.click(locator, '添加')`) and mark only what matters.
- Play long waits fast (`await d.until(..., speed=4)`) instead of cutting them.

## 4. Record

```bash
$PY $S/scripts/demo_record.py --story /path/to/story.py --work /tmp/demo-work --quick
$PY $S/scripts/demo_record.py --story /path/to/story.py --work /tmp/demo-work
```

`--quick` is a fast trial: it skips viewer pauses and only waits for the app. Use it to catch selector and state
errors. Record for real afterwards; `work/timeline.json` is overwritten and the old frames removed.

Before recording, the script wipes only `frames` and the paths listed in `wipe`, checks the port is free, starts the
command from the story, and waits for the app to answer. The app's log is `work/server.log`. On Windows the app and
everything it starts is stopped with `taskkill /T`; elsewhere the whole process group is stopped.

## 5. Check and render

```bash
$PY $S/scripts/demo_render.py --work /tmp/demo-work --check
$PY $S/scripts/demo_render.py --work /tmp/demo-work --out /tmp/demo-work/demo.mp4
```

`--check` verifies, without looking at pictures: marked regions are non-empty and match `expect` colours, labels do
not sit on page content, boxes are inside the camera, steps/clicks are visible, captions fit, and glyphs exist in the
font. Fix the story or the timing and record again. Rendering also compares sampled output frames with the frames it
drew and writes `work/render.json`.

**If the user wants no narration, the silent video is the deliverable — stop here and report.**

## 6. Narrate (only if asked for)

```bash
$PY $S/scripts/demo_voice.py --work /tmp/demo-work            # all steps
$PY $S/scripts/demo_voice.py lines --work /tmp/demo-work      # inspect pronunciation/timing first
```

It writes the narrated video next to the silent one: `<name>-配音版.mp4` for Mandarin, `<name>-narrated.mp4` for the
other languages. The steps are resumable: reference clip → (Qwen: trial) → takes → speech/speaker checks →
choose/fit/mix → verify. Read `references/narration.md` for settings, pronunciation fixes and tight lines, and
`references/engines.md` for the engines, their voices, keys and costs. The final `check` must say
`没有发现问题`; any `听写有出入` line means the voice said something else — fix the caption, add a `say` override,
re-speak that line, or choose another voice.

## 7. Report

Give the user the output path (silent and, if asked for, narrated), duration, resolution/fps, number of
captions/marks, the narration engine and voice, and the narration check result. Mention any `注意：` warnings that
remain, and never hide a failed check.

## Troubleshooting first moves

- `缺 …` → run `python3 scripts/demo_env.py` and follow the `→` line.
- Port already in use → change `PORT` in the story; do not stop the existing service.
- `点不到这个元素` → the element is covered or off-screen; scroll/zoom first, or pick another target.
- Page width mismatch → the page is not responsive at `VIEW`; adjust `VIEW` or the page, keep the 64:31 ratio.
- Narration line too tight → shorten that caption or give it more time, then record again.
- `Kokoro 的词表里没有这些词` → those words are skipped by Kokoro; add them to `VOICE['say']` in the caption's
  spelling (e.g. `"API": "A P I"`, `"exported": "export ed"`), or use Qwen or a remote engine for English.
- Font boxes (□□□) → on Linux install Noto Sans CJK; Windows and macOS have their own Chinese faces; or set
  `DEMO_FONT_*` (see `references/environment.md`).

## Under Codex

Codex loads the same `SKILL.md`. It has no `AskUserQuestion` tool: ask the step-0 questions in plain words. It may
run with a different `PATH` — use `py -3` or the full path of the skill's Python. Install the skill with
`git clone … ~/.agents/skills/autoDemoRecordingSkill` (or let Codex's skill-installer place it in
`~/.codex/skills`); both are discovered. `agents/openai.yaml` gives it a display name and a starting prompt.

## Privacy

The work folder contains screenshots of whatever the app showed. Use a throwaway instance with sample data, never
real accounts, customers or production records. Do not commit `work/` or rendered videos without reviewing them.
`timeline.json` also records the story file path and the capture time. A remote narration service receives the
caption text of every line; a local engine sends nothing.
