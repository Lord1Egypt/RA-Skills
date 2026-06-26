---
name: admirarr
description: "Manage a Jellyfin/Plex + *Arr media server stack — check status, add content, monitor downloads, diagnose issues, restart services."
version: 1.0.0
metadata:
  openclaw:
    requires:
      bins:
        - admirarr
---

# Admirarr

CLI for self-hosted media server stacks. One binary, 26 commands, JSON output everywhere.

Install: `curl -fsSL https://get.admirarr.dev | sh`

## Commands

### Status & Diagnostics

```bash
admirarr status [-o json] [--live]     # Fleet dashboard — services, libraries, queues, disk
admirarr health [-o json]              # Health warnings from Radarr, Sonarr, Prowlarr
admirarr disk [-o json]                # Disk space breakdown
admirarr docker [-o json]              # Docker container status
admirarr doctor [-o json]              # 15 diagnostic categories, 34 checks
admirarr doctor --fix                  # Built-in fixes → AI agent for the rest
```

### Library

```bash
admirarr movies [-o json]             # Movie library with file status
admirarr shows [-o json]              # TV shows with episode counts
admirarr recent [-o json]             # Recently added (Jellyfin or Plex)
admirarr history [-o json]            # Watch history
admirarr missing [-o json]            # Monitored without files
admirarr requests [-o json]           # Seerr media requests
```

### Search & Add

```bash
admirarr search "<query>" [-o json]   # Search all Prowlarr indexers
admirarr find "<query>" [-o json]     # Search Radarr releases
admirarr add-movie "<query>"          # Interactive: search → pick → add to Radarr
admirarr add-show "<query>"           # Interactive: search → pick → add to Sonarr
```

### Downloads

```bash
admirarr downloads [-o json]          # Active qBittorrent torrents
admirarr downloads pause [hash|all]   # Pause torrents
admirarr downloads resume [hash|all]  # Resume torrents
admirarr downloads remove <hash> [--delete-files]
admirarr queue [-o json]              # Radarr + Sonarr import queues
```

### Indexers

```bash
admirarr indexers [-o json]           # Prowlarr indexer status
admirarr indexers setup               # Interactive indexer wizard
admirarr indexers add <name>          # Add an indexer
admirarr indexers remove <name>       # Remove an indexer
admirarr indexers test                # Test all indexer connectivity
admirarr indexers sync                # Sync indexers to config.yaml
```

### Quality Profiles

```bash
admirarr recyclarr                    # Recyclarr status
admirarr recyclarr sync [instance]    # Run Recyclarr sync
admirarr recyclarr verify             # Check quality profiles
admirarr recyclarr instances          # List configured instances
```

### Management

```bash
admirarr scan                         # Trigger media server library scan
admirarr restart <service>            # Restart a Docker container
admirarr logs <service>               # Recent logs
admirarr setup                        # Full setup wizard (12 phases)
admirarr migrate                      # Generate Docker Compose stack
```

## Services

**Default stack:** Jellyfin, Radarr, Sonarr, Prowlarr, qBittorrent, Gluetun, Seerr, Bazarr, FlareSolverr, Watchtower

**Optional:** Plex, Lidarr, Readarr, Whisparr, SABnzbd, Autobrr, Unpackerr, Recyclarr, Profilarr, Tdarr, Tautulli, Jellystat, Notifiarr, Maintainerr

Auto-detects media server (Jellyfin first, then Plex). Services detected via HTTP regardless of deployment method.

## Workflow Patterns

| Goal | Commands |
|---|---|
| Understand stack state | `status` → `doctor` → `health` |
| Fix an issue | `doctor -o json` → identify → `restart` / fix → `doctor` again |
| Add content | `movies -o json` (check exists) → `add-movie` → `downloads` → `queue` |
| Stuck downloads | `downloads -o json` → `queue -o json` → `health` → `doctor` |
| Missing content | `missing -o json` → `requests -o json` |

## Rules

- `-o json` when parsing output
- Confirm with user before `restart` or destructive actions
- Present data as clean tables, not raw JSON
- Never delete user files or media
- Never modify *Arr databases directly
