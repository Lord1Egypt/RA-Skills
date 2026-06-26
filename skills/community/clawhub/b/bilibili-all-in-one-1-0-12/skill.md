---
name: bilibili-all-in-one
description: >
  A comprehensive Bilibili toolkit that integrates hot trending monitoring,
  video downloading, video watching/playback, subtitle downloading,
  and video publishing capabilities into a single unified skill.
  Supports Bilibili session cookie authentication for publishing and
  high-quality downloads. Requests go to official Bilibili API endpoints
  and YouTube oEmbed API (for YouTube stats) over HTTPS.
version: 1.0.12
type: code
implementation: python
interface: cli-and-api
runtime: python>=3.8
languages:
  - zh-CN
  - en
tags:
  - bilibili
  - video-download
  - hot-trending
  - subtitle
  - danmaku
  - video-publish
  - video-player
  - youtube-stats
  - batch-download
  - multi-format
author: wscats
license: MIT
homepage: https://github.com/wscats/bilibili-all-in-one
repository: https://github.com/wscats/bilibili-all-in-one
entry_point: main.py
required_env_vars:
  - BILIBILI_SESSDATA
  - BILIBILI_BILI_JCT
optional_env_vars:
  - BILIBILI_BUVID3
install: pip install -r requirements.txt
---

# Bilibili All-in-One Skill

A comprehensive Bilibili toolkit that integrates hot trending monitoring, video downloading, video watching/playback, subtitle downloading, and video publishing capabilities into a single unified skill.

> **⚠️ Required Environment Variables:** `BILIBILI_SESSDATA`, `BILIBILI_BILI_JCT` (required), `BILIBILI_BUVID3` (optional)
> These are sensitive Bilibili session cookies needed for authenticated operations (publishing, high-quality downloads).
> Features that do NOT require authentication: hot monitoring, standard-quality downloads, subtitle listing, danmaku, stats viewing.
>
> **📦 Install:** `pip install -r requirements.txt` (all standard PyPI packages: httpx, bilibili-api-python, aiohttp, beautifulsoup4, lxml, requests)
>
> **🔗 Source:** [github.com/wscats/bilibili-all-in-one](https://github.com/wscats/bilibili-all-in-one)

---
### 何时激活

当用户说出或暗示以下内容时，本 Skill 会被激活：

| 触发场景 | 匹配的模块 | 典型触发词 |
|---|---|---|
| 查看B站热门、热搜、排行榜、必看榜 | 🔥 Hot Monitor | "热门"、"热搜"、"排行"、"趋势"、"必看"、"流行"、"榜单" |
| 下载B站视频、提取音频、批量下载 | ⬇️ Downloader | "下载"、"保存视频"、"提取音频"、"导出MP4"、"批量下载" |
| 查看视频播放量、点赞数、数据追踪、对比 | 👀 Watcher | "播放量"、"点赞"、"数据"、"统计"、"对比"、"监控"、"追踪"、"观看量" |
| 下载字幕、转换字幕格式、合并字幕 | 📝 Subtitle | "字幕"、"CC"、"SRT"、"ASS"、"字幕下载"、"字幕转换"、"翻译" |
| 播放视频、获取弹幕、播放列表 | ▶️ Player | "播放"、"弹幕"、"播放地址"、"分P"、"播放列表"、"danmaku" |
| 上传视频、发布、定时发布、草稿、编辑、删除 | 📤 Publisher | "上传"、"发布"、"投稿"、"定时发布"、"草稿"、"编辑视频"、"删除视频" |
| 涉及YouTube视频数据查询 | 👀 Watcher | "YouTube"、"油管"、"YTB"、"YouTube观看量" |
| 提及B站链接或BV号 | 自动识别 | `BV*`、`bilibili.com/video/*`、`b23.tv/*` |

> 💡 **提示**：只要用户消息中包含 B站/Bilibili 相关操作意图，或包含 BV 号、bilibili 链接，本 Skill 即会被自动激活。无需显式声明调用。

---

## Features
| Module | Description |
|---|---|
| 🔥 **Hot Monitor** | Monitor Bilibili hot/trending videos and topics in real-time |
| ⬇️ **Downloader** | Download Bilibili videos with multiple quality and format options |
| 👀 **Watcher** | Watch and track video engagement metrics (supports Bilibili & YouTube) |
| 📝 **Subtitle** | Download and process subtitles in multiple formats and languages |
| ▶️ **Player** | Get playback URLs, danmaku (bullet comments), and playlist info |
| 📤 **Publisher** | Upload, schedule, edit, and manage videos on Bilibili |

## Installation

### Requirements

- Python >= 3.8
- ffmpeg (optional, for merging video/audio streams)

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Dependencies

- `httpx >= 0.24.0`
- `bilibili-api-python >= 16.0.0`
- `aiohttp >= 3.8.0`
- `beautifulsoup4 >= 4.12.0`
- `lxml >= 4.9.0`
- `requests >= 2.31.0`

## Configuration

Some features (downloading high-quality videos, publishing, etc.) require Bilibili authentication. You can provide credentials in three ways:

### 1. Environment Variables

```bash
export BILIBILI_SESSDATA="your_sessdata"
export BILIBILI_BILI_JCT="your_bili_jct"
export BILIBILI_BUVID3="your_buvid3"
```

### 2. Credential File

Create a JSON file (e.g., `credentials.json`):

```json
{
  "sessdata": "your_sessdata",
  "bili_jct": "your_bili_jct",
  "buvid3": "your_buvid3"
}
```

### 3. Direct Parameters

Pass credentials directly when initializing:

```python
from main import BilibiliAllInOne

app = BilibiliAllInOne(
    sessdata="your_sessdata",
    bili_jct="your_bili_jct",
    buvid3="your_buvid3",
)
```

> **How to get cookies:** Log in to [bilibili.com](https://www.bilibili.com), open browser DevTools (F12) → Application → Cookies, and copy the values of `SESSDATA`, `bili_jct`, and `buvid3`.

## ⚠️ Security & Privacy

### Credential Handling

This skill handles **sensitive Bilibili session cookies**. Please read the following carefully:

| Concern | Detail |
|---|---|
| **What credentials are needed?** | `SESSDATA`, `bili_jct`, `buvid3` — Bilibili browser cookies |
| **Which features require authentication?** | Publishing (upload/edit/delete/schedule/draft), downloading 1080p+/4K quality videos |
| **Which features work WITHOUT credentials?** | Hot monitoring, standard-quality downloads, subtitle listing, danmaku fetching, stats viewing |
| **Where are credentials sent?** | To official Bilibili API endpoints (`api.bilibili.com`, `member.bilibili.com`) over HTTPS. YouTube metadata uses `www.youtube.com/oembed` (no credentials sent) |
| **Are credentials persisted to disk?** | **NO** — unless you explicitly call `auth.save_to_file()`. Credentials stay in memory by default |
| **File permissions for saved credentials** | `0600` (owner read/write only) — restrictive by default |

### Best Practices

1. 🧪 **Use a test account** — Do NOT provide your primary Bilibili account cookies for evaluation/testing purposes.
2. 🔒 **Prefer in-memory credentials** — Pass credentials via environment variables or direct parameters rather than saving to a file.
3. 📁 **If you must save credentials** — Use `auth.save_to_file()` which creates files with `0600` permissions. Delete the file when no longer needed.
4. 🐳 **Run in isolation** — When possible, run this skill in an isolated container/environment and inspect network traffic.
5. 🌐 **Verify network traffic** — All HTTP requests go to Bilibili's official domains and YouTube oEmbed API only. You can verify by monitoring outbound connections.
6. ❌ **No exfiltration** — This skill does NOT send credentials to any third-party service, analytics endpoint, or telemetry server.

### Network Endpoints Used

| Domain | Purpose |
|---|---|
| `api.bilibili.com` | Video info, stats, hot lists, subtitles, danmaku, playback URLs |
| `member.bilibili.com` | Video publishing (upload, edit, delete) |
| `upos-sz-upcdnbda2.bilivideo.com` | Video file upload CDN |
| `www.bilibili.com` | Web page scraping fallback |
| `www.youtube.com` | YouTube video metadata via oEmbed API (no auth required) |

### Credential Requirement by Module

| Module | Auth Required? | Notes |
|---|---|---|
| 🔥 Hot Monitor | ❌ No | All public APIs |
| ⬇️ Downloader | ⚠️ Optional | Required only for 1080p+ / 4K quality |
| 👀 Watcher | ❌ No | Public stats APIs |
| 📝 Subtitle | ❌ No | Public subtitle APIs |
| ▶️ Player | ⚠️ Optional | Required for high-quality playback URLs |
| 📤 Publisher | ✅ **Required** | All operations need `SESSDATA` + `bili_jct` |

## Usage

### CLI

```bash
python main.py <skill_name> <action> [params_json]
```

### Python API

```python
import asyncio
from main import BilibiliAllInOne

app = BilibiliAllInOne()

async def demo():
    result = await app.execute("hot_monitor", "get_hot", limit=5)
    print(result)

asyncio.run(demo())
```

---

## Skills Reference

### 1. 🔥 Hot Monitor (`bilibili_hot_monitor`)

Monitor Bilibili hot/trending videos and topics in real-time. Supports filtering by category, tracking rank changes.

#### Actions

| Action | Description | Parameters |
|---|---|---|
| `get_hot` | Get popular/hot videos | `page`, `page_size` |
| `get_trending` | Get trending series/topics | `limit` |
| `get_weekly` | Get weekly must-watch list | `number` (week number, optional) |
| `get_rank` | Get category ranking videos | `category`, `limit` |

#### Supported Categories

`all`, `anime`, `music`, `dance`, `game`, `tech`, `life`, `food`, `car`, `fashion`, `entertainment`, `movie`, `tv`

#### Examples

```bash
# Get top 10 hot videos
python main.py hot_monitor get_hot '{"page_size": 10}'

# Get trending topics
python main.py hot_monitor get_trending '{"limit": 5}'

# Get this week's must-watch
python main.py hot_monitor get_weekly

# Get game category rankings
python main.py hot_monitor get_rank '{"category": "game", "limit": 10}'
```

```python
# Python API
result = await app.execute("hot_monitor", "get_hot", page_size=10)
result = await app.execute("hot_monitor", "get_rank", category="game", limit=10)
```

---

### 2. ⬇️ Downloader (`bilibili_downloader`)

Download Bilibili videos with support for multiple quality options, batch downloading, and format selection.

#### Actions

| Action | Description | Parameters |
|---|---|---|
| `get_info` | Get video information | `url` |
| `get_formats` | List available qualities/formats | `url` |
| `download` | Download a single video | `url`, `quality`, `output_dir`, `format`, `page` |
| `batch_download` | Download multiple videos | `urls`, `quality`, `output_dir`, `format` |

#### Quality Options

`360p`, `480p`, `720p`, `1080p` (default), `1080p+`, `4k`

#### Format Options

`mp4` (default), `flv`, `mp3` (audio only)

#### Examples

```bash
# Get video info
python main.py downloader get_info '{"url": "BV1xx411c7mD"}'

# List available formats
python main.py downloader get_formats '{"url": "BV1xx411c7mD"}'

# Download in 1080p MP4
python main.py downloader download '{"url": "BV1xx411c7mD", "quality": "1080p", "format": "mp4"}'

# Extract audio only
python main.py downloader download '{"url": "BV1xx411c7mD", "format": "mp3"}'

# Batch download
python main.py downloader batch_download '{"urls": ["BV1xx411c7mD", "BV1yy411c8nE"], "quality": "720p"}'
```

```python
# Python API
info = await app.execute("downloader", "get_info", url="BV1xx411c7mD")
result = await app.execute("downloader", "download", url="BV1xx411c7mD", quality="1080p")
```

---

### 3. 👀 Watcher (`bilibili_watcher`)

Watch and monitor Bilibili (and YouTube) videos. Track view counts, comments, likes, and other engagement metrics over time.

#### Actions

| Action | Description | Parameters |
|---|---|---|
| `watch` | Get detailed video information | `url` |
| `get_stats` | Get current engagement statistics | `url` |
| `track` | Track metrics over time | `url`, `interval` (minutes), `duration` (hours) |
| `compare` | Compare multiple videos | `urls` |

#### Supported Platforms

- **Bilibili**: `https://www.bilibili.com/video/BVxxxxxx` or `BVxxxxxx`
- **YouTube**: `https://www.youtube.com/watch?v=xxxxx` or `https://youtu.be/xxxxx`

#### Examples

```bash
# Get video details
python main.py watcher watch '{"url": "BV1xx411c7mD"}'

# Get current stats
python main.py watcher get_stats '{"url": "BV1xx411c7mD"}'

# Track views every 30 minutes for 12 hours
python main.py watcher track '{"url": "BV1xx411c7mD", "interval": 30, "duration": 12}'

# Compare multiple videos
python main.py watcher compare '{"urls": ["BV1xx411c7mD", "BV1yy411c8nE"]}'
```

```python
# Python API
details = await app.execute("watcher", "watch", url="https://www.youtube.com/watch?v=dQw4w9WgXcQ")
comparison = await app.execute("watcher", "compare", urls=["BV1xx411c7mD", "BV1yy411c8nE"])
```

---

### 4. 📝 Subtitle (`bilibili_subtitle`)

Download and process subtitles/CC from Bilibili videos. Supports multiple subtitle formats and languages.

#### Actions

| Action | Description | Parameters |
|---|---|---|
| `list` | List available subtitles | `url` |
| `download` | Download subtitles | `url`, `language`, `format`, `output_dir` |
| `convert` | Convert subtitle format | `input_path`, `output_format`, `output_dir` |
| `merge` | Merge multiple subtitle files | `input_paths`, `output_path`, `output_format` |

#### Supported Formats

`srt` (default), `ass`, `vtt`, `txt`, `json`

#### Supported Languages

`zh-CN` (default), `en`, `ja`, and other language codes available on the video.

#### Examples

```bash
# List available subtitles
python main.py subtitle list '{"url": "BV1xx411c7mD"}'

# Download Chinese subtitles in SRT format
python main.py subtitle download '{"url": "BV1xx411c7mD", "language": "zh-CN", "format": "srt"}'

# Download English subtitles in ASS format
python main.py subtitle download '{"url": "BV1xx411c7mD", "language": "en", "format": "ass"}'

# Convert SRT to VTT
python main.py subtitle convert '{"input_path": "./subtitles/video.srt", "output_format": "vtt"}'

# Merge subtitle files
python main.py subtitle merge '{"input_paths": ["part1.srt", "part2.srt"], "output_path": "merged.srt"}'
```

```python
# Python API
subs = await app.execute("subtitle", "list", url="BV1xx411c7mD")
result = await app.execute("subtitle", "download", url="BV1xx411c7mD", language="zh-CN", format="srt")
```

---

### 5. ▶️ Player (`bilibili_player`)

Play Bilibili videos with support for playback control, playlist management, and danmaku (bullet comments) display.

#### Actions

| Action | Description | Parameters |
|---|---|---|
| `play` | Get complete playback info | `url`, `quality`, `page` |
| `get_playurl` | Get direct play URLs | `url`, `quality`, `page` |
| `get_danmaku` | Get danmaku/bullet comments | `url`, `page`, `segment` |
| `get_playlist` | Get playlist/multi-part info | `url` |

#### Danmaku Modes

| Mode | Description |
|---|---|
| 1 | Scroll (right to left) |
| 4 | Bottom fixed |
| 5 | Top fixed |

#### Examples

```bash
# Get playback info
python main.py player play '{"url": "BV1xx411c7mD", "quality": "1080p"}'

# Get direct play URLs
python main.py player get_playurl '{"url": "BV1xx411c7mD", "quality": "720p"}'

# Get danmaku
python main.py player get_danmaku '{"url": "BV1xx411c7mD"}'

# Get playlist for multi-part video
python main.py player get_playlist '{"url": "BV1xx411c7mD"}'

# Get page 3 of a multi-part video
python main.py player play '{"url": "BV1xx411c7mD", "quality": "1080p", "page": 3}'
```

```python
# Python API
play_info = await app.execute("player", "play", url="BV1xx411c7mD", quality="1080p")
danmaku = await app.execute("player", "get_danmaku", url="BV1xx411c7mD")
playlist = await app.execute("player", "get_playlist", url="BV1xx411c7mD")
```

---

### 6. 📤 Publisher (`bilibili_publisher`)

Publish videos to Bilibili. Supports uploading videos, setting metadata, scheduling publications, and managing drafts.

> ⚠️ **Authentication Required**: All publisher actions require valid Bilibili credentials.

#### Actions

| Action | Description | Parameters |
|---|---|---|
| `upload` | Upload and publish a video | `file_path`, `title`, `description`, `tags`, `category`, `cover_path`, `dynamic`, `no_reprint`, `open_elec` |
| `draft` | Save as draft | `file_path`, `title`, `description`, `tags`, `category`, `cover_path` |
| `schedule` | Schedule future publication | `file_path`, `title`, `schedule_time`, `description`, `tags`, `category`, `cover_path` |
| `edit` | Edit existing video metadata | `bvid`, `title`, `description`, `tags`, `cover_path` |
| `delete` | Delete a video | `bvid` |

#### Upload Parameters

| Parameter | Type | Default | Description |
|---|---|---|---|
| `file_path` | string | *required* | Path to the video file |
| `title` | string | *required* | Video title (max 80 chars) |
| `description` | string | `""` | Video description (max 2000 chars) |
| `tags` | string[] | `["bilibili"]` | Tags (max 12, each max 20 chars) |
| `category` | string | `"171"` | Category TID |
| `cover_path` | string | `null` | Path to cover image (JPG/PNG) |
| `no_reprint` | int | `1` | 1 = original content, 0 = repost |
| `open_elec` | int | `0` | 1 = enable charging, 0 = disable |

#### Examples

```bash
# Upload and publish
python main.py publisher upload '{"file_path": "./video.mp4", "title": "My Video", "description": "Hello World", "tags": ["test", "demo"], "category": "171"}'

# Save as draft
python main.py publisher draft '{"file_path": "./video.mp4", "title": "Draft Video"}'

# Schedule publication
python main.py publisher schedule '{"file_path": "./video.mp4", "title": "Scheduled Video", "schedule_time": "2025-12-31T20:00:00+08:00"}'

# Edit video metadata
python main.py publisher edit '{"bvid": "BV1xx411c7mD", "title": "New Title", "tags": ["updated"]}'

# Delete a video
python main.py publisher delete '{"bvid": "BV1xx411c7mD"}'
```

```python
# Python API (authentication required)
app = BilibiliAllInOne(sessdata="xxx", bili_jct="xxx", buvid3="xxx")

result = await app.execute("publisher", "upload",
    file_path="./video.mp4",
    title="My Video",
    description="Published via bilibili-all-in-one",
    tags=["python", "bilibili"],
)
```

---

## Project Structure

```
bilibili-all-in-one/
├── skill.json              # Skill configuration & parameter schema
├── skill.md                # This documentation file
├── README.md               # Project README (Chinese)
├── LICENSE                  # MIT License
├── requirements.txt        # Python dependencies
├── .gitignore              # Git ignore rules
├── main.py                 # Entry point & unified BilibiliAllInOne class
├── src/
│   ├── __init__.py         # Package exports
│   ├── auth.py             # Authentication & credential management
│   ├── utils.py            # Shared utilities, API constants, helpers
│   ├── hot_monitor.py      # Hot/trending video monitoring
│   ├── downloader.py       # Video downloading
│   ├── watcher.py          # Video watching & stats tracking
│   ├── subtitle.py         # Subtitle downloading & processing
│   ├── player.py           # Video playback & danmaku
│   └── publisher.py        # Video uploading & publishing
└── tests/
    ├── __init__.py
    └── test_all_skill_examples.py  # Comprehensive unit tests
```

## Skill Origin

This skill integrates the functionality of the following individual skills into one unified toolkit:

| Original Skill | Source | Integrated Module |
|---|---|---|
| bilibili-hot-monitor | [Jacobzwj/bilibili-hot-monitor](https://clawhub.ai/Jacobzwj/bilibili-hot-monitor) | `hot_monitor` |
| bililidownloader | [caiyundc880518/bililidownloader](https://clawhub.ai/caiyundc880518/bililidownloader) | `downloader` |
| bilibili-youtube-watcher | [donnycui/bilibili-youtube-watcher](https://clawhub.ai/donnycui/bilibili-youtube-watcher) | `watcher` |
| bilibili-subtitle-download-skill | [DavinciEvans/bilibili-subtitle-download-skill](https://clawhub.ai/DavinciEvans/bilibili-subtitle-download-skill) | `subtitle` |
| bilibili-player | [e421083458/bilibili-player](https://clawhub.ai/e421083458/bilibili-player) | `player` |
| bilibili-video-publish | [Johnnyxu820/bilibili-video-publish](https://clawhub.ai/Johnnyxu820/bilibili-video-publish) | `publisher` |

## Response Format

All skill actions return a JSON object with a unified structure:

```json
{
  "success": true,
  "...": "action-specific fields"
}
```

On error:

```json
{
  "success": false,
  "message": "Error description"
}
```

## License

MIT
