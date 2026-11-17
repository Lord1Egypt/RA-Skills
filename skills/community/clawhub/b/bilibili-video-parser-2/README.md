# B站视频解析

把B站视频链接转成中文字幕连贯稿和交互式 HTML 分析报告。优先使用CC字幕（秒出），无字幕时用 faster-whisper 本地转写。

## ⚠️ 安全声明

使用本工具前请知悉以下行为：

- **网络访问**：会访问 api.bilibili.com 获取视频元数据、CC字幕、音频流直链
- **音频下载**：无CC字幕时，从B站 CDN 下载音频流文件到临时目录
- **模型下载**：首次运行（无CC字幕时）会自动从 Hugging Face 下载 Whisper base 模型（约 74MB）
- **本地文件写入**：连贯稿 txt 和 HTML 报告会写入脚本同级 `work/` 目录（可用 `--out-dir` 指定）
- **推荐操作**：仅在信任的视频链接上使用；打开生成的 HTML 报告前确认来源可信

## 核心能力

- 从B站链接提取 BV号，通过公开 API 获取标题/UP主/时长等元数据
- **CC字幕优先**：有CC字幕的视频直接使用字幕数据，跳过转写，秒出结果
- 无字幕时基于 faster-whisper 离线语音转文字（base 模型，CPU，int8）
- 本地规则提取分析（一句话总结/核心观点/金句/结构拆解/内容判断/亮点）
- 生成交互式胶囊卡片 HTML 报告（六大模块，点击展开）
- 不依赖：ffmpeg、yt-dlp、curl、cookie、登录、API key

## 快速开始

```bash
# 安装依赖
pip install faster-whisper

# 解析视频（长链/短链/BV号都行）
python scripts/transcribe.py "https://www.bilibili.com/video/BV1Mu3y6NEzT"
python scripts/transcribe.py "https://b23.tv/xxx"
python scripts/transcribe.py "BV1Mu3y6NEzT"

# 用更准的 small 模型（长视频推荐）
python scripts/transcribe.py "<链接>" --model small

# 自定义输出目录
python scripts/transcribe.py "<链接>" --out-dir ./outputs
```

## 输出文件

| 文件 | 说明 |
|------|------|
| `MMDD-<BV号>-连贯稿.txt` | 纯文本字幕（无时间戳） |
| `MMDD-<BV号>-报告.html` | 交互式 HTML 报告（六大模块） |

终端默认只打印连贯稿前 500 字摘要，完整内容见 txt 文件。需全文打印加 `--print-transcript`。

## 要求

- Python 3.10+
- 首次运行（无CC字幕时）自动下载 Whisper base 模型（约 74MB）
- CPU 可用，无需 GPU
