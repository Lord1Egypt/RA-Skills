---
 name: doubao-launch
 description: Launch Doubao desktop application and configure real-time translation window.
 tools:
   - launch_doubao
---

# Doubao Launch

## Usage

```bash
python scripts/doubao_auto_workflow.py [--dual|--single] --json-output
```

## Parameters

- `mode` (optional): "dual" or "single", default: "dual"

## Returns

```json
{
  "success": true,
  "window_handle": 123456,
  "window_title": "Doubao - Real-time Subtitles",
  "mode": "dual"
}
```

## Tools

## launch_doubao

Launch Doubao application


## Workflow Integration

This skill is part of the YouTube translation workflow:
1. **youtube-audio-download**: Download audio from YouTube
2. **doubao-launch**: Launch Doubao translation window
3. **audio-play**: Play the downloaded audio
4. **doubao-capture**: Capture translated subtitles

## Execution

All skills execute on Windows Python via WSL cross-platform call:
```
wsl -> python.exe scripts/doubao_auto_workflow.py ...
```

## Error Handling

All skills return JSON with `success` field:
- `success: true` - Operation completed
- `success: false` - Check `error_code` and `error_message`

## Notes

- Windows GUI automation requires visible desktop (no RDP disconnect)
- Output files are stored in Windows `works/` directory
- WSL accesses Windows files via `/mnt/h/...`
