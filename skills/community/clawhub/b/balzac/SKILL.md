---
name: balzac
description: AI content platform CLI — create workspaces, manage SEO keywords, generate article suggestions, write articles, and publish to WordPress, Webflow, Wix, GoHighLevel, or webhooks.
homepage: https://developer.hirebalzac.ai
metadata: {"clawdbot":{"emoji":"✍️","requires":{"bins":["balzac"],"env":["BALZAC_API_KEY"]},"install":[{"id":"npm","kind":"npm","package":"balzac-cli","bins":["balzac"],"label":"Install Balzac CLI (npm)"}]}}
---

# Balzac CLI

AI-powered SEO content platform. Authenticate, create a workspace from any domain, and Balzac analyzes your site, generates keyword-driven article suggestions, writes SEO-optimized articles, and publishes them.

```bash
npm install -g balzac-cli
```

Get an API key: https://app.hirebalzac.ai/api_keys

## Setup

```bash
export BALZAC_API_KEY=bz_your_key_here
# Or: balzac auth login bz_your_key_here

balzac config set workspace <workspace-id>   # set default workspace
```

## Core Workflow

```bash
# 1. Create workspace from a domain
balzac workspaces create --domain https://myblog.com --wait
balzac config set workspace "$(balzac --json workspaces list | jq -r '.workspaces[0].id')"

# 2. Generate suggestions and accept one (5 credits)
balzac suggestions generate                          # costs 1 credit
sleep 30
balzac suggestions list --status proposed
balzac suggestions accept <suggestion-id>            # costs 5 credits

# 3. Or write directly from a topic (5 credits)
balzac write "How to use AI for content marketing" --wait

# 4. Export or publish
balzac articles export <id> --format markdown
balzac articles publish <id> --integration <integration-id>
```

## Commands

| Command | What it does |
|---------|-------------|
| `balzac workspaces list/create/get/delete` | Manage workspaces |
| `balzac keywords list/create/enable/disable` | Manage SEO keywords |
| `balzac suggestions list/generate/accept/reject` | AI article suggestions |
| `balzac briefings create --topic "..."` | Direct write instruction (5 cr) |
| `balzac write "topic" [--wait]` | Shortcut: briefing + optional wait |
| `balzac articles list/get/export/rewrite/publish` | Manage articles |
| `balzac articles regenerate-picture <id>` | New cover image (1 cr) |
| `balzac competitors list/add/remove` | Track competitor domains |
| `balzac links list/add/remove` | Reference links for articles |
| `balzac integrations list/create/get/reconnect` | Publishing integrations |
| `balzac settings get/update` | Workspace settings |
| `balzac tones list` | Available tones of voice |
| `balzac config set/get/reset` | CLI configuration |

## Credit Costs

| Action | Credits |
|--------|---------|
| Generate 10 suggestions | 1 |
| Write article (accept suggestion or create briefing) | 5 |
| Rewrite article | 3 |
| Regenerate picture | 1 |

## Key Notes

- Use `--json` flag for scriptable JSON output; pipe to `jq`.
- Use `-w <id>` or `balzac config set workspace <id>` for workspace-scoped commands.
- Article writing is async — use `write --wait` or poll `articles get <id>`.
- Workspace creation is async — use `--wait` flag.
- Supported integrations: WordPress, Webflow, Wix, GoHighLevel, Webhook.
- Run `balzac <command> --help` for full option details.
