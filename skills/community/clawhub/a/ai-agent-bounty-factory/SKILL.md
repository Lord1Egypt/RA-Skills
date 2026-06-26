---
name: ai-agent-bounty-factory
description: |
  Autonomous bounty discovery and submission system for earning passive income
  through freelance AI agent task markets. Polls ClawTasks, OpenWork, Dework, and
  Layer3 to find tasks matching agent capabilities, scores by skill match (50%),
  budget (30%), recency (20%), generates proposals, submits automatically, and
  tracks earnings across platforms.

  Commands:
  - bounty_factory.py discover    Find matching bounties
  - bounty_factory.py submit <id>  Submit proposal for specific bounty
  - bounty_factory.py proposal <id> Preview generated proposal
  - bounty_factory.py submit-all Auto-submit all qualifying bounties
  - bounty_factory.py status     Show pipeline stats and earnings

  Environment: BOUNTY_TRACKER, BOUNTY_EARNINGS (JSON files), PROPOSAL_MODE
  (proposal or instant). Python 3.9+, zero deps, optional SQLite for persistence.

  Proposal mode: no stake required, lower acceptance rate but zero risk.
  Instant mode: requires staking, higher visibility, risk of stake loss.
  Pipeline tracks: submitted, accepted, in_progress, submitted_deliverable, paid.
compatibility: Created for Zo Computer
metadata:
  author: ssyopros.zo.computer
allowed-tools: Bash, Read
---

# AI Agent Bounty Factory

Autonomous income generation through freelance task marketplaces. Runs 24/7 to discover, propose, and earn.

## Scoring Algorithm

Each bounty is scored 0-100:
- **Skill Match (50 pts)** - How well required skills match agent capabilities
- **Budget (30 pts)** - Higher budgets score proportionally higher
- **Recency (20 pts)** - Newer bounties get priority; decays over 20 hours

Minimum threshold to auto-submit: 50 points.

## Commands

```bash
# Discover matching bounties
python scripts/bounty_factory.py discover

# Preview proposal for a bounty
python scripts/bounty_factory.py proposal bt_001

# Submit proposal for specific bounty
python scripts/bounty_factory.py submit bt_001

# Auto-submit all qualifying bounties
python scripts/bounty_factory.py submit-all

# Check pipeline status and earnings
python scripts/bounty_factory.py status
```

## Proposal Modes

- **proposal mode** (default): No staking required. Lower acceptance rate but zero financial risk.
- **instant mode**: Requires staking. Higher visibility and acceptance rates but risk of stake loss if work rejected.

Set via: `export PROPOSAL_MODE="instant"`

## Pipeline Lifecycle

```
discovered -> scored -> proposal_generated -> submitted -> accepted
                                              -> rejected
               accepted -> in_progress -> submitted_deliverable -> approved -> paid
```

## Supported Platforms

- ClawTasks (USDC on Base)
- OpenWork ($OPENWORK tokens)
- Dework
- Layer3

Configure API keys for each platform in environment variables.