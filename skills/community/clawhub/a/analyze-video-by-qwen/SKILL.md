---
name: analyze-video-with-qwen
description: 使用 Qwen 3.5 Plus 模型分析视频内容，支持本地文件和远程 URL，可自定义分析提示词和抽帧频率
---

# Analyze Video with Qwen

## Overview

使用阿里云 Qwen 3.5 Plus 多模态模型对视频进行智能分析。支持本地视频文件和远程 URL，可自定义分析问题和视频抽帧频率（FPS）。

## 何时使用

- 需要理解视频内容、场景描述
- 需要视频中的动作识别、物体检测
- 需要生成视频摘要或分析报告
- 需要分析远程在线视频

## 快速用法

### 分析本地视频

默认设置分析视频：

```bash
python scripts/analyze.py /path/to/video.mp4
```

自定义提示词：

```bash
python scripts/analyze.py /path/to/video.mp4 --prompt "请详细描述视频中的每个场景"
```

自定义抽帧频率（FPS越高，分析越精细）：

```bash
python scripts/analyze.py /path/to/video.mp4 --fps 5
```

### 分析远程视频 URL

直接分析远程视频：

```bash
python scripts/analyze.py https://example.com/video.mp4
```

组合使用：

```bash
python scripts/analyze.py /path/to/video.mp4 --fps 3 --prompt "视频中出现了哪些人物和物体？"
python scripts/analyze.py https://example.com/video.mp4 --fps 4 --prompt "请详细描述视频场景"
```

## 参数说明

| 参数 | 说明 | 默认值 | 必填 |
|------|------|--------|------|
| `video_source` | 视频文件路径或远程 URL（支持 http/https） | - | 是 |
| `--fps` | 抽帧频率，每秒抽取的帧数 | 2 | 否 |
| `--prompt` | 分析提示词 | "这段视频描绘的是什么景象？" | 否 |

## 配置

API Key 从 `~/.openclaw/openclaw.json` 的 `skills.dashscope.apiKey` 字段读取。

如未配置，请添加以下内容：

```json
{
  "skills": {
    "dashscope": {
      "apiKey": "your-dashscope-api-key"
    }
  }
}
```

## 备注

- 本地视频路径可以是绝对路径或相对路径
- 远程视频 URL 必须是可公开访问的直链
- FPS 越高，API 调用成本越高，建议根据视频长度和需求调整
