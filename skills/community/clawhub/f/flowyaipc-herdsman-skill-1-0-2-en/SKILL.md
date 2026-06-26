---
name: headsman-skill
description: Integration package for the Herdsman model engine. Used by other agent platforms to call scripts in this directory and protocol specifications when connecting to OpenAI, Anthropic, or AGUI-compatible services.
---

# Herdsman Skill

This directory is not a single script but an integration package for reuse by other agent platforms, enabling external agents to reliably access the Herdsman local model engine.

## Use Cases

- Other agent platforms need to use Herdsman as an OpenAI-compatible backend
- Platforms want to access Herdsman via the Anthropic Messages-compatible interface
- Platforms that support the AG-UI protocol need to connect to `/agui`
- Need to reliably call text, image, OCR, embedding, and speech capabilities without writing long JSON in shell

## Default Connection

- Service address: `http://127.0.0.1:8080`
- OpenAI root path: `http://127.0.0.1:8080/v1`
- Anthropic endpoint: `http://127.0.0.1:8080/v1/anthropic/messages`
- AGUI endpoint: `http://127.0.0.1:8080/agui`
- API Key: Empty by default; if configured, use `Authorization: Bearer <key>`

## Mandatory Rules

### 1. Do not construct complex `curl` commands directly

Do not construct complex prompts, tools, base64 images, or long-timeout tasks directly in the shell. Prefer using Python scripts under `scripts/`, or generate temporary Python files following the same pattern.

### 2. Run model discovery first

Before calling any model, always run:

```bash
python headsman-skill/scripts/check_model.py
```

If you know the model name, you can also:

```bash
python headsman-skill/scripts/check_model.py "<model_id>"
```

### 3. Long tasks must explicitly set longer timeouts

- Image generation, editing, img2img: recommended `timeout >= 120`
- OCR: recommended `timeout >= 120`
- Speech synthesis, recognition, streaming: recommended `timeout >= 120`
- Text chat: recommended `timeout >= 60`

### 4. Save image results to disk

If results will be reused in subsequent conversations, save them to `outputs/` and return the absolute path or cache URL to the user.

## Protocol Priority

### OpenAI Compatible

Preferred for:

- Chat completions
- Tool calls
- Embeddings
- Rerank
- Image generation / editing / img2img
- **OCR text recognition**
- Speech recognition / synthesis / streaming

Core endpoints:

- `GET /v1/models`
- `POST /v1/chat/completions`
- `POST /v1/embeddings`
- `POST /v1/rerank`
- `POST /v1/images/generations`
- `POST /v1/images/edits`
- `POST /v1/images/img2img`
- `GET  /v1/images/cache/:filename`
- **`POST /v1/ocr`**
- `POST /v1/audio/transcriptions`
- `GET  /v1/audio/transcriptions/stream?model=` (WebSocket)
- `POST /v1/audio/speech`
- `GET  /v1/audio/speech/stream/:token`
- `GET  /v1/audio/info?model=`

Additional parameters for chat completions (OpenAI Chat Completions compatible extensions):

| Parameter | Type | Description |
|-----------|------|-------------|
| `reasoning_effort` | string | Reasoning level: `low` / `medium` / `high`; local llama.cpp maps to template parameters |
| `thinking_enabled` | boolean | Enable or disable thinking mode for supported models; local llama.cpp maps to `enable_thinking` |
| `thinking_tokens` | number | Thinking token budget; local llama.cpp maps to `reasoning_budget` |

### Anthropic Compatible

For platforms that only support the Anthropic Messages style, the endpoint is:

- `POST /v1/anthropic/messages`

Therefore:

- If the platform supports custom full endpoints, it can connect directly
- If the SDK hardcodes `/v1/messages`, add a lightweight proxy on the platform side or use raw HTTP requests

### AGUI

For platforms supporting the AG-UI protocol event stream:

- `POST /agui`

AGUI is more suitable for protocol clients or SDKs; raw HTTP is not recommended. In the current state, `state` should at least provide `model`, and may optionally include `webSearch`, `tools`, `task_type`, `pass_through`.

## Recommended Scripts

- `scripts/herdsman_client.py`: General HTTP client wrapper
- `scripts/check_model.py`: Model discovery and filtering
- `scripts/chat_completion.py`: OpenAI chat completion (supports reasoning_effort / thinking)
- `scripts/generate_image.py`: Text-to-image generation with auto-download
- `scripts/edit_image.py`: Image editing with support for local files, URLs, masks, and additional reference images
- `scripts/img2img.py`: Image-to-image (style transfer, inpainting)
- **`scripts/ocr.py`: OCR text recognition, supports direct local image recognition**
- `scripts/transcribe_audio.py`: Speech transcription, supports local files, URLs, and data URLs
- `scripts/audio_speech.py`: Text-to-speech (TTS), supports VoiceDesign, VoiceClone, and streaming
- `scripts/anthropic_messages.py`: Anthropic Messages compatible invocation

## Directory Structure

- `references/api-examples.md`: Capability-based call examples
- `references/platform-integration.md`: OpenAI / Anthropic / AGUI integration guide
- `references/error-codes.md`: Common errors and agent-side handling strategies
- `references/model-capabilities.md`: Model capabilities and endpoint mapping
- `outputs/`: Recommended directory for saving generated images

## Best Practices

1. Use `check_model.py` first to get installed models
2. Choose OpenAI, Anthropic, or AGUI based on the platform protocol
3. Use Python scripts instead of shell concatenation for long tasks
4. Save image results as files or cache URLs, avoiding large base64 payloads
5. When encountering `model_not_found`, `model_not_installed`, `invalid_model_capability`, re-run model discovery
6. Speech transcription supports both JSON body (`audio` field) and `multipart/form-data` (`file` field)
7. Before OCR, use `check_model.py` to confirm `paddleocr-ppocrv5-server` or another OCR model is installed

## Speech Extension: TTS Voice Clone + ASR Standalone Transcription

The following three scripts are advanced speech tools integrated with Herdsman, supporting a full workflow from audio conversion to ASR transcription to voice cloning.

### Script Overview

| Script | Function | External Dependency |
|--------|----------|-------------------|
| `scripts/convert_audio.py` | Audio format conversion (any format to 16kHz WAV) | ffmpeg |
| `scripts/transcribe_standalone.py` | ASR speech transcription (pure urllib, no herdsman_client dependency) | Herdsman ASR model |
| `scripts/tts_voice_clone.py` | Voice cloning TTS synthesis | Herdsman qwen3-tts-voiceclone |

---

### convert_audio.py

Convert audio in any format (MP3/M4A/OGG, etc.) to 16kHz mono WAV. No Herdsman dependency.

```bash
uv run python scripts/convert_audio.py <input_path> [output_path]
```

**Parameters:**
- `input_path` — Path to the reference audio file
- `output_path` — Optional, defaults to same directory as input with `.wav` extension

**Examples:**
```bash
uv run python scripts/convert_audio.py ref.mp3
uv run python scripts/convert_audio.py ref.mp3 ref.wav
```

---

### transcribe_standalone.py

Standalone ASR transcription script (pure urllib, no dependency on `herdsman_client.py`). Dynamic model selection, supports absolute output paths.

```bash
uv run python scripts/transcribe_standalone.py <audio_path> --model <model_id> [--language <language>] [--output <absolute_path>]
```

**Parameters:**
- `audio_path` — Input audio file path (.wav/.mp3/.m4a, etc.)
- `--model` — ASR model ID (**required**, dynamic selection)
- `--language` — Language code (optional, auto-detect by default)
- `--output` / `-o` — Output file **absolute path**, writes both `.txt` + `.json` (optional, prints only if not specified)
- `--timeout` — Timeout in seconds (default 300)

**Tested model recommendations:**

| Model | Recommendation | Notes |
|-------|---------------|-------|
| `sherpa-onnx-paraformer-zh-small` | ⭐ Preferred | Simplified Chinese, preserves filler words, ~5s fastest |
| `whisper-base` | Alternative | General high accuracy, Traditional Chinese output |
| `funasr` | ⚠️ | WebSocket streaming only, HTTP not supported |
| `sherpa-onnx-streaming-zipformer-zh-14m` | ⚠️ | Streaming only, HTTP does not support full transcription |

**Examples:**
```bash
# Recommended
uv run python scripts/transcribe_standalone.py audio.wav --model sherpa-onnx-paraformer-zh-small --output "D:/result.txt"
# Print only
uv run python scripts/transcribe_standalone.py audio.wav --model whisper-base
```

---

### tts_voice_clone.py

Voice cloning TTS synthesis using `qwen3-tts-voiceclone`. Three dynamic parameters: reference audio WAV, original text, target script.

```bash
uv run python scripts/tts_voice_clone.py <ref_audio_wav> <ref_text> <target_text> [--output <path>]
```

**Parameters:**
- `ref_audio_wav` — 16kHz mono WAV path
- `ref_text` — Original text corresponding to the reference audio
- `target_text` — Target text to be synthesized with cloned voice
- `--output` / `-o` — Output audio path (default `ripple_tts_cloned.wav`)
- `--timeout` — Timeout in seconds (default 180)

**Examples:**
```bash
uv run python scripts/tts_voice_clone.py ref.wav "original text" "target synthesis text" -o output.wav
```

---

### Full Workflow

```bash
# 1. Convert to WAV
uv run python scripts/convert_audio.py source.mp3 ref.wav

# 2. ASR transcription (extract audio text for comparison)
uv run python scripts/transcribe_standalone.py ref.wav --model sherpa-onnx-paraformer-zh-small --output "D:/transcribed.txt"

# 3. Voice clone synthesis
uv run python scripts/tts_voice_clone.py ref.wav "original text" "target synthesis text" -o final.wav
```

### Notes

- Reference audio recommended 10-60 seconds, low background noise, natural speech rate
- The original text must **exactly match** the audio content, otherwise cloning quality is affected
- ASR transcription supports **absolute paths** via `--output` for cross-directory use
- Error messages output to stderr, normal results output to stdout
