---
name: feishu-voice-tts
description: 将文本转为语音并通过飞书 audio 消息发送给指定用户。用于“给用户发语音”“把这段话转语音并发飞书”“语音播报结果”等场景，尤其当普通文件发送会降级为文本时使用。仅在指定 channel=feishu 时触发。优先在需要高可达、可听播报时使用。
---

# Feishu Voice TTS

## Overview

把文本转换为语音（edge-tts），再转码为飞书可用的 Opus（OGG 容器），调用飞书开放平台“先上传文件再发 audio 消息”的标准流程发送，避免“直接发文件被降级成文本”。

## Quick Start

执行脚本：

```bash
skills/feishu-voice-tts/scripts/send_feishu_voice.sh "用户你好，这是一条语音消息" "user_open_id"
```

参数：

1. `text`（必填）要播报的文本
2. `open_id`（必填，可用环境变量替代）飞书用户 open_id
3. `voice`（可选）edge-tts 音色，默认 `zh-CN-YunxiNeural`

环境变量（可选，优先级高于配置文件）：

- `FEISHU_APP_ID`
- `FEISHU_APP_SECRET`
- `FEISHU_OPEN_ID`
- `EDGE_TTS_VOICE`

## Workflow

按以下顺序执行，不要跳步：

1. 文本转语音：`edge-tts` 生成 mp3
2. 转码：`ffmpeg` 转为 `audio/ogg`（opus 编码，16k 单声道）
3. 获取 tenant token：飞书 `/auth/v3/tenant_access_token/internal`
4. 上传语音文件：飞书 `/im/v1/files`，拿 `file_key`
5. 发送 audio 消息：飞书 `/im/v1/messages`，`msg_type=audio` + `file_key`

成功时脚本输出：

```json
{"success": true, "message_id": "...", "file_key": "..."}
```

## Requirements

- `ffmpeg` 可用
- `edge-tts` 可用（脚本自动尝试以下入口）：
  - `edge-tts`
  - `~/Library/Python/3.14/bin/edge-tts`
  - `python3 -m edge_tts`
- 本机存在 OpenClaw 配置：`~/.openclaw/openclaw.json`
  - 默认读取：`channels.feishu.accounts.feishu-main.appId/appSecret`

## Failure Handling

- 缺少依赖：按报错安装（例如 `python3 -m pip install --user edge-tts`）
- 飞书 API 失败：脚本会直接输出原始 JSON 错误，按 `code/msg` 排查
- 被降级成文本：确认发送的是 `msg_type=audio` 且 `content` 里是上传后的 `file_key`

## scripts/

- `scripts/send_feishu_voice.sh`：完整自动化脚本（TTS + 转码 + 上传 + 发送）
