```markdown
---
name: potplayer
description: Use PotPlayer to play local or network audio/video files. Supports scenarios such as direct playback, playlist management, seek playback, fullscreen, subtitle loading, etc. Use this skill when the user asks to play videos, audio, anime, TV series, or movies.
---

# PotPlayer Player

Play local or network audio/video files using PotPlayer.

## Executable Path

```
C:\Program Files\DAUM\PotPlayer\PotPlayerMini64.exe
```

## Basic Playback

```powershell
# Play a single file
& "C:\Program Files\DAUM\PotPlayer\PotPlayerMini64.exe" "C:\Media\test.mp4"

# Play network streams (m3u8/http)
& "C:\Program Files\DAUM\PotPlayer\PotPlayerMini64.exe" "https://example.com/video.m3u8"

# Play multiple files (auto-added to playlist)
& "C:\Program Files\DAUM\PotPlayer\PotPlayerMini64.exe" "1.mp4" "2.mkv" "3.avi"
```

> Paths containing spaces or Chinese characters must be enclosed in double quotes.

## Common Parameters

### Playback Control

```powershell
# Start playback from specified time (seconds or hh:mm:ss.ms)
& "C:\Program Files\DAUM\PotPlayer\PotPlayerMini64.exe" "video.mp4" /seek=120
& "C:\Program Files\DAUM\PotPlayer\PotPlayerMini64.exe" "video.mp4" /seek=00:05:30.000

# Fullscreen playback
& "C:\Program Files\DAUM\PotPlayer\PotPlayerMini64.exe" "video.mp4" /fullscreen

# Set volume (0-100)
& "C:\Program Files\DAUM\PotPlayer\PotPlayerMini64.exe" "video.mp4" /volume=80

# Muted playback
& "C:\Program Files\DAUM\PotPlayer\PotPlayerMini64.exe" "video.mp4" /mute

# Auto-play last file
& "C:\Program Files\DAUM\PotPlayer\PotPlayerMini64.exe" /autoplay
```

### Playlist

```powershell
# ✅ Recommended: Add to existing instance's playlist (no new instance created)
& "C:\Program Files\DAUM\PotPlayer\PotPlayerMini64.exe" /add "video.mp4"

# Insert after current playing item
& "C:\Program Files\DAUM\PotPlayer\PotPlayerMini64.exe" /insert "video.mp4"

# Add to list sorted by name
& "C:\Program Files\DAUM\PotPlayer\PotPlayerMini64.exe" "D:\Movies\*.mp4" /sort

# Add to list in random order
& "C:\Program Files\DAUM\PotPlayer\PotPlayerMini64.exe" "D:\Movies\*.mp4" /randomize
```

### Window & Instance

```powershell
# Force new instance
& "C:\Program Files\DAUM\PotPlayer\PotPlayerMini64.exe" "video.mp4" /new

# Open in current instance
& "C:\Program Files\DAUM\PotPlayer\PotPlayerMini64.exe" "video.mp4" /current

# Start minimized
& "C:\Program Files\DAUM\PotPlayer\PotPlayerMini64.exe" "video.mp4" /min

# Start maximized
& "C:\Program Files\DAUM\PotPlayer\PotPlayerMini64.exe" "video.mp4" /max
```

### Subtitles & Configuration

```powershell
# Specify subtitle file
& "C:\Program Files\DAUM\PotPlayer\PotPlayerMini64.exe" "video.mp4" /sub="subtitle.srt"

# Load specified configuration preset
& "C:\Program Files\DAUM\PotPlayer\PotPlayerMini64.exe" "video.mp4" /config="PresetName"
```

### Devices & Recording

```powershell
# Open DVD
& "C:\Program Files\DAUM\PotPlayer\PotPlayerMini64.exe" /dvd

# Open webcam
& "C:\Program Files\DAUM\PotPlayer\PotPlayerMini64.exe" /cam

# Screen recording
& "C:\Program Files\DAUM\PotPlayer\PotPlayerMini64.exe" /cap
```

### Dialogs

```powershell
# Open file selection dialog
& "C:\Program Files\DAUM\PotPlayer\PotPlayerMini64.exe" /filedlg

# Open URL input dialog
& "C:\Program Files\DAUM\PotPlayer\PotPlayerMini64.exe" /urldlg

# Open folder selection dialog
& "C:\Program Files\DAUM\PotPlayer\PotPlayerMini64.exe" /folderdlg
```

## Common Scenario Examples

```powershell
# Anime: Fullscreen network stream playback
& "C:\Program Files\DAUM\PotPlayer\PotPlayerMini64.exe" "https://example.com/anime.m3u8" /fullscreen

# Resume from last position
& "C:\Program Files\DAUM\PotPlayer\PotPlayerMini64.exe" "movie.mkv" /seek=00:45:00

# Fullscreen with subtitles
& "C:\Program Files\DAUM\PotPlayer\PotPlayerMini64.exe" "movie.mkv" /fullscreen /sub="movie.ass"

# Batch play videos in folder (sorted)
& "C:\Program Files\DAUM\PotPlayer\PotPlayerMini64.exe" "D:\Movies\*.mp4" /sort

# Add to existing playlist (won't interrupt current playback)
& "C:\Program Files\DAUM\PotPlayer\PotPlayerMini64.exe" /add "next_episode.mp4"
```

## Notes

- Parameters are case-insensitive (`/Seek` and `/seek` are equivalent)
- Multiple parameters are separated by spaces, order generally doesn't matter
- Paths with special characters must be enclosed in double quotes
- The `/add` parameter avoids creating new instances and is recommended for continuous playback
- Supports network stream addresses such as m3u8, http, rtsp, etc.
```