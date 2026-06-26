---
name: "seedance-api"
description: "调用火山引擎 Seedance 视频生成 API。当用户需要生成视频、文生视频、图生视频时使用此 skill。"
version: "1.0.0"
required_env_vars:
  - VOLCENGINE_API_KEY
---

# Seedance Video API 调用

此 skill 用于调用火山引擎 Seedance 视频生成 API，支持文生视频、图生视频、首尾帧视频等功能。

**使用方式：** 用户只需提供视频描述，我直接调用 API 生成视频并返回本地文件。

## 支持的模型

| 名称 | Model ID | 说明 |
|------|----------|------|
| 1.5-pro (最新) | `doubao-seedance-1-5-pro-251215` | 默认，支持有声视频 |
| 1.0-pro | `doubao-seedance-1-0-pro-250121` | |
| 1.0-pro-fast | `doubao-seedance-1-0-pro-fast-250121` | 快速模式 |
| 1.0-lite-t2v | `doubao-seedance-1-0-lite-t2v-241118` | 文生视频 |
| 1.0-lite-i2v | `doubao-seedance-1-0-lite-i2v-241118` | 图生视频 |

## 直接调用

用户说"生成一个xxx视频"时，直接运行：

```bash
python seedance_api.py "一只小猫打哈欠"
```

指定参数：
```bash
python seedance_api.py "一只小猫打哈欠" -m 1.5-pro -d 5 -r 16:9 -s 720p
```

图生视频：
```bash
python seedance_api.py "小猫奔跑" -i "https://example.com/cat.jpg"
```

首尾帧视频：
```bash
python seedance_api.py "过渡动画" --first-frame "https://example.com/start.jpg" --last-frame "https://example.com/end.jpg"
```

## 参数说明

| 参数 | 说明 | 默认值 |
|------|------|--------|
| -m, --model | 模型版本 | 1.5-pro |
| -d, --duration | 视频时长(秒) 2-12 | 5 |
| -r, --ratio | 宽高比 16:9/4:3/1:1/3:4/9:16/21:9/adaptive | 16:9 |
| -s, --resolution | 分辨率 480p/720p/1080p | 720p |
| -o, --output-dir | 输出目录 | output |
| -i, --image | 图生视频：参考图片 URL | - |
| --first-frame | 首尾帧视频：首帧图片 URL | - |
| --last-frame | 首尾帧视频：尾帧图片 URL | - |
| --no-audio | 不生成音频 | - |
| --seed | 随机种子 | - |
| --fixed | 固定摄像头 | - |
| --watermark | 添加水印 | - |

## 使用此 Skill

当用户需要以下功能时，使用此 skill：
- 生成视频（文生视频）
- 根据图片生成视频（图生视频）
- 首尾帧生成视频
- 使用 Seedance 视频模型进行视频生成

在调用前，确保：
1. 已获取火山引擎 API Key
2. 已开通 Seedance 视频生成模型服务
3. 了解所需的使用场景和参数配置
