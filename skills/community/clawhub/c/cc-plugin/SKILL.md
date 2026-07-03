---
metadata:
  author: es6kr
  version: "0.1.0"
name: cc-plugin
description: |
  Claude Code plugin lifecycle management.
  cache - clean old plugin cache versions (cleanup only — NOT for cache miss/error diagnosis) [cache.md],
  create - plugin authoring guide (structure, plugin.json, components) [create.md],
  dev-reflect - reflect a local dev source repo into the marketplace clone for testing before push [dev-reflect.md],
  hud - OMC HUD statusline configuration (omcHud elements, omcLabel toggle, wrapper sed fallback) [hud.md],
  marketplace - clone/list/update marketplace repos [marketplace.md],
  troubleshoot - cache miss / cache error / installation failures / cache sync / HUD diagnostics — ALL plugin errors route here [troubleshoot.md].
  "plugin", "marketplace", "plugin cache cleanup", "plugin install", "plugin not installed",
  "cache miss", "cache error", "plugin error", "load error", "reload errors",
  "marketplace clone", "marketplace update", "plugin troubleshoot",
  "dev reflect", "test before push",
  "HUD error", "OMC HUD", "omcHud", "omcLabel", "statusline", "[OMC#" triggers.
---

# Plugin

Claude Code plugin lifecycle management: create, install, update, cache, troubleshoot.

## Topics

| Topic | Description | Guide |
|-------|-------------|-------|
| cache | **Cleanup only** — clean old plugin cache versions and temp directories. **NOT for "cache miss" or load errors** — use troubleshoot instead | [cache.md](./cache.md) |
| create | Plugin authoring guide (structure, plugin.json, components) | [create.md](./create.md) |
| dev-reflect | Reflect a local dev source repo's plugin/skill changes into the registered marketplace clone for local testing before commit/push (helper: `scripts/dev-reflect.sh`) | [dev-reflect.md](./dev-reflect.md) |
| hud | OMC HUD statusline configuration: omcHud elements, omcLabel toggle, wrapper sed fallback, version compatibility | [hud.md](./hud.md) |
| marketplace | Clone, list, and update marketplace repositories | [marketplace.md](./marketplace.md) |
| troubleshoot | **All plugin errors** — cache miss, load errors, `/reload-plugins` errors, `/doctor` failures, installation failures, cache sync, HUD diagnostics | [troubleshoot.md](./troubleshoot.md) |

## Routing rule (HARD STOP)

| User says | Topic |
|-----------|-------|
| "cache miss", "cache error", "load error", "reload errors", "plugin not loading", "plugin not installed" | **troubleshoot** (NOT cache) |
| "cache cleanup", "old versions", "disk space", "remove temp_git_*" | cache |

`cache.md` only owns deletion of stale versions. Any diagnostic of "why isn't this plugin working" — including the literal phrase "cache miss" — routes to `troubleshoot.md`.

## Paths

```
Marketplaces: ~/.claude/plugins/marketplaces/
Cache:        ~/.claude/plugins/cache/<marketplace>/<plugin>/<version>/
```
