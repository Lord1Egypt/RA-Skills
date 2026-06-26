---
name: chord-analyzer
description: "Analyze music audio files to extract chord progressions, key signature, tempo, and song structure. Use when user wants to identify chords, analyze a song's harmony, or extract musical information from audio files (mp3, wav, m4a, etc.)."
homepage: https://github.com/librosa/librosa
metadata: { "openclaw": { "emoji": "🎸", "requires": { "bins": ["python3"], "pip": ["librosa", "numpy"] } } }
---

# Chord Analyzer Skill

Analyze music audio files to extract chord progressions, key signature, tempo, and song structure.

## When to Use

✅ **USE this skill when:**

- User wants to analyze a song's chords and harmony
- "What are the chords in this song?"
- "Analyze this audio file"
- "Extract the chord progression"
- "What key is this song in?"
- User provides an audio file path and asks for musical analysis

## When NOT to Use

❌ **DON'T use this skill when:**

- Only wants general music info (lyrics, artist) → use web search
- Wants to generate music → use music generation skills
- Needs professional-grade transcription → recommend specialized software (Chordify, Hookpad)
- Requires detailed instrument separation → use dedicated source separation tools

## Supported Formats

- **Audio**: mp3, wav, m4a, flac, ogg
- **Duration**: Works best for songs under 5 minutes

## Installation

First time use requires installing dependencies:

```bash
pip3 install librosa numpy scipy scikit-learn soundfile
```

## Usage

### Basic Analysis

```bash
# Analyze an audio file
python3 chord_analyzer.py

# Edit the script to change the audio path
# Default: /Users/chentiewen/Music/网易云音乐/example.mp3
```

### Script Integration

Copy the `chord_analyzer.py` script to your workspace and modify the `audio_path` variable:

```python
audio_path = "/path/to/your/song.mp3"
result = analyze_audio(audio_path)
```

## Output

The analyzer provides:

1. **Key Signature**: Detected musical key (e.g., C, F#m, G)
2. **Tempo**: Speed in BPM with rhythm classification
3. **Chord Progression**: Complete chord sequence with timestamps
4. **Chord Statistics**: Most frequently used chords
5. **Song Structure**: Intro/Verse/Outro segmentation (basic)

### Sample Output

```
调性: F#m
速度: 123.0 BPM
节奏: 快板 (Allegro)

和弦走向:
F#mdim → A → D → Bm → E → A → D → Bm → E ...

主要和弦:
  A: 15次 (20.3%)
  E: 14次 (18.9%)
  D: 12次 (16.2%)
```

## How It Works

1. **Load Audio**: Uses `librosa.load()` to read audio at 22.05kHz
2. **Extract Chroma**: Computes chroma features (pitch class profiles) using STFT
3. **Detect Key**: Analyzes chroma energy across all 12 keys (major + minor)
4. **Track Tempo**: Uses `librosa.beat.beat_track()` for tempo detection
5. **Analyze Chords**: Samples chroma at measure boundaries and matches against chord templates
6. **Merge & Simplify**: Combines consecutive identical chords

## Limitations

- **Accuracy**: Chord detection is approximated; not professional-grade
- **Complexity**: Struggles with heavily layered or distorted music
- **Structure**: Simple segmentation (not verse/chorus detection)
- **Melody**: Does not extract melodic lines or instrument parts
- **Chord Extensions**: Detects basic triads (major, minor, diminished), not 7th/9th chords

## For Complete Transcription

For professional music transcription, recommend:

- **Chordify**: https://chordify.net (online chord detection)
- **Hookpad**: https://www.hooktheory.com/hookpad (theory + chords)
- **MuseScore**: https://musescore.org (manual transcription)
- **Capo**: https://capoapp.com (slow down + chord detection)

## Notes

- Analysis takes ~10-30 seconds depending on song length
- Best results with clear, non-distorted audio
- Works best for pop/rock/folk styles with clear harmony
- Not suitable for atonal, experimental, or heavily percussive music
