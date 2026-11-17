> **V7 兼容性说明**：本文件从 V6 完整继承。V7 保留所有 V6 能力，本文件内容完全有效。
> V7 新增 references 见 `references/edge-cloud-architecture.md` / `references/zero-upload-privacy.md` / `references/npu-scheduling-guide.md` / `references/edge-cloud-protocol.md` / `references/audit-report-v7.md`。
> 原始文件版本：V6 · 继承版本：V7 · 继承日期：2026-08-15

# 本地 TTS 集成指南（V6）

## 概述
本指南说明如何将 OpenVINO 优化的语音合成（TTS）能力集成到 AI 通识课教学系统中，实现课文朗读、游戏配音、多语言教学、语音故事等教学生产力场景。

## 技术选型

### 推荐模型
| 模型 | 用途 | OpenVINO 优化 | 模型大小 | 合成速度 |
|------|------|--------------|---------|---------|
| Edge-TTS | 高质量多语言 TTS | 云端 API 备选 | - | 实时 |
| PaddleSpeech FastSpeech2 | 中文语音合成 | INT8 量化 | ~80MB | 5x 实时 (GPU) |
| VITS | 端到端语音合成 | FP16 | ~120MB | 3x 实时 (GPU) |
| CosyVoice | 零样本语音克隆 | FP16 | ~200MB | 2x 实时 (GPU) |

### 硬件加速策略
- **GPU**：主力声学模型推理
- **CPU**：声码器（Vocoder）推理 + 音频后处理
- **NPU**：韵律预测模型（低功耗）

## 部署架构

### Client/Server 模式
```python
# tts_service.py — 本地 TTS 微服务
from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from openvino.runtime import Core
import numpy as np

app = FastAPI(title="AI通识课 TTS 服务", version="6.0.0")

ie = Core()
tts_model = ie.compile_model(
    model="models/fastspeech2_fp16.xml",
    device_name="GPU"
)
vocoder = ie.compile_model(
    model="models/hifigan_fp16.xml",
    device_name="CPU"  # 声码器放 CPU
)

@app.post("/api/v1/tts/synthesize")
async def synthesize_speech(text: str, speaker: str = "default", speed: float = 1.0):
    """文字转语音 — 课文朗读/游戏配音"""
    # 声学模型推理
    mel_spectrogram = tts_inference(text, speaker, speed, tts_model)
    # 声码器推理
    audio = vocoder_inference(mel_spectrogram, vocoder)
    
    return StreamingResponse(
        iter([audio]),
        media_type="audio/wav",
        headers={"Content-Disposition": "inline; filename=speech.wav"}
    )

@app.post("/api/v1/tts/stream")
async def stream_speech(text: str):
    """流式语音合成 — 低延迟首包输出"""
    # 分句流式合成
    sentences = split_sentences(text)
    for sent in sentences:
        audio_chunk = synthesize_chunk(sent)
        yield audio_chunk

@app.get("/api/v1/tts/voices")
async def list_voices():
    """可用音色列表"""
    return {
        "voices": [
            {"id": "female_teacher", "name": "女教师", "language": "zh-CN", "style": "温和"},
            {"id": "male_narrator", "name": "男旁白", "language": "zh-CN", "style": "沉稳"},
            {"id": "child_voice", "name": "童声", "language": "zh-CN", "style": "活泼"},
            {"id": "english_female", "name": "English Female", "language": "en-US", "style": "Clear"},
        ]
    }
```

### 启动服务
```bash
uvicorn tts_service:app --host 127.0.0.1 --port 8903
```

## 教学场景集成

### 场景一：游戏角色配音（能力二增强）
```javascript
// 为 p5.js 游戏角色生成语音
async function speakAsCharacter(text, characterId) {
    const response = await fetch('http://127.0.0.1:8903/api/v1/tts/synthesize', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            text: text,
            speaker: characterId,  // 角色对应不同音色
            speed: 1.0
        })
    });
    const audioBlob = await response.blob();
    const audioUrl = URL.createObjectURL(audioBlob);
    const audio = new Audio(audioUrl);
    audio.play();
    return audio;
}

// 游戏中使用
function onNPCDialogue() {
    speakAsCharacter('欢迎来到 AI 知识闯关！', 'wise_owl');
}
```

### 场景二：课文朗读
```javascript
// 课文自动朗读
async function readAloud(text, voice = 'female_teacher') {
    const response = await fetch('http://127.0.0.1:8903/api/v1/tts/synthesize', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ text, speaker: voice, speed: 0.9 })
    });
    const audioBlob = await response.blob();
    playAudio(audioBlob);
}
```

## OpenVINO 优化步骤

### 1. 模型转换与量化
```bash
# FastSpeech2 → OpenVINO IR
optimum-cli export openvino --model PaddleSpeech/fastspeech2_csmsc --weight-format fp16 models/fastspeech2_fp16
# INT8 量化
optimum-cli export openvino --model PaddleSpeech/fastspeech2_csmsc --weight-format int8 models/fastspeech2_int8
```

### 2. 性能验证
| 指标 | 目标值 | 测试方法 |
|------|--------|---------|
| 合成实时率 (RTF) | <0.5 | 100 句测试集 |
| 首包延迟 | <200ms | 流式合成测试 |
| 自然度 MOS | ≥3.5 | 主观评测（5分制） |
| 音色相似度 | ≥85% | 说话人相似度测试 |

## 错误降级
| 场景 | 降级方案 |
|------|---------|
| GPU 不可用 | 降级为 CPU 推理（RTF 增加 2-3x） |
| TTS 服务崩溃 | 降级为浏览器原生 SpeechSynthesis API |
| 模型加载失败 | 降级为 Edge-TTS 云端 API |
| 合成质量差 | 降低语速或使用备选音色 |

## 质量门控
- [ ] 合成 RTF <0.5（GPU 推理）
- [ ] MOS 自然度评分 ≥3.5
- [ ] 首包延迟 <200ms（流式模式）
- [ ] 支持至少 4 种音色
- [ ] 中英文混合朗读准确率 ≥95%
- [ ] 内存峰值 <500MB
