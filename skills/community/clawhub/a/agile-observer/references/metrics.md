# Agile Metrics Reference

## Supported Metrics

### 1. Cycle Time
- **Definition:** Time from when work begins on an item until it's completed.
- **Trello:** Measures time a card spends between a "doing" list and a "done" list.
- **Jira:** Uses issue transition timestamps (In Progress → Done).
- **Calculation:** `completed_date - started_date` per item; report median + P85.

### 2. Throughput
- **Definition:** Number of items completed per time unit (day/week/sprint).
- **Trello:** Count cards moved to a "done" list within the period.
- **Jira:** Count issues transitioned to "Done" status within the period.

### 3. WIP (Work in Progress)
- **Definition:** Number of items currently being worked on.
- **Trello:** Count cards in lists matching "doing"/"in progress"/"review" patterns.
- **Jira:** Count issues in "In Progress" status category.
- **Healthy range:** Typically ≤ 2× team size.

### 4. Sprint Burndown (Scrum only)
- **Definition:** Remaining work (story points or count) vs. ideal burn rate per sprint day.
- **Data needed:** Sprint start/end dates, total committed points, daily completion.
- **Output:** Day-by-day comparison: ideal remaining vs. actual remaining.

### 5. Cumulative Flow
- **Definition:** Stacked area of items in each workflow state over time.
- **Interpretation:** Widening bands = bottleneck; narrowing = flow improvement.

### 6. Aging WIP
- **Definition:** How long current in-progress items have been open.
- **Alert threshold:** Items older than 2× the median cycle time are flagged.

### 7. Blocker Rate
- **Definition:** Percentage of items currently blocked.
- **Detection:** Trello labels containing "blocked"/"blocker"; Jira "Flagged" field.

### 8. Team Health Indicators (composite)
- **Flow Efficiency:** Active work time / total lead time (target: >40%).
- **Predictability:** Standard deviation of cycle time (lower = more predictable).
- **Staleness:** Items with no activity in >5 days.

## Output Formats

### Text Report (default)
```
📊 Sprint Health — [Board/Project Name]
Period: [start] → [end]

🔄 Throughput: 12 items/week (↑ from 9 last week)
⏱ Cycle Time: Median 2.3d | P85 4.1d
📋 WIP: 7 items (⚠️ above limit of 6)
🚫 Blocked: 2 items (15%)
🧓 Aging: 1 item > 8 days ("Refactor auth module")

🟢 Health: GOOD — steady flow, minor WIP overshoot
```

### CSV Export
Generate a CSV for external charting when requested:
```
date,metric,value
2026-03-10,throughput,3
2026-03-10,wip,6
2026-03-10,cycle_time_median,2.1
```
