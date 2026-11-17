# bid-collection Skill — Quick Start Guide

## Install the Skill

Place the `bid-collection` folder in your `Desktop/skills/` directory, then type in Claude Code:

```
/bid-collection
```

The skill loads and **shows a command help menu** (no-arg invocation does NOT auto-start collection — no outbound requests or local writes occur until you explicitly pick a subcommand like `scan` or `monitor`).

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

> ⚠️ **Before running, you must acknowledge these side effects:**
> - Creates a host scheduled task via `CronCreate` (modifies host scheduling)
> - Periodically sends outbound HTTP requests to monitored platforms (ongoing network traffic)
> - Sends `PushNotification` for new leads
> - Writes run logs to `leads-output/bid/monitor.log`
>
> **Activation limits:** default interval 120 min; default max 48 runs (~4 days, then auto-stops); **not persistent across sessions by default** (cron lives only for the current session/process unless `--persist` is set); run `monitor --stop` to stop and clean up the cron task.
>
> The skill will restate these side effects and ask for explicit confirmation before actually starting.

```bash
# Start monitoring (default: scan every 2 hours, max 48 runs, session-only)
/bid-collection monitor

# Custom scan interval (every 60 minutes)
/bid-collection monitor --interval=60

# Limit max runs (auto-stop after 24 runs)
/bid-collection monitor --max-runs=24

# Persist cron across sessions (use --stop to clean up later)
/bid-collection monitor --persist

# Stop monitoring and clean up the cron task
/bid-collection monitor --stop
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

> ⚠️ **Security warning — `add-source` triggers outbound requests (SSRF risk):**
> Adding a custom source will cause this skill to send outbound WebSearch/WebFetch requests to that URL and ingest its content in subsequent `scan`/`monitor` runs.
> - **Only add trusted public tender/procurement platforms.**
> - Adding untrusted sources may: send requests to attacker-controlled hosts (SSRF-like), expose your search keywords to unexpected third parties, and cause the skill to process malicious/misleading content.
> - Internal/localhost/metadata addresses (e.g. `127.0.0.1`, `169.254.169.254`, `localhost`, private ranges) will be rejected.
>
> The skill will restate this risk and ask for explicit confirmation before adding the source.

```bash
# View current monitoring channels (no outbound request)
/bid-collection list-sources

# Add a custom monitoring source (triggers outbound requests to this URL — confirm first)
/bid-collection add-source https://example-bid-platform.com

# Remove a monitoring source (no outbound request)
/bid-collection remove-source https://example-bid-platform.com
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