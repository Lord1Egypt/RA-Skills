---
name: feishu-voice-sender
description: |
  飞书语音消息发送器。基于 Edge TTS，一键将文字转为语音发送到飞书。
  
  使用场景：
  - 发送语音通知/提醒到飞书
  - 文字转语音自动播报
  
  触发词：飞书语音、语音发送、tts、文字转语音
---

# Feishu Voice Sender - 飞书语音发送器

极简版 Edge TTS 语音发送工具，一键生成并发送到飞书。

## 特性

- 🎙️ **单一供应商**：Edge TTS（免费高质量）
- 🎭 **多语音选择**：xiaoxiao、yunyang、yunxi 等
- 🔄 **自动格式转换**：自动转为飞书 OPUS 格式
- 📱 **一键发送**：生成后直接发送到飞书

## 安装依赖

```bash
pip install edge-tts
sudo apt-get install ffmpeg
```

## 快速开始

```bash
cd ~/.openclaw/skills/feishu-voice-sender/scripts

# 默认语音（xiaoxiao 温暖女声）
python3 voice_sender.py "你好老大，任务已完成"

# 指定语音
python3 voice_sender.py "系统告警" yunyang
```

## 语音列表

| 语音 | 性别 | 风格 | 推荐场景 |
|:---|:---:|:---|:---|
| **xiaoxiao** | 女 | 温暖、专业 | ⭐ 日常工作 |
| **yunyang** | 男 | 专业、可靠 | 正式通知 |
| **yunxi** | 男 | 活泼、阳光 | 轻松内容 |
| **xiaoyi** | 女 | 活泼、卡通 | 趣味内容 |
| **yunjian** | 男 | 新闻播报 | 紧急通知 |
| **xiaobei** | 女 | 辽宁话 | 幽默方言 |

## 使用示例

```bash
# 日常汇报
python3 voice_sender.py "老大，今日数据已更新"

# 紧急通知
python3 voice_sender.py "系统告警，服务器异常" yunjian
```

## 文件结构

```
feishu-voice-sender/
├── SKILL.md
└── scripts/
    └── voice_sender.py   # 极简版，单文件
```

---

*极简 Edge TTS 飞书语音发送器*
