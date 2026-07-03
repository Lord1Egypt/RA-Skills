# Known Pitfalls & Solutions

Comprehensive list of issues encountered during AI science video production,
with root causes and verified fixes.

---

## 1. F5-TTS Chinese Generation Too Short

**Severity:** P0 (blocks entire pipeline)

**Symptom:** F5-TTS MLX generates audio that is only 0.5-0.9 seconds per sentence,
regardless of text length. Chinese text is completely unusable.

**Root Cause:** The `estimate_duration` parameter is not set. Without it, the model
has no information about the target duration and generates the minimum possible output.

**Fix:**
```python
audio = generate(
    text=long_chinese_text,
    ref_audio_path=ref_path,
    ref_audio_text=ref_text,
    steps=64,
    cfg_strength=2.5,
    speed=1.0,
    estimate_duration=True,  # ← THIS IS THE FIX
)
```

**Verification:** After adding the parameter, the model estimates the target duration
(e.g., 19.08s for ~80 characters) and generates approximately correct-length audio
(e.g., 11.98s actual). Use `atempo` to fine-tune the remaining mismatch.

**Post-fix adjustment:**
```bash
# If actual=11.98s, target=10.0s → atempo = 11.98/10.0 = 1.198
ffmpeg -i generated.wav -filter:a "atempo=1.198" output.wav
```

---

## 2. Alpha Channel Compositing: White Circle, No Human

**Severity:** P0

**Symptom:** After `alphamerge` with circular mask, the PiP area shows only a white
circle. The digital human is not visible at all.

**Root Cause:** The `alphamerge` filter parameters are reversed — the mask is used as
the color source, and the human video's alpha is used as the alpha channel. Since the
mask has no color data, the output is white.

**Fix — Correct filter order:**
```bash
ffmpeg -i content.mp4 -i human.mp4 -i mask.png \
  -filter_complex "
    [1:v]scale=120:120,format=rgba[ov_rgba];
    [ov_rgba][2:v]alphamerge[ov_circle];     # ← human RGBA FIRST, mask SECOND
    [0:v][ov_circle]overlay=20:H-h-20:shortest=1[vout]
  "
```

The human video RGBA (`[ov_rgba]`) is the color source for `alphamerge`.
The circular mask PNG (`[2:v]`) provides the alpha channel. The filter merges:
- Color from input 0 (human RGBA)
- Alpha from input 1 (circular mask)

---

## 3. Concat Format Mismatch: Silent Segments

**Severity:** P0

**Symptom:** After `ffmpeg concat` of intro + content + outro, some segments play
with no audio. No error message from FFmpeg.

**Root Cause:** The segments have different audio formats:
- Intro: 48000Hz stereo (from Google Flow output)
- Content: 16000Hz mono (from SadTalker/Pillow rendering)
- Outro: 48000Hz stereo (from Google Flow output)

FFmpeg concat demuxer silently fails on format mismatch, producing silent output
for the incompatible segment.

**Fix — Unify all segments before concatenation:**
```bash
# Re-encode each segment to unified format
for seg in intro.mp4 content.mp4 outro.mp4; do
  ffmpeg -i "$seg" \
    -c:v libx264 -crf 20 \
    -c:a aac -ar 48000 -ac 2 -b:a 192k \
    "unified_${seg}"
done

# Now concatenate
ffmpeg -f concat -safe 0 -i concat_list.txt -c copy final.mp4
```

---

## 4. Subtitle Style Inconsistency (Intro vs Outro)

**Severity:** P1

**Symptom:** Intro subtitles use Pillow-rendered karaoke-style (word-by-word orange
highlight), but outro subtitles use ASS format with different colors and no highlight
animation. The visual inconsistency is noticeable.

**Root Cause:** Two different rendering engines were used:
- Intro: Pillow frame-by-frame PNG rendering (correct, looks great)
- Outro: ASS subtitle format with FFmpeg subtitles filter (requires libass, not
  available on macOS FFmpeg builds)

When libass is unavailable, FFmpeg silently falls back to basic text rendering
that ignores ASS style tags.

**Fix — Always use Pillow for all subtitles:**
1. Abandon ASS format entirely
2. Render intro AND outro subtitles with the same Pillow script
3. Use identical parameters (font, size, colors, background, animation style)
4. Verify 7 style properties match exactly (see qa_checklist.md, Section 7)

**Style properties that must match:**
- Rendering engine: Pillow (both)
- Font: STHeiti Medium 44px
- Spoken color: #FF6B2B (orange)
- Unspoken color: #FFFFFF (white)
- Outline: 2px black
- Background: rgba(0,0,0,160)
- Display mode: Per-sentence with word-by-word highlight

---

## 5. AI-Generated Background Music Gaps

**Severity:** P1

**Symptom:** At ~1:20 into the outro, there's a 2-second "noise" or "click" sound.
On detailed analysis, it's actually the background music suddenly cutting out and
coming back.

**Root Cause:** Google Flow's AI-generated video includes background music with
inherent silence gaps. The gaps are:
- 366ms at 7.78s
- 119ms at 8.86s
- 106ms at 9.65s

When music cuts out abruptly and comes back, the sudden amplitude change is
perceived as a "click" or "pop."

**Fix — Smooth each gap with crossfades:**
```python
# For each gap > 80ms:
# 1. Extract audio before gap
# 2. Apply 250ms fade-out ending at gap start
# 3. Extract audio after gap
# 4. Apply 250ms fade-in starting at gap end
# 5. Concatenate: before_fade + after_fade
```

```bash
# Single-gap fix example (gap at 7.78s, duration 366ms)
ffmpeg -i audio.wav \
  -filter_complex "
    [0:a]atrim=0:7.78,afade=t=out:st=7.53:d=0.25[part1];
    [0:a]atrim=8.146,afade=t=in:d=0.25[part2];
    [part1][part2]concat=n=2:v=0:a=1
  " fixed.wav
```

**Detection:** Use `scripts/audio_analyzer.py` to automatically find gaps.
Threshold: any silence >80ms with amplitude < -60dB.

---

## 6. Audio Channel Imbalance (Right Channel Dropout)

**Severity:** P1

**Symptom:** Crunching/crackling noise in one channel, or the right channel
periodically drops to near-zero amplitude while left channel is normal.

**Root Cause:** The source audio has an unstable right channel that flickers
between normal and near-silent 20+ times. This is a defect in the source video's
audio track.

**Fix — Duplicate left channel to both channels:**
```bash
ffmpeg -i input.wav -af "channelmap=map=FL-FL|FL-FR" -ar 48000 -ac 2 output.wav
```

This maps the left channel (FL) to both output channels (FL and FR), eliminating
the unstable right channel entirely.

**Why not downmix to mono?** Downmixing to mono (`-ac 1`) causes codec mismatch
when concatenating with stereo segments later (intro/outro are stereo). The
channelmap approach preserves stereo format.

---

## 7. Alimiter Parameter Compatibility

**Severity:** P2 (technical)

**Symptom:** `alimiter` filter rejects certain parameter combinations with
opaque error messages.

**Root Cause:** FFmpeg `alimiter` has version-dependent parameter validation.
Some builds reject `attack` and `release` parameters but accept `limit`.

**Fix — Minimal alimiter invocation:**
```bash
# Working: only specify limit
ffmpeg -i input.mp4 -af "alimiter=limit=-0.9dB" output.mp4

# May fail on some FFmpeg builds:
# ffmpeg -i input.mp4 -af "alimiter=limit=-0.9dB:attack=0.1:release=0.2"
```

Start with only `limit`. Add `attack` and `release` only if the build accepts them.

---

## 8. Subtitle {} Bracket Artifacts

**Severity:** P2 (cosmetic)

**Symptom:** Subtitle text shows literal `{}` curly braces remnants from ASS
tag cleanup.

**Root Cause:** When cleaning ASS-style tags from text, regex `re.sub(r'\{[^}]*\}',
'', text)` might leave behind unmatched braces or partial tags.

**Fix — Aggressive cleanup before rendering:**
```python
import re

def clean_text(text):
    # Remove ASS tags: {\xxx}
    text = re.sub(r'\{[^}]*\}', '', text)
    # Remove any remaining isolated braces
    text = text.replace('{', '').replace('}', '')
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text).strip()
    return text
```

---

## 9. Wrong TTS Audio Source for PiP

**Severity:** P1

**Symptom:** Picture-in-picture segment has degraded audio quality or stereo
imbalance compared to other segments.

**Root Cause:** The SadTalker output video contains a re-encoded 16000Hz AAC audio
track. Using SadTalker's audio as the PiP audio source degrades quality and may
introduce right-channel artifacts.

**Fix — Always use the original audio source:**
```bash
ffmpeg -i content_video.mp4 -i sadtalker_output.mp4 \
       -i content_audio.wav -i circle_mask.png \
  -filter_complex "..." \
  -map "[vout]" -map 2:a \    # ← Map audio from content_audio.wav (input #2),
  ...                          #   NOT from SadTalker output (input #1)
```

---

## Summary Table

| # | Issue | Severity | Detection | Fix Complexity | Recurrence Risk |
|---|-------|----------|-----------|----------------|-----------------|
| 1 | F5-TTS too short | P0 | Audio length < 1s per sentence | Low (add parameter) | High (easy to forget) |
| 2 | Alpha compositing reversed | P0 | White circle in PiP | Low (swap inputs) | Medium |
| 3 | Concat format mismatch | P0 | Silent segments after concat | Medium (re-encode all) | High (different sources) |
| 4 | Subtitle style mismatch | P1 | Visual comparison | Medium (unify engine) | Medium |
| 5 | BGM silence gaps | P1 | Audio analysis / ear | Medium (crossfade per gap) | Medium (AI-generated BGM) |
| 6 | Channel imbalance | P1 | Crackling in right channel | Low (channelmap) | Medium (source defect) |
| 7 | Alimiter params | P2 | FFmpeg error | Low (use minimal params) | Low |
| 8 | Bracket artifacts | P2 | Visible {} in subtitles | Low (regex cleanup) | Low |
| 9 | Wrong audio source | P1 | Degraded PiP audio quality | Low (remap audio input) | Medium |
