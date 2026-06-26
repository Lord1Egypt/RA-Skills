<h1 align="center">🤫 Agent Hush</h1>

<p align="center">
  <strong>Silent privacy guardian — catches sensitive data before it leaves your machine</strong>
</p>

<p align="center">
  <a href="LICENSE"><img src="https://img.shields.io/badge/License-MIT-blue.svg?style=for-the-badge" alt="MIT License"></a>
  <a href="https://www.python.org/"><img src="https://img.shields.io/badge/Python-3.6+-green.svg?style=for-the-badge&logo=python&logoColor=white" alt="Python 3.6+"></a>
  <a href="https://github.com/elliotllliu/agent-hush/stargazers"><img src="https://img.shields.io/github/stars/elliotllliu/agent-hush?style=for-the-badge" alt="GitHub Stars"></a>
</p>

<p align="center">
  <a href="#install">Install</a> · <a href="./README.md">中文</a> · <a href="#what-it-looks-like">Demo</a> · <a href="#detection-coverage">Coverage</a>
</p>

---

## Why Agent Hush?

You ask your Agent to push code, publish a Skill, sync files — but have you ever thought about what's hiding in those files?

- 🔑 "Push my code" → The **API Key in your config got pushed to GitHub** for the world to see
- 🏠 "Sync my workspace" → MEMORY.md contains your **real name, phone number, server IP** — now public
- 🔐 "Publish this Skill" → Forgot there's a **database connection string with credentials** in the directory
- 📁 "Share this project" → File paths reveal your **username and system structure**
- 🗝️ "Commit this" → .env wasn't in .gitignore, **Discord Bot Token went straight into git history**

**This happens every day.** Thousands of secrets are accidentally committed to GitHub daily.

**Agent Hush takes care of it for you:**

After installing, you work as usual. Your Agent automatically runs a security check before every outbound action — blocks and tells you if there's a problem, and you don't even know it checked if everything's clean.

**Like airport security: you just walk through, it watches for you.**

## Install

Copy this line and send it to your Agent:

```
Install Agent Hush: https://raw.githubusercontent.com/elliotllliu/agent-hush/main/docs/install.md
```

Done. No step two.

## What It Looks Like

### 🔑 Catching a leaked key before push

```
User: Push my code

Agent: Hold on — config.json line 12 has a GitHub Token (ghp_***abcd),
       pushing it would expose it. Want me to replace it before pushing?

User: Yes

Agent: Done, replaced and pushed ✅
```

### 🏠 Catching PII before Skill publish

```
User: Publish this Skill to ClawHub

Agent: Your SKILL.md has a real server IP (49.51.***.114)
       and an SSH command. Everyone would see these after publishing.
       Want me to remove them?

User: Do it

Agent: Replaced and published ✅
```

### 📁 Privacy warning during workspace sync

```
User: Sync to GitHub

Agent: MEMORY.md has your real name and phone number,
       TOOLS.md has server IPs and SSH key paths.
       These would go up with the push. Want me to handle them?

User: Handle MEMORY.md, leave TOOLS.md alone

Agent: MEMORY.md sanitized, pushed ✅
```

### ✅ When everything's clean — you feel nothing

```
User: Push my code

Agent: Pushed ✅

(Agent checked but found nothing — didn't bother you)
```

**No commands to learn. No habits to change. Just install it.**

## Smart Allowlist

Not everything detected needs to be fixed. Tell your Agent "ignore this" and it'll never flag it again:

```
Agent: Your files have 192.168.1.100 — want me to handle it?

User: Ignore it, it's a test IP

Agent: Got it, won't flag this again ✅
```

Supports wildcards — like "ignore all example.com emails":

```
User: Stop flagging example.com emails

Agent: Done, added to allowlist: *@example.com ✅
```

The allowlist lives in your project directory and travels with it. No config files to edit.

## Detection Coverage

**🔴 High confidence (auto-blocks):**
- AWS Key (`AKIA`), GitHub Token (`ghp_`), OpenAI Key (`sk-proj-`)
- Slack Token, Discord Bot Token, Anthropic Key
- 196 Gitleaks community rules (Stripe, Twilio, SendGrid, 190+ more)
- Private key blocks (`-----BEGIN PRIVATE KEY-----`)
- Database connection strings (`mysql://user:pass@host`)
- Chinese ID card numbers, credit card numbers

**🟡 Low confidence (warns but doesn't block):**
- Generic `password=xxx`, `token=xxx` assignments
- Private IPs (192.168.x.x, 10.x.x.x)
- SSH key paths, SSH commands
- Email addresses, phone numbers
- Absolute paths (`/root/`, `/home/user/`)

## Security

A privacy tool must hold itself to the highest standard:

- 🔒 **Runs locally** — All scanning happens on your machine. Nothing is sent to any server
- 👀 **Fully open source** — Every line of code is auditable
- 📦 **Zero dependencies** — Only Python standard library, no supply chain risk
- 🛡️ **Read-only by default** — Scans don't modify files, sanitized output goes to copies
- 💾 **Auto-backup** — Even if you choose to modify in place, originals are backed up first

## Contributing

Every industry, every platform has unique key formats and privacy data. We can't cover them all, but you can help:

**🔧 Found an uncovered sensitive data type?**
A cloud platform's API key, a payment system's credentials, a country's ID format — open an [Issue](https://github.com/elliotllliu/agent-hush/issues) or submit a [PR](https://github.com/elliotllliu/agent-hush/pulls).

**⚡ Want it to detect something new?**
Tell your Agent: "Add a rule to detect XXX format keys" and it'll configure it automatically.

Every rule you contribute helps another developer avoid a leak.

## Technical Details

- **Language**: Python 3.6+, zero dependencies (stdlib only)
- **Detection**: 220+ regex rules with confidence layering
- **Sources**: Gitleaks community rules + AI ecosystem rules + national PII standards

### How is confidence determined?

Based on methods validated in academic research and industry practice:

- **Format uniqueness** ([NDSS 2019 "How Bad Can It Git?"](https://www.ndss-symposium.org/ndss-paper/how-bad-can-it-git-characterizing-secret-leakage-in-public-github-repositories/)) — `AKIA` is an AWS-exclusive prefix, used nowhere else → high confidence. `password=xxx` appears in any codebase → low confidence
- **Shannon entropy analysis** — Real secrets have near-random character distribution (high entropy), while code variables are readable words (low entropy). Agent Hush uses structural analysis to identify function calls, env lookups, and template variables, filtering out low-entropy matches
- **Industry alignment** — TruffleHog (Verified / Unverified layering) and GitHub Secret Scanning (exact / fuzzy match layering) both use similar approaches

Result: **high-confidence items are handled automatically without breaking anything, low-confidence items only warn without touching code.**

## ⭐ Why Star?

This tool protects your own privacy. We'll keep maintaining it.

- New key formats from major platforms? We add detection rules ASAP
- Community-contributed rules get merged for everyone's benefit
- As the agent ecosystem evolves, we keep adapting

Every push, every publish shouldn't be a privacy leak.

Star it, and remember to use it next time you push. ⭐

## Acknowledgments

Secret detection rules are based on [Gitleaks](https://github.com/gitleaks/gitleaks) (MIT License), maintained by 200+ community contributors. Agent Hush adds PII detection, infrastructure info detection, confidence-based layering, and Agent ecosystem integration on top.

## License

MIT

---

_🤫 Hush — keeping secrets where they belong._
