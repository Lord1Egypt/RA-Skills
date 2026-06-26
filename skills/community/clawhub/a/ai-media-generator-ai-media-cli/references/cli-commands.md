# ai-media CLI Commands

## Install Matrix

```bash
# Rust
cargo install ai-media-generator

# npm / pnpm / bun
npm install -g ai-media-generator
pnpm add -g ai-media-generator
bun add -g ai-media-generator

# Python
pipx install ai-media-generator
uv tool install ai-media-generator
```

实际可执行命令：

```bash
ai-media
```

## Config

### `ai-media config set-key <KEY>`

- 用途：保存受管 API key
- 例子：`ai-media config set-key gm_xxx`

### `ai-media config show`

- 用途：打印当前配置
- 输出：pretty JSON

## Default Platform

当前默认平台固定为 `ricebowl.ai`，用户不需要手动设置 `base_url`。

历史兼容说明：

- 旧版文档可能会出现 `ai-media config set-base-url ...`
- 旧版环境变量可能会出现 `AI_MEDIA_BASE_URL`
- 这两种写法现在都不作为默认用户路径推荐

## Models

### `ai-media models list`

- 用途：查看当前 API 暴露的模型
- 输出：按 `Videos` 和 `Images` 分组的人类可读文本

### `ai-media models list --json`

- 用途：给 agent、脚本、流水线消费
- 输出：JSON，包含每个模型的 `parameters` manifest

### `ai-media models show --model <MODEL>`

- 用途：查看单个模型的参数要求
- 例子：`ai-media models show --model veo3-1`
- JSON：`ai-media models show --model nano-banana --json`

### `ai-media models show`

- 用途：查看单个模型的参数元数据
- 输出：人类可读文本，或 `--json`

```bash
ai-media models show --model veo3.1
ai-media models show --model veo3.1 --json
```

优先用它来判断某个模型应该传哪些 `--param KEY=VALUE`。

## Image

### `ai-media image generate`

用法：

```bash
ai-media image generate [OPTIONS] --model <MODEL> --prompt <PROMPT>
```

参数：

- `--model <MODEL>` 必填
- `--prompt <PROMPT>` 必填
- `--aspect-ratio <ASPECT_RATIO>` 选填
- `--response-format <RESPONSE_FORMAT>` 选填
- `--image <IMAGE_URL>` 选填，可重复
- `--metadata-json <JSON>` 选填
- `--param <KEY=VALUE>` 选填，可重复
- `--wait` 选填
- `--poll-interval <POLL_INTERVAL>` 选填，默认 `5`

常用例子：

```bash
ai-media image generate \
  --model nano-banana \
  --prompt "a cinematic ramen bowl on a wooden table" \
  --aspect-ratio 1:1
```

```bash
ai-media image generate \
  --model nano-banana \
  --prompt "studio portrait lighting, close-up ramen bowl" \
  --aspect-ratio 1:1 \
  --image https://example.com/reference.png \
  --param vendor_options='{"style":"cinematic"}' \
  --wait \
  --poll-interval 3
```

行为：

- 不带 `--wait`：打印初始创建任务响应
- 带 `--wait`：轮询直到任务变成 `completed` 或 `failed`
- `--param` 值会合并进请求 body，像 `true`、`8`、`["url"]` 这样的值会优先按 JSON 解析

### `ai-media image get`

用法：

```bash
ai-media image get [OPTIONS] --task-id <TASK_ID>
```

参数：

- `--task-id <TASK_ID>` 必填
- `--wait` 选填
- `--poll-interval <POLL_INTERVAL>` 选填，默认 `5`

## Video

### `ai-media video generate`

用法：

```bash
ai-media video generate [OPTIONS] --model <MODEL> --prompt <PROMPT>
```

参数：

- `--model <MODEL>` 必填
- `--prompt <PROMPT>` 必填
- `--aspect-ratio <ASPECT_RATIO>` 选填
- `--duration <DURATION>` 选填
- `--image <IMAGE_URL>` 选填，可重复
- `--param <KEY=VALUE>` 选填，可重复
- `--wait` 选填
- `--poll-interval <POLL_INTERVAL>` 选填，默认 `8`

常用例子：

```bash
ai-media video generate \
  --model seedance-pro-fast \
  --prompt "steam rising from a rice bowl, cinematic close-up" \
  --aspect-ratio 16:9 \
  --duration 5 \
  --param resolution=720p \
  --param seed=42
```

```bash
ai-media video generate \
  --model veo3-1 \
  --prompt "slow dolly shot over a steaming rice bowl" \
  --aspect-ratio 16:9 \
  --duration 4 \
  --image https://example.com/start-frame.png \
  --param audio=true \
  --wait
```

行为：

- 不带 `--wait`：打印初始创建任务响应
- 带 `--wait`：轮询直到任务变成 `SUCCESS` 或 `FAILURE`
- `--param` 值会合并进请求 body，像 `true`、`8`、`["url"]` 这样的值会优先按 JSON 解析

### `ai-media video get`

用法：

```bash
ai-media video get [OPTIONS] --task-id <TASK_ID>
```

参数：

- `--task-id <TASK_ID>` 必填
- `--wait` 选填
- `--poll-interval <POLL_INTERVAL>` 选填，默认 `5`

## Task

### `ai-media task get`

用法：

```bash
ai-media task get [OPTIONS] --kind <KIND> --task-id <TASK_ID>
```

参数：

- `--kind <KIND>` 必填，可选值：`image`、`video`
- `--task-id <TASK_ID>` 必填
- `--wait` 选填
- `--poll-interval <POLL_INTERVAL>` 选填，默认 `5`

## Config Precedence

```text
AI_MEDIA_API_KEY
  -> local config file
  -> built-in ricebowl.ai default
```

本地配置文件路径：

```text
<system config dir>/ai-media/config.json
```

## Script-Friendly Usage

适合自动化的命令：

- `ai-media config show`
- `ai-media models list --json`
- `ai-media models show --model`
- `ai-media image generate`
- `ai-media image get`
- `ai-media video generate`
- `ai-media video get`
- `ai-media task get`

例子：

```bash
ai-media models list --json
ai-media image get --task-id img_task_xxx | jq .
```

## Model Family Templates

这些模板对应 upstream API 里最常见的模型专属字段。遇到更细的模型参数，先跑 `models show --model <MODEL>`，再决定哪些字段走内建 flag，哪些字段走 `--param`。
先跑 `ai-media models show --model <MODEL>`，再决定要塞哪些 `--param KEY=VALUE`。

### Veo

文本转视频常见参数：

- `--aspect-ratio 16:9`
- `--param enhance_prompt=true`
- `--param enable_upsample=true`

```bash
ai-media video generate \
  --model veo3.1 \
  --prompt "cinematic bowl of ramen under soft light" \
  --aspect-ratio 16:9 \
  --param enhance_prompt=true \
  --param enable_upsample=true
```

图生视频常见参数：

- `--aspect-ratio 16:9`
- `--param images='["https://example.com/reference.png"]'`

```bash
ai-media video generate \
  --model veo3.1 \
  --prompt "steam drifting upward, gentle camera push-in" \
  --param images='["https://example.com/reference.png"]' \
  --aspect-ratio 16:9
```

### Seedance / 参考图视频

- `--aspect-ratio 16:9`
- `--param images='["https://example.com/reference.png"]'`

```bash
ai-media video generate \
  --model doubao-seedance-1-5-pro-251215 \
  --prompt "slow push-in over the food" \
  --param images='["https://example.com/reference.png"]' \
  --duration 4
```

### Flux / Recraft / 其他图片模型

- `size=1024x1024`

```bash
ai-media image generate \
  --model bfl/flux-2-max \
  --prompt "minimal product photo of a ceramic bowl" \
  --param size=1024x1024
```

## Historical Notes

如果你在旧脚本里看到 `set-base-url` 或 `AI_MEDIA_BASE_URL`，那是历史兼容写法。当前默认路径里，只有 `AI_MEDIA_API_KEY` 还保留为推荐的可覆盖配置。
