# Herdsman Error Code Reference

## Unified Error Format

OpenAI compatible endpoints typically return:

```json
{
  "error": {
    "message": "Error description",
    "type": "error type",
    "code": "error code"
  }
}
```

Anthropic compatible endpoints also return structured errors, but field names may differ slightly. For agents, prefer reading:

1. HTTP status code
2. `error.code`
3. `error.message`

## Common Error Codes

### Model Related

| Code | HTTP Status | Meaning | Agent Handling |
|------|-------------|---------|----------------|
| `model_not_found` | 404 | Model does not exist | Re-run `check_model.py`, correct the model name |
| `model_not_installed` | 400 | Model not installed | Prompt the platform or user to install the model first |
| `model_start_failed` | 500 | Model failed to start | Usually related to VRAM, memory, or runtime initialization failure |
| `invalid_model_type` | 400 | Model type mismatch | Switch to the correct model type, e.g., do not use an embedding model for chat |
| `invalid_model_capability` | 400 | Model capability not supported | Switch to a model that supports the required capability |
| `model_not_exists` | 400 | Model does not exist or is in an abnormal state | Fall back to model list and rediscover |

### Request Related

| Code | HTTP Status | Meaning | Agent Handling |
|------|-------------|---------|----------------|
| `invalid_request` | 400 | Request body format error | Check JSON, field names, required parameters |
| `invalid_request_error` | 400 | Generic request error | Read `message` to locate the issue |
| `invalid_filename` | 400 | Invalid filename | Use only valid output names |
| `invalid_path` | 400 | Invalid path | Ensure an absolute path is passed and the file exists |

### OCR Related

| Code | HTTP Status | Meaning | Agent Handling |
|------|-------------|---------|----------------|
| `invalid_image_format` | 400 | Image format not supported | Convert to PNG/JPG or other common formats |
| `invalid_image_data` | 400 | Image data decoding failed | Check if base64 encoding is correct or image is corrupted |
| `ocr_engine_error` | 500 | OCR engine internal error | Check if the model is installed and working; retry once |

### Audio / Speech Related

| Code | HTTP Status | Meaning | Agent Handling |
|------|-------------|---------|----------------|
| `invalid_audio_format` | 400 | Audio format not supported | Convert to WAV/PCM16 or check documentation |
| `language_not_supported` | 400 | Language code not supported | Query supported languages via `/v1/audio/info?model=` |
| `speaker_not_found` | 400 | Specified speaker does not exist | Query supported speakers via `/v1/audio/info?model=` |
| `voice_description_error` | 400 | VoiceDesign mode parameter error | Check voice_description format |

### Runtime & Server

| Code | HTTP Status | Meaning | Agent Handling |
|------|-------------|---------|----------------|
| `internal_error` | 500 | Internal service error | Treat as service exception, retry once later |
| `server_error` | 500 | Generic server error | Read message and log it |
| `runtime_error` | 500 | Inference runtime error | Check if model can start or backend is available |
| `runtime_not_supported` | 400 | Current backend does not support this capability | Change model or switch capability |

### Generation Result Related

| Code | HTTP Status | Meaning | Agent Handling |
|------|-------------|---------|----------------|
| `generation_failed` | 500 | Generation task failed | Degrade parameters appropriately and retry once |
| `cache_error` | 500 | Cache or disk write failed | Check disk permissions, temp directory, and space |

## Recommended Troubleshooting Order

### 1. Check HTTP Status Code First

- `400`: Request parameter or model capability mismatch
- `404`: Usually wrong model name
- `500`: Usually model startup, runtime, or service state anomaly

### 2. Then Check Error Code

- `model_not_found`: Re-run model discovery first
- `invalid_model_capability`: Model exists but capability is wrong
- `model_start_failed`: Model exists but failed to start

### 3. Finally Read message

`message` often provides actionable clues, such as:

- Insufficient VRAM
- Model not installed
- Runtime not supported
- Missing request field

## Agent Handling Strategies

### May Silently Retry Once

- `internal_error`
- `server_error`
- `generation_failed`
- `ocr_engine_error`

### Should Not Blindly Retry

- `model_not_found`
- `model_not_installed`
- `invalid_model_type`
- `invalid_model_capability`
- `invalid_request`
- `invalid_audio_format`
- `invalid_image_format`
- `invalid_image_data`
- `language_not_supported`
- `speaker_not_found`

### Typical Handling Flow

1. If model error, run `check_model.py` first
2. If capability mismatch, change the model instead of retrying
3. If audio error, query `/v1/audio/info?model=` to confirm capabilities first
4. If image or speech long task fails, degrade parameters and retry once
5. If OCR error, confirm image format and base64 encoding are correct first
6. If consecutive failures, report "local compute service is currently experiencing abnormal responses"

## Examples

### Chat interface incorrectly used an embedding model

```json
{
  "error": {
    "message": "Model type 'embedding' is not supported for chat completions. Only text-generation models are supported.",
    "type": "invalid_request_error",
    "code": "invalid_model_type"
  }
}
```

Handling: Switch to a text generation or multimodal model.

### Image editing capability missing

```json
{
  "error": {
    "message": "Model 'stable-diffusion-v3' does not support image editing. Use models with 'image-edit' capability.",
    "type": "invalid_request_error",
    "code": "invalid_model_capability"
  }
}
```

Handling: Switch to a model that supports `image-edit`.

### Model startup failed

```json
{
  "error": {
    "message": "Failed to start model: out of memory",
    "type": "server_error",
    "code": "model_start_failed"
  }
}
```

Handling: Check VRAM, memory, and runtime status first; do not retry indefinitely.

### Language not supported

```json
{
  "error": {
    "message": "Language 'fr' is not supported for this model",
    "type": "invalid_request_error",
    "code": "language_not_supported"
  }
}
```

Handling: Query `/v1/audio/info?model=whisper-base` to confirm supported languages.

### OCR image format error

```json
{
  "error": {
    "message": "Invalid image format. Supported formats: PNG, JPG, BMP, TIFF",
    "type": "invalid_request_error",
    "code": "invalid_image_format"
  }
}
```

Handling: Convert the image to PNG or JPG and retry.
