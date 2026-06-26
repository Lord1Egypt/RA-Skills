---
name: ffmpeg-chinese-subtitle
version: 1.0.0
description: |
  Windows 上使用 ffmpeg 正确生成中文字幕的解决方案。
  用 Pillow 在图片上绘制字幕，ffmpeg 只负责图片转视频，完全避开编码问题。
author: "systiger"
tags: ["ffmpeg", "subtitle", "chinese", "视频", "字幕"]
---

# ffmpeg Chinese Subtitle

Windows 上使用 ffmpeg 正确生成中文字幕的解决方案。

## 问题背景

在 Windows 上使用 ffmpeg 的 `drawtext`、`subtitles`、`ass` 滤镜处理中文字幕时，会遇到以下问题：

| 错误码 | 原因 |
|--------|------|
| 返回码 -22 (EINVAL) | 字体路径转义问题 |
| 字幕不显示 | 中文编码被截断 |
| 乱码 | 字符集不匹配 |

## 解决方案

**核心思路**：用 Pillow 在图片上绘制字幕，ffmpeg 只负责图片转视频。

### 方案对比

| 方案 | 状态 | 原因 |
|------|------|------|
| `drawtext=text='中文'` | ❌ 失败 | 命令行参数截断 |
| `subtitles='中文.srt'` | ❌ 失败 | 路径编码问题 |
| `ass='中文.ass'` | ❌ 失败 | 同上 |
| **Pillow 绘制 + ffmpeg** | ✅ 成功 | Python 原生支持 Unicode |

## 快速使用

```python
from ffmpeg_subtitle import add_subtitle_to_image

# 在图片上添加字幕
add_subtitle_to_image(
    image_path="input.png",
    subtitle_text="这是中文字幕",
    output_path="output.png",
    font_size=24,
    y_offset=50
)
```

## 参数说明

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `image_path` | - | 输入图片路径 |
| `subtitle_text` | - | 字幕文本 |
| `output_path` | - | 输出图片路径 |
| `font_size` | 24 | 字体大小 |
| `y_offset` | 50 | 距底部的偏移量（像素） |
| `font_color` | (255,255,255) | 字体颜色 RGB |
| `shadow_color` | (0,0,0) | 阴影颜色 RGB |

## 依赖

```
Pillow>=10.0.0
```

## 字体

默认使用 Windows 系统字体：
- 主字体：`C:/Windows/Fonts/msyh.ttc`（微软雅黑）
- 备用字体：`C:/Windows/Fonts/simhei.ttf`（黑体）

## 触发词

`ffmpeg字幕`、`中文字幕`、`视频字幕`、`字幕烧录`

## 文件结构

```
ffmpeg-chinese-subtitle/
├── SKILL.md           # 技能说明文档
├── README.md          # 详细使用指南
├── ffmpeg_subtitle.py # 核心模块
├── example.py         # 完整示例
└── package.json       # 包信息
```

## License

MIT

## Author

systiger
