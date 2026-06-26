# Output Format Specifications

Detailed documentation for all supported output formats.

## TXT Format

Plain text with inline timestamps and speaker labels.

### Format Structure

```
[HH:MM:SS.mmm] Speaker A: Transcribed text here.
[HH:MM:SS.mmm] Speaker B: Response text here.
[OVERLAP] [HH:MM:SS.mmm] Speaker A: Overlapping speech.
```

### Elements

- **Timestamp**: `[HH:MM:SS.mmm]` - Hours:Minutes:Seconds.milliseconds
- **Speaker**: `Speaker A`, `Speaker B`, etc.
- **Overlap marker**: `[OVERLAP]` prefix for overlapping speech

### Example

```
[00:00:01.234] Speaker A: Hello, welcome to the meeting.
[00:00:05.678] Speaker B: Thank you for joining today.
[OVERLAP] [00:00:10.123] Speaker A: Let's get started.
[00:00:10.456] Speaker B: Yes, let's begin.
```

---

## JSON Format

Structured JSON with full metadata including word-level timestamps and confidence scores.

### Format Structure

```json
[
  {
    "text": "Full segment text",
    "start": 1234,
    "end": 5678,
    "confidence": 0.95,
    "speaker_id": "Speaker A",
    "is_overlap": false,
    "words": [
      {
        "word": "Hello",
        "start": 1234,
        "end": 1500,
        "confidence": 0.98
      }
    ]
  }
]
```

### Fields

| Field | Type | Description |
|-------|------|-------------|
| text | string | Full segment text |
| start | integer | Start time in milliseconds |
| end | integer | End time in milliseconds |
| confidence | float | Segment confidence (0.0-1.0) |
| speaker_id | string | Speaker label (e.g., "Speaker A") |
| is_overlap | boolean | Whether segment overlaps with another |
| words | array | Word-level details |

### Word Object Fields

| Field | Type | Description |
|-------|------|-------------|
| word | string | Individual word |
| start | integer | Word start time (ms) |
| end | integer | Word end time (ms) |
| confidence | float | Word confidence (0.0-1.0) |

---

## SRT Format

SubRip subtitle format - standard for video subtitles.

### Format Structure

```
1
00:00:01,234 --> 00:00:05,678
[Speaker A] Hello, welcome to the meeting.

2
00:00:05,678 --> 00:00:10,123
[Speaker B] Thank you for joining today.
```

### Key Differences from TXT

- Uses **comma** for milliseconds: `00:00:01,234` (not period)
- Sequential numbering for each subtitle
- Arrow separator `-->` between start and end
- Speaker label in brackets at start of text

### Timestamp Format

`HH:MM:SS,mmm` where:
- HH = hours (2 digits)
- MM = minutes (2 digits)
- SS = seconds (2 digits)
- mmm = milliseconds (3 digits, comma-separated)

---

## ASS Format

Advanced SubStation Alpha - styled subtitles with speaker-specific colors.

### Format Structure

```
[Script Info]
Title: Transcription
ScriptType: v4.00+
PlayResX: 1920
PlayResY: 1080

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Default,Arial,16,&H00FFFFFF,&H000000FF,&H00000000,&H00000000,0,0,0,0,100,100,0,0,1,2,2,2,10,10,10,1
Style: SpeakerA,Arial,16,&H00FFFF,&H000000FF,&H00000000,&H00000000,0,0,0,0,100,100,0,0,1,2,2,2,10,10,10,1
Style: SpeakerB,Arial,16,&H00FFFF00,&H000000FF,&H00000000,&H00000000,0,0,0,0,100,100,0,0,1,2,2,2,10,10,10,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
Dialogue: 0,0:00:01.23,0:00:05.68,SpeakerA,,0,0,0,,Hello, welcome to the meeting.
Dialogue: 0,0:00:05.68,0:00:10.12,SpeakerB,,0,0,0,,Thank you for joining today.
```

### Speaker Colors

| Speaker | Color | Hex Code |
|---------|-------|----------|
| Speaker A | Yellow | `&H00FFFF` |
| Speaker B | Cyan | `&H00FFFF00` |
| Speaker C | Magenta | `&H00FF00FF` |
| Speaker D | Green | `&H0000FF00` |
| Speaker E | Orange | `&H0000A5FF` |

### Timestamp Format

`H:MM:SS.cc` where:
- H = hours (1 digit)
- MM = minutes (2 digits)
- SS = seconds (2 digits)
- cc = centiseconds (2 digits)

### Special Character Escaping

ASS requires escaping special characters:
- `\n` → `\N` (line break)
- `\` → `\\`

---

## Markdown Format

Speaker-grouped sections with timestamps.

### Format Structure

```markdown
## Speaker A

- [00:00:01] Hello, welcome to the meeting.
- [00:00:10] Let's get started.

## Speaker B

- [00:00:05] Thank you for joining today.
- [00:00:15] I agree, let's proceed.
```

### Elements

- **Speaker headers**: `## Speaker X`
- **List items**: `- [HH:MM:SS] Text`
- **Overlap marker**: `[OVERLAP]` prefix in text

### Speaker Ordering

Speakers are ordered by their first appearance in the audio.

### Timestamp Format

`[HH:MM:SS]` - Hours:Minutes:Seconds (no milliseconds)

---

## Comparison Table

| Feature | TXT | JSON | SRT | ASS | MD |
|---------|-----|------|-----|-----|-----|
| Timestamps | Yes | Yes | Yes | Yes | Yes |
| Speaker labels | Yes | Yes | Yes | Yes | Yes |
| Word-level data | No | Yes | No | No | No |
| Confidence scores | No | Yes | No | No | No |
| Overlap detection | Yes | Yes | No | No | Yes |
| Styling support | No | No | No | Yes | No |
| Video compatibility | No | No | Yes | Yes | No |

---

## Usage Examples

### Generate SRT for video

```bash
asr-skill video.mp4 -f srt
# Output: video.srt
```

### Generate ASS with speaker colors

```bash
asr-skill meeting.mp4 -f ass
# Output: meeting.ass (speakers in different colors)
```

### Generate JSON for analysis

```bash
asr-skill interview.mp3 -f json
# Output: interview.json (with word-level timestamps)
```

### Generate Markdown documentation

```bash
asr-skill podcast.mp3 -f md
# Output: podcast.md (speaker-grouped sections)
```
