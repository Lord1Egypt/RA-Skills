---
name: AI Audio Processing Studio
slug: ai-audio-processing
description: AI驱动的全栈音频处理技能。覆盖语音转文字（多语言ASR）、文字转语音（TTS含情感控制）、音频降噪与修复、音乐信息检索（MIR）、自动混音与母带处理、播客制作流水线、实时翻译配音。支持Whisper/Bark/OpenVoice/Demucs等前沿模型，兼容DAW工作流（Ableton/Logic/Reaper）。
version: 1.0.0
author: ai-gaoqian
tags:
  - audio
  - speech
  - music
  - podcast
  - asr
metadata:
  openclaw:
    requires:
      - python>=3.10
      - ffmpeg
      - torch>=2.0
---

# AI Audio Processing Studio

AI-powered full-stack audio processing skill. Covers ASR, TTS, noise reduction, music analysis, auto-mixing, podcast production, and real-time dubbing.

## Core Modules

### 1. Speech-to-Text (ASR)
- Multi-language transcription (100+ languages via Whisper)
- Speaker diarization (identify who spoke when)
- Timestamp-aligned subtitles (SRT/VTT/ASS)
- Real-time streaming transcription
- Domain-specific vocabulary customization (medical/legal/tech)
- Punctuation and capitalization restoration

### 2. Text-to-Speech (TTS)
- Natural voice synthesis (Bark/OpenVoice/CosyVoice)
- Emotion control (happy, sad, angry, neutral, enthusiastic)
- Voice cloning from 10-second sample
- Multi-speaker dialog generation
- Speed and pitch adjustment
- Audiobook narration pipeline (chapter-aware)

### 3. Audio Restoration & Enhancement
- Noise reduction (stationary + non-stationary)
- De-click, de-clip, de-ess processing
- Reverb removal and room acoustics correction
- Audio upscaling (8kHz→48kHz via super-resolution)
- Old recording restoration (vinyl crackle, tape hiss)
- Voice isolation from background music

### 4. Music Information Retrieval (MIR)
- Beat/tempo detection and BPM analysis
- Key and chord recognition
- Instrument separation (vocals/drums/bass/other via Demucs)
- Music structure analysis (verse/chorus/bridge detection)
- Genre classification and mood tagging
- Melody extraction and MIDI transcription

### 5. Auto-Mixing & Mastering
- Automatic level balancing (LUFS normalization)
- EQ matching to reference tracks
- Dynamic compression optimization
- Stereo width enhancement
- Loudness compliance (Broadcast/Streaming: -14 LUFS, -23 LUFS, -16 LUFS)
- Multi-format export (WAV/FLAC/MP3/AAC/OGG)

### 6. Podcast Production Pipeline
```
Record → Transcribe → Edit by text → Mix & Master → Export
```
- Text-based audio editing (cut by deleting transcript)
- Intro/outro templating with dynamic content
- Ad-insertion point detection
- Show notes and chapter marker generation
- RSS feed generation for publishing

### 7. Real-time Translation Dubbing
- Speech→Translate→TTS pipeline
- Lip-sync timing adjustment
- Multi-track dubbing for multilingual content
- Voice preservation across translations (voice cloning)
- Subtitle burn-in with styling

## Supported Audio Formats
- Input: WAV, MP3, FLAC, AAC, OGG, M4A, WMA, AIFF, OPUS
- Output: WAV (24-bit/48kHz), FLAC, MP3 (320kbps), AAC, OGG

## Usage Examples

```yaml
# Transcribe meeting recording
action: transcribe
input: meeting_2026-06-13.wav
language: zh
speakers: 4
output: meeting_transcript.srt
diarization: true

# Podcast production
action: podcast_pipeline
input: raw_interview.wav
host_voice: host_profile.json
guest_voice: guest_sample.wav
intro_music: intro.mp3
output: episode_042_final.mp3
chapters: auto
show_notes: true
```
