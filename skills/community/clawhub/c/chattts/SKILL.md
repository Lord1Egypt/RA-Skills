---
name: chattts
description: High-quality, conversational Text-to-Speech (TTS) generation via local ChatTTS API.
metadata: {"clawdbot":{"emoji":"🎙️","requires":{"bins":["node"],"env":["http://172.23.252.114:8020"]},"primaryEnv":"http://172.23.252.114:8020"}}
---

# ChatTTS Voice Generator

AI-optimized conversational text-to-speech using a local ChatTTS server. Designed to generate highly natural human voices with realistic laughs, breathing, and pauses.

## Generate Speech

```bash
node {baseDir}/scripts/tts.mjs "你要转换的语音文本"
node {baseDir}/scripts/tts.mjs "你好啊！[laugh] 今天天气真不错，[uv_break] 我们出去玩吧？" --seed 2048
node {baseDir}/scripts/tts.mjs "写代码真是太开心了！" --seed 1234 --temperature 0.5
```

## Options
- `--seed <number>`: Random seed to fix the speaker's voice/timbre (default: 2048). Change this number to switch between different male/female voices.
- `--temperature <float>`: Controls the emotional variance and stability (default: 0.3). Lower is more stable and clear, higher (e.g., 0.6) is more expressive but might mumble.
- `--top_p <float>`: Top P sampling parameter for voice generation (default: 0.7).

## Notes
- Requires the local ChatTTS FastAPI server to be running (default target: http://172.23.252.114:8020).
- Ensure CHATTTS_API_URL is set in your .env file if the API is hosted on a different machine.
- PRO TIP: Always try to insert [laugh] (laughter) and [uv_break] (pauses/breaths) into the text to make the generated voice sound exactly like a real human.
- The script will return the absolute local file path of the generated .wav audio file.