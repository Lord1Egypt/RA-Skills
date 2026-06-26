# Recraft V4 Pro (fal.ai)

## Model

| Model | Endpoint | Description |
|-------|----------|-------------|
| Recraft V4 Pro | `fal-ai/recraft/v4/pro/text-to-image` | Design & marketing focused, color control |

## Input Schema

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `prompt` | string | ✅ | — | Text prompt |
| `image_size` | ImageSize/enum | | `"square_hd"` | `square_hd`, `square`, `portrait_4_3`, `portrait_16_9`, `landscape_4_3`, `landscape_16_9` or `{"width": W, "height": H}` |
| `colors` | list[RGBColor] | | — | Preferable colors array (e.g. `[{"r": 255, "g": 0, "b": 0}]`) |
| `background_color` | RGBColor | | — | Preferable background color |
| `enable_safety_checker` | boolean | | `true` | |

## Output Schema

```json
{
  "images": [{"url": "https://...", "width": 1024, "height": 1024, "content_type": "image/jpeg"}]
}
```

## Python Example

```python
import fal_client
result = fal_client.subscribe("fal-ai/recraft/v4/pro/text-to-image", arguments={
    "prompt": "Minimalist product packaging for organic tea, clean typography",
    "image_size": "landscape_16_9",
    "colors": [{"r": 34, "g": 139, "b": 34}],
    "background_color": {"r": 255, "g": 255, "b": 255},
})
```
