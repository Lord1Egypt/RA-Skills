---
name: fast-douyin-publish
description: 抖音视频自动发布助手。一键上传视频到抖音，支持自动文案生成和标签优化。
license: MIT
metadata:
  author: DeadLining
  tags: ["douyin-publisher", "douyin", "video", "automation"]
---

# 抖音视频发布助手

一键抖音登陆，上传视频到抖音。

## Features

- ✅ **一键发布** - 简单操作，快速发布
- ✅ **自动文案** - 智能生成标题和标签（标题长度限制30字符）
- ✅ **发布记录** - 自动保存发布历史
- ✅ **二维码登录** - 安全便捷，无需密码

## Quick Start

### 0. 进入 Conda 环境（mllm 为作者本地环境）

```bash
conda activate mllm
```

### 1. 安装依赖

```bash
pip install playwright
playwright install chromium
```

### 2. 配置账号

首次运行自动创建 `config/accounts.json`

### 3. 发布视频

```bash
# 手动指定标题和标签
python scripts/auto_publisher.py "video.mp4" --title "我的视频" --tags "AI,科技,创新"

# 无头模式
python scripts/auto_publisher.py "video.mp4" --title "我的视频" --tags "AI,科技" --headless
```

**注意**：`--title` 和 `--tags` 是必填参数。如果用户未提供标题或标签，skill 应根据视频文件名自动生成标题和标签。

## Platform

| Platform | Login | Title Limit | Duration Limit |
|----------|-------|-------------|----------------|
| 抖音  | QR Code | 30 chars | 15 min |

## Scripts

- `scripts/auto_publisher.py` - 主发布程序

## Config

- `config/accounts.json` - 账号配置
- `config/publish_log.json` - 发布记录
- `config/cookies/douyin.json` - 登录状态

## Commands / Triggers

Use this skill when:
- "发布视频到抖音"
- "上传视频到抖音"
- "抖音发布"

## Security Notes

- Cookie 保存在本地，注意保密
- 定期更新登录状态
- 不要分享账号配置文件

## Troubleshooting

### Login timeout
- Check network connection
- Manually visit the platform website
- Re-run and scan QR code again

### Publish failed
- Check video format (MP4 recommended)
- Check video size limits
- View browser window for error details

### Playwright errors
```bash
pip install --upgrade pip
pip install playwright
playwright install chromium
```
