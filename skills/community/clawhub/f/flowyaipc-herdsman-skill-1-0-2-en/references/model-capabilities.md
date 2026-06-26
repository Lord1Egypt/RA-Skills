# Herdsman Model Capabilities

## Before You Start

Other agent platforms should not assume model names or capabilities. Follow this order:

1. Run `scripts/check_model.py` first
2. Get the list of installed models from `GET /v1/models`
3. Match model types based on target capability

## Model Types & Recommended Endpoints

| Model Type | Recommended Endpoint | Typical Use |
|------------|---------------------|-------------|
| `text-generation` | `/v1/chat/completions` | General chat, summarization, structured output |
| `multimodal` | `/v1/chat/completions` | Text chat, image understanding |
| `embedding` | `/v1/embeddings` | Vectorization, retrieval indexing |
| `reranking` | `/v1/rerank` | Reranking, post-retrieval refinement |
| `image-generation` | `/v1/images/generations` | Text-to-image |
| `image-edit` | `/v1/images/edits` | Image editing, local modification |
| `image-to-image` | `/v1/images/img2img` | Image-to-image, style transfer |
| **`ocr`** | **`/v1/ocr`** | **Image text recognition** |

## Typical Capability Mapping

### Text

| Capability | Recommended Endpoint | Notes |
|------------|---------------------|-------|
| Text generation | `/v1/chat/completions` | Most common entry point |
| Tool calling | `/v1/chat/completions` | Pass via `tools` field |
| Vision understanding | `/v1/chat/completions` | Multimodal models only |
| Reasoning / Thinking | `/v1/chat/completions` | Via `reasoning_effort` / `thinking_enabled` parameters |

### Embedding & Rerank

| Capability | Recommended Endpoint | Notes |
|------------|---------------------|-------|
| Text embedding | `/v1/embeddings` | Text to vector |
| Document rerank | `/v1/rerank` | Post-retrieval refinement |

### Image

| Capability | Recommended Endpoint | Notes |
|------------|---------------------|-------|
| Text-to-image | `/v1/images/generations` | Generate images from text |
| Image editing | `/v1/images/edits` | Local editing, mask scenarios |
| Image-to-image | `/v1/images/img2img` | Style transfer, full repaint |
| Image cache | `GET /v1/images/cache/:filename` | Retrieve cached image files |

### OCR

| Capability | Recommended Endpoint | Notes |
|------------|---------------------|-------|
| **Image text recognition** | **`POST /v1/ocr`** | **Recognize text in images, returns full page text, per-line results, confidence, and bounding box coordinates** |

### Audio

| Capability | Recommended Endpoint | Notes |
|------------|---------------------|-------|
| Speech transcription | `POST /v1/audio/transcriptions` | Speech to text (JSON body or multipart) |
| Streaming ASR | `GET /v1/audio/transcriptions/stream?model={model}` | WebSocket real-time ASR |
| Speech synthesis | `POST /v1/audio/speech` | Text to audio |
| Streaming TTS | `POST + GET /v1/audio/speech/stream/:token` | Streaming TTS (create then pull) |
| Audio service info | `GET /v1/audio/info?model={model}` | Query supported speakers, languages, etc. |

## OCR Endpoint Details

`POST /v1/ocr` recognizes text in images.

### Supported Models

| Model | Description |
|-------|-------------|
| `paddleocr-ppocrv5-server` | PaddleOCR PP-OCRv5 Server text detection and recognition model |

### Request Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `model` | string | ✓ | OCR model name |
| `image_base64` | string | ✓ | Base64 image data, supports pure base64 or `data:image/...;base64` format |

### Response Fields

| Field | Type | Description |
|-------|------|-------------|
| `text` | string | Recognized full page text |
| `lines` | array | Per-line recognition results |
| `lines[].text` | string | Single line text |
| `lines[].score` | float | Confidence (0-1) |
| `lines[].box` | array | Bounding box coordinates `[[x1,y1],[x2,y1],[x2,y2],[x1,y2]]` |
| `image_width` | number | Image width |
| `image_height` | number | Image height |
| `elapsed_ms` | number | Recognition time (milliseconds) |

### Usage Tips

- OCR tasks recommended timeout >= 120s
- Recommended to use `scripts/ocr.py` for calling, which handles image reading and base64 encoding automatically
- Can also be called via `HerdsmanClient.ocr()` or `HerdsmanClient.ocr_image_file()` in Python code

## Speech Synthesis Parameters

Parameters supported by `POST /v1/audio/speech`:

| Parameter | Type | Description |
|-----------|------|-------------|
| `input` | string | **Required** Input text |
| `model` | string | **Required** Model ID |
| `voice` | string | Voice name (e.g., Cherry, zh-CN-YunxiNeural) |
| `speaker` | string | Speaker ID (uses voice if not set) |
| `voice_description` | string | VoiceDesign mode: natural language voice description |
| `ref_audio` | string | VoiceClone mode: reference audio (path/URL/base64) |
| `ref_text` | string | VoiceClone mode: reference audio text |
| `language` | string | Language code or name (e.g., Chinese, English) |
| `speed` | number | Speech speed (default 1.0) |
| `stream` | boolean | Returns stream_url if true |

## Speech Recognition Notes

`POST /v1/audio/transcriptions` supports two transmission methods:

- **JSON body**: Pass data URL or path/URL via the `audio` field
- **multipart/form-data**: Upload audio file via the `file` field

Streaming recognition connects via WebSocket to `/v1/audio/transcriptions/stream?model={model}`; the client sends PCM16/16k mono binary frames, and the server returns `{"text":"...","is_final":false}`.

## Capability Matching Guide

### For Chat, Agent Reasoning, Tool Calling

Prefer:

- `text-generation`
- `multimodal`

Avoid:

- `embedding`
- `reranking`
- Pure image models

### For Vector Database, RAG Indexing

Prefer:

- `embedding` (vectorization)
- `reranking` (rerank)

### For Image Generation

Prefer models with image generation capabilities, and distinguish:

- Text-to-image only: use `/v1/images/generations`
- Local modification: use `/v1/images/edits`
- Style transfer or full repaint: use `/v1/images/img2img`

### For OCR Text Recognition

- Currently recommended: `paddleocr-ppocrv5-server` model
- Use `POST /v1/ocr` endpoint
- Recommended timeout >= 120s
- Supports PNG, JPG, and other common image formats

### For Audio Processing

- Transcription: choose ASR models (e.g., whisper-base, funasr, qwen3-asr)
- Synthesis: choose TTS models (e.g., edge-tts, qwen3-tts-customvoice)
- Query `/v1/audio/info?model=` first to confirm capabilities before sending requests

## Runtime Differences

Different backends have varying capabilities. Integration parties should accept that "a model exists but the current runtime does not support a certain capability."

| Runtime | Text Gen | Image Gen | OCR | Audio | Embedding |
|---------|----------|-----------|-----|-------|-----------|
| `llama.cpp` | Usually supported | Usually not | Not supported | Usually not | Partial |
| `foundry-local` | Supported | May support | May support | Depends on model | May support |
| `funasr` | Not suitable for chat | Not supported | Not supported | Supported | Not supported |
| `sd-cpp` / `zimage-ov` / `comfyui` | Not suitable for chat | Supported | Not supported | Not supported | Not supported |
| `paddleocr` | Not suitable for chat | Not supported | **Supported** | Not supported | Not supported |

## Common Errors & Meanings

### `invalid_model_type`

The model type is wrong. For example, using an embedding model to call the chat endpoint.

### `invalid_model_capability`

The model category may be correct, but the specific capability is wrong. For example, using a text-to-image-only model for image editing.

### `model_not_installed`

The model may exist in the registry but is not yet installed on the machine.

### `language_not_supported` / `speaker_not_found`

The language or speaker queried via `/v1/audio/info?model=` does not exist for that model.

## Integration Suggestions

- Text-only platform: only expose text model list to the upper layer
- Image-only platform: only expose image model list to the upper layer
- If the platform auto-discovers models, use `/v1/models` results as the source of truth
- Do not hardcode model names in the skill; prefer runtime discovery
- Before speech-related calls, query `/v1/audio/info?model=` first
- Before OCR calls, confirm `paddleocr-ppocrv5-server` or another OCR model is installed
