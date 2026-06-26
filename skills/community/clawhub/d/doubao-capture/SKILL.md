---
 name: doubao-capture
 description: Capture Doubao translation results with auto-scroll and auto-end detection.
 tools:
   - capture_translation
---

# Doubao Capture

## Usage

```bash
python scripts/capture_doubao_scroll_v2.py --hwnd <window_handle> --output-dir <dir> --stop-auto --json-output
```

## Parameters

- `window_handle` (required): HWND from doubao-launch
- `output_dir` (optional): Output directory, default: "works/translations"
- `stop_auto` (optional): Auto-detect end, default: true
- `no_new_threshold` (optional): Consecutive empty reads threshold, default: 5

## Returns

```json
{
  "success": true,
  "text_file_path": "H:/works/translations/doubao_20240307_143022.txt",
  "line_count": 156,
  "char_count": 3847,
  "stopped_by": "auto_detect"
}
```

## Tools

## capture_translation

Capture translated subtitles from Doubao


## Workflow Integration

This skill is part of the YouTube translation workflow:
1. **youtube-audio-download**: Download audio from YouTube
2. **doubao-launch**: Launch Doubao translation window
3. **audio-play**: Play the downloaded audio
4. **doubao-capture**: Capture translated subtitles

## Execution

All skills execute on Windows Python via WSL cross-platform call:
```
wsl -> python.exe scripts/capture_doubao_scroll_v2.py ...
```

## Error Handling

All skills return JSON with `success` field:
- `success: true` - Operation completed
- `success: false` - Check `error_code` and `error_message`

## Notes

- Windows GUI automation requires visible desktop (no RDP disconnect)
- Output files are stored in Windows `works/` directory
- WSL accesses Windows files via `/mnt/h/...`
