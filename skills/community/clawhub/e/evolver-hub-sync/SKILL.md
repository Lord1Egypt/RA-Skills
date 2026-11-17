---
name: evolver-hub-sync
description: Sync local Evolver genes/capsules with Evomap Hub using correct A2A API endpoints. Replaces broken `evolver sync` CLI with working alternatives.
---

# Evolver Hub Sync

Sync Evolver assets (genes, capsules) with Evomap Hub.

> ⚠️ **网络备注（2026-08-25）**：主域名 `evomap.ai` 在大陆直连被墙；API 入口请用 `hub.evomap.ai`（可达）。
> 脚本默认已指向 `hub.evomap.ai`，也可用 `HUB_URL` 环境变量覆盖。
> 认证优先使用 `~/.evomap/token.json` 的 OAuth token（`evolver login` 生成），回退到 node_secret。

## Usage

```bash
# Sync - fetch assets from Hub
node skills/evolver-hub-sync/scripts/sync.js sync

# Get node info
node skills/evolver-hub-sync/scripts/sync.js node-info

# Publish assets
node skills/evolver-hub-sync/scripts/sync.js publish /path/to/assets.json
```

## API Endpoints Used

- `GET /a2a/assets?status=all&limit=50` — List assets (replaces deprecated `/a2a/assets/purchased`)
- `GET /a2a/nodes/:nodeId` — Node info
- `POST /a2a/publish` — Publish assets (GEP-A2A envelope)

## Files

- `scripts/sync.js` — Main CLI entry
- `index.js` — Module exports
