# Atoll API Field Reference

## Table of Contents

- [Task Fields](#task-fields)
- [Goal Fields](#goal-fields)
- [KPI Fields](#kpi-fields)
- [KPI Snapshots](#kpi-snapshots)
- [Initiative Fields](#initiative-fields)
- [Automation Rule Fields](#automation-rule-fields)
- [Custom View Fields](#custom-view-fields)
- [Board Context Response](#board-context-response)
- [Webhook Fields](#webhook-fields)
- [Setup Proposal Fields](#setup-proposal-fields)
- [Heartbeat Response](#heartbeat-response)
- [Analytics Response](#analytics-response)
- [Plan Limit Errors](#plan-limit-errors)
- [Agent Fields](#agent-fields)
- [Enums](#enums)

---

## Task Fields

Request bodies accept **camelCase** (`assigneeId`, `projectId`). Snake_case also accepted for backward compatibility. Responses always use snake_case.

```json
{
  "title": "Fix login bug",
  "description": "Markdown supported",
  "status": "todo",
  "priority": 1,
  "assigneeId": "member-uuid",
  "assigneeIds": ["member-uuid-1", "member-uuid-2"],
  "projectId": "project-uuid",
  "milestoneId": "milestone-uuid",
  "teamId": "team-uuid",
  "startDate": "2026-03-01",
  "dueDate": "2026-04-01",
  "recurrenceType": "weekly",
  "recurrenceInterval": 1,
  "labelIds": ["label-uuid-1", "label-uuid-2"]
}
```

Most fields work on both POST (create) and PATCH (update). `labelIds` is accepted on task create and bulk create. For existing tasks, use the label endpoints or `atoll label add/remove`.

- **Multiple assignees**: Use `assigneeIds` (array). Legacy `assigneeId` (single) still works. Responses include `assignees` array with `id`, `display_name`, `type`, `avatar_url`.
- **Start date**: Sets when work begins. Combined with `dueDate`, defines the Gantt time span.
- **Recurring tasks**: Set `recurrenceType` + optional `recurrenceInterval` (default 1). When marked `done`, a new instance is auto-created. Response includes `recurrence_next_date`.
- **Archived tasks**: Have `archived_at` timestamp. Excluded by default; pass `includeArchived=true`.
- **GET detail** returns enriched data: `milestone`, `assignee`, `assignees`, `sub_tasks`, `issue_labels`, `isBlocked`.

**Bulk create** (`POST /issues/bulk`):
```json
{ "issues": [{ "title": "Task 1", "status": "todo", "priority": 1, "projectId": "..." }] }
```
Returns `{ issues: [...], count: N }` (201). Max 50 per request.

## Plan Limit Errors

Creation endpoints may return `402` when an org reaches its billing plan limit:

```json
{
  "error": "Plan limit reached",
  "code": "PLAN_LIMIT_REACHED",
  "resource": "activeProjects",
  "plan": "free",
  "limit": 2,
  "usage": 2
}
```

`resource` is one of `humans`, `agents`, `activeProjects`, or `activeIssues`.

## Agent Fields

Create org-wide agents with `{ "name": "...", "role": "member", "setupScoped": false }`; org-wide creation is owner/admin-only. Create project-scoped agents with non-empty `projectIds`, for example `{ "name": "...", "projectIds": ["project-uuid"] }`; `projectId` remains accepted as a legacy/default-project alias and is merged with `projectIds`. Project-scoped agents are created as guests, and human members may only scope them to projects they can access. Create personal agents with `{ "name": "...", "personal": true }`; personal agents inherit their human owner's project access and reject explicit `projectId`/`projectIds`.

## Goal Fields

```json
{
  "title": "Reach 100 paying customers by Q2",
  "description": "Our primary growth objective",
  "owner_id": "member-uuid",
  "status": "active",
  "target_date": "2026-06-30"
}
```

## KPI Fields

```json
{
  "name": "paying_customers",
  "description": "Total active paying customers",
  "goal_id": "goal-uuid",
  "unit": "count",
  "unit_label": "customers",
  "target_value": 100,
  "target_direction": "increase",
  "source_type": "manual",
  "stale_after_hours": 168
}
```

Calculated task-completion KPIs use `source_type: "formula"` and are calculated from linked work instead of snapshots:

```json
{
  "name": "mvp_tasks_done",
  "goal_id": "goal-uuid",
  "source_type": "formula",
  "source_config": {
    "formula": "goal_linked_issue_completion",
    "done_statuses": ["done"]
  }
}
```

For `goal_linked_issue_completion`, `current_value` is the count of non-archived directly linked issues and milestone-linked issues in `done` status and `target_value` is the total non-archived directly linked issue and milestone-linked issue count under initiatives for the goal.

## KPI Snapshots

```json
{
  "value": 34,
  "source": "agent",
  "attribution_note": "Checked Stripe dashboard",
  "attributed_to_initiative_id": "initiative-uuid",
  "attributed_to_issue_id": "issue-uuid"
}
```

Recording a snapshot auto-updates the KPI's `current_value`.

Calculated KPIs do not accept manual snapshots.

`api_poll` snapshots are written by published KPI HTTP Syncs and include provenance: `source_sync_id`, `source_sync_run_id`, `source_config_hash`, `source_recorded_for`, `observed_at`, and optional `provider_recorded_at`.

## KPI HTTP Syncs

```json
{
  "name": "PostHog visitors",
  "schedule": "daily",
  "request_config": {
    "method": "GET",
    "url": "https://us.posthog.com/api/projects/123/query/",
    "headers": {
      "Authorization": {
        "secretRef": "posthog_api_key",
        "format": "Bearer {value}"
      }
    }
  },
  "extraction_config": {
    "contentType": "json",
    "pointer": "/results/0/value",
    "numeric": {
      "mode": "number",
      "percentageScale": null
    }
  },
  "freshness_config": {}
}
```

V1 syncs are `GET` only, `https` only, JSON only, exact-host allowlisted, no redirects, no request bodies, no inline query strings, and no secret values. Machine actors can create drafts and validate configs only after the host is allowlisted. Human admins manage allowlists, secrets, dry-runs, publishing, disabling, and snapshot-writing run-now actions in Atoll.

## Initiative Fields

```json
{
  "title": "Launch self-serve onboarding flow",
  "description": "Reduce friction for new signups",
  "goal_id": "goal-uuid",
  "owner_id": "member-uuid",
  "status": "active",
  "target_date": "2026-05-15",
  "project_id": "project-uuid"
}
```

Create accepts `projectId` as a camelCase alias for `project_id`. Guest/project-scoped callers must pass a project they can edit when creating initiatives.

For portfolio-style initiatives (grouping projects):
```json
{
  "title": "Q2 Platform Rewrite",
  "description": "Migrate all services to new architecture",
  "owner_id": "member-uuid",
  "start_date": "2026-04-01",
  "target_date": "2026-06-30"
}
```

Use `title` for create/update requests; create also accepts legacy `name`. Atoll keeps the legacy `name` field in sync for compatibility. Create accepts `goalId`, `ownerId`, and `targetDate` aliases for `goal_id`, `owner_id`, and `target_date`.

Add/remove projects with `{ "project_id": "uuid" }`.

## Initiative Target Fields

Targets attach to initiatives and track commitments separately from business KPIs. Use `mode: "progress"` for initiative outputs and `mode: "gate"` for hard launch prerequisites. Gate target heartbeat signals use stateful copy such as `0/5 retailers complete`; agents must not convert them into fractional KPI pace.

```json
{
  "title": "Get 5 retailers live by July 5",
  "description": "Prerequisite before price comparison launch",
  "mode": "gate",
  "unit": "count",
  "unit_label": "retailers",
  "current_value": 0,
  "target_value": 5,
  "target_direction": "increase",
  "target_date": "2026-07-05",
  "due_soon_days": 7
}
```

Target work links use `{ "issue_id": "issue-uuid" }` at `.../targets/{targetId}/issues` and `{ "milestone_id": "milestone-uuid" }` at `.../targets/{targetId}/milestones`. Target response rows include linked `issueIds` and `milestoneIds` when returned by the target list/get endpoints.

## Automation Rule Fields

```json
{
  "name": "Auto-assign urgent bugs",
  "trigger_event": "issue.created",
  "conditions": [{ "field": "priority", "operator": "eq", "value": 0 }],
  "actions": [{ "type": "set_assignee", "value": "member-uuid" }],
  "enabled": true,
  "project_id": "project-uuid"
}
```

**Dry-run test**: Send `{ "issue_id": "uuid" }` or `{ "issue": { "status": "todo", "priority": 2 } }`. Returns `{ matched, actions_that_would_run }`.

## Custom View Fields

```json
{
  "name": "My Sprint View",
  "filters": { "status": ["in_progress", "todo"], "priority": [0, 1] },
  "sort": { "field": "priority", "direction": "asc" },
  "display_mode": "board",
  "color": "#6B7280",
  "icon": "list"
}
```

`display_mode`: `board`, `list`. `filters` and `sort` are freeform JSON.

## Board Context Response

`GET /api/orgs/{id}/projects/{projectId}/board-context` returns the strategy data used by the board filter toolbar:

```json
{
  "strategyContext": {
    "milestones": [{
      "id": "milestone-uuid",
      "name": "Public beta",
      "status": "active",
      "issueCount": 4,
      "completedCount": 2,
      "progress": 50,
      "linkedInitiatives": [{
        "id": "initiative-uuid",
        "title": "Activation launch",
        "status": "active",
        "progress": 40,
        "kpiImpactCount": 1,
        "linkedMilestoneIds": ["milestone-uuid"]
      }]
    }],
    "initiatives": [{
      "id": "initiative-uuid",
      "title": "Activation launch",
      "status": "active",
      "issueCount": 5,
      "completedCount": 2,
      "progress": 40,
      "kpiImpactCount": 1,
      "linkedMilestoneIds": ["milestone-uuid"]
    }],
    "issueInitiativeLinks": [{
      "issueId": "issue-uuid",
      "initiativeIds": ["initiative-uuid"]
    }]
  }
}
```

`issueInitiativeLinks` includes direct `initiative_issues` links and links inherited from an issue's milestone.

## Webhook Fields

```json
{
  "url": "https://example.com/webhook",
  "events": ["issue.created", "issue.updated"],
  "enabled": true
}
```

URL must be an HTTPS DNS hostname. IP literals, `localhost`, and `.local` hosts are rejected at creation; delivery refuses non-public DNS results and does not follow redirects. Response includes `secret` for HMAC signature verification. Store it immediately; it is shown only once. Delivery requests include `X-Atoll-Signature: sha256=<hmac>`, where the HMAC-SHA256 key is the SHA-256 hex digest of the webhook secret and the message is the exact raw request body. Delivery requests also include `X-Atoll-Delivery-Id` for receiver-side deduplication. Delivery history includes retry `status` and `next_retry_at`.

## Setup Proposal Fields

First-run setup proposals are editable drafts. Setup-scoped local agents and ChatKit tools can submit or revise drafts; owner/admin humans apply them.

```json
{
  "setupSessionId": "setup-session-uuid",
  "proposal": {
    "projects": [{ "name": "Launch v1", "description": "..." }],
    "goals": [{ "title": "Reach 100 paying customers", "target_date": "2026-06-30" }],
    "kpis": [{ "name": "paying_customers", "target_value": 100, "target_direction": "increase" }],
    "initiatives": [{ "title": "Content pipeline", "description": "Publish and distribute launch content", "expected_impact": "Increase qualified signups" }],
    "milestones": [{ "name": "Public beta", "description": "Launch the public beta workspace", "due_date": "2026-05-15" }],
    "issues": [{ "title": "Instrument signup funnel", "description": "Track signup start, completion, and activation", "priority": 1 }]
  },
  "evidence": {
    "summary": "Optional notes about repo files or user answers that informed the proposal"
  }
}
```

Proposal JSON currently supports at most one item in each collection: `projects`, `goals`, `kpis`, `initiatives`, `milestones`, and `issues`. A revision replaces the active draft and preserves the previous revision as history. ChatKit tools and setup-scoped agents cannot apply proposals.

## Heartbeat Response

```json
{
  "agent": { "id": "...", "display_name": "Growth Agent" },
  "timestamp": "2026-03-29T12:00:00Z",
  "goals": [{
    "goal": { "id", "title", "status", "target_date" },
    "days_remaining": 93,
    "kpis": [{
      "kpi": { "name", "current_value", "target_value" },
      "pace_needed": 0.71,
      "pace_actual": 0.42,
      "trend": "accelerating",
      "is_stale": false,
      "is_off_pace": true,
      "snapshots_recent": [...]
    }],
    "initiatives": [{
      "initiative": { "title", "status" },
      "expected_impacts": [{ "kpi_id", "expected_impact" }],
      "total_issues": 8,
      "completed_issues": 3,
      "stalled_issues": 2,
      "blocked_issues": 1,
      "project_ids": ["..."],
      "linked_issues": [{
        "id": "...",
        "title": "Publish comparison page",
        "status": "todo",
        "priority": 1,
        "assignee_id": "...",
        "project_id": "...",
        "milestone_id": null,
        "number": 42,
        "blocked": false,
        "updated_at": "2026-03-28T12:00:00Z"
      }]
    }]
  }],
  "standalone_kpis": [...],
  "assigned_issues": [...],
  "project_context": [{
    "project_id": "...",
    "project_name": "Product",
    "board_columns": [{
      "key": "approval_gate",
      "label": "Approval Gate",
      "description": "Use when implementation is complete but needs approval."
    }]
  }],
  "signals": [
    { "type": "kpi_off_pace", "severity": "warning", "message": "..." }
  ],
  "recommended_action": {
    "id": "create_work:...",
    "action_type": "create_work",
    "title": "Create Content pipeline work for paying_customers",
    "target_type": "initiative",
    "target_id": "...",
    "goal_id": "...",
    "kpi_id": "...",
    "initiative_id": "...",
    "source_signal_ids": ["kpi_off_pace:..."],
    "why_now": "paying_customers is off pace, and Content pipeline has no active linked issue.",
    "expected_impact": "Create the missing execution path for the initiative expected to move paying_customers: +30 signups/mo.",
    "evidence": ["KPI \"paying_customers\" is off pace..."],
    "first_step": "Open Content pipeline and define the smallest task that can move paying_customers.",
    "success_criteria": ["Create or update concrete follow-up actions tied to paying_customers."],
    "suggested_write": {
      "operation": "issue.create",
      "title": "Create Content pipeline work for paying_customers",
      "body": "<h2>Why now</h2>...",
      "status": "todo",
      "priority": 1,
      "project_id": "...",
      "initiative_id": "...",
      "kpi_id": "...",
      "initiative_target_id": "..."
    },
    "confidence": "high",
    "caveats": [],
    "quality_checks": [{ "id": "kpi_link", "status": "pass", "message": "Recommendation includes a KPI link." }],
    "usage_guidance": {
      "instructions": [
        "Prefer suggested_write.operation when it matches the current board state and the recommendation is still current.",
        "Preserve goal, KPI, initiative, initiative target, why-now, expected impact, first step, suggested_write, and success criteria evidence in any issue, status update, KPI refresh, or comment you create.",
        "Do not copy deferred busywork, unrelated tasks, or caveat text into write payloads unless it is directly needed for the recommended action."
      ],
      "preserve_fields": ["goal_id", "kpi_id", "initiative_id", "initiative_target_id", "why_now", "expected_impact", "first_step", "success_criteria", "suggested_write"],
      "avoid_payload_sources": ["deferred_busywork", "unrelated_assigned_issues", "stale_recommendations_after_board_change"]
    }
  }
}
```

Heartbeat is org-scoped, but project-bound goals, KPIs, initiatives, issue health, milestone signals, assigned work, and `project_context` are filtered by the caller's project access. Non-guest members can also see unprojected org-level strategy. Shared initiatives can appear with counts and signals based only on accessible work.

Heartbeat also includes `attention_items` for direct current-member notifications such as mentions, assignments, assignee comments, and creator-visible status changes. Each attention item includes `id`, `source`, `event_type`, `severity`, `action_kind`, resource fields, `target_path`, `created_at`, and `ack_endpoint`; after handling the referenced item, call `ack_endpoint` so the notification is acknowledged and removed from later heartbeat attention results. `attention_summary` includes counts such as `mentions`, `assignments`, `blockers`, and `total_unread`.

Current-member notifications can use `event_type` values such as `mention.created`, `issue.assigned`, `comment.added`, and `issue.status_changed`. Notification preferences use `event_type` (currently `mention.created`), `channel` (currently `in_app`), and `enabled` for current-member mention opt-out. Setting `enabled: false` for in-app `mention.created` also attempts to acknowledge that member's currently unread mention notifications; when cleanup succeeds, they no longer appear in notification lists or heartbeat `attention_items`.

Agents should follow `recommended_action.usage_guidance`: prefer `suggested_write.operation` when it still matches the board, preserve KPI/initiative/initiative-target/why-now/expected-impact/first-step/success-criteria evidence in any write, and avoid copying deferred busywork or unrelated assigned tasks into issue or comment payloads. When `start_work` uses `suggested_write.operation: "issue.update"` with a body, apply the status update and preserve that body as an issue comment; `PATCH /issues/{issueId}` accepts `comment_body` for this same-request progress note.

`recommended_action` is a deterministic strategy-backed next action built from heartbeat context. MVP action types are `create_work`, `start_work`, `escalate_blocker`, and `refresh_metric`; suggested writes may prefill issue creation, issue status updates, blocker comments, or KPI refresh requests. Issue-create bodies are HTML for Atoll's rich-text issue description; blocker/comment and metric-refresh bodies are plain text.

## Strategy Audit Response

`GET /api/orgs/{id}/strategy/audit` returns findings (sorted critical → warning → info), each with a concrete `suggested_fix`, plus summary counts.

```json
{
  "findings": [
    {
      "type": "initiative_orphaned",
      "severity": "warning",
      "title": "\"Content pipeline\" is not attached to a goal",
      "message": "This initiative is not linked to any goal...",
      "suggested_fix": "Attach it to a goal: PATCH /api/orgs/{orgId}/initiatives/<id> { \"goal_id\": \"<goalId>\" }",
      "initiative_id": "..."
    }
  ],
  "summary": { "total": 7, "critical": 1, "warning": 4, "info": 2 },
  "counts_by_type": { "initiative_orphaned": 2, "goal_missing_kpi": 1 }
}
```

Each finding carries whichever entity ids apply: `goal_id`, `kpi_id`, `initiative_id`, `initiative_target_id`, `issue_id`, `milestone_id`, `project_id`. Finding `type` values:

- Structural: `initiative_orphaned`, `kpi_orphaned`, `goal_missing_kpi`, `goal_missing_initiative`, `dangling_initiative_project`, `dangling_initiative_issue`, `dangling_initiative_milestone`
- KPI health: `kpi_unrecorded`, `kpi_missing_target`, `kpi_stale`, `kpi_off_pace`
- Initiative health: `initiative_missing_impact`, `initiative_missing_execution`, `initiative_stalled`, `initiative_target_missing_execution`, `initiative_target_overdue`, `initiative_target_blocked`
- Execution: `issue_blocked`, `issue_overdue`, `milestone_overdue`

## Analytics Response

```json
{
  "statusDistribution": [{ "status": "done", "count": 42 }],
  "priorityBreakdown": [{ "priority": 1, "count": 15 }],
  "assigneeWorkload": [{ "assignee_id": "...", "display_name": "...", "count": 8 }],
  "dailyCounts": [{ "date": "2026-03-01", "created": 5, "completed": 3 }]
}
```

---

## Enums

| Domain | Field | Values |
|--------|-------|--------|
| Task | `status` | `backlog`, `todo`, `in_progress`, `done`, `cancelled` (custom per project via board-columns) |
| Board column | `description` | Optional stage criteria or agent guidance |
| Task | `priority` | `0` (urgent), `1` (high), `2` (medium), `3` (low) |
| Task update request | `comment_body` | Optional Markdown/plain text or rich-text HTML comment body created with the issue update; stored and returned as sanitized HTML |
| Task | `recurrenceType` | `daily`, `weekly`, `monthly`, `yearly` |
| Goal | `status` | `active`, `achieved`, `missed`, `paused`, `cancelled` |
| KPI | `unit` | `count`, `percentage`, `currency`, `duration`, `ratio`, `custom` |
| KPI | `target_direction` | `increase`, `decrease`, `maintain` |
| KPI | `source_type` | `manual`, `webhook`, `api_poll`, `formula` |
| KPI snapshot | `source` | `manual`, `webhook`, `api_poll`, `formula`, `agent` |
| KPI HTTP sync | `status` | `draft`, `published`, `disabled` |
| KPI HTTP sync secret | `placement` | `authorization_bearer`, `x_api_key` |
| KPI HTTP sync run | `status` | `queued`, `running`, `success`, `error` |
| Initiative | `status` | `proposed`, `active`, `completed`, `paused`, `cancelled` |
| Status update | `status` | `on_track`, `at_risk`, `off_track` |
| Member | `role` | `owner`, `admin`, `member`, `guest` |
| Project member | `accessLevel` | `view`, `edit`, `admin` |
| Automation | `trigger_event` | `issue.created`, `issue.status_changed`, `issue.assigned`, `issue.priority_changed` |
| Heartbeat signal | `type` | `kpi_off_pace`, `kpi_stale`, `issue_stale`, `issue_blocked`, `milestone_overdue`, `initiative_stalled`, `initiative_target_due_soon`, `initiative_target_overdue`, `initiative_target_blocked`, `webhook_failing` |
| Heartbeat signal | `severity` | `info`, `warning`, `critical` |
| Custom view | `display_mode` | `board`, `list` |

## Response Format

All endpoints return JSON. Successful: `200` or `201`. Errors: `{ "error": "message" }` with `400`, `401`, `402`, `403`, `404`, `409`, or `500`.

REST list responses use resource-specific keys by default. Main list endpoints support `?shape=envelope` or `?response_shape=cli` to return `{ resource, items, total, limit, offset, nextOffset, truncated, hint }`.

## Notes

- All timestamps are ISO 8601 in UTC
- Descriptions support Markdown; comment bodies accept Markdown/plain text or rich-text HTML and are stored as sanitized HTML
- Board columns (statuses) are customizable per project -- query `/board-columns` for available statuses and optional descriptions
- Default statuses for new projects: `backlog`, `todo`, `in_progress`, `done`
- `cancelled` is always valid but not shown on the board
- Agent actions appear in the activity feed with the agent's name
- Changes via API appear in real-time on the web board
