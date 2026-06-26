---
name: fun-denoise
description: 智能音频降噪服务，基于阿里巴巴通义实验室 AI 算法，一键消除背景噪音，还原纯净人声。支持 wav、mp3、aac 等主流格式，适用于录音降噪、语音识别预处理、播客后期制作、会议录音优化等场景。当用户需要音频降噪、去除噪音、音频预处理、提升录音质量时使用。
---

# FunAudioDenoise 智能音频降噪

## 服务简介

FunAudioDenoise 是阿里云百炼平台提供的专业级音频降噪服务，采用深度学习算法精准分离人声与背景噪音，让您的录音更清晰、更专业。

### 核心优势

| 特性 | 说明 |
|------|------|
| **AI 智能降噪** | 基于通义实验室深度学习模型，精准识别人声，有效消除环境噪音 |
| **实时流式处理** | WebSocket 双向流式协议，支持边传边处理，响应迅速 |
| **多格式兼容** | 支持 wav、mp3、aac、opus、amr、pcm 等主流音频格式 |
| **大文件支持** | 单文件最大支持 2 小时或 1GB，满足长录音需求 |
| **质量评估** | 自动输出音频质量评分，帮助您了解录音状况 |

### 适用场景

- **会议录音** - 消除会议室回声、空调声、键盘声等干扰
- **播客制作** - 提升人声清晰度，打造专业音质
- **语音识别预处理** - 提高 ASR 识别准确率
- **在线教育** - 优化课程录音质量
- **采访录音** - 还原清晰的对话内容
- **有声书制作** - 打造沉浸式听书体验

## 快速开始

### 环境准备

```bash
pip install dashscope websocket-client
```
### 设置密钥（只需一次）

```bash
export DASHSCOPE_API_KEY="你的阿里云 API 密钥"
```

### 一行命令降噪

```bash
python denoise_cli.py input.mp3 output.wav
```

### Python API 调用

```python
from denoise_cli import denoise_audio

result = denoise_audio(
    input_path="noisy_recording.wav",
    output_path="clean_audio.wav"
)

if result["success"]:
    print(f"降噪完成！音频质量评分: {result['output_info']['voice_quality']}")
```

## 核心 API

### DenoiseParam 参数配置

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `model` | str | "fun-audio-denoising" | 模型名称（固定值） |
| `apikey` | str | None | DashScope API Key |
| `format` | str | "wav" | 音频格式：wav、mp3、aac、opus、amr、pcm |
| `sample_rate_in` | int | 16000 | 输入采样率（PCM 格式必填） |
| `sample_rate_out` | int | None | 输出采样率（默认同输入） |
| `enable_denoise` | bool | True | 是否启用降噪 |

### 处理结果元数据

```python
{
    "sample_rate_out": 48000,        # 输出采样率
    "voice_quality": "0.89",          # 音频质量评分 (0-1)
    "valid_speech_ms": "15000"        # 有效语音时长（毫秒）
}
```

## 使用示例

### 示例 1：命令行快速降噪

```bash
# 基础使用（自动推断格式）
python denoise_cli.py meeting_recording.mp3

# 指定输出文件
python denoise_cli.py interview.wav clean_interview.wav

# 自定义参数
python denoise_cli.py podcast.mp3 --format mp3 --sample-rate 48000
```

### 示例 2：Python 脚本集成

```python
import dashscope
from audio_process import Denoise, DenoiseParam, ResultCallback, DenoiseResult
import threading

# 设置 API Key
dashscope.api_key = "your-api-key"

class MyCallback(ResultCallback):
    def __init__(self):
        self.audio_data = b""
        self.complete_event = threading.Event()
    
    def on_event(self, result: DenoiseResult):
        if result.audio_frame:
            self.audio_data += result.audio_frame
    
    def on_complete(self):
        print("处理完成！")
        self.complete_event.set()

# 配置参数
param = DenoiseParam(
    format="wav",
    sample_rate_in=16000,
    enable_denoise=True
)

# 执行降噪
callback = MyCallback()
denoise = Denoise(param=param, callback=callback)
denoise.start_task()

# 发送音频数据
with open("input.wav", "rb") as f:
    while chunk := f.read(3200):
        denoise.send_audio_frame(chunk)

denoise.sync_stop_task()

# 保存结果
with open("output.wav", "wb") as f:
    f.write(callback.audio_data)
```

### 示例 3：批量处理多个文件

```python
from denoise_cli import denoise_audio
import os

input_dir = "raw_recordings/"
output_dir = "clean_recordings/"
os.makedirs(output_dir, exist_ok=True)

for filename in os.listdir(input_dir):
    if filename.endswith(".wav"):
        input_path = os.path.join(input_dir, filename)
        output_path = os.path.join(output_dir, f"clean_{filename}")
        
        result = denoise_audio(input_path, output_path, verbose=False)
        
        if result["success"]:
            quality = result["output_info"].get("voice_quality", "N/A")
            print(f"✓ {filename} - 质量评分: {quality}")
        else:
            print(f"✗ {filename} - 失败: {result['error']}")
```

## 最佳实践

### 1. 音频分帧策略

- **推荐帧大小**：3200 字节（对应 16000Hz 采样率下 100ms 音频）
- **发送间隔**：配合音频时长，模拟实时流（100ms 数据间隔 100ms 发送）
- **大文件处理**：分块读取，避免内存溢出

### 2. 采样率选择

| 场景 | 推荐采样率 | 说明 |
|------|------------|------|
| 语音识别 | 16000Hz | 平衡质量与处理速度 |
| 电话录音 | 8000Hz | 兼容传统电话系统 |
| 音乐/播客 | 44100Hz/48000Hz | 高保真音质 |

### 3. 质量评估解读

- `voice_quality` > 0.8：音频质量优秀
- `voice_quality` 0.5-0.8：音频质量良好，轻度噪音
- `voice_quality` < 0.5：音频质量较差，噪音较多

### 4. 异常处理建议

```python
try:
    denoise.start_task()
    # ... 发送音频数据
    denoise.sync_stop_task(timeout=120000)
except TimeoutError:
    print("处理超时，请检查网络连接")
except Exception as e:
    print(f"处理失败: {e}")
finally:
    denoise.close()  # 确保资源释放
```

## 命令行工具详解

```
usage: denoise_cli.py [-h] [--api-key API_KEY] [--format FORMAT]
                      [--sample-rate SAMPLE_RATE] [--no-denoise]
                      [--chunk-size CHUNK_SIZE] [--chunk-delay CHUNK_DELAY]
                      [-q]
                      input [output]

positional arguments:
  input                 输入音频文件路径
  output                输出音频文件路径（可选）

optional arguments:
  -h, --help            显示帮助信息
  --api-key API_KEY     DashScope API Key
  --format FORMAT       音频格式 (wav, mp3, pcm, aac, opus, amr)
  --sample-rate SAMPLE_RATE
                        采样率 (默认: 16000)
  --no-denoise          禁用降噪（仅转换格式）
  --chunk-size CHUNK_SIZE
                        分块大小（默认: 3200）
  --chunk-delay CHUNK_DELAY
                        分块发送间隔（默认: 0.1秒）
  -q, --quiet           静默模式
```

## 技术规格

| 项目 | 规格 |
|------|------|
| 支持格式 | wav、mp3、aac、opus、amr、pcm |
| 最大时长 | 2 小时 |
| 最大文件 | 1 GB |
| 输出采样率 | 自动优化（默认 48kHz） |
| 协议 | WebSocket 双向流式 |
| 延迟 | < 200ms（首包响应） |

## 相关资源
- [Denoise.py 源码](audio_process/Denoise.py) - SDK 实现源码

---

*FunAudioDenoise - 让每一句声音都清晰可闻*
