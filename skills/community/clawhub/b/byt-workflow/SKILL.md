---
 name: byt-workflow
 description: YouTube video translation workflow, download audio, launch Doubao, play audio, capture translation
 tools:
   - youtube_translate
---

# Byt Workflow

## Usage

```bash
python workflow.py <youtube_url> [mode]
```

## Parameters

- `url` (required): YouTube video URL
- `mode` (optional): Translation mode (dual, single, chinese, bilingual), default: "dual"

## Workflow Steps

1. **Download YouTube audio** - Uses youtube-audio-download skill
2. **Launch Doubao** - Uses doubao-launch skill
3. **Play audio** - Uses audio-play skill
4. **Capture translation** - Uses doubao-capture skill

## Returns

```json
{
  "success": true,
  "audio_path": "H:/works/audio/video_title-xxxxx.mp3",
  "translation_path": "H:/works/translations/doubao_20240307_143022.txt",
  "duration": 1200
}
```

## Tools

## youtube_translate

Complete YouTube video translation workflow


## Workflow Integration

This skill is part of the YouTube translation workflow:
1. **youtube-audio-download**: Download audio from YouTube
2. **doubao-launch**: Launch Doubao translation window
3. **audio-play**: Play the downloaded audio
4. **doubao-capture**: Capture translated subtitles

## Execution

All skills execute on Windows Python via WSL cross-platform call:
```
wsl -> python.exe scripts/workflow.py ...
```

## Error Handling

All skills return JSON with `success` field:
- `success: true` - Operation completed
- `success: false` - Check `error_code` and `error_message`

## Notes

- Windows GUI automation requires visible desktop (no RDP disconnect)
- Output files are stored in Windows `works/` directory
- WSL accesses Windows files via `/mnt/h/...`
