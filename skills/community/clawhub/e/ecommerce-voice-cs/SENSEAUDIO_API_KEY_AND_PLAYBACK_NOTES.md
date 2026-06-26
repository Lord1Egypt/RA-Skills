# SenseAudio API Key And Playback Notes

## Summary

This round includes two changes:

- API key loading now prioritizes the environment variable `SENSEAUDIO_API_KEY`
- Audio output now defaults to MP3 and returns a host playback protocol block

## API Key Behavior

The skill now uses this order:

1. Check environment variable `SENSEAUDIO_API_KEY`
2. If missing, ask the caller or user to provide `api_key`

Result:

- If `SENSEAUDIO_API_KEY` exists, `api_key` is no longer treated as required during configuration collection
- If `SENSEAUDIO_API_KEY` does not exist, `api_key` is still requested normally

## Playback Design Chosen

The selected design is:

1. Generate and retain the MP3 file on disk
2. Return `audio_file` as the persistent artifact path
3. Return a `playback` object so the host can immediately play the same file

This means the file is not lost, and the host can still provide an instant playback experience.

## Response Contract

When audio generation succeeds, the response now contains:

```json
{
  "audio_file": "tts_output\\cs_reply_20260315_210818.mp3",
  "playback": {
    "action": "play_audio",
    "auto_play": true,
    "source_type": "local_file",
    "path": "tts_output\\cs_reply_20260315_210818.mp3",
    "format": "mp3",
    "mime_type": "audio/mpeg",
    "retain_file": true
  }
}
```

Field meaning:

- `audio_file`: persistent file path kept on disk
- `playback.action`: host should treat this as an audio playback instruction
- `playback.auto_play`: host should play immediately
- `playback.source_type`: current source is a local file path
- `playback.path`: exact file path the host should play
- `playback.format`: file format, currently expected to be `mp3` by default
- `playback.mime_type`: media MIME type for the host player
- `playback.retain_file`: do not delete the file after playback

During configuration-only stages where no audio is generated:

```json
{
  "audio_file": null,
  "playback": null
}
```

## Host Contract For 龙虾

Recommended host behavior:

1. Read the skill response
2. If `playback` is present and `playback.action == "play_audio"`, immediately play `playback.path`
3. Do not delete the file after playback because `retain_file` is `true`
4. If autoplay fails, keep `audio_file` for retry or manual playback

## Default Audio Format

The skill now defaults `audio_format` to `.mp3` in the main `handle(payload)` flow.

Callers can still override it explicitly, for example:

```python
{
    "audio_format": ".wav"
}
```

But for host autoplay, MP3 is now the default path.

## Files Changed

- `helper.py`
- `src/ecommerce_voice_cs/voice.py`
- `src/ecommerce_voice_cs/skill.py`
- `README.MD`
- `SKILL.md`
- `SENSEAUDIO_API_KEY_AND_PLAYBACK_NOTES.md`

## Verification

- Verified that when `SENSEAUDIO_API_KEY` exists, `api_key` is no longer reported as missing
- Verified that when `SENSEAUDIO_API_KEY` does not exist, `api_key` is still reported as missing
- Verified `py_compile` passes
- Verified non-audio responses now return `playback: null`
