---
name: bilibili-video-downloader
description: |
  哔哩哔哩视频搜索与下载工具。使用场景：
  - 根据关键词搜索B站视频
  - 下载B站视频（支持多种清晰度）
  - 获取视频详情、弹幕、评论
  - 批量下载UP主视频
  - "帮我下载B站上的XX视频"
  - "搜索B站关于XX的视频"
  - "把B站这个视频下载下来"
  - "获取B站视频弹幕"
metadata:
  openclaw:
    emoji: "📺"
---

# Bilibili Video Downloader

基于 [yt-dlp](https://github.com/yt-dlp/yt-dlp) 封装的哔哩哔哩视频下载工具。

## 快速参考

| 脚本 | 用途 |
|------|------|
| `install-check.ps1` | 检查依赖是否安装 (Windows) |
| `install-check.sh` | 检查依赖是否安装 (macOS/Linux) |
| `search.ps1/sh <关键词> [数量]` | 搜索B站视频 |
| `download.ps1/sh <URL> [清晰度]` | 下载单个视频 |
| `video-info.ps1/sh <URL>` | 获取视频详情 |

## 快速开始

### Windows

```powershell
cd scripts\

# 1. 检查依赖
.\install-check.ps1

# 2. 搜索视频
.\search.ps1 -Keyword "Python教程" -Limit 10

# 3. 下载视频（默认最高清晰度）
.\download.ps1 -Url "https://www.bilibili.com/video/BV1xx411c7mD"

# 4. 指定清晰度下载
.\download.ps1 -Url "https://www.bilibili.com/video/BV1xx411c7mD" -Quality 1080
```

### macOS / Linux

```bash
cd scripts/

# 1. 检查依赖
./install-check.sh

# 2. 搜索视频
./search.sh "Python教程" 10

# 3. 下载视频
./download.sh "https://www.bilibili.com/video/BV1xx411c7mD"
```

## 搜索视频

### Windows
```powershell
.\search.ps1 -Keyword "关键词" -Limit 20

# 示例
.\search.ps1 -Keyword "深度学习" -Limit 20
.\search.ps1 -Keyword "考研数学" -Limit 10
```

### macOS / Linux
```bash
./search.sh "关键词" [结果数量]

# 示例
./search.sh "深度学习" 20
./search.sh "考研数学" 10
```

输出格式：
```
标题 | UP主 | 播放量 | BV号 | 链接
```

## 下载视频

### 单视频下载

**Windows:**
```powershell
.\download.ps1 -Url "<URL>" -Quality <清晰度> -OutputDir <目录>

# 清晰度选项: 360, 480, 720, 1080, 1080p+, 4K (默认best)

.\download.ps1 -Url "https://www.bilibili.com/video/BV1xx411c7mD"
.\download.ps1 -Url "https://www.bilibili.com/video/BV1xx411c7mD" -Quality 1080 -OutputDir ".\my-videos"
```

**macOS / Linux:**
```bash
./download.sh <URL> [清晰度] [输出目录]

./download.sh "https://www.bilibili.com/video/BV1xx411c7mD"
./download.sh "https://www.bilibili.com/video/BV1xx411c7mD" 1080 ./downloads
```

### 批量下载

创建包含URL的文件（每行一个）：
```
https://www.bilibili.com/video/BV1xx411c7mD
https://www.bilibili.com/video/BV1yy411c7nE
https://www.bilibili.com/video/BV1zz411c7oF
```

然后执行（macOS/Linux）：
```bash
./download-batch.sh urls.txt 1080 ./downloads
```

## 获取视频信息

**Windows:**
```powershell
.\video-info.ps1 -Url "https://www.bilibili.com/video/BV1xx411c7mD"
```

**macOS / Linux:**
```bash
./video-info.sh "https://www.bilibili.com/video/BV1xx411c7mD"
```

## 获取UP主视频列表 (macOS/Linux)

```bash
# 获取UP主视频列表
./up-videos.sh "UID" 50

# 示例：获取UID为208259的UP主前30个视频
./up-videos.sh 208259 30
```

如何获取UID：打开UP主主页，URL中的数字就是UID，如 `space.bilibili.com/208259`

## 获取评论 (macOS/Linux)

```bash
./comments.sh "https://www.bilibili.com/video/BV1xx411c7mD" 100
```

## 下载弹幕 (macOS/Linux)

```bash
./danmaku.sh "https://www.bilibili.com/video/BV1xx411c7mD" danmaku.xml
```

## 依赖要求

- Python 3.8+
- yt-dlp
- ffmpeg (用于合并音视频)

## 安装依赖

### Windows

```powershell
# 安装 Python
winget install Python.Python.3.12

# 安装 yt-dlp
pip install yt-dlp

# 安装 ffmpeg
winget install Gyan.FFmpeg
```

### macOS

```bash
# 安装 Python 和 yt-dlp
brew install python yt-dlp ffmpeg

# 或
pip3 install yt-dlp
```

### Ubuntu / Debian

```bash
sudo apt update
sudo apt install python3 python3-pip ffmpeg
pip3 install yt-dlp
```

## 注意事项

- 下载的视频仅供个人学习使用，请遵守版权法规
- 部分视频需要登录才能下载高清版本
- 大会员专享视频需要配置cookies
- 建议配置cookies以获得最佳下载体验

## 配置Cookies（可选）

如需下载大会员专享或高清视频，配置cookies：

1. 浏览器登录B站
2. 使用浏览器扩展导出cookies为txt格式（如 "Get cookies.txt"）
3. 保存为 `cookies.txt` 放在脚本目录

## 执行环境权限说明

⚠️ **重要提示**：本 Skill 的执行环境有安全限制，可能无法直接写入文件。

| 功能 | 状态 | 说明 |
|------|------|------|
| 获取视频信息 | ✅ 可用 | 可以获取标题、播放量、清晰度等 |
| 生成下载命令 | ✅ 可用 | 可以生成 yt-dlp 命令 |
| 自动下载文件 | ⚠️ 受限 | 取决于执行环境权限 |

### 解决方案

**方案 A：手动执行（推荐）**
AI 提供下载命令，你自己复制粘贴运行：
```powershell
yt-dlp "https://www.bilibili.com/video/BV18NzvB5EZu" -o "$HOME\Downloads\%(title)s.%(ext)s"
```

**方案 B：提升权限（可选）**
如需 AI 直接下载文件，请参考 [PERMISSIONS.md](PERMISSIONS.md) 配置权限。

## 工作原理

本Skill基于 [yt-dlp](https://github.com/yt-dlp/yt-dlp) 实现：
- 视频搜索：使用 yt-dlp 的搜索功能
- 视频下载：自动选择最佳音视频流并合并
- 信息获取：解析B站API返回的元数据
- 弹幕/评论：调用B站公开API获取
