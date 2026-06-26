# 🛡️ Avenger Initiative

> Encrypted GitHub backup & restore for any [OpenClaw](https://openclaw.ai) agent system.

Built by [MissionDeck.ai](https://missiondeck.ai) · [GitHub](https://github.com/ProSkillsMD/avenger-initiative) · [ProSkills.md](https://proskills.md/skills/avenger-initiative)

<p align="center">
  <a href="CHANGELOG.md">
    <img src="https://img.shields.io/badge/version-1.0.5-brightgreen.svg?style=for-the-badge" alt="Version">
  </a>
  &nbsp;
  <a href="https://missiondeck.ai">
    <img src="https://img.shields.io/badge/MissionDeck-ai-blueviolet?style=for-the-badge" alt="MissionDeck">
  </a>
  &nbsp;
  <a href="https://proskills.md/skills/avenger-initiative">
    <img src="https://img.shields.io/badge/ProSkills.md-verified-brightgreen?style=for-the-badge" alt="ProSkills.md">
  </a>
  &nbsp;
  <a href="https://clawhub.ai/Asif2BD/avenger-initiative">
    <img src="https://img.shields.io/badge/ClawHub-install-orange?style=for-the-badge" alt="ClawHub">
  </a>
  &nbsp;
  <a href="LICENSE">
    <img src="https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge" alt="MIT License">
  </a>
</p>

---

## What It Does

Avenger Initiative backs up your entire OpenClaw system to a **private GitHub repo** every night — configs, agent memories, SOUL files, custom skills, cron jobs — everything needed to fully restore from zero.

**Security model:**
- `openclaw.json` (API keys, bot tokens) → **AES-256-CBC encrypted** before leaving disk
- Everything else (SOUL.md, MEMORY.md, etc.) → plaintext in your private repo
- Encryption key stays on your machine — never committed to Git

**Branch-per-night strategy with smart retention:**

| Branch | Pattern | Retention |
|--------|---------|-----------|
| Daily | `backup/daily/YYYY-MM-DD` | Last 7 days |
| Weekly | `backup/weekly/YYYY-WNN` | Last 8 weeks |
| Monthly | `backup/monthly/YYYY-MM` | Last 12 months |

---

## Installation

### Option 1 — ClawHub CLI (recommended)

```bash
clawhub install avenger-initiative
```

> Get the ClawHub CLI: `npm install -g clawhub`

### Option 2 — ProSkills.md

Visit **[proskills.md/skills/avenger-initiative](https://proskills.md/skills/avenger-initiative)** and click **Install**.

### Option 3 — Manual

```bash
mkdir -p ~/.openclaw/workspace/skills
git clone https://github.com/ProSkillsMD/avenger-initiative \
  ~/.openclaw/workspace/skills/avenger-initiative
chmod +x ~/.openclaw/workspace/skills/avenger-initiative/scripts/*.sh
```

---

## Quick Start

### 1. Create a private GitHub vault repo

Go to [github.com/new](https://github.com/new) and create a **private** repo (e.g. `my-openclaw-vault`).

### 2. Set up Avenger Initiative

Tell your OpenClaw agent:

> **"Setup avenger"**

Or run manually:

```bash
bash ~/.openclaw/workspace/skills/avenger-initiative/scripts/setup.sh \
  --repo https://github.com/yourname/your-vault
```

### 3. Save your encryption key

After setup, you'll see a 64-character hex key. **Save it in your password manager.** Without it, `openclaw.json.enc` cannot be decrypted.

### 4. Daily backups run automatically at 02:00 UTC

---

## Usage

| Say this to your agent | What happens |
|------------------------|-------------|
| `"avenger backup"` | Runs backup now |
| `"avenger status"` | Shows last backup time and branch |
| `"restore from vault"` | Guided restore flow |
| `"avenger setup"` | First-time setup wizard |

---

## Restore

```bash
# Restore latest (main branch)
bash ~/.openclaw/workspace/skills/avenger-initiative/scripts/restore.sh

# Restore from a specific date
bash ~/.openclaw/workspace/skills/avenger-initiative/scripts/restore.sh \
  --branch backup/daily/2026-03-10

# After restore
openclaw gateway restart
```

---

## Requirements

- [OpenClaw](https://openclaw.ai) installed and running
- [GitHub CLI](https://cli.github.com) (`gh`) authenticated (`gh auth login`)
- `git`, `openssl` (standard on most systems)
- A private GitHub repo for your vault

---

## 🖥️ MissionDeck.ai — Your Agent Command Center

**[MissionDeck.ai](https://missiondeck.ai)** is the cloud dashboard for multi-agent coordination.

- Real-time Kanban for all agent tasks
- Team chat between agents and humans
- Claude Code session tracking
- Cloud sync via JARVIS Mission Control API
- Free tier — no credit card required

**Try it:** [missiondeck.ai](https://missiondeck.ai)

---

## Security

This skill uses:
- **`openssl enc -aes-256-cbc`** — encrypts your `openclaw.json` with your own key
- **`gh repo clone`** — clones your own private vault repo via GitHub CLI auth
- **`git push`** — pushes to your own private vault repo only
- **No external servers** — data goes only to your own GitHub account

See [SECURITY.md](SECURITY.md) for full script-by-script analysis and audit instructions.

---

## More by Asif2BD

```bash
clawhub install jarvis-mission-control   # Multi-agent task coordination
clawhub install openclaw-token-optimizer # Reduce token costs 50-80%
clawhub install claude-code-cli-openclaw # Claude Code CLI integration
clawhub search Asif2BD                   # All skills
```

---

## License

MIT © [ProSkillsMD](https://github.com/ProSkillsMD)

---

[MissionDeck.ai](https://missiondeck.ai) · Free tier · No credit card required
