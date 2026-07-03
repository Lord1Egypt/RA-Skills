# Professional QA Review Checklist

## Overview

Run this checklist systematically after final compositing and before delivery.
Each dimension has specific inspection criteria and verification methods.

---

## 1. Video Transitions

**Goal:** No jarring hard cuts between segments.

| Check | Method | Pass Criteria |
|-------|--------|---------------|
| Intro→Content transition | Extract frames around transition point, view sequentially | Smooth fade, no visible jump |
| Content→Content transitions | Same as above | 0.5s xfade applied, colors blend naturally |
| Content→Outro transition | Same as above | No abrupt scene change |

**Inspection command:**
```bash
# Extract transition zone (0.3s before/after)
ffmpeg -i output.mp4 -ss <transition_time-0.3> -t 0.6 -vf fps=6 trans_frames/frame_%02d.png
```

---

## 2. Video Encoding Quality

**Goal:** Consistent encoding quality across all segments.

| Check | Method | Pass Criteria |
|-------|--------|---------------|
| Bitrate consistency | `ffprobe` each segment's bitrate | All within ±20% of median |
| Resolution | `ffprobe` width/height | All 1280×720 |
| Frame rate | `ffprobe` r_frame_rate | All exactly 24/1 |
| Codec | `ffprobe` codec_name | All libx264 |

**Inspection command:**
```bash
ffprobe -v error -select_streams v:0 \
  -show_entries stream=codec_name,width,height,r_frame_rate,bit_rate \
  output.mp4
```

---

## 3. Audio Artifacts

**Goal:** Zero audible artifacts — no noise, pops, clicks, or silence gaps.

| Check | Method | Pass Criteria |
|-------|--------|---------------|
| Noise/pops | Second-by-second peak analysis | No isolated peaks >3× mean |
| Silence gaps | Gap detection (threshold: >50ms below -60dB) | Zero gaps >80ms |
| Overall level | RMS normalization check | Consistent loudness across segments |

**Inspection command:**
```bash
python3 scripts/audio_analyzer.py output.mp4
```

---

## 4. Audio Transitions

**Goal:** Smooth audio joins between all segments.

| Check | Method | Pass Criteria |
|-------|--------|---------------|
| acrossfade applied | Check segment boundaries | 0.5s acrossfade at each join |
| No volume jumps | Compare RMS before/after boundary | < 3dB difference |
| No phase cancellation | Stereo correlation check at joins | Correlation > 0.5 |

---

## 5. Audio Clipping

**Goal:** No digital clipping anywhere in the audio track.

| Check | Method | Pass Criteria |
|-------|--------|---------------|
| Peak detection | Scan all samples for max absolute value | Peak < 32000 (16-bit) / < -0.9dB |
| Limiter active | Verify alimiter in FFmpeg filter chain | `alimiter=limit=-0.9dB` in command |
| Margin check | Headroom at loudest moment | > 1dB headroom |

**Danger threshold:** Any sample with absolute value > 32000 (out of 32768) is at risk.
Immediate action: increase alimiter limit or reduce source volume.

---

## 6. Subtitle Synchronization

**Goal:** Subtitles perfectly aligned with spoken audio.

| Check | Method | Pass Criteria |
|-------|--------|---------------|
| Word timing | Whisper transcription → compare timestamps | All words within ±100ms of audio |
| Sentence boundaries | Verify start/end of each subtitle sentence | Matches audio sentence boundaries |
| No orphan frames | Check for subtitle frames with no audio | Zero orphan frames |

**Verification command:**
```bash
whisper model small --language zh --word_timestamps True output.mp4
# Compare word timestamps with rendered subtitle frames
```

---

## 7. Subtitle Visual Consistency

**Goal:** Intro and outro subtitles are visually identical.

| Property | Intro Value | Outro Value | Match? |
|----------|-------------|-------------|--------|
| Rendering engine | Pillow | Pillow | ✓/✗ |
| Font | STHeiti Medium | STHeiti Medium | ✓/✗ |
| Font size | 44px | 44px | ✓/✗ |
| Spoken color | #FF6B2B | #FF6B2B | ✓/✗ |
| Unspoken color | #FFFFFF | #FFFFFF | ✓/✗ |
| Outline | 2px black | 2px black | ✓/✗ |
| Background bar | rgba(0,0,0,160) | rgba(0,0,0,160) | ✓/✗ |
| Display mode | Per-sentence | Per-sentence | ✓/✗ |
| Highlight mode | Word-by-word | Word-by-word | ✓/✗ |

All 8 properties must match. Any mismatch = P0 issue, must fix.

---

## 8. Pronunciation Accuracy

**Goal:** All Chinese pronunciation is correct and natural.

| Check | Method | Pass Criteria |
|-------|--------|---------------|
| Whisper cross-check | Transcribe with Whisper, compare to script | 100% character match (after correction mapping) |
| Technical terms | Manual spot-check of domain terms | All correctly pronounced |
| Proper names | Check personal/organization names | All correctly pronounced |

**Correction mapping:**
Maintain a dictionary of known Whisper mis-transcriptions and verify against it:
```python
corrections = {
    "材领": "才林",
    "Anthropy": "Anthropic",
    "Cloud Code": "Claude Code",
    "RT能徵": "AI智能",
    "自然圓眼": "自然语言",
}
```

---

## Issue Severity Classification

| Level | Definition | Examples | Action |
|-------|-----------|----------|--------|
| P0 | Must fix | Audio clipping, subtitle sync off, wrong pronunciation, visual inconsistency | Block delivery |
| P1 | Should fix | Awkward transition timing, minor loudness variation, suboptimal font rendering | Fix before delivery if time permits |
| P2 | Nice to have | Slightly suboptimal color balance, minor aesthetic preference | Note for next iteration |

**Delivery criteria:** P0 = 0, P1 ≤ 2.

---

## Post-Review Actions

1. Create issue list sorted by severity (P0 → P1 → P2)
2. For each issue, note: segment, timestamp, description, root cause, fix method
3. Apply P0 fixes immediately and re-verify
4. Rebuild with incremented version number (e.g., v11 → v12)
5. Re-run full checklist on new version
6. When P0=0 and P1≤2: deliver final version
