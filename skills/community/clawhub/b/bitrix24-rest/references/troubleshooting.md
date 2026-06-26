# Troubleshooting

Use this file when webhook calls fail or the agent cannot reach the portal.

## Default Behavior

Do the first diagnosis yourself before asking the user anything.

Preferred order:

1. Run `scripts/check_webhook.py --json`
2. Inspect the result: format, DNS, HTTP status
3. Report concrete findings and one next fix

## Typical Failure: No Webhook Configured

If `check_webhook.py` reports `"source": "missing"`:

Tell the user once: "Webhook не настроен. Попросите администратора указать его в настройках."
Do not ask the user to paste a webhook URL. Do not retry.

## Typical Failure: DNS Resolution Failed

Usually means:

- typo in the portal domain
- local network issue

Tell the user the portal address could not be reached. Name the host that failed.

## Typical Failure: Bad Format

Expected format:

```text
https://your-portal.bitrix24.ru/rest/<user_id>/<webhook>/
```

Common mistakes:

- copied portal URL instead of webhook URL
- extra quotes or spaces
- wrong user ID segment

## Typical Failure: HTTP 401 or Auth Errors

Usually indicates:

- revoked webhook
- wrong secret
- expired OAuth token

Ask the user to verify or regenerate the webhook in Bitrix24.

## Typical Failure: `ACCESS_DENIED` or `insufficient_scope`

Missing permissions. Tell the user exactly which scope family is likely missing:

- CRM
- Tasks
- Calendar
- Disk
- IM
- `imbot`

Do not just say "permissions issue" without naming the likely scope.

## User-Facing Style

Prefer:

- what you checked
- what failed
- what is already confirmed working
- one next action
- plain business language ("connection to Bitrix24", "access to calendar")
- doing the next safe step yourself before asking the user

Avoid:

- long lists of shell commands for the user
- asking for confirmation before a simple retry
- exposing webhook URLs or secrets
- talking about curl, MCP, JSON, DNS, or config mechanics unless explicitly asked
- multiple-choice menus

## Response Templates

Bad:

- "What you need to do now: 1. create env 2. source env 3. run curl 4. or try direct URL..."

Better for missing webhook:

- "Доступ к Битрикс24 не настроен. Попросите администратора указать вебхук в настройках."

Better when DNS failed:

- "Не удаётся связаться с Битрикс24. Похоже, адрес портала указан неверно."

Better when auth failed:

- "Связь с Битрикс24 есть, но доступ не подтверждён. Скорее всего, вебхук нужно обновить."

## Autonomous Retry Rule

For safe read-only requests:

- Execute immediately
- If it fails, run `check_webhook.py --json`
- If fixable, retry once automatically
- Only then report the blocker

Do not ask "Should I try again?" — just do it.
