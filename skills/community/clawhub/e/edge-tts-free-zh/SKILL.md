# Edge TTS Skill - 免费语音合成

🎤 使用微软 Edge TTS 实现免费的文本转语音功能，无需 API Key！

---

## 📦 安装

```bash
# 本地安装
cd ~/.openclaw/workspace/skills
git clone <repo-url> edge-tts

# 或通过 clawhub (如果已发布)
openclaw skills install edge-tts
```

---

## ⚙️ 配置

### 方式一：通过 CLI 配置

```bash
# 启用 Edge TTS
openclaw config set messages.tts.provider edge
openclaw config set messages.tts.auto always
openclaw config set messages.tts.providers.edge.enabled true
openclaw config set messages.tts.providers.edge.voice zh-CN-XiaoxiaoNeural

# 重启 Gateway
openclaw gateway restart
```

### 方式二：手动编辑配置

编辑 `~/.openclaw/openclaw.json`，添加/修改以下配置：

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

然后重启 Gateway：
```bash
openclaw gateway restart
```

---

## 🎤 可选语音

### 中文语音

| 语音 ID | 描述 | 性别 |
|---------|------|------|
| `zh-CN-XiaoxiaoNeural` | 温柔女声 | 女 |
| `zh-CN-YunxiNeural` | 阳光男声 | 男 |
| `zh-CN-YunjianNeural` | 成熟男声 | 男 |
| `zh-CN-XiaoyiNeural` | 活泼女声 | 女 |
| `zh-CN-XiaochenNeural` | 知性女声 | 女 |
| `zh-CN-liaoning-XiaobeiNeural` | 东北话 | 女 |
| `zh-CN-shaanxi-XiaoniNeural` | 陕西话 | 女 |

### 英文语音

| 语音 ID | 描述 |
|---------|------|
| `en-US-JennyNeural` | 美国女声 |
| `en-US-GuyNeural` | 美国男声 |
| `en-GB-SoniaNeural` | 英国女声 |
| `en-GB-RyanNeural` | 英国男声 |

### 其他语言

完整语音列表参考：https://speech.microsoft.com/portal/voicegallery

---

## 🧪 测试

```bash
# 使用 tts 工具测试
openclaw tts "你好，我是 Edge TTS"

# 或在聊天中直接说话，会自动触发 TTS (如果 auto: always)
```

---

## 📊 配置说明

| 配置项 | 说明 | 默认值 |
|--------|------|--------|
| `messages.tts.auto` | TTS 触发模式 | `always` / `never` / `mention` |
| `messages.tts.provider` | 默认 TTS 供应商 | `edge` |
| `messages.tts.providers.edge.enabled` | 是否启用 Edge TTS | `true` |
| `messages.tts.providers.edge.voice` | 语音 ID | `zh-CN-XiaoxiaoNeural` |

---

## 💡 使用场景

- ✅ **个人助手** - 让 AI 助手用语音回复
- ✅ **无障碍辅助** - 为视障用户提供语音输出
- ✅ **多语言支持** - 支持 100+ 种语言
- ✅ **成本敏感** - 完全免费，无 API 调用限制

---

## ⚠️ 注意事项

1. **网络连接** - Edge TTS 需要访问微软服务
2. **速率限制** - 微软可能有隐式速率限制，大量使用需注意
3. **音频格式** - 输出为音频文件，通过消息平台发送
4. **自动播放** - 部分平台/客户端可能需要用户手动播放音频

---

## 🔧 故障排查

### TTS 不工作

```bash
# 1. 检查配置
openclaw config get messages.tts

# 2. 检查 Gateway 状态
openclaw gateway status

# 3. 查看日志
openclaw gateway logs --follow

# 4. 运行诊断
openclaw doctor --fix
```

### 常见错误

| 错误 | 原因 | 解决方案 |
|------|------|----------|
| `microsoft: no provider registered` | Edge TTS 未正确配置 | 确保 `messages.tts.providers.edge.enabled` 为 `true` |
| 音频无法播放 | 平台不支持 | 检查消息平台是否支持音频附件 |
| 语音不对 | 语音 ID 错误 | 确认语音 ID 拼写正确 |

---

## 📚 相关资源

- [OpenClaw TTS 文档](https://docs.openclaw.ai/tts)
- [微软 Edge TTS 语音列表](https://speech.microsoft.com/portal/voicegallery)
- [Edge TTS Python 库](https://github.com/rany2/edge-tts)

---

## 📝 更新日志

- **2026-04-07** - 初始版本，支持 Edge TTS 配置和中文语音

---

## 📄 许可证

MIT License - 详见 [LICENSE](LICENSE) 文件

_作者：Roxy (洛琪希) 🐾_
