---
name: "视频下载器"
description: "使用yt-dlp和ffmpeg下载各种网站的视频。支持YouTube、B站、抖音等所有yt-dlp支持的网站。当用户要求下载视频、保存视频、抓取视频时调用此技能。"
---

# 视频下载器

使用yt-dlp和ffmpeg下载各种网站的视频，支持所有yt-dlp支持的网站。

## 功能特点

- 支持所有yt-dlp支持的网站（YouTube、B站、抖音、快手、Instagram、Twitter等）
- 自动下载并合并视频和音频流
- 默认下载1080p MP4格式
- 自动安装和更新yt-dlp
- 自动检测和使用ffmpeg进行视频合并

## 快速开始

最简单的下载方式：

```bash
python download_video.py "视频URL"
```

这会下载视频到用户下载目录（`~/Downloads`），文件名使用视频标题。

技能会自动：
- 下载并设置ffmpeg（如果未安装）
- 检查并安装yt-dlp（如果未安装）
- 合并视频和音频流

## 选项

### 质量设置

使用`-q`或`--quality`指定视频质量：

- `best`：最高质量
- `1080p`：全高清（默认）
- `720p`：高清
- `480p`：标清
- `360p`：较低质量

示例：
```bash
python download_video.py "URL" -q 1080p
```

### 格式选项

指定输出格式：

- `mp4`（默认）：最兼容的格式
- `webm`：现代格式
- `mkv`：Matroska容器

示例：
```bash
python download_video.py "URL" -q 1080p
```

### 只下载音频

使用`-a`或`--audio-only`只下载音频：

```bash
python download_video.py "URL" -a
```

### 自定义输出目录

使用`-o`或`--output`指定输出目录：

```bash
python download_video.py "URL" -o "D:/Videos"
```

## 完整示例

1. 下载1080p MP4视频到用户下载目录：
```bash
python download_video.py "https://www.youtube.com/watch?v=VIDEO_ID"
```

2. 下载B站视频：
```bash
python download_video.py "https://www.bilibili.com/video/BV..."
```

3. 只下载音频为MP3：
```bash
python download_video.py "URL" -a
```

4. 下载720p视频：
```bash
python download_video.py "URL" -q 720p
```

5. 下载到指定目录：
```bash
python download_video.py "URL" -o "D:/Videos"
```

## 工作原理

技能使用`yt-dlp`和`ffmpeg`：
- 自动下载并设置ffmpeg（如果未安装）
- 自动检查并安装yt-dlp（如果未安装）
- 获取视频信息
- 选择最佳的视频和音频流
- 使用内置ffmpeg合并视频和音频流
- 支持广泛的视频网站和格式

## 重要说明

- 默认下载到用户下载目录：`~/Downloads`
- 视频文件名自动从视频标题生成
- ffmpeg会自动下载到技能目录（`.trae/skills/视频下载器/ffmpeg/`）
- 较高质量的视频可能需要更长的下载时间和更多磁盘空间
- 某些网站可能需要使用浏览器cookies进行认证

## 使用浏览器cookies（可选）

对于需要登录的视频，可以使用浏览器cookies：

```bash
yt-dlp "URL" --cookies-from-browser chrome
yt-dlp "URL" --cookies-from-browser edge
yt-dlp "URL" --cookies-from-browser firefox
```

## 常见问题

1. **403 Forbidden错误**：YouTube等网站的反爬虫机制，可以尝试：
   - 更新yt-dlp：`pip install --upgrade yt-dlp`
   - 使用浏览器cookies
   - 筭待一段时间后重试

2. **视频质量不理想**：尝试使用不同的格式选择器或使用浏览器cookies

3. **ffmpeg下载失败**：如果自动下载ffmpeg失败，可以手动下载并解压到技能目录的`ffmpeg/`文件夹
