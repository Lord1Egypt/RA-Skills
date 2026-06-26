# Workflow Notes

## Deterministic stages

These stages are script-friendly and should stay deterministic:

1. Resolve / download Bilibili video
2. Extract wav with ffmpeg
3. Run ASR
4. Upload mp4 and obtain public URL
5. Create / update Notion page properties
6. Write transcript blocks
7. Append markdown summary blocks
8. Cleanup temp files

## Agent-owned stages

These stages should remain under agent judgment:

1. Whether to replace an existing Notion page body
2. Whether transcript quality is acceptable
3. How to phrase the summary and outline
4. How much progress reporting the user needs
5. When to stop and ask for confirmation

## Failure handling

- Bilibili 412 / 403 → retry with cookies or fall back to local asset path
- No official subtitles → ASR fallback
- ASR too slow → report progress, do not stay silent
- Notion update path wrong → stop and fix write path before continuing
- Summary obviously based on wrong transcript → do not append it
