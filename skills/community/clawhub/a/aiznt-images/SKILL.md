---
name: aiznt-images
description: >
  通用图生图（OpenAI 风格）与 Gemini generateContent 文生图。Use when: 文生图、异步出图、Gemini 图像模型。
metadata:
  openclaw:
    primaryEnv: TS_TOKEN
    requires:
      env:
        - AIZNT_PROXY_URLS
---

# 图生图 (aiznt-images)

## 命令

```bash
node scripts/images.js sync --body '{"prompt":"...","model":"..."}'
node scripts/images.js async --body '{...}'
node scripts/images.js async-fetch --task-id <id>
node scripts/images.js generate-content --model gemini-3-pro-image-preview --body '{...}'
```

## URL 键

- `v1_images_generations`
- `v1_images_generations_async`
- `v1_images_generations_async_fetch`（`{task_id}`）
- `v1_models_generate_content`（`{model}`）

配置同其它 aiznt-*：TsClaw「同步天树凭证」批量写入。
