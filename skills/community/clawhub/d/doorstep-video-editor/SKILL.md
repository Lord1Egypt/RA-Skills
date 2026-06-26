---
name: video-editor
description: "视频剪辑技能 - 基于moviepy + ffmpeg的视频处理工具箱。功能：(1) 裁剪/合并/分割视频，(2) 添加中文文字/字幕，(3) 添加/替换背景音乐，(4) 变速/调整尺寸，(5) 提取/替换音频，(6) 纯文字讲解视频生成。Use when: (1) 需要剪辑短视频（抖音/小红书），(2) 需要给视频加文字/字幕，(3) 需要合并多段视频，(4) 需要调整视频速度/尺寸，(5) 需要为视频配背景音乐。Triggers: '剪辑视频', '视频处理', '加文字', '加字幕', '合并视频', '加背景音乐', '变速', '视频裁剪', '竖屏转换'"
---

# Video Editor — 视频剪辑技能

## 概述

基于 moviepy v2 + ffmpeg 的本地视频剪辑工具箱。**无需任何外部API**，全部在本地完成。

## 前置条件

- Python: moviepy, pillow, numpy
- ffmpeg（由imageio-ffmpeg自动管理）

## 命令速查

```bash
# 查看视频信息
python {baseDir}/scripts/video_editor.py info "video.mp4"

# 裁剪片段 (3.5秒到8.2秒)
python {baseDir}/scripts/video_editor.py trim "video.mp4" 3.5 8.2

# 合并多个视频
python {baseDir}/scripts/video_editor.py merge "v1.mp4" "v2.mp4" "v3.mp4" -o=merged.mp4

# 加文字（底部）
python {baseDir}/scripts/video_editor.py text "video.mp4" "上门体育服务" bottom

# 加文字（顶部）
python {baseDir}/scripts/video_editor.py text "video.mp4" "私信我马上安排" top

# 加背景音乐（音量0.3）
python {baseDir}/scripts/video_editor.py music "video.mp4" "bgm.mp3" 0.3

# 变速（1.5倍）
python {baseDir}/scripts/video_editor.py speed "video.mp4" 1.5

# 转竖屏 (1080x1920)
python {baseDir}/scripts/video_editor.py resize "video.mp4" --width=1080 --height=1920

# 加字幕（需要JSON文件）
python {baseDir}/scripts/video_editor.py subtitles "video.mp4" "subtitles.json"

# 提取音频
python {baseDir}/scripts/video_editor.py audio "video.mp4" "output.mp3"

# 替换音频
python {baseDir}/scripts/video_editor.py replace_audio "video.mp4" "voiceover.mp3"

# 生成纯文字讲解视频
python {baseDir}/scripts/video_editor.py talk "上门体育服务，让运动像点外卖一样简单" 5
```

## 字幕JSON格式

```json
[
  {"start": 0, "end": 2.5, "text": "你是不是也有这些烦恼？"},
  {"start": 2.5, "end": 5, "text": "上班太累，没时间运动"},
  {"start": 5, "end": 7.5, "text": "私教太贵，健身房太远"},
  {"start": 7.5, "end": 10, "text": "上门体育，把私教带到你家"}
]
```

## 抖音/小红书常用操作

### 制作15秒竖屏宣传视频
1. 拍摄横屏素材 → resize转竖屏
2. 裁剪关键片段 → trim
3. 合并 > merge
4. 加文字标题 → text
5. 配背景音乐 → music

### 制作口播视频
1. 录制口播 → 提取音频
2. 替换更好的音轨 → replace_audio
3. 加字幕 → subtitles
4. 变速调整节奏 → speed
