---
name: feishu-asr
description: 使用本地Whisper模型识别飞书语音消息。离线免费，不需要注册，不需要联网。
---

# 飞书语音识别 ASR

## 触发条件

- 用户发送飞书语音消息
- 用户要求将语音转为文字
- 用户提到"语音识别"、"转文字"

## 工作流程

### 1. 获取语音文件

从飞书消息中获取语音文件的file_key，下载为.ogg或.m4a格式。

### 2. 音频格式转换

使用Python soundfile将音频转换为16kHz采样的WAV格式：

```python
import soundfile as sf
audio, sr = sf.read(voice_file)
# 如果是立体声，转为单声道
if len(audio.shape) > 1:
    audio = audio.mean(axis=1)
sf.write('output.wav', audio, 16000)
```

### 3. 使用Whisper识别

```python
import os
os.environ['HF_ENDPOINT'] = 'https://hf-mirror.com'  # 国内镜像

from transformers import WhisperForConditionalGeneration, WhisperProcessor, WhisperFeatureExtractor
import soundfile as sf

# 读取音频
audio, sr = sf.read('output.wav')
if len(audio.shape) > 1:
    audio = audio.mean(axis=1)

# 加载模型
processor = WhisperProcessor.from_pretrained('openai/whisper-tiny')
model = WhisperForConditionalGeneration.from_pretrained('openai/whisper-tiny')
feature_extractor = WhisperFeatureExtractor.from_pretrained('openai/whisper-tiny')

# 识别
input_features = feature_extractor(audio, sampling_rate=16000, return_tensors='pt').input_features
with torch.no_grad():
    predicted_ids = model.generate(input_features)

result = processor.batch_decode(predicted_ids, skip_special_tokens=True)[0]
```

## 依赖安装

```bash
pip install torch transformers soundfile
```

## 模型选择

- **whisper-tiny**: 75MB，适合CPU，最快
- **whisper-base**: 142MB，精度更好
- **whisper-small**: 466MB，精度高

## 注意事项

- 首次运行需要下载模型（约75MB-3GB）
- 建议使用国内镜像：HF_ENDPOINT=https://hf-mirror.com
- 模型会自动检测语言
