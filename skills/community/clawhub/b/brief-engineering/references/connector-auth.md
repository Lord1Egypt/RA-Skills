# Operational connector authentication

Skill version: **1.0.7**.

Read this before collecting Slack, Splunk or SignalFx. A skill can select and call
tools; it cannot add an MCP server to a RovoClaw principal or move a laptop secret
into a cloud workspace.

## RovoClaw Cloud

## Deterministic connector preflight

Run this before every collection. It is the only source for the run's connector
coverage rows and selected routes. Start a fresh result on every run; do not merge it
with a prior dashboard or memory row.

1. Record `installedSkillVersion: "1.0.7"` from this skill's metadata and an ISO-8601
   `preflightAt` timestamp. First run `command -v is`. If it is absent, do not infer
   that either direct connector is unregistered: emit `runtime-unavailable` for both
   direct routes and stop their discovery for this run.
2. Slack: inspect `twg rovo list-apps -o json`. If Slack is `ready`, select
   `twg-rovo-search`; otherwise select `slack-consent-or-runtime-action`. A missing IS
   Slack tool never changes this selection.
3. Splunk: run `is tools list --filter splunk_search_service --one-line`. If a
   registered result exists, select that resolved Ops Sherpa tool exclusively, inspect
   its schema, and do not probe or report legacy Splunk fallbacks. Mark it `failed` if
   one complete, bounded schema-valid call fails; capture its error class only. If
   absent, select `jsm-alerts-only`.
4. SignalFx: discover `get_service_metrics` and `get_sqs_metrics`. If a registered
   approved metric tool exists, select it and inspect its schema. Mark it `failed` if
   one complete, bounded schema-valid call fails; capture its error class only.
   Otherwise select `socrates-alert-history`. This fallback is alert history, never
   live metric coverage. A failing `jsm_..._operations_search_sfx_signalflow` is not a
   substitute for an approved direct metric tool.
5. Emit the exact shape below, then render it verbatim into the current dashboard
   coverage section. Rebuild and replace the dashboard after every skill update so an
   old coverage row cannot survive.

```json
{
  "installedSkillVersion": "1.0.7",
  "preflightAt": "<iso8601>",
  "connectors": {
    "slack": { "route": "twg-rovo-search", "status": "ready|action-required", "action": "<none or exact consent/runtime action>" },
    "splunk": { "route": "<resolved splunk_search_service tool|jsm-alerts-only|runtime-unavailable>", "status": "registered|not-registered|failed|runtime-unavailable", "action": "<none, register Ops Sherpa splunk_search_service for this RovoClaw principal, or repair the registered Ops Sherpa RovoClaw runtime>" },
    "signalfx": { "route": "<resolved metric tool|socrates-alert-history|runtime-unavailable>", "status": "live-metrics|alert-history-only|failed|runtime-unavailable", "action": "<none, register approved get_service_metrics or get_sqs_metrics for this RovoClaw principal, or repair the registered SignalFx RovoClaw runtime>" }
  }
}
```

### Slack

Slack uses the invoking user's delegated Rovo connection. Do not request or store a
Slack API token.

```bash
twg rovo list-apps -o json
twg rovo search "<service> DLQ latency workflow failed production" \
  --app slack --updated-since 7d --limit 50 -o json
```

Proceed only when the Slack app is `ready`. Apply the signal-pack channel ID allowlist
to every returned `/archives/<channel-id>/` URL. If consent is required, show that
action once and stop Slack collection for the run. Do not inspect IS Slack tools or
mark Slack unavailable because one is absent; delegated `twg rovo search --app slack`
is the route.

### Splunk

Prefer a registered Ops Sherpa `splunk_search_service` tool. Discover the concrete
tool name and schema instead of guessing its prefix.

```bash
is tools list --filter splunk_search_service --one-line
is tools schema <resolved-splunk-search-service-tool>
```

If the call reports `No cached token found for Splunk`, discover and call the registered
SLAuth generator once with:

```json
{
  "audience": "splunk.paas-inf.net",
  "environment": "production",
  "force": true,
  "groups": ["atlassian-all"],
  "mfa": true,
  "ttl": "8h"
}
```

The user must complete the MFA prompt. Retry the bounded Splunk aggregate once after
authentication succeeds. Use `service`, `env`, a short relative time window,
`include_raw: false`, limited result fields and a server-side time limit. If the retry
fails, report the real error and stop.

When no direct Splunk tool is registered, use `source = Splunk` JSM Ops alerts and
label direct logs `not registered`. When `splunk_search_service` is registered, it is the
only direct-log route: do not probe, use, or show obsolete multi-route fallbacks. If a
complete schema-valid request fails, label direct logs `failed`, retain the error class
and ask the integration owner to repair the registered Ops Sherpa RovoClaw runtime;
registration alone will not repair a broken route.

### SignalFx

Direct values require registered `get_service_metrics`, `get_sqs_metrics` or an
equivalent approved remote tool. Discover the tool and schema first:

```bash
is tools list --filter get_service_metrics --one-line
is tools list --filter get_sqs_metrics --one-line
```

If no tool is registered, use the bounded Socrates alert-history query below and label
live values `not registered`: it is history, not current metrics. Show this exact action:
`register approved get_service_metrics or get_sqs_metrics for this RovoClaw principal`.
If a direct call returns HTTP 401, show instead: `replace the expired SignalFx token in
the approved connector configuration`; do not retry or ask the user to paste a token
into chat. SignalFx user tokens currently expire every 30 days.

If an approved registered metric tool rejects one complete schema-valid request (as
the checked SignalFlow route did with `programText`), label direct values `failed` and
ask the integration owner to repair that RovoClaw runtime. Do not recast this as a
missing registration or retry it with alternate payload names.

```bash
is tools call reliability_insights_execute_socrates_query --cloud-id "$ATLASSIAN_CLOUD_ID" \
  --args '{"query":"SELECT alert_id, message, priority, status, integration_name, created_utc FROM production.sre_incident.opsgenie_alerts WHERE day_of_created >= DATE_SUB(CURRENT_DATE(), 14) AND lower(integration_name) LIKE '%signalfx%' ORDER BY created_utc DESC LIMIT 20"}'
```

## Local OpenClaw or Rovo Dev

The local runtime may run `npx --yes @atlassian/ops-sherpa@3.8.7` as a stdio MCP
server. Splunk uses SLAuth and MFA. SignalFx uses `SIGNALFX_API_TOKEN` and
`SIGNALFX_REALM=us1`.

Keep the SignalFx token in macOS Keychain or another approved secret store and inject
it into the MCP process environment at launch. Never write the token into this skill,
`scope.json`, a signal pack, dashboard HTML, logs or a ClawHub package. A local
Keychain token is not available to RovoClaw Cloud.

When direct remote tools are unavailable, use the creator-private Confluence relay in
`local-operational-relay.md`. It moves normalized signal envelopes, never credentials
or raw source responses. A fresh relay is a distinct coverage route; it does not make
the missing cloud MCP registration appear healthy.

## Coverage acceptance check

A successful run must distinguish these rows:

- `slack`: `checked` only after delegated search ran and the channel allowlist was
  applied.
- `splunk`: `checked` only after a direct bounded search completed; Splunk-originated
  alerts belong in a separate `splunk-alerts` row.
- `signalfx-values`: `checked` only after a direct metric call completed; detector
  alerts or Socrates history belong in a separate `signalfx-alert-history` row.

An empty successful query is `checked, 0 items`. Missing auth, HTTP 401, missing tool
registration or a failed retry is never healthy.
