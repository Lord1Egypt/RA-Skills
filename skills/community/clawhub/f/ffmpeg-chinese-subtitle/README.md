# ffmpeg Chinese Subtitle

> Windows 上使用 ffmpeg 正确生成中文字幕的解决方案

## 问题背景

在 Windows 上使用 ffmpeg 处理中文字幕时，会遇到各种编码问题：

```bash
# ❌ 这些方法在 Windows 上都会失败
ffmpeg -i input.mp4 -vf "drawtext=text='中文字幕':fontfile='C\\:/Windows/Fonts/msyh.ttc'" output.mp4
# 返回码 -22 (EINVAL)

ffmpeg -i input.mp4 -vf "subtitles='字幕.srt'" output.mp4
# 无法找到文件（路径编码问题）

ffmpeg -i input.mp4 -vf "ass='字幕.ass'" output.mp4
# 同样失败
```

## 根本原因

| 问题 | 原因 |
|------|------|
| `drawtext` 失败 | 字体路径中的反斜杠转义不稳定 |
| `subtitles` 失败 | SRT 文件路径包含中文字符时解析错误 |
| `ass` 失败 | 同上，文件路径编码问题 |
| 返回码 -22 | 参数无效 (EINVAL) |

## 解决方案

**核心思路**：用 Pillow 在图片上绘制字幕，ffmpeg 只负责图片转视频。

```
┌─────────────┐     ┌──────────────┐     ┌─────────────┐
│  原始图片    │ ──▶ │ Pillow 绘制   │ ──▶ │ 带字幕图片  │
└─────────────┘     │   中文字幕    │     └─────────────┘
                    └──────────────┘            │
                                                ▼
                    ┌──────────────┐     ┌─────────────┐
                    │   音频文件    │ ──▶ │  ffmpeg     │
                    └──────────────┘     │ 图片转视频  │
                                         └─────────────┘
                                                │
                                                ▼
                                         ┌─────────────┐
                                         │ 带字幕视频  │
                                         └─────────────┘
```

## 安装

```bash
pip install Pillow
```

## 快速开始

### 1. 添加字幕到图片

```python
from ffmpeg_subtitle import add_subtitle_to_image

add_subtitle_to_image(
    image_path="input.png",
    subtitle_text="这是中文字幕",
    output_path="output.png"
)
```

### 2. 创建带字幕的视频

```python
from example import create_video_with_subtitle

create_video_with_subtitle(
    image_path="cover.png",
    audio_path="audio.mp3",
    subtitle_text="欢迎观看本期视频",
    output_path="output.mp4"
)
```

## API 文档

### `add_subtitle_to_image()`

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `image_path` | str | - | 输入图片路径 |
| `subtitle_text` | str | - | 字幕文本 |
| `output_path` | str | - | 输出图片路径 |
| `font_size` | int | 24 | 字体大小 |
| `y_offset` | int | 50 | 距底部偏移（像素） |
| `font_color` | tuple | (255,255,255) | 字体颜色 RGB |
| `shadow_color` | tuple | (0,0,0) | 阴影颜色 RGB |
| `shadow_radius` | int | 2 | 阴影半径 |

### `create_video_with_subtitle()`

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `image_path` | str | - | 输入图片路径 |
| `audio_path` | str | - | 输入音频路径 |
| `subtitle_text` | str | - | 字幕文本 |
| `output_path` | str | - | 输出视频路径 |
| `width` | int | 1280 | 视频宽度 |
| `height` | int | 1024 | 视频高度 |

## 字体支持

自动检测系统字体：

- **Windows**: 微软雅黑、黑体、宋体
- **macOS**: PingFang SC
- **Linux**: Droid Sans Fallback

## 为什么不用 ffmpeg 原生字幕？

| 方案 | 状态 | 原因 |
|------|------|------|
| `drawtext` | ❌ | 命令行参数截断中文 |
| `subtitles` | ❌ | 文件路径编码问题 |
| `ass` | ❌ | 同上 |
| **Pillow + ffmpeg** | ✅ | Python 原生 Unicode 支持 |

## License

MIT

---

_作者: systiger_
