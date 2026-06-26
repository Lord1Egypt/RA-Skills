---
name: audio-handler
description: Read, analyze, convert, and process audio files (MP3, WAV, FLAC, AAC, M4A, OGG, OPUS, WMA). Use when working with audio: extracting metadata, converting formats, trimming, merging, adjusting volume, or transcribing. Triggers on mentions of audio files, file paths with audio extensions, or requests to process/convert audio.
---

# Audio Handler

Analyze, convert, and process audio files.

## Supported Formats

| Format | Extensions | Read | Convert | Metadata |
|--------|------------|------|---------|----------|
| MP3 | .mp3 | ✅ | ✅ | ✅ |
| WAV | .wav | ✅ | ✅ | ✅ |
| FLAC | .flac | ✅ | ✅ | ✅ |
| AAC/M4A | .m4a, .aac | ✅ | ✅ | ✅ |
| OGG | .ogg | ✅ | ✅ | ✅ |
| Opus | .opus | ✅ | ✅ | ✅ |
| WMA | .wma | ✅ | ✅ | ✅ |
| AIFF | .aiff, .aif | ✅ | ✅ | ✅ |

## Quick Commands

### Metadata (ffprobe)

```bash
# Get all metadata
ffprobe -v quiet -print_format json -show_format -show_streams audio.mp3

# Get duration only
ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 audio.mp3

# Get bitrate
ffprobe -v error -show_entries format=bit_rate -of default=noprint_wrappers=1:nokey=1 audio.mp3

# Get sample rate and channels
ffprobe -v error -select_streams a:0 -show_entries stream=sample_rate,channels -of default=noprint_wrappers=1 audio.mp3

# Human-readable info
ffprobe -hide_banner audio.mp3
```

### Convert Formats (ffmpeg)

```bash
# Convert to MP3 (good quality)
ffmpeg -i input.wav -codec:a libmp3lame -qscale:a 2 output.mp3

# Convert to MP3 (specific bitrate)
ffmpeg -i input.wav -codec:a libmp3lame -b:a 192k output.mp3

# Convert to WAV (uncompressed)
ffmpeg -i input.mp3 output.wav

# Convert to FLAC (lossless)
ffmpeg -i input.wav output.flac

# Convert to M4A/AAC
ffmpeg -i input.wav -codec:a aac -b:a 256k output.m4a

# Convert to OGG Vorbis
ffmpeg -i input.wav -codec:a libvorbis -qscale:a 5 output.ogg

# Convert to Opus (best for speech)
ffmpeg -i input.wav -codec:a libopus -b:a 64k output.opus
```

### Trim & Clip

```bash
# Trim audio (from 30s to 90s)
ffmpeg -i input.mp3 -ss 30 -to 90 -c copy output.mp3

# Trim from start to duration
ffmpeg -i input.mp3 -t 60 -c copy output.mp3  # First 60 seconds

# Trim with re-encode (more accurate)
ffmpeg -i input.mp3 -ss 30 -to 90 output.mp3
```

### Volume & Speed

```bash
# Adjust volume (2x louder)
ffmpeg -i input.mp3 -af "volume=2" output.mp3

# Reduce volume (half)
ffmpeg -i input.mp3 -af "volume=0.5" output.mp3

# Normalize audio
ffmpeg -i input.mp3 -af "loudnorm" output.mp3

# Speed up (1.5x)
ffmpeg -i input.mp3 -af "atempo=1.5" output.mp3

# Slow down (0.75x)
ffmpeg -i input.mp3 -af "atempo=0.75" output.mp3
```

### Merge & Concatenate

```bash
# Concatenate audio files
ffmpeg -i "concat:part1.mp3|part2.mp3|part3.mp3" -acodec copy output.mp3

# Merge with file list
echo "file 'part1.mp3'" > list.txt
echo "file 'part2.mp3'" >> list.txt
ffmpeg -f concat -safe 0 -i list.txt -c copy output.mp3

# Mix two audio tracks
ffmpeg -i voice.mp3 -i music.mp3 -filter_complex amix=inputs=2:duration=longest output.mp3
```

### Extract Audio from Video

```bash
# Extract audio track
ffmpeg -i video.mp4 -vn -acodec copy audio.aac

# Extract and convert
ffmpeg -i video.mp4 -vn -acodec libmp3lame -b:a 192k audio.mp3
```

### Playback (macOS)

```bash
# Play audio file
afplay audio.mp3

# Play with volume (0.0 to 1.0)
afplay -v 0.5 audio.mp3

# Play in background
afplay audio.mp3 &

# Stop playback
killall afplay
```

### Text-to-Speech (macOS)

```bash
# Speak text
say "Hello, this is a test"

# Save to file
say -o output.aiff "This will be saved as audio"

# List voices
say -v ?

# Use specific voice
say -v "Samantha" "Hello, I am Samantha"

# Convert to MP3
say -o temp.aiff "Text to convert" && ffmpeg -i temp.aiff output.mp3 && rm temp.aiff
```

## Scripts

### audio_info.sh

Get comprehensive audio metadata.

```bash
~/Dropbox/jarvis/skills/audio-handler/scripts/audio_info.sh <audio_file>
```

### convert_audio.sh

Convert between formats with quality options.

```bash
~/Dropbox/jarvis/skills/audio-handler/scripts/convert_audio.sh <input> <output> [quality]
```

### trim_audio.sh

Trim audio with start/end times.

```bash
~/Dropbox/jarvis/skills/audio-handler/scripts/trim_audio.sh <input> <output> <start> <end>
```

### normalize_audio.sh

Normalize volume level.

```bash
~/Dropbox/jarvis/skills/audio-handler/scripts/normalize_audio.sh <input> <output>
```

## Quality Guide

| Use Case | Format | Settings |
|----------|--------|----------|
| Music archive | FLAC | `-codec:a flac` |
| Music portable | MP3 | `-codec:a libmp3lame -qscale:a 2` |
| Podcast/speech | Opus | `-codec:a libopus -b:a 64k` |
| Voice memo | M4A | `-codec:a aac -b:a 128k` |
| Uncompressed | WAV | `-codec:a pcm_s16le` |

## Notes

- `ffmpeg` handles almost all audio formats
- `-c copy` is fast but may be inaccurate for trimming
- Re-encode (`-af`) for precise cuts but takes longer
- Opus is best for speech at low bitrates
- Use `loudnorm` filter for consistent volume across files