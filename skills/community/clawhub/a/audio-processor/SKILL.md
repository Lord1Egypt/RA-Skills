---
name: audio-processor
description: "音频处理工具集 - 支持音频录制、剪辑、格式转换、频谱分析、降噪、变速变调等操作。Use when: (1) 需要处理音频文件（录音、剪辑、合并、分割）, (2) 需要转换音频格式（MP3/WAV/FLAC/OGG等）, (3) 需要分析音频特征（频谱、音量、静音检测）, (4) 需要对音频进行效果处理（降噪、变速、变调、混响）, (5) 需要提取或生成音频元数据"
---

# Audio Processor

音频处理全能工具集，基于 Python + ffmpeg + librosa/pydub 实现。

## 核心能力

### 1. 音频格式转换
- 支持 MP3 / WAV / FLAC / OGG / AAC / M4A 互转
- 批量转换目录内音频
- 自定义比特率、采样率、声道数

### 2. 音频剪辑与合并
- 按时间码裁剪（hh:mm:ss 格式）
- 去除首尾静音段
- 多段音频合并拼接
- 淡入淡出效果

### 3. 音频分析
- 波形可视化（matplotlib）
- 频谱分析（FFT +  spectrogram）
- 音量检测（RMS / dBFS）
- BPM / 节奏检测
- 静音段检测与分割

### 4. 音频效果处理
- 降噪（spectral gating）
- 变速不变调 / 变调不变速
- 音量标准化（peak / RMS / LUFS）
- 混响、延迟效果

### 5. 音频信息提取
- 时长、采样率、比特率、声道数
- ID3 标签 / 元数据读写
- 音频指纹生成

## 快速开始

```bash
# 格式转换
python3 scripts/convert_format.py input.wav output.mp3 --bitrate 320k

# 剪辑音频（从30秒到2分钟）
python3 scripts/cut_audio.py input.mp3 output.mp3 --start 00:00:30 --end 00:02:00

# 分析音频特征
python3 scripts/analyze_audio.py input.mp3 --output report.json

# 降噪处理
python3 scripts/denoise.py input.mp3 output.mp3

# 批量处理目录
python3 scripts/batch_process.py ./audio_dir/ --action convert --format mp3
```

## 依赖安装

```bash
pip install -r requirements.txt
```

核心依赖：ffmpeg（系统级）、pydub、librosa、soundfile、mutagen、numpy、matplotlib、noisereduce

## 脚本说明

| 脚本 | 功能 |
|------|------|
| `convert_format.py` | 格式转换，支持所有主流格式 |
| `cut_audio.py` | 按时间码裁剪音频 |
| `merge_audio.py` | 多文件合并拼接 |
| `analyze_audio.py` | 音频特征分析（波形/频谱/BPM） |
| `denoise.py` | 降噪处理 |
| `speed_pitch.py` | 变速变调 |
| `normalize_volume.py` | 音量标准化 |
| `batch_process.py` | 批量处理目录 |
| `extract_metadata.py` | 元数据提取与编辑 |
| `detect_silence.py` | 静音检测与自动分割 |

## 详细用法

参见 `references/` 目录：
- `audio-formats.md` - 支持的音频格式详解
- `effects-guide.md` - 效果处理参数指南
- `api-reference.md` - 脚本 API 参考
