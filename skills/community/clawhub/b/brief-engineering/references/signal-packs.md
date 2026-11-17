# Team signal pack contract

A signal pack is configuration a service owner registers once. Individual users never
edit it. It cannot grant access the user does not already have — it only tells the
brief what to look at and what to ignore.

## Shape

```json
{
  "packId": "idp-production-health",
  "selectors": {
    "services": ["idp-studio", "idp-workflow-processor", "idp-connector-service"],
    "projects": ["AURA"],
    "repositories": ["intelligent-document-processing"],
    "teams": ["ari:cloud:identity::team/<id>"]
  },
  "alertMatching": {
    "serviceAliases": [
      "idp-studio",
      "idp-workflow-processor",
      "idp-connector-service"
    ],
    "signalFxSources": ["SignalFx"],
    "splunkSources": ["Splunk"],
    "requiredTags": ["environment_type:prod"]
  },
  "thresholds": {
    "latency_p99_ms": 2000,
    "dlq_age_seconds": 3600,
    "directMetricsRequired": true
  },
  "workflows": {
    "example_business_workflow": {
      "criticality": "production-critical",
      "expectedCadenceHours": 24,
      "maxSilenceDays": 45
    },
    "test-reconciliation": { "criticality": "ignore" }
  },
  "slackChannels": ["C0A4HPC2DFS"],
  "owner": "team-email-or-ari"
}
```

## Matching rules

A pack attaches only on **exact** match of a confirmed service, project, repository or
team. Fuzzy matching is not permitted — it leaks one team's operational configuration
into another team's brief.

Service aliases must also be exact operational names. Do not register broad fragments
such as `idp` or adjacent-team names such as `idpaf`; both create convincing but
incorrect matches. Slack entries are exact channel IDs, never channel-name guesses.

Users cannot request a pack by ID. Attachment is recomputed on every run from confirmed
scope, so when ownership changes the pack detaches automatically.

A user with no matching pack still gets Atlassian work context, Compass ownership,
Spinnaker deploy state and alerts. They do not get another team's service aliases,
workflow rules or Slack channels, and those sources do not appear in their coverage
report.

## Why criticality must be declared

The brief cannot infer these, and guessing produces false alarms:

- which workflow is business-critical versus a test fixture
- how often a workflow is *expected* to run
- whether an empty result is a failure or a normal quiet day
- which alert names, tags and service aliases belong to the team
- DLQ and latency thresholds for this service's traffic shape
- which Slack channels are operational rather than social

A workflow marked `criticality: ignore` never produces a priority item regardless of
how long it has been silent. That is what stops the brief from flagging dormant test
workflows as incidents.

## Registering a pack

Store it at `memory/engineering-brief/signal-packs/<packId>.json`. Confirmed user scope
lives separately at `memory/engineering-brief/scope.json` — keep team configuration and
per-user confirmation in different files so a scope change never rewrites team config.
