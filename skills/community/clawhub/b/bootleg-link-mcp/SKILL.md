---
name: Bootleg-Link MCP
version: 0.9.0
description: "MCP Server — YouTube/Qobuz/Beatport 下载 | CDJ-2000 兼容 MP3 (48kHz/320k CBR/JPEG封面) | Bootleg-Link Flow (Try Before Buy) | 20 MCP Tools | 断点续传 | 智能命名 | 播放列表分页 | bgutil PO Token"
metadata:
  openclaw:
    emoji: "🎵"
    os: ["linux", "darwin"]
    requires:
      bins: ["python3>=3.10", "ffmpeg", "node>=24"]
---

# Bootleg-Link MCP v0.9.0

Python MCP server for downloading music from YouTube, Qobuz, and Beatport. Outputs CDJ-2000 compatible MP3 (48kHz/320k CBR/JPEG cover). Features task queue with resume, concurrent downloads, and intelligent file naming.

## Architecture

Single-file Python MCP server (`src/server.py`) over stdin/stdout JSON-RPC 2.0.

- **Multi-source**: YouTube (yt-dlp), Qobuz (qobuz-dl), Beatport (Playwright + requests)
- **CDJ-2000 Format**: 48kHz/320k CBR MP3, JPEG cover (WebP→JPEG auto-convert), no video streams
- **Task Queue**: In-memory + SQLite persistence, auto-resume on restart
- **Parallel Download**: ThreadPoolExecutor with configurable workers (max 32)
- **Paged Playlist**: Flat extraction (100/page) for large channel downloads
- **Smart Naming**: `Artist - Title (Mix) [LABEL].mp3` with auto artist extraction from YouTube metadata
- **YouTube Auth**: Playwright + Xvfb stealth Chromium login, bgutil PO Token provider
- **Config**: `~/.bootleg-link-mcp/config.json` for paths, proxy, quality, concurrency

## MCP Tools (20)

### Download & Task Management
| Tool | Description |
|------|-------------|
| `submit_download_task` | Submit YouTube URL (channel/playlist/video/search) |
| `query_progress` | Query task progress (incl. outputDir, url) |
| `list_tasks` | List all tasks with status filter |
| `cancel_task` | Cancel pending/downloading task |
| `clear_completed` | Clear completed/failed/cancelled tasks |
| `clear_database` | Clear ALL tasks and videos |
| `get_queue_status` | Queue metrics (active, queued, total) |

### YouTube
| Tool | Description |
|------|-------------|
| `youtube_login` | Playwright stealth Google login |
| `youtube_auth_status` | Check cookie authentication |
| `youtube_logout` | Clear YouTube cookies |

### Qobuz
| Tool | Description |
|------|-------------|
| `qobuz_login` | Login to Qobuz |
| `qobuz_search` | Search tracks/albums/artists |
| `qobuz_download` | Download (MP3 320 / CD FLAC / Hi-Res 96k / 192k) |
| `qobuz_my_purchases` | List purchased/favorite tracks |

### Beatport
| Tool | Description |
|------|-------------|
| `beatport_login` | Playwright login to Beatport |
| `beatport_search` | Search Beatport catalog |
| `beatport_download` | Download owned tracks |

## Dependencies

- `yt-dlp>=2026.05.25` — YouTube extraction (with Node.js for JS challenge solving)
- `mutagen` — MP3 ID3 tag + cover art embedding
- `playwright` — Stealth browser login (optional, for YouTube/Beatport auth)
- `qobuz-dl` — Qobuz integration (optional)
- `bgutil-ytdlp-pot-provider` — PO Token for YouTube (auto-started)
- `ffmpeg` — Audio extraction + format conversion
- Python 3.10+, Node.js 24+

## Configuration

`~/.bootleg-link-mcp/config.json`:

```json
{
  "paths": {
    "outputDir": "/mnt/e/music",
    "dbPath": "~/.bootleg-link-mcp/bootleg-link.db"
  },
  "proxy": { "http": "http://proxy:port", "https": "http://proxy:port" },
  "download": { "maxConcurrent": 32, "quality": "320" }
}
```

## Smart Directory

When no `outputDir` is specified, auto-creates subdirectories under `paths.outputDir` from URL content:
- Search query `[TECHAWAY RECORDS]` → `outputDir/TECHAWAY RECORDS/`
- Channel `@ChannelName` → `outputDir/ChannelName/`

## Bootleg-Link Flow (Try Before Buy)

Core workflow: YouTube fast preview → test in set → mark favorites → one-click Beatport/Qobuz replacement with full ID3/cover/name preservation.
