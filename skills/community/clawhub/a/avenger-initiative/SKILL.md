---
name: avenger-initiative
description: Encrypted GitHub backup and restore for any OpenClaw agent system. Creates branch-per-night backups with smart retention (7 daily, 8 weekly, 12 monthly branches). Backs up openclaw.json (AES-256 encrypted), agent memories, SOUL/IDENTITY files, cron jobs, and custom skills to a private GitHub vault. Triggers on phrases like "avenger backup", "backup system", "push to vault", "sync vault", "avenger restore", "restore from vault", "setup avenger", "avenger status", "avenger init", "configure backup", "set up backup". Also auto-runs after any critical config change.
version: 1.0.5
author: Matrix Zion (ProSkillsMD)
homepage: https://missiondeck.ai
license: MIT
tags: [backup, restore, encryption, github, security, devops]
openclaw: ">=2026.2"
---

# 🛡️ Avenger Initiative

Encrypted, branch-based GitHub backup and restore for any OpenClaw system.

## When This Skill Triggers

1. User says "setup avenger" / "configure backup" / "avenger init" → **Run SETUP flow**
2. User says "avenger backup" / "backup system" / "push to vault" → **Run BACKUP**
3. User says "restore from vault" / "avenger restore" → **Run RESTORE flow**
4. User says "avenger status" / "vault status" → **Show STATUS**
5. After any confirmed config change (gateway restart, config patch) → **Run BACKUP silently**

---

## SETUP FLOW (Agent-Guided)

When setup is triggered, **walk the user through it conversationally**. Ask one question at a time.

### Step 1 — Ask for the vault repo

> "To set up Avenger Initiative, I need a private GitHub repo to use as your vault. Have you created one already? If so, share the URL (e.g. `https://github.com/yourname/my-vault`). If not, I can help you create one."

### Step 2 — Handle the encryption key

> "Your `openclaw.json` (which contains all API keys and bot tokens) will be encrypted with AES-256 before being pushed. Do you have an existing encryption key from a previous Avenger setup, or should I generate a new one?"

### Step 3 — Run setup

```bash
bash ~/.openclaw/workspace/skills/avenger-initiative/scripts/setup.sh \
  --repo <vault-url>
```

### Step 4 — Show key and insist they save it

> "⚠️ **Your encryption key is below — save it NOW in 1Password, Bitwarden, or a secure note.**
> Without this key, your backup cannot be decrypted."

Wait for user to confirm "saved" before proceeding.

### Step 5 — Explain what will be backed up

- 🔐 `openclaw.json` — encrypted (all API keys, bot tokens, agent configs)
- 🧠 All memory logs and workspace files (SOUL, IDENTITY, MEMORY, TOOLS)
- 👥 Per-agent files for all agents
- 🔧 All custom skills
- 📋 Cron job definitions

**Retention policy:**
- Daily → 7 days
- Weekly → 8 weeks (created every Sunday)
- Monthly → 12 months (created 1st of each month)

### Step 6 — Run first backup & install cron

```bash
bash ~/.openclaw/workspace/skills/avenger-initiative/scripts/backup.sh
```

---

## BACKUP

```bash
bash ~/.openclaw/workspace/skills/avenger-initiative/scripts/backup.sh
```

Creates `backup/daily/YYYY-MM-DD` branch → merges to `main` → prunes per retention policy.  
On Sundays: also creates `backup/weekly/YYYY-WNN`.  
On 1st of month: also creates `backup/monthly/YYYY-MM`.

---

## RESTORE

```bash
bash ~/.openclaw/workspace/skills/avenger-initiative/scripts/restore.sh
```

Supports `--branch backup/daily/YYYY-MM-DD` to restore from a specific snapshot.  
Shows vault manifest, asks for confirmation, decrypts and restores all files.

After restore: `openclaw gateway restart`

---

## STATUS

Check `~/.openclaw/workspace/memory/avenger-backup.log` for last backup. Show timestamp, branch, and vault URL.

---

## File Locations

```
~/.openclaw/
├── credentials/
│   ├── avenger.key              ← Encryption key (NEVER commit)
│   └── avenger-config.json     ← Vault repo URL
└── workspace/skills/avenger-initiative/
    ├── SKILL.md
    ├── scripts/
    │   ├── backup.sh
    │   ├── restore.sh
    │   └── setup.sh
    └── references/
        └── security.md
```

---

## Security Model

- Vault repo should be **private** on GitHub
- `openclaw.json` → AES-256-CBC encrypted (PBKDF2, 100k iterations)
- All other files → plaintext (no secrets)
- Key lives only on the machine and in the user's password manager

See `references/security.md` for threat model and key rotation.

---

*More verified OpenClaw skills available at [proskills.md](https://proskills.md)*
