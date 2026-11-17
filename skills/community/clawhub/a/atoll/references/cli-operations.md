# CLI operations

Read this reference for routine Atoll CLI installation and resource operations. Load a more specific reference as well when the task involves the local runner, strategy heartbeat, execution lifecycle, or an integration.

## Quick Start — CLI (recommended)

Install globally or use via npx:

```bash
npm install -g @atollhq/cli   # or: npm exec --yes --ignore-scripts --package @atollhq/cli@latest -- atoll ...
```

Configure once:

```bash
atoll auth login --key sk_atoll_...
atoll config set-org org-uuid
```

`atoll issue list` and `atoll issue create` apply the selected default team unless a command-level `--team` override is passed. Issue command `--project` flags accept a project ID, slug, or exact name, including list and bulk defaults. In bulk JSON items, `project` accepts those references while `projectId` and `project_id` are canonical IDs. `--milestone` accepts a milestone ID, or an exact milestone name when a project is selected with `--project` or the active profile's default project.

Moving a blocker issue between projects requires one explicit destination release
column per dependency. REST callers pass
`dependencyReleaseMappings: [{ dependencyId, releaseColumnId }]`; REST also
accepts `dependency_release_mappings` and legacy `releaseColumnMappings`, with
`dependency_id` and `release_column_id` item aliases. MCP callers use
`dependency_release_mappings: [{ dependency_id, release_column_id }]`. The CLI
accepts `--dependency-release-mappings` with camelCase items
`[{ dependencyId, releaseColumnId }]`. A projectless move is rejected when the
issue blocks other work. Do not infer a destination column from a label or
position.

`atoll issue list --open` excludes terminal statuses `done` and `cancelled`,
plus archived issues, while preserving every custom and other non-terminal
status. It composes with other list filters, ordering, pagination, and JSON,
and cannot be combined with `--include-archived`.

Project and issue lists default to effectively active work. Use
`--archive-scope archived` for archived work or `--archive-scope all` for history.
Use `issue list --q <query>` with the same scope. `--include-archived` remains
an issue compatibility alias for `all`. Open-work filtering always excludes inherited
and individual archive. Project archive/restore requires owner/admin access;
restore preserves individual task archives and checks plan capacity atomically.
An archived project's work is read-only until project restore.

## Discover members

Use one member directory for humans and agents. Resolve a project by UUID, exact
slug, or exact name, then filter by member type and display name:

```bash
atoll member list --project project-slug --type human --search "Ada" --json
atoll member list --limit 25 --offset 25
```

The result is bounded to 25 members by default and 100 maximum. It returns
stable member IDs that can be used with issue assignment commands. The matching
MCP tool is `atoll_list_members`; it lists collaborators, while
`atoll_list_agent_profiles` selects the caller identity.

Full REST issue-list items include the canonical project-prefixed `identifier`
and collision-free `projectSlug` for project issues, or `null` for projectless
issues. Compact board/list views do not include these fields.

Common commands:

```bash
# Agent orientation
atoll heartbeat
atoll heartbeat --signals-only
atoll heartbeat --severity critical
atoll heartbeat --json
atoll heartbeat --full --json
atoll heartbeat --since <ack-cursor> --json
atoll heartbeat --cursor <page-cursor> --json
atoll heartbeat --ack <terminal-ack-cursor> --json
atoll agent-context

# List tasks
atoll issue list --json
atoll issue list --open
atoll issue list --status todo --priority 1 --limit 25
atoll issue list --scope blocked --initiative initiative-uuid --order-by due_date --order-dir asc

# View a task
atoll issue get ATOLL-42
atoll issue view ATOLL-42   # alias kept for humans
atoll issue delivery-context ATOLL-42

# Discover compact issue Artifacts, then fetch one body explicitly
atoll artifact list ATOLL-42
atoll artifact get <artifact-id> --issue ATOLL-42
atoll artifact create ATOLL-42 --kind implementation_plan --title "Implementation Plan" --body-file plan.md
atoll artifact update <artifact-id> --issue ATOLL-42 --expected-revision-id <revision-id> --body-file plan.md

# Create a task
atoll issue create --title "Fix login bug" --status todo --priority 1
atoll issue create --title "Plan rollout" --project project-slug --milestone "Launch"
atoll issue create --title "Weekly status review" --due-date 2026-07-06 --recurrence weekly
atoll issue create --title "MWF status review" --due-date 2026-07-06 --recurrence weekly --recurrence-days mon,wed,fri --recurrence-mode schedule --recurrence-time 09:00 --recurrence-timezone Asia/Singapore
atoll issue upsert --match-title --project <project-id> --title "Fix login bug" --status todo
atoll issue bulk-create --file ./issues.json --continue-on-error

# Update a task
atoll issue update ATOLL-42 --status in_progress
atoll issue update ATOLL-42 --status in_progress --comment-body "Starting this because the activation KPI is off pace."
atoll issue upsert ATOLL-42 --status in_progress
atoll issue bulk-update --file ./updates.json --dry-run

# Assign a task
atoll issue assign ATOLL-42 --to <user-id>
atoll issue assign ATOLL-42 --to self

# Comments
atoll comment add ATOLL-42 --body "Working on this now"
atoll comment add ATOLL-42 --body "tagging..." --mention-member <member-id>
atoll comment add ATOLL-42 --body "tagging..." --mention "Raphael Ubales"
atoll comment add ATOLL-42 --body "Agent update" --source-harness codex --source-thread-id <thread-id>
atoll comment add ATOLL-42 --body "Continuing this" --reply-to-comment <comment-id>

# --mention-member uses a stable Atoll org member ID; --mention exact-matches display names and fails on ambiguity.

# Labels, notifications, subtasks, activity
atoll label list
atoll label add ATOLL-42 bug
atoll notification list --json
atoll notification ack notification-uuid
atoll inbox list --json
atoll inbox view email-uuid --json
atoll inbox triage email-uuid --category support --priority 1 --status action_required
atoll inbox resolve email-uuid --note "Handled in ATOLL-123"
# Draft only; this does not send:
atoll inbox draft email-uuid --from support@atollhq.com --to user@example.com --subject "Re: Help" --body-file ./reply.txt
atoll subtask create ATOLL-42 --title "Verify recurrence"
atoll activity issue ATOLL-42

`atoll activity issue` reads the canonical task Activity timeline. It accepts
`--limit` (`1..100`) and `--offset` (default `0`) and excludes notification,
webhook, realtime, and delivery records; history from before the atomic
Activity contract can be partial.

# Read-only API fallback for uncommon inspection gaps
atoll api get /api/orgs/$ATOLL_ORG_ID/labels --json

# Dependencies
atoll dependency bulk-add --file ./dependencies.json --continue-on-error
atoll dependency chain ATOLL-42 --direction downstream --depth 2 --json

Dependency reads include a target issue `identifier` and `projectSlug` when the target belongs to a project. Inaccessible targets remain `issue: null`; projectless targets have both fields set to `null`.
Dependencies persist a release point in the blocking project's ordered board columns. Add `releaseColumnId` when creating an edge, or omit it to default to that project's `done` column. Use the dependency API PATCH route to change the release point; reads include `releaseColumnId`, `releaseColumn`, and `satisfied`.
Archiving a blocker preserves the dependency edge and configured release column while satisfying the dependency. Restoring it re-evaluates the same release point and can block the dependent again. Configurable release-point and cancelled-blocker behavior are unchanged.
The blocking issue must belong to a project because its release point is a board
column there; a projectless issue may be the blocked target.
The dependency-release migration backfills existing dependencies to the
blocking project's `done` column. During a rolling deployment, compatibility
reads may omit release fields from older rows; treat missing release metadata as
the legacy open-blocker behavior until the migration is applied.
Dependency reads preserve `release_column_id` as a compatibility alias where
snake_case consumers need it; POST and PATCH accept either `releaseColumnId` or
`release_column_id`. When deleting a board column, migrate issue
statuses and dependency release references with separate explicit targets.

`atoll dependency chain <identifier>` reads a bounded normalized dependency
graph. Use `--direction upstream|downstream|both` (default `both`),
`--depth` (default `2`, maximum `5`), `--limit`, and `--cursor`. Readable nodes
include readiness and release-condition state. Restricted nodes use opaque
tokens and `readiness: "unknown"`; never infer their issue identity. The cursor
is signed and revision-bound; graph changes while paging return `409 Stale
dependency chain cursor`, so restart without the cursor.

# Graph plans
atoll plan validate --file ./plan.json
atoll plan apply --file ./plan.json --dry-run

# Safe removal
atoll issue archive ATOLL-42
atoll issue unarchive ATOLL-42
atoll issue delete ATOLL-42 --dry-run
atoll issue delete ATOLL-42 --force

# Report friction to Atoll maintainers
atoll feedback "The status error should list custom board statuses"

# Projects & milestones
atoll project list
atoll project list --archive-scope archived
atoll project list --archive-scope all
atoll project archive <project>
atoll project restore <project>
atoll board-column create --project <project> --key review --label "In Review" --description "Ready for review"
atoll project delete <project-id> --confirm DELETE
atoll milestone list --project <project-id>
atoll milestone upsert --project <project-id> --name "v1.0" --date 2026-06-01

# Goals, KPIs, and initiatives
atoll goal create --title "Reach 100 paying customers by Q2" --target-date 2026-06-30
atoll kpi create --name paying_customers --goal "Reach 100 paying customers by Q2" --unit count --target 100 --current 34
atoll kpi create --name mvp_tasks_done --goal "Launch MVP" --internal-task-completion
atoll initiative create --title "Content pipeline" --goal "Reach 100 paying customers by Q2" --status active
atoll initiative delete "Content pipeline" --confirm DELETE
atoll initiative kpi link "Content pipeline" paying_customers --impact "+30 customers/mo"
atoll initiative target create "Content pipeline" --title "Publish 10 comparison posts" --mode progress --target 10 --current 0 --unit count --unit-label posts
atoll initiative target create "Retailer coverage" --title "Get 5 retailers live by July 5" --mode gate --target 5 --current 0 --unit count --unit-label retailers --target-date 2026-07-05 --due-soon-days 7
atoll initiative target issue link "Retailer coverage" "Get 5 retailers live by July 5" ATOLL-42
atoll kpi snapshot add paying_customers --value 42 --initiative "Content pipeline" --issue ATOLL-42 --note "End-of-week Stripe check"
atoll kpi snapshot list paying_customers --include-attribution --json
atoll heartbeat --explain-kpi paying_customers --json

# Audit the strategy chain for gaps (orphaned initiatives, goals with no KPI, etc.)
atoll strategy audit
atoll strategy audit --severity critical --json
```

Prefer the CLI for routine task operations, heartbeat checks, comments, feedback, and strategy setup. Use direct API calls when the CLI does not expose the needed endpoint yet.

CLI JSON conventions:

- Use `--json` for machine-readable output.
- List commands return `{ resource, items, total, limit, offset, nextOffset, truncated, hint }`.
- Project-scoped `atoll issue list --json` includes `project_context`; `atoll issue get/view --json` includes `status_column` plus `project_context` when available.
- For initiative execution context via API, `GET /api/orgs/{id}/initiatives/{initiativeId}/issues?details=1` returns accessible task details from linked projects, direct issue links, and linked milestones.
- Diagnostics and errors go to stderr.
- Machine-readable JSON preserves API strings exactly; human terminal output removes ANSI/VT, control, and bidirectional formatting characters from API-supplied strings.
- Interactive CLI update notices also go to stderr and are suppressed for JSON/non-TTY/CI/completion flows.
- `atoll agent-context` returns a versioned command/flag manifest, available profile context, and structured `cli.update_available` metadata.
- Weekly issue recurrence accepts unique selected weekdays with `--recurrence weekly --recurrence-days mon,wed,fri --recurrence-mode schedule --recurrence-time 09:00 --recurrence-timezone Asia/Singapore`. Read JSON exposes normalized `recurrence_days` and `recurrence_schedule`; unrelated updates preserve the schedule. Scheduled recurrence intervals are limited to `10000`. Use `--recurrence-mode schedule` with `--recurrence-time HH:MM` and `--recurrence-timezone IANA/Zone` to create the next task from the maintenance sweep while the current task remains open; `completion` remains the default and can retain larger positive intervals.
- `atoll heartbeat` uses compact delivery by default. Compact JSON is bounded to 25 signal groups and 16,384 UTF-8 bytes, with `counts`, `delta`, and `page`. Follow `page.next_cursor` until the terminal page, then acknowledge its `page.ack_cursor` with `atoll heartbeat --ack <cursor> --json`. Use an acknowledged cursor with `--since`; invalid or stale cursors return an error, and an expired baseline sets `delta.reset_required: true`. If a requested REST
`max_bytes` cannot fit the mandatory actionable record and compact response
envelope, the API returns `413 heartbeat_budget_too_small` without advancing a
page cursor or terminal receipt; retry with a larger budget or the 16 KiB
default. Use `--full` for the legacy full context; full mode cannot combine with `--since` or `--cursor`.
- Compact signal groups include dependency blockers grouped by root blocker and release condition. Expected waits are suppressed for an unsatisfied dependency when the readable blocker is before its release column and there is no active stall, threatened or overdue commitment, or explicit deadline, gate, permission, or stale anomaly. An unowned backlog or Todo blocker by itself is an ordinary wait and never alerts. Actionable groups surface active stalls, threatened or overdue commitments, and explicit anomalies; escalation metadata alone does not surface an expected wait. Initiative-target and stalled aggregates are also suppressed when every underlying dependency is an expected wait. Groups can include a bounded `suggested_read` REST, CLI, or private-MCP call. Public plugin MCP keeps legacy full heartbeat behavior; private MCP supports compact heartbeat, `atoll_ack_heartbeat`, and `atoll_get_dependency_chain`.
- `atoll heartbeat --json` includes the structured `cli` update metadata for agents, plus direct `attention`/`attention_items` and `recommended_action` when Atoll can propose one concrete strategy-backed next action. Handle direct attention items first, then call each handled item's `ack_endpoint`. Follow `recommended_action.usage_guidance`: prefer `suggested_write.operation` when it still matches the board, preserve KPI/initiative/initiative_target/why-now/expected-impact/first-step/success-criteria evidence, and avoid copying deferred busywork into issue or comment payloads. If a `start_work` recommendation uses `issue.update` with a body, update the issue status and preserve that body as an issue comment; `PATCH /issues/{issueId}` accepts `comment_body` for this same-request progress note.
- Authorized humans can configure an agent's included heartbeat sections and generated-signal focus in the Atoll **Heartbeats** UI. The saved policy is applied by the API before CLI or MCP request-level narrowing; it never changes project access, and existing heartbeat commands require no new arguments.
- GitHub `workflow_run` signals are accepted only when HMAC-signed and completed, then reread and matched exactly by repository, PR, workflow path, run attempt, and head SHA. Pull-request runs require provider PR membership. A completed `workflow_dispatch` run can have an empty PR list; Atoll requires exactly one distinct current linked PR and confirms its numeric repository IDs, PR identity, head SHA, and branch through GitHub. Several issues can link to that same PR. Ambiguous links, fork heads, changed heads, and newer runs do not produce verification. Signed nonterminal notifications are acknowledged without evidence. Manual dispatch does not emit the generic `ci.run.completed` automation trigger. Workflow verification is disabled by default and observe-only until an owner/admin enables it in **Settings > Integrations > GitHub**. `attention` mode can add one bounded `verification.completed` attention item through authorized REST or CLI heartbeat for exactly one eligible current agent assignee or, when there is no unambiguous assignee, an eligible configured delivery agent. The public MCP heartbeat excludes this private event type. Unresolved recipients and cancelled, obsolete, superseded, mismatched, or unreadable runs create no attention. Owners and admins can configure 1–10 workflow paths of at most 255 characters each; the bounded evidence list defaults to 25 items and accepts a maximum `limit` of 100. Signed pull-request writes and reconciliation bind PR links to the stable GitHub repository ID, so repository renames keep existing workflow evidence linked. Do not expect raw payloads, secrets, logs, or thread IDs in evidence; owner/admin reconciliation retries pending evidence after current GitHub and PR-link readback.
- Release-added required GitHub hook events mark existing reconciled and already-pending connections pending. The bounded 15-minute service sweep verifies immutable repository identity and upgrades hooks automatically; transient failures remain pending for retry, and owners/admins can reconcile manually.
- Issue delivery context is read with `atoll issue delivery-context <identifier>`; `--json` preserves `{ deliveryContext }`, while TTY output includes the full head SHA, review, actual required checks, configured verification, freshness, blocker, and partial state. The endpoint selects an open PR first, then the latest updated link, then the highest PR number. Required checks union active rulesets and classic branch protection for the base branch and use exact-head check-run/status evidence. `pending` review/workflow state with null provenance means no current-head observation and does not by itself set `partial`. Required-check collection is disabled by default; with the reader disabled, state `disabled` and aggregate `none` do not set `partial`. The server-only `ATOLL_GITHUB_REQUIRED_CHECKS_READ_ENABLED=1` flag enables read-only provider GETs; when enabled, partial or unavailable collection or aggregate `unknown` sets `partial`. This result does not authorize merge, deployment, production testing, or human acceptance. Configured workflows report `required: false`.
- Aggregate review state keeps each reviewer's latest exact-head opinion, ignores comments, and removes dismissed opinions. Change requests win. `approved` means at least one effective approval and no effective change request; it does not prove required-review counts or branch protection.
- `atoll plan validate/apply` consumes `schemaVersion: "atoll.plan.v1"` files with `milestones`, `issues`, `dependencies`, `initiativeLinks`, and `milestoneLinks`; local `key` values can be referenced by `milestoneKey`, `issueKey`, `dependsOn`, `blockedBy`, or `blocks`.

### Bulk create tasks from a plan

`POST /api/orgs/{id}/issues/bulk` with `{ "issues": [{...}, ...] }` (max 50).

## Automation rules

Use `atoll automation list`, `get <rule-uuid>`, `create --file rule.json`,
`update <rule-uuid> --file patch.json`, `test <rule-uuid> [--file preview.json]`,
`runs <rule-uuid> --limit 20`, `enable`, `disable`, and `delete --force`.
Use `delete <rule-uuid> --dry-run` to preview deletion. Use `--json`
for machine-readable results and `--file -` for standard input. Create defaults
to disabled when `enabled` is omitted, but the JSON must include an explicit
`project_id` UUID or `null` for Organization-wide scope; update preserves omitted
fields.
List uses the selected organization and applies a project filter only with
explicit `--project`; it does not inherit the default project.

Rule files use the canonical Automation Rule Fields contract. CI rules require
`project_id: null`, only `create_issue` or `send_webhook` actions, and event conditions. Use
conclusion `failure` and `has_linked_issue: false` for unlinked CI failures.
The action chooses its target project/status and accepts approved
`{{repository}}`, `{{workflow}}`, `{{conclusion}}`, `{{run_url}}` substitutions.
CI `test` sends `{}` by default, uses marked fixed examples, rejects overrides,
and executes no actions. Inspect the preview before explicitly enabling.
Rule writes, tests, and run history require owner/admin access; CLI does not bypass it.
`runs` preserves created issue IDs and interrupted-action evidence. For an invalid
rule, use separate `disable`, `update` while disabled, `test`, and `enable`
operations. Human `get` output includes invalid state and validation paths;
`--json` preserves the API response.

### Select an Artifact source

Use `--source-reference-id <uuid>` on `artifact create` or `artifact update` to
select a canonical External Reference already in the issue's Context. The CLI
resolves its Context link ID before saving. On update, use `--clear-source` to
clear the new revision's source. The two flags cannot be combined. Omit both
to inherit the current snapshot. A source-only update still requires
`--expected-revision-id`.

`artifact get` and write readback request `source_provenance_v1`; text output
shows an authorized source link, and JSON includes `revision.source_reference`.
Historical snapshots survive removal of the live Context link. Atoll does not
import or synchronize the source content. Typed MCP source fields remain
unavailable.

## Manual Web references

For a manual Web link, supply both selectors:

```bash
atoll external-reference link --issue ATOLL-42 --url https://example.com/document \
  --provider external_document --object-type document --json
```

Omitted selectors keep the verified GitHub flow. Manual links contain no provider
proof or fetched content; JSON returns `resolvable: false` and
`resolution_error: "not_verified"`, which means no verification was attempted.
List/get/unlink include manual references. Context v1 and typed MCP creation
remain provider-only; use this CLI command or REST for manual creation.

### Choose the column for recurring tasks

Read `atoll issue list --project <project> --json` for real column UUIDs.
Use `--recurrence-spawn-column <uuid>` on issue create, update, or upsert; use
`--clear-recurrence-spawn-column` to reset to the current project default.
Bulk JSON accepts nullable `recurrenceSpawnColumnId`. Target-only edits preserve
the current status and schedule. Root-owned occurrence edits route to the
authorized series root. After a deliberate series move, completing an older
occurrence creates the next task in the current series project and target.
Untouched legacy completion retains local behavior.

```bash
atoll issue update ATOLL-42 --recurrence-spawn-column <column-uuid> --json
atoll issue update ATOLL-42 --clear-recurrence-spawn-column --json
atoll board-column delete <column-uuid> --project <project> --confirm DELETE \
  --reassign-to <status-column-uuid> --release-reassign-to <release-column-uuid> \
  --recurrence-reassign-to <nonterminal-column-uuid> --json
```

Deletion requires project edit/admin access and exact `--confirm DELETE`.
Its independent replacements follow the existing REST contract. The client
does not retry deletion. After a timeout or connection loss, read the project
workflow and affected issues before deciding whether another request is needed.

## Products and strategy ownership

Products are optional groups within one organization. Product visibility does
not grant access to sibling projects. Product detail returns metadata only;
use the existing project and strategy lists with a Product filter for related work.

```bash
atoll product list --archive-scope all --search "Core" --exact --limit 25 --offset 0 --json
atoll product get <product-uuid> --json
atoll product create --name "Core" --description "Primary offering" --json
atoll product update <product-uuid> --name "Core Platform" --clear-description --json
atoll product archive <product-uuid> --json
atoll product restore <product-uuid> --json
atoll project set-product <project-uuid> --product <product-uuid> --json
atoll project set-product <project-uuid> --none --json
atoll project list --product none --json
atoll goal create --title "Retain customers" --product <product-uuid> --json
atoll kpi list --product <product-uuid> --json
atoll initiative update <initiative-uuid> --product none --json
```

`product view` aliases `get`. CLI Product references accept a UUID or an exact,
case-insensitive authorized name. Ambiguous names fail; use a UUID. Slugs are
output identifiers and remain stable after renames; they are not name aliases.
List filters support `--product <uuid|exact-name|none>` on project, goal, KPI and
initiative. The strategy create/update commands accept the same option.
Omission preserves existing scope or ownership; `none` explicitly selects no
Product (Organization ownership for strategy). `owner_id` still identifies a
member. Initiative `--org-wide` suppresses a configured default project when
an owner-wide list or create is intended.

Product and affiliation writes require organization owner/admin permissions.
Product archive changes no project or task lifecycle. Archived projects can
still change affiliation. Restore an archived Product before assigning to it
or editing its metadata. Detach or move out without restoring it. Strategy
owner changes retain metric history and links, and the existing server rejects
conflicting goal ownership. JSON mutations preserve `{ product, changed }` or
`{ project, changed }`; reads preserve `{ product }`. A repeated lifecycle or
affiliation write returns `changed: false`. Lists use the standard bounded page.
Project/strategy reads retain nullable `product_id` without catalog expansion.

## Project-owned webhook destinations

A project destination has an immutable `project_id`, `purpose: "automation"`,
and `events: []`. It receives targeted automation actions and explicit pings;
it never subscribes to organization broadcasts.

Agents need project read access and separate grants:

- `webhook.create(project)` creates a destination. The same transaction grants
  its creator `webhook.manage(new webhook)` and `webhook.dispatch(new webhook)`
  and increments the agent permission revision. It grants no authority over
  another destination. A human can revoke these grants independently.
- `webhook.manage(webhook)` permits edits, disable/delete, write-only credential
  rotation, explicit ping, redacted history, and proven same-project redelivery.
- `automation.manage(project)` or existing project Admin access permits rule
  management. A project `send_webhook` action separately requires the execution
  actor's current `webhook.dispatch(webhook)` and matching rule, event, and
  destination projects. Project Admin alone grants no webhook permission to agents.

Human project administrators can manage their project's destinations. Current
project access, enabled agent lifecycle, and unarchived project state are
checked again in the durable write and delivery paths. Dispatch revocation
blocks new and queued automation attempts; Manage revocation blocks later
pings and manual replay. An attempt already authorized before a concurrent
revocation can finish. Existing pinned credentials and logical retry identity
remain unchanged. A disabled or deleted destination cannot accept a new attempt.
Organization-owned destinations keep their existing administration and delivery
behavior; omitting project context never grants a project agent organization access.

Use `GET /api/webhooks?orgId=ORG&projectId=PROJECT` for redacted project metadata.
The response includes `can_create`; each row includes `can_manage` and
`can_dispatch`. POST includes `project_id` in the body. Item operations use the
saved owner; optional `?projectId=PROJECT` additionally checks the expected owner.
Changing or clearing `project_id`, adding subscriptions, or using another
project's destination is rejected. Hidden scopes return 404, missing grants 403,
invalid configurations 400, and archived or changed scopes 409.

Bearer and receiver-supplied Standard Webhooks secrets are write-only. Omit them
on update to preserve them. Later reads expose only configuration booleans and
origin-level URL display. The generated Atoll signing secret is returned once
on create, including through typed MCP. Store it securely; normal tool output
may remain in conversation history. Rule dry-run sends nothing; Test webhook
sends a distinct ping. History excludes payloads, responses, raw errors and secrets.

```bash
atoll webhook list --project PROJECT --json
atoll webhook create --project PROJECT --url https://receiver.example.com/atoll \
  --bearer-secret-file - --json
atoll webhook update WEBHOOK --project PROJECT --standard-secret-file /private/receiver-secret
atoll webhook test WEBHOOK --project PROJECT --json
atoll webhook history WEBHOOK --project PROJECT --json
atoll webhook redeliver WEBHOOK DELIVERY --project PROJECT --json
atoll webhook update WEBHOOK --project PROJECT --disable
atoll webhook delete WEBHOOK --project PROJECT --force
```

Secret files or `-` (stdin) keep credentials out of command arguments. Supply
only one secret through stdin per call. Both MCP profiles expose
`atoll_list_webhooks`, `atoll_create_webhook`, `atoll_update_webhook`,
`atoll_test_webhook`, `atoll_list_webhook_deliveries`, `atoll_redeliver_webhook`,
and `atoll_delete_webhook`, with optional explicit `project_id`. API authorization
remains authoritative; agent permission administration remains human-only.

## Agent heartbeat management permissions

Organization administrators can grant **Manage own heartbeat** (`heartbeat.manage_self`) independently from **Manage other agents' heartbeats** (`heartbeat.manage_others`). The self grant uses the Organization target with a null ID. The other-agent grant targets a same-organization agent UUID (`target_kind: agent`) or Organization for all other agents. Other never includes self. No agent receives these grants by default.

Both grants cover briefing policy and outbound configuration, including creating an outbound configuration. They do not grant project access, permission editing, agent lifecycle control or webhook creation/administration. Current followed-owner project access still applies. A project destination also requires the caller's existing `webhook.dispatch` grant on that webhook and project access for both caller and target. Organization destinations require `webhook.organization_manage`.

Settings and previews contain only the caller/target resource intersection. Hidden saved selections return a generic unavailable flag. A delegated full replacement or reset conflicts if it would discard a selection the caller cannot inspect. Self reset can clear stale selections. Missing policy means the organization default, then the built-in default. PUT replaces the full policy/configuration; omitted fields are not explicit null. Preview sends nothing and records no acknowledgement. Test queues a labeled empty payload, returns queued rather than accepted, and uses the actual tester's current authority.

Disabled/revoked callers cannot authenticate. Inactive targets cannot be changed or tested. A grant is not a project or destination permission. Atoll rechecks authority before writes, queueing and each retry. Losing the saved author's authority stops pending delivery; adding a grant later does not revive an old wake. Requests already authorized and in flight cannot be recalled. Integration/setup keys cannot use these grants. Human management rules and the ordinary heartbeat read/ack contract are unchanged.

Use `GET /api/orgs/{id}/heartbeat-targets?limit=25&offset=0` for bounded authorized target discovery. Per-agent management uses `/api/orgs/{id}/agents/{agentId}/heartbeat-policy` (GET/PUT/DELETE), `/heartbeat-preview` (POST), `/outbound-heartbeat` (GET/PUT/DELETE), and outbound `/preview` or `/test` (POST). Responses and errors are private/no-store. Missing, foreign and unauthorized targets are concealed as 404; unsupported actor classes use 403, invalid input 400 and authorized lifecycle/scope conflicts 409. Reconcile a lost write/test response before retrying.

Typed CLI source commands are `heartbeat targets`, `heartbeat policy get|set|reset|preview` and `heartbeat outbound get|set|disable|preview|test`, with `--agent self` or an exact UUID. Set reads the complete JSON from `--body-file PATH` or stdin (`-`). Policy preview accepts an optional draft file. Outbound preview uses saved settings. No URL or secret input is accepted by these commands. Bare `heartbeat` and its cursors/acknowledgement stay unchanged.

Full/private MCP has typed list/get/set/reset/preview/test tools. Existing full/public `atoll_get_auth_context` reports the new grants truthfully. New public heartbeat management tools remain unavailable during the public tool freeze. CLI, MCP and skill package availability depends on a separate package release; source changes do not prove that an installed version contains these commands.


A CLI or full/private MCP outbound test can return `core_write_uncertain` with `retryable: false` after a lost, malformed or server-error response. Read `heartbeat outbound get --agent UUID` or `atoll_get_outbound_heartbeat` for the same agent and inspect authorized history before taking further action. Do not repeat the test while the outcome is unclear. The clients do not retry the POST automatically.
