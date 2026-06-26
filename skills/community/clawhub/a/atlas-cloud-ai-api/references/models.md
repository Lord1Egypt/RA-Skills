# Atlas Cloud — Model Reference & Selection Guide

Read this file when you need the full model list, pricing details, or help choosing a model.

## Always Verify Model IDs

Model IDs update frequently. **Never guess or hardcode without verification.** Fetch the latest list:

```
GET https://console.atlascloud.ai/api/v1/models
```

No authentication required. Returns all models with exact `model` ID, `type`, `displayName`, `price`, and `schema` URL.

**Important:** Only models with `display_console: true` are publicly available.

---

## Image Models (priced per image)

| Model ID | Name | Price |
|----------|------|-------|
| `google/nano-banana-2/text-to-image` | Nano Banana 2 Text-to-Image | $0.072 |
| `google/nano-banana-2/text-to-image-developer` | Nano Banana 2 Developer | $0.056 |
| `google/nano-banana-2/edit` | Nano Banana 2 Edit | $0.072 |
| `google/nano-banana-2/edit-developer` | Nano Banana 2 Edit Developer | $0.056 |
| `bytedance/seedream-v5.0-lite` | Seedream v5.0 Lite | $0.032 |
| `bytedance/seedream-v5.0-lite/edit` | Seedream v5.0 Lite Edit | $0.032 |
| `bytedance/seedream-v5.0-lite/sequential` | Seedream v5.0 Lite Sequential | $0.032 |
| `alibaba/qwen-image/edit-plus-20251215` | Qwen-Image Edit Plus | $0.021 |
| `alibaba/wan-2.6/image-edit` | Wan-2.6 Image Edit | $0.021 |
| `z-image/turbo` | Z-Image Turbo | $0.01 |
| `bytedance/seedream-v4.5` | Seedream v4.5 | $0.036 |

## Video Models (priced per generation)

| Model ID | Name | Price |
|----------|------|-------|
| `kwaivgi/kling-v3.0-std/text-to-video` | Kling v3.0 Std T2V | $0.153 |
| `kwaivgi/kling-v3.0-std/image-to-video` | Kling v3.0 Std I2V | $0.153 |
| `kwaivgi/kling-v3.0-pro/text-to-video` | Kling v3.0 Pro T2V | $0.204 |
| `kwaivgi/kling-v3.0-pro/image-to-video` | Kling v3.0 Pro I2V | $0.204 |
| `bytedance/seedance-v1.5-pro/text-to-video` | Seedance 1.5 Pro T2V | $0.222 |
| `bytedance/seedance-v1.5-pro/image-to-video` | Seedance 1.5 Pro I2V | $0.222 |
| `bytedance/seedance-v1.5-pro/image-to-video-fast` | Seedance 1.5 Pro I2V Fast | $0.018 |
| `vidu/q3/text-to-video` | Vidu Q3 T2V | $0.06 |
| `vidu/q3/image-to-video` | Vidu Q3 I2V | $0.06 |
| `alibaba/wan-2.6/image-to-video` | Wan-2.6 I2V | $0.07 |
| `alibaba/wan-2.6/image-to-video-flash` | Wan-2.6 I2V Flash | $0.018 |
| `kwaivgi/kling-v2.6-pro/avatar` | Kling v2.6 Pro Avatar | $0.095 |
| `kwaivgi/kling-v2.6-std/avatar` | Kling v2.6 Std Avatar | $0.048 |

## LLM Models (per million tokens)

| Model ID | Name | Input | Output |
|----------|------|-------|--------|
| `qwen/qwen3.5-397b-a17b` | Qwen3.5 397B A17B | $0.55 | $3.50 |
| `qwen/qwen3.5-122b-a10b` | Qwen3.5 122B A10B | $0.30 | $2.40 |
| `qwen/qwen3.5-35b-a3b` | Qwen3.5 35B A3B | $0.225 | $1.80 |
| `qwen/qwen3.5-27b` | Qwen3.5 27B | $0.27 | $2.16 |
| `qwen/qwen3-coder-next` | Qwen3 Coder Next | $0.18 | $1.35 |
| `moonshotai/kimi-k2.5` | Kimi K2.5 | $0.50 | $2.60 |
| `zai-org/glm-5` | GLM 5 | $0.95 | $3.15 |
| `zai-org/glm-4.7` | GLM 4.7 | $0.52 | $1.75 |
| `minimaxai/minimax-m2.5` | MiniMax M2.5 | $0.295 | $1.20 |
| `minimaxai/minimax-m2.1` | MiniMax M2.1 | $0.29 | $0.95 |
| `deepseek-ai/deepseek-v3.2-speciale` | DeepSeek V3.2 Speciale | $0.40 | $1.20 |
| `qwen/qwen3-max-2026-01-23` | Qwen3 Max | $1.20 | $6.00 |

---

## Model Type → Endpoint Mapping

| Type | Endpoint |
|------|----------|
| `"Image"` | `POST https://api.atlascloud.ai/api/v1/model/generateImage` |
| `"Video"` | `POST https://api.atlascloud.ai/api/v1/model/generateVideo` |
| `"Text"` | `POST https://api.atlascloud.ai/v1/chat/completions` |

---

## Price Structure (API Response)

The price field in the API response has this structure:

- **Image/Video models**: Use `price.actual.base_price` — cost per generation
- **LLM models**: Use `price.actual.input_price` and `price.actual.output_price` — cost per million tokens
- Fallback chain: `price.actual` → `price.sku.text` → top-level `inputPrice`/`basePrice`
- `price.discount`: Discount percentage (e.g., "85" means 85% of original price = 15% off)

---

## Model Schema

Each model has a `schema` field pointing to an OpenAPI JSON file describing all available parameters:

```python
import requests

# Fetch public model list
models = requests.get("https://console.atlascloud.ai/api/v1/models").json()["data"]
public_models = [m for m in models if m.get("display_console") == True]

# Find a specific model
model = next(m for m in public_models if m["model"] == "bytedance/seedream-v5.0-lite")

# Fetch parameter schema
if model.get("schema"):
    schema = requests.get(model["schema"]).json()
    # schema["components"]["schemas"]["Input"]["properties"] contains all available parameters
```

---

## Model Selection Guide

| Use Case | Recommended Model | Why |
|----------|-------------------|-----|
| **Cheapest image** | `z-image/turbo` ($0.01) | Ultra-low cost, good for prototyping |
| **Best quality image** | `google/nano-banana-2/text-to-image` ($0.072) | Google Imagen quality |
| **Budget image** | `bytedance/seedream-v5.0-lite` ($0.032) | Great quality at low cost |
| **Image editing** | `google/nano-banana-2/edit` or `alibaba/qwen-image/edit-plus-20251215` | Full edit with references |
| **Budget video** | `vidu/q3/text-to-video` ($0.06) or `alibaba/wan-2.6/image-to-video-flash` ($0.018) | Lowest cost video |
| **Best quality video** | `kwaivgi/kling-v3.0-pro/text-to-video` ($0.204) | Cinematic quality |
| **Video with audio** | `bytedance/seedance-v1.5-pro/text-to-video` ($0.222) | Native audio-visual sync |
| **Avatar animation** | `kwaivgi/kling-v2.6-pro/avatar` ($0.095) | Talking head specialist |
| **Best LLM** | `qwen/qwen3.5-397b-a17b` ($0.55/$3.50/M) | Flagship 397B MoE |
| **Cheapest LLM** | `minimaxai/minimax-m2.1` ($0.29/$0.95/M) | Low cost, good quality |
| **Code generation** | `qwen/qwen3-coder-next` ($0.18/$1.35/M) | Code specialist |
| **Strong reasoning** | `moonshotai/kimi-k2.5` ($0.50/$2.60/M) | Best reasoning performance |
