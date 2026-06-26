# Publish Notes

## Suggested ClawHub metadata
- slug: `douyin-video-analysis`
- name: `Douyin Video Analysis`
- version: `0.1.0`
- changelog: `Initial release: capture Douyin metadata/audio, transcribe, summarize, critically analyze, and save into Obsidian.`

## Requires
- macOS with Google Chrome
- browser automation bridge skill/scripts available
- temporary write access to `/tmp/douyin_transcribe/`
- Python venv support
- local `mlx-whisper` install in the temp venv during runtime
- Obsidian vault at the configured BobVault path

## Important limits
- Some Douyin media URLs may still fail if anti-bot protections change
- Transcript quality depends on the selected Whisper model
- Final critical analysis still expects human/agent judgment rather than pure automation
