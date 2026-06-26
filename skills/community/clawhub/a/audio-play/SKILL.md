---
 name: audio-play
 description: Play audio files using Windows media player. Non-blocking execution.
 tools:
   - play_audio
---

# Audio Play

## Usage

```bash
python scripts/audio_play.py <audio_path> [--config player_config.json]
```

## Parameters

- `audio_path` (required): Absolute path to audio file
- `config` (optional): Player configuration file

## Player Config (player_config.json)

```json
{
  "player": "vlc",
  "player_path": "C:/Program Files/VideoLAN/VLC/vlc.exe"
}
```

## Returns

```json
{
  "success": true,
  "audio_path": "H:/works/audio/xxx.mp3",
  "player_used": "vlc",
  "duration": 1200
}
```

## Tools

## play_audio

Play audio file with media player


## Workflow Integration

This skill is part of the YouTube translation workflow:
1. **youtube-audio-download**: Download audio from YouTube
2. **doubao-launch**: Launch Doubao translation window
3. **audio-play**: Play the downloaded audio
4. **doubao-capture**: Capture translated subtitles

## Execution

All skills execute on Windows Python via WSL cross-platform call:
```
wsl -> python.exe scripts/audio_play.py ...
```

## Error Handling

All skills return JSON with `success` field:
- `success: true` - Operation completed
- `success: false` - Check `error_code` and `error_message`

## Notes

- Windows GUI automation requires visible desktop (no RDP disconnect)
- Output files are stored in Windows `works/` directory
- WSL accesses Windows files via `/mnt/h/...`
