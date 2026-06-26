# Example migration: Daily briefing job

## Symptoms

A daily briefing keeps using old settings even after the system changed.

Typical signs:
- old model still in use
- old formatting still in use
- requested changes take multiple attempts to stick
- delivery route behaves differently from current runtime expectations

## Root causes to check

- manifest pins an outdated model
- session mode is isolated but still behaves like a stale long-lived context
- prompt changes live partly in chat history instead of files
- outbound delivery route uses misleading session metadata
- verification rules freeze old configuration

## Before

Example brittle pattern:

```json
{
  "model": "openai/gpt-5.2",
  "session": "isolated",
  "wake": "now",
  "to": "channel:1476754066481877155",
  "verify": {
    "requirePromptExact": true,
    "requireModelExact": true,
    "requireDeliveryExact": true,
    "requireScheduleExact": true
  }
}
```

Problems:
- old model pin
- exact model verification locks drift in place
- outbound target may not be the provider-valid DM form
- prompt exactness can hide where the true source of truth lives

## After

Recommended fresh-runtime pattern:

```json
{
  "slug": "daily-ai-briefing",
  "cronId": "replace-with-live-cron-id-if-tracked-locally",
  "name": "daily-ai-briefing",
  "agentId": "main",
  "schedule": {
    "kind": "cron",
    "expr": "0 8 * * *",
    "tz": "Australia/Brisbane"
  },
  "runtimeMode": "fresh-isolated",
  "triggerMode": "wake-only",
  "promptFile": "automation/jobs/daily-ai-briefing/prompt.md",
  "policyFiles": [
    "automation/jobs/daily-ai-briefing/policy.md"
  ],
  "delivery": {
    "channel": "discord",
    "target": "user:270548320366100480",
    "accountId": "default",
    "mode": "runtime-send"
  },
  "modelPolicy": {
    "mode": "inherit-default"
  },
  "verify": {
    "requirePromptPath": true,
    "requirePolicyPaths": true,
    "requireDeliveryExact": true,
    "requireScheduleExact": true,
    "requireModelExact": false
  }
}
```

If you're using a local automation manager, keeping `slug` and `cronId` in the manifest makes reconciliation and verification deterministic.

## Why this fixes drift

- prompt is loaded from file every run
- policy is loaded from file every run
- delivery target is explicit and provider-valid
- model follows current default unless intentionally pinned
- exact model verification no longer preserves an outdated pin

## Validation checklist

After migration, confirm:
- editing the prompt changes the next run
- editing the policy changes the next run
- changing the default model affects the next run
- delivery still works after a live send test
- attachments work if the job needs them

## Provider-specific reminder

For Discord DMs, outbound sends may require `user:<discord_user_id>` even if session metadata suggests a `channel:<id>` route.
