---
name: bilibili-ytdlp-summary
description: 当用户提供 B 站视频链接、BV 号或 b23.tv 短链，使用 yt-dlp 下载音频 + 硅基流动 ASR 转写，优先尝试官方字幕。支持 QQbot 自动推送。需要 node、yt-dlp 和 SILICONFLOW_API_KEY。
metadata: {"openclaw":{"homepage":"https://cloud.siliconflow.cn/me/account/ak","primaryEnv":"SILICONFLOW_API_KEY","requires":{"bins":["node","yt-dlp"],"env":[]}}}
---

# B 站视频转录与总结（yt-dlp 增强版）

当用户给出 B 站视频链接，并希望了解视频内容、获取转录文字或让 AI 做总结时，使用这个 skill。

## 触发条件

满足以下两点时触发：

- 用户输入的是 B 站标准链接、`BV...` 号，或者 `https://b23.tv/...` 短链接。
- 用户意图是转录、提取字幕、总结、分析视频内容。

## 工作流程

1. 先检查 `node` 和 `yt-dlp` 是否可用。
2. 如果大概率需要语音转写，再检查 `SILICONFLOW_API_KEY` 是否已注入。
3. 运行 `scripts/bilibili_pipeline.mjs`。
4. 使用 `yt-dlp --dump-json` 获取视频元信息（标题、BV号、时长等）。
5. **优先使用官方字幕** — 从 B 站 API 拉取字幕文件。
6. 如果没有字幕，则通过 `yt-dlp` 下载最佳音频流（m4a 格式）。
7. 如果存在 API key，则调用硅基流动 `TeleAI/TeleSpeechASR` 进行转写。
8. 获取文字后，按用户要求进行总结；如果用户没有说明，就默认输出重点总结。

## 与旧版爬虫方案的区别

旧版通过纯 HTML 爬虫提取 `__playinfo__` 数据，但 B 站已全面转向 SPA 渲染，该方法基本失效。

**新版改为使用 yt-dlp 下载音频**，yt-dlp 内部处理了 B 站的 WBI 签名、重定向、cookie 等复杂逻辑，成功率大幅提升。

## 依赖与环境检查

首次成功运行前先检查：

- `node --version` 是否可用（要求 Node.js 18+）。
- `yt-dlp --version` 是否可用。
- 如果要做 ASR，`SILICONFLOW_API_KEY` 是否已注入。

如果缺少 Node.js，请先引导用户安装 Node.js 18+。

如果缺少 yt-dlp，安装方式：

```bash
pip3 install yt-dlp
```

如果缺少 API key，请提示用户前往以下页面创建：

- https://cloud.siliconflow.cn/me/account/ak

## 输出文件

脚本会在输出目录写入：

- `summary.md`：包含视频信息、AI 结构化总结和完整文字稿的文档
- `transcript.txt`：纯文字稿
- `probe_result.json`：页面解析结果
- `transcription_result.json`：硅基流动转写返回结果

> **音频自动清理**：转写完成后，音频文件自动删除，避免占用磁盘空间。

## 说明

- 基于 [bilibili-video-transcribe-summary](https://clawhub.ai/Markusbetter/bilibili-video-transcribe-summary) 修改，核心改为 yt-dlp 下载方案
- 已验证可处理长视频（30+ 分钟）的下载和 ASR 转写
- 音频文件转写后自动清理
- 支持通过 QQbot 自动推送处理结果
