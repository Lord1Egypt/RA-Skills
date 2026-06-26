# 🎵 ACE-Step 音乐发送方案总结

## ✅ 已完成的功能

### 1. 基础音乐生成
```bash
# 使用虚拟环境生成
source ~/ace-step-env/bin/activate
cd ~/workspace/ace-step
python cli.py --prompt "Peaceful piano" --duration 30
```

### 2. 生成后发送脚本

| 脚本 | 功能 | 用法 |
|------|------|------|
| `demo-send-feishu.sh` | 生成 + 本地通知 | `bash demo-send-feishu.sh "描述" 30` |
| `generate-and-send.sh` | 多平台发送 | `bash generate-and-send.sh "描述" -c telegram` |
| `feishu_music_sender.py` | Python 版本 | `python feishu_music_sender.py "描述"` |

---

## 📤 发送到飞书/其他平台的方案

### 方案 A: 本地文件 + 手动发送 (立即可用)

**流程**:
1. 生成音乐到 `~/Music/ACE-Step/`
2. 使用 AirDrop/Finder 分享
3. 或手动上传到飞书

```bash
# 生成
bash skills/ace-step/demo-send-feishu.sh "Peaceful piano" 30

# 手动发送到飞书
open ~/Music/ACE-Step/
# 拖拽文件到飞书聊天窗口
```

### 方案 B: Telegram Bot (需配置)

```bash
# 1. 配置环境变量
export TELEGRAM_BOT_TOKEN="your_bot_token"
export TELEGRAM_CHAT_ID="your_chat_id"

# 2. 生成并发送
bash skills/ace-step/generate-and-send.sh "Piano" -c telegram
```

### 方案 C: Discord Webhook (需配置)

```bash
# 1. 配置环境变量
export DISCORD_WEBHOOK_URL="https://discord.com/api/webhooks/..."

# 2. 生成并发送  
bash skills/ace-step/generate-and-send.sh "Piano" -c discord
```

### 方案 D: OpenClaw 集成 (推荐用于自动化)

**思路**: 使用 OpenClaw 的 `message` 工具发送

```python
# 生成后调用 OpenClaw 发送
import subprocess

# 发送文字通知
subprocess.run([
    "openclaw", "message", "send",
    "--channel", "feishu",
    "--target", "user:ou_232e435f3b7b35533206709e39cb19b5",
    "--text", f"🎵 音乐生成完成: {file_path}"
])
```

**注意**: 大文件需要通过云存储中转:
1. 上传到飞书云盘/阿里云 OSS
2. 获取分享链接
3. 发送链接而非文件

---

## 🚀 推荐的工作流程

### 日常快速使用
```bash
# 1. 生成音乐
bash skills/ace-step/demo-send-feishu.sh "你想要的音乐描述"

# 2. 自动播放 (回答 y)
# 3. 查看生成的文件路径
# 4. 使用 AirDrop 或其他方式分享
```

### 自动化流程 (Agent 调用)
```python
# 其他 Agent 可以这样调用
import subprocess

result = subprocess.run([
    "bash", "skills/ace-step/demo-send-feishu.sh",
    "Peaceful piano for meditation", "60"
], capture_output=True, text=True)

# 解析输出获取文件路径
# 然后发送到指定渠道
```

---

## 📁 已创建的文件

```
skills/ace-step/
├── demo-send-feishu.sh      # ✅ 演示脚本 (已测试)
├── generate-and-send.sh     # 多平台发送
├── feishu_music_sender.py   # Python 版本
├── generate_and_send.py     # 通用 Python 版本
├── SEND_GUIDE.md            # 完整发送指南
└── AGENT_USAGE.md           # Agent 使用文档
```

---

## 🎯 下一步建议

### 短期 (立即可做)
1. **测试 demo-send-feishu.sh** - 已可用
2. **配置 Telegram Bot** - 如果需要 Telegram 发送
3. **配置 Discord Webhook** - 如果需要 Discord 发送

### 中期 (自动化)
1. **接入飞书云盘 API** - 自动上传并分享链接
2. **创建快捷指令** - macOS Shortcuts 一键生成+发送
3. **定时任务** - 定时生成音乐并发送

### 长期 (高级功能)
1. **Web 界面** - Gradio UI 供多用户使用
2. **多 Agent 协作** - 一个 Agent 生成，另一个发送
3. **音乐库管理** - 自动分类、标签、搜索

---

## 💡 常见问题

### Q: 为什么不用 OpenClaw 直接发送文件？
**A**: OpenClaw 的 `message` 工具对文件大小有限制，且不同平台 API 不同。大文件建议:
1. 上传到云存储
2. 发送链接
3. 或使用平台 Bot API 直接发送

### Q: 文件太大怎么办？
**A**: 使用 ffmpeg 压缩:
```bash
ffmpeg -i input.wav -codec:a libmp3lame -qscale:a 2 output.mp3
# 可将 20MB WAV 压缩到 2MB MP3
```

### Q: 如何完全自动化？
**A**: 使用 Telegram Bot 或 Discord Webhook，无需人工干预即可发送。

---

有任何问题随时询问！🎵
