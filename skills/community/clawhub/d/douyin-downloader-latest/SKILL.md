---
name: douyin-downloader
description: 抖音无水印视频下载器，支持分享链接解析、批量下载和元数据保存
triggers:
  - 下载抖音
  - 解析抖音
  - 保存抖音
  - douyin download
  - 无水印
  - tiktok video
---

# 🎵 抖音下载器 (douyin-downloader)

下载抖音视频（无水印），支持分享链接解析和批量下载。

## 功能

1. **单链接解析** - 解析抖音分享链接，获取无水印视频地址
2. **批量下载** - 支持多个链接同时下载
3. **自动命名** - 根据视频信息自动生成文件名
4. **元数据保存** - 可选保存视频描述、作者信息等

## 使用示例

```
下载这个抖音视频：https://v.douyin.com/xxxxx

解析这些链接：
- https://v.douyin.com/xxx1
- https://v.douyin.com/xxx2
```

## 配置

在 `TOOLS.md` 中添加：

```markdown
### 抖音下载器

- 默认保存目录：~/Videos/douyin
- 是否保存元数据：true
```

## 依赖

- Node.js 18+
- ffmpeg（可选，用于视频处理）

## 注意事项

- 仅支持公开视频
- 请遵守抖音用户协议，仅用于个人学习
- 不要用于商业用途或批量爬取
