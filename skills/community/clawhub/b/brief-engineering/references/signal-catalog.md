# Signal catalogue

Every connector the brief can draw on, with live verification status. All `is` calls
need `--cloud-id "$ATLASSIAN_CLOUD_ID"`.

Verified 2026-08-27. Re-check before relying on any entry — status has changed within
hours during testing.

## Read this first: three failure modes that look identical

Every failing call prints something similar. They are not the same problem.

| Symptom | Meaning | What fixes it |
| --- | --- | --- |
| exit 1 with `MCP_TOOL_CONFIGURATION_INVALID_INPUT` | **Usually your arguments.** A missing required field produces exactly the same error as a genuine platform fault | Run `is tools schema <tool>` and supply every `*` field |
| exit 1 with `MCP_SERVER_REGISTRATION_PERMISSION_DENIED` | The MCP server is not granted to this principal | An access request, not a bug report |
| exit 2 | OAuth consent missing | Surface the consent link, retry after approval |
| `not found on requested MCP surfaces` | The tool name does not exist here | Enumerate with `is tools list --filter <x> --one-line` |
| HTTP 200 with implausible results | A wrong parameter name was **silently ignored** | Check counts against expectation |

Three tools I first recorded as broken were actually my own missing arguments:
`jira_aggregate_issues_using_jql` needed `operation` and explicit `cloudId`,
`calendar_get_events` needed `timeMin` and `timeMax`, and `c360_query_licenses` needs
`domain`. **Always exhaust the schema before declaring a platform fault.**

The silent-ignore case is the most dangerous: `compass_component_search` takes
`queryString`, and passing `query` returns all 88,539 components looking entirely valid.

**Pass `target_id_cloudId` inside `--args` whenever the schema lists it.** The
`--cloud-id` flag alone is not enough for several tools. This single change recovered
`jsm_..._operations_search_metrics`, which had been recorded as a platform fault
through two rounds of testing.

## Working — verified with live data

### Deployment and release

| Tool | Returns |
| --- | --- |
| `spinnaker_spinnaker_spinnaker_get_deployments` | prod/staging/dev nested by region then cluster, with `stable.timestamp`, `stable.createdBy`, `inProgress`. Empty object means not tracked under that name, not healthy |
| `shard_lifecycle_service_list_shards` | shard inventory |
| `switcheroo_..._search_target_app` | feature gate target apps |

### Ownership, dependencies, structure

| Tool | Key parameter | Returns |
| --- | --- | --- |
| `compass_..._component_search` | **`queryString`** | name, `typeId`, `ownerTeam.displayName`. Options: `includeOnCallSchedules`, `includeDependsOn`, `includeCustomFields`, `ownerIds` |
| `compass_..._component_get_package_dependencies` | `componentId` full ARI | dependency edges |
| `compass_..._component_get_event_sources` | `componentId` full ARI | event sources |
| `jsm_..._operations_get_service_dependencies` | `serviceId` as **graph ARI** | calls / calledBy graph. Note the ARI form is `ari:cloud:graph::service/...`, not the Compass component ARI |

Compass custom fields are unusually valuable. Services returning Spinnaker state carry
`platform = micros` plus `business-unit` and `public-facing`; a service missing
`platform` is unregistered, which explains an empty deploy response.

### Work context and planning

| Tool | Returns |
| --- | --- |
| `twg work query --scope me --since <N>d` | issues, pages, videos, devActivity, pullRequests |
| `twg jira workitem query --jql "<jql>"` | full issue list — 50 returned on test |
| `twg pull-requests query` | PR list. Zero results is a valid answer, not an error |
| `twg videos query --since <N>d` | Loom activity |
| `twg projects query --scope me --role contributor` | Atlas projects |
| `jira_..._aggregate_issues_using_jql` | exact counts. **Requires `operation` and explicit `cloudId`** |
| `confluence_cloud_get_my_permissions` | current user's global permissions |

### Change and customer

| Tool | Returns |
| --- | --- |
| `migrations_find_migration` | TPS tasks with `status`, `statusReason`, `migrationSchedule`, sharding context |
| `c360_..._query_customers` | customer records |
| `c360_..._query_licenses` | licences — **requires `domain`** |
| `notifications` | direct Atlassian notifications |
| `google_..._calendar_get_events` | calendar events — **requires `timeMin` and `timeMax`** as ISO 8601 UTC |
| `support_insights_healthcheck` | Support Insights service health |

### Operational health and alerts

| Tool | Returns |
| --- | --- |
| `twg jsm alert query --query 'source = SignalFx'` | SignalFx-originated JSM Ops alerts |
| `twg jsm alert query --query 'source = Splunk'` | Splunk-originated JSM Ops alerts |
| `reliability_insights_get_..._table_schema` | column lists and canonical SQL for 24 SRE tables. **Requires `table`**; `action` is one of schema, columns, queries, events |
| `reliability_insights_execute_socrates_query` | SELECT-only SQL against the SRE warehouse for history and recurrence |

Reliability Insights is the most valuable recovery in the catalogue. It exposes
`opsgenie_alerts`, `incident`, `service`, `alerts`, `anomaly`, `pir`, `impacts`,
`change_logs_prod` and sixteen more tables through SQL.

Verified live: 260,000 alert rows over seven days, and IDP-specific alerts including a
P2 CloudWatch alarm on `idp-connector-service--prod-east`.

Working query for service alerts:

```sql
SELECT alert_id, message, priority, status, integration_name, created_utc, count
FROM production.sre_incident.opsgenie_alerts
WHERE day_of_created >= DATE_SUB(CURRENT_DATE(), 14)
  AND lower(message) LIKE '%<service>%'
ORDER BY created_utc DESC
LIMIT 20
```

Notes from testing: always constrain on `day_of_created`, since the table is partitioned
on it and unbounded scans time out. There is no service column — alerts are matched on
`message`, so use a `LIKE` on the service name. `integration_name` reveals the alert
source, which distinguishes a SignalFx detector from a CloudWatch alarm.

### Other verified warehouse tables

**Production incidents** live in a different catalogue path — `sre_incident_source`,
not `production.sre_incident`:

```sql
SELECT issuekey, summary, severity, status, hot_type, start_utc
FROM sre_incident_source.incident_landing
ORDER BY batch_id DESC
LIMIT 20
```

Returns live HOT tickets with severity such as `2 - Major` and status such as `Fixing`.
There is no `priority` column — it is `severity`. The error messages name valid
alternatives when a column is wrong, so read them rather than guessing.

**Feature gate changes** track config-driven risk, often the cause of an unexplained
behaviour change:

```sql
SELECT changeId, eventTime, event, kind
FROM production.experimentation_switcheroo.change_logs_prod
WHERE eventTime >= DATEADD(day, -7, CURRENT_DATE())
ORDER BY eventTime DESC
```

Note this table uses `DATEADD(day, -7, ...)` against `eventTime`, while the alert table
uses `DATE_SUB(CURRENT_DATE(), 7)` against `day_of_created`. The dialect is not
consistent between tables — fetch canonical SQL with `action: queries` per table rather
than reusing a pattern.

`production.sre_incident.service` also returns rows and is worth exploring for service
metadata.

## Alerts via twg — the best path

`twg jsm alert query` reaches JSM Ops directly and works where the IS tool does not.
Full Opsgenie search syntax, live data, responders included.

```bash
twg jsm alert query --query 'status = open AND (message: *<service-a>* OR message: *<service-b>*)' \
  --limit 20 --site hello -o json --agent-fields @evidence
```

Verified: returned alerts created seconds earlier, plus an open P2
`OpenSearchFreeStorageSpace` on `idp-workflow-processor--prod-east` open since
7 August, with `tinyId 459118`, source `Prometheus` and the responding team ARI.

Useful query forms:

- `status = open` — everything currently paging
- `message: *<service>*` — per-service, wildcards supported
- `teams = "<team name>"` — by responding team
- `status = open AND priority = P1`
- sort with `--sort createdAt|lastOccurredAt|priority --order asc|desc`

Rows arrive under `data.values`. Use `--agent-fields @evidence` for responders, tags and
description; `@compact` for a scan.

Prefer this over `production.sre_incident.opsgenie_alerts` for current state — the SQL
table is better for aggregates and history, `twg` is better for what is open right now.
`twg jsm incident query` and `twg jsm pir query` cover declared incidents and retros.

## Failing — platform-side, not fixable by the caller

Each retried with the full required argument set including `target_id_cloudId`, and
where relevant with `--mcp-surface rovo` and `--refresh-tools`.

| Tool | Error | Blocks | Workaround |
| --- | --- | --- | --- |
| `jsm_..._operations_search_alert` | `MCP_TOOL_CONFIGURATION_INVALID_INPUT` | alert search | **`twg jsm alert query`** |
| `jsm_..._operations_search_sfx_signalflow` | `MCP_TOOL_CONFIGURATION_INVALID_INPUT` after the real required `programText` field was supplied twice | metric values | JSM Ops SignalFx-originated alerts |
| `jsm_..._operations_search_services` | fails on every shape | service resolution | Compass component search |
| `monolith_cicd_portal_gateway_get_environment_status` | same, with valid `environment` and `product` | monolith deploys | not needed for micros |
| `environment_manager_get_cell_status` | same, with a well-formed `cellId` | cell status | unconfirmed |
| `ares_..._get_apollo_clusters` | `MCP_SERVER_REGISTRATION_PERMISSION_DENIED` | OpenSearch capacity | access request |

**Read the error text, not just the code.** A schema-valid request can still reveal an
honest permission denial rather than a bad input error.

The Ares permission denial blocks OpenSearch cluster health. Splunk selection is
governed by `splunk_search_service` preflight in `connector-auth.md`; never show or
probe obsolete Splunk fallback routes when that registered route exists.

## Needs consent — exit 2

| Tool | Action |
| --- | --- |
| `zendesk_..._brand_query` | surface the consent link once, then retry |

## Slack — delegated Rovo search works

`twg rovo list-apps` reports Slack as connected and ready for the current principal.
`twg rovo search ... --app slack` returned current message links on 2 September 2026.
This CLI search is the supported delegated route even if the RovoClaw MCP catalogue has
no message-search tool. Treat those as separate surfaces; do not turn a missing MCP
tool into `Slack disconnected`.

The search API does not accept a channel ID filter. The skill therefore checks the
`/archives/<channel-id>/` segment of every returned URL against the team signal pack and
discards everything else. DMs and raw message bodies are never retained.

## SignalFx — live metrics need a registered tool; Socrates is alert history

`twg jsm alert query --query 'source = SignalFx'` returned current SignalFx alerts with
priority, state, responder, tags and timestamps. Use it for SLO burn, latency detector
and success-rate alerts. Match to confirmed services and group repeated messages.

This does not return the current p95/p99 value or a baseline. Direct values remain `not
checked` unless RovoClaw tool discovery finds an approved SignalFx tool for the current
principal. Without one, use the bounded Socrates alert-history query in
`connector-auth.md` and label it `signalfx-alert-history`, never live metrics. The
required action is: `register approved get_service_metrics or get_sqs_metrics for this
RovoClaw principal`.

## Splunk — Ops Sherpa direct search wins when registered

`twg jsm alert query --query 'source = Splunk'` returned Splunk-originated alerts with
priority, state, responder and timestamps. This is enough to surface a configured
Splunk alert, but not to inspect raw events or run a new SPL query.

When preflight finds registered Ops Sherpa `splunk_search_service`, inspect its schema
and use it as the exclusive direct-search route. Do not probe or report the obsolete
four-route fallback. If it is not registered, treat direct logs and DLQ counts as `not
checked` and retain JSM Ops alerts only. The skill cannot grant that access.

## No registered route

Forge app consumption was not present in the checked connector catalogue. It needs an
approved usage source or a team metric contract; never estimate it.

## Alert and incident enrichment — mostly unavailable

Tested with real identifiers from `twg jsm alert query` and `sre_incident_source`.

| Tool | Correct parameter | Result |
| --- | --- | --- |
| `jsm_..._operations_get_snr_insights` | `id` + `type` | **working** |
| `jsm_..._operations_get_risk_insights_change_windows` | `issueKeyOrId` | `MCP_TOOL_CONFIGURATION_INVALID_INPUT` |
| `jsm_..._operations_get_suggested_resources_by_key` | **`incidentIdOrKey`**, not `issueKeyOrId` | `MCP_TOOL_EXECUTION_SERVER_NOT_FOUND` |

`get_snr_insights` works. Called with `{"id":"<tinyId>","type":"alert",
"target_id_cloudId":"<cloud>"}` it returns `modelPrediction`, `userClassification` and
`status`.

Caveat from testing: on a real 20-day-old production alert it returned
`modelPrediction: UNKNOWN`. The model has no verdict for every alert, so treat a known
classification as a bonus and never let `UNKNOWN` suppress an item. Age and environment
remain the primary signal-versus-noise test.

The other two are unavailable, so no automatic runbook or freeze-window lookup. Fetch
runbooks from Compass `component_get_documentation` instead.

**A fourth distinct error code.** `MCP_TOOL_EXECUTION_SERVER_NOT_FOUND` means the
backing server is not deployed — different again from a bad argument, a permission
denial, or an unregistered tool name. Note also that the schema advertised
`issueKeyOrId` while the server demanded `incidentIdOrKey`: **the published schema can
be wrong, and the runtime error is more trustworthy.**

## Net position

The RovoClaw-native path covers work, ownership, deployments, incidents, Slack evidence,
and SignalFx/Splunk-originated alerts. Direct log search, current SignalFx values and
Forge consumption still need registered operational connectors. The brief must label
those sources `not checked`; a quiet alert query is not proof that the underlying
service is healthy.

## Parsing twg output

`twg` writes large payloads to a temp JSON file and prints the path — parse the file,
not the summary. Results sit under `data.items.sections` keyed by `issues`, `pages`,
`videos`, `devActivity`, `pullRequests`; counts under `data.counts.sections`. Note
`data.items.hydration` is a plain string, so iterating it as a dict will fail.
