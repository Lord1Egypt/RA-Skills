# AI Agent Bounty Factory Skill

Autonomous bounty discovery, evaluation, and submission system for earning passive income through freelance AI agent task marketplaces. Scans ClawTasks, OpenWork, Dework, and Layer3 to find high-value tasks matching agent capabilities.

## Features

- **Multi-Platform Discovery** - Aggregates bounties from multiple freelance markets
- **Smart Scoring** - Scores tasks by skill match (50%), budget (30%), and recency (20%)
- **Auto-Proposal Generation** - Creates competitive proposals tailored to each task
- **Pipeline Tracking** - Tracks submissions, acceptances, and payments
- **24/7 Autopilot** - Runs continuously to find and capture opportunities
- **Python 3.9+ Compatible** - Zero external dependencies; optional SQLite for persistence

## Setup

```bash
# Configure tracker files
export BOUNTY_TRACKER="bounty_tracker.json"
export BOUNTY_EARNINGS="earnings.json"
export PROPOSAL_MODE="proposal"  # or "instant" (requires staking)

# Discover matching bounties
python scripts/bounty_factory.py discover

# Preview proposal for a bounty
python scripts/bounty_factory.py proposal bt_001

# Submit proposal
python scripts/bounty_factory.py submit bt_001

# Submit all matching bounties at once
python scripts/bounty_factory.py submit-all

# Check pipeline status
python scripts/bounty_factory.py status
```

## Use Cases

- Autonomous income generation through freelance AI agent work
- Automated multi-platform bounty monitoring
- Scale proposal submission without manual effort
- Track earnings across platforms and optimize approach
- Match agent capabilities to highest-value tasks