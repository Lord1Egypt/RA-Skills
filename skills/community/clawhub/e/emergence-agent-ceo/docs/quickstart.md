# Quickstart: MVP Mode (IM-Only, 30 Minutes)

This guide gets you from zero to a running CEO Agent in 30 minutes, using only IM channels and mobile GitHub. No IDE required.

## Prerequisites

- A cloud VM (4C/8G minimum, ~$25/mo)
- A GitHub account and repository
- LLM API access (DeepSeek-V4 Pro recommended for CEO, DeepSeek-V4 Flash for sub-agents)
- SSH access to your VM

## Step 1: Clone the Workspace

```bash
ssh root@your-vm-ip
git clone https://github.com/emergencescience/emergence-agent-ceo.git
cd emergence-agent-ceo
```

## Step 2: Configure Your Environment

```bash
cp .env.example .env
# Edit .env with your LLM API keys and GitHub repo info
nano .env
```

Set `CEO_LLM_MODEL` to a logic model (DeepSeek-V4 Pro, Claude Sonnet, or GLM-5.1). Set `SUB_AGENT_LLM_MODEL` to DeepSeek-V4 Flash.

## Step 3: Install the Runtime

```bash
npm install -g openclaw
openclaw init
openclaw gateway start
```

## Step 4: Set Up GitHub Authentication

```bash
# Option A: Use GitHub CLI (recommended)
gh auth login

# Option B: Set GITHUB_TOKEN in .env
# GITHUB_TOKEN=ghp_your_token_here
```

## Step 5: Send Your First Message

Create your first strategic directive as a GitHub Issue:

```bash
gh issue create \
  --title "Market analysis: AI agent infrastructure landscape" \
  --label "signal/drill-down,priority/medium" \
  --body "Research the current state of agent infrastructure tools. Identify 3-5 trends worth writing about."
```

Or send the same message via IM to the CEO Agent.

## Step 6: Review the Output

The CEO Agent will:
1. Read the issue during its next heartbeat
2. Write analysis as an issue comment
3. Assign tasks to Growth Leader or DevOps Leader
4. Sub-agents will commit drafts and open PRs

Review PRs on mobile github.com, approve or request changes.

That's it. You're running.

## What's Next

When you're ready for the full experience (IDE review, CLI capability amplifiers, local file management), see [two-tier-setup.md](two-tier-setup.md).
