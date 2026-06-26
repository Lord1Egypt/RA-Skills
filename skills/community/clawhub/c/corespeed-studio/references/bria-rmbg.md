# Background Removal — BRIA RMBG 2.0 (fal.ai)

## Model

| Model | Endpoint | Description |
|-------|----------|-------------|
| BRIA RMBG 2.0 | `fal-ai/bria/background/remove` | Professional background removal |

## Input Schema

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `image_url` | string | ✅ | — | Image URL |

## Output Schema

```json
{"image": {"url": "https://..."}}
```

Returns a PNG with transparent background.

## Python Example

```python
import fal_client
result = fal_client.subscribe("fal-ai/bria/background/remove", arguments={
    "image_url": "https://example.com/product.jpg",
})
image_url = result["image"]["url"]
```
