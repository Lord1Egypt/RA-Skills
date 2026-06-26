# 飞书语音消息发送技能

根据当前 channel 自动选择语音发送方式。

## 功能

- 自动检测当前 channel 类型
- 飞书频道：使用小米 MiMo TTS 生成语音并发送飞书原生语音消息
- 其他频道：使用文字消息或相应格式

## 安装

```bash
clawhub install feishu-voice-sender
```

## 使用

```bash
# 发送语音消息
python3 feishu_voice_sender.py "你好，世界！"

# 指定 channel
python3 feishu_voice_sender.py "你好，世界！" feishu
```

## 依赖

- 小米 MiMo TTS 技能
- ffmpeg
- MIMO_API_KEY