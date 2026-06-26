---
name: senseaudio-audiobook-generator
description: Generate audiobooks from novels and long-form text with chapter management and character voices. Use when users mention audiobooks, narrating books, or converting lengthy written content to audio.
compatibility:
  required_credentials:
    - name: SENSEAUDIO_API_KEY
      description: API key from https://senseaudio.cn/platform/api-key
      env_var: API_KEY
homepage: https://senseaudio.cn
source: https://github.com/anthropics/skills
---

# SenseAudio Audiobook Generator

Convert novels, books, and long-form written content into professional audiobooks with natural narration and character voices.

## What This Skill Does

This skill helps you create audiobooks by:
- Converting long texts (novels, books, articles) into audio
- Automatically handling chapter divisions
- Supporting multiple character voices for dialogue
- Distinguishing between narration and character speech
- Managing long content with automatic chunking

## When to Use This Skill

Use this skill when you need to:
- Create audiobooks from novels or books
- Convert long-form articles to audio
- Generate narrated versions of written content
- Produce audio for e-learning materials
- Create accessible audio versions of text documents

## How It Works

### Basic Workflow

1. **Prepare the text** - Format with chapter markers and dialogue tags
2. **Configure narration** - Choose narrator voice and character voices
3. **Process chapters** - Generate audio for each chapter or section
4. **Combine audio** - Merge all segments into complete audiobook
5. **Add metadata** - Include chapter markers and timestamps

### Text Format

Structure your content like this:

```
# Chapter 1: The Beginning

[Narrator]
It was a dark and stormy night. The old mansion stood alone on the hill.

[Character: John, Voice: male_0004_a]
"I don't think we should go in there," John whispered nervously.

[Character: Sarah, Voice: female_0006_a]
"Don't be silly. It's just an old house."

[Narrator]
They pushed open the creaky door and stepped inside.
```

### Voice Configuration

**Narrator voice**: Choose a clear, neutral voice for narration
- Recommended: male_0004_a (calm male) or female_0027_a (clear female)
- Speed: 0.9-1.0 for comfortable listening
- Pitch: 0 (neutral)

**Character voices**: Assign distinct voices to each character
- Use different voice IDs for different characters
- Adjust pitch slightly to differentiate (+2/-2)
- Vary speed for character personality (excited: 1.1, calm: 0.9)

### Chapter Management

For long books, process by chapters:

```python
chapters = [
    {"title": "Chapter 1", "text": "...", "start_time": 0},
    {"title": "Chapter 2", "text": "...", "start_time": 1234},
    # ...
]
```

Benefits:
- Easier to manage and debug
- Allows chapter navigation in audio players
- Can resume generation if interrupted
- Enables parallel processing

## Implementation Steps

### Step 1: Parse and Structure Content

Extract structure from the text:
```python
import re

def parse_audiobook_text(text):
    sections = []
    current_section = {"type": "narrator", "text": "", "voice": "male_0004_a"}

    for line in text.split('\n'):
        # Chapter markers
        if line.startswith('# Chapter'):
            if current_section["text"]:
                sections.append(current_section)
            sections.append({"type": "chapter", "title": line[2:]})
            current_section = {"type": "narrator", "text": "", "voice": "male_0004_a"}

        # Narrator
        elif line.startswith('[Narrator]'):
            if current_section["text"]:
                sections.append(current_section)
            current_section = {"type": "narrator", "text": "", "voice": "male_0004_a"}

        # Character dialogue
        elif match := re.match(r'\[Character: (\w+), Voice: ([\w_]+)\]', line):
            if current_section["text"]:
                sections.append(current_section)
            current_section = {
                "type": "character",
                "character": match.group(1),
                "voice": match.group(2),
                "text": ""
            }

        else:
            current_section["text"] += line + " "

    if current_section["text"]:
        sections.append(current_section)

    return sections
```

### Step 2: Generate Audio Segments

For each section, call the TTS API:

```python
import requests
import binascii

def generate_audio_segment(text, voice_id, output_file, speed=1.0):
    url = "https://api.senseaudio.cn/v1/t2a_v2"
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "SenseAudio-TTS-1.0",
        "text": text,
        "stream": False,
        "voice_setting": {
            "voice_id": voice_id,
            "speed": speed,
            "vol": 1.0,
            "pitch": 0
        },
        "audio_setting": {
            "format": "mp3",
            "sample_rate": 32000,
            "bitrate": 128000,
            "channel": 2
        }
    }

    response = requests.post(url, headers=headers, json=payload)
    data = response.json()

    # Decode hex audio
    audio_hex = data['data']['audio']
    audio_binary = binascii.unhexlify(audio_hex)

    # Save to file
    with open(output_file, 'wb') as f:
        f.write(audio_binary)

    return data['extra_info']['audio_length']  # Duration in ms
```

### Step 3: Handle Long Text

Split long chapters into manageable chunks:

```python
def chunk_text(text, max_length=5000):
    """Split text at sentence boundaries"""
    sentences = re.split(r'([.!?]+\s+)', text)
    chunks = []
    current_chunk = ""

    for i in range(0, len(sentences), 2):
        sentence = sentences[i]
        separator = sentences[i+1] if i+1 < len(sentences) else ""

        if len(current_chunk) + len(sentence) + len(separator) > max_length:
            if current_chunk:
                chunks.append(current_chunk.strip())
            current_chunk = sentence + separator
        else:
            current_chunk += sentence + separator

    if current_chunk:
        chunks.append(current_chunk.strip())

    return chunks
```

### Step 4: Combine Audio Files

Merge all segments into a complete audiobook:

```python
from pydub import AudioSegment

def create_audiobook(segments, output_file, chapter_markers=None):
    audiobook = AudioSegment.empty()
    chapter_times = []
    current_time = 0

    for i, segment_file in enumerate(segments):
        # Load segment
        segment = AudioSegment.from_mp3(segment_file)

        # Check if this is a chapter start
        if chapter_markers and i in chapter_markers:
            chapter_times.append({
                "chapter": chapter_markers[i],
                "time": current_time
            })

        # Add segment
        audiobook += segment
        current_time += len(segment)

        # Add pause between segments (300ms)
        if i < len(segments) - 1:
            audiobook += AudioSegment.silent(duration=300)
            current_time += 300

    # Export with metadata
    audiobook.export(
        output_file,
        format="mp3",
        bitrate="128k",
        tags={
            "title": "Audiobook",
            "artist": "SenseAudio TTS",
            "album": "Generated Audiobook"
        }
    )

    return chapter_times
```

## Advanced Features

### Dialogue Enhancement

Make dialogue more natural:
- Add slight pauses before character speech: `<break time=200>`
- Vary character emotions based on context
- Use different pitch for different characters

### Narration Styles

Adjust narrator voice for different genres:
- **Fiction**: Slightly expressive (speed: 1.0, varied pitch)
- **Non-fiction**: Clear and steady (speed: 0.95, neutral pitch)
- **Children's books**: Animated (speed: 1.1, varied emotions)
- **Technical**: Slow and clear (speed: 0.9, neutral)

### Chapter Markers

Add ID3 tags for chapter navigation:
```python
from mutagen.mp3 import MP3
from mutagen.id3 import ID3, CHAP, TIT2, CTOCFlags

def add_chapter_markers(mp3_file, chapters):
    audio = MP3(mp3_file, ID3=ID3)

    # Add chapters
    for i, chapter in enumerate(chapters):
        audio.tags.add(
            CHAP(
                element_id=f"chp{i}",
                start_time=chapter["time"],
                end_time=chapters[i+1]["time"] if i+1 < len(chapters) else len(audio.info.length * 1000),
                sub_frames=[TIT2(text=chapter["chapter"])]
            )
        )

    audio.save()
```

### Progress Tracking

For long books, track progress:
```python
def generate_audiobook_with_progress(sections, output_dir):
    total = len(sections)
    completed = 0

    for i, section in enumerate(sections):
        output_file = f"{output_dir}/segment_{i:04d}.mp3"

        # Skip if already generated
        if os.path.exists(output_file):
            completed += 1
            continue

        # Generate audio
        generate_audio_segment(
            section["text"],
            section["voice"],
            output_file=output_file
        )

        completed += 1
        print(f"Progress: {completed}/{total} ({completed*100//total}%)")
```

## Error Handling

Common issues:

**Text too long**: Chunk into smaller segments (max 10,000 chars per request)

**Voice consistency**: Save voice mappings to ensure same character uses same voice

**Memory issues**: Process chapters separately, don't load entire book at once

**API rate limits**: Add delays between requests (e.g., 1 second)

## Output Format

The skill produces:
- Individual chapter audio files (MP3)
- Complete audiobook file (MP3)
- Chapter markers and timestamps (JSON)
- Metadata file with voice mappings and settings

## Example Usage

**User request**: "Convert this novel into an audiobook with different voices for each character"

**Skill actions**:
1. Parse the novel text and identify chapters
2. Extract character dialogue and assign voices
3. Generate audio for each section
4. Combine all audio with chapter markers
5. Export final audiobook with metadata
6. Provide playback instructions and chapter list

## Tips for Best Results

- Use consistent voice IDs for the same character throughout
- Add natural pauses between paragraphs and chapters
- Test a sample chapter before processing the entire book
- Keep narrator voice neutral and clear
- Use higher quality settings (44100 Hz) for final production
- Consider adding background ambience for immersive experience

## Reference

For detailed API documentation, see the SenseAudio TTS API reference in the `references/` directory.
