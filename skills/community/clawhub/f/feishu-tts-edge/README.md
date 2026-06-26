# Feishu Voice Sender

飞书语音消息发送工具。基于 Edge TTS，一键发送语音到飞书。

## 安装

```bash
pip install edge-tts
sudo apt-get install ffmpeg
```

## 使用

```bash
cd scripts
python3 voice_sender.py "要发送的文字" [语音]
```

## 语音选项

| 语音 | 性别 | 风格 |
|:---|:---:|:---|
| **xiaoxiao** | 女 | 温暖专业 ⭐默认 |
| **yunyang** | 男 | 专业可靠 |
| yunxi | 男 | 活泼阳光 |
| xiaoyi | 女 | 活泼卡通 |
| yunjian | 男 | 新闻播报 |
| xiaobei | 女 | 辽宁话 |

## 示例

```bash
# 默认语音（xiaoxiao 温暖女声）
python3 voice_sender.py "你好老大，任务已完成"

# 指定语音
python3 voice_sender.py "系统告警，请立即处理" yunyang
```

## 依赖

- Python 3.8+
- edge-tts
- FFmpeg
