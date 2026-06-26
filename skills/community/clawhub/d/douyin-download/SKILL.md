---
name: douyin-download
description: 抖音无水印视频下载和文案提取工具
metadata:
  openclaw:
    emoji: 🎵
    requires:
      bins: [ffmpeg]
      env: [SILI_FLOW_API_KEY]
---

# douyin-download Skill

抖音无水印视频下载和文案提取工具。

## 功能

- 🎬 获取无水印视频下载链接
- 📥 下载抖音视频
- 🎙️ 从视频中提取语音文案（需要 API Key）
- ✂️ 语义分段（调用 OpenClaw 内置 LLM）

## 环境变量

- `SILI_FLOW_API_KEY` - 硅基流动 API 密钥（用于语音转文字）

获取 API Key: https://cloud.siliconflow.cn/

## 使用方法

### 获取视频信息

```bash
node /root/.openclaw/workspace/skills/douyin-download/douyin.js info "抖音分享链接"
```

### 下载视频

```bash
node /root/.openclaw/workspace/skills/douyin-download/douyin.js download "抖音链接" -o /tmp/douyin-download
```

### 提取文案（自动语义分段）

```bash
#SILI_FLOW_API_KEY="your-api-key"
node /root/.openclaw/workspace/skills/douyin-download/douyin.js extract "抖音链接"
```

- 自动调用 Silicon Flow ASR 提取文字
- 自动调用 OpenClaw 内置 LLM 进行**自然语义分段**

### 跳过语义分段

```bash
node /root/.openclaw/workspace/skills/douyin-download/douyin.js extract "抖音链接" --no-segment
```
