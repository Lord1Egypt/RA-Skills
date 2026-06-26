---
name: ai-image-generation
description: Use when someone asks for ai image generation, image generator, text-to-image, image-to-image, prompt-to-image, image model selection, or CLI-based image workflows on ricebowl.ai.
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
    skillKey: ai-image-generation
    emoji: "🖼️"
    homepage: https://github.com/214140846/ai-media-generator
    install:
      - kind: node
        package: ai-media-generator
        bins: [ai-media]
---

# AI Image Generation

用这个 skill 处理这些请求：

- `ai image generation`
- `ai image generator`
- `image generator`
- `text to image`
- `image to image`
- `prompt to image`
- 选图片模型、讲图片参数、跑图片生成任务

如果用户的搜索意图已经更具体，优先切到更窄的 skill：

- `text-to-image`
- `image-to-image`
- `flux-image-generator`
- `nano-banana-image-generator`

## Default Route

```text
ricebowl.ai
  -> recharge credits
  -> create API key
  -> set key
  -> models show --model <MODEL>
  -> image generate
  -> image get
```

## Recommended Template

```bash
ai-media config set-key <KEY>
ai-media models list --json
ai-media models show --model <MODEL>
ai-media image generate \
  --model <MODEL> \
  --prompt "<subject>, <style>, <lighting>" \
  --aspect-ratio 1:1 \
  --image https://example.com/reference.png \
  --param vendor_options='{"style":"cinematic"}' \
  --wait
```

如果要做横幅图，就把 `--aspect-ratio` 改成 `16:9`。
如果模型还有额外字段，就先跑 `models show --model <MODEL>`，再用 `--param KEY=VALUE` 传递。

## Core Commands

```bash
ai-media config set-key <KEY>
ai-media config show
ai-media models list --json
ai-media models show --model <MODEL>
ai-media image generate --model <MODEL> --prompt <PROMPT>
ai-media image get --task-id <TASK_ID>
```

## When To Load References

- 参数全表、默认值、输出行为：读 `../ai-media-cli/references/cli-commands.md`
- 充值、生成 key、平台 onboarding：读 `../ai-media-cli/references/platform-onboarding.md`

## Response Pattern

如果用户是第一次接触，优先给：

1. 最短安装命令
2. 平台充值和 key 路径
3. 一组可直接复制的配置命令
4. 一条可直接运行的图片生成命令

如果用户在比模型或调脚本，补充：

- `models list --json`
- `models show --model`
- `AI_MEDIA_API_KEY`
- `image get --task-id`
