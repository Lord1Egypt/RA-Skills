---
name: douyin-video
description: 抖音视频下载工具 - 解析抖音链接，下载视频并发送
categories:
  - media
  - downloader
emoji: 📹
metadata:
  openclaw:
    requires:
      bins: ["node"]
---

# 抖音下载器

## 功能

- 🎬 解析抖音分享链接
- 📥 下载抖音视频到本地
- 💾 返回视频文件路径

## 使用方法

### 在 OpenClaw 中调用

```bash
node ~/.openclaw/workspace/skills/douyin-downloader/scripts/douyin.js "抖音分享链接"
```

### 输出

返回视频信息和本地文件路径：
- 视频标题
- 作者
- 点赞数
- 收藏数
- 分享数
- 本地文件路径（`~/.openclaw/workspace/douyin-downloads/douyin_last.mp4`）

**注意**: 
- 视频文件保存在工作区目录，**不会被系统自动清理**
- **自动清理**: 下载新视频时，会自动删除上一个视频
- **只保留一个视频**: 始终使用固定文件名 `douyin_last.mp4`
- **节省空间**: 不会累积多个视频文件
- 如需保留某个视频，请在下载后手动复制到其他目录

## 环境变量

无需配置，直接使用！

## 示例

**输入**:
```
https://v.douyin.com/FSfWiKriBuY/
```

**输出**:
```json
{
  "title": "这就是大大阮迪慧中的大大吗",
  "author": "香菇菇",
  "video_id": "7616783829047129778",
  "file_path": "~/.openclaw/workspace/douyin-downloads/douyin_last.mp4",
  "file_size": "3.73MB",
  "statistics": {
    "digg_count": 285756,
    "share_count": 180347,
    "collect_count": 40346
  }
}
```
