---
name: copilot-usage
description: >-
  Display GitHub Copilot premium request usage, quota, billing stats, and per-model multipliers for the authenticated user. Use when the user asks about their Copilot usage, remaining premium requests, which models they used, monthly quota status, overage costs, or wants a Copilot usage dashboard or report. Works with Free, Pro, Pro+, Business, and Enterprise plans. Requires gh CLI authenticated with manage_billing:copilot and user scopes. Triggers on — copilot usage, copilot quota, premium requests, copilot billing, how many copilot requests, show copilot stats.
---

# Copilot Usage Skill

Fetch and display GitHub Copilot premium request usage via the GitHub REST API.

## Important API Limitations

The GitHub Billing API **does not expose the plan quota** (e.g., 50, 300, or 1500 requests/month). This information is not available in any endpoint. Therefore:

1. **The user must configure their plan once** — stored in `~/.config/copilot-usage/config.json`
2. On first run, the script detects missing config and prompts the user to set their plan

Explain this limitation clearly to the user when asking for their plan. Reference: https://docs.github.com/en/rest/billing/usage

## Auth Requirements

- Requires `gh` CLI authenticated with scopes: `manage_billing:copilot` + `user`
- Fine-grained tokens are **not supported** by GitHub billing endpoints — classic PAT required
- Check: `gh auth status`
- Fix: `gh auth login` then `gh auth refresh -s manage_billing:copilot`

## Usage

```bash
bash scripts/copilot-usage.sh                        # current month
bash scripts/copilot-usage.sh --month 3 --year 2026  # specific month
bash scripts/copilot-usage.sh --model claude          # filter by model
bash scripts/copilot-usage.sh --json                  # raw JSON output
bash scripts/copilot-usage.sh --set-plan pro+         # configure plan
bash scripts/copilot-alert.sh --threshold 80          # quota alert check
```

## Model Multipliers

The `grossQuantity` returned by the API **already includes the multiplier**. The script reverse-calculates the actual number of prompts sent and shows both values. See `references/multipliers.md` for the full table.

Key insight: `actual_prompts = grossQuantity / multiplier`

## What the Dashboard Shows

- Monthly quota used vs. remaining (requires plan config)
- Progress bar with percentage
- Overage count and cost
- Per-model breakdown with multiplier, gross requests, and estimated actual prompts
- Days until monthly reset
- Warning if plan config is missing or stale

## Config File

Stored at `~/.config/copilot-usage/config.json`:
```json
{
  "plan": "pro+",
  "quota": 1500,
  "set_at": "2026-04-08"
}
```

## Handling Errors

- **403 Forbidden** — token lacks billing scope: `gh auth refresh -s manage_billing:copilot`
- **404 Not Found** — verify endpoint path or plan eligibility (org/enterprise users must use org-level endpoints)
- **Config missing** — run `bash scripts/copilot-usage.sh --set-plan <plan>`

## API Endpoints

See `references/api.md` for full endpoint documentation and response schemas.
