# 🎵 ACE-Step 音乐发送指南

## 概述

生成音乐后，可以通过多种方式发送给你：

| 方式 | 优点 | 缺点 | 适用场景 |
|------|------|------|----------|
| **本地播放** | 即时、无损 | 仅限本机 | 快速预览 |
| **AirDrop** | 快速、原文件 | 需在同一网络 | 发送到 iPhone/iPad |
| **飞书云盘** | 永久保存、分享方便 | 需上传时间 | 长期存储 |
| **Telegram Bot** | 自动发送、跨平台 | 需配置 Bot | 自动化流程 |
| **Discord Webhook** | 频道分享、社区 | 需 Webhook | 团队协作 |

---

## 方法 1: 本地播放 (最简单)

```bash
# 生成后自动播放
afplay ~/Music/ACE-Step/music_xxx.wav

# 或使用 QuickTime
open ~/Music/ACE-Step/music_xxx.wav
```

---

## 方法 2: AirDrop (Mac -> iPhone)

```bash
# 生成后使用 AirDrop
./skills/ace-step/generate-and-send.sh "Peaceful piano" --no-send
open ~/Music/ACE-Step/
# 然后手动 AirDrop
```

---

## 方法 3: 飞书发送 (推荐 ⭐)

### 步骤 1: 上传到飞书云盘

使用 OpenClaw 的 feishu_drive 工具：

```bash
# 1. 创建文件夹
openclaw feishu drive create_folder --name "ACE-Step音乐"

# 2. 上传文件 (需实现文件上传功能)
# 注意: 当前 feishu_drive 工具可能不支持直接上传文件
# 需要先将文件放到飞书可访问的位置
```

### 步骤 2: 发送消息通知

```python
# 使用 message 工具发送通知
message.send(
    channel="feishu",
    target="user:ou_232e435f3b7b35533206709e39cb19b5",
    text="🎵 音乐生成完成! 文件: music_xxx.wav"
)
```

### 完整流程脚本

```bash
#!/bin/bash
# generate-and-notify.sh

PROMPT="$1"
DURATION="${2:-30}"

# 生成音乐
source ~/ace-step-env/bin/activate
cd ~/workspace/ace-step
python cli.py --prompt "$PROMPT" --duration "$DURATION" \
    --output ~/Music/ACE-Step/latest.wav

# 发送飞书通知
# 需要配置 OpenClaw message 工具
openclaw message send \
    --channel feishu \
    --target "user:ou_232e435f3b7b35533206709e39cb19b5" \
    --text "🎵 音乐生成完成: $PROMPT ($DURATION秒)"
```

---

## 方法 4: Telegram Bot

### 配置步骤

1. **创建 Bot**:
   - 找 @BotFather 创建新 bot
   - 获取 Token: `123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11`

2. **获取 Chat ID**:
   - 给 bot 发送任意消息
   - 访问: `https://api.telegram.org/bot<Token>/getUpdates`
   - 找到 `chat.id`

3. **设置环境变量**:
   ```bash
   export TELEGRAM_BOT_TOKEN="your_token_here"
   export TELEGRAM_CHAT_ID="your_chat_id"
   ```

4. **发送文件**:
   ```bash
   curl -X POST "https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/sendAudio" \
       -F "chat_id=${TELEGRAM_CHAT_ID}" \
       -F "audio=@/path/to/music.wav" \
       -F "caption=🎵 ACE-Step Generated"
   ```

---

## 方法 5: Discord Webhook

### 配置步骤

1. **创建 Webhook**:
   - Discord 服务器设置 -> 集成 -> Webhook
   - 复制 Webhook URL

2. **设置环境变量**:
   ```bash
   export DISCORD_WEBHOOK_URL="https://discord.com/api/webhooks/..."
   ```

3. **发送文件**:
   ```bash
   curl -X POST "$DISCORD_WEBHOOK_URL" \
       -H "Content-Type: multipart/form-data" \
       -F "file=@/path/to/music.wav" \
       -F "content=🎵 New music from ACE-Step"
   ```

---

## 推荐方案: 智能发送脚本

创建一个智能脚本，根据文件大小自动选择最佳发送方式：

```bash
#!/bin/bash
# smart-send.sh

FILE="$1"
FILE_SIZE=$(stat -f%z "$FILE")
FILE_MB=$((FILE_SIZE / 1024 / 1024))

echo "文件大小: ${FILE_MB}MB"

if [ $FILE_MB -lt 20 ]; then
    # 小于 20MB: 直接通过 Telegram/Discord 发送
    echo "使用 Telegram Bot 发送..."
    # telegram send code here
elif [ $FILE_MB -lt 100 ]; then
    # 小于 100MB: 上传到飞书云盘
    echo "上传到飞书云盘..."
    # feishu upload code here
else
    # 大于 100MB: 本地保存，发送通知
    echo "文件较大，请在本地查看:"
    echo "  open $FILE"
fi
```

---

## 完整自动化示例

```bash
#!/bin/bash
# 完整自动化流程

# 1. 生成音乐
PROMPT="A peaceful piano melody with soft rain sounds"
OUTPUT="~/Music/ACE-Step/$(date +%Y%m%d_%H%M%S).wav"

source ~/ace-step-env/bin/activate
cd ~/workspace/ace-step
python cli.py \
    --prompt "$PROMPT" \
    --duration 60 \
    --output "$OUTPUT"

# 2. 发送到多个渠道
./skills/ace-step/send-to-all.sh "$OUTPUT" \
    --feishu \
    --telegram \
    --message "🎵 新音乐: $PROMPT"

# 3. 备份到 iCloud
# (自动同步)

echo "✅ 完成!"
```

---

## 快速命令参考

```bash
# 生成并播放
afplay $(python skills/ace-step/feishu_music_sender.py "Piano" -d 30 | grep "SAVED" | awk '{print $2}')

# 生成后 AirDrop
open ~/Music/ACE-Step/

# 发送到 Telegram (需配置)
./skills/ace-step/generate-and-send.sh "Electronic" -c telegram

# 发送到 Discord (需配置)
./skills/ace-step/generate-and-send.sh "Jazz" -c discord
```

---

## 注意事项

1. **文件大小限制**:
   - Telegram Bot: 20MB
   - Discord: 8MB (普通), 50MB (Nitro)
   - 飞书: 取决于云盘空间

2. **格式转换**:
   ```bash
   # WAV 转 MP3 (减小文件大小)
   ffmpeg -i input.wav -codec:a libmp3lame -qscale:a 2 output.mp3
   ```

3. **网络要求**:
   - 首次使用需下载模型 (~4GB)
   - 发送文件需要稳定网络

---

## 待实现功能

- [ ] 飞书云盘自动上传
- [ ] 微信文件传输
- [ ] 邮件发送
- [ ] 自动格式转换 (WAV -> MP3)
- [ ] 批量生成和发送

---

有任何问题请随时询问！
