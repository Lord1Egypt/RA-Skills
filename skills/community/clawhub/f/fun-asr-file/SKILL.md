---
name: fun-asr-file
description: "阿里云百炼 FunASR 本地音频文件识别（非流式），使用阿里云 DashScope API 进行语音转文字。针对本地音频文件优化，支持自动格式转换，适合批量文件转写场景。"
version: "1.1.0"
---

# Fun-ASR-File

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
pip install dashscope
# 如需自动格式转换，请安装 FFmpeg
```

### 转写音频文件

```bash
python scripts/cli.py audio.wav
# 支持 .wav / .mp3 / .m4a / .flac / .ogg 等格式
# 会自动转换为 API 要求的格式（16kHz, 单声道, pcm_s16le）
```

---

*版本：1.1.0*
*创建于：2026-03-16*
*更新：2026-04-09 - 改为非流式调用，优化本地文件处理*
