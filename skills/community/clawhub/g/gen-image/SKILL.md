---
name: gen-image
description: AI生成图片，支持Kolors/FLUX/Qwen-Image等模型（需SiliconFlow API）
homepage: https://siliconflow.cn
metadata: {"openclaw":{"emoji":"🎨","requires":{"bins":["curl"],"env":["SILICONFLOW_API_KEY"]},"primaryEnv":"SILICONFLOW_API_KEY"}}
---

# AI 图片生成

使用 SiliconFlow API 调用 Kolors、FLUX、Qwen-Image 等模型生成图片。

## Generate Image

```bash
curl -X POST "https://api.siliconflow.cn/v1/images/generations" \
  -H "Authorization: Bearer $SILICONFLOW_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "Kolors/Kolors",
    "prompt": "your image description",
    "image_size": "1024x1024",
    "num_inference_steps": 20
  }'
```

## Available Models

- `Kwai-Kolors/Kolors` - High quality image generation (正确ID)
- `black-forest-labs/FLUX.1-schnell` - Fast generation
- `black-forest-labs/FLUX.1-dev` - FLUX dev version
- `Qwen/Qwen-Image` - Qwen image generation

> 注意：模型ID可能更新，可通过 `curl -s "https://api.siliconflow.cn/v1/models" -H "Authorization: Bearer $SILICONFLOW_API_KEY" | jq '.data[].id'` 查询最新列表

## Parameters

- `prompt`: Image description (required)
- `image_size`: `1024x1024`, `1024x1792`, `1792x1024` (default: 1024x1024)
- `num_inference_steps`: 1-50 (default: 20)
- `negative_prompt`: Things to avoid (optional)
- `seed`: Random seed (optional)

## API Key

Get your API key from: https://cloud.siliconflow.cn

Set environment variable:
```bash
export SILICONFLOW_API_KEY="your-api-key"
```

Or configure in OpenClaw:
```json5
{
  skills: {
    entries: {
      "siliconflow-image": {
        enabled: true,
        env: {
          SILICONFLOW_API_KEY: "your-api-key"
        }
      }
    }
  }
}
```