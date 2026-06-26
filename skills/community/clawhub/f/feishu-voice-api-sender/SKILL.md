---
name: feishu-voice-send
description: "飞书语音消息发送：使用官方 API 上传 OPUS 音频并发送语音消息，解决 OpenClaw 内置发送缺少 duration 参数的问题。| Send voice messages via Feishu official API, fixing OpenClaw's missing duration parameter bug."
requires:
  binaries:
    - python3      # Python 3 runtime
    - requests     # HTTP library (pip install requests)
    - ffprobe      # Audio duration detection (ffmpeg package)
    - uvx          # edge-tts runner
  runtime:
    - edge-tts    # Microsoft Edge TTS (via uvx)
---

# Feishu Voice Send Skill

## 功能

通过飞书官方 API 发送语音消息，解决 OpenClaw 内置发送缺少 `duration` 参数的问题。

## 核心问题

OpenClaw 内置的飞书媒体发送存在 bug：
- `uploadFileFeishu` 缺少 `duration` 参数
- `sendFileFeishu` 发送 audio 消息时 content 缺少 `duration`

飞书官方 API 要求：
- 上传 opus 文件时必须提供 `duration`（毫秒）
- 发送 audio 消息时 content 必须包含 `file_key` 和 `duration`

本 skill 直接调用飞书官方 API，绕过 OpenClaw 内置函数的 bug。

## 使用方式

### 方式一：发送现有音频文件

```bash
python3 /mnt/d/wslspace/workspace/skills/feishu-voice-send/scripts/send_voice.py <音频文件路径> <接收者open_id>
```

### 方式二：直接生成 TTS 并发送

```bash
python3 /mnt/d/wslspace/workspace/skills/feishu-voice-send/scripts/tts_and_send.py "要转换的文字" <接收者open_id>
```

## 核心脚本

### send_voice.py

直接发送现有的 .ogg 音频文件：

```bash
python3 scripts/send_voice.py <ogg文件路径> <open_id>
```

### tts_and_send.py

1. 用 edge-tts 生成 TTS（mp3）
2. 用 ffmpeg 转换为标准 Ogg Opus
3. 自动获取 duration
4. 调用官方 API 发送语音消息

```bash
python3 scripts/tts_and_send.py "文字内容" <open_id> [-v voice] [-r rate]
```

参数：
- `文字内容`（必须）：要转换的文字
- `open_id`（必须）：接收者飞书 open_id
- `-v voice`：TTS 音色，默认 zh-CN-YunjianNeural
- `-r rate`：语速，默认 -10%（即90%速度）

## 示例

### 发送音频文件

```bash
python3 scripts/send_voice.py /path/to/audio.ogg <接收者open_id>
```

### 发送 TTS 语音

```bash
python3 scripts/tts_and_send.py "你好，这是语音测试。" <接收者open_id>
```

### 使用不同音色和语速

```bash
python3 scripts/tts_and_send.py "Hello world" <接收者open_id> -v en-US-EmmaNeural -r 0
```

## 技术说明

### 关键问题

OpenClaw 内置的飞书媒体发送存在 bug：
- `uploadFileFeishu` 缺少 `duration` 参数
- `sendFileFeishu` 发送 audio 消息时 content 缺少 `duration`

飞书官方 API 要求：
- 上传 opus 文件时必须提供 `duration`（毫秒）
- 发送 audio 消息时 content 必须包含 `file_key` 和 `duration`

### 解决方案

直接调用飞书官方 API，不走 OpenClaw 内置函数：

1. 获取 tenant_access_token
2. 上传 opus 文件（带 duration）
3. 发送 audio 类型消息（content 包含 file_key 和 duration）

## 依赖

- Python 3
- requests
- ffprobe（ffmpeg 的一部分）
- edge-tts（通过 uvx 运行）

## 凭证配置

脚本从以下途径获取飞书凭证（优先级从高到低）：

### 方式一：环境变量（推荐）

设置环境变量，最灵活：

```bash
# 在终端中设置
export APP_ID="cli_xxxxxxxxxxxxxx"
export APP_SECRET="xxxxxxxxxxxxxxxxxxxxxxxx"

# 或直接运行
APP_ID="cli_xxxxxxxxxxxxxx" APP_SECRET="xxxxxxxx" python3 scripts/send_voice.py ...
```

### 方式二：OpenClaw 配置（自动）

如果脚本在 OpenClaw 环境下运行，会自动从 `~/.openclaw/openclaw.json` 读取 main 账号的凭证。

### 方式三：手动修改脚本

如果以上方式都不适用，可以直接在脚本开头修改：

```python
APP_ID = "cli_xxxxxxxxxxxxxx"
APP_SECRET = "xxxxxxxxxxxxxxxxxxxxxxxx"
```

**注意**：方式三会随 skill 更新丢失，不推荐。

### 获取飞书应用凭证

1. 前往 [飞书开放平台](https://open.feishu.cn/app) 创建应用
2. 获取应用的 `App ID` 和 `App Secret`
3. 配置应用权限（需要 `im:message` 相关权限）
4. 将机器人添加到飞书群或与用户单聊
