---
name: daily-commit-logbook
description: Generate daily internship logbook drafts and weekly internship reports from GitHub and GitLab commit activity. Build Indonesian MIS-friendly summaries, prepare Telegram approval requests before submission, and install OpenClaw cron delivery for daily and weekly reporting flows. Use when setting up commit-based internship logbooks, weekly LaTeX reports, repo-aware activity summaries, or approval-before-submit automation.
---

# Daily Commit Logbook

Generate Indonesian internship logbook text from GitHub and GitLab activity, then optionally schedule Telegram approval flows and weekly LaTeX reports.

## Quick start

Generate today's report:

```bash
GITHUB_USER="your-github-username" bash scripts/generate-report.sh
```

Or save reusable local config in `daily-commit-logbook/.env`:

```bash
GITHUB_USER=your-github-username
WEEKLY_REPORT_AUTHOR=Internship Student
WEEKLY_REPORT_WEEK_ONE_START=2026-01-05
```

Setup daily Telegram approval delivery:

```bash
bash scripts/setup-cron.sh \
  --time "18:00" \
  --timezone "WIB" \
  --github-user "your-github-username" \
  --telegram-chat "<telegram-chat-id>"
```

Setup the Monday weekly report delivery:

```bash
bash scripts/setup-weekly-cron.sh \
  --time "18:10" \
  --timezone "WIB" \
  --telegram-chat "<telegram-chat-id>"
```

## Required environment

Install and authenticate:

- `gh` for GitHub activity
- `glab` for GitLab activity
- `jq` for JSON processing
- OpenClaw CLI for cron setup

If the scripts are not installed at the workspace root, set `OPENCLAW_WORKSPACE=/path/to/workspace` before running them.

## Main scripts

- `scripts/generate-report.sh` - build the daily dual-version report and save `reports/commit-report-YYYY-MM-DD.md`
- `scripts/extract-mis-activity.sh` - extract the MIS-ready activity paragraph from the daily report
- `scripts/render-telegram-approval-request.sh` - generate the daily report, save a pending draft, and print a Telegram-ready approval request
- `scripts/submit-pending-logbook.sh` - submit the latest pending MIS draft after explicit user confirmation
- `scripts/render-whatsapp-message.sh` - direct-submit helper for manual fallback/debugging
- `scripts/generate-weekly-report.sh` - generate the previous week's LaTeX report
- `scripts/render-weekly-telegram-message.sh` - print a Telegram-ready weekly summary message
- `scripts/setup-cron.sh` - install the recurring daily OpenClaw cron job
- `scripts/setup-weekly-cron.sh` - install the recurring Monday weekly report cron job

## Behavior

1. Fetch same-day push activity from GitHub and GitLab.
2. Read changed files and diff hunks, not only commit titles.
3. Apply repo-specific context from `references/repo-contexts.json`.
4. Render Indonesian logbook text in two versions, standard and more natural for MIS.
5. Save a pending MIS draft and wait for explicit confirmation before submission.
6. Reuse the same diff-aware analysis for weekly internship reports.

## References

- Read `references/format-guide.md` for Indonesian phrasing and activity patterns.
- Edit `references/repo-contexts.json` to describe your repos and mark personal repos as excluded from internship reports.

## Notes

- The daily setup script writes `daily-commit-logbook/.env` with the chosen GitHub username for later runs.
- The weekly report author defaults to `Internship Student` unless `WEEKLY_REPORT_AUTHOR` is set.
- The internship week number defaults to week 1 unless `WEEKLY_REPORT_WEEK_ONE_START` is configured.
- The normal flow is Telegram approval first, MIS submission second.
