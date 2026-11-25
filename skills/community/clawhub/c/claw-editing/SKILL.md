---
name: claw-editing
description: Edit OpenClaw / OpenClaw Foundation videos (release updates, feature shorts, interviews) in the house style. Pick clean takes, cut, clean up speech, and add the signature fresco motion graphics (claw-and-spark title card, lower thirds, section overlays, animated explainers, "OpenClaw Foundation" end card, thumbnail), then QA it and write YouTube/X/LinkedIn copy. Use when asked to edit a video "with my skill", give it "the OpenClaw treatment", or add OpenClaw-style graphics.
version: 1.0.0
homepage: https://openclaw.ai
metadata: {"openclaw": {"emoji": "🦞", "os": ["darwin"], "requires": {"bins": ["ffmpeg", "ffprobe", "python3"]}, "envVars": [{"name": "OPENCLAW_FFMPEG", "required": false, "description": "Path to an ffmpeg binary to use instead of the one on PATH (ffprobe must sit beside it)."}], "install": [{"id": "brew", "kind": "brew", "formula": "ffmpeg", "bins": ["ffmpeg", "ffprobe"]}]}}
---

# OpenClaw video editing

This is Graham McBain's (OpenClaw Foundation) editing workflow, distilled from the 9.9 update, the 10.1 short and the "What is OpenClaw Enterprise" interview. He hands over a raw or rough video and expects a finished, branded video he can post, plus the parts to rework it later. Read `{baseDir}/references/preferences.md` before deciding anything editorial. It's his actual feedback, and following it is the point of this skill.

## What "done" looks like

1. **A finished video**, versioned (`… - v1.mp4`, then `v2`, `v3`…), saved next to his source. Never overwrite his source or an earlier version.
2. **A `Motion Graphics/` folder** next to it, containing:
   - `clips/`: every graphic as ProRes 4444 with alpha, fades baked in.
   - `source/`: the scripts and plan used.
   - `contact-sheet.jpg`
   - `README.md` with a placement table.
3. **Show him where it is.**
   - Give the full path in plain words.
   - On a Mac with a GUI session, also run `open -R "<video>"` to reveal it in Finder.
   - When he's chatting from a phone or messaging app, send the contact sheet image as a preview. The video itself is usually too big to send.
4. **An honest report:** what was cut, which graphics and where, what QA checked and what it didn't (frames checked, not a full watch), and anything he must check, such as wording you invented, uncertain names, or long cutaways.
5. **Then offer** to write the YouTube description with chapters, an X post and a LinkedIn post (`{baseDir}/references/social-copy.md`).

## Setup (once per machine; safe to re-run)

```bash
bash {baseDir}/scripts/setup.sh
PY=~/.cache/claw-editing/venv/bin/python
S={baseDir}/scripts
```

`setup.sh` creates a venv at `~/.cache/claw-editing/venv` and installs from PyPI:
- skia-python, pillow, numpy
- mlx-whisper on Apple Silicon, faster-whisper elsewhere

The first transcription downloads the Whisper model (about 1.6 GB) from Hugging Face. ffmpeg comes from `PATH` (`brew install ffmpeg`), or set `OPENCLAW_FFMPEG`. Use an ffmpeg build with `prores_ks` and `libx264`; Homebrew's has both. Fonts are macOS system fonts (Baskerville, Avenir Next Condensed), so this skill is macOS-only. Run project scripts with `PYTHONPATH=$S` so they can `import render, overlays`.

**The video must be on the machine you're running on.** If his footage is on another Mac (his gateway may be a different machine from his laptop), ask him to copy it over, or use a paired node to fetch it first. Save outputs beside the footage.

Keep project scripts and plans in the **project folder** (for example `<video folder>/Motion Graphics/source/`), not only in a temp dir. A scratch folder was wiped between sessions once, and only the copies saved next to the deliverables survived.

## Workflow

### 1. Look before deciding
- `ffprobe` the file: resolution, **frame rate** (59.94 raw camera, 30 for screen-recorded calls), audio rate, duration.
- Transcribe: `$PY $S/transcribe.py <video> <work>`. Read the whole transcript.
- Contact sheet every 20 s: `$PY $S/contact_sheet.py <video> <work>/sheet.jpg --every 20 --cols 6 --width 384`. Look at the image yourself for framing (where faces sit), split-screen layouts, existing burned-in overlays (old title cards, name tags, end cards), people looking away or down, and interruptions (a dog, a false start).
- If there are burned-in overlays to replace, look for a clean version of the same recording. Align it by audio cross-correlation and frame matching before trusting it (`{baseDir}/references/pipeline.md`).

### 2. Decide the shape (see references/preferences.md)
- **Raw multi-take recording, such as a release short:** pick the single cleanest complete take of each line, and drop false starts, repeats, asides and personal preamble. Start on substance.
  - If he names the topics, cover exactly those, in the grouping he describes.
  - Features he says "go together" play as one quick run under one list card.
  - The standalone highlight goes last, before the close.
- **Already-edited video (interview, podcast):** don't re-cut. Add a title card, name tags, section overlays, a few animated explainers and an end card, and replace any old-style overlays.
- Only ask him when the answer changes the edit and the footage can't settle it.

### 3. Find exact cut points and beats
Whisper word times run 0.1–0.4 s early.
- `$PY $S/envelope.py <work>/audio16k.wav <t0> <t1>` gives dB per 20 ms. Cut inside dips (below about −40 dB). An onset is where the level jumps.
- Before committing a tight splice, transcribe a test join (both sides concatenated), so a leaked syllable from the next word gets caught.
- Use envelope onsets, not raw Whisper times, for any graphic that should land on a word.

### 4. Build the graphics
Read `{baseDir}/references/style-guide.md`. Library: `scripts/render.py` (core: palette, fresco texture, spark, embers, claw, `Card`, `LowerThird`, `em_bookend`) and `scripts/overlays.py` (`PanelTag`, `SectionOverlay`, `Explainer` and explainer drawing helpers). Call `R.set_fps(<source fps>)` first. Worked projects to copy from:

| Video type | Graphics script | Edit / composite script |
|---|---|---|
| Short feature update (raw takes) | `examples/short_update_graphics.py` | `examples/short_update_edit.py` → generalised as `scripts/edit.py` |
| Interview / call (already edited) | `examples/enterprise_interview_graphics.py` | `examples/enterprise_interview_composite.py` → `scripts/composite.py` |
| Longer update with per-section cards | `scripts/render.py` `build()` | `examples/long_update_recut_composite.py` |

Always check stills before encoding. Render a few frames (`clip.frame(i)` → PNG), composite lower thirds over a real frame of the footage, and look at them for text collisions, labels near the frame edge and anything covering faces. Every round of this has found something.

Encode the clips in parallel (`xargs -P 8`), one ProRes 4444 `.mov` per clip, named by what it is (`intro-title`, `section-03`, `mg-trusted-untrusted`, `lt-06-mac-setup`, `outro-foundation`).

### 5. Assemble
- **Cutting raw footage:** write a plan JSON and run `$PY $S/edit.py plan.json` (format in the script docstring). It cuts frame-accurately, adds splice fades, applies a high-pass and light denoise (it removes the denoiser's measured latency), runs two-pass loudnorm to −16 LUFS, keeps silence under the title and end cards, places overlays by segment and offset, and can add the thumbnail.
- **Already-edited video:** `$PY $S/composite.py plan.json`. The audio is stream-copied untouched unless a thumbnail is prepended.
- Long renders (a 22-minute 1080p video with about 20 overlays) take around 15–20 min. Start them as a background process, tell him roughly how long, and check back instead of blocking.

### 6. QA (do all of it, report honestly)
`$PY $S/qa.py <out.mp4> <work>/qa --source <src> --edl <work>/edl.json --times <t,…>`
- The **transcript of the finished video** reads cleanly in the intended order, with no doubled or clipped words at splices.
- **Sync:** about 0 ms lag on every segment versus the source.
- **Loudness:** about −16 LUFS, peak at or below −2 dB.
- **Frame count** matches the plan, the thumbnail and cover art are present when requested, and old overlays are fully covered on their first frame.
- **Contact sheet:** look at it, with a time inside every graphic and either side of every cut.

Report what you verified and say plainly that you haven't watched it end to end.

## Things he cares about (short version; reasons are in references/preferences.md)
- The look comes from the openclaw.ai Foundation social image (`assets/style-reference.png`): dark fresco, a red claw reaching toward an ember spark. Use the style, not that exact image.
- **Graphics are drawn in code.** Ask before spending money or credits on AI image generation.
- The **end card just says "OpenClaw Foundation".** No tagline, no URL.
- The **title card** keeps his own title wording. The old cartoon lobster mascot is retired for this style.
- **Section overlays** on interviews are lower-third-style markers, not full-screen section cards. Full-screen animation is for the illustrative passages.
- **Captions use the speaker's own words.** Anything you invent, or are unsure of (garbled model names, people's titles), gets flagged in your report, not slipped in.
- A **thumbnail he provides** is held as the first 1 s and embedded as cover art, in a new version. Remind him that YouTube needs it uploaded separately.

## Reference files
- `references/preferences.md`: every piece of his feedback, with the reasoning. Read it first.
- `references/style-guide.md`: palette, type, layouts, motion timings, emblem patterns, sizes.
- `references/pipeline.md`: ffmpeg recipes and gotchas that cost time (adelay bug, denoiser latency, VFR clean sources, shell quirks, 24-bit WAVs).
- `references/social-copy.md`: YouTube description and chapters, X post and thread, LinkedIn post templates and rules.
