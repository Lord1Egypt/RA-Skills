---
name: feishu-tts-pro
description: 将文字转换为语音并以飞书语音气泡消息发送。使用 Edge-TTS（微软，免费，无限次）生成中文语音，FFmpeg 转码为 ogg/opus，上传到飞书作为 audio 类型消息。支持自定义音色、接收者和 Python 环境。当用户要求用语音回复、发语音消息、TTS 朗读内容时触发。
metadata:
  openclaw:
    emoji: "🎤"
    requires:
      bins: ["ffmpeg"]
      env:
        - FEISHU_APP_ID
        - FEISHU_APP_SECRET
        - FEISHU_DEFAULT_USER
        - EDGE_TTS_VOICE
        - PYTHON_BIN
---

# feishu-tts-pro

将中文文字转换为语音，直接发送为飞书语音气泡消息。

## 使用方法

```bash
# 发送语音消息（默认发送给 FEISHU_DEFAULT_USER）
tts-send "你好，这是番茄的语音回复"

# 发送给指定用户
tts-send "你好" ou_xxxxx
```

## 环境变量（必填）

| 变量 | 说明 |
|------|------|
| `FEISHU_APP_ID` | 飞书应用 App ID |
| `FEISHU_APP_SECRET` | 飞书应用 App Secret |
| `FEISHU_DEFAULT_USER` | 默认接收者的 open_id（可选，未提供时需要命令行参数） |

## 环境变量（可选）

| 变量 | 默认值 | 说明 |
|------|--------|------|
| `EDGE_TTS_VOICE` | `zh-CN-YunxiNeural` | Edge-TTS 音色 |
| `PYTHON_BIN` | 系统 Python | Python 路径（用于 edge-tts） |

## 可选音色

| 音色 | 说明 |
|------|------|
| `zh-CN-YunxiNeural` | 云希（男声，活泼阳光，默认） |
| `zh-CN-XiaoxiaoNeural` | 晓晓（女声，温和） |
| `zh-CN-YunyangNeural` | 云扬（男声，专业） |
| `zh-CN-XiaoyiNeural` | 晓逸（女声，甜美） |
| `zh-CN-tianxiangNeural` | 天祥（男声，大气） |

## 技术流程

1. Edge-TTS 生成 MP3（使用指定音色）
2. FFmpeg 转码为 ogg/opus（16kHz, mono, 飞书兼容）
3. 上传到飞书（file_type=opus，duration 嵌入）
4. 发送 audio 消息气泡

## 依赖

- **Node.js** 18+
- **Python** 3.8+ + edge-tts（`pip install edge-tts`）
- **FFmpeg**（系统安装）

## 安装 edge-tts

```bash
pip install edge-tts
```

或使用 uv：

```bash
uv pip install edge-tts --python /path/to/your/python
```

## 配置示例

在 `AGENTS.md` 或 `openclaw.json` 中配置：

```json
{
  "skills": {
    "entries": {
      "feishu-tts-pro": {
        "env": {
          "FEISHU_APP_ID": "cli_xxxxxxxxxxxx",
          "FEISHU_APP_SECRET": "xxxxxxxxxxxxxxxx",
          "FEISHU_DEFAULT_USER": "ou_xxxxxxxxxxxx",
          "EDGE_TTS_VOICE": "zh-CN-YunxiNeural"
        }
      }
    }
  }
}
```

## 故障排除

**TTS 生成失败**
- 确认 edge-tts 已安装：`python -c "import edge_tts"`
- 确认 Python 路径正确

**语音气泡无时长显示**
- 上传时需要传入 duration 参数（毫秒）
- 脚本已自动处理

**发送失败 (code=99991663)**
- 检查 App ID/Secret 是否正确
- 确认飞书应用已开通「发消息」权限

---

*Powered by 番茄 (OpenClaw Agent)*