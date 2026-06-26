# Port Notes — game-ops-monitor

Originally created for Hermes Agent; adapted to be dual-platform compatible (Hermes + OpenClaw).

## Dual-Platform Compatibility

| Feature | OpenClaw | Hermes |
|---------|----------|--------|
| Metadata namespace | `openclaw` | `hermes` |
| Trigger mechanism | Slash commands (`/game-ops-monitor`) | Natural language skill matching |
| User config | EXTEND.md (YAML) | Environment variables / skill config |
| Tool interface | `AskUserQuestion` (batched) | `clarify` tool (one at a time) |

## Design Decisions

### 1. Dual metadata block

The SKILL.md includes BOTH `openclaw` and `hermes` metadata namespaces. This allows:
- OpenClaw agents to discover the skill via slash commands and `openclaw` tags
- Hermes agents to discover via natural language and `hermes` tags
- ClaWHub to index the skill properly for both platforms

### 2. Environment-based configuration

Instead of EXTEND.md (OpenClaw's user config approach), this skill uses environment variables:

```bash
SCOUTER_COLLECTOR_URL=http://<collector-ip>:6188
SCOUTER_OBJ_TYPE=Java
```

This is more portable and works with both:
- Hermes CronJobs (can inject env vars)
- OpenClaw CLI (can set env vars globally)

### 3. REST API only

No platform-specific notification channels stored directly in code. Notification workflows (Feishu, DingTalk) are handled by separate skills (`game-alert`) that are platform-specific. This skill focuses only on data collection and is notification-agnostic.

### 4. Shell-only implementation

All examples use `curl` and `jq` — standard tools available on any Linux/macOS system. No Python scripts, no npm dependencies. This maximizes portability.

## For ClaWHub Publication

### Required files for ClaWHub

```
skills/game-ops-monitor/
├── SKILL.md           # Main skill file (this repo)
├── PORT_NOTES.md      # This file
└── references/
    ├── scouter-deploy-guide.md   # Deployment guide
    ├── quickstart.md             # Quick start for new users
    └── alert-workflow.md         # Alert configuration guide
```

### ClaWHub metadata (in SKILL.md frontmatter)

```yaml
platforms: [linux, macos]
prerequisites:
  commands: [curl, jq]
  environment:
    - SCOUTER_COLLECTOR_URL
    - SCOUTER_OBJ_TYPE
```

## Syncing with upstream

If Scouter releases a new version with API changes:

1. Check release notes: https://github.com/scouter-project/scouter/releases
2. Update API endpoints in SKILL.md if changed
3. Update version number in frontmatter
4. Test against staging environment
