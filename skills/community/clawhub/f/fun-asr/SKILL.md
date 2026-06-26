---
name: fun-asr
description: "阿里云百炼 FunASR 录音文件识别，使用阿里云 DashScope API 进行语音转文字。当用户需要转录音频文件时触发。"
version: "1.0.0"
---

# Fun-ASR

Fun-ASR 是通义实验室百聆团队推出的端到端语音识别大模型，是基于数千万小时真实语音数据训练而成，具备强大的上下文理解能力与行业适应性。

## 激活条件

| 触发场景 | 说明 |
|----------|------|
| 用户发送音频文件 | `.wav` / `.mp3` / `.m4a` / `.flac` / `.ogg` 等格式 |
| 用户要求转录 | "转写音频"、"语音转文字" |
| 音频文件处理 | 需要提取音频中的文字内容 |

## 配置

设置环境变量：

```bash
export DASHSCOPE_API_KEY="sk-xxx"
```

## 使用方法

### 安装依赖

```bash
pip install dashscope librosa
```

### 转写音频文件

```bash
python scripts/cli.py audio.wav
```

---

*版本：1.0.0*
*创建于：2026-03-16*
