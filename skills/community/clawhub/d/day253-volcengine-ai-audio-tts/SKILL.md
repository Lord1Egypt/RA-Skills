---
name: volcengine-ai-audio-tts
description: Text-to-speech generation on Volcengine (ByteDance) speech services. Use when users need narration, multi-language speech output, voice selection, or TTS troubleshooting. Supports online one-shot HTTP API (openspeech.bytedance.com).
---

Category: provider

# Volcengine 语音合成 TTS

## Validation

```bash
mkdir -p output/volcengine-ai-audio-tts
python -m py_compile skills/ai/audio/volcengine-ai-audio-tts/scripts/generate_tts.py && echo "py_compile_ok" > output/volcengine-ai-audio-tts/validate.txt
```

Pass criteria: command exits 0 and `output/volcengine-ai-audio-tts/validate.txt` is generated.

## Output And Evidence

- Save generated audio files, request payloads, and response metadata to `output/volcengine-ai-audio-tts/`.
- Keep one validation log per execution.

## Prerequisites

- Python 3.8+. No extra SDK required (uses `requests` and stdlib).
- Install: `pip install requests`
- Set environment variables (from Volcengine 豆包语音控制台):
  - `VOLCENGINE_TTS_APP_ID` — 应用 ID
  - `VOLCENGINE_TTS_TOKEN` — 应用 Token（用于 Authorization: Bearer;${token}）
  - `VOLCENGINE_TTS_CLUSTER` — 业务集群，如 `volcano_tts`（标准音色）

Optional: use `.env` in repo root or script directory; script will load them.

## Normalized interface (tts.generate)

### Request
- `text` (string, required) — 合成文本，UTF-8，单次建议 ≤1024 字节
- `voice_type` (string, required) — 音色，见 [发音人参数列表](https://www.volcengine.com/docs/6561/79824)，如 `BV700_streaming`
- `encoding` (string, optional) — 编码格式：`pcm` | `wav` | `mp3` | `ogg_opus`，默认 `mp3`
- `rate` (int, optional) — 采样率 8000/16000/24000，默认 24000
- `speed_ratio` (float, optional) — 语速 [0.2, 3]，默认 1.0
- `volume_ratio` (float, optional) — 音量 [0.1, 3]，默认 1.0
- `pitch_ratio` (float, optional) — 音高 [0.1, 3]，默认 1.0
- `language` (string, optional) — 语言，如 `cn`

### Response
- `audio_path` (string) — 本地保存的音频文件路径
- `sample_rate` (int)
- `format` (string)
- `duration_ms` (string, when returned by API)
- `code` (int) — 3000 表示成功

## Quick start (Python script)

```bash
# 使用内联 JSON 请求
python skills/ai/audio/volcengine-ai-audio-tts/scripts/generate_tts.py \
  --request '{"text":"你好，这是一段测试语音。","voice_type":"BV700_streaming"}' \
  --output output/volcengine-ai-audio-tts/audio/out.mp3

# 使用请求文件
python skills/ai/audio/volcengine-ai-audio-tts/scripts/generate_tts.py \
  --file request.json \
  --output output/volcengine-ai-audio-tts/audio/out.wav \
  --print-response
```

## Operational guidance

- 每次请求的 `reqid` 需唯一，脚本内使用 UUID。
- 长文本请分段多次调用或使用异步长文本接口。
- 音色与 `cluster` 需与控制台一致；复刻音色使用 speaker id 作为 `voice_type`。
- 遇 429 请降低并发或增加间隔。

## Output location

- Default output: `output/volcengine-ai-audio-tts/audio/`
- Override base dir with `OUTPUT_DIR`.

## Workflow

1) Confirm user intent, text, voice, and output format.
2) Run one minimal request to verify credentials and cluster/voice_type.
3) Execute the target synthesis with explicit parameters.
4) Verify results and save output/evidence files.

## References

- `references/api_reference.md` — 请求/响应参数与错误码
- [在线语音合成 API - HTTP 一次性合成](https://www.volcengine.com/docs/6561/79820)
- [参数基本说明](https://www.volcengine.com/docs/6561/79823)
- [发音人参数列表](https://www.volcengine.com/docs/6561/79824)
- Source list: `references/sources.md`
