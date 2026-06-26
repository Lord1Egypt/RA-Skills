**English** | [中文](README.zh-CN.md)

# Follow GitHub

> Your personalized GitHub digest — delivered daily or weekly, in your inbox or chat.

A skill that tracks three things and remixes them into a scannable summary:

1. **People you follow** — new repos they create, repos they star, releases from
   projects they maintain
2. **GitHub Trending** — what's hot on GitHub right now, optionally filtered by language
3. **Hot new projects** — recently-created repos picking up stars fast

All fetched **live** from the GitHub API and `github.com/trending`. No central
server, no third-party data pipeline — just your own token hitting GitHub directly.

Inspired by [follow-builders](https://github.com/zarazhangrui/follow-builders).

## Quick Start

For OpenClaw / ClawHub users:

```bash
openclaw skills install follow-github
```

Then start a conversation and say `配置 follow-github` or `set up follow-github`.

## What You Get

A daily or weekly digest, delivered in one of these ways depending on your setup:

- OpenClaw in-chat delivery
- Telegram bot message
- Email via Resend
- On-demand in the terminal

You can configure:

- Which streams to include: Following, Trending, Hot New Projects
- Which languages to filter for Trending / Hot
- Digest language: English, Chinese, or bilingual
- Delivery frequency, time, timezone, and channel

## Example Output

```markdown
# GitHub Digest — 2026-04-20

## From People You Follow

**karpathy**
- starred unslothai/unsloth — 2-5x faster LLM finetuning [Python] ★ 18.4k
- created karpathy/llm-c — LLM training in pure C [C]

3 people you follow starred anthropics/claude-cookbook
(starred by levie, simonw, swyx)

## Trending

- forrestchang/andrej-karpathy-skills — single CLAUDE.md for Claude Code
  [Markdown] +45k ★ this week
- NousResearch/hermes-agent — the agent that grows with you [Python] +38k ★

## Notable New Projects

- multica-ai/multica — open-source managed agents platform
  [TypeScript] ★ 17.2k (created 9 days ago)
```

Language, tone, section order, and filters are all **customizable through
conversation** after first run.

## More Installation Options

Pick the one that matches your agent.

### Option 1: ClawHub (easiest, OpenClaw users)

```bash
openclaw skills install follow-github
```

Then start a conversation and say "配置 follow-github" — the skill walks you
through setup interactively.

### Option 2: Claude Code

```bash
# Per-user (available in all projects)
git clone https://github.com/Miraclemin/follow-github ~/.claude/skills/follow-github

# OR per-project (scoped to one repo)
git clone https://github.com/Miraclemin/follow-github .claude/skills/follow-github
```

Claude Code auto-discovers skills in these directories. Start a new session
and ask "set up follow-github".

### Option 3: Codex CLI (or any other agent)

Codex doesn't have a first-class skill system, so run it as a reference
doc + scripts:

```bash
git clone https://github.com/Miraclemin/follow-github ~/agents/follow-github
cd ~/agents/follow-github/scripts && npm install
```

Then point your agent at `SKILL.md` — either by referencing it in your
`AGENTS.md` / system prompt, or by running:

```bash
# In Codex
"Read ~/agents/follow-github/SKILL.md and follow its instructions"
```

### Option 4: Manual (any setup)

```bash
git clone https://github.com/Miraclemin/follow-github
cd follow-github/scripts && npm install
node prepare-digest.js   # outputs the raw JSON (needs config first)
```

---

## First-Run Setup

The skill walks you through a 10-step interactive onboarding:

| # | What it asks |
|---|---|
| 1 | Intro (no input needed) |
| 2 | Your GitHub username |
| 3 | A GitHub Personal Access Token (guided setup) |
| 4 | Which content streams you want (any combination) |
| 5 | Language filter (e.g. Python, Rust — or all) |
| 6 | Frequency and time (daily/weekly + timezone) |
| 7 | Delivery method (auto-detected on OpenClaw) |
| 8 | Digest language (English / Chinese / Bilingual) |
| 9 | Cron job is registered automatically |
| 10 | Sample digest sent immediately for feedback |

Your preferences land in `~/.follow-github/config.json`; your token goes to
`~/.follow-github/.env` (never committed, never transmitted except to GitHub).

### Delivery Methods

The onboarding also configures how the digest reaches you:

- **OpenClaw**: delivered through OpenClaw's built-in channel system
- **Telegram**: uses your own bot token plus chat ID
- **Email**: uses your own Resend API key and email address
- **On-demand**: no scheduled delivery; ask for the digest when you want it

For non-persistent agents like Claude Code or Codex CLI, Telegram or email is
the recommended way to receive scheduled digests after the terminal closes.

### Telegram Setup

If you choose Telegram delivery, the agent should guide you through:

1. Open Telegram and search for `@BotFather`
2. Send `/newbot`
3. Pick a bot name and a username ending in `bot`
4. Copy the bot token BotFather returns
5. Open a chat with the bot and send it any message first
6. Save the token as `TELEGRAM_BOT_TOKEN` in `~/.follow-github/.env`
7. Fetch the chat ID with:

```bash
curl -s "https://api.telegram.org/bot<TOKEN>/getUpdates" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d['result'][0]['message']['chat']['id'])" 2>/dev/null || echo "No messages found — send a message to your bot first"
```

### Email Setup

If you choose email delivery, the agent should guide you through:

1. Create a free account at https://resend.com
2. Create an API key in the Resend dashboard
3. Save it as `RESEND_API_KEY` in `~/.follow-github/.env`
4. Put your destination email address into `config.delivery.email`

### GitHub Token Setup

The onboarding guides you through this, but for reference:

1. Open https://github.com/settings/personal-access-tokens/new (fine-grained token)
2. **Repository access**: Public Repositories (read-only)
3. **Permissions**: `Metadata: Read` is sufficient (it's the default)
4. Copy the token (starts with `github_pat_`) and paste during onboarding

---

## Customization (by conversation)

After setup, just talk to the agent. Examples:

| You say | What changes |
|---|---|
| "Switch to daily" | `config.frequency` → `daily`, cron re-registered |
| "Only show me Rust" | `config.languages` → `["rust"]` |
| "Drop the trending section" | `config.sources.trending` → `false` |
| "Make summaries shorter" | `~/.follow-github/prompts/summarize-*.md` edited |
| "Change tone to more casual" | `~/.follow-github/prompts/digest-intro.md` edited |
| "Show my settings" | Reads and displays config.json |
| "Reset prompts to default" | Deletes your custom prompts |

Your custom prompt files in `~/.follow-github/prompts/` override the skill's
defaults — updates to the skill won't clobber your personalization.

---

## Architecture

```
GitHub API (live)         ──┐
github.com/trending scrape ─┼──▶ prepare-digest.js (local)
GitHub Search API (live)   ──┘              │
                                             ▼ JSON blob
                                        LLM (your agent)
                                             │  remixes with prompts
                                             ▼
                                        deliver.js ──▶ stdout / Telegram / Email
```

**Three-tier prompt loading** (for flexibility):
1. `~/.follow-github/prompts/*.md` — your customizations (highest priority)
2. `<remoteUrl>/*.md` — optional remote updates (configurable in `config.prompts.remoteUrl`)
3. `./prompts/*.md` — bundled defaults (fallback)

**Deduplication** via `~/.follow-github/state.json` — each event or hot repo
is shown only once per 30-day window.

**No central feed** — unlike `follow-builders`, every user runs their own
fetches. This keeps the skill zero-infrastructure: no server to maintain, no
GitHub Actions, no API keys to provision.

---

## Configuration Reference

```json
{
  "platform": "openclaw",
  "github": { "username": "your-handle" },
  "sources": {
    "following": true,
    "trending": true,
    "hot": true
  },
  "languages": ["python", "typescript"],
  "frequency": "weekly",
  "weeklyDay": "monday",
  "deliveryTime": "09:00",
  "timezone": "Asia/Shanghai",
  "delivery": { "method": "stdout" },
  "digestLanguage": "zh",
  "prompts": { "remoteUrl": null },
  "onboardingComplete": true
}
```

All fields are editable through conversation — you shouldn't need to touch
this file directly.

---

## Requirements

- Node.js 18+ (uses native `fetch`)
- A GitHub Personal Access Token (read-only public access)
- Optional: `openclaw` CLI, or Claude Code, or any LLM-capable CLI agent
- Optional for scheduled delivery outside OpenClaw: a Telegram bot token or Resend API key

---

## License

MIT — see [LICENSE](./LICENSE).

## Privacy

- Your GitHub token stays in `~/.follow-github/.env`, not in this repo
- Telegram and Resend keys, if used, also stay in `~/.follow-github/.env`
- Your preferences and dedup state stay in `~/.follow-github/`
- The repo only fetches public GitHub data plus your own authenticated API requests

---

## Related

- [follow-builders](https://github.com/zarazhangrui/follow-builders) — the
  original inspiration, tracks AI builders on X and YouTube podcasts
- [ClawHub](https://clawhub.ai) — the skill registry for OpenClaw

中文文档：[README.zh-CN.md](./README.zh-CN.md)
