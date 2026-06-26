---
name: agile-observer
description: "Proactive agile metrics and team health analysis for Trello and Jira boards. Computes cycle time, throughput, WIP, sprint burndown, aging work items, and blocker detection. Use when: analyzing sprint/board health, generating agile reports, checking team flow metrics, identifying bottlenecks, computing cycle time or throughput, reviewing WIP limits, detecting stale or blocked items, or creating sprint health summaries. Triggers on: how is the sprint going, board health, cycle time, throughput, burndown, agile metrics, team flow, WIP, blocked items, sprint report, agile health check."
---

# Agile Observer

Proactive agile metrics engine for Scrum Masters and Agile Coaches.
Analyzes Trello or Jira boards to compute flow metrics, detect problems, and generate health reports.

## Workflow

1. **Identify platform and credentials.** Ask for Trello or Jira. Look for credential files in workspace secrets (`trello-credentials.json` or `jira-credentials.json`).
2. **List boards/projects.** Fetch available boards and let the user choose, or use the one specified.
3. **Fetch board data.** Pull lists/statuses, cards/issues, and movement history using the API patterns in references.
4. **Classify workflow states.** Map list names or status categories to: backlog, doing, review, done.
5. **Compute metrics.** Calculate cycle time, throughput, WIP, aging, and blockers.
6. **Generate health report.** Assess overall health and add coaching suggestions.

## Metrics to Compute

| Metric | Formula | Source |
|--------|---------|--------|
| Cycle Time (median + P85) | Time from "doing" to "done" per item | Card/issue transition history |
| Throughput | Items completed in period | Cards/issues moved to done |
| WIP | Items currently in doing/review | Current board state |
| Aging WIP | In-progress items with no activity for 5+ days | dateLastActivity or changelog |
| Blockers | Items with "blocked" label or blocker priority | Labels/flags |
| Sprint Burndown | Done points vs. committed points (Jira only) | Story points field |

## List/Status Classification

Map names to workflow states using these patterns (case-insensitive):
- **Backlog:** backlog, to do, todo, icebox, upcoming
- **Doing:** doing, in progress, working, development, dev, active
- **Review:** review, testing, qa, validation, code review
- **Done:** done, complete, finished, deployed, released, closed

For Jira, use `statusCategory.key`: `new` = backlog, `indeterminate` = doing, `done` = done.

## Health Score Logic

- **🟢 GOOD:** No significant issues. Steady flow.
- **🟡 ATTENTION:** WIP exceeds 10 items, OR items aging without activity, OR blockers present.
- **🔴 CONCERN:** Cycle time median exceeds 7 days, OR multiple blockers, OR very low throughput.

## Report Format

```
📊 Agile Health Report — [Board/Project Name]
Period: last [N] days

🔄 Throughput: [X] items completed
⏱  Cycle Time: Median [X]d | P85 [X]d ([N] items measured)
📋 WIP: [X] items in progress
📈 Sprint Progress: [X]/[Y] points ([Z]%) — Jira only
🚫 Blocked: [X] items — [names]
🧓 Stale: "[item]" (no activity [X]d)

[🟢/🟡/🔴] Health — [summary]
```

## Coaching Suggestions

Include actionable advice based on findings:
- High WIP: "Consider a WIP limit of [team size x 1.5]. What needs finishing before starting something new?"
- Slow cycle time: "Where do items spend the most time? Look at the flow between columns."
- Stale items: "This item hasn't moved in [X] days. Still a priority, or should we park it?"
- Blockers: "What would it take to unblock [item]? Who needs to be involved?"
- Good health: "Flow looks healthy. What's one thing to improve next sprint?"

## Platform API Details

- **Trello endpoints and patterns:** See `references/trello-api.md`
- **Jira endpoints and patterns:** See `references/jira-api.md`
- **Detailed metric definitions:** See `references/metrics.md`

## Credential Formats

### Trello
```json
{"api_key": "...", "token": "..."}
```
Also accepts: `apiKey` + `apiToken`

### Jira
```json
{"instance": "mycompany", "email": "user@example.com", "api_token": "..."}
```

## Scheduling

For automated recurring reports, create a cron job:
- Schedule: weekly Monday 9:00 AM
- Task: Run agile-observer for board [X], deliver report to primary channel
