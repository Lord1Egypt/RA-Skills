> **V7 兼容性说明**：本文件从 V6 完整继承。V7 保留所有 V6 能力，本文件内容完全有效。
> V7 新增 references 见 `references/edge-cloud-architecture.md` / `references/zero-upload-privacy.md` / `references/npu-scheduling-guide.md` / `references/edge-cloud-protocol.md` / `references/audit-report-v7.md`。
> 原始文件版本：V6 · 继承版本：V7 · 继承日期：2026-08-15

# 本地 ASR 集成指南（V6）

## 概述
本指南说明如何将 OpenVINO 优化的语音识别（ASR）能力集成到 AI 通识课教学系统中，实现课堂录音转写、语音答题、口语评测等教学生产力场景。

## 技术选型

### 推荐模型
| 模型 | 用途 | OpenVINO 优化 | 模型大小 | 实时率 |
|------|------|--------------|---------|--------|
| Whisper-small | 通用语音识别 | FP16 推理 | ~460MB | 0.3x (GPU) |
| Whisper-tiny | 轻量语音识别 | INT8 量化 | ~75MB | 0.1x (GPU) |
| FunASR Paraformer | 中文语音识别 | INT8 量化 | ~200MB | 0.2x (GPU) |
| SenseVoice-Small | 多语言+情感识别 | FP16 | ~230MB | 0.25x (GPU) |

### 硬件加速策略
- **GPU**：主力推理设备，处理 Whisper/FunASR 模型
- **NPU**：运行 VAD（语音活动检测）模型，低功耗持续监听
- **CPU**：音频预处理（重采样、降噪）和文本后处理

## 部署架构

### Client/Server 模式
```python
# asr_service.py — 本地 ASR 微服务
from fastapi import FastAPI, UploadFile, WebSocket
from openvino.runtime import Core
import whisper
import numpy as np

app = FastAPI(title="AI通识课 ASR 服务", version="6.0.0")

# OpenVINO 推理引擎
ie = Core()
whisper_model = ie.compile_model(
    model="models/whisper-small-fp16.xml",
    device_name="GPU"
)

@app.post("/api/v1/asr/transcribe")
async def transcribe_audio(file: UploadFile):
    """音频文件转文字 — 课堂录音→结构化文本"""
    audio_data = await file.read()
    result = whisper_transcribe(audio_data, whisper_model)
    return {
        "status": "success",
        "data": {
            "text": result["text"],
            "segments": result["segments"],  # 带时间戳的段落
            "language": result["language"],
            "word_timestamps": result["word_timestamps"]
        },
        "ai_tool": "asr",
        "hardware": {"gpu": True, "npu": False},
        "inference_time_ms": result["time_ms"]
    }

@app.websocket("/api/v1/asr/stream")
async def stream_transcribe(websocket: WebSocket):
    """实时流式语音识别 — 课堂实时转写"""
    await websocket.accept()
    audio_buffer = []
    while True:
        chunk = await websocket.receive_bytes()
        audio_buffer.append(chunk)
        if len(audio_buffer) >= 5:  # 每 5 个 chunk 推理一次
            result = whisper_transcribe_stream(audio_buffer, whisper_model)
            await websocket.send_json(result)
            audio_buffer = []

@app.post("/api/v1/asr/evaluate")
async def evaluate_pronunciation(file: UploadFile, reference_text: str):
    """口语评测 — 学生发音→评分+纠错"""
    audio_data = await file.read()
    result = pronunciation_evaluate(audio_data, reference_text)
    return {
        "status": "success",
        "data": {
            "score": result["score"],  # 0-100
            "errors": result["errors"],  # 发音错误列表
            "fluency": result["fluency"],  # 流利度
            "accuracy": result["accuracy"]  # 准确度
        }
    }
```

### 启动服务
```bash
uvicorn asr_service:app --host 127.0.0.1 --port 8902
```

## 教学场景集成

### 场景一：语音答题（能力四增强）
```javascript
// 学生通过语音回答问题
async function voiceAnswer(audioBlob, question) {
    const formData = new FormData();
    formData.append('file', audioBlob);
    
    const response = await fetch('http://127.0.0.1:8902/api/v1/asr/transcribe', {
        method: 'POST',
        body: formData
    });
    
    const result = await response.json();
    const studentAnswer = result.data.text;
    
    // 将语音识别结果与标准答案对比
    return evaluateAnswer(studentAnswer, question.expectedAnswer);
}
```

### 场景二：课堂录音自动转写
```javascript
// 实时转写课堂内容
const ws = new WebSocket('ws://127.0.0.1:8902/api/v1/asr/stream');
ws.onmessage = (event) => {
    const data = JSON.parse(event.data);
    displayRealtimeTranscript(data.text);
};

// 录音并发送
navigator.mediaDevices.getUserMedia({ audio: true }).then(stream => {
    const recorder = new MediaRecorder(stream);
    recorder.ondataavailable = (e) => ws.send(e.data);
    recorder.start(1000); // 每秒发送一次
});
```

## OpenVINO 优化步骤

### 1. 模型转换
```bash
# Whisper → OpenVINO IR
optimum-cli export openvino --model openai/whisper-small --task automatic-speech-recognition --weight-format fp16 models/whisper-small-fp16
# INT8 量化
optimum-cli export openvino --model openai/whisper-small --task automatic-speech-recognition --weight-format int8 models/whisper-small-int8
```

### 2. VAD 模型部署到 NPU
```python
# Silero VAD — 部署到 NPU 实现低功耗语音检测
vad_model = ie.compile_model(
    model="models/silero_vad.xml",
    device_name="NPU"  # NPU 低功耗持续运行
)
```

### 3. 性能验证
| 指标 | 目标值 | 测试方法 |
|------|--------|---------|
| 实时率 (RTF) | <0.5 (GPU) | 1 小时课堂录音 |
| 词错误率 (WER) | ≤15% | 教学场景测试集 |
| 中文识别准确率 | ≥90% | 普通话教学录音 |
| 首字延迟 | <500ms | 流式推理测试 |

## 错误降级
| 场景 | 降级方案 |
|------|---------|
| GPU 不可用 | 降级为 CPU 推理（RTF 增加 3-5x） |
| ASR 服务崩溃 | 降级为键盘输入答题 |
| 模型加载失败 | 降级为浏览器原生 Web Speech API |
| 识别置信度低 | 标记「待确认」并提供候选文本 |

## 质量门控
- [ ] WER ≤15%（普通话教学场景）
- [ ] 实时率 <0.5（GPU 推理）
- [ ] 流式首字延迟 <500ms
- [ ] 支持中文+英文混合识别
- [ ] 内存峰值 <1GB
- [ ] 口语评测评分与人工评分相关性 ≥0.85
