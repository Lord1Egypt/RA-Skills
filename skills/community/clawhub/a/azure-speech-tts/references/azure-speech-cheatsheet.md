# Azure Speech TTS Cheatsheet

## Configuration

Default config file: `config.json`

```json
{
  "default_voice": "zh-CN-Yunqi:DragonHDOmniLatestNeural",
  "default_format": "mp3",
  "default_output_dir": "download",
  "default_timeout_seconds": 60
}
```

Secret values still belong in environment variables:
- `AZURE_SPEECH_KEY`
- `AZURE_SPEECH_REGION`

Optional overrides:
- `AZURE_SPEECH_VOICE`
- `AZURE_SPEECH_FORMAT`

Precedence:
1. CLI flag
2. Environment variable
3. `config.json`
4. Built-in fallback

## Common defaults

- Default voice in the helper script: `zh-CN-Yunqi:DragonHDOmniLatestNeural`
- Default output format: `audio-24khz-48kbitrate-mono-mp3`
- Default output folder: `download/`

## Output format aliases

| Alias | Azure format | Extension |
|---|---|---|
| `mp3` | `audio-24khz-48kbitrate-mono-mp3` | `.mp3` |
| `wav` | `riff-24khz-16bit-mono-pcm` | `.wav` |
| `pcm` | `raw-16khz-16bit-mono-pcm` | `.pcm` |
| `ogg` | `ogg-24khz-16bit-mono-opus` | `.ogg` |

## Plain text example

```bash
python3 scripts/azure_tts.py \
  --text "你好，这是一段测试语音。" \
  --voice zh-CN-Yunqi:DragonHDOmniLatestNeural \
  --format mp3 \
  --output download/test.mp3
```

## SSML example

```bash
python3 scripts/azure_tts.py \
  --ssml-file temp/input.ssml \
  --format wav \
  --output download/test.wav
```

SSML input must include a full `<speak>` root element.

## Useful SSML notes

- Use `<prosody rate="..." pitch="...">` for pacing and pitch.
- Use `style` for expressive neural voices, e.g. `cheerful`, `sad`, `chat`.
- Use `styledegree` for stronger or weaker expression when the voice supports it.
- Use `role` only when the target voice supports it.

## Good trigger phrases for the skill

- “用 Azure Speech 把这段文字转成语音”
- “生成一个 mp3 / wav 语音文件”
- “用 Azure TTS 朗读这段内容”
- “帮我写个 SSML 并合成”
