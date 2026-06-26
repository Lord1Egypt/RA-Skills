---
name: ai-video-generation
description: Use when someone asks for ai video generation, video generator, text-to-video, image-to-video, prompt-to-video, video model selection, or CLI-based video workflows on ricebowl.ai.
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
    skillKey: ai-video-generation
    emoji: "🎬"
    homepage: https://github.com/214140846/ai-media-generator
    install:
      - kind: node
        package: ai-media-generator
        bins: [ai-media]
---

# AI Video Generation

用这个 skill 处理这些请求：

- `ai video generation`
- `ai video generator`
- `video generator`
- `text to video`
- `image to video`
- `prompt to video`
- `sora2 video generator`
- `veo video generator`
- `seedance video generator`

如果用户的搜索意图已经更具体，优先切到更窄的 skill：

- `text-to-video`
- `image-to-video`
- `veo-video-generator`
- `seedance-video-generator`

## Default Route

```text
ricebowl.ai
  -> recharge credits
  -> create API key
  -> set key
  -> models show --model <MODEL>
  -> choose text-to-video or image-to-video
  -> video generate
  -> video get / task get
```

## Recommended Template

```bash
ai-media config set-key <KEY>
ai-media models list --json
ai-media models show --model <MODEL>
ai-media video generate \
  --model <MODEL> \
  --prompt "<scene>, <camera movement>, <mood>" \
  --aspect-ratio 16:9 \
  --duration 4 \
  --param enhance_prompt=true \
  --wait
```

如果模型偏短片，就把 `--duration` 调成 `2`。
如果是图生视频模型，就把参考图放进 `--image https://...`。

## Core Commands

```bash
ai-media config set-key <KEY>
ai-media config show
ai-media models list --json
ai-media models show --model <MODEL>
ai-media video generate --model <MODEL> --prompt <PROMPT>
ai-media video get --task-id <TASK_ID>
ai-media task get --kind <image|video> --task-id <TASK_ID>
```

## When To Load References

- 参数全表、默认值、输出行为：读 `../ai-media-cli/references/cli-commands.md`
- 充值、生成 key、平台 onboarding：读 `../ai-media-cli/references/platform-onboarding.md`

## Response Pattern

如果用户是第一次接触，优先给：

1. 最短安装命令
2. 平台充值和 key 路径
3. 一组可直接复制的配置命令
4. 一条可直接运行的视频生成命令

如果用户在选模型或做自动化，补充：

- `models list --json`
- `models show --model`
- `task get --kind video`
- `--wait`
- `--poll-interval`
