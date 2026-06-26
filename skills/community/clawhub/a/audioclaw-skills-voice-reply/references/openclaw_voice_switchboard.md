# Official capability summary

Sources used:
- `https://senseaudio.cn/docs/text_to_speech_api`
- `https://senseaudio.cn/docs/voice_api`

# Voice lookup rule

When AudioClaw needs to find or verify a voice:
- Check the local runtime catalog first with `python3 scripts/openclaw_voice_switchboard.py --list-voices`
- If the user asks for the official public voice list, pricing tier, or a voice not present in the local catalog, open `https://senseaudio.cn/docs/voice_api`
- Treat `https://senseaudio.cn/docs/voice_api` as the canonical public reference for:
  - official voice names
  - `voice_id`
  - free / VIP / SVIP package notes
  - whether a voice family exposes multiple emotional variants
- After selecting a candidate `voice_id`, still validate it at runtime because API-key permissions may differ across accounts

Confirmed public TTS request fields:
- `model`
- `text`
- `stream`
- `voice_setting.voice_id`
- `voice_setting.speed`
- `voice_setting.vol`
- `voice_setting.pitch`
- `audio_setting.format`
- `audio_setting.sample_rate`

Confirmed parameter ranges from the public docs:
- `speed`: `[0.5, 2.0]`
- `vol`: `[0, 10]`
- `pitch`: `[-12, 12]`

Important boundary:
- The public TTS docs do not show a standalone `emotion` field.
- Emotion is surfaced in practice through different official `voice_id` variants and voice-family bundles.
- The voice API page also states that multi-scene emotional switching such as `温柔 / 严肃 / 活力` is part of custom or selected voice offerings.
- For AudioClaw final-file generation, prefer non-stream TTS unless you truly need token-by-token playback. It is simpler and avoids stream reassembly edge cases.
- The current official HTTP TTS path still authenticates with `Authorization: Bearer API_KEY`.
- The API key page shows both `API Key` and `Public Key`, but the public TTS HTTP docs do not require `Public Key` for this server-side path.

# Why this skill exists

AudioClaw usually wants a stable contract:
- pass text
- pass desired tone
- get back one local audio file and a trace id

This skill hides three runtime problems:
- a requested emotion may need a different `voice_id`
- a requested paid voice may not be available to the current key
- repeated replies should reuse cached audio instead of regenerating it
- some users want a persistent "always reply with voice" mode
- AudioClaw media send may fail if the output file is not readable by the sender or is not referenced relative to the workspace
- some Feishu-style voice channels prefer `ogg/opus`, while the public TTS service returns `mp3/wav/pcm/flac`
- AudioClaw may try `send_file(path=...)` even when Feishu really needs an `audio` message type

# AudioClaw request examples

Basic assistant reply:

```json
{
  "text": "我们已经收到你的需求，今天下午会把结果发给你。",
  "scene": "assistant",
  "emotion": "calm"
}
```

Switch to a named family and let the skill pick the best emotion variant:

```json
{
  "text": "新品今晚八点开售，现在下单还有首发赠品。",
  "scene": "sales",
  "voice_family": "male_0027",
  "emotion": "promo",
  "allow_fallback": true
}
```

Force a specific voice:

```json
{
  "text": "我先把重点说清楚，再给你完整报告。",
  "voice_id": "male_0004_a",
  "emotion": "serious",
  "strict_voice": true
}
```

Persist a user preference:

```json
{
  "preference_key": "feishu:ou_xxx",
  "reply_mode": "voice",
  "voice_id": "male_0004_a",
  "emotion": "calm",
  "scene": "assistant"
}
```

Force a Feishu-friendly voice-note delivery:

```json
{
  "text": "这是一次飞书语音发送测试。",
  "scene": "assistant",
  "emotion": "calm",
  "delivery_profile": "feishu_voice"
}
```

# Response shape

The main script prints a JSON manifest. The fields AudioClaw usually needs are:
- `delivery.reply_mode`
- `delivery.voice_enabled`
- `delivery.delivery_profile`
- `delivery.file_mode`
- `delivery.openclaw_media_reference`
- `resolved.voice_id`
- `resolved.official_emotion`
- `resolved.emotion_strategy`
- `resolved.settings`
- `audio.path`
- `audio.trace_id`

The AudioClaw wrapper script prints:
- `mode`
- `audio_path`
- `chat_id`
- `message_id`
- `send_result`
- `manifest`

# AudioClaw workspace note

For Feishu or Lark media sending, the most reliable pattern is:
- write the output under the AudioClaw workspace
- keep the file mode readable, typically `0644`
- send `MEDIA:./relative/path` instead of a random absolute path when the channel expects workspace-relative media
- if the downstream channel expects a voice-note style upload, use `delivery_profile=feishu_voice` so the final file is transcoded to `ogg/opus`
- this publishable bundle does not include a bundled ffmpeg binary; use system `ffmpeg` or install `imageio-ffmpeg`
- if you do not provide `--out` but do provide `--openclaw-workspace-root`, this skill will now write into `workspace/state/audio/` automatically to avoid fragile temp files at the workspace root
- current AudioClaw docs still describe `MEDIA:...` lines for outbound attachments, but this AudioClaw environment is not rendering them
- AudioClaw's generic `send_file` path is fine for normal files, but Feishu voice notes need official upload plus `msg_type=audio`
- for AudioClaw on Feishu, prefer `scripts/picoclaw_voice_reply.py` and let it send the audio directly
- do not pass the local path or `MEDIA:...` to the `message` tool, because AudioClaw will send those strings literally

# Notes for same-speaker emotion switching

There are two distinct modes:

1. `voice_variant`
- Best option.
- The chosen voice family already has multiple official emotional variants.

2. `parameter_shaping`
- Fallback option.
- The skill keeps the same voice and nudges `speed / pitch / vol`.

If the product requirement is "same speaker, many emotions, same timbre", use:
- a voice family that already exposes multiple emotional variants, or
- an authorized custom voice with matching rights.
