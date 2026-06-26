---
name: ffmpeg_multimedia_editing
description: 使用 FFmpeg 进行多媒体编辑，包括视频剪辑、拼接、转码、特效、截图、水印、变速、音频处理等 20 种操作。当用户提到"FFmpeg""视频剪辑""视频拼接""视频压缩""视频格式转换""截图""水印""变速""倒放""GIF""音频提取""音频降噪""音量调节""画中画""裁剪""旋转""字幕""过渡特效""分段拆分""音乐拼接""音画合成""首尾帧""翻转""缩放""截图""硬字幕""软字幕""慢动作""加速""时间戳""时长""转码""编码"以及含义相近的词汇时引用；当用户需要对本地视频或音频文件进行处理时引用。不涉及 AI 内容生成。
metadata:
  openclaw:
    requires:
      bins:
        - uv
        - ffmpeg
        - ffprobe
      anyBins:
        - python
        - python3
        - py
      env:
        - OUTPUT_ROOT
---

# FFmpeg 多媒体编辑工具箱

使用 FFmpeg 对本地视频和音频文件进行编辑处理，支持 20 种常用操作。本 Skill 不调用任何外部 API，所有处理在本地完成。

适用场景：

- 用户需要对视频文件进行剪辑、拼接、转码、压缩、加特效等操作
- 用户需要从视频中提取音频、截图、获取首尾帧
- 用户需要添加字幕、水印、画中画等叠加效果
- 用户需要音频拼接、提取、降噪、音量调节
- 用户需要进行视频和 GIF 之间的转换
- 用户需要变速（慢动作/加速）、倒放、分段拆分

## 使用脚本

脚本位于 skill 目录内的 `scripts/`，运行时始终使用绝对路径。

设 `FFMPEG_SKILL_DIR` 为 `.claude/skills/ffmpeg-multimedia-editing` 的绝对路径。

### 视频操作

| 功能 | 脚本 | 关键参数 |
|------|------|----------|
| 字幕 | `video_subtitle.py` | `--input`, `--subtitle <srt/ass>`, `--mode soft\|hard` |
| 视频拼接 | `video_concat.py` | `--inputs a.mp4 b.mp4 ...` |
| 截图 | `video_screenshot.py` | `--input`, `--time`, `--interval`, `--count` |
| 获取首尾帧 | `video_firstlast_frame.py` | `--input` |
| 过渡特效 | `video_transition.py` | `--inputs a.mp4 b.mp4`, `--type fade\|dissolve`, `--duration` |
| 视频剪辑 | `video_trim.py` | `--input`, `--start`, `--end` |
| 格式转换 | `video_convert.py` | `--input`, `--format webm` |
| 压缩/缩放 | `video_compress_scale.py` | `--input`, `--resolution 720p`, `--crf 28` |
| 变速 | `video_speed.py` | `--input`, `--speed 0.5` |
| 水印 | `video_watermark.py` | `--input`, `--watermark <img>`, `--position top-right` |
| 裁剪/旋转/翻转 | `video_crop_rotate.py` | `--input`, `--crop WxH+X+Y`, `--rotate 90`, `--flip h\|v` |
| 画中画 | `video_pip.py` | `--main`, `--overlay`, `--position bottom-right` |
| 倒放 | `video_reverse.py` | `--input` |
| 分段拆分 | `video_split.py` | `--input`, `--segment-duration 60` |
| 视频/GIF互转 | `video_gif_convert.py` | `--input`, `--to gif\|mp4` |
| 音画合成 | `video_image_compose.py` | `--images <glob>`, `--duration 5`, `--audio` |

### 音频操作

| 功能 | 脚本 | 关键参数 |
|------|------|----------|
| 音乐拼接 | `audio_concat.py` | `--inputs a.mp3 b.mp3 ...` |
| 音频提取/替换 | `audio_extract_replace.py` | `--input video.mp4`, `--extract-audio` |
| 音量调节 | `audio_volume.py` | `--input`, `--volume 1.5`, `--normalize` |
| 音频降噪 | `audio_denoise.py` | `--input`, `--strength medium` |

## 快速调用

```powershell
# 截图
uv run --python python $FFMPEG_SKILL_DIR/scripts/video_screenshot.py --input video.mp4 --time 00:01:30

# 视频拼接
uv run --python python $FFMPEG_SKILL_DIR/scripts/video_concat.py --inputs a.mp4 b.mp4 c.mp4

# 音频提取
uv run --python python $FFMPEG_SKILL_DIR/scripts/audio_extract_replace.py --input video.mp4 --extract-audio

# 字幕嵌入
uv run --python python $FFMPEG_SKILL_DIR/scripts/video_subtitle.py --input video.mp4 --subtitle subs.srt
```

## 输出约定

- 本地输出目录：`outputs/ffmpeg/<operation>/`（相对于 `OUTPUT_ROOT`，默认为项目根目录）
- 所有脚本输出 JSON 至少包含：
  - `type` — `video` / `audio` / `image`
  - `operation` — 操作名称（如 `subtitle`, `concat`, `trim`）
  - `local_path` — 输出文件路径
  - `input_path` — 输入文件路径
  - `elapsed_seconds` — 处理耗时

## 配置

- 依赖：`ffmpeg`（full build 8.1+）和 `ffprobe`，需在 PATH 中可用
- 环境变量：`OUTPUT_ROOT`（可选，输出根目录，支持 `~` 展开，默认为用户主目录）
- 无需环境变量或外部 API 密钥
- 所有操作在本地执行，不涉及网络传输

## 协作方式

- 本 skill 为独立工具，可直接完成所有多媒体编辑操作
- 不与 content_generation_workflow 集成，也不依赖 AI 生成能力
- 如果用户需要将编辑后的文件上传为公网链接，可后续调用 qiniu skill 处理
