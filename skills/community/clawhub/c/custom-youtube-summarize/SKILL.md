---
name: custom-youtube-summarize
description: Extract transcript from a YouTube video using Python and summarize it.
---

## Description
Extracts subtitles from YouTube videos and generates summaries. Use when users provide YouTube URLs with requests like "summarize this video" or "explain this content".

## Setup
1. Create script at `{baseDir}/transcript_extract.py` with provided code
2. All libraries are already installed in the skills folder.
3. Therefore, no additional action is required to run Python files.

## Usage
When receiving a YouTube URL:
1. Executes: `python3 {baseDir}/transcript_extract.py "<YOUTUBE_URL>"`
2. Captures output between `[TRANSCRIPT-START]` and `[TRANSCRIPT-END]`
3. Uses LLM to generate summary from raw transcript text

## Configuration
```yaml
script_path: "{baseDir}/transcript_extract.py"
supported_languages: ["ko", "en"]
```

## Example
**Input:**  
`https://youtu.be/dQw4w9WgXcQ` (with "summarize this" context)
`https://youtu.be/M-S2ctyAeaY?si=PEYq7Uy8HA8bpUUv` 이 영상 요약해줘
다음 영상 요약 `https://youtu.be/M-S2cty`
Summarize `https://youtube.com/watch?v=ch4EsgfHOJc`
요약 `https://youtube.com/watch?v=ch4EsgfHOJc`
`https://youtube.com/watch?v=chgasgwHOJc` 이거 내용 뭐야?
`https://youtube.com/watch?v=qsnuQI62sda` Tell me the content of this video
Tell me the content of this video `https://youtube.com/watch?v=qsnuQI62sda`

**Output:**  
```markdown
[TRANSCRIPT-START]
Never gonna give you up, never gonna let you down...
[TRANSCRIPT-END]

This video contains the iconic Rickroll meme track by Rick Astley. The lyrics revolve around themes of loyalty and commitment, featuring the artist's signature bassline and 80s production style. Despite its simple lyrics, it remains one of YouTube's most enduring viral pranks.
```

## Notes
- Handles both manually created and auto-generated subtitles
- Falls back to English if Korean subtitles aren't available
- Returns error messages if no transcript exists or URL is invalid
```