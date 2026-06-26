---
name: article-tts
description: "拍照或文字转音频：文章照片 OCR 提取文字，或直接接收文字，生成 Microsoft Edge TTS 语音，支持中英文、自动转写、语速调节、逐句拆分。| Capture article photos (OCR) or plain text, generate natural audio via Edge TTS. Bilingual support (EN/ZH), configurable speed, voice, and sentence splitting."
requires:
  binaries:
    - tesseract        # OCR engine
    - uvx              # uvx runner (from uv package)
    - edge-tts        # Microsoft Edge TTS (via uvx, no install needed)
  runtime:
    - python3 (with PIL/Pillow)
    - tessdata (language models)
install: |
  # Install Tesseract OCR + Chinese language pack
  apt-get update && apt-get install -y tesseract-ocr tesseract-ocr-chi-sim

  # English language pack is included by default
  # If needed: apt-get install tesseract-ocr-eng

  # uvx / uv will auto-download edge-tts on first run (no manual install)
credentials:
  # OpenClaw handles channel authentication via its own plugin system.
  # The agent will automatically detect which channel is active and use
  # the appropriate credentials already configured in OpenClaw.
  # No extra env vars needed — the skill just calls message(...).
  #
  # Supported channels (via OpenClaw message tool):
  #   feishu       — Feishu bot (app_id/app_secret from Feishu Open Platform)
  #   telegram     — Telegram bot (bot token from BotFather)
  #   discord      — Discord bot (bot token + guild)
  #   whatsapp     — WhatsApp Business API / linked device
  #   signal       — Signal (phone number + signal-cli)
  #   imessage     — iMessage (via macOS/icloud)
  #   openclaw-weixin — WeChat Work / 个人微信
  #
  # If the target channel is not configured, the skill saves files locally
  # and notifies the user of the output path.
---

# Article TTS Skill

## Default Configuration

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `lang` | `en` | 语言：`en` 或 `zh` |
| `skipConfirmation` | `false` | 是否跳过文字确认步骤 |
| `speed` | `90%` | TTS 语速（`--rate=-10%` = 90%） |
| `voice` | `en-US-EmmaNeural`（英文）/ `zh-CN-XiaoxiaoNeural`（中文） | TTS 声音 |
| `splitSentences` | `false` | 是否生成按句拆分的音频 |

## Supported Languages

| 语言 | OCR 语言包 | TTS Voice |
|------|-----------|-----------|
| `en` | `eng`（预装） | `en-US-EmmaNeural` |
| `zh` | `chi_sim`（需安装） | `zh-CN-XiaoxiaoNeural` |

> **中文 OCR 语言包安装：**
> - Linux（WSL/Debian/Ubuntu）：`apt-get install tesseract-ocr-chi-sim`
> - macOS：`brew install tesseract-lang`（自带中文）
> - Windows：下载 `chi_sim.traineddata` 放入 Tesseract 安装目录的 `tessdata` 文件夹

## Workflow

### Input Types

- **图片**：OCR 提取文字（需要 `lang` 指定语言）
- **纯文字**：直接 TTS，无需 OCR

### Standard Flow（默认，需确认）

```
图片 → OCR 提取文字 → 展示给用户确认 → 用户确认 → 生成 TTS → 发送
文字 → 直接生成 TTS → 发送
```

### Skip-Confirmation Flow ⚠️

用户说"不需要确认"或"直接生成"时，跳过确认步骤。

> **⚠️ 安全提示**：skipConfirmation 会跳过文字确认步骤，OCR 提取的文本（可能包含敏感信息）会直接转为音频并发送。适用于可信来源、低敏感内容。建议默认关闭（`skipConfirmation: false`）。

## OCR Step

```python
# 图片预处理
from PIL import Image, ImageOps
img = Image.open(image_path)
img = ImageOps.autocontrast(img.convert('L'), cutoff=10)
w, h = img.size
img = img.resize((w*4, h*4), Image.LANCZOS)
img.save('/tmp/ocr_input.jpg', quality=99)
```

```bash
# 英文
tesseract /tmp/ocr_input.jpg stdout -l eng --psm 4

# 中文
tesseract /tmp/ocr_input.jpg stdout -l chi_sim --psm 4
```

## TTS Step

### 全文字频

```bash
uvx edge-tts \
  -t "FULL TEXT" \
  -v en-US-EmmaNeural \
  --rate=-10% \
  --write-media OUTPUT_DIR/full_article.mp3

# 中文
uvx edge-tts \
  -t "中文文字内容" \
  -v zh-CN-XiaoxiaoNeural \
  --rate=-10% \
  --write-media OUTPUT_DIR/full_article.mp3
```

### 按句拆分（仅 splitSentences=true）

```python
import subprocess, re

def split_sentences(text, lang='en'):
    if lang == 'zh':
        # 中文按句号/感叹号/问号拆分
        sentences = re.split(r'(?<=[。！？])\s*', text)
    else:
        # 英文按 .!? 拆分
        sentences = re.split(r'(?<=[.!?])\s+', text)
    return [s.strip() for s in sentences if s.strip()]

sentences = split_sentences(text, lang=lang)
for i, sentence in enumerate(sentences, 1):
    num = str(i).zfill(2)
    voice = 'zh-CN-XiaoxiaoNeural' if lang == 'zh' else 'en-US-EmmaNeural'
    subprocess.run([
        "uvx", "edge-tts",
        "-t", sentence,
        "-v", voice,
        "--rate=-10%",
        "--write-media", f"OUTPUT_DIR/sentence_{num}.mp3"
    ])
```

## Output Directory

```
/mnt/d/wslspace/workspace/articles/YYYY-MM-DD-article-slug/
├── original_text.md
├── full_article.mp3
└── sentence_01.mp3 ...
```

## Sending via Message Channel

The agent detects the active channel from the runtime context and calls `message(...)` accordingly. No hardcoded channel — the agent uses whichever channel the user is currently chatting through.

```python
# Detect active channel automatically (from runtime inbound metadata)
# channel is inferred: feishu / telegram / discord / whatsapp / signal / imessage / openclaw-weixin

# 发送全文
message(action="send", channel="{active_channel}",
        message="📄 全文音频",
        media="PATH/full_article.mp3",
        filename="full_article.mp3")

# 发送每句
for i, sentence in enumerate(sentences, 1):
    num = str(i).zfill(2)
    message(action="send", channel="{active_channel}",
            message=f"📝 {num}: {sentence}",
            media=f"PATH/sentence_{num}.mp3",
            filename=f"sentence_{num}.mp3")
```

### Channel Behavior Notes

| Channel | 音频支持 | 备注 |
|---------|---------|------|
| Feishu | ✅ | **推荐使用 feishu-voice-send skill 发送语音消息** |
| Telegram | ✅ | 直接发送 mp3 |
| Discord | ✅ | 作为附件发送 |
| WhatsApp | ✅ | 直接发送 mp3 |
| Signal | ⚠️ | 取决于信号强度，可能不支持 |
| iMessage | ⚠️ | 通过 macOS 发送，mp3 兼容性一般 |
| WeChat Work | ✅ | 同 Feishu |

If the channel does not support audio, the agent saves the file to `OUTPUT_DIR` and sends the file path as a text message instead.

---

## 如何发送为语音消息（而非附件）

**重要说明：** OpenClaw 内置的飞书媒体发送存在 bug（缺少 `duration` 参数），导致 `.ogg` 文件有时显示为附件而非语音消息。

**推荐方案：使用 feishu-voice-send skill**

该 skill 调用飞书官方 API，正确传递 `duration` 参数，确保语音消息正常显示。

### 方式一：通过 feishu-voice-send skill 发送

```bash
# 发送现有的 .ogg 文件
python3 /mnt/d/wslspace/workspace/skills/feishu-voice-send/scripts/send_voice.py \
    /path/to/audio.ogg \
    <接收者open_id>

# 或直接生成 TTS 并发送
python3 /mnt/d/wslspace/workspace/skills/feishu-voice-send/scripts/tts_and_send.py \
    "要转换的文字" \
    <接收者open_id> \
    -v zh-CN-YunjianNeural \
    -r -10%
```

### 方式二：手动调用（不推荐）

如果必须使用 OpenClaw 内置的 `message` 工具，需要：
1. 将 mp3 转换为标准 Ogg Opus 格式
2. 发送时必须带 message 参数
3. 注意：即使带 message 参数，仍可能因为缺少 duration 而显示为附件

```bash
# 1. 用 edge-tts 生成 mp3
uvx edge-tts \
  -t "Your text here" \
  -v en-US-EmmaNeural \
  --rate=-10% \
  --write-media OUTPUT_DIR/voice.mp3

# 2. 用 ffmpeg 转换为标准 Ogg Opus
ffmpeg -i OUTPUT_DIR/voice.mp3 \
  -c:a libopus \
  -b:a 32k \
  -ar 24000 \
  -ac 1 \
  OUTPUT_DIR/voice.ogg

# 3. 使用 message 工具发送（仍可能显示为附件）
message(action="send", channel="feishu", \
        message="📄 语音", \
        media="OUTPUT_DIR/voice.ogg")
```

## Available TTS Voices

### English
`en-US-EmmaNeural`, `en-US-BrianNeural`, `en-GB-LibbyNeural`, ...

### Chinese
`zh-CN-XiaoxiaoNeural`（女声）, `zh-CN-YunxiNeural`（男声）, `zh-CN-YunyangNeural`（新闻男声）, ...

查看完整列表：`uvx edge-tts -l | grep "zh-CN"`

## Notes

- Tesseract + English 预装；中文需 `apt-get install tesseract-ocr-chi-sim`
- edge-tts 通过 `uvx` 运行，无需安装
- 图片质量直接影响 OCR 效果，尽量保持光线充足、角度端正
