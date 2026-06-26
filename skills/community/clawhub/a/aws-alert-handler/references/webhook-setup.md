# Webhook setup (optional)

How to wire AWS alerts directly to the bot via OpenClaw's webhook endpoint.
This is one deployment option — the skill also works on pasted / piped
JSON without any webhook infrastructure.

## Overview

```
CloudWatch Alarm / Security Hub finding
  → SNS topic (or EventBridge API destination)
  → HTTPS POST to the bot's webhook endpoint
  → OpenClaw routes the payload to an agent turn
  → the agent runs aws-alert-handler
```

## OpenClaw config

Enable hooks and add a mapping for AWS alerts. This shape is verified
against the OpenClaw `hooks.mappings` schema (see
[gateway configuration reference](https://docs.openclaw.ai/gateway/configuration-reference)).

```json5
{
  hooks: {
    enabled: true,
    token: "a-strong-shared-secret",
    path: "/hooks",
    mappings: [
      {
        id: "aws-alert",
        name: "AWS Alert",
        match: { path: "/hooks/aws-alert" },
        action: "agent",
        sessionKey: "hook:aws-alert:{{MessageId}}",
        messageTemplate: "AWS alert received:\n\n{{payload}}",
        thinking: "low",
      },
    ],
  },
}
```

Template syntax notes (verified against OpenClaw's `renderTemplate` at
`src/gateway/hooks-mapping.ts`):
- `{{payload}}` — the full request body. Since it's an object, the
  template renderer emits it as `JSON.stringify(payload)`, which is
  exactly the shape this skill wants.
- `{{payload.foo.bar}}` — deep-path access into the payload (returns
  empty string if the path doesn't exist).
- `{{MessageId}}` — shorthand for `{{payload.MessageId}}` (bare names
  default to payload lookup). Present on SNS Notification envelopes.
- `{{headers.Authorization}}` — request header access.
- `{{path}}`, `{{now}}` — request path, ISO timestamp.

## Security: SNS signature verification (important)

OpenClaw's webhook endpoint authenticates callers with the `Authorization:
Bearer <token>` header, which protects against random internet traffic.
But SNS HTTPS delivery does NOT carry your bearer token by default — the
payload is SigV4-signed by AWS with `Signature` + `SigningCertURL` fields
in the envelope, which OpenClaw does not verify.

Practical implications:

1. *Anyone who knows your webhook URL and token can POST AWS-looking JSON.*
   They can spoof alerts.
2. *You can still authenticate the token from SNS* via an intermediary:
   - A reverse proxy (nginx/Caddy) that injects the bearer token before
     forwarding to the bot
   - An EventBridge API destination using EventBridge Connections (which
     does carry custom headers)
   - A Lambda between SNS and the webhook that verifies the SNS signature
     and then re-posts with the bearer token

For production-grade deployments where alert integrity matters, the Lambda
pattern is cleanest. For trusted networks (tailnet, VPC-private) with
high-entropy tokens, direct SNS → webhook is acceptable.

---

## HTTPS requirement

SNS requires a valid public HTTPS endpoint (signed cert, not self-signed).
Common patterns:

- *Tailscale Funnel* — simplest for self-hosted bots. Funnel exposes a
  Tailscale-assigned HTTPS URL that terminates at your bot.
- *Reverse proxy (nginx / Caddy) with Let's Encrypt* — traditional pattern.
- *API Gateway fronting a VPC-private endpoint* — if you're already on AWS
  and prefer AWS-native ingress.

## SNS subscription

Once the bot's webhook URL is reachable over HTTPS, subscribe SNS:

```bash
aws sns subscribe \
  --topic-arn arn:aws:sns:us-west-2:<account>:<topic> \
  --protocol https \
  --notification-endpoint https://<your-bot>.example.com/hooks/aws-alert
```

You need `sns:Subscribe` on the topic. Two setups require extra work:

- *Cross-account topic*: the topic owner must update the topic policy to
  allow subscriptions from your principal. Without that, `sns:Subscribe`
  permission on the consumer side isn't enough.
- *Cross-account endpoint*: some orgs restrict SNS to deliver only to
  endpoints in the same account. If your bot is in a different account
  than the topic, check the topic policy's `aws:SourceArn` conditions.

SNS sends a `SubscriptionConfirmation` message first (not an alert). The
webhook must GET the `SubscribeURL` in that message to confirm. Three
options:

- *Manual console*: go to the SNS console, find the pending subscription
  (status `PendingConfirmation`), click `Confirm Subscription`.
- *CLI*: extract the `Token` field from the webhook payload the bot
  received, then:
  ```bash
  aws sns confirm-subscription \
    --topic-arn arn:aws:sns:<region>:<account>:<topic> \
    --token <token-from-payload>
  ```
  The token comes from the `Token` field of the SNS
  `SubscriptionConfirmation` message body. `parse-alert.sh` exits 4 on
  that message and prints the `SubscribeURL` on stderr — which contains
  the token as a query parameter — but the cleanest extraction is just
  `jq -r '.Token' < incoming-payload.json`.
- *Automated*: write a `hooks.mappings` entry that detects
  `Type: SubscriptionConfirmation` and calls `curl $SubscribeURL` via a
  transform module (out of scope for this doc).

After confirmation, every alert published to that SNS topic arrives at
the webhook as a POST with the SNS envelope in the body.

## EventBridge alternative

If you prefer EventBridge over SNS:

1. Create an EventBridge API destination pointing at the same HTTPS URL.
2. Create a rule matching `aws.cloudwatch` or `aws.securityhub` events
   (per your needs).
3. Target the API destination.

The payload arrives as the raw EventBridge event (no SNS envelope).
`parse-alert.sh` handles both shapes.

## Troubleshooting

- *SNS subscription stuck in `PendingConfirmation`*: SNS couldn't reach
  the webhook, or the webhook couldn't GET the SubscribeURL. Check
  network reachability and webhook logs.
- *401 / 403 from the webhook*: the `Authorization: Bearer <token>`
  header is missing. Some SNS configurations don't support custom
  headers — you may need an EventBridge API destination with connection
  auth, or a reverse proxy that injects the header.
- *Alerts arrive but the skill doesn't fire*: check the agent's
  configured skills and whether the message content matches the skill's
  description. `openclaw logs -f` is the friend here.

## When NOT to use a webhook

- You're already reading alerts from a Slack channel (skip the webhook,
  the skill parses the pasted JSON directly via `parse-alert.sh`).
- You don't have a public HTTPS endpoint for the bot.
- Alert volume is low enough that polling + manual paste is fine.

The webhook path is the best-fit integration for production use cases
where alerts need to reach the bot automatically. It's not required for
trying the skill.
