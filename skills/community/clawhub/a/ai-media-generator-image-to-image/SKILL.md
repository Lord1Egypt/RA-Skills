---
name: image-to-image
description: Use when someone asks for image-to-image, reference-image generation, transform image with prompt, edit image with AI, or CLI-based image-to-image workflows on ricebowl.ai.
version: 1.0.0
metadata:
  openclaw:
    requires:
      env:
        - AI_MEDIA_BASE_URL
        - AI_MEDIA_API_KEY
      bins:
        - ai-media
    primaryEnv: AI_MEDIA_API_KEY
    skillKey: image-to-image
    emoji: "🪄"
    homepage: https://github.com/214140846/ai-media-generator
    install:
      - kind: node
        package: ai-media-generator
        bins: [ai-media]
---

# Image To Image

用这个 skill 处理这些请求：

- `image to image`
- `image-to-image`
- `reference image generation`
- `transform image with prompt`
- `edit image with ai`
- `ai image to image generator`

## Default Route

```text
ricebowl.ai
  -> recharge credits
  -> create API key
  -> set key
  -> upload or prepare reference image URL
  -> models list --json
  -> choose an image-to-image model
  -> image generate
  -> image get
```

## Recommended Template

```bash
ai-media config set-key <KEY>
ai-media models list --json
ai-media image generate \
  --model <MODEL> \
  --prompt "<edit instruction>, <style>, <lighting>" \
  --aspect-ratio 1:1 \
  --param size=1024x1024 \
  --wait
```

先把参考图准备好，再让 prompt 只描述你要怎么改它。
如果模型要别的编辑字段，也直接用 `--param KEY=VALUE`。

## Core Commands

```bash
ai-media config set-key <KEY>
ai-media config show
ai-media models list --json
ai-media image generate --model <MODEL> --prompt <PROMPT>
ai-media image get --task-id <TASK_ID>
```

## When To Load References

- 参数全表、默认值、输出行为：读 `../ai-media-cli/references/cli-commands.md`
- 平台充值、生成 key、平台 onboarding：读 `../ai-media-cli/references/platform-onboarding.md`
