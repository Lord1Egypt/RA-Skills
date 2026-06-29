# bid-collection Skill — Quick Start Guide

## Install the Skill

Place the `bid-collection` folder in your `Desktop/skills/` directory, then type in Claude Code:

```
/bid-collection
```

The skill loads automatically.

## Quick Command Reference

### 1️⃣ One-Click Scan for Latest Tender Leads

```bash
# General scan for recent tender/procurement info
/bid-collection scan tender procurement 2026 --days=7

# Scan AI/LLM related projects
/bid-collection scan AI LLM procurement tender

# Filter by budget (>¥1M)
/bid-collection scan system development tender --budget-min=1000000
```

### 2️⃣ Targeted Track Scanning

```bash
# Core track: Large Language Models
/bid-collection scan LLM training inference service procurement

# Core track: Digital Transformation
/bid-collection scan digital transformation data governance data platform tender

# Dedicated coverage: SuYan (China Mobile Suzhou Research)
/bid-collection scan SuYan procurement tender
```

### 3️⃣ Start Scheduled Background Monitoring

```bash
# Start monitoring (default: scan every 2 hours)
/bid-collection monitor

# Custom scan interval (every 60 minutes)
/bid-collection monitor --interval=60
```

### 4️⃣ Generate Summary Report

```bash
# View all lead summaries
/bid-collection report

# Core tracks only
/bid-collection report --track=core

# Urgent leads only
/bid-collection report --priority=urgent

# Detailed export
/bid-collection report --output=detail
```

### 5️⃣ Manage Monitoring Sources

```bash
# View current monitoring channels
/bid-collection list-sources

# Add a custom monitoring source
/bid-collection add-source https://example-bid-platform.com
```

## Usage Scenarios

### Scenario 1: Daily Lead Monitoring

```bash
# Morning summary
/bid-collection scan tender procurement --days=1

# Start background continuous monitoring
/bid-collection monitor
```

### Scenario 2: Urgent Opportunity Discovery

```bash
# Find high-match urgent projects
/bid-collection scan AI LLM tender --budget-min=5000000

# View details and contact info
```

### Scenario 3: Competitor Analysis

```bash
# Check competitor award activity
/bid-collection scan XX Company awarded

# Analyze industry trends
/bid-collection report --track=ai   # AI track only
```

## Best Practices

1. **First use**: Run `scan` for a full sweep to build an initial lead pool
2. **Daily**: Run `scan <keywords> --days=1` for today's new projects
3. **Ongoing**: Start `monitor` for real-time push of new leads
4. **Weekly**: Run `report` to review and prioritize lead follow-ups
5. **Monthly**: Export full monthly report analyzing track distribution and win opportunities

## Customization Guide

### Modify Business Tracks & Matching Rules

Edit `references/bid-matching-rules.md`:
- Adjust track weight percentages
- Add or modify matching keywords
- Update key buyer focus list
- Change irrelevant information filter rules

### Modify Monitoring Sources

Edit `references/monitoring-sources.md`:
- Add/remove target procurement platforms
- Adjust provincial/municipal trading center list
- Add industry-specific monitoring sources

### Customize Output Fields

Default output: Project Name, Buyer, Business Track, Budget, Deadline, Status.

Modify the output format template in `SKILL.md` as needed.

## Tips

- 💡 Budget params `--budget-min` / `--budget-max` are in **CNY (yuan)**
- 💡 Use `--days=N` to control search time window (default: 3 days)
- 💡 Once monitoring starts, new leads are pushed via PushNotification
- 💡 Canceled/abandoned projects may be re-tendered — keep tracking
- 💡 Run multiple monitor instances (different keyword combinations) simultaneously