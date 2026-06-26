---
name: aws-alert-handler
description: >
  Normalize Security Hub ASFF, Inspector v2, and CloudWatch alarm JSON
  into a consistent shape. Auto-unwraps SNS and EventBridge envelopes.
  Use when an AWS alert from any delivery path needs structured fields,
  or before handing off to `incident-triage`.
---

# AWS Alert Handler

Normalize AWS alerts into a consistent JSON shape. Works standalone or as
the first step of an [`incident-triage`](https://clawhub.ai/ggettert/incident-triage)
workflow.

## Scope

Parses Security Hub (ASFF), Inspector v2 (raw API or EventBridge envelope),
and CloudWatch alarm state changes (EventBridge or SNS-direct). Any of these
wrapped in an SNS `Notification` envelope is unwrapped automatically.

Does *not* parse custom Slack messages, AWS Chatbot output, or Cost Anomaly
findings. Format details and out-of-scope guidance:
[references/alert-formats.md](references/alert-formats.md).

## Usage

Pipe any alert JSON into the unified entry point:

```bash
cat alert.json | scripts/parse-alert.sh
echo "$ALERT_JSON" | scripts/parse-alert.sh
```

`parse-alert.sh` auto-detects the format, unwraps SNS envelopes, and
dispatches to the right format-specific parser.

For webhook-based delivery (SNS → OpenClaw `/hooks/aws-alert`) see
[references/webhook-setup.md](references/webhook-setup.md).

## Normalized output shape

Conforms to the shared [`normalized-alert-v0`](../interfaces/normalized-alert-v0.md)
interface. Core fields:

- `source` — `security-hub | inspector2 | cloudwatch-alarm`
- `source_subtype` — format-specific (e.g. `guardduty`, `package-vulnerability`)
- `severity` — `CRITICAL | HIGH | MEDIUM | LOW | INFORMATIONAL`
- `state` — `ACTIVE | ALARM | OK | INSUFFICIENT_DATA | RESOLVED`
- `account_id`, `region`, `resource_ids[]`, `title`, `summary`, `detected_at`, `console_url`
- `raw` — the original payload, preserved

Inspector v2 findings additionally carry `inspector_score` (CVSS 0.0–10.0)
when present. Full schema, examples, severity-mapping rules, and the
CloudWatch noise-filter list: [references/severity-mapping.md](references/severity-mapping.md)
and the [interface contract](../interfaces/normalized-alert-v0.md).

## Exit codes

`parse-alert.sh` exits:
- `0` — normal parse success; stdout is the normalized JSON
- `2` — payload didn't match any known format; stderr lists accepted shapes
- `3` — missing `jq`
- `4` — SNS `SubscriptionConfirmation` (not an alert); stderr includes the `SubscribeURL`
- `10` — non-incident alarm filtered out; stdout is the skip sentinel (see below)

## Skip sentinel

The CloudWatch parser emits a skip sentinel instead of a normalized
payload for known non-incident alarms (ECS TargetTracking autoscaling,
Elastic Beanstalk default alarms, EC2 AutoScaling policies, Synthetics
canary state changes). When this happens, `parse-alert.sh` exits 10 and
stdout is:

```json
{ "skip": "non-incident-alarm", "reason": "...", "alarm_name": "..." }
```

On exit 10, drop the event: do not invoke downstream handling, do not
post to chat.

## Optional: hand off to incident-triage

If `incident-triage` is installed and the alert warrants triage, invoke
it and pass the full normalized payload — the shape includes everything
triage needs to classify, scope, correlate, investigate, and advise.

## Works well with

- [`ggettert/incident-triage`](https://clawhub.ai/ggettert/incident-triage) — recommended downstream for full triage workflow.
- `github` — used by `incident-triage` during the Correlate step.

## Security

- Parser scripts run locally; no external API calls.
- The `raw` field preserves the full original payload. If alerts may
  contain sensitive data, strip `raw` before posting anywhere visible.
- For webhook-delivered alerts: OpenClaw's bearer-token auth protects
  the endpoint, but SNS does not send your bearer token by default. See
  [references/webhook-setup.md](references/webhook-setup.md#security-sns-signature-verification-important)
  for spoofing risk and mitigation patterns.
