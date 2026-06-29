---
name: douyin-video-to-txt
description: 抖音视频转文本知识库 — Download Douyin videos, transcribe to text via faster-whisper, save to Obsidian knowledge base.
args: <douyin_url> - 抖音视频链接
version: 2.0.1
---

# 抖音视频转文本知识库（douyin-video-to-txt）

下载抖音视频 → 提取音频 → faster-whisper 转写文字 → 输出双版本字幕 → 写入 Obsidian 知识库

纯本地运行，不需要任何外部 API Key。

## Prerequisites

| 工具 | 用途 | 安装 |
| --- | --- | --- |
| **yt-dlp** | 下载抖音视频 | `brew install yt-dlp` |
| **FFmpeg** | 提取音频 | `brew install ffmpeg` |
| **faster-whisper** | 语音转文字 | `pip3 install faster-whisper` |

环境变量（可选，用于 Obsidian 知识库路径）：
- `OBSIDIAN_VAULT_PATH` — Obsidian vault 根目录，默认 `~/Documents`

## Workflow

### Step 1: 获取视频信息并下载

```bash
mkdir -p /tmp/douyin_analysis/{VIDEO_ID}
cd /tmp/douyin_analysis/{VIDEO_ID}
yt-dlp --print-json "{DOUYIN_URL}" 2>/dev/null | python3 -c "
import json, sys
d = json.load(sys.stdin)
print(f'ID={d[\"id\"]}')
print(f'Title={d[\"title\"]}')
print(f'Duration={d[\"duration\"]}')
print(f'Uploader={d.get(\"uploader\",\"\")}')
print(f'UploadDate={d.get(\"upload_date\",\"\")}')
"
yt-dlp -o "video.mp4" "{DOUYIN_URL}" 2>/dev/null
```

### Step 2: 提取音频

```bash
ffmpeg -i video.mp4 -ar 16000 -ac 1 -c:a pcm_s16le audio.wav -y 2>/dev/null
```

### Step 3: 语音转文字（双版本输出）

```python
from faster_whisper import WhisperModel

model = WhisperModel('small', device='auto', compute_type='auto')
segments, info = model.transcribe('/tmp/douyin_analysis/{VIDEO_ID}/audio.wav', language='zh')

all_segments = []
for seg in segments:
    all_segments.append(seg)

# 输出 1: 带时间戳版本
with open('/tmp/douyin_analysis/{VIDEO_ID}/text.txt', 'w', encoding='utf-8') as f:
    for seg in all_segments:
        line = f'[{seg.start:.1f}s -> {seg.end:.1f}s] {seg.text.strip()}'
        f.write(line + '\n')

# 输出 2: 纯文字稿（无时间戳）
plain_lines = []
for seg in all_segments:
    plain_lines.append(seg.text.strip())
plain_text = '\n'.join(plain_lines)

with open('/tmp/douyin_analysis/{VIDEO_ID}/text_plain.txt', 'w', encoding='utf-8') as f:
    f.write(plain_text)
```

### Step 4: 写入 Obsidian 知识库

把纯文字稿保存到知识库中合适的目录下。每条视频保存为一个独立的 markdown 文件，格式如下：

```markdown
---
source: 抖音
url: {DOUYIN_URL}
author: {UPLOADER}
date: {UPLOAD_DATE}
duration: {DURATION}s
tags: [抖音转录, {AUTHOR}]
---

# {TITLE}

**来源：** 抖音 | **作者：** {UPLOADER} | **时长：** {DURATION}s

---

## 文字稿

{PLAIN_TEXT}
```

知识库路径规则：
- 优先写入 `$OBSIDIAN_VAULT_PATH/douyin_text/{TITLE_SLUG}.md`
- 如果 `OBSIDIAN_VAULT_PATH` 未设置，默认 `~/Documents/douyin_text/`
- 自动创建目录（如果不存在）

```bash
VAULT="${OBSIDIAN_VAULT_PATH:-$HOME/Documents}"
TARGET_DIR="$VAULT/douyin_text"
mkdir -p "$TARGET_DIR"

# 用视频标题做文件名（清理特殊字符）
SAFE_TITLE=$(echo "$VIDEO_TITLE" | sed 's/[\/:*?"<>|]/_/g' | cut -c1-60)
NOTE_PATH="$TARGET_DIR/${SAFE_TITLE}.md"

python3 << 'PYEOF'
import os
url = "{DOUYIN_URL}"
title = """{TITLE}"""
uploader = "{UPLOADER}"
date = "{UPLOAD_DATE}"
duration = "{DURATION}"

with open('/tmp/douyin_analysis/{VIDEO_ID}/text_plain.txt', 'r', encoding='utf-8') as f:
    plain_text = f.read()

note = f"""---
source: 抖音
url: {url}
author: {uploader}
date: {date}
duration: {duration}s
tags: [抖音转录, {uploader}]
---

# {title}

**来源：** [抖音]({url}) | **作者：** {uploader} | **时长：** {duration}s

---

## 文字稿

{plain_text}
"""

with open('{NOTE_PATH}', 'w', encoding='utf-8') as f:
    f.write(note)
PYEOF
```

### Step 5: 生成 AI 总结

读取 text.txt 和 text_plain.txt，用 AI 生成：
1. AI 标题（不超过 30 字）
2. AI 摘要（200-300 字）
3. 核心要点（3-5 条结构化要点）

同时把 AI 总结追加写入 Obsidian 笔记文件（在文字稿下方追加 `## AI 总结` 和 `### 核心要点` 部分）。

### 完整示例（一镜到底）

```bash
# 装依赖（首次）
brew install yt-dlp ffmpeg 2>/dev/null
pip3 install faster-whisper 2>&1 | tail -3

URL="https://www.douyin.com/video/xxxxx"
VID="xxx"
mkdir -p /tmp/douyin_analysis/$VID
cd /tmp/douyin_analysis/$VID

# 下载
yt-dlp -o "video.mp4" "$URL"

# 提取音频
ffmpeg -i video.mp4 -ar 16000 -ac 1 -c:a pcm_s16le audio.wav -y 2>/dev/null

# 转写（双版本）
python3 << 'PYEOF'
from faster_whisper import WhisperModel
model = WhisperModel('small', device='auto', compute_type='auto')
segments, info = model.transcribe('audio.wav', language='zh')
segs = [seg for seg in segments]

with open('text.txt', 'w', encoding='utf-8') as f:
    for seg in segs:
        f.write(f'[{seg.start:.1f}s -> {seg.end:.1f}s] {seg.text.strip()}\n')

plain = '\n'.join(s.text.strip() for s in segs)
with open('text_plain.txt', 'w', encoding='utf-8') as f:
    f.write(plain)
PYEOF

# 写入知识库
VAULT="${OBSIDIAN_VAULT_PATH:-$HOME/Documents}"
TARGET="$VAULT/douyin_text"
mkdir -p "$TARGET"
cp text_plain.txt "$TARGET/video-title.txt"
```

## Output

### 临时文件（`/tmp/douyin_analysis/{VIDEO_ID}/`）

| 文件 | 内容 |
| --- | --- |
| `video.mp4` | 下载的原视频 |
| `audio.wav` | 提取的音频（16kHz 单声道） |
| `text.txt` | **带时间戳**的完整字幕文本 |
| `text_plain.txt` | **纯文字稿**（无时间戳，连续文本） |

### 知识库文件

| 路径 | 内容 |
| --- | --- |
| `$OBSIDIAN_VAULT/douyin_text/{标题}.md` | 含元数据 + 完整文字稿 + AI 总结的笔记 |

## 注意事项

- **首次运行** faster-whisper 会从 HuggingFace 下载模型（small 约 466MB），需要网络连接
- **Apple Silicon** 上使用 `device='auto'` 会自动用 MPS（Metal）加速，速度很快
- **Proxy 问题**：如果 yt-dlp 下载失败，检查是否有代理在跑
- **标题清理**：文件名的特殊字符（`/ : * ? " < > |`）会自动替换为 `_`
- **AI 总结**：由 AI 在转写后生成，会追加到 Obsidian 笔记的文字稿下方

## 已知问题

- 长视频（>30分钟）转写时间较长，small 模型大约 1:1 实时
- Obsidian vault 路径优先从环境变量 `OBSIDIAN_VAULT_PATH` 读取，默认 `~/Documents`
