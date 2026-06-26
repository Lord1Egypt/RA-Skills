---
name: audio-command-handler
description: Handle audio messages as commands. When user sends an audio file (WAV/PCM/MP3), transcribe it using iFlytek Speed Transcription and either (1) execute the transcription as a command if no text accompanies the audio, or (2) use the transcription as context for the accompanying text command. For "audio + text command" scenarios where results exceed 58 characters, automatically save to file and upload via uploader skill. Use when user sends audio files with or without accompanying text instructions.
---

# Audio Command Handler

Process audio messages and execute them as commands.

## Workflow

### Scenario 1: Audio Only (No Text)

User sends an audio file without any text instruction:

1. **Transcribe** the audio using `ifly-speed-transcription` skill
2. **Use transcription as the command** - execute it as if the user typed it
3. **Return result directly** - no file upload needed, regardless of length

### Scenario 2: Audio + Text Command

User sends an audio file WITH a text instruction:

1. **Transcribe** the audio using `ifly-speed-transcription` skill
2. **Execute the text command** with the transcription as context/input
3. **Check result length**:
   - If ≤ 58 characters: return result directly
   - If > 58 characters: save to file, upload via `uploader` skill, return URL

## Quick Reference

### Transcription

```bash
python3 ~/.openclaw/workspace/skills/ifly-speed-transcription/scripts/transcribe.py /path/to/audio.mp3
```

### Upload

```bash
python3 ~/.openclaw/workspace/skills/uploader/scripts/upload_media.py /path/to/file.txt
```

## Execution Flow

```
┌─────────────────┐
│  Audio Message  │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   Transcribe    │
│ (ifly-speed-    │
│  transcription) │
└────────┬────────┘
         │
         ▼
┌─────────────────┐     NO      ┌──────────────┐
│ Has Text Cmd?   │────────────►│ Use Transcrip│
└────────┬────────┘              │ as Command   │
         │ YES                   └──────┬───────┘
         ▼                              │
┌─────────────────┐                     │
│ Execute Text    │                     │
│ Cmd with Trans  │                     │
│ Context         │                     │
└────────┬────────┘                     │
         │                              │
         │                              ▼
         │                    ┌──────────────┐
         │                    │ Return Direct│
         │                    │ to User      │
         │                    │ (no upload)  │
         │                    └──────────────┘
         │
         ▼
┌─────────────────┐
│ Result > 58 ch? │
└────────┬────────┘
         │
         ┌─────────────┴─────────────┐
         │ YES                       │ NO
         ▼                           ▼
┌─────────────────┐         ┌──────────────┐
│ Save to File    │         │ Return Direct│
│ Upload via      │         │ to User      │
│ uploader skill  │         └──────────────┘
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Return URL to   │
│ User            │
└─────────────────┘
```

## Example Scenarios

### Example 1: Audio Only

User sends: 🎤 audio file (speech: "帮我查一下明天上海的天气")

**Flow:**
1. Transcribe → "帮我查一下明天上海的天气"
2. Execute as command → check Shanghai weather for tomorrow
3. Return weather info directly (no upload, regardless of length)

### Example 2: Audio + Command (Short Result)

User sends: 🎤 audio file + text "帮我总结这段录音"

**Flow:**
1. Transcribe audio → get text content
2. Execute "帮我总结这段录音" with transcription as context
3. If summary ≤ 58 chars → return directly

### Example 3: Audio + Command (Long Result)

User sends: 🎤 audio file + text "帮我根据这段录音写一篇文章"

**Flow:**
1. Transcribe audio → get text content
2. Execute command with transcription as context
3. Result > 58 chars → save to file, upload
4. Return: "已生成内容，下载链接：https://..."

## Notes

- **Audio formats**: WAV, PCM, MP3 (16kHz, 16-bit, mono recommended)
- **Max duration**: 5 hours
- **Language support**: Chinese, English, 202+ Chinese dialects
- **Result threshold**: 58 characters (configurable per implementation)
- **File location**: Saved to `~/.openclaw/workspace/` before upload
