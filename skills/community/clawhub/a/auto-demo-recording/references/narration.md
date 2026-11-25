# Narration

`demo_voice.py` reads the captions of a finished silent video and speaks them in the video's language, then muxes the
result under the picture. The video stream is copied, never re-encoded, so the picture and its length stay exactly as
rendered. Narration is optional: without it, the silent video is the deliverable.

It is not a single TTS call per caption. The script builds one fixed voice, speaks every line several times, checks
what was said and in whose voice, picks the steadiest take that fits its caption, and then verifies the finished
file. Everything is resumable and cached under `work/voice/`.

Which engine speaks is the user's choice: **local Qwen3-TTS** on an NVIDIA GPU, **local Kokoro** on any CPU, or a
**remote service** (OpenAI-compatible, ElevenLabs, Alibaba DashScope). The engines, their voices, keys and costs are
in [`engines.md`](engines.md); this file is about the narration as a whole.

## Requirements

- the skill's own Python (for `faster-whisper`, `sherpa-onnx`, `pypinyin`, `soundfile`, `soxr`, `scipy`);
- `ffmpeg` with `atempo` and `ebur128`;
- one of the engines:
  - Qwen: an NVIDIA GPU with about **6 GB free VRAM**, a Python with CUDA `torch`, `faster-qwen3-tts`, `librosa`,
    and the Qwen3-TTS **Base** and **CustomVoice** 1.7B models;
  - Kokoro: the Kokoro model (`demo_env.py setup --kokoro`) and `sherpa-onnx` in the skill's Python;
  - remote: a key (`demo_env.py key …`) and, for a self-hosted or third-party endpoint, its `base_url`.

`references/environment.md` explains how to install all of this. `scripts/demo_env.py` says what is missing and which
engines can speak.

## Commands

```bash
PY=~/.cache/auto-demo-recording/venv/bin/python
S=~/.claude/skills/autoDemoRecordingSkill

$PY $S/scripts/demo_voice.py --work /tmp/demo-work                 # everything, in order
$PY $S/scripts/demo_voice.py lines --work /tmp/demo-work           # inspect the script; no model needed
$PY $S/scripts/demo_voice.py anchor --work /tmp/demo-work          # make/list reference clips (Qwen: 32 candidates)
$PY $S/scripts/demo_voice.py anchor 2-5 --work /tmp/demo-work      # Qwen: take candidate 2-5 as the voice
$PY $S/scripts/demo_voice.py trial --work /tmp/demo-work           # Qwen: compare candidate voices
$PY $S/scripts/demo_voice.py takes 12 15 --work /tmp/demo-work     # re-speak lines 12 and 15
$PY $S/scripts/demo_voice.py build --work /tmp/demo-work           # choose/fit/mix again
$PY $S/scripts/demo_voice.py check --work /tmp/demo-work           # verify the finished file
```

The output defaults to the rendered video's name plus `-配音版` (Mandarin) or `-narrated` (other languages). Use
`--video` and `--out` to point at other files:

```bash
$PY $S/scripts/demo_voice.py --work /tmp/demo-work --video /tmp/demo-work/demo.mp4 --out /tmp/demo-work/demo-voiced.mp4
```

The script refuses a video whose duration differs from `timeline.json` by more than 0.5 s: it must be the
whole video rendered from that timeline.

## What the steps do

| Step | Work |
| --- | --- |
| `lines` | prints every caption, its window, its length (字 or syllables), the pace it needs and how it will be said |
| anchor | Qwen: the built-in speaker says one reference text in 4 styles × 8 clips; each is measured and heard. Others: one clip from the chosen voice, whose pace sets the speaking speed |
| trial | Qwen only: a few tight and ordinary lines are spoken after each shortlisted reference; the steadiest voice that fits wins |
| takes | every line is spoken `takes` times (6 Qwen, 4 Kokoro, 2 remote by default) |
| hear | faster-whisper writes down what was said, in the video's language; the script is compared with it; CAM++ compares the voice with the reference clip |
| build | for each line, the best take is chosen, fitted into its caption window, levelled, mixed, and muxed |
| check | the finished file in numbers: picture packets unchanged, same duration, every line inside its caption, loudness/peaks, voice similarity, re-listening |

Caches make re-runs cheap: a take already spoken with the current text, engine and voice is not spoken again.
Changing the reference voice deletes the takes made after another reference (they would sound different).

## Settings

The defaults live in `DEFAULTS` in `scripts/demo_voice.py`. Override them in the story's `VOICE` dict (recorded
into the timeline) or in `work/voice/settings.json` (local, not recorded; highest priority):

```json
{
  "engine": "kokoro",
  "speaker": "zf_039",
  "language": "zh",
  "pace": 4.2,
  "takes": 8,
  "fastest": 1.10,
  "say": {"API": "A P I", "2026": "二零二六"}
}
```

| Key | Default | Meaning |
| --- | --- | --- |
| `engine` | first that can speak | `qwen`, `kokoro`, `openai`, `compatible`, `elevenlabs`, `dashscope` |
| `language` | the story's `LANGUAGE` | `zh` `en` `ja` `ko` `de` `fr` `es` `it` `pt` `ru`; it must be the captions' language |
| `speaker` | the engine's usual voice | Qwen speaker, Kokoro voice (name or number), remote voice id |
| `model` / `base_url` / `language_code` / `instructions` | the service's own | remote only; the key is never set here (environment or `demo_env.py key`) |
| `styles` | 4 instruct texts | Qwen: the deliveries the reference clips are tried in |
| `candidates` | `8` | Qwen: clips per style |
| `anchor_text` | `null` | what the reference says; default: title + first plain captions |
| `anchor` | `null` | Qwen: reference to use, e.g. `2-5`; default: chosen by the trial |
| `say` | `{}` | pronunciation overrides for captions, e.g. `{"WPS 365": "W P S 三六五"}` |
| `pace` | the language's (4.3 字/秒 zh, 4.0 syllables/s en) | target pace where the captions leave a choice |
| `takes` | 6 / 4 / 2 by engine | times each line is spoken |
| `lead` / `gap` | `0.25` / `0.30` | a line starts/ends this long after/before its caption boundary |
| `lead_min` / `gap_min` | `0.10` / `0.15` | how far those give way when time is short |
| `fastest` | `1.12` | no line is sped up more than this (never slowed down) |
| `loudness` | `-16.0` | integrated LUFS of the narration |
| `peak` | `-1.5` | peak ceiling in dBFS |

Unknown keys stop the script and list the valid ones. After changing settings, run `build` (and `check`); after
changing `speaker`, `engine`, `styles`, `candidates` or `anchor_text`, run `anchor` again (or delete `work/voice`).

## Languages

The captions are the narration script, so the narration is in the caption language (`LANGUAGE` in the story). The
recorder gives a caption its reading time by that language's own rule, and the narration counts the same way:

| Language | Unit | Pace (units/s) | Reading (caption gets) | File name |
| --- | --- | --- | --- | --- |
| 普通话 `zh` | 字 | 4.3 | 5.5 字/s | `-配音版` |
| English `en` | syllable | 4.0 | 3.8 /s | `-narrated` |
| 日本語 `ja` | 拍 | 7.0 | 6.6 /s | `-narrated` |
| 한국어 `ko` | 음절 | 5.0 | 4.7 /s | `-narrated` |
| de / fr / es / it / pt / ru | syllable | 4.2–5.2 | 4.0–4.9 /s | `-narrated` |

Numbers and letters are read out in the caption's language: `demo_text.spoken()` turns `2026-11-19`, `25%`,
`12,500`, `$12.50`, `3rd`, `1,250` and short capitals (`API`) into words, in Mandarin or in English. The other
languages are given to the engine as written: write their numbers as words where it matters. For Japanese and Korean
the check compares characters, so it is more forgiving than for English.

## Changing the voice

- **Qwen**: the model ships nine speakers; set `speaker` and run `anchor` again. The reference clip fixes pitch,
  timbre and pace; `demo_voice.py anchor 2-5` chooses one manually, otherwise the trial picks the candidate whose
  lines fit best and move least in pitch. There is no cloning of the user's own voice.
- **Kokoro**: set `speaker` to a voice name or number (`demo_voice.py anchor` shows the list of what it tried, and
  `references/engines.md` the recommended ones). The voice itself does not vary between takes.
- **Remote**: set `speaker` to the service's voice id; `instructions` (OpenAI) or the voice's own settings shape the
  delivery.

## Pronunciation

Anything the rules get wrong is fixed with `say`; keys are matched case-insensitively and ignore spaces. Use
`demo_voice.py lines` to see the exact text that will be spoken; if the line differs from the caption, the caption
is printed below it. For Kokoro, words the lexicon does not have are skipped (the anchor step lists them), so
English captions with brand names may need `say` (e.g. `"GitHub": "git hub"`) or another engine.

## Fitting

Every line must start after its caption appears and end before the next one (minus `lead`/`gap`). When a line
is too long for its window, the pauses around it are reduced first, then it is sped up with `atempo` — up to
`fastest`. Beyond that the check reports the line; the fix is **shorter text or more time in the picture**, not
a faster voice. Engines with a speed parameter are already asked to speak near the pace the video wants, so this
rarely happens; DashScope has no speed parameter, so a fast-speaking voice or shorter captions may be needed.

To give a line more time, lengthen the gap before the next caption in the story (for example, an extra
`await d.read()`), then record and render again.

## Verification

`check` writes `work/voice/check.json`, cuts each spoken line into `work/voice/final/NNN.wav`, and reports:

- picture packets identical to the silent video, same container duration;
- each line's beginning/end relative to its caption; lines touching the boundary;
- lines sped beyond `fastest`;
- sound outside caption windows;
- what the recogniser heard for every line, and syllables/words that differ;
- voice similarity to the reference (CAM++); below `0.65` is reported;
- integrated loudness, peaks and their spread; whether the muxed sound matches the mixed track (offset/correlation).

The final line must be `没有发现问题`. Read the `注意：` lines and the `听写有出入` entries: most are fixed by
shortening one caption, adding a `say` override, re-speaking one line, or choosing another voice, in that order.

## Time and space

On a recent NVIDIA GPU, Qwen takes a few minutes for a short demo and tens of minutes for a long one. Kokoro speaks
faster than real time on a laptop CPU (about 0.2× the audio length per line), and a remote service is bounded by the
network and the provider. Re-runs after a caption change only speak the changed lines. `work/voice/` can grow to
hundreds of MB (WAV takes); delete it to start over.
