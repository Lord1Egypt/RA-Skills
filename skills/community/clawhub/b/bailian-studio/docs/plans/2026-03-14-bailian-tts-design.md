# Bailian Studio TTS 播报设计文档

**目标**
- 在 `dev/bailian-studio` 中新增百炼 TTS 播报能力。
- 仅实现 **文本 → 语音播放**（不包含语音输入/识别）。
- 输出格式为 **WAV**，使用 **simpleaudio** 播放。

**范围**
- 新增脚本 `scripts/tts_speak.py`。
- 支持通过环境变量或 `secrets/bailian.env` 覆盖模型/音色/采样率。
- 依赖 `dashscope` 与 `simpleaudio`。

---

## 设计概览

采用“**TTS 生成 WAV → simpleaudio 播放**”的流程。配置统一通过现有 `env.py` 读取（新增 TTS 相关键）。无配置时使用百炼默认模型与默认音色。

---

## 组件与接口

### 新增脚本
- `scripts/tts_speak.py`
  - 参数：`--text "..."`
  - 行为：
    1. 读取配置（API Key、模型、音色、采样率）。
    2. 调用百炼 TTS API 获取 WAV。
    3. 本地播放并输出完成提示。

### 配置项（环境变量或 `secrets/bailian.env`）
- `DASHSCOPE_API_KEY`
- `BAILIAN_TTS_MODEL`（默认官方默认）
- `BAILIAN_TTS_VOICE`（默认音色）
- `BAILIAN_TTS_SAMPLE_RATE`（默认 16000）

---

## 流程

1. 解析命令行参数（文本）。
2. 读取配置（env/file）。
3. 调用百炼 TTS（WAV）。
4. simpleaudio 播放。
5. 输出完成日志。

---

## 验收标准

- `python3 scripts/tts_speak.py --text "测试"` 能播出声音。
- 未配置时使用默认模型/音色。
- `secrets/bailian.env` 可覆盖配置。

---

## 后续扩展（不在本次范围）

- 语音输入（ASR）。
- 情感/语速/音量等高级参数。
- 直接语音对话链路（STT → LLM → TTS）。
