# Edge TTS Skill for OpenClaw

🎤 免费语音合成技能 - 使用微软 Edge TTS

---

## 快速开始

### 1. 安装

```bash
# 克隆或复制此技能目录到 ~/.openclaw/workspace/skills/edge-tts
```

### 2. 配置

```bash
# 启用 Edge TTS
openclaw config set messages.tts.provider edge
openclaw config set messages.tts.providers.edge.enabled true
openclaw config set messages.tts.providers.edge.voice zh-CN-XiaoxiaoNeural

# 重启
openclaw gateway restart
```

### 3. 测试

直接和 AI 聊天，回复会自动转换为语音！

---

## 特性

- ✅ **完全免费** - 无需 API Key
- ✅ **多语言** - 支持 100+ 种语言
- ✅ **高质量** - 微软 Neural 语音
- ✅ **易配置** - 几条命令即可启用

---

## 推荐语音

### 中文
- `zh-CN-XiaoxiaoNeural` - 温柔女声 (推荐)
- `zh-CN-YunxiNeural` - 阳光男声
- `zh-CN-XiaoyiNeural` - 活泼女声

### 英文
- `en-US-JennyNeural` - 美国女声
- `en-US-GuyNeural` - 美国男声

---

## 配置示例

```json
{
  "messages": {
    "tts": {
      "auto": "always",
      "provider": "edge",
      "providers": {
        "edge": {
          "enabled": true,
          "voice": "zh-CN-XiaoxiaoNeural"
        }
      }
    }
  }
}
```

---

## 许可证

MIT
