---
name: feishu-edge-tts-win
description: 飞书语音消息发送技能（Windows 版）。使用 Edge TTS（微软，免费）生成语音并以飞书语音气泡发送。
---

# 飞书语音消息发送（Windows）

## 快速使用

在 `skills\feishu-edge-tts-win\scripts` 目录执行：

```bash
python .\send_voice.py "要发送的文本" YOUR_FEISHU_OPEN_ID --voice zh-CN-XiaoxiaoNeural --config %USERPROFILE%\.openclaw\openclaw.json
```

也可以从任意目录执行：

```bash
python %USERPROFILE%\.openclaw\workspace\skills\feishu-edge-tts-win\scripts\send_voice.py "要发送的文本" YOUR_FEISHU_OPEN_ID --voice zh-CN-XiaoxiaoNeural --config %USERPROFILE%\.openclaw\openclaw.json
```

## 工作流程

1. `edge-tts` 生成 MP3
2. `ffmpeg` 转换为 OPUS（飞书语音格式）
3. 飞书 API 上传 OPUS 获取 `file_key`
4. 发送 `msg_type=audio` 消息

关键点：必须使用 `msg_type: audio` + `file_key`，否则会显示为普通文件而不是语音气泡。

## 音色

仅使用：`zh-CN-XiaoxiaoNeural`

## 依赖安装

```bash
pip install edge-tts
```

`ffmpeg` 需要可执行（已加入 PATH）。可用 `ffmpeg -version` 自检。

## 飞书配置

脚本读取 `openclaw.json` 的 `channels.feishu.appId` 和 `channels.feishu.appSecret`。
请在命令中显式传入 `--config`，例如：

```bash
--config %USERPROFILE%\.openclaw\openclaw.json
```
