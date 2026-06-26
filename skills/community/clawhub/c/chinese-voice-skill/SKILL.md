---
name: Chinese Voice Skill
description: 使用微软 Edge TTS 生成高质量中文语音，默认使用 XiaoxiaoNeural 语音。当用户需要语音回复时自动触发。
read_when:
  - 生成中文语音
  - 创建语音回复
  - 使用 TTS 合成语音
  - 需要语音回复
  - 中文语音对话
  - edge-tts 语音生成
  - 语音对话
  - TTS 转换
  - 发送语音
  - 语音合成
  - 开启语音
  - 开始语音
  - 用语音回复
metadata: {"clawdbot":{"emoji":"🎤","priority":10,"requires":{"bins":["python","pip"]}}}
allowed-tools: Bash(edge-tts:*)
---

# Edge TTS 中文语音合成技能

## 概述

使用微软 Edge TTS 生成高质量中文语音，默认使用 XiaoxiaoNeural 语音。当用户需要语音回复时自动触发。

## 能力

- **语音合成**: 将文本转换为高质量的中文语音
- **默认语音**: zh-CN-XiaoxiaoNeural（甜美自然的中文语音）
- **备用方案**: 当 edge-tts 不可用时，自动降级到系统自带的 System.Speech
- **平台支持**:
  - ✅ QQ 发送（<qqmedia> wav 格式）

## 使用方式

### 基本用法

当用户表达需要语音回复时（如"生成语音"、"用语音告诉我"、"用语音说"），系统会自动：

1. 检测 edge-tts 是否可用
2. 使用 Edge TTS + XiaoxiaoNeural 生成语音
3. 发送 `<qqmedia>输出文件.wav</qqmedia>`

### 前置条件

1. **Python 3.7+** 已安装（用于运行 edge-tts）
2. **pip** 可用
3. **QQ 通道** 已配置（用于发送 wav 格式语音）

## 配置选项

### 语音选择

- 默认: `zh-CN-XiaoxiaoNeural`
- 其他可选微软语音:
  - `zh-CN-YunxiNeural`（沉稳）
  - `zh-CN-XiaoyiNeural`（温柔）
  - `zh-CN-YunyangNeural`（磁性）

### 语音参数

- `Rate`: 语速（默认 0，可调整 -5 到 5）
- `Volume`: 音量（默认 1.0，范围 0 到 1）

## 技术实现

### 命令行调用

使用 Python 的 edge_tts 模块：

```bash
python -m edge_tts --voice "zh-CN-XiaoxiaoNeural" --text "要转换的文本" --write-media "输出文件.wav"
```

### 安装 edge-tts

如果未安装，使用 pip 安装：

```bash
pip install --user edge-tts -i https://mirrors.aliyun.com/pypi/simple/
```

### 备用语音方案

如果 edge-tts 不可用，系统会自动使用系统自带的中文 TTS。

## 输出格式

- **文件格式**: WAV（微软 TTS 标准格式）
- **采样率**: 24000 Hz
- **声道**: 单声道
- **位深度**: 16-bit

## 注意事项

1. **网络要求**: edge-tts 需要访问微软服务器
2. **文件大小**: 生成的语音文件通常在 50-200 KB
3. **自动清理**: 临时文件可能由系统自动清理
4. **备用方案**: 当 edge-tts 不可用时自动降级，不影响基本功能

## 示例

```
用户: 生成语音，"你好！这是一段测试文本。"

AI: [调用 edge-tts 生成语音]
[发送 <qqmedia>C:\Users\ADMINI~1\AppData\Local\Temp\xxx.wav</qqmedia>]
[提示语音生成完成]
```

## 故障排除

### edge-tts 未安装

使用 pip 安装 edge-tts：

```bash
pip install --user edge-tts -i https://mirrors.aliyun.com/pypi/simple/
```

### edge-tts 路径问题

检查 edge-tts 是否在 PATH 中：

```powershell
Get-Command edge-tts.exe -ErrorAction SilentlyContinue
```

### 语音未生成

1. 检查网络连接
2. 查看错误信息
3. 确认 QQ 通道已配置
4. 确认 ffmpeg 已安装（如需转换格式）
