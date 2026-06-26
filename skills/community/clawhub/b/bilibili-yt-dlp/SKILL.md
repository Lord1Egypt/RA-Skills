---
name: bilibili-yt-dlp
description: 使用 yt-dlp 和 ffmpeg 下载哔哩哔哩视频。
---

# 哔哩哔哩视频下载器

## 描述

一个用于下载哔哩哔哩视频的技能，使用 yt-dlp 下载，并使用 ffmpeg 合并音视频。

## 何时使用

在需要以下操作时使用此技能：

- 下载哔哩哔哩视频 (b23.tv/xxx 或 bilibili.com/video/xxx)
- 从哔哩哔哩网页提取视频
- 保存带音频的哔哩哔哩视频

## 前置要求

- 安装 yt-dlp：`pip3 install yt-dlp`
- 安装 ffmpeg：
  - **Mac**: `brew install ffmpeg`
  - **Windows**: 从 https://ffmpeg.org/download.html 下载或使用 `winget install ffmpeg`

## 使用方法

### 方法 1: 使用 yt-dlp（推荐）

```bash
# 查看可用格式
yt-dlp --list-formats "https://www.bilibili.com/video/BVxxxx"

# 下载最佳画质（4K/1080P60 可能需要大会员）
yt-dlp -f "best" -o "/path/to/video.mp4" "URL"

# 下载指定格式（视频+音频）
yt-dlp -f "30064+30216" -o "/path/to/video.mp4" "URL"
```

### 格式代码

| 画质 | 视频ID | 音频ID | 分辨率 |
|------|--------|--------|--------|
| 720P | 30064 | 30216 | 720x1280 |
| 480P | 30032 | 30216 | 480x852 |
| 360P | 30016 | 30216 | 360x640 |

### 方法 2: 使用浏览器手动下载

1. 在浏览器中打开哔哩哔哩链接：
```bash
browser action=open url="https://b23.tv/xxxxxx"
```

2. 使用浏览器控制台提取视频 URL：
```javascript
// 从 window.__playinfo__ 获取
var playinfo = window.__playinfo__;
JSON.stringify(playinfo);
```

3. 分别下载视频和音频，然后使用 ffmpeg 合并：
```bash
ffmpeg -i video.mp4 -i audio.m4a -c copy -y output.mp4
```

## 示例

### 示例 1: 使用 yt-dlp 下载（带 ffmpeg 合并）

```bash
# 先分别下载视频和音频
yt-dlp -f "30064+30216" -o "/Users/xbos1314/Documents/openclaw/file/video.%(ext)s" "https://www.bilibili.com/video/BV1EVZyBvEDu"

# 这将下载两个文件：视频和音频
# 然后使用 ffmpeg 合并（如果 yt-dlp 没有自动合并）
ffmpeg -i video.f30064.mp4 -i video.f30216.m4a -c copy -y output.mp4
```

### 示例 2: 简单下载（可能不适用于大会员专属内容）

```bash
yt-dlp -o "/Users/xbos1314/Documents/openclaw/file/video.mp4" "https://www.bilibili.com/video/BVxxxx"
```

## 注意事项

- 部分视频需要哔哩哔哩大会员才能下载高清画质（4K、1080P60）
- 格式选择：使用视频+音频格式代码以确保包含音频
- 默认输出目录：你的工作空间
- 视频 URL 有时效限制，可能会过期
- 如需认证，使用 --cookies-from-browser 或 --cookies
- **下载完成后使用 `browser action=close` 关闭浏览器标签页**
- 下载完成后将视频发送给用户 发送成功后删除视频文件
## 技术细节

- 使用 yt-dlp 下载哔哩哔哩视频
- 使用 ffmpeg 合并分离的视频和音频流
- 需要选择正确的格式以获得最佳效果
- 720P (30064+30216) 推荐给非大会员用户使用
