# 🎬 Bili Collection Pipeline

> B站合集批量转录工具 —— 下载→提音频→Whisper转录→LLM后处理

一键把B站**整个合集**转成可读的文本！从200+集的波士顿圆脸，到36集的MIT电磁学公开课，这套流水线已经实战验证了数千集。

## 核心流程

```
B站合集链接
    │
    ▼
📥 拉取视频列表 (B站API)
    │
    ▼
📦 批量下载 (you-get / yt-dlp)
    │
    ▼
🎵 提取音频 (ffmpeg → 16kHz mono WAV)
    │
    ▼
🎤 Whisper 转录 (faster-whisper small/large)
    │
    ▼
🛠️  后处理
    ├── 语义分段 (Jaccard词汇连贯性 + 结构信号)
    └── LLM润色 (DeepSeek / 本地LLM — 可选)
    │
    ▼
📚 知识库归档 (.md文件 + INDEX.md)
```

## 特性

- **合集级支持** — 不仅限于UP主空间，直接解析B站合集（播单）
- **断点续传** — 每集完成自动记录进度，重跑自动跳过
- **语义分段** — 基于词汇连贯性的智能分段，不是死板按字数切
- **GPU加速** — 支持 NVIDIA CUDA，RTX 4050 实测 ~7x 实时
- **后处理可选** — 错别字修正 / 删口头禅 / 散文化改写（DeepSeek API）

## 快速开始

### 依赖

```bash
# Python 3.10+
pip install faster-whisper requests

# 外部工具
# you-get: https://github.com/soimort/you-get
# ffmpeg: https://ffmpeg.org/
# yt-dlp: https://github.com/yt-dlp/yt-dlp (可选，you-get备选)
```

### 用法

**步骤1：拉取合集视频列表**

```bash
python3 scripts/fetch_collection.py <B站视频链接> --output videos.json
```

**步骤2：批量转录**

```bash
python3 scripts/transcribe_collection.py videos.json \
    --output ./transcripts \
    --model small \
    --progress progress.json
```

**步骤3：语义分段**

```bash
python3 scripts/semantic_segment.py ./transcripts/*.md
```

## 命令行参数

### transcribe_collection.py

| 参数 | 说明 | 默认 |
|------|------|------|
| `videos_json` | 视频列表JSON | 必填 |
| `--output` | 输出目录 | `./transcripts` |
| `--model` | Whisper模型尺寸 | `small` |
| `--device` | 运行设备 | `cuda` (auto-fallback to cpu) |
| `--progress` | 进度文件 | `progress.json` |
| `--downloader` | 下载器 | `you-get` |
| `--skip-download` | 跳过下载(已有音频) | false |
| `--limit` | 最大处理集数 | 全部 |

### semantic_segment.py

| 参数 | 说明 | 默认 |
|------|------|------|
| `files` | 待分段文件 | 必填 |
| `--force` | 强制重分(跳过检查) | false |

## 输出结构

```
transcripts/
├── 合集名-1-视频标题.md
├── 合集名-2-视频标题.md
├── ...
└── INDEX.md          # 自动生成目录索引
```

每个 .md 文件格式：
```markdown
# 视频标题

> BVID: BVxxxxx | 时长: 10分43秒

转录内容...
## 段落1
...
## 段落2
...
```

## 实战案例

- **波士顿圆脸「MAGA东山再起」** — 203集，~51h视频，全量转录
- **战争研究所「研究一下」** — 102集，~17.6h视频
- **山河有声「战略杂谈」** — 126集，~44.7h视频
- **MIT 8.02 电磁学公开课** — 36集，英文→中文全量翻译
- **金砖支付合集** — 8集

## 技术栈

| 组件 | 工具 |
|------|------|
| 下载 | you-get / yt-dlp |
| 音频提取 | ffmpeg (16kHz, mono, pcm_s16le) |
| 语音识别 | faster-whisper (small) |
| 语义分段 | 基于Jaccard相似度 + 结构信号 |
| LLM后处理 | DeepSeek / OpenAI / LM Studio (可选) |
| 输出格式 | Markdown (.md) |

## 许可

MIT
