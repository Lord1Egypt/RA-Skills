# ASR Service — SenseVoice-Small 🎤

中文语音识别技能，基于 [FunASR SenseVoice-Small](https://github.com/modelscope/FunASR) 模型，通过 [InferFabric](https://github.com/vincentlau2046-sudo/inferfabric) 托管部署。

## 功能

| 功能 | 说明 |
|------|------|
| 语音转文字 | 中/英/日/韩/粤 5 语种，自动语言检测 |
| 说话人分离 | 多人对话场景，标注 SPK0/SPK1... |
| SRT 字幕 | 一键生成 SRT 格式字幕文件 |
| VTT 字幕 | 一键生成 VTT 格式字幕文件 |
| 长音频 | VAD 自动切分，支持任意时长 |
| 情感/事件检测 | SenseVoice 内置（server 端已清洗标记） |

## 架构

```
消费者 (Nova / CLI / 其他 Skill)
  → ASRSkill (transcribe / transcribe_srt / transcribe_vtt / serve_status)
    → IFFManager → iff switch sensevoice-small
    → httpx → http://localhost:8881/v1/audio/transcriptions
    → Postprocessor → TranscriptionResult / SRT / VTT
```

**职责边界**：IFF 管进程生命周期 + GPU 调度，Skill 管 API 调用 + 后处理。

## 环境要求

### 硬件

- **GPU**: NVIDIA GPU，≥2GB VRAM（SenseVoice-Small ~900MB）
- **CUDA**: 11.8+

### 软件

- **Python**: 3.12+
- **Conda**: Miniconda 或 Anaconda
- **InferFabric**: v4.7.0+（ASR 服务托管）
- **FunASR**: 1.4.1+（含 funasr-server CLI）

### 依赖 Python 包

- `httpx` — HTTP 客户端
- `pyyaml` — 配置文件解析

## 一键安装

```bash
# 1. 创建 Conda 环境 + 安装 FunASR
conda create -n sensevoice python=3.12 -y
conda activate sensevoice
pip install "funasr>=1.4.1" modelscope httpx pyyaml

# 2. 预下载 SenseVoice-Small 模型（可选，首次调用也会自动下载）
python -c "from funasr import AutoModel; AutoModel(model='iic/SenseVoiceSmall', vad_model='fsmn-vad')"

# 3. 验证 funasr-server 可用
funasr-server --help

# 4. 安装 InferFabric（如未安装）
pip install inferfabric
# 或参考 https://github.com/vincentlau2046-sudo/inferfabric

# 5. 在 InferFabric 中注册 ASR 服务
# 将 sensevoice-small.yaml 放入 IFF 的 models.d/ 目录
# 示例配置：
cat > /path/to/inferfabric/models.d/sensevoice-small.yaml << 'EOF'
name: sensevoice-small
type: asr_server
description: "SenseVoice-Small ASR"
port: 8881
conda_env: sensevoice
start_cmd: "funasr-server --model sensevoice --device cuda --port 8881"
health_url: "http://localhost:8881/health"
gpu_role: shared
EOF

# 6. 安装 ASR Skill
openclaw skills install asr-service
```

### 快速验证安装

```bash
# 启动 ASR 服务
iff switch sensevoice-small

# 等待就绪后测试
curl -s http://localhost:8881/health
# 期望: {"status":"ok","device":"cuda","models_loaded":["sensevoice"]}

# CLI 转写测试
python ~/.openclaw/workspace/skills/asr-service/scripts/asr_cli.py transcribe test.wav

# 停止服务
iff stop sensevoice-small
```

## API

### Python 调用

```python
from asr_service import ASRSkill

skill = ASRSkill()

# 基本转写
result = skill.transcribe("meeting.mp3")
print(result.text)

# 带说话人分离
result = skill.transcribe("meeting.mp3", speaker_labels=True, response_format="verbose_json")
for seg in result.segments:
    print(f"[{seg.get('speaker', '?')}] {seg['text']}")

# SRT 字幕
srt_text = skill.transcribe_srt("video.mp3", speaker_labels=True)

# VTT 字幕
vtt_text = skill.transcribe_vtt("video.mp3")

# 服务状态
status = skill.serve_status()
```

### CLI

```bash
# 基本转写
asr_cli.py transcribe audio.mp3

# 带说话人分离
asr_cli.py transcribe audio.mp3 --speakers

# SRT 字幕
asr_cli.py srt audio.mp3 --speakers

# VTT 字幕
asr_cli.py vtt audio.mp3

# 服务状态
asr_cli.py serve-status
```

## 配置

`config.yaml`:

```yaml
service:
  name: sensevoice-small
  base_url: http://localhost:8881
  health_timeout: 120
  switch_timeout: 120

retry:
  max_attempts: 3

defaults:
  model: sensevoice
  language: null        # null = 自动检测
  response_format: json
```

## 约束

- 所有 API 请求显式传 `model="sensevoice"`，不依赖默认值
- 不使用 `/asr` 端点（会无条件触发 vLLM 加载）
- 说话人分离需要 `fsmn-vad` + `cam++` 模型（首次 `speaker_labels=True` 时自动下载，~28MB）
- TTS/ASR/VLA 等非 LLM 服务走直连端口，不经过 IFF Proxy

## 版本历史

| 版本 | 日期 | 变更 |
|------|------|------|
| 1.1.0 | 2026-08-05 | 说话人分离 + SRT/VTT 字幕输出 |
| 1.0.0 | 2026-08-05 | 初始版本，SenseVoice-Small 转写 |

## License

MIT
