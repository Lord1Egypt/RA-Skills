---
name: feishu-voice-note-ffmpeg
description: "解决飞书 IM 语音气泡问题——通过 ffmpeg 将 TTS 输出的 mp3 转为飞书支持的 ogg-opus 格式。适用场景：(1) 在飞书机器人的 TTS 回复中需要显示语音气泡而非文件附件, (2) Edge TTS 或其他只支持 mp3/webm 输出的 TTS 引擎需要适配飞书, (3) 自定义 TTS provider 的飞书集成。包含核心原理、ffmpeg 命令、OpenClaw pipeline 集成方案。"
metadata: {"openclaw":{"homepage":"https://open.feishu.cn/document/ukTMukTMukTM/uAjLw4CM/ukTMukTMukTM/reference/im-v1/message/create_json"}}
---

# 飞书语音气泡 ffmpeg 方案

在飞书机器人中，语音消息只有以 `ogg-opus` 格式发送才会显示为可播放的语音气泡。
纯文本附件或其他格式会显示为文件附件，无法内联播放。

## 使用方式

适合在以下场景直接套用：

- TTS 已经能正常生成音频，但飞书里只显示为附件
- 希望把现有 mp3 / webm-opus 输出适配成飞书语音气泡
- 正在做 OpenClaw / 自定义机器人 / 自定义消息管线的飞书语音集成

## 核心原理

```
TTS 引擎（Edge TTS）
  → 输出 mp3（Edge TTS 原生仅支持 mp3 和 webm-opus）
    → ffmpeg 转码为 ogg-opus
      → 飞书 API 接收 ogg → 显示语音气泡 ✅
```

**为什么需要转码：**
- Edge TTS 仅支持 `audio-24khz-48kbitrate-mono-mp3`（mp3）和 `webm-opus` 格式
- 飞书官方只将 `ogg-opus` 识别为语音消息（`msg_type: audio`）
- webm 容器的 opus 文件飞书不识别，可能被当作视频或未知格式
- mp3 文件在飞书中只能作为文件附件发送

## 飞书官方推荐命令

```bash
ffmpeg -i input.mp3 -acodec libopus -ac 1 -ar 16000 output.opus
```

参数说明：
- `-acodec libopus` — 使用 Opus 编码器
- `-ac 1` — 单声道（语音消息标准）
- `-ar 16000` — 16kHz 采样率（语音质量与文件大小的平衡点）

## 在 OpenClaw 中的集成方案

### 方案概述

在 TTS provider 的 `synthesize` 函数中，检测当前通道是否要求语音气泡（通过 `target` 参数判断），如果是则：

1. 调用目标 TTS 引擎生成 mp3
2. 自动调用 ffmpeg 转成 ogg-opus
3. 返回 `.opus` 文件路径给消息发送管线
4. 飞书通道检测到 `fileType: "opus"` 后以 `msg_type: "audio"` 发送 → 语音气泡

### 关键集成点

```
TTS provider synthesize()
  → 生成 mp3 临时文件
  → 若 target === "voice-note"（飞书通道自动触发）:
    → ffmpeg -i temp.mp3 ... temp.opus
    → 返回 temp.opus 路径
  → 否则直接返回 mp3 路径
```

### 出错处理

- 如果 ffmpeg 转码失败（未安装、参数错误等），降级为返回原始 mp3 文件
- 降级后 mp3 会作为文件附件发送，不会导致崩溃

## 格式验证

转码后的 opus 文件可通过以下方式验证：

```bash
# 查看文件格式
ffprobe output.opus

# 确认编码器
ffprobe -show_streams output.opus | findstr codec

# 确认飞书兼容性
# 文件扩展名必须为 .opus
# MIME 类型应为 audio/opus 或 audio/ogg
```

## 实施建议

- 优先在 **TTS provider 输出后、消息发送前** 做转码
- 不建议把转码逻辑塞进上层业务逻辑；媒体格式适配应尽量留在音频管线内部
- 先保证失败可降级，再追求“始终发语音气泡”

## 已知限制

- ffmpeg 必须安装在系统 PATH 中
- 转码增加约 50-200ms 延迟（取决于音频时长）
- 临时文件需要及时清理，避免磁盘占用
- 更新 TTS provider 或消息通道组件后，集成代码可能需要重新应用
- 飞书 API 要求 opus 文件大小不超过一定限制（通常语音消息几秒内的文件无问题）
