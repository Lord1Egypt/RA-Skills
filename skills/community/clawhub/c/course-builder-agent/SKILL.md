---
name: course-builder-agent
displayName: 课件自动生产线
slug: course-builder-agent
description: "输入文案，自动生成带数字人讲解的课件视频。一条龙：文案分页→中文幻灯片→配音→字幕→数字人驱动→合成视频。由VideoCraft Pro + 飞影数字人 + edge-tts 融合驱动。"
version: "1.0.0"
author: "智美人团队"
tags:
  - course
  - education
  - video
  - digital-human
  - automation
  - presentation
  - content-creation
metadata:
  openclaw:
    emoji: "🎬"
    requires:
      skills: [video-craft-pro, edge-tts]
---

# 🎬 课件自动生产线 — Course Builder Agent

> 输入文案，自动生成完整课件视频，带数字人讲解。

## 流程概览

```
文案输入 (Markdown/纯文本)
    │
    ▼
① 文案分析器 —— 自动分页，每页2-3个要点
    │
    ▼
② 中文幻灯片 —— 深色科技风，Noto Sans CJK字体
    │
    ▼
③ TTS配音 —— edge-tts Xiaoxiao/晓晓/云扬 可选
    │
    ▼
④ 字幕生成 —— 按TTS时长自动分割，SRT格式
    │
    ▼
⑤ 数字人驱动 —— [可选] 飞影数字人驱动口型同步
    │
    ▼
⑥ FFmpeg合成 —— 幻灯片+配音+字幕 → mp4视频
    │
    ▼
最终输出：带数字人的课件视频
```

## 使用方式

### 最简单：一句命令

```
course-builder> 生成课件 文案.txt
```

### 自定义配置

```
course-builder> 生成课件 文案.txt \
    --style 深色科技风 \
    --voice Xiaoxiao \
    --digital-human 智美人.jpg \
    --duration 3分钟
```

### 已经有PPT内容

```
course-builder> 生成课件 \
    --title "第03节：让AI学会记忆" \
    --pages 8 \
    --voice Xiaoxiao
```

## 参数说明

| 参数 | 说明 | 默认值 |
|------|------|--------|
| 文案 | 支持.md/.txt或直接粘贴 | 必填 |
| --style | 幻灯片风格（深色科技风/极简白/渐变） | 深色科技风 |
| --voice | 配音声线 | Xiaoxiao（知性女声） |
| --digital-human | 数字人照片路径 | 无（纯幻灯片） |
| --width | 视频宽 | 1920 |
| --height | 视频高 | 1080 |
| --fps | 帧率 | 10 |
| --caption | 字幕字体大小 | 36 |

## 内部流程

### 第一步：文案分析
- 自动拆分段落 → 每段一页幻灯片
- 代码块单独标记 → 用代码背景展示
- 识别标题层级 → 对应幻灯片标题大小

### 第二步：幻灯片生成 zh-slides.py
- Noto Sans CJK 中文字体
- 深色科技风背景
- 代码块深色背景+高亮注释

### 第三步：配音生成
- edge-tts 调用
- zh-CN-XiaoxiaoNeural（默认）
- 可选：Yunyang/Yunxi/Xiaohan/Xiaoshuang

### 第四步：字幕生成
- 按字数比例分配时间
- 每句2-5秒
- SRT标准格式

### 第五步：数字人（可选）
- 飞影数字人MCP接口
- 上传照片克隆形象
- 音频驱动口型同步
- 叠加到视频指定位置（开篇/结尾/全程）

### 第六步：合成
- ffmpeg slides concat
- 音频对齐到-shortest
- 字幕嵌入（可选）
- 输出mp4

## 参考文件

- `scripts/build.py` — 主构建脚本
- 调用 video-craft-pro/scripts/zh-slides.py 生成幻灯片
- 使用 edge-tts 生成配音
- 调用飞影数字人MCP（如已配置）
