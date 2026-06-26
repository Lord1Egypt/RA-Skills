---
name: fish-speech
description: Fish Audio S2 Pro TTS.
---

# Fish Audio S2 Pro TTS

Dual-AR architecture (Slow AR 4B + Fast AR 400M), 10 RVQ codebooks, ~21 Hz frame rate, 80+ languages.

- **Model**: [fishaudio/s2-pro](https://huggingface.co/fishaudio/s2-pro)
- **Output**: 44.1 kHz WAV/PCM mono
- **VRAM**: ≥24GB for inference, A800/H200 recommended
- **Technical Report**: [arXiv 2603.08823](https://arxiv.org/abs/2603.08823) | [Architecture](references/architecture.md)

## Installation

See [references/install.md](references/install.md). Quick summary:

```bash
conda create -n fish-speech python=3.12 && conda activate fish-speech
pip install -e .[cu129]     # CUDA 12.9
# or: uv sync --python 3.12 --extra cu129
# minimal: pip install fish-speech

apt install portaudio19-dev libsox-dev ffmpeg  # System dependencies
hf download fishaudio/s2-pro --local-dir checkpoints/s2-pro
```

## Server Deployment

**vLLM-Omni (recommended, OpenAI compatible):**
```bash
pip install fish-speech
vllm serve fishaudio/s2-pro --omni --port 8091
# Endpoints: POST /v1/audio/speech, /v1/audio/speech/batch
```

**SGLang-Omni (high-performance streaming):**
```bash
sgl-omni serve --model-path fishaudio/s2-pro --config examples/configs/s2pro_tts.yaml --port 8000
# RTF 0.195, TTFA ~100ms, throughput 3000+ t/s
```

**Docker:**
```bash
docker compose --profile webui up    # Port 7860
COMPILE=1 docker compose --profile webui up  # ~10x speedup
```

**Native API Server:**
```bash
python tools/api_server.py --llama-checkpoint-path checkpoints/s2-pro --decoder-checkpoint-path checkpoints/s2-pro/codec.pth --listen 0.0.0.0:8080
```

## Raw CLI Inference (Three Steps)

```bash
# 1. Extract VQ tokens
python fish_speech/models/dac/inference.py -i "ref.wav" --checkpoint-path "checkpoints/s2-pro/codec.pth"
# 2. Generate semantic tokens
python fish_speech/models/text2semantic/inference.py --text "Text" --prompt-text "Reference text" --prompt-tokens "fake.npy"
# 3. Decode to audio
python fish_speech/models/dac/inference.py -i "codes_0.npy"
```

## API Calls

### cURL

```bash
# Basic TTS
curl -X POST http://localhost:8091/v1/audio/speech \
  -H "Content-Type: application/json" \
  -d '{"input": "Hello."}' --output out.wav

# Voice cloning (vLLM)
curl -X POST http://localhost:8091/v1/audio/speech \
  -H "Content-Type: application/json" \
  -d '{"input": "Cloned voice.", "ref_audio": "https://...", "ref_text": "Reference transcription"}' --output cloned.wav

# Streaming PCM
curl -N -X POST http://localhost:8091/v1/audio/speech \
  -H "Content-Type: application/json" \
  -d '{"input": "Streaming.", "stream": true, "response_format": "pcm"}' --no-buffer | play -t raw -r 44100 -e signed -b 16 -c 1 -

# Batch
curl -X POST http://localhost:8091/v1/audio/speech/batch \
  -H "Content-Type: application/json" \
  -d '{"items": [{"input": "Sentence 1"}, {"input": "Sentence 2"}], "voice": "default"}'
```

### Python

```python
import requests
resp = requests.post("http://localhost:8091/v1/audio/speech", json={
    "input": "Hello.", "voice": "default",
    "ref_audio": "https://...", "ref_text": "Reference text"
})
with open("out.wav", "wb") as f: f.write(resp.content)

# OpenAI SDK
from openai import OpenAI
client = OpenAI(base_url="http://localhost:8091/v1", api_key="none")
client.audio.speech.create(model="fishaudio/s2-pro", voice="default", input="Hello.").stream_to_file("out.wav")
```

SGLang format: `"references": [{"audio_path": "...", "text": "..."}]`

## Request Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `input` | string | Required | Text to synthesize |
| `voice` | string | `"default"` | Voice |
| `response_format` | string | `"wav"` | wav/mp3/flac/pcm/aac/opus |
| `speed` | float | `1.0` | Speech speed (0.25-4.0) |
| `stream` | bool | false | Streaming (requires `response_format="pcm"`) |
| `ref_audio` | string | null | Reference audio URL/base64/file:// |
| `ref_text` | string | null | Reference audio transcription |
| `max_new_tokens` | int | 2048 | Max generation tokens |
| `temperature` | float | null | Sampling temperature |
| `top_p` | float | null | Nucleus sampling |
| `top_k` | int | null | Top-K |
| `repetition_penalty` | float | null | Repetition penalty |
| `seed` | int | null | Random seed |

## Emotion Tags

Embed `[tag]` anywhere in the text, supports 15000+ free-form tags:

```
[excited]Today is a great day![pause] [whisper in small voice]But there's a secret…
[professional broadcast tone]Welcome.
```

Common: `[excited]` `[angry]` `[sad]` `[whisper]` `[shouting]` `[laughing]` `[pause]` `[emphasis]` `[echo]` `[inhale]` `[sigh]` `[singing]`

Full reference: [references/emotion-tags.md](references/emotion-tags.md)

## Multi-Speaker

```text
<|speaker:0|>Hello, welcome.
<|speaker:1|>Thank you, glad to be here.
```

## LoRA Fine-tuning

⚠️ Not recommended for models after RL. Only fine-tune Slow AR:

```bash
# Preparation: data/SPK1/*.mp3 + *.lab
python tools/vqgan/extract_vq.py data --config-name modded_dac_vq --checkpoint-path checkpoints/openaudio-s1-mini/codec.pth
python tools/llama/build_dataset.py --input data --output data/protos
python fish_speech/train.py --config-name text2semantic_finetune project=my_project +lora@model.model.lora_config=r_8_alpha_16
python tools/llama/merge_lora.py --lora-config r_8_alpha_16 --base-weight checkpoints/openaudio-s1-mini --lora-weight results/my_project/checkpoints/step_xxx.ckpt --output checkpoints/merged/
```

See [references/finetune.md](references/finetune.md)

## Important Notes

1. Voice cloning: Reference audio 10-30 seconds, clear and noise-free, provide accurate transcription
2. Without reference audio, voice tends to sound mechanical
3. vLLM is easy to deploy; SGLang has better latency/throughput
4. SGLang: BF16 RoPE precision must match training; if early EOS occurs, switch to FA3
5. Fast AR torch.compile can achieve ~5x speedup
6. Docker image does not include model weights; mount checkpoints