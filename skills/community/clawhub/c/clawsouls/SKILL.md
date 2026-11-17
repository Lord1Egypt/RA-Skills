---
name: clawsouls
version: 0.6.8
description: Manage AI agent personas (Souls) for OpenClaw, Hermes Agent, ZeroClaw, and other agents that use Soul Spec workspace files (SOUL.md, IDENTITY.md, AGENTS.md). Installs/switches/restores persona files in the agent workspace, searches and publishes to the clawsouls.ai registry (network + token auth), optionally syncs encrypted agent memory via Git (explicit `sync`/`swarm` commands only), and detects the local agent platform. Use only when the user explicitly asks to manage personas — e.g. "install a soul", "switch persona to X", "list souls", "restore my previous soul", "publish my soul", or "login to clawsouls". Workspace-modifying and publishing actions should be confirmed with the user first.
---

# ClawSouls — AI Persona Manager

Manage Soul packages that define an AI agent's personality, behavior, and identity.

Souls use `owner/name` namespacing (e.g., `clawsouls/surgical-coder`, `TomLeeLive/my-soul`).

## Prerequisites

Ensure `clawsouls` CLI is available:

> 모든 명령은 `clawsouls@0.16.1` 로 버전을 고정한다 — 게시 후 도구 코드가 바뀌지 않게(ClawHub 보안 리뷰 지적, 2026-09-29). 새 CLI 를 쓰려면 이 스킬을 함께 올린다.

```bash
npx clawsouls@0.16.1 --version
```

If not installed, install globally:

```bash
npm install -g clawsouls
```

Current version: **v0.6.8**

## Commands

### Install a Soul

```bash
npx clawsouls@0.16.1 install clawsouls/surgical-coder
npx clawsouls@0.16.1 install clawsouls/surgical-coder --force       # overwrite existing
npx clawsouls@0.16.1 install clawsouls/surgical-coder@0.1.0         # specific version
```

80+ souls available. Browse all at https://clawsouls.ai

**Official souls** (owner: `clawsouls`):

- **Development:** code-reviewer, coding-tutor, debug-detective, api-architect, ml-engineer, sysadmin-sage, devops-veteran, gamedev-mentor, prompt-engineer, frontend-dev, backend-dev, mobile-dev, cloud-architect, database-admin, qa-engineer
- **Writing & Content:** tech-writer, storyteller, scifi-writer, copywriter, content-creator, journalist, poet, screenwriter, academic-writer
- **Professional:** data-analyst, project-manager, legal-advisor, startup-founder, hr-manager, marketing-strategist, sales-coach, product-manager
- **Education:** math-tutor, philosophy-prof, mentor-coach, science-tutor, history-prof, language-teacher, economics-tutor
- **Creative:** music-producer, ux-designer, chef-master, graphic-designer, video-editor, podcast-host, dungeon-master, game-designer
- **Lifestyle:** personal-assistant, fitness-coach, travel-guide, life-coach, meditation-guide, nutrition-advisor, productivity-guru, financial-planner
- **Science:** research-scientist, data-scientist
- **Security:** security-auditor
- **MBTI:** mbti-intj, mbti-intp, mbti-entj, mbti-entp, mbti-infj, mbti-infp, mbti-enfj, mbti-enfp, mbti-istj, mbti-isfj, mbti-estj, mbti-esfj, mbti-istp, mbti-isfp, mbti-estp, mbti-esfp
- **Special:** surgical-coder, korean-translator
- **General:** brad, minimalist

### Activate a Soul

```bash
npx clawsouls@0.16.1 use clawsouls/surgical-coder
```

- Automatically backs up current workspace files (SOUL.md, IDENTITY.md, AGENTS.md, HEARTBEAT.md, STYLE.md, examples/)
- Never overwrites USER.md, MEMORY.md, or TOOLS.md
- Requires gateway restart to take effect

### Restore Previous Soul

```bash
npx clawsouls@0.16.1 restore
```

Reverts to the most recent backup created by `use`.

### List Installed Souls

```bash
npx clawsouls@0.16.1 list
```

Shows installed souls in `owner/name` format.

### Create a New Soul

```bash
npx clawsouls@0.16.1 init my-soul
```

Scaffolds a new soul directory with `soul.json`, SOUL.md, IDENTITY.md, AGENTS.md, HEARTBEAT.md, README.md.

### Export a Soul

```bash
npx clawsouls@0.16.1 export claude-md           # generate CLAUDE.md from current workspace soul files
npx clawsouls@0.16.1 export system-prompt       # generate a system prompt string
```

Combines SOUL.md, IDENTITY.md, AGENTS.md, HEARTBEAT.md, STYLE.md into a single file. Useful for Claude Code, Cursor, Windsurf, and other tools that use a single config file.

### Version Management

```bash
npx clawsouls@0.16.1 version bump patch    # 1.0.0 → 1.0.1
npx clawsouls@0.16.1 version bump minor    # 1.0.0 → 1.1.0
npx clawsouls@0.16.1 version bump major    # 1.0.0 → 2.0.0
npx clawsouls@0.16.1 diff                  # colored diff of soul files
```

### Soul Testing (Phase 9)

```bash
npx clawsouls@0.16.1 test                  # Level 1 (schema) + Level 2 (soulscan)
npx clawsouls@0.16.1 test --level 3       # + Level 3 (behavioral LLM tests)
```

Level 3 requires `soul.test.yaml` in the soul directory and an LLM provider (OpenAI/Anthropic/Ollama).

### Doctor, Migrate, Search, Info, Update (Phase 10)

```bash
npx clawsouls@0.16.1 doctor                # 12 environment checks
npx clawsouls@0.16.1 migrate               # migrate soul from v0.3 → v0.4 → v0.5
npx clawsouls@0.16.1 search "engineer"     # search souls from registry
npx clawsouls@0.16.1 info clawsouls/brad  # show soul metadata
npx clawsouls@0.16.1 update                # update installed soul to latest
```

### Validate a Soul

```bash
npx clawsouls@0.16.1 validate ./my-soul/
npx clawsouls@0.16.1 validate --soulscan ./my-soul/   # with SoulScan security analysis
npx clawsouls@0.16.1 check ./my-soul/                 # alias
```

Validates against the spec: schema, required files. Add `--soulscan` for full security & quality analysis with scoring. Also runs automatically before publish.

### SoulScan — Security & Integrity Scanner

```bash
npx clawsouls@0.16.1 soulscan              # scan current OpenClaw workspace
npx clawsouls@0.16.1 soulscan ./my-soul/   # scan a specific directory
npx clawsouls@0.16.1 soulscan --init       # initialize baseline checksums
npx clawsouls@0.16.1 soulscan -q           # quiet mode for cron (SOULSCAN_OK / SOULSCAN_ALERT)
npx clawsouls@0.16.1 scan                  # alias
```

SoulScan checks active soul files for:

- **Integrity**: SHA-256 checksum comparison — detects tampering since last scan
- **Security**: 53 pattern checks (prompt injection, code execution, XSS, data exfiltration, privilege escalation, social engineering, harmful content, secret detection)
- **Quality**: File structure, content length, schema validation
- **Persona Consistency**: Cross-validates name/tone across SOUL.md, IDENTITY.md, soul.json

**Cron usage** — periodic tamper detection:

```bash
# Run every hour to monitor workspace integrity
npx clawsouls@0.16.1 soulscan -q
# Exit code 0 = OK, 1 = alert (tampered or security issue)
```

**First run**: Use `--init` to establish baseline checksums without triggering alerts.

SOULSCAN™ — Score: 0-100, Grades: Verified (90+) / Low Risk (70+) / Medium Risk (40+) / High Risk / Blocked

### Publish a Soul

```bash
export CLAWSOULS_TOKEN=<token>
npx clawsouls@0.16.1 publish ./my-soul/
```

Publishes to `username/soul-name` namespace automatically. Requires authentication token. Runs validation automatically before publishing — blocks on failure.

### Login / Get Token

```bash
npx clawsouls@0.16.1 login
```

Instructions to get API token: Sign in at https://clawsouls.ai → Dashboard → Generate API Token.

## Workflow

### Installing & Switching Personas

1. **Browse** — Check available souls at https://clawsouls.ai or suggest from the categorized list above
2. **Install** — `npx clawsouls@0.16.1 install clawsouls/surgical-coder`
3. **Activate** — `npx clawsouls@0.16.1 use clawsouls/surgical-coder`
4. **Restart** — Run `soulclaw gateway restart` to apply the new persona
5. **New Session** — Send `/new` in chat to clear previous persona context from conversation history
6. **Restore** — If they want to go back, `npx clawsouls@0.16.1 restore`

### Publishing a Soul

1. **Login** — `npx clawsouls@0.16.1 login` → get token from dashboard
2. **Set token** — `export CLAWSOULS_TOKEN=<token>`
3. **Create** — `npx clawsouls@0.16.1 init my-soul` → edit files
4. **Publish** — `npx clawsouls@0.16.1 publish ./my-soul/`
5. **Manage** — Dashboard at https://clawsouls.ai/dashboard (delete, view downloads)

### Memory Sync (Swarm)

```bash
npx clawsouls@0.16.1 sync                  # sync encrypted memory to/from GitHub
npx clawsouls@0.16.1 swarm                 # multi-agent memory branch & merge system
```

Sync agent memory across machines via encrypted Git. Uses `age` encryption for local-first privacy.

### Soul Checkpoints (Rollback)

```bash
npx clawsouls@0.16.1 checkpoint            # manage soul checkpoints
npx clawsouls@0.16.1 checkpoint create     # create a checkpoint of current soul state
npx clawsouls@0.16.1 checkpoint list       # list available checkpoints
npx clawsouls@0.16.1 checkpoint restore    # restore from a checkpoint
```

Checkpoint-based rollback for persona contamination detection and recovery.

### Platform Detection

```bash
npx clawsouls@0.16.1 platform              # show detected agent platform(s) and workspace path
npx clawsouls@0.16.1 detect                # alias
```

Detects which agent platform is running (OpenClaw, SoulClaw, ZeroClaw, Hermes Agent, etc.) and shows workspace paths. If detection misses your platform, run soul commands from inside the agent workspace directory — souls are plain Soul Spec files, so any workspace that reads SOUL.md works.

## Platform Notes

| Platform | Workspace | Apply changes |
|---|---|---|
| OpenClaw / SoulClaw | agent workspace dir | `soulclaw gateway restart` + `/new` |
| Hermes Agent | Hermes workspace (reads SOUL.md / AGENTS.md natively; imports OpenClaw layouts) | restart the Hermes session, then start a new chat |
| ZeroClaw | workspace dir (OpenClaw-style markdown via IdentityConfig) | see `ZEROCLAW_ADAPTER.md` |

Hermes details: `HERMES_ADAPTER.md` in this repo.

## MCP Server (for Claude Desktop / Cowork)

For Claude Desktop or Cowork users, there's also a dedicated MCP server:

```bash
npx -y soul-spec-mcp@0.6.0
```

Or add to Claude Desktop config (`claude_desktop_config.json`):

```json
{ "mcpServers": { "soul-spec": { "command": "npx", "args": ["-y", "soul-spec-mcp@0.6.0"] } } }
```

6 tools: `search_souls`, `get_soul`, `install_soul`, `preview_soul`, `list_categories`, `apply_persona`

GitHub: https://github.com/clawsouls/soul-spec-mcp

## Security & Privacy Disclosure

Full transparency on what this skill can touch — review before use in workspaces containing sensitive prompts, memories, or client data.

**What this skill does:**
- **Local file changes**: `use`/`restore`/`checkpoint` replace persona files (SOUL.md, IDENTITY.md, AGENTS.md, HEARTBEAT.md, STYLE.md) in the agent workspace. An automatic backup is created before every `use`. USER.md, MEMORY.md, TOOLS.md are never overwritten.
- **Network calls**: `install`/`search`/`info`/`update` talk to the clawsouls.ai registry. `publish` uploads your soul directory to a public registry.
- **Memory sync (opt-in only)**: `sync`/`swarm` move agent memory to/from a Git remote you configure, encrypted locally with `age` before leaving the machine. These commands never run implicitly — only on explicit user request.
- **Platform detection**: `platform`/`detect` inspect the local environment to find the agent workspace path. Nothing is transmitted.
- **Token handling**: `publish` uses `CLAWSOULS_TOKEN` (env var). Never echo it, commit it, or leave it in shell history.

**Ask the user before:**
- `use` — switching personas rewrites workspace identity files (routine requests like "change personality" should be confirmed once before files change)
- `publish` — uploads content publicly; list the files being uploaded first
- `sync`/`swarm` — pushes (encrypted) memory to a remote

**Safety recommendations:** keep backups enabled (default), use `soulscan` to verify soul integrity after installs, and only install souls from owners you trust.

## Important Notes

- After `use`, always remind the user to run `soulclaw gateway restart` **and then `/new`** to start a fresh session (old conversation history retains the previous persona's identity)
- The `use` command creates automatic backups — data loss is unlikely
- Souls may include STYLE.md and examples/ for enhanced persona customization
- Published souls appear at `https://clawsouls.ai/souls/owner/name`
- Users can leave reviews (1-5 stars) on any soul they don't own
- For custom registry (local testing), set env: `CLAWSOULS_CDN=/path/to/souls`
- Website available in 5 languages: English, Korean, Japanese, Chinese, Spanish (e.g., `clawsouls.ai/ko/souls/...`)
- Share any soul to your OpenClaw bot: the install command is included in the share text
- **The Soul Thesis** — Read the manifesto: https://clawsouls.ai/en/manifesto
- **Research paper** — "Soul-Driven Interaction Design": https://doi.org/10.5281/zenodo.18772585
- Legal: [Privacy Policy](https://clawsouls.ai/en/privacy) · [Terms of Service](https://clawsouls.ai/en/terms)
