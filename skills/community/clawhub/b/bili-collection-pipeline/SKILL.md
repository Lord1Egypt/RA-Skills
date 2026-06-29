---
name: bili-collection-pipeline
description: "B站/YouTube合集批量转录：拉取列表→下载→Whisper转录→语义分段→Markdown"
metadata:
  openclaw:
    requires:
      bins: [you-get, ffmpeg]
    install:
      - id: python
        kind: pip
        package: faster-whisper requests
        label: Install Python deps
---

# Bili Collection Pipeline

一键批量转录 B站合集 或 YouTube 播放列表，输出按语义分段的 Markdown 文件。

Supports **Bilibili** collections AND **YouTube** playlists!

## 流程 / Pipeline

```
B站视频/YouTube链接 → fetch_collection.py → 视频列表JSON
                                           → transcribe_collection.py → 下载→提音频→Whisper转录
                                                                          → semantic_segment.py → 语义分段
                                                                                                 → .md知识库
```

## 前置依赖 / Dependencies

```bash
# System tools
# you-get:  https://github.com/soimort/you-get          (for Bilibili)
# ffmpeg:   https://ffmpeg.org/
# yt-dlp:   https://github.com/yt-dlp/yt-dlp           (for YouTube + Bilibili fallback)
#   pip install yt-dlp

# Python
pip install faster-whisper requests
```

## 完整用法 / Usage

### 1. 拉取合集视频列表 (Fetch collection)

```bash
# Bilibili (by any video URL or BVID)
python3 scripts/fetch_collection.py "https://www.bilibili.com/video/BV1GeDSYhEVZ" -o collection.json

# YouTube (by playlist or video URL)
python3 scripts/fetch_collection.py "https://youtube.com/playlist?list=PLxxxxx" -o collection.json
python3 scripts/fetch_collection.py "https://youtu.be/xxxxx" -o collection.json
```

脚本自动检测是 B站还是 YouTube 链接。

### 2. 批量转录 (Batch transcribe)

```bash
python3 scripts/transcribe_collection.py collection.json \
    --output ./output --model small --device cuda --progress progress.json
```

- 自动断点续传（每集完成写入 progress.json）
- B站视频：you-get 下载（自动降级 yt-dlp）
- YouTube 视频：yt-dlp 下载音频
- 输出按 `标题.md` 命名

### 3. 语义分段 (Semantic segmentation)

```bash
python3 scripts/semantic_segment.py ./output/*.md
```

基于 Jaccard 词汇连贯性 + 结构信号进行智能分段。

### 4. (可选) LLM后处理

用 DeepSeek / OpenAI 兼容 API 做错别字修正或散文化改写。

## 文件说明 / Files

| 文件 | 作用 |
|------|------|
| `scripts/fetch_collection.py` | 解析B站合集或YouTube播放列表，输出JSON |
| `scripts/transcribe_collection.py` | 批量下载→转录→输出.md |
| `scripts/semantic_segment.py` | 语义分段v2算法 |

## 注意事项 / Notes

- **GPU显存**: Whisper small ~2GB, large-v3 ~6GB
- **yt-dlp**: YouTube 转录需要安装 `pip install yt-dlp`
- **B站412**: 如遇 you-get 412 封锁，脚本自动降级 yt-dlp
- **进度恢复**: 中断后重跑同一条命令会自动跳过已完成视频

## 实战战果 / Production Stats

- 波士顿圆脸「MAGA东山再起」203集 ✅ (B站)
- 战争研究所「研究一下」102集 ✅ (B站)
- 山河有声「战略杂谈」126集 ✅ (B站)
- MIT 8.02 电磁学 36集 ✅ (B站)
- YouTube 播放列表 ✅ (支持中)
