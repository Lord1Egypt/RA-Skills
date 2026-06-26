---
name: free-douyin-downloader
description: 下载抖音视频到本地文件。当用户需要下载抖音视频、提取抖音链接内容、或保存抖音分享的视频时使用。支持抖音短链（v.douyin.com）、分享文本（含短链）、视频直链（douyin.com/video/...）三种输入格式。
---

# Douyin Downloader

下载抖音视频到本地，无水印（720p）。

## 用法

```bash
python3 scripts/douyin_download.py <链接或分享文本> [输出文件名]
```

**参数：**
- `<链接或分享文本>`：支持以下格式（必填）
  - 短链：`https://v.douyin.com/xxxxx/`
  - 分享文本：`7.15 复制打开抖音... https://v.douyin.com/xxxxx/`（直接粘贴整段文字即可）
  - 视频直链：`https://www.douyin.com/video/1234567890`
- `[输出文件名]`：可选，默认以视频标题命名，扩展名 `.mp4`

## 示例

```bash
# 短链
python3 scripts/douyin_download.py "https://v.douyin.com/FKWYQmtQ79E/"

# 分享文本（整段粘贴）
python3 scripts/douyin_download.py "7.15 复制打开抖音，看看【xxx的作品】 https://v.douyin.com/FKWYQmtQ79E/ "

# 指定输出文件名
python3 scripts/douyin_download.py "https://v.douyin.com/FKWYQmtQ79E/" my_video.mp4
```

## 注意

- 图文笔记类型不支持下载（脚本会提示）
- 需要网络可访问 douyin.com / iesdouyin.com
- 依赖：Python 3 标准库，无需额外安装
