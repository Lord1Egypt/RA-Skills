# Coherence Network API — Full Endpoint Reference

Base URL: `CN_API="${COHERENCE_API_URL:-https://api.coherencycoin.com}"`

Interactive docs: `$CN_API/docs`

## Health & Status

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/health` | Liveness probe (status, version, uptime) |
| GET | `/api/ready` | Readiness probe (DB check) |
| GET | `/api/version` | API version |

## Ideas

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| GET | `/api/ideas` | — | List portfolio (limit, offset, sort, filters) |
| GET | `/api/ideas/{id}` | — | Get idea with full scores |
| POST | `/api/ideas` | key | Create idea |
| PATCH | `/api/ideas/{id}` | key | Update idea |
| GET | `/api/ideas/cards` | — | Card feed (search, filter, cursor pagination) |
| GET | `/api/ideas/cards/changes` | — | Delta feed since token |
| GET | `/api/ideas/showcase` | — | Validated/shipped ideas |
| GET | `/api/ideas/resonance` | — | Ideas generating the most energy |
| GET | `/api/ideas/progress` | — | Portfolio progress dashboard |
| GET | `/api/ideas/health` | — | Governance health |
| GET | `/api/ideas/count` | — | Total idea count |
| POST | `/api/ideas/select` | — | Weighted stochastic selection |
| GET | `/api/ideas/selection-ab/stats` | — | A/B test comparison stats |
| GET | `/api/ideas/storage` | — | Storage info |
| GET | `/api/ideas/{id}/progress` | — | Single idea progress |
| GET | `/api/ideas/{id}/activity` | — | Idea activity feed |
| GET | `/api/ideas/{id}/tasks` | — | Tasks linked to idea |
| POST | `/api/ideas/{id}/advance` | key | Advance to next stage |
| POST | `/api/ideas/{id}/stage` | key | Set specific stage |
| POST | `/api/ideas/{id}/fork` | key | Fork an idea |
| POST | `/api/ideas/{id}/stake` | key | Stake on an idea |
| POST | `/api/ideas/{id}/questions` | key | Add question |
| POST | `/api/ideas/{id}/questions/answer` | key | Answer question |

## Spec Registry

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| GET | `/api/spec-registry` | — | List specs (limit, offset) |
| GET | `/api/spec-registry/{id}` | — | Get spec detail |
| POST | `/api/spec-registry` | key | Create spec |
| PATCH | `/api/spec-registry/{id}` | key | Update spec |
| GET | `/api/spec-registry/cards` | — | Card feed with search |

## Value Lineage

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| GET | `/api/value-lineage/links` | — | List lineage links |
| GET | `/api/value-lineage/links/{id}` | — | Get link |
| POST | `/api/value-lineage/links` | key | Create link |
| POST | `/api/value-lineage/links/{id}/usage-events` | key | Add usage event |
| GET | `/api/value-lineage/links/{id}/valuation` | — | Get valuation/ROI |
| POST | `/api/value-lineage/links/{id}/payout-preview` | — | Preview payouts |
| POST | `/api/value-lineage/minimum-e2e-flow` | key | Full end-to-end flow |

## Contributors

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| GET | `/api/contributors` | — | List contributors |
| GET | `/api/contributors/{id}` | — | Get contributor |
| POST | `/api/contributors` | — | Register contributor |
| GET | `/api/contributors/{id}/contributions` | — | Contributor's contributions |

## Contributions

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| GET | `/api/contributions` | — | List contributions |
| GET | `/api/contributions/{id}` | — | Get contribution |
| POST | `/api/contributions` | — | Create contribution |
| POST | `/api/contributions/github` | — | Track GitHub contribution |
| POST | `/api/contributions/record` | — | Record open contribution |
| GET | `/api/contributions/ledger/{id}` | — | Contributor ledger |
| GET | `/api/contributions/ledger/{id}/ideas` | — | Contributor idea investments |

## Assets

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| GET | `/api/assets` | — | List assets |
| GET | `/api/assets/{id}` | — | Get asset |
| POST | `/api/assets` | — | Create asset |
| GET | `/api/assets/{id}/contributions` | — | Asset contributions |

## Distributions

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| POST | `/api/distributions` | — | Trigger value distribution |

## Coherence

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| GET | `/api/coherence/score` | — | Get coherence score |

## Governance

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| GET | `/api/governance/change-requests` | — | List change requests |
| GET | `/api/governance/change-requests/{id}` | — | Get change request |
| POST | `/api/governance/change-requests` | key | Create change request |
| POST | `/api/governance/change-requests/{id}/votes` | key | Cast vote |

## Federation — Instances

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| GET | `/api/federation/instances` | — | List instances |
| GET | `/api/federation/instances/{id}` | — | Get instance |
| POST | `/api/federation/instances` | key | Register instance |
| POST | `/api/federation/sync` | key | Receive sync payload |
| GET | `/api/federation/sync/history` | — | Sync history |

## Federation — Nodes

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| GET | `/api/federation/nodes` | — | List nodes |
| POST | `/api/federation/nodes` | key | Register node |
| POST | `/api/federation/nodes/{id}/heartbeat` | — | Node heartbeat |
| GET | `/api/federation/nodes/capabilities` | — | Fleet capabilities |
| GET | `/api/federation/nodes/stats` | — | Aggregated node stats |
| POST | `/api/federation/nodes/{id}/measurements` | — | Post measurements |
| GET | `/api/federation/nodes/{id}/measurements` | — | Get measurements |

## Federation — Strategies

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| GET | `/api/federation/strategies` | — | Get strategies |
| POST | `/api/federation/strategies/compute` | key | Compute strategies |
| POST | `/api/federation/strategies/{id}/effectiveness` | — | Report effectiveness |

## Friction

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| GET | `/api/friction/events` | — | List friction events |
| POST | `/api/friction/events` | — | Create friction event |
| GET | `/api/friction/report` | — | Friction report (window_days) |
| GET | `/api/friction/entry-points` | — | Entry point analysis |
| GET | `/api/friction/categories` | — | Category breakdown |

## Agent — Tasks

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| POST | `/api/agent/tasks` | — | Create task |
| GET | `/api/agent/tasks` | — | List tasks |
| GET | `/api/agent/tasks/{id}` | — | Get task |
| PATCH | `/api/agent/tasks/{id}` | — | Update task |
| POST | `/api/agent/tasks/{id}/execute` | token | Execute task |
| GET | `/api/agent/tasks/{id}/log` | — | Task log |
| GET | `/api/agent/tasks/{id}/stream` | — | Task stream |
| GET | `/api/agent/tasks/{id}/events` | — | Task events (SSE) |
| POST | `/api/agent/tasks/pickup-and-execute` | token | Pick up and execute |
| POST | `/api/agent/tasks/upsert-active` | — | Upsert active task |
| GET | `/api/agent/tasks/attention` | — | Tasks needing attention |
| GET | `/api/agent/tasks/count` | — | Task count |
| GET | `/api/agent/tasks/active` | — | Active tasks |
| GET | `/api/agent/tasks/activity` | — | Recent activity |

## Agent — Monitoring

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| GET | `/api/agent/effectiveness` | — | Agent effectiveness |
| GET | `/api/agent/collective-health` | — | Collective health |
| GET | `/api/agent/status-report` | — | Status report |
| GET | `/api/agent/pipeline-status` | — | Pipeline status |
| GET | `/api/agent/metrics` | — | Metrics |
| GET | `/api/agent/usage` | — | Usage |
| GET | `/api/agent/visibility` | — | Visibility |
| GET | `/api/agent/lifecycle/summary` | — | Lifecycle summary |
| GET | `/api/agent/orchestration/guidance` | — | Orchestration guidance |
| GET | `/api/agent/fatal-issues` | — | Fatal issues |
| GET | `/api/agent/monitor-issues` | — | Monitor issues |
| GET | `/api/agent/integration` | — | Integration info |

## Agent — Run State & Runners

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| POST | `/api/agent/run-state/claim` | — | Claim run state |
| POST | `/api/agent/run-state/heartbeat` | — | Heartbeat |
| POST | `/api/agent/run-state/update` | — | Update run state |
| GET | `/api/agent/run-state/{id}` | — | Get run state |
| POST | `/api/agent/runners/heartbeat` | — | Runner heartbeat |
| GET | `/api/agent/runners` | — | List runners |

## Automation Usage

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| GET | `/api/automation/usage` | — | Usage overview |
| GET | `/api/automation/usage/snapshots` | — | Usage snapshots |
| GET | `/api/automation/usage/external-tools` | — | External tool events |
| GET | `/api/automation/usage/alerts` | — | Usage alerts |
| GET | `/api/automation/usage/readiness` | — | Provider readiness |
| GET | `/api/automation/usage/daily-summary` | — | Daily summary |
| GET | `/api/automation/usage/subscription-estimator` | — | Subscription estimator |
| GET | `/api/automation/usage/provider-validation` | — | Validation report |
| POST | `/api/automation/usage/provider-validation/run` | — | Run validation probes |
| POST | `/api/automation/usage/provider-heal/run` | — | Run auto-heal |

## Gates

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| GET | `/api/gates/pr-to-public` | — | Validate PR to public |
| GET | `/api/gates/merged-contract` | — | Validate merged contract |

## Authentication

- `X-API-Key` — Required for write operations marked "key" above
- `X-Admin-Key` — Admin operations (reset-database)
- `X-Agent-Execute-Token` — Agent task execution
- Read operations (no "key" marker) work without authentication
