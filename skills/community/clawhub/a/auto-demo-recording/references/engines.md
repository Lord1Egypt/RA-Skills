# Narration engines

`demo_voice.py` speaks each caption with one of three kinds of engine. Which one is the story's `VOICE['engine']`
(or `work/voice/settings.json`, which wins); left empty, the first that can speak on this machine is taken:
Qwen on the GPU, then Kokoro on the CPU, then a remote service that has a key.

| Engine | Where | Needs | Languages | Voices | Speed control |
| --- | --- | --- | --- | --- | --- |
| `qwen` | local NVIDIA GPU | ~6.5 GB free VRAM, CUDA torch, `faster-qwen3-tts`, the two Qwen3-TTS 1.7B models | zh en ja ko de fr es it pt ru | 9 built-in speakers, cloned per video | yes (pace is fitted after the reference clip) |
| `kokoro` | local CPU | the Kokoro model (`demo_env.py setup --kokoro`, ~400 MB), `sherpa-onnx` | zh, en | v1.1: 100 Mandarin + 3 English; v1.0: 8 Mandarin + 28 English | yes (`GenerationConfig.speed`) |
| `openai` | remote | an OpenAI API key | 10 (voice-dependent) | `alloy ash ballad coral echo fable nova onyx sage shimmer verse marin cedar` | yes (`speed` 0.25–4) |
| `compatible` | remote | `base_url`, usually a key | as the service | as the service | as the service |
| `elevenlabs` | remote | an ElevenLabs key and a **voice id** | 10 (multilingual models) | the account's voices (ids) | yes (`voice_settings.speed` 0.7–1.2) |
| `dashscope` | remote | an Alibaba Cloud DashScope key | 10 | 48 voices (`Cherry`, `Serena`, `Ethan`, `Ono Anna`, …) | no: it speaks at its own pace |

## Choosing

- **The user has a local model that is ready → use it.** Qwen sounds best but needs the GPU; Kokoro runs anywhere.
- **The user offers an API key → use it.** Ask for the provider, the key, and (for ElevenLabs) the voice id; write
  `engine`, `speaker`, and if given `model` and `base_url` into `VOICE`. The key goes into the environment or
  `demo_env.py key <provider>=…`, never into the story file.
- **No narration wanted → do not run `demo_voice.py` at all.** The silent video is the deliverable.
- **A line the recogniser hears wrong** is fixed the same way on every engine: shorten the caption, add a `say`
  override, or re-speak that line. Kokoro additionally skips words its lexicon does not have: `demo_voice.py anchor`
  lists them before any line is spoken.

## Voices

### Qwen (`qwen`)

Nine speakers of the 1.7B CustomVoice model; the reference clip is made with one of them and every line is spoken as
a continuation of it, so the voice is fixed for the whole video.

| id | voice | id | voice |
| --- | --- | --- | --- |
| `serena` | female, warm (default zh) | `ryan` | male, bright (default en) |
| `vivian` | female, cool | `aiden` | male, American |
| `ono_anna` | female, playful (default ja) | `uncle_fu` | male, low |
| `sohee` | female, Korean feel (default ko) | `eric` | Sichuan dialect |
| | | `dylan` | Beijing dialect |

`speaker` may be written `Serena`, `ONO_ANNA` or `ono anna`; it is normalised. Only the nine exist — the larger
Qwen voice catalogue belongs to the DashScope service, not to the local model.

### Kokoro (`kokoro`)

`speaker` is a voice id such as `zf_039` or `af_maple`, or its number (`24` = `zf_039` in v1.1). Choosing a voice
by ear: `demo_voice.py lines` shows what is said; `voice/anchor` holds the reference clip; the check reports voice
drift. The defaults below were picked because a recogniser heard them right most often in testing:

| Language | v1.1 (recommended) | v1.0 |
| --- | --- | --- |
| zh | `zf_039` (female, 24) / `zm_013` (male, 62) | `zf_xiaoyi` |
| en | `af_maple` / `af_sol` / `bf_vale` | `af_bella` |

v1.1 is `kokoro-multi-lang-v1_1` (103 voices, Chinese + English). v1.0 has 54 voices and more English ones, but its
Mandarin is less reliable. English words missing from the lexicon are skipped silently by sherpa-onnx; the anchor
step warns about them, and `say` overrides fix them.

### Remote services

`openai` and `compatible` share one shape: `POST {base_url}/audio/speech` with `{model, voice, input,
response_format, speed?, instructions?}` and `Authorization: Bearer <key>`.

```python
VOICE = {'engine': 'openai', 'speaker': 'cedar', 'model': 'gpt-4o-mini-tts',
         'instructions': 'Speak calmly and clearly.'}

VOICE = {'engine': 'compatible', 'speaker': 'alloy', 'model': 'tts-1', 'base_url': 'http://127.0.0.1:8080/v1'}
```

OpenAI has deprecated the `/v1/audio/speech` models (shutdown announced for 2027-01-06); the endpoint is kept
because it is the shape most services copy. Set `model` to whatever the service offers.

`elevenlabs`: `POST {base_url}/{voice_id}?output_format=pcm_24000` with `xi-api-key`; `base_url` defaults to
`https://api.elevenlabs.io/v1/text-to-speech`, `model` to `eleven_multilingual_v2`. A voice id is required.

```python
VOICE = {'engine': 'elevenlabs', 'speaker': '21m00Tcm4TlvDq8ikWAM'}   # the public example voice, Rachel
```

`dashscope`: `POST {base_url}/api/v1/services/aigc/multimodal-generation/generation` with
`{model: qwen3-tts-flash, input: {text, voice, language_type}}`; the answer carries a URL to a WAV file that is
fetched right away. `base_url` defaults to `https://dashscope.aliyuncs.com`; use `https://dashscope-intl.aliyuncs.com`
for the international region.

```python
VOICE = {'engine': 'dashscope', 'speaker': 'Cherry', 'language_code': 'Chinese'}
```

Keys are looked up in this order: `VOICE['api_key']` (discouraged), `DEMO_TTS_API_KEY`, the provider's own variable
(`OPENAI_API_KEY`, `ELEVENLABS_API_KEY`, `DASHSCOPE_API_KEY`), then `secrets.json` under the skill home, written by:

```bash
python3 scripts/demo_env.py key openai=sk-…     # mode 600; `key --list` shows which are set, masked
```

## How the remote and CPU engines are driven

Qwen clones a voice from a reference clip, and `demo_voice.py` picks that clip (anchor → trial). The other engines
have a fixed voice per id, so the pipeline is shorter:

1. **anchor** — the reference text is spoken once at speed 1; its pace is measured, and later lines are asked for at
   the pace the captions want (`speed = 4.3 / measured`, clamped to 0.8–1.35; DashScope has no speed, so it keeps
   its own and lines that do not fit are sped up at the mixing, which `check` reports beyond 1.12).
2. **takes** — every line is spoken several times (6 for Qwen, 4 for Kokoro, 2 by default for a remote service: each
   call is a request, and possibly a bill).
3. **hear** — Whisper transcribes each take in the video's language; the text is compared with the script
   (`demo_text.differs`, word-aware for English and other spaced languages, syllable-aware for Mandarin), and CAM++
   compares the voice with the anchor clip.
4. **build / check** — as for Qwen: choose the take that says the text and fits its window, level, mix, then verify
   the finished file (same picture packets, same length, every line inside its caption, voice similarity, loudness).

Costs: a remote service sees one request per take plus one per check re-listen (local); a 60-second, 9-line video
with 2 takes is about 20 requests. Keep `takes` low for paid services.
