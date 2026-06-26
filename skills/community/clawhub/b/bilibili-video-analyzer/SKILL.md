---
name: bilibili-video-analyzer
description: Analyzes Bilibili academic/educational videos to extract knowledge points and generate clean-style study notes with screenshots. Use this skill when users provide a Bilibili video link and want to generate a professional learning report in card format with core concepts, detailed explanations, key points, and automatically captured screenshots.
---

# Bilibili Video Analyzer

## Overview

This skill analyzes Bilibili academic and educational videos to generate professional **clean-style learning notes** (清洁版学习笔记). It automates the complete workflow from video download and transcription to AI-powered content analysis and report generation with key screenshots.

**📚 Extended Resources:**
- 📖 [Best Practices Guide](references/BEST_PRACTICES.md) - 全面的最佳实践指南
- ✅ [Quality Checklist](references/QUICK_QUALITY_CHECKLIST.md) - 28项质量检查清单
- 📁 [References Index](references/README.md) - 参考文档导航

## When to Use This Skill

**Trigger phrases:**
- "分析这个B站视频: [link]"
- "帮我总结这个视频的知识点"
- "生成这个视频的学习报告"
- "提取这个视频的关键内容"

---

## Installation

### Prerequisites

- **Python 3.7+**
- **FFmpeg** (for video processing)
- Sufficient disk space (~1-2GB per video analysis)

### Install from PyPI

```bash
pip install railgun-bili-tools
```

### Verify Installation

```bash
bili-dl --version
```

### Install FFmpeg

**macOS:**
```bash
brew install ffmpeg
```

**Ubuntu/Debian:**
```bash
sudo apt install ffmpeg
```

**Windows:**
Download from [ffmpeg.org](https://ffmpeg.org/download.html) and add to PATH

---

## Workflow

**7-Step Automated Process:**

### Step 1: Login Check
```bash
bili-dl status
# If not logged in: bili-dl login
```

### Step 2: Parse Video Information
Extract metadata (title, uploader, duration) using `BilibiliParser`

### Step 3: Download Video
```bash
bili-dl download <video_url> --quality 1080p --output <output_dir>
```

### Step 4: Transcribe Audio
```bash
bili-dl transcribe <video_path> --model medium --srt
```

### Step 5: AI Content Analysis ⭐

**Claude analyzes the subtitle content and extracts:**
- **6-10 核心知识点** (knowledge point cards)
- Each point includes:
  - `title` (10-15字)
  - `core_concept` (20-30字核心概念)
  - `details` (200-400字详细说明,Markdown格式)
  - `key_points` (3-5个关键要点)
  - `timestamp` (视频时间戳)

**Output JSON Structure:**
```json
{
  "summary": "视频总览(100-200字)",
  "knowledge_points": [...],
  "key_screenshots": [
    {"timestamp": 280, "description": "截图描述", "reason": "选择原因"}
  ],
  "knowledge_framework": "知识体系结构",
  "practical_value": "实践价值说明",
  "learning_suggestions": ["学习建议1", "学习建议2", ...]
}
```

### Step 6: Capture Screenshots
```python
# 使用 scripts/screenshot_tool.py
ffmpeg -y -ss <timestamp> -i <video_path> -vframes 1 -q:v 2 <output.jpg>
```

### Step 7: Generate Report
Use `scripts/report_generator.py` to create clean-style learning notes

**Output Format:**
- 标题: 《{视频标题}》学习笔记
- 概览: 视频时长 + 知识点数量
- 核心内容: 📌 知识点卡片(核心概念 + 详细说明 + 关键要点 + 配图)
- 全文总结: 核心知识框架 + 实践价值 + 学习建议

## Quality Standards

**Based on successful case (BV1ms4y1Y76i):**

| Metric | Standard | Example |
|--------|----------|---------|
| 知识点数 | 6-10个 | 7个 |
| 单点字数 | 200-400字 | 平均320字 |
| 核心概念 | 20-30字 | 简洁有力 |
| 关键要点 | 3-5个/点 | 便于记忆 |
| 截图数量 | 10张 | 均匀分布 |
| 质量评分 | ≥25/28 | 优秀标准 |

**📋 Use [Quality Checklist](references/QUICK_QUALITY_CHECKLIST.md) for self-assessment**

---

## Key Features

✅ **Content Structure**
- Card-based layout (卡片式布局)
- Balanced information density (200-400字/点)
- Clear hierarchy (##/###/####)

✅ **Knowledge Extraction**
- 4-dimensional model: 现象+原因+方案+案例
- Core concept in one sentence (20-30字)
- 3-5 key points per card

✅ **Visual Support**
- 10 key screenshots
- 600px uniform width
- Precise timestamp alignment

✅ **Summary Framework**
- Knowledge structure tree
- Multi-dimensional practical value
- 6 actionable learning suggestions

---

## Technical Implementation

### Extract Subtitles
```python
from srt_parser import parse_srt_file, get_full_transcript
segments = parse_srt_file(srt_path)
full_text = get_full_transcript(segments, include_timestamps=False)
```

### Batch Screenshots
```python
import subprocess
for ts in timestamps:
    cmd = ["ffmpeg", "-y", "-ss", str(ts), "-i", video_path,
           "-vframes", "1", "-q:v", "2", output_file]
    subprocess.run(cmd)
```

### Safe JSON Output
```python
import json
output_path.write_text(
    json.dumps(analysis, ensure_ascii=False, indent=2),
    encoding='utf-8'
)
```

---

## Resources

### Scripts
- `scripts/srt_parser.py` - Parse SRT subtitle files
- `scripts/screenshot_tool.py` - Capture video frames at specific timestamps
- `scripts/report_generator.py` - Generate clean-style learning notes

### Reference Docs
- 📖 [BEST_PRACTICES.md](references/BEST_PRACTICES.md) - 全面的最佳实践指南(535行)
- ✅ [QUICK_QUALITY_CHECKLIST.md](references/QUICK_QUALITY_CHECKLIST.md) - 28项质量检查清单
- 📁 [references/README.md](references/README.md) - 参考文档导航

---

## Quick Start Guide

**For First-Time Users:**
1. Read this SKILL.md to understand the workflow
2. Check [BEST_PRACTICES.md](references/BEST_PRACTICES.md) sections 1-5
3. Review the example case: `reports/2026-02-28/BV1ms4y1Y76i_*/`
4. Use [Quality Checklist](references/QUICK_QUALITY_CHECKLIST.md) to evaluate your output

**For Experienced Users:**
1. Generate notes using the skill
2. Quick check with the quality checklist
3. Reference best practices when needed
4. Optimize using technical implementation code

---

## Version

**Current**: v1.1.0 (2026-02-28)
- ✅ Enhanced content generation guidelines
- ✅ Comprehensive best practices documentation
- ✅ 28-item quality checklist
- ✅ Real successful case examples

See [CHANGELOG.md](CHANGELOG.md) for version history.
