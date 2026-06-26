---
name: faster-whisper-zh
description: 使用 faster-whisper 的本地语音转文字工具。支持 GPU 加速的高性能转录，包含词级时间戳和蒸馏模型。当用户要求"转录音频"、"语音转文字"或"whisper"时使用此技能。
metadata:
  {
    "openclaw":
      {
        "requires":
          {
            "bins": ["ffmpeg", "python3"],
            "pip": ["faster-whisper", "torch"],
          },
      },
  }
---

# Faster-Whisper 中文版

基于 faster-whisper 的高性能本地语音转文字工具。

## 安装设置

### 1. 运行安装脚本
执行安装脚本以创建虚拟环境并安装依赖包。脚本会自动检测 NVIDIA GPU 以启用 CUDA 加速。

```bash
./setup.sh
```

系统要求：
- Python 3.10 或更高版本
- ffmpeg（系统已安装）

## 使用方法

使用转换脚本转换音频文件。

## 适用场景
- 会议录音转文字纪要
- 语音笔记转文字记录
- 音频文件内容提取
- 访谈录音整理
- 培训录音转文字材料
- 视频字幕生成
- 播客内容转录
- 语音转文字
- 音频转文字

### 基本转录
```bash
export HF_HOME=/config/huggingface
export HF_ENDPOINT=https://hf-mirror.com
.venv/bin/python3 scripts/transcribe.py
```

### 高级选项
- **指定模型**: `.venv/bin/python3 scripts/transcribe.py audio.mp3 --model large-v3-turbo`
- **词级时间戳**: `.venv/bin/python3 scripts/transcribe.py audio.mp3 --word-timestamps`
- **JSON 输出**: `.venv/bin/python3 scripts/transcribe.py audio.mp3 --json`
- **语音活动检测（静音去除）**: `.venv/bin/python3 scripts/transcribe.py audio.mp3 --vad`
- **指定语言**: `.venv/bin/python3 scripts/transcribe.py audio.mp3 --language zh`
- **GPU 加速**: `.venv/bin/python3 scripts/transcribe.py audio.mp3 --device cuda`
- **CPU 优化**: `.venv/bin/python3 scripts/transcribe.py audio.mp3 --device cpu --compute-type int8`

### 完整命令示例

```bash
# 中文转录，使用 GPU 加速
.venv/bin/python3 scripts/transcribe.py 会议录音.mp3 --language zh --device cuda --compute-type float16

# 英文转录，包含词级时间戳
.venv/bin/python3 scripts/transcribe.py interview.wav --language en --word-timestamps --json

# 快速 CPU 转录，优化性能
.venv/bin/python3 scripts/transcribe.py audio.m4a --device cpu --compute-type int8 --model distil-large-v3

# 批量处理脚本
.venv/bin/python3 scripts/batch_transcribe.sh /path/to/audio/files/
```

## 可用模型

- `large-v3-turbo` (默认):推荐用于多语言或最高准确度任务
- `large-v3`: 原始大模型，准确度最高
- `distil-large-v3`: 速度和准确性的最佳平衡
- `medium`: 中等大小，平衡性能
- `small`: 小型模型，速度快
- `base`: 基础模型，资源需求最低
- `tiny`: 微型模型，速度最快
- `medium.en`, `small.en`: 仅支持英语的更快版本

## 模型选择指南

| 模型 | 大小 | 推荐用途 | 硬件要求 |
|------|------|----------|----------|
| `large-v3-turbo` | 1.5GB | 专业级转录 | 高性能 GPU |
| `medium` | 1.5GB | 平衡性能 | 普通配置 |
| `distil-large-v3` | 756MB | 通用中文转录 | 中等配置 |
| `small` | 500MB | 快速转录 | 低配置 |
| `tiny` | 150MB | 实时转录 | 最低配置 |

## 性能优化

### GPU 加速配置
```bash
# NVIDIA GPU (CUDA)
.venv/bin/python3 scripts/transcribe.py audio.mp3 --device cuda --compute-type float16

# Apple Silicon (macOS)
.venv/bin/python3 scripts/transcribe.py audio.mp3 --device mps
```

### CPU 优化配置
```bash
# 高性能 CPU
.venv/bin/python3 scripts/transcribe.py audio.mp3 --device cpu --compute-type int8 --beam-size 3

# 低资源环境
.venv/bin/python3 scripts/transcribe.py audio.mp3 --device cpu --compute-type int8 --model small --beam-size 1
```

## 故障排除

### 常见问题

- **未检测到 GPU**: 确保 NVIDIA 驱动和 CUDA 正确安装。CPU 转录速度会显著变慢。
- **内存不足错误**: 使用更小的模型（如 `small` 或 `base`）或使用 `--compute-type int8`
- **模型下载失败**: 设置环境变量 `HF_ENDPOINT=https://hf-mirror.com` 使用国内镜像
- **音频格式不支持**: 使用 ffmpeg 转换音频格式：`ffmpeg -i input.m4a output.wav`

### 错误解决方案

1. **CUDA 不可用**
   ```bash
   # 检查 CUDA 安装
   nvidia-smi
   
   # 如果未安装，重新运行安装脚本
   ./setup.sh
   ```

2. **ffmpeg 未找到**
   ```bash
   # Ubuntu/Debian
   sudo apt install ffmpeg
   
   # macOS
   brew install ffmpeg
   
   # CentOS/RHEL
   sudo yum install ffmpeg
   ```

3. **Python 版本过低**
   ```bash
   # 检查 Python 版本
   python3 --version
   
   # 需要 Python 3.10+
   ```

## 环境变量配置

```bash
# 设置 HuggingFace 缓存目录（避免重复下载）
export HF_HOME=/config/huggingface

# 使用国内镜像加速下载
export HF_ENDPOINT=https://hf-mirror.com

# 设置 PyTorch CUDA 版本（如有需要）
export CUDA_VISIBLE_DEVICES=0
```

## 批量处理

创建 `batch_transcribe.sh` 脚本进行批量处理：

```bash
#!/bin/bash
# 批量转录脚本
for audio_file in *.mp3 *.wav *.m4a; do
    if [ -f "$audio_file" ]; then
        echo "处理: $audio_file"
        ./scripts/transcribe.py "$audio_file" --output "${audio_file%.*}.txt"
    fi
done
```

## 输出格式

### 纯文本输出
```
[00:00:00.000 --> 00:00:05.000] 欢迎使用 faster-whisper 语音转文字工具。
[00:00:05.000 --> 00:00:10.000] 这是一个高性能的本地转录解决方案。
```

### JSON 输出
```json
{
  "text": "完整的转录文本...",
  "segments": [
    {
      "start": 0.0,
      "end": 5.0,
      "text": "欢迎使用 faster-whisper 语音转文字工具。",
      "words": [
        {"word": "欢迎", "start": 0.0, "end": 0.5},
        {"word": "使用", "start": 0.5, "end": 1.0}
      ]
    }
  ]
}
```

## 更新日志

### v1.0.5 (2026-04-16)
- 重新调整命令
- 原需激活虚拟环境更改为直接执行虚拟环境的python3

## 技术支持

如有问题，请：
1. 查看本文档的故障排除部分
2. 检查系统要求是否满足
3. 确保网络连接正常（模型下载需要网络）
4. 查看脚本错误信息进行调试

---

**提示**: 首次运行会下载所选模型（large-v3-turbo 约 1.5GB）。请确保有足够的磁盘空间和稳定的网络连接。