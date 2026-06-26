---
name: gh-monitor
description: GitHub repo monitoring: Track issues/PRs/CI runs, new activity, label filters, notifications via cron/message. Extends gh CLI + gh-issues skill. Triggers: "watch repo", "gh alerts", "PR status [repo]", "issues monitor".</description>
---

# GH Monitor

## Examples
- \"Watch open bugs in myrepo\": gh issue list --label bug --state open --limit 20
- \"PR status\": gh pr list --state open --limit 10
- Daily cron: cron add schedule.cron expr=\"0 9 * * *\" payload.systemEvent \"Check GH: new issues/PRs\"

## Workflow
1. Setup: gh auth status; gh repo view owner/repo
2. Query: gh search issues \"is:open label:bug\" --json
3. Alert: message urgent PRs/unmerged.
4. Advanced: gh run list --status failure; browser for comments.

Read refs/gh-commands.md + gh-issues/SKILL.md.

## Scripts
scripts/check-repo.py: Poll + notify.

assets/alert-template.md: Slack/Discord format.

