---
name: feishu-voice
description: 飞书语音消息发送技能。使用 Edge TTS（微软，免费无限次）生成语音并以飞书语音气泡形式发送。当用户要求用语音回复、发语音消息、TTS 朗读内容时触发。默认音色：云希（zh-CN-YunxiNeural，活泼阳光男声）。
---

# 飞书语音消息发送

## 快速使用

```bash
python3 ~/.openclaw/workspace/skills/feishu-voice/scripts/send_voice.py \
  "要说的内容" \
  <open_id>
```

## 工作流程

1. edge-tts 生成 mp3
2. ffmpeg 转换为 opus（飞书语音格式）
3. 飞书 API 上传文件获取 file_key（file_type=opus）
4. 发送 msg_type=audio 消息

**关键**：必须用 `msg_type: audio` + `file_key`，不能用普通文件上传，否则显示为文件而非语音气泡。

## 音色选择

```bash
# 查看所有中文音色
edge-tts --list-voices | grep zh-CN

# 常用中文男声
zh-CN-YunxiNeural    # 云希 - 活泼阳光（默认，小龙虾专用）
zh-CN-YunjianNeural  # 云间 - 激情澎湃
zh-CN-YunxiaNeural   # 云夏 - 可爱萌
zh-CN-YunyangNeural  # 云扬 - 专业严肃

# 常用中文女声
zh-CN-XiaoxiaoNeural # 小小 - 温柔
zh-CN-XiaoyiNeural   # 小艺 - 活泼

# 指定音色发送
python3 ~/.openclaw/workspace/skills/feishu-voice/scripts/send_voice.py \
  "内容" <open_id> --voice zh-CN-YunyangNeural
```

## 依赖安装

```bash
pip install edge-tts  # 一次性安装，永久免费
# ffmpeg 通常已预装，如没有：yum install ffmpeg / apt install ffmpeg
```

## 飞书配置

需要 openclaw.json 中的 feishu appId / appSecret，脚本自动读取。
