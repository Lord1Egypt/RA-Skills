---
name: github-bounty-hunter
description: Automatically scan GitHub repositories for open issues with 0 comments, evaluate their value, claim them, and submit PRs. Automates the entire GitHub bounty hunting workflow for passive income generation. Use when the user wants to find and complete GitHub issues for money, automate bounty hunting, or set up passive income from open source contributions.
---

# GitHub Bounty Hunter

Automate the entire GitHub bounty hunting workflow: scan for opportunities, evaluate value, claim issues, and submit PRs.

## What This Skill Does

1. **Scans** GitHub for 0-comment issues (first-mover advantage)
2. **Evaluates** issue value and complexity
3. **Claims** viable issues automatically
4. **Submits** PRs with quality implementations
5. **Tracks** submissions and monitors merge status

## Usage

### Quick Start

```bash
# Scan and process issues automatically
bash scripts/bounty_hunter.sh
```

### Configuration

Edit `scripts/config.sh` to customize:

```bash
MIN_VALUE=10           # Minimum estimated value ($)
MAX_COMPLEXITY=5       # Max complexity (1-10 scale)
AUTO_CLAIM=true        # Auto-claim issues
AUTO_SUBMIT=true       # Auto-submit PRs
```

### Automated Operation

Set up cron for continuous scanning:

```bash
# Every 30 minutes
*/30 * * * * bash ~/.openclaw/workspace/skills/github-bounty-hunter/scripts/bounty_hunter.sh
```

## How It Works

1. **Discovery**: Searches GitHub for `is:issue is:open comments:0`
2. **Filtering**: Removes spam, duplicates, and low-value issues
3. **Evaluation**: Scores based on:
   - Repository stars/activity
   - Issue clarity and scope
   - Estimated time to complete
   - Potential payout
4. **Claiming**: Comments on issue to claim it
5. **Implementation**: Generates solution and submits PR
6. **Tracking**: Monitors PR status and merge events

## Scripts

- `bounty_hunter.sh` - Main automation script
- `config.sh` - Configuration settings
- `evaluator.sh` - Issue value evaluation
- `tracker.sh` - PR status tracking

## Best Practices

- Start with `AUTO_CLAIM=false` to review opportunities first
- Focus on repositories with clear contribution guidelines
- Maintain high PR quality to build reputation
- Track merge rate and adjust strategy

## Revenue Potential

- **Conservative**: $50-200/month (5-10 merged PRs)
- **Moderate**: $200-500/month (10-25 merged PRs)
- **Aggressive**: $500-1000/month (25-50 merged PRs)

Success depends on:
- PR quality and merge rate
- Time invested
- Repository selection
- Market conditions
