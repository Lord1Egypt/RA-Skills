---
name: conversation-video
description: Generate animated conversation videos with multi-voice TTS audio and timed text overlays. Use when the user needs to (1) turn a transcript or dialogue into a video with synced subtitles, (2) create podcast-style conversation visuals, (3) produce customer discovery interview videos, (4) animate multi-speaker content with distinct voices and styling, or (5) generate any video where spoken text appears on screen with speaker labels.
---

# Conversation Video

Generate multi-voice conversation videos from text transcripts. Two paths: quick ffmpeg (no dependencies) or rich Remotion (React animations).

## Prerequisites

| Tool | Path / Notes |
|------|-------------|
| ffmpeg | System install or Jellyfin ffmpeg at `/usr/lib/jellyfin-ffmpeg/ffmpeg` |
| supertonic-tts | Python package for multi-voice TTS (see scripts/generate_audio.py for load logic) |
| Node.js + npm | Only needed for Remotion path |

## Workflow

### 1. Build a transcript manifest

Create a JSON file with your conversation:

```json
[
  {"speaker": "NARRATOR",   "text": "Customer Discovery Interview", "voice": "M1", "speed": 1.0, "align": "center"},
  {"speaker": "INTERVIEWER","text": "Walk me through when you first realized...", "voice": "M5", "speed": 0.95, "align": "left"},
  {"speaker": "CUSTOMER",   "text": "I was looking for a marketer agent.", "voice": "M2", "speed": 1.0, "align": "right"}
]
```

Fields: `speaker` (label), `text` (spoken text), `voice` (supertonic voice name e.g. M1-M5, F1-F2), `speed` (optional playback speed), `align` (left/right/center for video placement).

### 2. Generate audio + timing manifest

```bash
python scripts/generate_audio.py manifest.json output.wav
```

Outputs:
- `output.wav` — concatenated multi-voice audio
- `output_timings.json` — per-segment start/end times for video sync

### 3. Render video (choose path)

**Path A: ffmpeg — fast, no Node.js needed**

```bash
python scripts/ffmpeg_render.py output_timings.json output.wav video.mp4
```

Options: `--width`, `--height`, `--font-size`, `--bg`, `--font`, `--crf`

**Path B: Remotion — richer animations, React-based**

Copy the boilerplate:
```bash
cp -r assets/remotion-boilerplate ./my-video
cd my-video
npm install
```

Edit `src/Conversation.tsx`:
1. Replace `conversation` array with your lines (duration in frames, 30fps)
2. Set `SpeakerConfig` colors/alignment
3. Uncomment `<Audio src={staticFile("audio.wav")} />` and place audio in `public/`

Render:
```bash
npx remotion render src/index.ts Conversation out/video.mp4
```

## Speaker Customization

Default color/alignment map (edit in either ffmpeg or Remotion):

| Speaker | Color | Align |
|---------|-------|-------|
| NARRATOR | #cbd5e1 | center |
| INTERVIEWER | #60a5fa | left |
| CUSTOMER | #34d399 | right |

Add more by extending the config map in the respective renderer.

## Resources

- **scripts/generate_audio.py** — Multi-voice TTS with timing export
- **scripts/ffmpeg_render.py** — ffmpeg drawtext video renderer
- **assets/remotion-boilerplate/** — Copyable Remotion project template
- **references/remotion-patterns.md** — Advanced Remotion techniques (JSON data loading, word-by-word reveal, audio sync)
- **references/ffmpeg-guide.md** — ffmpeg drawtext syntax and timing reference
