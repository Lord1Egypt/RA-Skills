# Two-Tier Setup Guide: Laptop IDE + VPS Agent Team

This guide walks through setting up the full two-tier architecture: interactive human work on the laptop, autonomous agent work on the VPS.

## Architecture Overview

```
LAPTOP (Human Stakeholder)              VPS (Agent Team)
──────────────────────────              ──────────────────
IDE: Cursor / Google Anti-gravity       CEO Agent (Hermes)
CLIs: gh, Railway, Vercel, Yutu         ├── cron heartbeat
                                        ├── market survey
                                        ├── task creation & delegation
                                        ├── Growth Leader (content)
                                        └── DevOps Leader (infra)
                │
                │ GitHub Repository (shared state)
                │
```

## VPS Setup (Tier 2)

### 1. Provision the VM

Any cloud provider works. We recommend 4C/16G for comfortable parallel agent sessions.

```bash
ssh root@your-vm-ip
apt update && apt upgrade -y
```

### 2. Install OpenClaw

```bash
npm install -g openclaw
openclaw init
openclaw gateway start
```

### 3. Clone the Workspace

```bash
git clone https://github.com/emergencescience/emergence-agent-ceo.git
cd emergence-agent-ceo
```

### 4. Configure Environment

```bash
cp .env.example .env
# Edit with your LLM API keys and GitHub info
```

### 5. Set Up GitHub Authentication

```bash
gh auth login
```

### 6. Configure Cron Heartbeat

```bash
crontab -e

# CEO heartbeat: every hour, 9-18 UTC, weekdays
0 9-18 * * 1-5 cd /home/agent/emergence-agent-ceo && openclaw run --skill ceo-heartbeat

# Daily pulse: 08:30 UTC
30 8 * * * cd /home/agent/emergence-agent-ceo && openclaw run --skill pulse-generate
```

## Laptop Setup (Tier 1)

### 1. Clone the Same Repository

```bash
git clone https://github.com/YOUR_ORG/YOUR_REPO.git
cd YOUR_REPO
```

### 2. Set Up Your IDE

Use Cursor or Google Anti-gravity. Point the IDE to your cloned workspace.

### 3. Install CLI Tools

```bash
# GitHub CLI (already installed if you have gh auth set up)
gh auth login

# Optional: Railway, Vercel, Yutu
# These are your capability amplifiers — the agent can request them, you invoke them
```

### 4. Your Daily Workflow

```bash
# Morning: pull updates
git pull

# Review any PRs the agents opened
gh pr list --state open

# Read agent analysis in issue comments
gh issue list --state open

# Create new strategic directives
gh issue create --title "..." --body "..."

# Edit, approve, or request changes to agent drafts
# Push your changes
git push
```

## The Workflow in Practice

| Time | Activity | Who |
| :--- | :--- | :--- |
| 07:00 | Competitor scan | CEO Agent (cron) |
| 08:30 | Daily pulse signal | Growth Leader (cron) |
| 09:00 | Heartbeat: check issues, delegate | CEO Agent (cron) |
| 09:30 | Pull updates, review PRs | Human (laptop) |
| 10:00 | Create new issues, edit drafts | Human (laptop) |
| 10:30-17:00 | Sub-agents execute tasks | Growth/DevOps Leaders |
| 14:00 | Social publishing (if approved) | Growth Leader |

## Troubleshooting

| Issue | Fix |
| :--- | :--- |
| CEO agent not picking up issues | Check crontab, verify gh auth status on VPS |
| Sub-agents not executing | Check SOUL.md for each sub-agent, verify workspace directories exist |
| Human can't see agent output | Ensure agent pushes to GitHub, not just local commits |
| Token costs too high | Verify CEO uses logic model, sub-agents use Flash tier |
