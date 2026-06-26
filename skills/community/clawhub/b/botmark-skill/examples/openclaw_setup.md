# OpenClaw Setup

OpenClaw bots use BotMark as a **native skill** — no tool registration needed.

## How It Works

OpenClaw loads `SKILL.md` into the bot's context on every session start. The SKILL.md contains complete exec-based instructions: the bot uses `curl` for API calls and `python3` for the evaluation engine. No HTTP tool registration, no gateway restart, no SOUL.md modification.

## Quick Start (Recommended)

One command handles everything — install, register, and API Key configuration:

```bash
bash setup.sh
```

Or download and run directly:
```bash
curl -fsSL https://botmark.cc/skill/setup.sh | bash
```

The script will:
1. Detect your OpenClaw installation path
2. Copy skill files to `~/.openclaw/workspace/skills/botmark-skill/`
3. Prompt for your API Key (get one free at https://botmark.cc)
4. Save the Key to `openclaw.json` (OpenClaw native config)
5. Verify everything is ready

After running, start a new OpenClaw session and say "跑个分" or "benchmark".

## Alternative Installation Methods

### Method 1: Via ClawHub

```bash
clawhub install botmark-skill
```

Then configure your API Key (pick one):

**Option A** — Edit `~/.openclaw/openclaw.json` (recommended):
```json
{
  "skills": {
    "entries": {
      "botmark-skill": {
        "apiKey": "bm_live_xxxxx"
      }
    }
  }
}
```
OpenClaw automatically maps `apiKey` → `$BOTMARK_API_KEY` because SKILL.md declares `primaryEnv: "BOTMARK_API_KEY"`.

**Option B** — Set environment variable:
```bash
export BOTMARK_API_KEY=bm_live_xxxxx
```

**Option C** — Do nothing. The bot will ask for the Key on first use and save it automatically.

### Method 2: Via Skill URL

1. In your OpenClaw bot settings, add a skill from URL:
   ```
   https://botmark.cc/api/v1/bot-benchmark/skill?format=openclaw
   ```
2. Configure API Key (same options as above)

### Method 3: Manual Install

```bash
# Copy skill files
cp -r botmark-skill/ ~/.openclaw/workspace/skills/botmark-skill/

# Run setup for API Key configuration
bash ~/.openclaw/workspace/skills/botmark-skill/setup.sh
```

## API Key Resolution Order

The bot checks for API Key in this order (first non-empty wins):

| Priority | Source | How to configure |
|----------|--------|------------------|
| 1 | `$BOTMARK_API_KEY` env var | `openclaw.json` `skills.entries.apiKey` (auto-injected) or shell export |
| 2 | `.botmark_env` file | Auto-saved on first interactive setup |
| 3 | Interactive prompt | Bot asks owner, saves to `.botmark_env` for future sessions |

For most users, the first-use interactive prompt is the easiest — just say "跑个分" and the bot will guide you.

## What Gets Installed

| File | Purpose |
|------|---------|
| `SKILL.md` | Complete evaluation flow instructions — loaded by OpenClaw each session |
| `botmark_engine.py` | Local scoring engine — cached, auto-updated when version changes |
| `engine_meta.json` | Engine version metadata |
| `setup.sh` | One-command setup script |
| `.botmark_env` | Persisted API Key (created on first use, chmod 600) |

## Skill Loading in OpenClaw

OpenClaw scans skills from three directories (highest priority first):

1. `~/.openclaw/workspace/skills/` — workspace skills (per-project)
2. `~/.openclaw/skills/` — managed skills (shared, installed by ClawHub)
3. Bundled skills — shipped with OpenClaw

Skills are loaded on **every new session start**. No registration step needed — if `SKILL.md` is in the right directory, it's loaded automatically.

## Troubleshooting

| Problem | Solution |
|---------|----------|
| Skill not loading | Verify: `ls ~/.openclaw/workspace/skills/botmark-skill/SKILL.md` |
| API Key not found | Run `bash setup.sh` or set in `openclaw.json` |
| "python3 not found" | Install Python 3.8+ and ensure it's on PATH |
| Skill loads but evaluation fails | Check `openclaw skills list --eligible` for gating issues |

## For Non-OpenClaw Platforms

If you're using Coze, Dify, or other platforms that support HTTP tool registration, use `skill_openclaw.json` instead:
1. Download [`skill_openclaw.json`](../skill_openclaw.json)
2. Register the 4 HTTP tools from the file
3. Inject `evaluation_instructions` into the bot's system prompt

## Usage

Once installed, the bot's owner can say:
- "Run BotMark" / "benchmark" / "evaluate yourself" / "跑个分" / "测评"
- The bot handles everything automatically using exec (curl + python3)
