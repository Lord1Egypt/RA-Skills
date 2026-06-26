# Message Iterator

This module is for persistent news intake.

It continuously polls public RSS feeds, scores headlines, and stores high-signal alerts into a local SQLite database.

It also converts those alerts into event-driven stock pools automatically, so the desk does not wait for manual watchlist updates.

## Target Alert Types

1. `huge_future`
   - Something with unusually large future potential.
   - Examples: AI model breakthroughs, new chips, data-center buildouts, robots, batteries, quantum, fusion.
2. `huge_name_release`
   - A globally famous company or person releases or announces something.
   - Examples: OpenAI, NVIDIA, Microsoft, Meta, Google, Apple, Tesla, xAI, Jensen Huang, Sam Altman, Elon Musk.
3. `huge_conflict`
   - A major conflict, strike, sanction, or energy-route disruption.
   - Examples: Middle East escalation, Hormuz threats, refinery strikes, shipping disruption.

## What The Iterator Produces

For each high-signal item it stores:

- title
- link
- source feed
- published time
- matched categories
- matched entities and keywords
- impacted watchlist groups
- score and signal strength

For each reporting window it also builds:

- `event_focus_huge_conflict_benefit`
- `event_focus_huge_conflict_headwind`
- `event_focus_huge_conflict_defensive`
- `event_focus_huge_future`
- `event_focus_huge_name_release`

These pools are written into `event_watchlists.json` and can be pulled directly into the morning brief and opening checklist.

## Default Market Mapping

- `huge_future`
  - `cross_cycle_ai_hardware`
  - `cross_cycle_semis`
  - `cross_cycle_software_platforms`
  - `cross_cycle_anchor12`
- `huge_name_release`
  - mapped by entity, with big-tech releases usually flowing to the same technology groups
- `huge_conflict`
  - `war_shock_core12`
  - `war_benefit_oil_coal`
  - `war_headwind_compute_power`
  - `defensive_gauge`

## Run Modes

### One-Off Poll

```bash
python3 scripts/news_iterator.py poll
```

### Continuous Loop

```bash
python3 scripts/news_iterator.py loop --interval-seconds 300
```

### Generate A Report

```bash
python3 scripts/news_iterator.py report --hours 12
```

## Long-Running Deployment

The simplest portable deployment is:

```bash
nohup python3 scripts/news_iterator.py loop --interval-seconds 300 > ~/uwillberich-news-iterator.log 2>&1 &
```

On macOS, the better deployment is `launchd`. This runs one poll on a fixed interval instead of keeping a Python process alive forever:

```bash
python3 scripts/install_news_iterator_launchd.py install --interval-seconds 300
python3 scripts/install_news_iterator_launchd.py status
```

The script stores state under:

- `~/.uwillberich/news-iterator/`

By default it writes:

- `news_iterator.sqlite3`
- `latest_alerts.md`
- `alerts.jsonl`
- `event_watchlists.json`

## Practical Workflow

1. Let the iterator run in the background.
2. Check the markdown report when you prepare the next session.
3. Let the auto-generated event stock pools flow into the desk reports.
4. If the top alerts skew to `huge_conflict`, use the split pools:
   - benefit: oil and coal
   - headwind: compute power, IDC, and power names
   - defensive: low-volatility shelters
5. If the top alerts skew to `huge_future` or `huge_name_release`, narrow into the generated technology pool first, then the static quality pools.

## Classification Notes

- Matching is term-boundary aware, so short words like `AI` do not trigger on unrelated text such as `said`.
- Conflict entities are tracked separately from big-name entities, so `Iran`, `Israel`, `Hormuz`, and similar terms can trigger the war overlay directly.
- The markdown snapshot is a rolling lookback report, while `alerts.jsonl` stays append-only for audit and later replay.

## What Not To Do

- Do not treat every alert as actionable.
- Do not confuse raw attention with sustained market leadership.
- Do not let conflict overlays permanently replace the core quality pools.
