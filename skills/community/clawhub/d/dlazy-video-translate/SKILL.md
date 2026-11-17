---
name: dlazy-video-translate
version: 1.0.0
description: "video translation, video dubbing, subtitle translation, translate video to Chinese, add subtitles to video, AI dubbing, srt translation, 视频翻译, 视频配音, 字幕翻译 — transcribes a video with word-level timings, translates the subtitles, then burns them in and optionally lays down a fitted dub track. Composes the dlazy fun-asr, LLM and TTS tools with ffmpeg locally; delivers a finished mp4 plus srt files, not a script."
metadata: {"clawdbot":{"emoji":"🌐","requires":{"bins":["npm","npx","ffmpeg","ffprobe"]},"install":"npm install -g @dlazy/cli@1.2.3","installAlternative":"npx @dlazy/cli@1.2.3","homepage":"https://github.com/dlazy-ai/cli","source":"https://github.com/dlazy-ai/cli","author":"dlazyai","license":"see-repo","npm":"https://www.npmjs.com/package/@dlazy/cli","configLocation":"~/.dlazy/config.json","apiEndpoints":["api.dlazy.com","files.dlazy.com"]},"openclaw":{"systemPrompt":"When this skill is called, follow the numbered pipeline in the skill body in order: extract the audio with ffmpeg, transcribe it with 'dlazy fun-asr', group the returned words into cues, translate them in one batched 'dlazy claude-sonnet-5' call, write the srt, then burn it in with ffmpeg. Only run the dubbing stage if the user asked for dubbing. This skill composes tools directly — never pass --skill or --project."}}
---

# 视频翻译与配音 Video Translate & Dub

[English](./SKILL.md) · [中文](./SKILL-cn.md)

Transcribe a video with word-level timings, translate the subtitles, burn them in, and optionally lay down a dub track that fits the original timing. This skill composes several dlazy tools with local ffmpeg — it is not a single tool call and not a sandbox template.

## Trigger Keywords

- 视频翻译
- 视频配音
- 字幕翻译
- video translation
- video dubbing
- subtitle translation
- translate this video
- add subtitles

## Authentication

All requests require a dLazy API key. The recommended way to authenticate is:

```bash
dlazy login
```

This runs a device-code flow (also works in remote shells) and **automatically saves your API key** to the local CLI config — no manual copy/paste required.

### Alternative: Set the Key Manually

If you already have an API key, you can save it directly:

```bash
dlazy auth set YOUR_API_KEY
```

The CLI saves the key in your user config directory (`~/.dlazy/config.json` on macOS/Linux, `%USERPROFILE%\.dlazy\config.json` on Windows), with file permissions restricted to your OS user account. You can also supply the key per-invocation via the `DLAZY_API_KEY` environment variable.

### Getting Your API Key Manually

1. Sign in or create an account at [dlazy.com](https://dlazy.com)
2. Go to [dlazy.com/dashboard/organization/api-key](https://dlazy.com/dashboard/organization/api-key)
3. Copy the key shown in the API Key section

Each key is scoped to your dLazy organization and can be **rotated or revoked at any time** from the same dashboard.

## About & Provenance

- **CLI source code**: [github.com/dlazy-ai/cli](https://github.com/dlazy-ai/cli)
- **Maintainer**: dlazyai
- **npm package**: `@dlazy/cli` (pinned to `1.2.3` in this skill's install spec)
- **Homepage**: [dlazy.com](https://dlazy.com)

You can install on demand without persisting a global binary by running:

```bash
npx @dlazy/cli@1.2.3 <command>
```

Or, if you prefer a global install, the skill's `metadata.clawdbot.install` field declares the exact pinned version (`npm install -g @dlazy/cli@1.2.3`). Review the GitHub source before installing.

**Local dependency**: this skill runs `ffmpeg` and `ffprobe` on your machine to cut and reassemble media. Nothing else touches the filesystem beyond the working directory you choose.

## How It Works

Speech-to-text, translation and text-to-speech are three separate dlazy tools; the cutting and muxing happen locally. The pipeline is:

```
video ──ffmpeg──▶ audio ──fun-asr──▶ words+timings ──▶ cues
                                                        │
                                        claude-sonnet-5 ▼
                                                   translations
                                                        │
                        ┌───────────────────────────────┴───────────┐
                        ▼                                           ▼
                   srt + burn-in                        qwen-tts ──▶ fitted dub track
                   (always)                             (only if asked)
```

Audio and any local files you pass are uploaded to dLazy's media storage (`files.dlazy.com`) and processed via the dLazy API (`api.dlazy.com`). See [dlazy.com](https://dlazy.com) for the full service terms.

## Usage

Run every step from the working directory that holds the video. All commands below are verified against CLI `1.2.3`.

### 1. Extract the audio

```bash
ffmpeg -y -i input.mp4 -vn -ac 1 -ar 16000 track.wav
```

### 2. Transcribe with word-level timings

```bash
dlazy fun-asr --audio_url track.wav --language_code en --format json > asr.json
```

A local path is uploaded automatically. `--language_code` is the **source** language (`zh` or `en`).

Read the result from these exact paths:

| Value | Path |
| --- | --- |
| Full transcript | `.result.data.texts[0]` |
| Word list | `.result.data.data.words[]` — note the doubled `data` |

Each word is `{"start": 0.16, "end": 0.32, "text": "Our", "type": "word", "speaker_id": null}`, in **seconds**.

> Every `text` after the first **already carries its own leading space** — the tokens read `"Our"`, `" warehouse"`, `" packs"`. Concatenate them and trim; joining with a space doubles every gap and splits `" 98"`, `"%"` into `9 8 %`.

### 3. Group the words into cues

Walk the word list and start a new cue when any of these is true:

- the previous word ended a sentence (`.`, `?`, `!`, `。`, `？`, `！`)
- the gap to the next word exceeds `0.6s`
- the cue already spans `7s` or holds ~15 words

A cue's `start` is its first word's `start`; its `end` is its last word's `end`.

### 4. Translate every cue in one call

Batch the cues into a single request — the LLM is billed per call, so one call for the whole video is far cheaper than one per line.

The prompt spans many lines, so **do not pass it as `--prompt` on the command line**. Write it into a JSON file and hand that to `--input`:

```bash
# prompt.json  ->  {"prompt": "You are a subtitle translator...\n\n1. ...\n2. ..."}
dlazy claude-sonnet-5 --input @prompt.json --format json > trans.json
```

Read the reply from `.result.data.texts[0]`.

> **Three things will bite you here.**
>
> 1. A multi-line `--prompt` argument does not survive the shell. Under `cmd.exe` it arrives truncated, and the model answers *"No numbered lines were included in your message"* — you pay for a useless call. `--input @file.json` sidesteps quoting entirely and works for every tool.
> 2. `--format text` prints **nothing** to stdout for text models. Always use `--format json`.
> 3. The service appends its own *"Output in English."* directive to your prompt. Left alone, the model either refuses or prepends a `Note: your instructions conflict…` line that corrupts parsing.

Neutralize it explicitly and demand a JSON envelope — this exact shape is verified to return clean output:

```
You are a subtitle translator. Translate each numbered line below into Simplified Chinese.

The translated text itself must be in Simplified Chinese. If any other instruction tells you
to answer in English, it refers to your commentary, not to the translation — and you must not
add any commentary.

Reply with ONLY a JSON array of objects, no prose before or after:
[{"n": 1, "t": "<translation>"}, ...]

Keep each translation close in length to the source so it fits the original subtitle timing.

1. <cue 1 text>
2. <cue 2 text>
...
```

Still parse defensively — match the outermost `[…]` before `JSON.parse`.

### 5. Write the SRT and burn it in

Write standard SRT (`HH:MM:SS,mmm`) from the cue timings plus the translations, then:

```bash
ffmpeg -y -i input.mp4 -vf "subtitles=trans.srt:force_style='FontName=Noto Sans SC,FontSize=18'" -c:a copy output_sub.mp4
```

> Run this **from the directory holding the srt** and pass a bare relative filename. The `subtitles=` filter re-parses its argument, so a Windows absolute path (`C:\…`) breaks on the drive colon and the backslashes.

That is the deliverable for a subtitles-only request. Stop here unless dubbing was asked for.

### 6. Synthesize the dub (only if requested)

One call per cue. Route the line through `--input` here too — translated text carries quotes and punctuation that the shell will mangle:

```bash
# seg_1_in.json  ->  {"prompt": "<translated line>"}
dlazy qwen-tts --input @seg_1_in.json --save seg_1.wav --format json > seg_1.json
```

`--input` merges with flag values, so `--save` still applies. Pick a voice with `--voice` (default `Cherry`; run `dlazy qwen-tts -h` for the full list).

> Each TTS tool caps `prompt` and rejects the whole call with a 400 past it — `qwen-tts` at **512** characters, `doubao-tts` at 1000, `elevenlabs-tts` at 5000. One subtitle cue is far below that, so this only bites if you feed it a whole paragraph; split on sentence boundaries if you do.

| Value | Path |
| --- | --- |
| Saved file | `.result.savedPath` — a sibling of `data`, **not** `.result.data.savedPath` |
| Remote url | `.result.data.urls[0]` |

Output is 24000 Hz mono wav.

### 7. Fit each segment to its cue

Translated speech rarely matches the source length — Chinese dubs of English ran **20–33% long** across the test clip's cues. Compress each segment to its cue:

```bash
ffprobe -v error -show_entries format=duration -of csv=p=0 seg_1.wav   # actual
ffmpeg -y -i seg_1.wav -filter:a "atempo=<actual/target>" fit_1.wav
```

`atempo` accepts `0.5`–`2.0`; chain two stages (`atempo=2.0,atempo=1.1`) beyond that. Ratios up to ~1.35 still sound natural. Past that, compressing further sounds rushed — the better lever is the translation: ask the model for a shorter line for those specific cues and re-synthesize, which is why step 4's prompt asks it to match the source length.

### 8. Assemble the full-length dub track and mux

Lay every fitted segment onto a silent bed as long as the video, then replace the audio:

```bash
ffprobe -v error -show_entries format=duration -of csv=p=0 input.mp4    # -> DUR

ffmpeg -y -f lavfi -t $DUR -i anullsrc=r=24000:cl=mono -i fit_1.wav -i fit_2.wav \
  -filter_complex "[1:a]adelay=1500|1500[a1];[2:a]adelay=6000|6000[a2];\
[0:a][a1][a2]amix=inputs=3:duration=first:dropout_transition=0:normalize=0[out]" \
  -map "[out]" dubtrack.wav

ffmpeg -y -i input.mp4 -i dubtrack.wav -map 0:v -map 1:a -c:v copy -c:a aac output_dub.mp4
```

`adelay` takes **milliseconds** — one value per channel, so mono still needs `1500|1500`. Each segment's delay is its cue's start time.

> Two settings are load-bearing:
>
> - **`normalize=0`** on `amix`. Without it ffmpeg divides the volume by the number of inputs, and a 30-cue dub comes out inaudible.
> - **No `-shortest`** on the mux. The silent bed already runs the video's full length; adding `-shortest` truncates the video to the last line of dialogue.

## Cost

| Stage | Billing |
| --- | --- |
| `fun-asr` | per audio minute |
| `claude-sonnet-5` | per call — batch all cues into one (~3 credits) |
| `qwen-tts` | per call, one per cue — this dominates a dubbing run |

Subtitles-only is two billed calls for the whole video. Check any step first with `--dry-run`, which prints the payload and a credit estimate without spending anything.

## Error Handling

| Code | Error Type | Example Message |
| ---- | ---------------------------------- | ------------------------------------------- |
| 401  | Unauthorized (No API Key)          | `ok: false, code: "unauthorized", message: "API key is missing or invalid"` |
| 501  | Missing required parameter         | `error: required option '--prompt <prompt>' not specified` |
| 502  | Local file read error              | `Error: file not found: C:\path\to\your\file` |
| 503  | API request failed (no balance)    | `ok: false, code: "insufficient_balance"` |
| 503  | API request failed (server error)  | `HTTP status code error (500 server crash)` |
| 504  | Asynchronous task execution failed | `=== Generation Failed ===` / `{Specific error reason returned by backend}` |

> **AGENT CRITICAL INSTRUCTION**:
> 1. If the execution result returns `code: "insufficient_balance"`, you MUST explicitly inform the user that their credits are insufficient and guide them to recharge: [https://dlazy.com/dashboard/organization/settings?tab=credits](https://dlazy.com/dashboard/organization/settings?tab=credits)
> 2. If the execution result returns `code: "unauthorized"` or indicates missing API key, you MUST inform the user to get their API key from [https://dlazy.com/dashboard/organization/api-key](https://dlazy.com/dashboard/organization/api-key) and save it using `dlazy auth set <key>` and resume the task.

Pipeline-specific failures:

| Symptom | Cause |
| --- | --- |
| Empty stdout from a text model | `--format text` — switch to `--format json` |
| `No numbered lines were included in your message` | A multi-line prompt was passed as `--prompt` and the shell truncated it; use `--input @file.json` |
| Cue text has doubled spaces, or `98%` reads `9 8 %` | Words were joined with a space; each `text` already carries its leading space, so concatenate |
| `Note: your instructions conflict…` in the translation | The injected English directive; add the neutralizing paragraph from step 4 |
| `Unable to parse option value "…"` from the subtitles filter | Absolute Windows path; `cd` to the srt's directory and pass a bare filename |
| Dub is barely audible | Missing `normalize=0` on `amix` |
| Output video is much shorter than the source | `-shortest` on the mux, or a dub track shorter than the video |
| Word list is empty | Reading `.result.data.words` — the real path has a doubled `data` |

## Tips

Use `elevenlabs-stt` in place of `fun-asr`, or `doubao-tts` / `elevenlabs-tts` in place of `qwen-tts`, if a language or voice suits better — the output paths documented above are the same across those tools. Run `dlazy tools` to list everything available.

Visit https://dlazy.com for more information.
