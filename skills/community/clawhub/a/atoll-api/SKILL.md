---
name: atoll
description: Use Atoll for project, issue, goal, KPI, initiative, milestone, artifact, external reference, PRD, implementation plan, comment, dependency, runner, and workflow operations. Activate for Atoll planning, execution, project-management, local-runner, or integration requests.
metadata: { "openclaw": { "primaryEnv": "ATOLL_API_KEY" } }
---

# Atoll

Base URL: `https://atollhq.com`

Use the available Atoll connection for live data and controlled actions. In MCP
clients, use the connected Atoll tools; do not assume a shell, installed CLI,
local profile, or API key. In CLI environments, prefer the typed Atoll CLI.
Live tool schemas, CLI help, and linked references define the contract.

Heartbeat is compact by default for REST and private CLI/MCP calls. Read the
strategy and heartbeat reference for bounded pages, terminal acknowledgement,
delta cursors, grouped dependency blockers, and the explicit `--full`/`view=full`
legacy response. The public plugin MCP heartbeat remains legacy full mode. If a
requested `max_bytes` cannot fit the mandatory actionable record and compact
envelope, REST returns `413 heartbeat_budget_too_small` without advancing a page
cursor or terminal receipt; retry with a larger budget or the 16 KiB default.
Dependency-chain cursors are signed and revision-bound; graph drift returns `409 Stale dependency chain cursor`, so restart without the cursor.
Private heartbeat also carries durable execution attention. Handle resolved
answers before open requests and acknowledge them with the exact versions; the
acknowledgement never resumes an execution.

Read actor work with `atoll work recommendations --json` or the typed full/public
MCP tool `atoll_get_work_recommendations`. Machines query only self; human target
inspection uses manageable/assignable scope and caller/target permission
intersection. Read the endpoint and field references for current-work inspection,
hidden availability, global bounds, and signed stale cursors. Recommendations are
snapshots: they never reserve, assign, start, retry, or authorize execution.
The existing project-wide read uses `atoll work project-recommendations --project
UUID --json` or MCP `view: project`; actor choices use `work actors --project UUID`
or MCP `view: actors`. Do not rerank locally or treat failure chronology as retry
supersession.

## Route to the relevant reference

Read only the references required for the current task:

- Authentication, saved profiles, organization or project selection, and
  environment conflicts: [authentication-and-profiles.md](references/authentication-and-profiles.md)
- PRDs, implementation plans, Artifact discovery, links, and revisions:
  [artifact-workflow.md](references/artifact-workflow.md)
- Routine CLI commands for issues, comments, goals, KPIs, initiatives,
  dependencies, artifacts, and other resources:
  [cli-operations.md](references/cli-operations.md)
- Installing, diagnosing, configuring, or operating the headless local runner,
  repository bindings, loopback UI, leases, or recovery:
  [local-runner.md](references/local-runner.md)
- Configure GitHub verification with `resume` only when the exact PR, commit,
  runner host, and preserved Codex thread can be bound. The mode is disabled by
  default and fails closed when the binding or verification event is uncertain:
  [api-fields.md](references/api-fields.md#external-operational-delivery-context)
- Strategy, KPI pace, initiatives, heartbeat signals, autonomous prioritization,
  and common strategy workflows:
  [strategy-and-heartbeat.md](references/strategy-and-heartbeat.md)
- Agent executions, evidence, human-attention requests, resolution, and
  version-fenced lifecycle transitions:
  [execution-and-attention.md](references/execution-and-attention.md)
- Remote MCP exposes typed execution and requester-attention tools in both
  profiles. Use the lifecycle guidance in the execution reference; human
  resolution and runner/harness control remain outside those MCP tools.
- The public MCP profile also exposes typed issue, dependency-chain, label,
  subtask, strategy audit, activity, notification, project, board-column, goal,
  and KPI tools. Use the existing API authorization and exact field contracts;
  `atoll_delete_project` needs `confirmation: "DELETE"` and owner/admin access.
  It can still fail while linked Artifacts or active executions block deletion.
  Archive and unarchive emit the normal `issue.updated` webhook event. When a
  core write returns `core_write_uncertain`, read the resource and reconcile
  before replay; the server does not retry automatically. Goal and KPI tools
  accept exact human-readable goal titles and KPI names as documented in the
  API references.
- Automation-rule create, update, enable, disable, and delete can also return
  `core_write_uncertain`. For a create, list rules in the same scope and get a
  possible match by UUID. Set `project_id` to `"none"` for organization-wide
  rules. For other writes, get the exact rule and compare its definition or
  enabled state; for delete, check whether its UUID remains in the list.
  Reconcile before retrying any uncertain rule write.
- Local runner lifecycle management associates leases with canonical executions,
  uses a durable private outbox, and resumes resolved human attention only with
  the exact retained thread and closed IDs/outcome; notification and GitHub
  resume contracts remain separate.
- Remote MCP setup, GitHub repository and External Reference tools, AI-assisted setup, KPI HTTP sync, or advanced REST access:
  [integrations-and-api.md](references/integrations-and-api.md)
- Completed manual GitHub workflow dispatches require one current linked PR and
  canonical same-repository head and branch proof. Nonterminal notifications
  create no evidence; manual dispatch does not trigger generic CI automation.
- GitHub pull-request delivery context, required checks, and exact-head evidence:
  [api-fields.md](references/api-fields.md#external-operational-delivery-context)
  A `plan_restricted` required-check error is actionable plan-unavailable
  evidence; keep configured workflows separate because they remain `required: false`.
- Cross-resource authorization, privacy, automation, attachment, feedback, and
  other platform-specific rules: [platform-rules.md](references/platform-rules.md)
- Exact endpoint inventory: [api-endpoints.md](references/api-endpoints.md)
- Request and response fields, enums, and validation:
  [api-fields.md](references/api-fields.md)

Outbound webhooks support optional Standard Webhooks signing with a receiver
supplied canonical `whsec_` secret. Read the webhook references before creating
or updating a destination; signing secrets are write-only and automatic retry
delivery ids remain stable. Grok Automations and Hermes support this receiver
contract; see the integration reference for their setup and event caveats.

The human-only manageable-agent inventory includes admin-only personal owner
names and shared agent/integration capacity. Non-admins receive null owner and
capacity metadata. See the Agent Fields reference; machine callers remain
forbidden on this management route. API-key integrations continue to consume
the agent allowance, and failed billing reads never imply zero usage.

Agent creation can select an allowlisted built-in icon with `avatarPreset`.
Manage an existing guest agent icon through the member avatar endpoint: upload
a custom image with `POST`, select a built-in preset with `PATCH`, or remove it
with `DELETE`. Read [api-endpoints.md](references/api-endpoints.md) and
[api-fields.md](references/api-fields.md) for the exact contract and limits.

For automation rule V1 actions (including create issue and send webhook), explicit project or
organization scope, CI create-or-webhook rules, scheduled `schedule.issue_time`
rules, event conditions, validation, safe
disabling, repair, and example-only CI dry runs, read [Automation Rule Fields](references/api-fields.md#automation-rule-fields).
Use `atoll automation` for rule management, previews, and run history; see
[CLI operations](references/cli-operations.md#automation-rules).
Both full/private and public MCP profiles also expose typed list, get, create,
update, enable, disable, test, run-history, and delete tools. MCP creation
requires explicit scope and always leaves the rule disabled; test is a dry run.
Use the same separate disable, repair, test, and enable sequence for invalid
rules. Project Admins may manage bounded rules and authorized history in their project; send_webhook additionally needs the matching destination and explicit Dispatch grant. Organization-wide rules retain organization authorization. Project rules cannot change scope or create issues outside their source project.
REST rule lists accept `?project_id=<UUID>` for exact project rules or
`?project_id=none` for organization-wide rules only. Omission lists all rules
in the organization. See [list filter access and validation](references/api-endpoints.md#automation-rules).
Rule creates require an explicit `project_id`: use a project UUID for project
scope or `null` for organization scope. Partial updates preserve the saved
scope when `project_id` is omitted; include it only when intentionally changing
scope. An invalid rule executes no actions. Repair an invalid rule with
separate `disable`, `update` while it is disabled, `test`, and `enable`
operations. Enable only after the latest saved revision passes the dry run.

For recurring issues, completion remains the default materialization mode.
Scheduled recurrence uses the existing issue create/update REST and CLI inputs
with a local time and an IANA timezone. Its interval must be at most `10000`;
completion-mode roots can retain larger positive intervals. See
[Task Fields](references/api-fields.md#task-fields) and
[CLI operations](references/cli-operations.md). The recurrence root owns the
schedule. Its occurrences can remain open without delaying later occurrences.
Both MCP profiles expose completion recurrence type/interval and nullable
spawn-column inputs on existing issue create/update tools. Scheduled inputs
remain REST/CLI only. Read the real project workflow before selecting a target.
The next task uses the current series project and target after a series move,
including completion of an older occurrence. Column deletion requires explicit
confirmation and atomic status, dependency, and recurrence remaps. See
[API endpoints](references/api-endpoints.md#recurrence-and-column-deletion-parity).

Do not load every reference by default. Start with this entrypoint and load a
topic reference only when the requested operation needs it.

## Workflow contract

### Select the actor and project

For actor-dependent MCP calls:

1. Reuse the `profile_ref` already established in the current conversation.
2. If none is established, call `atoll_list_agent_profiles` before an
   actor-dependent read or write.
3. Select a profile directly when the user names it. Otherwise select a unique
   profile only when the organization or project clearly identifies it.
4. Ask when multiple authorized profiles remain plausible.
5. Include the chosen `profile_ref` in every later actor-dependent call.

A `profile_ref` is an opaque selector, not a credential. Do not persist it,
expose it as a secret, silently switch actors, or infer identity from a mutable
server-side active profile. If the selector is invalid, rediscover profiles. If
no profile is authorized, explain that the user must authorize one.

For CLI work, use the named profile required by the repository or user. Resolve
the organization and project from live accessible data. Do not carry mutable
IDs or board mappings across conversations without checking them.

### Read before write, then verify

For state-changing work:

`resolve actor -> resolve organization/project -> read the target -> inspect
linked context when relevant -> make the smallest required write -> read back
the changed resource -> verify the requested final state`

Before creating work, search for a matching issue, milestone, goal, KPI, or
initiative or Artifact. Update the existing resource when it represents the request. Never
invent an ID, success response, stored value, or visible state.

Readback is mandatory for requested mutations. Report both the stored value and
the user-visible value when both exist, and state anything that could not be
verified.

Use the narrowest available typed command or tool. Use raw REST only when the
typed surface does not cover the operation and the current environment authorizes
REST access. In MCP clients, if a required tool is unavailable, report that
limitation; do not bypass it through CLI or raw API access. Do not duplicate
tool schemas from memory.

### Preserve the Atoll model

- Goals describe directional business outcomes and deadlines.
- KPIs measure business outcomes and pace.
- Initiatives are bets expected to move one or more KPIs.
- Initiative targets measure commitments or launch gates.
- Milestones are delivery checkpoints.
- Issues are executable work.

Preserve links between these layers. Do not turn them into interchangeable
standalone tasks.

### Resolve workflow from live data

Board columns belong to projects. Use `atoll_get_project_workflow`, then
`atoll_move_issue` (or the corresponding typed CLI operation), instead of
guessing. Match the visible destination label and verify both the stored status
key and visible label after the move. Never treat a key such as
`ready_to_build` as universal.

### Preserve archive state

Project and issue collections default to effectively active work. Use the
explicit `archive_scope` filter for archive/history reads; an exact authorized
reference can still resolve archived work. A task is archived when its own
`archived_at` is set or its parent project is archived. Check `archive_reason`
and `effective_archived` before selecting work; never infer eligibility from
workflow status alone.

Use `atoll project archive <project>` or `atoll project restore <project>`
in CLI environments, or typed
`atoll_archive_project` / `atoll_restore_project` in either MCP profile.
Organization owner/admin access is required. Archived projects are read-only,
including their tasks. Project restore preserves independent task archives and
can fail atomically on plan capacity. Read the API references for query enums,
response fields, and `PROJECT_ARCHIVED` / `PLAN_LIMIT_REACHED` conflicts.

### Discover collaborators and assignees

Use `atoll member list` or the typed MCP tool `atoll_list_members` to find
authorized human and agent collaborators. Filter by project, member type, and
display name. Use the returned stable member ID in issue `assignee_id` or
`assignee_ids` writes. This directory returns a compact projection and does not
include email or auth identifiers. `atoll_list_agent_profiles` selects the
caller identity; it is not the organization member directory.

### Plan implementation-ready work

Store substantial PRDs and implementation plans in linked Artifacts. Read
[the Artifact workflow](references/artifact-workflow.md) before planning or
revising them. Keep comments to short summaries and Artifact references.

For implementation planning, inspect the relevant project and existing work
first. The result must let another coding agent start without repeating the
product reasoning. Include only the sections that matter:

- Outcome
- Context and current behavior
- Product behavior
- Relevant repository or API surfaces
- Edge cases and compatibility
- Tests
- Acceptance criteria

Keep product decisions, security boundaries, and unresolved questions
explicit. Do not add project-specific workflow keys as universal instructions.

## Safety boundaries

- Credentials belong in approved local configuration or environment variables.
  Never print, store in Atoll content, or include them in commands shown with
  real values.
- Project and organization authorization remain authoritative. Do not retry as
  another identity to bypass a concealed or denied resource.
- Preserve idempotency keys and expected versions for lifecycle writes. After a
  timeout or ambiguous failure, read state before retrying.
- Keep attention requests, comments, evidence, and feedback free of credentials,
  private paths, prompts, logs, or raw sensitive payloads.
- Publication, deployment, production mutation, destructive deletion, and
  external communication require the authority applicable to the current task.

### MCP project events

Modern public OAuth MCP clients can monitor `issue.status_changed`, `attention.created`, and `execution.state_changed`. Each subscription requires an accessible project UUID; discover the live workflow before choosing status filters. Resolve `profile_ref` as for tools. ChatGPT manages callback verification, finite grants, refresh, and unsubscribe through `events/*` protocol methods. API-key/private/stdio clients use tools and Heartbeat. Payloads are compact immutable snapshots; fetch full current state with read tools. No replay is provided.

### Atoll Command Center MCP App

The public plugin offers an app-only global `atoll.open` entrypoint with empty
arguments. The overview shows all authorized agents before profile selection,
with workspace/attention filters and exact open assigned-work counts from every
issue page. Incomplete reads stay visible with Retry, including under attention.
Status labels are project-specific; assignment totals are not unique issue totals
or presence. Each read carries that agent's exact org and opaque `profile_ref`.
Open an agent for assigned work and lazy `filter: "by_me"` Activity; open an issue
for authorized details. Browsing does not write. The model-facing business
tools and modern MCP Events remain available. Full/private and stdio omit the
UI entrypoint.


Opening an agent automatically focuses its authorized discussion scope. Opening
an issue from that agent replaces the scope after a current authorized read.
Returning to All agents clears only owned Atoll context. Optional Working Set
pins stay local until explicitly focused. Project/issue selection, deselection,
clear and profile changes still use official model context. Direct host deep
links and lazy hydration do not add context. Authorization cleanup removes known
stale or inaccessible Atoll references and their owned summary, preserves other
valid selections and foreign content, and offers retry if removal fails.
A stale pending update is reconciled to the latest external host snapshot;
failed preservation warns and offers explicit retry without an update loop. `structuredContent.atoll` contains `source: "atoll"`, `version:
2`, opaque `profile_ref`, and compact agent/project/issue `entities`. Version 1
project/issue envelopes remain readable. Agent references carry only kind,
profile_ref, display_name, designation and organization summary. Other entities
use stable UUIDs,
display identity and already-loaded workflow labels. Read current details with
existing tools under that profile before acting. Saved labels are not authority.
Restoration loads identity first; detail reads are lazy and authorized. Unknown
or malformed Atoll context and foreign host content remain intact. Unsupported
hosts label selection local. Discuss with ChatGPT opens an editable draft;
only the explicit Send to ChatGPT action sends standard `ui/message` user text.
Errors, timeouts and unsupported hosts retain the draft for retry. Navigation,
focus and cancellation send nothing. Prompts identify the authorized agent/issue
and request current Atoll reads; opaque profile_ref stays in structured scope.
No entity bodies, foreign host context, credentials or fake reply are included.


OpenAI deep links use the same canonical app routes: `/`,
`/projects/<uuid>`, `/issues/<uuid>`, `/attention/<uuid>`,
`/executions/<uuid>`. Resolve with the explicitly selected authorized
`profile_ref`; a link is identity, not permission. Invalid shapes/UUIDs are
rejected before reads; unavailable entities never trigger a silent profile
search. Direct host navigation does not add Model-App Context; issue navigation from
an agent focuses that authorized issue automatically. Atoll issue/project web
surfaces show Open in ChatGPT only when the deployment has the explicit public
build-time `NEXT_PUBLIC_ATOLL_PLUGIN_ID`. Never guess this published ID or
confuse it with OAuth/marketplace configuration. Web URLs target global
`atoll.open` and encode the complete canonical path once. Keep normal Atoll
URLs for unsupported hosts (including Android). Local synthetic-ID tests do
not prove published-plugin setup or authenticated provider acceptance.

## Composer mentions (desktop)

In supported ChatGPT desktop Composer surfaces, use `@` to find authorized
issues, projects, human and agent members, goals, KPIs and initiatives. Search
uses currently authorized OAuth connection profiles, not a global or default
actor. Exact display names and authorized human issue identifiers such as
`AH-123` precede loose name matches. Empty queries return a bounded first page;
search does not download a full directory.

The app-only, read-only `search_mentions` extension accepts `{ "query": "text" }`
and returns `{ "items": [...] }` with standard MCP ResourceLinks. Results show
type, organization, profile and available project context. Identical entities
under different profiles keep separate links so the follow-up actor stays clear.
It is separate from the ordinary business tools and `atoll.open`.

A failed profile does not remove results from healthy profiles. Incomplete
searches keep the strict `structuredContent: { "items": [...] }` shape and add
`_meta["atoll/mentions"]: { "partial": true, "skipped": [...] }` plus a safe text
warning. Each skipped entry contains `profile_ref`, `display_name`, HTTP `status`
(or `null` for network/response errors), and a short fixed `reason`; upstream
response bodies and credentials are never included. If every profile fails, the tool returns
`isError: true` with `structuredContent: { "items": [] }`. An empty authorized
profile list is a successful empty result. Transient network and HTTP 5xx reads
retry once after 100 ms; HTTP 4xx and invalid response shapes do not retry.
Concealed 400/403/404 collection reads remain empty pages without warnings.

Resources use `atoll://profiles/<opaque-profile-ref>/<entity-kind>/<UUID>`, where
entity kind is `issues`, `projects`, `members`, `goals`, `kpis` or `initiatives`.
Reads validate the current grant and entity permission under that exact profile.
Malformed routes, revoked profiles and inaccessible records fail without trying
another actor. Resource text contains concise identity and current state,
including `profile_ref`; it excludes long descriptions, histories and secrets.
Fetch current details with the same profile before acting. Mention discovery and
resource reads do not write Atoll records or alter sidebar Model-App Context.

The full/private MCP profile omits this host-specific extension. Normal typed
list tools remain available in both profiles. Provider publication and signed-in
desktop `@` selection are separate acceptance steps; local protocol tests do not
prove that provider flow. No mobile workaround is included.

## Bounded collection search

Projects, goals, KPIs and initiatives accept `q` for case-insensitive literal
substring matching of the display name/title, `q_exact=true` for the complete
name, and `limit`/`offset` for server-side pagination. Defaults in bounded mode
are 25 results, maximum 100, and offset 0. Filtering and authorization precede
pagination; offsets beyond matching results return an empty page with the exact
total. KPI pages include current calculated values. Use `shape=envelope`
(or `response_shape=cli`) for `resource`, `items`, `total`, `limit`, `offset`,
`nextOffset`, `truncated` and `hint`. Supplying a search or pagination parameter
also selects bounded retrieval. Calls without these parameters retain their
legacy resource-key response and full-list behavior.

Members add `member_id=<UUID>` and `q_exact=true` in bounded directory mode.
Identity filtering uses the same collaborator visibility rules and safe fields
as name search; it does not grant access or return credentials or account email.
Members and initiatives also accept `scope=accessible_projects` for a bounded
union under the current actor. The server derives project IDs; callers cannot
supply ID arrays. Guests see only accessible project-linked initiatives and
eligible collaborators. Existing member/admin projectless initiative rights
remain. Empty project access gives guests an empty page. Unknown scope or scope
combined with an explicit project returns `400`. Explicit project scope remains
`project_id` for initiatives and `projectId` for members.

Full issue lists resolve authorized human identifiers such as `AH-123`,
`ATOLL-123`, `#123` or a number before loose title/description matching. They also
accept `q_exact=true` for the full title. The exact flag is rejected with `400`
for compact `view=board`/`view=list`; existing compact search stays unchanged.
The existing issue filters and actor/project authorization still apply.

CLI list commands for projects, goals, KPIs, initiatives and members use
`--search`, `--exact`, `--limit` and `--offset`; issue list uses `--q` with
`--exact`. Member list also supports `--member-id`. These filters are evaluated
by the API. Existing public/private MCP list tools expose `q`, `q_exact`,
`limit` and `offset`; `atoll_list_members` adds `member_id`. Member and initiative
lists expose `--accessible-projects` in the CLI and `scope=accessible_projects`
in MCP. The initiative flag suppresses a configured default project and cannot
combine with `--project` or `--org-wide`. Normal MCP goal/KPI/initiative calls
without query, exact, paging or scope options retain legacy full-list responses.
Composer search uses a constant number of bounded list calls per profile and
entity kind, independent of the number of accessible projects.

## Native interactive issue creation

Use plugin-only `atoll_create_issue_interactive` only when the user asks to choose
or confirm fields in native forms. Pass explicit `profile_ref`. Supporting
registered desktop hosts require protocol 2026-07-28 MRTR, standard form
elicitation and the OpenAI rich-form extension. Unsupported hosts use ordinary
`atoll_create_issue` with complete values. Cancel/decline/invalid/expired state
creates nothing. Final confirmation rechecks profile, project, live workflow,
milestone and searched assignees, then sends one canonical create. Do not retry
an uncertain outcome; reconcile the original issue first. Deterministic creation
keeps its existing required title and behavior. No mobile workaround or client
deployment secret is needed.

Milestone lists accept optional `q`, `q_exact`, `limit`, `offset` and envelope
shape under the existing project endpoint. They filter/page in the database and
preserve progress/status counts. Old absent-option REST/MCP calls stay unpaged;
CLI keeps its old request when no new options are supplied.


### Conversation Working Set

Open the app-only `atoll.working_set` thread entrypoint with `{}` in a supported
host. Search authorized issues/projects and add local pins. Add/remove is local;
explicit selection shares one active canonical Atoll reference through the
existing context controller. Active requires accepted shared context; unsupported
or failed sharing stays local. Removing a pin does not deselect shared context;
unpinned references retain explicit Deselect/Clear selection controls.
Status/priority/assignees refresh through existing reads; dependencies/activity
are lazy. In-panel **Open details** preserves same-instance pins. Profile changes
clear pins and fence old reads. Recreated panels rebuild from current authorized
context only; unshared pins are ephemeral. No thread ID, persistent record,
transcript request, automatic message or Atoll write is added. Native provider
acceptance remains separate from controlled-host evidence.

Artifact source provenance is available through web, REST, and private CLI.
Create/revise accepts `source_external_reference_link_id`; revise omission
inherits and null clears. Add `projection=source_provenance_v1` on Artifact
create/revise or single-revision GET to read an authorized immutable source.
Default REST and typed MCP Artifact output remain unchanged. See the Artifact
field reference for target authorization and unlink semantics.

## Vercel deployment context

Vercel deployment observations use `provider: "vercel"`, `object_type: "deployment"`,
and `provenance: "vercel_api"` in existing scoped External Reference reads.
Metadata contains only label, environment, state, optional exact revision, and
provider effective time. A complete authenticated repository/SHA tuple proves
identity. Later missing fields cannot erase that proof; contradictory known
identity is rejected. Partial observations are never combined to invent proof.
The mapped project always receives the reference. An issue receives it only
when exactly one unarchived issue in that project has the same numeric GitHub
repository ID and exact SHA. Preview/staging supersession is chronological;
production supersession follows an authenticated project production target and
supports rollback to an older build. Deployment evidence does not change issue
status, authorize release, or prove acceptance. Generic list/get/unlink work;
manual link remains GitHub-pull-request-only. Unlink does not suppress later
verified ingestion. See https://docs.atollhq.com/integrations/vercel.

## Compact Context discovery

Use `atoll context list --issue ATOLL-42 --json` or `--project project-slug`
before loading detail. Full/private MCP exposes `atoll_list_context` with exactly
one issue/project UUID. Inspect authority, freshness, current revision/SHA, and
safe summaries; follow each group cursor with the same target/limit and deduplicate
by item ID. Load only the needed existing Artifact, reference, or delivery detail.
See [Context fields](references/api-fields.md#compact-context-index).
The public index and delivery-detail tools remain unavailable pending AH-3067
and release of the public tool freeze. Existing public Artifact and reference
reads are unchanged. Evidence never implies a later delivery or acceptance gate.


Assigned workload filters: MCP `atoll_list_issues` supports `scope: "mine"` and
`open_only: true`. Either input uses the existing compact `view=list` REST path;
true maps to `open=true` and mine includes multi-assignee links. Follow every
`nextOffset` before claiming exact totals. Compact reads can omit identifiers
and retain existing `q_exact` restrictions. Per-project workflow labels must
not be reused across different projects with equal status keys.

## Manual Web references

Use CLI `external-reference link` with `--provider external_document --object-type document`
or the scoped REST route to add a manual HTTPS URL. Content is not fetched or
verified. Typed MCP creation remains GitHub-only; list/get/unlink can read manual
references. See the External References fields reference for trust semantics.

## Agent lifecycle boundary

Only enabled agents can authenticate or receive new work. Disable preserves history and capacity; enable needs fresh credentials and consent and does not resume work. Revoke retains historical identity and is terminal. Lifecycle administration requires a human session; CLI/MCP do not expose it. Read `references/api-endpoints.md` for state/version, capability, replay, and runner-lease rules.

## Product grouping

When grouping projects, use the Products REST contracts in
`references/api-endpoints.md` and `references/api-fields.md`. Products are
optional, same-org metadata; they never grant project access or archive child
work. Owner/admin writes use the dedicated project affiliation PUT endpoint.
Use explicit `product_id: null` to detach through REST or MCP, or `atoll project set-product <project> --none` through CLI. Use the typed Product tools described below.

## Product ownership of strategy

Goals, KPIs and initiatives each have an independent nullable `product_id`.
`null` means Organization ownership; a UUID means a Product in the same organization.
Existing records stay Organization-owned. `owner_id` still identifies a person.
Product ownership is never inferred from a goal, KPI impact or execution project.

Existing POST and PATCH routes accept `product_id`. Omitted on POST means
Organization; omitted on PATCH preserves the owner; explicit `null` detaches.
Owner changes require an organization owner/admin and preserve record IDs,
snapshots, source/sync configuration, targets, history and explicit links.
Lists accept `product_id=UUID` for an exact owner or `product_id=none` for
Organization-owned records. Omit it for all authorized owners. Ownership filters
combine with existing filters before counts and pagination; response envelopes stay unchanged.

A direct KPI/initiative goal link permits the same Product, or Organization
ownership on either side. Two different non-null Product owners conflict.
Moving a goal checks all linked KPIs and initiatives. A conflict returns `409`;
reassign linked strategy first or use Organization as an intermediate owner.
KPI names are unique within one owner, so separate Products can each have an MRR KPI.
Explicit KPI impacts and execution links can cross Product groups within the same
organization when existing access checks permit them. Formula KPIs still use
explicit goal-to-initiative-to-task/milestone links.

Archived Products retain their strategy. Ordinary edits to existing owned records
and moving/detaching out remain allowed; new assignment into an archived Product
returns `409` until restore. Malformed ownership input returns `400`, missing or
foreign Products return concealed `404`, and permission failures keep existing
`403`/`404` semantics. Product identity or access to a contributing project grants
no additional strategy access. Actual owner changes add one projectless
`strategy.product_changed` Activity event with actor, record kind/id and old/new Product IDs.

Typed CLI strategy list/create/update commands accept `--product <uuid|exact-name|none>`.
Both MCP profiles accept `product_id` on list/create/update: lists use a UUID or
`"none"`; writes use a UUID or `null`. Omission preserves existing behavior.
Use `owner_id` only for the human/member owner, independently of Product ownership.

## Typed Product tools

A Product mutation can return `core_write_uncertain` if its result is lost or
cannot be verified. It may already have taken effect. Read the exact Product or
project before another write. For create, search authorized Products by exact
name with `archive_scope: "all"`, inspect candidates with `atoll_get_product`,
and reconcile the requested fields before another create. Names are not unique;
do not blindly retry. Authoritative permission and conflict errors stay unchanged.

Both full/private MCP and the public plugin expose `atoll_list_products`,
`atoll_get_product`, `atoll_create_product`, `atoll_update_product`,
`atoll_archive_product`, `atoll_restore_product`, and `atoll_set_project_product`.
Use `atoll_list_products` to discover authorized UUIDs. Product reads return
metadata only, without child counts or implicit sibling access. Product list
supports `archive_scope` (`active`, `archived`, `all`), `q`, `q_exact`, `limit`
(1–100), and `offset`.

`atoll_update_product` replaces supplied name/description values; null clears the
description. `atoll_set_project_product` replaces or clears existing affiliation.
Both tools advertise `destructiveHint: true`. Omitted update fields stay unchanged.

Product tool IDs are UUIDs. `atoll_set_project_product` requires `product_id`
as a UUID or explicit `null`. Project list accepts optional `product_id` as a
UUID or `"none"` for standalone projects. Goal, KPI and initiative list tools
accept the same filter; their create/update tools accept optional nullable
`product_id`. Omit it to preserve legacy defaults or the existing owner;
`null` selects Organization ownership. Human `owner_id` remains separate.

Public tools require the selected opaque `profile_ref` on each actor-dependent
call. Discover it with `atoll_list_agent_profiles`; never switch profiles to
bypass a denied write. Existing REST permissions remain authoritative, including
owner/admin Product and ownership writes and concealed inaccessible reads.
Mutation outputs retain the server's `changed` flag. Product archive leaves
project/task lifecycle unchanged. Continue to use bounded project and strategy
lists for authorized related records; heartbeat gains no full Product catalog.

CLI: `atoll product list|view|get|create|update|archive|restore`; project affiliation uses `atoll project set-product <project> --product <uuid|exact-name>` or `--none`. Read the CLI reference for nullable ownership and filters.

### Earliest runner starts

Use nullable `agent_not_before` (ISO calendar date) on issue create/update to defer new Atoll runner claims in the saved workspace IANA timezone. Do not derive this gate from start/due dates. Heartbeat keeps assigned tasks and supplies `workspace_date`. Existing work, replay and attention resume continue. `atoll workspace-calendar get|set` and both MCP profiles expose `atoll_get_workspace_timezone` / `atoll_set_workspace_timezone` for timezone access; owner/admin access is required to set the zone. See the task fields and CLI reference.

### Atomic strategy setup

`POST /api/orgs/{id}/strategy/setup` creates a goal, manual KPI, optional
initiative, KPI impact link and optional initial snapshot in one transaction.
Requires organization owner/admin access and the existing projectless strategy
write permissions. Send a UUID `idempotency_key`, `goal_title`, and `kpi_name`.
Optional fields: nullable `product_id`, `goal_description`, `goal_target_date`
(YYYY-MM-DD), `current_value`, `target_value`, `initiative_title`, and
`expected_impact`; `unit` defaults to `count`, `target_direction` to `increase`.
Units and directions use the existing KPI enums. Numbers must be finite JSON
numbers. The same Product applies to all created records.

Returns HTTP 201 with `{ "setup": { "goal_id": "UUID", "kpi_id": "UUID",
"initiative_id": "UUID or null" } }`. Retry the identical request with the same
key after a lost response. The key is scoped to organization and actor; replay
returns the original IDs, including after later edits or deletion. A changed
payload with the same key returns 409 with `code: "idempotency_conflict"`.
Use a new key only for the changed request. Invalid input returns 400; existing
permission, Product archive/tenant, and KPI-name conflict rules still apply.
Any failure rolls back all new records and the replay receipt. This wave adds
the atomic REST operation; typed CLI/MCP chain orchestration remains deferred.

## Human organization role governance

Human organization roles remain owner/admin-managed. Agent role PATCH is deprecated and returns `400 agent_permissions_required`. Use human-only GET/PUT `/api/orgs/{id}/agents/{agentId}/permissions` with `expected_revision` to change scoped agent access without replacing identity, keys or OAuth profiles. An agent cannot expand its own or another agent’s grants.

## Scoped agent permissions

An agent has one stable identity. Humans edit its Projects, Product KPI creation,
individual KPI permissions, Product-wide KPI permissions, and automation access
without replacing its member ID, API keys, or OAuth profiles. Human roles remain
unchanged. Agent `role` is a compatibility projection; it is not the grant source.
Read `GET /api/auth/me` → `auth.permissions` for explicit grants, permission
revision, owner project following, and effective project access with sources.
Use `atoll agent-context --live-permissions` for the selected CLI profile, or
`atoll_get_auth_context` in full/public MCP. CLI context reports conflicts, tenant
mismatch or unavailable reads without switching identities or printing errors.

Project access remains `project_members` View/Edit/Admin. Optional owner following
uses the human owner's current project access only. It never inherits the owner's
organization strategy or administration permissions. Project access does not grant
Product KPI access. New scoped agents have no KPI-create permission by default.

`kpi.create` targets one Product or Organization. An agent must send `product_id`
explicitly: a Product UUID or `null` for Organization. KPI creation, its explicit
creator `kpi.manage` grant, and an optional initial snapshot commit atomically.
The response KPI includes `effective_access: { level: "manage", source:
"explicit_kpi_grant" }`. Creating a KPI grants no access to existing KPIs. Removing
the creator's grant removes access unless another explicit grant covers the KPI.
Names remain unique within their Product or Organization owner; duplicate creation
returns `409`. An archived Product or incompatible Goal cannot receive the KPI.

KPI Read permits reading the measurement. Record includes Read and recording
non-formula snapshots. Manage includes Read, Record, definition/target changes,
and deletion. Ownership changes still require strategy ownership permission.
Product-wide grants cover current and future KPIs under that Product. Organization
scope covers organization-owned KPIs only; `all_kpis` explicitly covers every KPI
in the organization, including all Products. Grants add access; removing a narrow
grant cannot override a broader grant. KPI filtering happens before pagination and
counts. Selected formula measurements stay canonical; source issues and initiative
links require separate access.

Human-only `GET` and `PUT /api/orgs/{id}/agents/{agentId}/permissions` inspect and
replace permissions. PUT requires `expected_revision`, `follow_owner_projects`,
`projects: [{ project_id, access_level }]`, and `grants: [{ capability, target_kind,
target_id }]`. A stale revision or active execution conflict returns `409` without
a partial update. Stop active executions and reload before changing access. Grants
and project membership changes are audited together. Agents cannot administer
grants. Legacy agent role PATCH is rejected with `agent_permissions_required`;
legacy project PATCH remains a compatibility adapter. No CLI/MCP permission-write
tool is exposed because this control requires a verified human session.

Project webhook creation uses `webhook.create(project)`. Creation atomically grants
its agent creator `webhook.manage(new webhook)` and `webhook.dispatch(new webhook)`.
Manage and Dispatch are independently revocable. Sending also requires project
rule management and current project access. Project Admin alone grants agents no
webhook rights. Organization administration retains its explicit organization grant.

**Delete agent** uses terminal revoke. It permanently invalidates credentials and
execution authority, releases the agent slot, hides it from active agent lists and
pickers, and disables active automation rules that execute as that identity. Past
work, attribution, grant history and the member row remain. It cannot be undone.
Disable remains reversible and keeps the slot; enabling requires fresh credentials.
`DELETE /api/orgs/{id}/agents/{agentId}` remains the human-only idempotent adapter.
The stored marker stays `lifecycle_state: "revoked"`. Use **Show deleted agents**
for history. Admin agent list APIs accept `include_deleted=true` for deliberate
history reads.

### Heartbeat task selection

An authorized human can configure per-agent `task_filters` in the existing heartbeat policy and preview exclusions before saving. Rules cover due days in workspace timezone, not-before, assigned or team-unassigned scope, dependency release and recent execution attempts. Existing calls consume the saved policy in full/compact output. Defaults preserve selection; direct attention and strategy keep their controls. See the heartbeat API field reference. No new CLI/MCP command or automatic start is added.

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

### Outbound heartbeat receivers

Humans and explicitly scoped agents can configure conditional outbound heartbeat
delivery. Use the two independent heartbeat management grants described below.
Project and destination authority remain separate. Receivers get bounded `agent.heartbeat` schema v1
items with a stable `wakeId`; deduplicate it across retries. A 2xx means accepted,
never completed. Outbound acceptance does not acknowledge inbound heartbeat or
human attention. Date windows remain calendar-day based. See the heartbeat
API field and endpoint references for settings, test and retry semantics.

### Scoped heartbeat management

Explicit `heartbeat.manage_self` and independent `heartbeat.manage_others` grants authorize per-agent policy and outbound configuration. Other excludes self; webhook dispatch and resource access remain separate. Read the strategy/heartbeat and CLI references before configuring, previewing or testing a heartbeat. Integration/setup keys are excluded. Typed management is full/private MCP only while the public tool freeze remains. Existing public auth context still reports grants truthfully.

If a CLI/full-private MCP outbound test returns `core_write_uncertain`, inspect the same agent’s authorized outbound history before taking further action. Do not repeat the test while its outcome is unclear. See the CLI and strategy/heartbeat references.

### Attention categories and event wakes

Heartbeat policy supports optional attention_categories: assignment, mention,
blocker and execution, under the attention master. Omission keeps all enabled.
Assigned work and assignment events are separate. Outbound informational and
actionable attention require explicit opt-in; accepted event revisions do not
wake again, even with any_eligible_work. Delivery acceptance never reads or
acknowledges notifications or resumes execution. See the strategy/heartbeat and
API field references for canonical mappings, saved-versus-draft previews and
private MCP management. Public management remains frozen.
## API-key request limits

Each API key has separate, shared fixed one-minute budgets: **120 GET reads**
and **60 other requests**. Human sessions and OAuth agent tokens are unchanged.
The exact heartbeat GET, heartbeat/ack POST, and runners/self GET, PUT and
DELETE org routes remain available for signal delivery and runner continuity.
Existing route-specific limits still apply.

On 429 `rate_limited`, wait for `Retry-After` seconds. The JSON body contains
`error`, `message`, `retry_after_seconds`, `suggestions` and `docs_url`.
`X-RateLimit-Limit` and `X-RateLimit-Remaining` describe the selected budget;
`X-RateLimit-Reset` is its reset time in Unix seconds. Successful requests below
20% remaining also include `X-Atoll-RateLimit-Hint` without changing JSON.

Use `atoll heartbeat --signals-only` every **15 minutes or longer** instead of
list loops. Follow signals with scoped reads. For individual issues, inspect
`GET /api/orgs/:id/activity` and fetch issues that changed. Issue lists do not
support `updated_since`. For writes, batch supported operations, back off, and
use an idempotency key where supported; otherwise check existence before create.

Recognized CLI responses include `X-Atoll-CLI-Latest` when a fresh cached npm
version is available, plus `X-Atoll-Upgrade-Command` and `X-Atoll-Upgrade-Docs`.
The server reads https://registry.npmjs.org/@atollhq/cli/latest in the background
with a 500 ms abortable deadline. Requests never wait for this lookup. The
process cache lasts one hour, coalesces refreshes, and retries failures no more
than once per minute. Cold or expired caches produce no latest-version warning
until a refresh succeeds; a failed refresh does not reuse an expired version.
There is no default minimum. `ATOLL_MIN_CLI_VERSION` is an optional explicit
compatibility floor, reported as `X-Atoll-Upgrade` only to older clients.
It remains advisory and does not reject requests. The latest-version notice is
also advisory and appears only when the CLI is behind the published version.
Run `npm i -g @atollhq/cli@latest` or `bun add -g @atollhq/cli@latest`.
The CLI writes one upgrade notice per process to stderr, including error
responses. It also prints 429 advice and the docs URL to stderr. MCP error text
retains all actionable 429 fields. JSON response shapes for successful requests
are unchanged.

See https://docs.atollhq.com/api-reference/rate-limits for details.

## Explicit GitHub PR associations

Link a GitHub pull request through the issue's Add link action or the canonical
External Reference API, CLI, or supported MCP link tool. Issue identifiers in PR
titles, branches, bodies, and commit messages never create associations.
Signed events refresh evidence only for current explicit links. Unlink removes
one issue association; later events cannot restore it. One PR can be linked to
several issues, and each link is independent. A merge does not set an issue to
Done. A saved authorized automation can change status through the normal issue
mutation contract. PR/check/review evidence does not prove human acceptance.

The compatibility GET `/api/orgs/{id}/issues/{issueId}/pr-links` reads canonical
associations only. Compatibility POST delegates to the canonical reference
operation and returns `{ externalReference }`; use the External References
routes for new clients. Historical inferred rows are retained as inactive
internal delivery state, never promoted into associations. Canonical references,
delivery evidence, and audit history are preserved.

## Sub-issues

Use `parent_id` to split one deliverable into full issues. Checklist `sub_tasks`
and recurrence `recurrence_parent_id` remain separate. Only one hierarchy level
is allowed. A child cannot be a parent. Self-parent and cross-organization links
are rejected. Children can use another project in the same organization.

POST and PATCH issue requests accept a parent UUID or `null`. Omit it on PATCH
to preserve the link; send `null` to detach. Attach, detach, and reparent require
edit access to the child and the old and new parents. Creating a child defaults
project, milestone, and team from its parent when those fields are absent.
Moving a child to another project keeps its parent. Deleting or archiving a
parent detaches its children and keeps their issues.

`GET /api/orgs/{id}/issues?parent_id=UUID` filters children before pagination.
`GET /api/orgs/{id}/issues/{issueId}/children?limit=25&offset=0` returns authorized
`issues`, `total`, `limit`, `offset`, `parent`, and `rollup`. Detail responses
include authorized `parent` (id, number, title, project_id) and
`sub_issues_rollup`. Rollups contain `total`, `done`, and `by_terminal_column`,
keyed by each child's project column UUID (canonical `done`/`cancelled` keys for projectless children). Only readable, active children count;
columns with stage `done` count as done. Parent status does not change.

CLI: `atoll issue create --title "Tests" --parent AP-123`,
`atoll issue update AP-124 --parent AP-123`,
`atoll issue update AP-124 --clear-parent`, `atoll issue children AP-123`, and
`atoll issue list --parent AP-123`. Use `--limit` and `--offset` for pages.
Full and public MCP issue create/update accept nullable `parent_id`; list
accepts its UUID filter. Omission preserves old clients. Next-child selection
and heartbeat hierarchy are described below. Checklists and recurrence remain separate.

### Next child and heartbeat hierarchy

Split work that exceeds one PR or one session into deliverable sub-issues,
not checklist steps. Use a milestone when pieces span weeks or form a phase;
more than about a dozen children is a signal to review that choice.

Read the next open, unblocked child with `atoll issue next --parent AP-123`
or MCP `atoll_next_child` with `parent_id` (UUID or issue identifier).
REST: `GET /api/orgs/{id}/issues/{issueId}/next-child` (UUID path).
All surfaces return `{ "issue": { ... } }`, or `{ "issue": null }` when none
remain. Only authorized, non-archived children are considered, including
children in other projects. Terminal columns use each child's project workflow.
Dependency release points determine blocking. Order is priority ascending
(0 highest), null last, then UUID ascending. This read does not claim work,
apply agent assignment/not-before filters, or grant permission to start it.
Check existing execution and runner eligibility before execution.

Heartbeat retains `assigned_issues` for compatibility and adds
`assigned_issue_groups` with readable parent context. Compact actionable child
signals share a parent group. Parent at-risk signals name visible blocked,
stalled (in progress without updates for at least 3 days), or off-pace (past due
in the workspace calendar) children. Hierarchy does not add runnable tasks,
change outbound task eligibility, or close a parent.


### Parent close decisions

Automatic parent close is off by default. Do not guess a done destination.
Closing a parent with open children requires `open_children_action: close` plus
explicit `child_done_columns` for every changed child project, or
`open_children_action: detach` to leave open children detached and unchanged.
All changed issues require edit access. Use `atoll_get_sub_issue_policy` and
`atoll_set_sub_issue_policy` (full/public MCP), or
`atoll project sub-issue-policy PROJECT_ID`. Enabling requires explicit done and
not-done reopen targets. An unauthorized automatic parent change must not block
child completion; inspect the parent's `sub_issues_action`. Automatically closed
parents reopen to the previous valid column or saved fallback; manually closed
parents need review. See the API references for exact request shapes.
