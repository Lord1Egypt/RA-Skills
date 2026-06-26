# Herdsman Platform Integration Guide

This document addresses "how other agent platforms can integrate Herdsman."

## 1. OpenAI Compatible Platforms

This is the most recommended integration method.

### Configuration

- `base_url`: `http://127.0.0.1:8080/v1`
- `api_key`: Leave empty if not configured; pass `Bearer` Token if configured

### Suitable Platforms

- Chat platforms that support custom OpenAI Base URL
- Platforms that support function calling or tool calling
- IDE agents that support custom local LLM endpoints

### Recommended Flow

1. Use `GET /v1/models` for model discovery
2. Select a text model as the default chat model
3. Select image models separately for image capabilities, do not mix
4. Use dedicated models for audio capabilities

### Minimal Example

```python
from herdsman_client import HerdsmanClient

client = HerdsmanClient(base_url="http://127.0.0.1:8080")
models = client.list_models()
print(models)
```

## 2. Anthropic Compatible Platforms

Herdsman already provides an Anthropic Messages compatible endpoint, but the path is:

- `http://127.0.0.1:8080/v1/anthropic/messages`

### Notes

- This is not the official default `/v1/messages`
- If the upstream platform must use `/v1/messages`, a forwarding proxy is needed
- If the platform supports custom full endpoints, it can be used directly

### Recommended Scenarios

- The platform SDK internally uses Anthropic format for packaging
- You prefer not to rewrite message mapping logic to OpenAI format

### Minimal Example

```bash
python headsman-skill/scripts/anthropic_messages.py "Please summarize the following content" --model qwen2.5-7b-instruct
```

## 3. AGUI Platforms

Herdsman exposes:

- `POST /agui`

This is more suitable for AG-UI protocol clients rather than hand-writing HTTP requests.

### Confirmed Key State Fields

`state` should include:

- `model`: Required, model name
- `webSearch`: Optional, boolean
- `tools`: Optional, array of strings
- `task_type`: Optional, task type
- `pass_through`: Optional, extension parameter object

### Integration Tips

- If the platform already has an AG-UI SDK, prefer using the SDK
- If not, prefer the OpenAI compatible endpoint over direct raw connection to `/agui`
- `model` must use a text or multimodal model name synchronized to the Herdsman local registry

## 4. Model Selection Guide

### Text Tasks

- Select text models from the `GET /v1/models` list
- Do not use embedding, rerank, or image models for chat

### Embedding & Rerank

- Embedding models go through `/v1/embeddings`
- Rerank models go through `/v1/rerank`

### Image Tasks

- Confirm image models are installed first
- Distinguish models for text-to-image, image editing, and img2img based on capability

### Audio Tasks

- Transcription and synthesis typically require longer timeouts
- The platform side must allow binary or streaming result return
- Use `/v1/audio/info?model=` to query TTS speakers and ASR supported languages

## 5. API Key Policy

The `api.api_key` in the default configuration can be empty.

If non-empty, the platform side should add:

```text
Authorization: Bearer <api_key>
```

## 6. Troubleshooting

### Platform Cannot Connect

- Check if the service is running on `127.0.0.1:8080`
- Check if the base URL is correct
- OpenAI platforms should point to `/v1`

### Model Name Not Found

- Run `scripts/check_model.py` first
- Do not rely on historically hardcoded model names

### Anthropic Platform Not Working

- Check if it allows custom full endpoints
- If only `/v1/messages` is allowed, add a forwarding layer

### AGUI Platform Call Fails

- Confirm `state.model` is passed correctly
- Confirm the platform is actually compatible with the AG-UI event protocol

### TTS / ASR Not Working

- Use `scripts/check_model.py` to confirm the model exists
- Use `/v1/audio/info?model=` to query model capabilities
- Check if timeout is long enough (recommended >= 120s)
