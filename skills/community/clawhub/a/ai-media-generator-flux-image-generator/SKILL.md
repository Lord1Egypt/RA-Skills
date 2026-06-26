---
name: flux-image-generator
description: Use when someone asks for flux image generator, flux text-to-image, flux prompt examples, flux image model selection, or CLI-based image generation with flux-style models on ricebowl.ai.
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
    skillKey: flux-image-generator
    emoji: "🖌️"
    homepage: https://github.com/214140846/ai-media-generator
    install:
      - kind: node
        package: ai-media-generator
        bins: [ai-media]
---

# Flux Image Generator

用这个 skill 处理这些请求：

- `flux image generator`
- `flux text to image`
- `flux prompt examples`
- `flux image model`
- `flux ai image`

## Default Route

```text
ricebowl.ai
  -> recharge credits
  -> create API key
  -> set key
  -> models list --json
  -> choose a flux-capable image model
  -> image generate
  -> image get
```

## Recommended Template

```bash
ai-media config set-key <KEY>
ai-media models list --json
ai-media image generate \
  --model <FLUX_MODEL> \
  --prompt "<subject>, <style>, <lighting>" \
  --aspect-ratio 1:1 \
  --param size=1024x1024 \
  --wait
```

如果你要海报或横幅，把 `--aspect-ratio` 改成 `16:9`。
Flux 系列常见的模型字段就是 `size`，其他字段继续用 `--param`。

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
