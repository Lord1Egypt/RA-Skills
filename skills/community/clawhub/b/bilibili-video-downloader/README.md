# Bilibili Video Downloader

🎬 哔哩哔哩视频搜索与下载工具

## 功能特性

- 🔍 **视频搜索** - 根据关键词搜索B站视频
- ⬇️ **视频下载** - 支持多种清晰度（360P/480P/720P/1080P/1080P+/4K）
- 📊 **视频详情** - 获取标题、UP主、播放量、点赞等信息
- 📦 **批量下载** - 支持批量下载多个视频
- 👤 **UP主视频** - 获取指定UP主的全部视频列表
- 💬 **评论弹幕** - 获取视频评论和弹幕数据

## 安装

### 依赖要求

- Python 3.8+
- yt-dlp
- ffmpeg

### Windows

```powershell
winget install Python.Python.3.12
pip install yt-dlp
winget install Gyan.FFmpeg
```

### macOS

```bash
brew install python yt-dlp ffmpeg
```

### Linux

```bash
sudo apt install python3 python3-pip ffmpeg
pip3 install yt-dlp
```

## 使用方法

### 搜索视频

```powershell
# Windows
.\search.ps1 -Keyword "Python教程" -Limit 10

# macOS/Linux
./search.sh "Python教程" 10
```

### 下载视频

```powershell
# Windows
.\download.ps1 -Url "https://www.bilibili.com/video/BV1xx411c7mD" -Quality 1080

# macOS/Linux
./download.sh "https://www.bilibili.com/video/BV1xx411c7mD" 1080
```

### 获取视频信息

```powershell
# Windows
.\video-info.ps1 -Url "https://www.bilibili.com/video/BV1xx411c7mD"

# macOS/Linux
./video-info.sh "https://www.bilibili.com/video/BV1xx411c7mD"
```

## 可用脚本

| 脚本 | 功能 | Windows | macOS/Linux |
|------|------|---------|-------------|
| install-check | 检查依赖安装 | ✅ | ✅ |
| search | 搜索视频 | ✅ | ✅ |
| download | 下载单个视频 | ✅ | ✅ |
| download-batch | 批量下载 | ❌ | ✅ |
| video-info | 获取视频详情 | ✅ | ✅ |
| comments | 获取评论 | ❌ | ✅ |
| danmaku | 下载弹幕 | ❌ | ✅ |
| up-videos | 获取UP主视频 | ❌ | ✅ |

## ⚠️ 执行环境权限说明

本 Skill 的执行环境可能有安全限制：

| 功能 | 状态 | 说明 |
|------|------|------|
| 获取视频信息 | ✅ 可用 | 可以获取标题、播放量、清晰度等 |
| 生成下载命令 | ✅ 可用 | 可以生成 yt-dlp 命令 |
| 自动下载文件 | ⚠️ 受限 | 取决于执行环境权限 |

### 使用方式

**方式 1：手动执行（推荐）**
AI 提供下载命令，你自己复制粘贴运行：
```powershell
yt-dlp "https://www.bilibili.com/video/BV18NzvB5EZu" -o "$HOME\Downloads\%(title)s.%(ext)s"
```

**方式 2：提升权限（可选）**
如需 AI 直接下载文件，请参考 [PERMISSIONS.md](PERMISSIONS.md) 配置权限。

## 注意事项

- 下载的视频仅供个人学习使用，请遵守版权法规
- 部分视频需要登录才能下载高清版本
- 大会员专享视频需要配置 cookies

## 技术原理

基于 [yt-dlp](https://github.com/yt-dlp/yt-dlp) 实现：
- 视频搜索：使用 yt-dlp 的搜索功能
- 视频下载：自动选择最佳音视频流并合并
- 信息获取：解析B站API返回的元数据
- 弹幕/评论：调用B站公开API获取

## 许可证

MIT License
