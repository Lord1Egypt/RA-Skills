---
name: byted-mediakit-tools
display_name: 火山引擎音视频处理工具集
description: 火山引擎 AI MediaKit 音视频处理工具集，提供视频理解、音频提取、视频剪辑、音视频拼接、画质增强、文生视频、音视频合成等能力。当用户提及音频剪辑、视频剪辑、音视频拼接、文生视频、音频提取、画质增强、视频理解、音视频合成、媒体裁剪等需求时必须调用本Skill。当用户需要视频理解时，宿主agent必须自动解析用户的具体要求作为prompt参数传入，同时传入视频URL和fps参数；max_frames 为可选参数。
permissions:
  - network
  - file_read
  - file_write
  - temp_storage
env:
  - name: AMK_API_KEY
    description: AMK（AI MediaKit）访问密钥，调用剪辑/拼接/转码等媒体能力所需
    required: true
    secret: true
    default: ''
  - name: AMK_ENV
    description: AMK 服务端环境，取值 prod（生产）或 boe（BOE）
    required: true
    secret: false
    default: 'prod'
  - name: AMK_ENABLE_CLIENT_TOKEN
    description: 为 true 时，除视频理解外的请求会自动携带 8 位 client_token（幂等）；取值 true / false
    required: false
    secret: false
    default: 'false'
  - name: ARK_API_KEY
    description: 火山引擎方舟 OpenAPI 密钥，仅在使用视频理解（understand_video_content）时需要
    required: false
    secret: true
    default: ''
  - name: ARK_MODEL_ID
    description: 方舟模型 ID，仅在使用视频理解（understand_video_content）时需要
    required: false
    secret: false
    default: ''
---

> **说明**：宿主若在环境中注入 `ARK_SKILL_API_BASE` / `ARK_SKILL_API_KEY`（例如供其他 Skill 走 SkillHub 网关），与本 Skill 的 `AMK_API_KEY`、`ARK_API_KEY`（视频理解）**相互独立**，请勿混淆。

> ⚠️ **严格执行**：必须先完成 **环境检查**；环境缺失须提示用户，不可跳过。

> `<SKILL_DIR>` 为 `byted-mediakit-tools` 所在目录。
> 当前方法返回的 `链接仅供下载，不支持播放能力`
> `禁止修改任何返回数据信息`，如 `play_url` 、`request_id` 、`task_id` 等
> 用户明确声明需要重新执行时：除 `understand_video_content` 外的方法需 **生成新的 `client_token`（不要复用上一次的 `client_token`）**，避免命中上次的幂等结果

# 火山引擎 AI MediaKit 音视频处理工具集

## 概览

本工具集基于火山引擎 AI MediaKit 提供一站式音视频处理能力，包括：

- 🎬 **视频理解**：AI 分析视频内容，生成自然语言描述
- ✂️ **音视频剪辑**：精确裁剪音视频时长
- 🔗 **音视频拼接**：拼接多个片段，支持转场效果
- 🎵 **音频提取**：从视频中提取音频轨道
- 🖼️ **画质增强**：提升视频画质、分辨率、帧率
- 🎬 **文生视频**：图片生成视频，支持动画效果
- 🎧 **音视频合成**：合成新的音轨与视频

---

## 获取密钥

在开始使用前，请先获取必要的 API 密钥：

- **AI MediaKit 控制台**：https://console.volcengine.com/imp/ai-mediakit/
- **方舟模型与密钥**：https://console.volcengine.com/ark/region:ark+cn-beijing/model/detail?Id=doubao-seed-1-8

---

## 快速开始

### 1. 环境配置

在 `<SKILL_DIR>/.env` 中配置环境变量（首次使用会自动创建模板）：

```bash
# AMK API Key (必填) - https://console.volcengine.com/imp/ai-mediakit/
AMK_API_KEY=your_amk_api_key_here
# AMK 环境取值 prod 或 boe
AMK_ENV=prod
# 是否启用 client_token 自动注入（用于幂等）
AMK_ENABLE_CLIENT_TOKEN=false
# 方舟 密钥（可选，仅使用视频理解功能时必须配置）
ARK_API_KEY=your_ark_api_key_here
# 方舟 模型ID（可选，仅使用视频理解功能时必须配置）
ARK_MODEL_ID=doubao-seed-1-8
```

### 2. 依赖安装

```bash
cd <SKILL_DIR>/scripts
python3 -m venv .venv
. .venv/bin/activate
python -m pip install -U pip
python -m pip install -r requirements.txt
```

---

## 核心功能

### 同步能力（立即返回结果）

| 能力                         | 说明                                             |
| ---------------------------- | ------------------------------------------------ |
| **understand_video_content** | 视频内容理解，使用 AI 分析视频并生成自然语言描述 |

### 异步能力（默认自动等待结果）

| 能力                      | 说明                                    |
| ------------------------- | --------------------------------------- |
| **trim_media_duration**   | 裁剪音视频时长，精确到毫秒              |
| **concat_media_segments** | 拼接多个音视频片段，支持转场效果        |
| **extract_audio**         | 从视频中提取音频轨道，支持 mp3/m4a 格式 |
| **enhance_video**         | 视频画质增强，支持超分、插帧等          |
| **image_to_video**        | 图片生成视频，支持动画和转场            |
| **mux_audio_video**       | 音视频合成，支持时长对齐                |

### 辅助能力

| 能力           | 说明                       |
| -------------- | -------------------------- |
| **query_task** | 查询异步任务执行状态和结果 |

---

## 使用示例

### 视频理解

```bash
./byted-mediakit-tools.sh understand_video_content \
  --video_url "https://example.com/video.mp4" \
  --prompt "总结视频内容" \
  --fps 1
```

### 视频裁剪

```bash
# 裁剪前 10 秒
./byted-mediakit-tools.sh trim_media_duration \
  --type video \
  --source "https://example.com/video.mp4" \
  --start_time 0 \
  --end_time 10
```

### 音视频拼接

```bash
./byted-mediakit-tools.sh concat_media_segments \
  --type video \
  --sources "https://example.com/1.mp4" "https://example.com/2.mp4"
```

### 音频提取

```bash
./byted-mediakit-tools.sh extract_audio \
  --video_url "https://example.com/video.mp4" \
  --format mp3
```

### 画质增强

```bash
./byted-mediakit-tools.sh enhance_video \
  --video_url "https://example.com/video.mp4" \
  --tool_version professional \
  --resolution 1080p
```

### 图片生成视频

```bash
./byted-mediakit-tools.sh image_to_video \
  --images "image_url=https://example.com/1.jpg,duration=3,animation_type=zoom_in" \
           "image_url=https://example.com/2.jpg,duration=3,animation_type=pan_left"
```

### 音视频合成

```bash
./byted-mediakit-tools.sh mux_audio_video \
  --video_url "https://example.com/video.mp4" \
  --audio_url "https://example.com/audio.mp3" \
  --is_audio_reserve false
```

### 异步任务（不等待结果）

```bash
# 使用 --no-wait 立即返回 task_id
./byted-mediakit-tools.sh --no-wait trim_media_duration \
  --type video \
  --source "https://example.com/video.mp4" \
  --start_time 0 \
  --end_time 10

# 查询任务结果
./byted-mediakit-tools.sh query_task --task_id "amk-xxx-xxx"
```

---

## 响应格式

### 同步响应（视频理解）

```json
{
  "status": "success",
  "result": {
    "choices": [
      {
        "role": "assistant",
        "content": "视频内容分析结果..."
      }
    ]
  }
}
```

### 异步响应（默认自动等待）

```json
{
  "task_id": "amk-tool-extract-audio-xxxxxxxxxxxxxx",
  "duration": 82.454056,
  "play_url": "https://example.vod.cn-north-1.volcvideo.com/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx.mp3?preview=1&auth_key=***",
  "request_id": "20260401xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
  "status": "completed",
  "task_type": "extract-audio"
}
```

### 异步响应（--no-wait）

```json
{
  "status": "pending",
  "task_id": "amk-xxx-xxx",
  "message": "任务已提交，已跳过等待，可调用 query_task 接口传入 task_id 查询结果",
  "query_example": "./byted-mediakit-tools.sh query_task --task_id amk-xxx-xxx"
}
```

### 错误响应

```json
{
  "status": "failed/canceled/timeout",
  "task_id": "amk-xxx-xxx",
  "message": "错误详情"
}
```

---

## 详细文档

各功能的详细参数说明请参考 `reference/` 目录下的对应文档：

| 能力                     | 文档链接                                                                       |
| ------------------------ | ------------------------------------------------------------------------------ |
| understand_video_content | [reference/understand_video_content.md](reference/understand_video_content.md) |
| query_task               | [reference/query_task.md](reference/query_task.md)                             |
| concat_media_segments    | [reference/concat_media_segments.md](reference/concat_media_segments.md)       |
| enhance_video            | [reference/enhance_video.md](reference/enhance_video.md)                       |
| extract_audio            | [reference/extract_audio.md](reference/extract_audio.md)                       |
| image_to_video           | [reference/image_to_video.md](reference/image_to_video.md)                     |
| mux_audio_video          | [reference/mux_audio_video.md](reference/mux_audio_video.md)                   |
| trim_media_duration      | [reference/trim_media_duration.md](reference/trim_media_duration.md)           |
| 统一响应格式             | [reference/common_response.md](reference/common_response.md)                   |

---

## 注意事项

1. **返回链接**：所有返回的 `play_url` 等链接仅供下载，不支持直接播放
2. **幂等性**：重新执行任务时，请确保生成新的 `client_token`（`AMK_ENABLE_CLIENT_TOKEN=true` 时自动处理）
3. **视频理解**：使用视频理解功能必须配置 `ARK_API_KEY` 和 `ARK_MODEL_ID`
4. **超时处理**：大文件处理可能耗时较长，建议使用 `--no-wait` 配合 `query_task` 轮询

---

© 北京火山引擎科技有限公司 2026 版权所有
