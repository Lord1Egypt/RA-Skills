# agentic-commerce-news

> Agentic Commerce Weekly Briefing — scans the past 7 days of X/Twitter, industry media, and VC announcements for startups, products, funding rounds, and opinions endorsed by influential voices (VCs, founders, AI leaders) in the agentic commerce space, then produces a structured news briefing.

## What it does

A news aggregation skill focused on **agentic commerce** — the rapidly evolving space where AI agents shop, compare, check out, and pay on behalf of humans. On every invocation, it:

1. Launches 10+ parallel WebSearch queries across different angles, scoped to the past 7 days
2. Filters results to items with credible VC / institutional / platform endorsement
3. Classifies each item into the 9-layer Agentic Commerce Stack (Brand Discovery → Payments → Consumer Agent → Full-Stack Platform)
4. Generates cards grouped by event type (funding / product launch / founder quote / partnership / report)
5. Appends a summary table and weekly trend takeaways

## When it triggers

- User types `/agentic-commerce-news`
- User mentions keywords like "agentic commerce news", "AI commerce updates", "agent shopping this week"
- User asks things like "what's new in agentic commerce this week?" or "who's funding AI shopping startups?"
- User asks to set up a scheduled/recurring digest on agentic commerce

## Scheduling

Three ways to run this on a schedule, depending on your environment:

| Environment | Command | Notes |
|-------------|---------|-------|
| Claude Code (session) | `CronCreate` tool | In-session only, not persisted across restarts |
| Claude Code (persistent) | `/schedule` skill | Runs on claude.ai infrastructure, survives restarts |
| OpenClaw | `openclaw cron add` | 24/7 background execution |

### Example: Daily 8am digest in Claude Code

Say to Claude:
> "Set up a daily task to run agentic-commerce-news at 8am."

Claude will use `CronCreate` with `"3 8 * * *"` (8:03am — nudged a few minutes off the round hour to avoid API pile-ups).

### Example: OpenClaw persistent schedule

```bash
openclaw cron add \
  --name "Agentic Commerce Daily" \
  --cron "3 8 * * *" \
  --tz "America/New_York" \
  --message "Run the agentic-commerce-news skill to surface the past week's agentic commerce activity" \
  --channel <your-channel> \
  --to "<your-id>"
```

## Quality Gates

- Only items from the past 7 days qualify
- Every item must have credible endorsement (VC investment, public recommendation by a recognized figure, inclusion in a major report, or official platform partnership)
- Every item must include a source link
- Minimum 5 items (a quiet week is OK — do not pad with stale news)
- Exclude pure PR / sponsored content

## Output Format

```
## Agentic Commerce Weekly Briefing (Apr 8 – Apr 15)
> 8 noteworthy signals from the past week

### Funding
### ProductName (raised $XM) — one-line summary
**Date:** Apr 12
**Endorsement:** who invested
**Key points:**
- point 1
- point 2
**Layer:** Payment Infrastructure
Source: https://...

### Product Launches
...

### Founder / VC Opinions
...

## At a Glance

| Date | Company / Person | Event Type | One-line Summary | Layer |
|------|------------------|-----------|-------------------|-------|
| ... | ... | ... | ... | ... |

## Weekly Takeaways
1. ...
2. ...
```

## Installation

### Option A: Clone from GitHub

```bash
git clone https://github.com/xuxinmaxen/agentic-commerce-news.git \
  ~/.claude/skills/agentic-commerce-news
```

Restart your Claude Code session to pick it up.

### Option B: Install from ClawHub

```bash
clawhub install agentic-commerce-news
```

### Option C: Manual copy (Claude Code)

```bash
# Copy into ~/.claude/skills/
cp -r agentic-commerce-news ~/.claude/skills/

# Verify frontmatter
cat ~/.claude/skills/agentic-commerce-news/SKILL.md | head -5
```

Restart your Claude Code session to pick it up.

## Dependencies

- Claude Code ≥ 1.0 (requires the `WebSearch` tool)
- (Optional) `CronCreate` tool or `openclaw cron` — for scheduled execution
- **No** API keys or external services required

## Customization

To adjust the search strategy:

1. Edit the Phase 1 section of `SKILL.md` to add or replace WebSearch query templates
2. Edit the Phase 3 classification table to introduce new vertical segments
3. Edit the Phase 4 card format to tweak output style

To change the time window (e.g., 3 days or 30 days instead of 7):

- Update the `## Time Window` section's "past 7 days" phrasing
- Adjust the `this week` / `today` keywords in the search queries

## License

MIT-0 (MIT No Attribution) — free to use, modify, and redistribute. No attribution required. See [LICENSE](LICENSE).
