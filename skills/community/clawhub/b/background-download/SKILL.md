---
name: background-download
description: Asynchronous background download with retry, status tracking via Ontology, notifications to original channel. Supports resume on broken connections.
author: hp
author_email: hansponddg@139.com
license: MIT
ontology:
  reads: [DownloadTask]
  writes: [DownloadTask]
  preconditions:
    - "DownloadTask.url must exist"
    - "DownloadTask.path must exist"
  postconditions:
    - "Created DownloadTask has status=pending"
---

# Background Download Skill

中文：后台异步下载技能
- 非阻塞下载，不占用主会话
- 支持断点续传，自动重试
- 通过 Ontology 跟踪状态
- 结果通知到原请求渠道

Asynchronous background file download with:
- Non-blocking: returns immediately to user, downloads in background
- Resumeable: uses curl/wget built-in continue (`-c`)
- Retry: configurable max retries (default 3)
- Status tracking: all tasks stored in Ontology knowledge graph
- Notification: sends completion/failure notification to **original channel**
- Housekeeping: heartbeat cleans up zombie tasks, archives old completed tasks

## Commands

### `start` - Start a new background download

```bash
python3 scripts/download.py start --title "Title" --url "https://example.com/file.zip" --path "/path/to/save/file.zip" --channel "feishu:direct:user_id" [--max-retries 3]
```

### `status` - Check download status by task id

```bash
python3 scripts/download.py status --id down_xxxxxxx
```

### `list` - List all download tasks filtered by status

```bash
python3 scripts/download.py list [--status pending|downloading|completed|failed|archived]
```

### `archive` - Archive old completed tasks

```bash
python3 scripts/download.py archive --days 7
```

### `cleanup-zombies` - Mark stale downloading tasks as failed

```bash
python3 scripts/download.py cleanup-zombies --hours 2
```

## Architecture

```
User requests download
  ↓
Create DownloadTask in Ontology (status=pending)
  ↓
Fork background download process, exit immediately (non-blocking)
  ↓
Background:
  Update status → downloading
  Loop:
    Download with curl -C - (resume)
    If success:
      Update status → completed
      Send notification to original channel
      Done
    If fail:
      retry_count += 1
      If retry_count < max_retries: wait 30s → retry
      Else:
        Update status → failed
        Send failure notification to original channel
        Done

Heartbeat daily:
  cleanup-zombies --hours 2
  archive --days 7
```

## Ontology Schema

See `references/schema.json` for DownloadTask definition.

Required properties:
- `title`: Human-readable download name
- `url`: Download URL
- `path`: Local path to save file
- `status`: pending|downloading|completed|failed|archived
- `retry_count`: Current number of retries
- `max_retries`: Maximum retries (usually 3)
- `created_by_channel`: Original channel identifier (`channel_type:channel_id:user_id`) for notification

## Usage Example

```python
# From another skill
from scripts.download import start_download
start_download(
    title="Obsidian Windows",
    url="https://github.com/obsidianmd/obsidian-releases/releases/download/v1.12.4/Obsidian-1.12.4.exe",
    path="/home/user/files/Obsidian.exe",
    channel="feishu:direct:ou_xxxxxxx",
    max_retries=3
)
```

## Notification

Completion/failure notifications are sent via `openclaw message send` to the original channel recorded in `created_by_channel`.

## Requirements

- `ontology` skill must be installed and initialized
- `curl` or `wget` available on system
