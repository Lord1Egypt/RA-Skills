---
name: youtube-download
description: Download YouTube videos, playlists, audio, thumbnails, metadata, and subtitles with yt-dlp. Use when you need to fetch media from YouTube URLs, choose video/audio quality or formats, save files locally, pass cookies for private or age-restricted videos, resume downloads, or ensure yt-dlp is installed and updated before downloading.
compatibility:
  tools:
    - bash
    - python
  dependencies:
    - yt-dlp
---

# YouTube Download

## Overview

Use `yt-dlp` for all YouTube downloads on Linux, macOS, and Windows. Before downloading, ensure `yt-dlp` exists and update it to the newest available version when possible.

Prefer the bundled helper. Resolve `<skill-dir>` to this skill folder and use the available Python command for the current platform:

```bash
python3 youtube-download/scripts/youtube_download.py "https://www.youtube.com/watch?v=VIDEO_ID"
```

Use `python3` on most Linux/macOS systems. Use `py -3` or `python` on Windows when that is the configured Python launcher.

The helper checks for `yt-dlp`, installs it with `<python> -m pip install --user -U yt-dlp` if missing, tries `yt-dlp -U`, falls back to pip upgrade when self-update is unavailable, then runs the download. If a pip-installed executable is not on `PATH`, the helper searches common per-user script directories and falls back to `python -m yt_dlp`.

## Workflow

1. Confirm the user provided a YouTube URL or ask for one.
2. Pick an output directory. Default to `youtube-downloads/` in the current working directory unless the user specifies another path.
3. Use the helper script for routine downloads so installation and updating are handled consistently.
4. Pass through any advanced `yt-dlp` options after `--`.
5. Report the output directory and the important downloaded filenames when finished.

## Common Commands

Download best video and audio:

```bash
python3 youtube-download/scripts/youtube_download.py "URL"
```

Download a playlist:

```bash
python3 youtube-download/scripts/youtube_download.py "PLAYLIST_URL" --playlist
```

Extract MP3 audio:

```bash
python3 youtube-download/scripts/youtube_download.py "URL" --audio --audio-format mp3
```

Save subtitles and thumbnail:

```bash
python3 youtube-download/scripts/youtube_download.py "URL" --subtitles --thumbnail
```

Use browser cookies for private, member-only, age-restricted, or region-sensitive videos:

```bash
python3 youtube-download/scripts/youtube_download.py "URL" --cookies-from-browser chrome
```

Pass extra `yt-dlp` flags:

```bash
python3 youtube-download/scripts/youtube_download.py "URL" -- --write-info-json --write-comments
```

## Notes

- `yt-dlp -U` can automatically update official standalone builds. Some package-managed installs disable self-update; use pip upgrade as the fallback.
- The helper is platform-neutral: it looks for `yt-dlp`, `yt-dlp.exe`, or `yt-dlp.cmd`, then checks user install paths such as Python `Scripts` on Windows and user `bin` directories on Linux/macOS.
- Avoid downloading copyrighted material unless the user has rights or permission.
- For login-required content, prefer `--cookies-from-browser` or `--cookies FILE` instead of asking the user for credentials.
- If YouTube rate limits or blocks the download, retry with cookies, a lower concurrency setting, or the user's requested proxy/VPN setup.
