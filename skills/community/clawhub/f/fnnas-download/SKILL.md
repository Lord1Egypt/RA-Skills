---
name: fnnas-download
description: Manage qBittorrent download tasks on 飞牛NAS - list torrents and add magnet links
tools: Bash
---

# NAS Download Manager

Manage download tasks on the user's 飞牛NAS using qBittorrent API.

## Usage

Execute the shell script at `~/.claude/skills/fnnas-download/nas-download.sh` with appropriate commands.

## Commands

### list
List download tasks. By default shows only incomplete downloads (progress < 100%).

```bash
~/.claude/skills/fnnas-download/nas-download.sh list
```

Add `-all` flag to show all tasks:

```bash
~/.claude/skills/fnnas-download/nas-download.sh list -all
```

### add
Add a new download task.

For magnet links:
```bash
~/.claude/skills/fnnas-download/nas-download.sh add 'magnet:?xt=...'
```

For torrent files:
```bash
~/.claude/skills/fnnas-download/nas-download.sh add /path/to/file.torrent
```

## Connection Details

- NAS Host: user@192.168.1.100
- Authentication: SSH key-based
- qBittorrent: Unix socket at /home/user/qbt.sock

## Configuration

Edit the variables at the top of `nas-download.sh`:
- `NAS_HOST`: SSH connection string (user@host)
- `QBT_SOCK`: Path to qBittorrent unix socket
- `QBT_PASSWORD`: qBittorrent WebUI password
