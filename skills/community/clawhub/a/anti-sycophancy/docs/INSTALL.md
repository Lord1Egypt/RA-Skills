# Installation Guide

> **[中文版](./INSTALL.zh-CN.md)**

## Prerequisites

- **Claude Code** (version with hook support) — for Layer 1
- **OpenClaw** — for Layer 2 + Layer 3

---

## Method 1: Via ClawhHub (Recommended)

```bash
npx clawhub@latest install 0xcjl/anti-sycophancy
```

This automatically installs all applicable layers for your detected platform.

---

## Method 2: Via Claude Code (after manual clone)

```bash
# 1. Clone the repo
git clone https://github.com/0xcjl/anti-sycophancy.git ~/.claude/skills/anti-sycophancy

# 2. Use Claude Code
/anti-sycophancy install
```

---

## Method 3: Via ClawhHub + Claude Code combination

```bash
# Install via ClawhHub
npx clawhub@latest install 0xcjl/anti-sycophancy

# Then deploy layers manually
/anti-sycophancy install
```

---

## What Gets Installed

### Claude Code

| Layer | File | Purpose |
|-------|------|---------|
| Layer 1 | `~/.claude/hooks/sycophancy-transform.{sh,py}` | Hook script |
| Layer 1 | `~/.claude/settings.json` → `UserPromptSubmit` | Hook registration |
| Layer 2 | `~/.claude/skills/anti-sycophancy/SKILL.md` | Skill content |
| Layer 3 | `~/.claude/CLAUDE.md` | Persistent rules |

### OpenClaw

| Layer | File | Purpose |
|-------|------|---------|
| Layer 2 | `~/.claude/skills/anti-sycophancy/SKILL.md` | Skill content |
| Layer 3 | `{workspace}/SOUL.md` | Persistent rules |

---

## Platform-Specific Installation

### Claude Code Only

```bash
/anti-sycophancy install-claude-code
```

Installs: Layer 1 (hook) + Layer 3 (CLAUDE.md rules)

### OpenClaw Only

```bash
/anti-sycophancy install-openclaw
```

Installs: Layer 3 (SOUL.md rules)

---

## Verify Installation

```bash
/anti-sycophancy status
```

Expected output:
```
anti-sycophancy 安装状态
├── Claude Code
│   ├── Layer 1 Hook: ✅
│   ├── Layer 2 SKILL: ✅
│   └── Layer 3 CLAUDE.md: ✅
└── OpenClaw
    ├── Layer 1 Hook: ❌ (requires Plugin SDK)
    ├── Layer 2 SKILL: ✅
    └── Layer 3 SOUL.md: ✅
```

Test the hook:
```bash
/anti-sycophancy verify
```

---

## Uninstallation

```bash
/anti-sycophancy uninstall
```

This removes all installed layers while preserving the skill file itself.

---

## Troubleshooting

### Hook not transforming prompts

1. Check `~/.claude/settings.json` → `hooks` → `UserPromptSubmit` contains `"sycophancy-transform.sh"`
2. Run `/anti-sycophancy verify` to test
3. Check Python 3 is available: `python3 --version`

### Skill not triggering

- Say one of the trigger keywords: "防御谄媚", "批判模式", "play devil's advocate", "anti-sycophancy"
- Or describe your intent: "先泼冷水", "不要迎合我", "I want to hear counterarguments"

### Layer 3 rules not taking effect

- Claude Code: Rules load from `~/.claude/CLAUDE.md` on session start. Start a new session.
- OpenClaw: Rules load from `{workspace}/SOUL.md`. Restart the agent.
