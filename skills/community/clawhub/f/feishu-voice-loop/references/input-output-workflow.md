# Input / Output Workflow

## Goal

The core product shape is:

1. **Input text or voice**
2. **Call OpenAI TTS to generate speech**
3. **Return audio to Feishu or a web player**

When the input is voice, insert one extra step before TTS:
- local audio file -> transcription text

## Voice input

Use `scripts/transcribe_audio.py` when you have a local audio file and want text.

Example:

```bash
python3 scripts/transcribe_audio.py /path/to/input.ogg
```

Behavior:
- Reads the first configured Whisper-style CLI model from `~/.openclaw/openclaw.json`
- Reuses the existing `tools.media.audio.models[0]` configuration
- Writes a JSON result with the transcript text

Best use cases:
- Testing a full voice loop locally
- Turning Feishu-downloaded audio into text before replying
- Building a reusable voice interface skill for others

## Voice output

Use `scripts/openai_tts_feishu.py` when you already have text and want to send a Feishu voice message.

Example:

```bash
python3 scripts/openai_tts_feishu.py \
  --to ou_xxx \
  --text "这条是语音测试。"
```

## Full loop

Typical end-to-end flow:

1. Receive or save an audio file locally
2. Run `transcribe_audio.py` to get text
3. Decide the response text
4. Run `openai_tts_feishu.py` to synthesize and deliver the reply

This means the skill can be packaged as a reusable voice-in / voice-out building block, not just a TTS sender.
