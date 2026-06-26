# Architecture Documentation

## Overview
The Douyin Download Skill follows a "Local-Heavy" architecture to ensure zero API costs and full control over transcription quality.

## Data Flow
1. **Input Parsing**: Any raw string input is parsed using regex to extract a valid `https://v.douyin.com` or `https://www.douyin.com` URL.
2. **Dynamic Redirection Handling**: Short-links are followed using lightweight HTTP requests.
3. **Playwright Navigation**: A Chromium instance navigates to a modified "Jingxuan" URL, which is less protected than the standard video landing page.
4. **Metadata Extraction**: SSR (Server-Side Rendering) data in `_ROUTER_DATA` or `RENDER_DATA` is parsed for the title, author, and audio URL.
5. **Transcription**:
   - If subtitles exist in the SSR data, they are returned immediately.
   - Otherwise, the audio file is downloaded and processed by a local Whisper `base` model.
6. **File Persistence**: A formatted Markdown file with YAML frontmatter is saved to the user's Obsidian directory.

## Dependencies
- `playwright`: Browser automation.
- `openai-whisper`: Local AI transcription.
- `requests`: Network utility.
- `aiohttp`: Async network utility.
- `ffmpeg`: Binary for audio processing (provided in `resources/`).
