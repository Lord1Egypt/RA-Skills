---
name: bilibili-transcribe-summary
description: 当用户提供 B 站视频链接、BV 号或 b23.tv 短链，并希望转录、提取字幕、总结或分析视频内容时使用。先检查 Node.js 环境和 SILICONFLOW_API_KEY，优先尝试官方字幕；如果没有字幕，则获取匿名音频地址，下载为 .m4s 后直接改名为 .mp3，无需转码；有 API key 时调用硅基流动 ASR，再按用户要求总结；如果用户没有特别要求，默认输出重点总结。
metadata: {"openclaw":{"homepage":"https://cloud.siliconflow.cn/me/account/ak","primaryEnv":"SILICONFLOW_API_KEY","requires":{"bins":["node"],"env":[]}}}
---

# B 站视频转录与总结

当用户给出 B 站视频链接，并希望了解视频内容、获取转录文字或让 AI 做总结时，使用这个 skill。

## 触发条件

满足以下两点时触发：

- 用户输入的是 B 站标准链接、`BV...` 号，或者 `https://b23.tv/...` 短链接。
- 用户意图是转录、提取字幕、总结、分析视频内容。

## 工作流程

1. 先检查 `node --version`，要求 Node.js 18 及以上。
2. 如果大概率需要语音转写，再检查 `SILICONFLOW_API_KEY` 是否存在。
3. 运行 `scripts/bilibili_pipeline.mjs`。
4. 优先使用官方字幕。
5. 如果没有字幕，则从页面播放信息中提取匿名音频地址。
6. 下载得到 `.m4s` 文件后，直接改名为 `.mp3`，不做转码。
7. 如果存在 API key，则调用硅基流动 `TeleAI/TeleSpeechASR` 进行转写。
8. 获取文字后，按用户要求进行总结；如果用户没有说明，就默认输出重点总结。

## 首次成功后的标记文件

脚本在第一次成功执行 `probe` 或 `run` 后，会在输出目录写入 `.skill-ready.json`。

如果这个文件已经存在，就默认环境已经准备过了，后续再次使用时不必重复做依赖和 API key 的提示说明，直接执行即可。只有当脚本真正失败时，再回退到安装或配置引导。

## 依赖与环境检查

首次成功运行前先检查：

- `node --version` 是否可用。
- 如果要做 ASR，`SILICONFLOW_API_KEY` 是否已注入。
- 如果环境限制联网，需要先申请网络权限。

如果输出目录里已经存在 `.skill-ready.json`，则默认跳过重复检查。

如果缺少 Node.js，请先引导用户安装 Node.js 18+，再继续执行。

如果缺少 API key，请提示用户前往以下页面创建：

- https://cloud.siliconflow.cn/me/account/ak

然后再设置环境变量并重试，例如：

```powershell
$env:SILICONFLOW_API_KEY="你的_key"
```

```bash
export SILICONFLOW_API_KEY="你的_key"
```

更完整的安装与重试说明，请阅读 `setup.md`。

## 常用命令

只探测，不下载音频：

```bash
node scripts/bilibili_pipeline.mjs probe "https://www.bilibili.com/video/BV1R6PzzAE9k" --output-dir ./output
```

完整执行：

```bash
node scripts/bilibili_pipeline.mjs run "https://www.bilibili.com/video/BV1R6PzzAE9k" --output-dir ./output
```

短链接也可直接使用：

```bash
node scripts/bilibili_pipeline.mjs run "https://b23.tv/lsocHNd" --output-dir ./output
```

## 输出文件

脚本会在输出目录写入：

- `probe_result.json`：页面解析结果、字幕信息、候选音视频地址
- `audio.mp3`：匿名音频流下载后改名得到的文件
- `transcription_result.json`：硅基流动转写返回结果
- `transcript.txt`：最终可直接阅读的文字稿
- `.skill-ready.json`：表示这个输出目录至少成功跑通过一次

如果成功拿到文字稿，脚本结束时也会把 transcript 直接打印到 stdout，调用方不必再额外读取 `transcript.txt`。

## 回复规则

拿到文字之后：

- 如果用户要求完整转录，就输出完整文字或引用 `transcript.txt`。
- 如果用户要求重点分析某一部分，就只围绕该部分总结。
- 如果用户没有特别要求，默认给出重点总结。
- 需要说明文字来源是官方字幕还是 ASR。
- 如果字幕和 ASR 都不可用，就明确说明阻塞原因并停止。

## 说明

- 这个 skill 已验证可处理标准 B 站链接和 `b23.tv` 短链接。
- 在当前验证流程里，匿名下载得到的 `.m4s` 音频文件，直接改名为 `.mp3` 后即可用于硅基流动转写，无需转码。
- 匿名获取能力不是绝对稳定，部分视频仍可能因为 B 站限制而失败。
