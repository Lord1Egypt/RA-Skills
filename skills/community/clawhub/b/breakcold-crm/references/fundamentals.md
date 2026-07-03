# Fundamentals

The shared plumbing every Breakcold MCP workflow depends on. Read this once when starting a non-trivial session; agents that skip it tend to waste tool calls re-discovering things they already know.

## 1. Endpoints and regions

Breakcold MCP is a Streamable HTTP MCP server. The path is `/mcp/v1`. There are two regional URLs — the user's workspace lives in exactly one:

- **United States:** `https://http.us.breakcold.com/mcp/v1`
- **Europe:** `https://http.eu.breakcold.com/mcp/v1`

**Match the URL to where the user's workspace is hosted.** Cross-region calls are slower and may produce stale data. If you're not sure, ask once and remember.

## 2. Authentication — never ask twice

Two supported modes:

- **OAuth** — preferred when the MCP client supports sign-in. Calls execute as the signed-in Breakcold user and enforce org/workspace/record permissions automatically.
- **Bearer token** — for clients that can't OAuth or for service-style agents. Uses the token's configured scopes and workspace limits.

Org header: `X-Breakcold-Organization-Id` is required when the user belongs to more than one active Breakcold organization. If you get an org-related error on the first call, that header is missing.

**Universal rule:** the user should never have to re-authenticate inside a workflow. If a tool call returns an auth error mid-session, surface a single message:

> "Looks like Breakcold needs you to reconnect. Tap reconnect and I'll pick up exactly where I left off."

Then wait. Don't loop, don't re-attempt, don't ask for credentials in chat — passwords and API keys are never entered through the chat.

## 3. Workspace selection

```
workspaces_list  →  one or many
```

- **One workspace:** pick silently, never mention it.
- **Multiple workspaces:** ask once at the start of the session with the names returned by the API ("Which workspace? Acme HQ or Acme EU?") and cache the ID for the rest of the session.

A second `workspaces_list` in the same session is wasted budget.

## 3.5. Resolving the current user ID

The Breakcold MCP does not expose a dedicated "get me" or "current user" tool. But knowing **who the authenticated user is** matters for almost every write — it's the default assignee for tasks (see `action-tasks.md`), the implicit author for notes, and the actor on breadcrumb activities. The agent should resolve this **as part of the boot sequence**, not on the fly when creating the first task.

### Where the user ID appears

In order of likelihood, the user's ID surfaces here:

1. **`capabilities_list` response** — often includes the authenticated actor's identity along with scopes. **Check this first.** If the response carries an `actorId` / `userId` / `me` field, cache it as `CURRENT_USER_ID` and skip the rest.
2. **`workspaces_list` response** — workspaces typically list their members, and the authenticated actor is one of them. Some responses tag the requesting member explicitly (a `self: true` flag or equivalent); others just include the membership list and you need to cross-reference with the actor token. If you can identify the user from this response, cache and skip.
3. **Any write response** — `records_create`, `tasks_create`, `notes_create`, `custom_activities_create` all stamp the creator's ID on the returned object. `createdBy`, `creatorId`, `authorId`, `actorId` are the common field names. **Read the field on the first write of the session and cache it from then on.**

### What to do when you reach step 3 unresolved

If both `capabilities_list` and `workspaces_list` came back without surfacing the user ID, **don't make a probe call just to learn the user ID** — that wastes a tool call and creates an orphan record. Instead, defer:

- Let the first legitimate write of the session resolve it.
- For that first write, if the tool requires an assignee (like `tasks_create`'s `assigneeUserIds`), call it without the assignee first, read the user ID from the response, then immediately update the just-created task to add the assignee.
- For every write after that, use the cached `CURRENT_USER_ID`.

### What never to do

- **Never make a dedicated probe call just to learn the user's ID.** Don't create a test record, test activity, or test task whose only purpose is to read the creator ID off the response. That's wasted budget and risks leaving an orphan record. The user ID will surface on the first *legitimate* write of the session — wait for that.
- **Never leave `assigneeUserIds` empty/null on tasks the agent creates on the user's behalf.** Unassigned tasks vanish from everyone's queue and the user thinks the workflow silently failed. If you genuinely have no user ID after the steps above, create the task, read the ID from the response, then `tasks_update` to add the assignee. That's an extra call but it's the price of correctness.
- **Never ask the user "what's your user ID?"** They don't know it (it's an opaque string like `hs7wgdn9n31gbw7232j2w5wr6x84jbr9`). Resolve it from API responses.
- **Don't assume one workspace's member list applies to another.** If the user switches workspaces mid-session (rare), re-resolve. Workspace-scoped IDs aren't portable.

## 4. Schema discovery — lazy and cached

The user's CRM schema is composed of four metadata layers. Discover **only what the current action needs**, and cache it.

```
crm_objects_list        →  IDs and names for "Person", "Company", "Deal", and any custom object
crm_fields_list         →  for one object_id at a time
crm_field_options_list  →  for one select/multiselect field at a time
crm_record_views_list   →  for one object_id (only when working with views)
inbox_views_list        →  only when working with inbox views
```

### Discovery cheatsheet by action

| Action you're running              | Discover                                              |
|------------------------------------|-------------------------------------------------------|
| Auto-tasks                         | objects (Person at minimum), fields, members          |
| Pipeline auto-movement             | objects, fields, options for the pipeline-stage field |
| Reports                            | objects, fields, options for status/stage/source      |
| Prospect research                  | objects, fields, options (notes auto-link)            |
| Contact detection                  | objects, fields, options for type/source              |
| CRM setup / reorg                  | everything — start from scratch                       |

### Identifying the "pipeline stage" field

There is no flag called `is_pipeline_stage` on a field. Identify it by:
- Field type is `select` (single-select).
- Field name contains "stage", "status", "pipeline", or the equivalent in the user's language (`étape`, `etapa`, `fase`, `stadium`, etc.).
- It has 4+ options whose ordering implies progression.

If two select fields qualify, ask the user which one — once. Cache the answer on the object so you never ask again that session.

## 5. Attribute types — what you can actually set

Field values you set via `records_create` / `records_update` are typed. Use the right shape per type:

| Type            | Value shape                                            | Notes                                                                |
|-----------------|--------------------------------------------------------|----------------------------------------------------------------------|
| `text`          | string                                                 | Plain string.                                                        |
| `textarea`      | string                                                 | Multi-line text.                                                     |
| `select`        | option ID                                              | Must be an existing option. Look it up via `crm_field_options_list`. |
| `multiselect`   | array of option IDs                                    | Same as select but as an array.                                      |
| `number`        | number                                                 | Integer or float.                                                    |
| `currency`      | `{ amount, currency_code }`                            | ISO 4217 currency code.                                              |
| `date`          | ISO date string `YYYY-MM-DD`                           | No time.                                                             |
| `datetime`      | ISO 8601 string with timezone                          | Always include timezone.                                             |
| `email`         | email string                                           | Validate before sending.                                             |
| `phone`         | E.164 string                                           | E.g. `+33123456789`.                                                 |
| `url`           | URL string                                             | Include scheme.                                                      |
| `location`      | structured location                                    | See API reference for exact shape.                                   |
| `linkedin`      | LinkedIn URL or handle                                 | Treat as URL.                                                        |
| `twitter`       | Twitter URL or handle                                  | Treat as URL.                                                        |
| `facebook`      | Facebook URL                                           |                                                                      |
| `whatsapp`      | E.164 phone                                            |                                                                      |
| `telegram`      | Telegram handle or URL                                 |                                                                      |
| `checkbox`      | boolean                                                |                                                                      |
| `member`        | user ID (from workspace members)                       | For "assignee" / "owner" fields.                                     |
| `relation`      | record ID (or array)                                   | To link Person → Company, Deal → Person, etc.                        |

If unsure of the exact shape, call the matching `crm_fields_get` to inspect.

## 6. Records, conversations, tasks, notes — how they link

This is the part that makes Breakcold special. Hold this model clearly:

- **Records** are the nouns: Person, Company, Deal (and any custom object).
- **Conversations** live in the Inbox. Each conversation has a channel (`email`, `linkedin`, `whatsapp`, `telegram`, `meeting`, etc.) and is composed of **messages**.
- A conversation can be **linked to one or more records**. That linkage is what makes "open the task → land in the conversation" work.
- **Tasks** and **notes** are always created against a record (`tasks_create`, `notes_create` both take a record ID). A task linked to a record whose conversation thread is also linked to that record will, when opened, deep-link the user into that conversation. **Always link follow-up tasks to a record that has the relevant conversation linked.**
- **Custom activities** (`custom_activities_create`) are timeline entries on a record. Use them as both audit trail and shared memory between agent runs.

### Listing conversations

- `inbox_conversations_list` — conversations linked to a specific record. Use this when you start from a record and want its history.
- `inbox_conversations_search` — list or search inbox conversations workspace-wide, optionally filtered by inbox view, channel, or record-link state. Use this for inbox-first workflows (contact detection, reports) where you start from activity, not from a record.

### Reading messages

- `inbox_messages_list` — messages in one conversation, paged.
- `inbox_messages_get` — one message by ID.

Always paginate. Don't try to read entire long threads into context — read the last N messages relevant to the question.

## 7. Rate limits — what to do when you hit them

Four budgets, checked simultaneously. The first one you exhaust blocks the call:

| Limit                              | Budget                                                              |
|------------------------------------|---------------------------------------------------------------------|
| Organization                       | 600 requests/min                                                    |
| Workspace                          | 300 requests/min                                                    |
| MCP application or agent identity  | 180 requests/min                                                    |
| Route (same tool, same org)        | 120 requests/min                                                    |

On a hit you get HTTP `429` and JSON-RPC error `-32029` with message `Public API rate limit exceeded`. A `Retry-After` header (seconds) is usually included.

**Behavior:**

1. Wait the `Retry-After` interval. If absent, default to 5 seconds.
2. Resume from the exact step you stopped at — don't restart the workflow.
3. Don't fan out parallel retries.
4. If you're being throttled repeatedly inside one workflow, you're doing too much in one shot. Break the job into smaller batches (e.g., process 50 records per minute instead of 500).
5. Tell the user once if it materially delays the result. Don't surface every 429.

## 7.5. Page sizes and pagination discipline

Every paginated endpoint in the Breakcold API follows the same shape: a `limit` query parameter (default 50, max 100), a cursor-based pagination model via `cursor`, and a response shape with `data: [...]` and `pagination: { cursor, hasMore }`.

**The skill caps `limit` at 20.** This is lower than the API maximum on purpose:

| Limit value      | Per-page response size (typical)  | Behavior on common agent runtimes        |
|------------------|------------------------------------|------------------------------------------|
| `limit: 100`     | ~500KB+ for records with many fields | Saved to file; agent reads truncated preview; model loses confidence |
| `limit: 50`      | ~200-300KB                          | Often saved to file; preview-only        |
| **`limit: 20`**  | **~80-120KB**                       | **Returned inline; model sees full data** |
| `limit: 10`      | ~40-60KB                            | Inline; very safe, but wastes round trips |

The ~50KB-150KB inline threshold varies by runtime, but 20 records is the sweet spot — safe under every runtime we've tested, while not so small that pagination round-trips dominate.

### What the API actually exposes

From the OpenAPI spec, the parameters available on the high-traffic list endpoints:

**`records_list`** (`GET /records`):
- `limit` (1-100, default 50) — **always pass `20`**.
- `cursor` — opaque pagination cursor from previous response.
- `workspaceId` — required scope.
- `objectTypeId` / `objectTypeSlug` — scope by object.
- **`viewId`** — filter by a saved record view. **Prefer this whenever the user has a relevant view.** The user's saved views ARE the filter language; the API doesn't expose `where field = X` syntax.
- `archived` (default false) — already excludes archives, you don't need to filter client-side.
- `search` — text match on display name.

**`inbox_conversations_search`** (`GET /inbox/conversations`):
- `limit` (1-100, default 50) — **always pass `20`**.
- `cursor`.
- `workspaceId` (required).
- **`viewId`** — saved inbox view.
- **`hasLinkedRecords`** (boolean) — filter to conversations already linked to a record (true) or floating ones (false).
- `search`.

**Filters that do NOT exist (don't try to pass them):**
- ❌ `updatedAfter` / `createdAfter` date filter.
- ❌ Generic `where field = X` syntax.
- ❌ `stage = X` or `assignedTo = X` direct field filters.
- ❌ Multiple `viewId` values (single view per call).

### The "views as filters" pattern

Breakcold's filtering primitive is the user's saved views. When a workflow needs a narrowed cohort:

1. Call `crm_record_views_list` (or `inbox_views_list`) at the start of the workflow.
2. Identify a relevant view by name (e.g., "Active prospects", "Hot deals", "Unassigned"). Use simple keyword matching against the view name.
3. Surface it to the user: "I'll run on the **{view name}** view — say so if you'd rather use a different one or sweep everything."
4. Pass `viewId` on every `records_list` / `inbox_conversations_search` call.

The user already organizes their workspace with views; the agent rides on top of that mental model instead of trying to invent its own filter language.

### The page-by-page loop (the canonical pattern)

```
cursor = None
while True:
    page = records_list(workspaceId, objectTypeId, limit=20, cursor=cursor, viewId=optional)

    # 1. Filter client-side immediately — never carry rejected records forward
    active = [r for r in page.data if r not in terminal_stages]

    # 2. For the active set on this page, fetch detail in parallel
    #    Batch size ≤10 in parallel to respect rate limits
    conversations = parallel_fetch(active, batch_size=10)

    # 3. Decide and mutate immediately, on this page's records only
    for record, convs in zip(active, conversations):
        decision = decide(record, convs)
        if decision == MUTATE:
            tasks_create(...)         # or records_update, notes_create
            custom_activities_create(...)  # breadcrumb

    # 4. Discard this page's raw data before fetching next
    if not page.pagination.hasMore:
        break
    cursor = page.pagination.cursor
```

**Key invariants:**
- Never hold more than one page of raw record data in working context.
- Never delegate any step of this loop to a sub-agent.
- Process each page completely before fetching the next.
- For one-shot user-initiated runs, **stop after the first page** and ask the user to confirm "continue" before sweeping the rest. (See SKILL.md universal rule "Small-batch first for one-shot runs.")
- For scheduled routine runs, run end-to-end without confirmation.

### Reading data from the list response

The list responses include enough metadata that you often don't need to refetch:

- `records_list` returns `displayName`, `fields` (all field values), `createdAt`, `updatedAt`, `isArchived`. You usually don't need `records_get` after a `records_list` unless you specifically need data not in `fields`.
- `inbox_conversations_search` returns `channel`, `subject`, **`lastMessageAtMs`**, `lastMessageSnippet`, `isClosed`, `hasLinkedRecords`, `attendees`, `assignees`. You usually don't need `inbox_messages_list` to compute staleness — the timestamp is in the list response.

**Anti-pattern:** calling `inbox_messages_list` on every conversation just to check "when was the last message?" — the `lastMessageAtMs` field already tells you, and you can decide staleness from it without fetching messages. Only fetch messages when you need their *content* (to derive a topic for a task title, or to assess sentiment).

## 8. Caching guidance — what to remember between calls

Per session, hold these in your own scratchpad:

- Workspace ID (and the chosen one if multiple).
- Object IDs (Person, Company, Deal, custom).
- Field IDs (especially the pipeline-stage field, status, source, type, owner).
- Option IDs (pipeline stages mapped to their position and to their semantic meaning).
- Member list (user IDs and display names — needed for "assign to" decisions).
- Any IDs you read recently that you're about to mutate.

If you must drop something to fit context, drop the field/option dictionary — re-fetching that is cheaper than re-fetching the full pipeline state.

## 9. Error handling — common shapes

| Symptom                                       | Likely cause                                          | Recovery                                                                       |
|-----------------------------------------------|-------------------------------------------------------|--------------------------------------------------------------------------------|
| Auth/credential error                         | Token expired, scope missing, OAuth lapsed            | Surface the one-tap reconnect message. Wait.                                   |
| `X-Breakcold-Organization-Id` missing         | User has multiple orgs                                | Add the header (use the org id from `workspaces_list` context). Retry once.    |
| 404 on a record                               | Record archived or wrong workspace                    | Check workspace, then `records_restore` only if user explicitly asks.          |
| 409 conflict on create                        | Duplicate exists                                      | Search for the existing record and use it instead.                             |
| 400 on field value                            | Wrong shape (e.g. sent string for select field)       | Re-fetch the field with `crm_fields_get` and adjust.                           |
| 429                                           | Rate limit                                            | See section 7.                                                                 |

## 10. Sanity checks before any big batch

Run this quick checklist mentally before kicking off any multi-step batch (CRM setup, contact detection across an entire inbox, mass pipeline progression):

- Workspace confirmed.
- Object IDs cached for every object you'll touch.
- Pipeline-stage field identified, options cached with ordering.
- For automation: criteria confirmed with the user in **one** message.
- For routines: frequency confirmed, recap channel confirmed, assignee confirmed.

If any item is missing, fix it first. Restarting halfway through a 500-record sweep is much more expensive than spending 30 seconds up front.

## 11. Canonical tool-call examples

Verified against Breakcold's OpenAPI spec. Field values follow the typing rules in section 5 — copy these as templates and replace the placeholder IDs with cached ones from your discovery pass.

### Identifiers used in examples

All Breakcold IDs are opaque strings, minimum 6 characters. The placeholders below use a `<prefix>_xxx` convention for clarity:

| Placeholder       | What it is                                                           |
|-------------------|----------------------------------------------------------------------|
| `<workspace_id>`  | From `workspaces_list`                                               |
| `<object_id>`     | From `crm_objects_list` (Person, Company, Deal, custom)              |
| `<record_id>`     | From `records_list` / `records_get`                                  |
| `<field_id>`      | From `crm_fields_list`                                               |
| `<option_id>`     | From `crm_field_options_list`                                        |
| `<user_id>`       | A workspace member's user ID                                         |
| `<conversation_id>` | From `inbox_conversations_list`                                    |

### records_create — basic person

```json
{
  "workspaceId": "<workspace_id>",
  "objectTypeSlug": "person",
  "fields": {
    "name": "Ada Lovelace",
    "email": "ada@example.com",
    "linkedin": "https://www.linkedin.com/in/adalovelace"
  }
}
```

Use `objectTypeSlug` (e.g., `"person"`, `"company"`, `"deal"`) for built-in objects when known; use `objectTypeId` for custom objects.

### records_create — deal with select stage, currency, and relation to a Person

```json
{
  "workspaceId": "<workspace_id>",
  "objectTypeSlug": "deal",
  "fields": {
    "name": "Acme — Q2 expansion",
    "stage":    { "optionId": "<option_id_qualified>" },
    "value":    { "amount": 48000, "currencyCode": "USD" },
    "owner":    "<user_id>",
    "channels": [
      { "optionId": "<option_id_email>" },
      { "optionId": "<option_id_linkedin>" }
    ],
    "primary_contact": "<record_id_person>"
  }
}
```

- Single-select fields take `{ "optionId": "..." }`.
- Multi-select fields take an array of `{ "optionId": "..." }`.
- Currency takes `{ "amount": number, "currencyCode": "ISO_4217" }`.
- Member fields (owner, assignee) take a user ID string.
- Relation fields take a record ID (or array of record IDs for many-relations).

### records_update — change pipeline stage and fill a field

```json
{
  "fields": {
    "stage":        { "optionId": "<option_id_proposal>" },
    "lost_reason":  null,
    "industry":     { "optionId": "<option_id_saas>" }
  }
}
```

PATCH semantics — only the fields included are updated. Use `null` to clear a previously-set value.

### tasks_create — follow-up linked to a conversation (Action 1)

```json
{
  "title": "Follow up — email thread went quiet (9 days)",
  "descriptionPlain": "Auto-created by breakcold-crm on signal of >7d quiet thread.",
  "dueAt": 1748044800000,
  "assigneeUserIds": ["<user_id>"],
  "conversationId": "<conversation_id>"
}
```

- `dueAt` is **Unix milliseconds**, not seconds.
- `assigneeUserIds` is an array — Breakcold supports multiple assignees.
- `conversationId` is the secret sauce — it makes opening the task deep-link straight into the thread. **Include it whenever the task is about a specific conversation.**

### notes_create — research note (Action 4)

```json
{
  "title": "Prospect research — Acme Corp",
  "content": "<p><strong>COMPANY — Acme Corp</strong><br>What they do: Mid-market B2B SaaS for fleet operations...</p>",
  "contentPlain": "COMPANY — Acme Corp\nWhat they do: Mid-market B2B SaaS for fleet operations..."
}
```

- `content` is HTML. `contentPlain` is the plain-text fallback used in search and exports.
- Always provide both — the HTML for display, the plain version for everything else.

### custom_activities_create — breadcrumb (the memory pattern)

```json
{
  "title": "[breakcold-crm:auto-tasks 2026-05-23] Follow-up task created",
  "descriptionPlain": "Last activity 9 days ago (email); assigned to Sarah.",
  "startAt": 1748044800000,
  "linkedRecordIds": ["<record_id_related_deal>"],
  "participantUserIds": ["<user_id>"]
}
```

- The `title` carries the prefix that future runs can filter on (see `routines.md`).
- `startAt` is **Unix milliseconds**.
- `linkedRecordIds` lets one activity span multiple records (e.g., person + their deal).
- One activity per record per run is the right cadence — don't write one per micro-decision.

### crm_fields_create — single-select with options (Action 6)

```json
{
  "slug": "source",
  "name": "Source",
  "fieldType": "select",
  "isMultiple": false,
  "options": [
    { "id": "tmp_1", "fieldDefinitionId": "tmp_field", "value": "inbound",   "label": "Inbound",   "order": 0, "color": "blue",   "isDefault": false, "isActive": true },
    { "id": "tmp_2", "fieldDefinitionId": "tmp_field", "value": "outbound",  "label": "Outbound",  "order": 1, "color": "green",  "isDefault": false, "isActive": true },
    { "id": "tmp_3", "fieldDefinitionId": "tmp_field", "value": "referral",  "label": "Referral",  "order": 2, "color": "violet", "isDefault": false, "isActive": true },
    { "id": "tmp_4", "fieldDefinitionId": "tmp_field", "value": "event",     "label": "Event",     "order": 3, "color": "amber",  "isDefault": false, "isActive": true }
  ]
}
```

- `fieldType`: `"text"`, `"textarea"`, `"select"`, `"multiselect"`, `"number"`, `"currency"`, `"date"`, `"datetime"`, `"email"`, `"phone"`, `"url"`, `"location"`, `"linkedin"`, `"twitter"`, `"facebook"`, `"whatsapp"`, `"telegram"`, `"checkbox"`, `"member"`, `"relation"`.
- For `relation`, include `targetObjectTypeId`, `relationCardinality` (e.g., `"one_to_many"`), `inverseName`, and `inverseSlug`.
- `options[].id` and `fieldDefinitionId` can be temporary tokens — Breakcold reassigns them on creation.

### crm_record_views_create — Kanban Pipeline view (Action 6)

```json
{
  "name": "Pipeline",
  "emoji": "📊",
  "type": "kanban",
  "isDefault": true,
  "kanbanFieldDefinitionId": "<field_id_stage>",
  "kanbanWinOptionIds":  ["<option_id_won>"],
  "kanbanLossOptionIds": ["<option_id_lost>"],
  "config": {
    "columns": [
      { "fieldId": "<field_id_name>",        "width": 240 },
      { "fieldId": "<field_id_stage>",       "width": 140 },
      { "fieldId": "<field_id_value>",       "width": 120 },
      { "fieldId": "<field_id_close_date>",  "width": 120 },
      { "fieldId": "<field_id_owner>",       "width": 120 }
    ],
    "filters": [
      { "fieldId": "<field_id_stage>", "operator": "is_not", "value": ["<option_id_lost>"] }
    ],
    "sorts": [
      { "fieldId": "<field_id_value>", "direction": "desc" }
    ]
  }
}
```

- `type: "kanban"` is the board view; use `"table"` for list views.
- `kanbanWinOptionIds` / `kanbanLossOptionIds` tell Breakcold which stages are terminal, so cards in those columns get the right visual treatment.
- The `config` object is the **full saved config** — when you `crm_record_views_update`, you replace the entire config, so include everything you want preserved.

### crm_record_views_create — At Risk Deals (table view)

```json
{
  "name": "At risk",
  "emoji": "⚠️",
  "type": "table",
  "isDefault": false,
  "config": {
    "columns": [
      { "fieldId": "<field_id_name>",          "width": 240 },
      { "fieldId": "<field_id_stage>",         "width": 140 },
      { "fieldId": "<field_id_last_activity>", "width": 160 },
      { "fieldId": "<field_id_value>",         "width": 120 },
      { "fieldId": "<field_id_owner>",         "width": 120 }
    ],
    "filters": [
      { "fieldId": "<field_id_stage>",         "operator": "is_not", "value": ["<option_id_won>", "<option_id_lost>"] },
      { "fieldId": "<field_id_last_activity>", "operator": "older_than_days", "value": 14 }
    ],
    "sorts": [
      { "fieldId": "<field_id_last_activity>", "direction": "asc" }
    ]
  }
}
```

### inbox_views_create — Unanswered

```json
{
  "workspaceId": "<workspace_id>",
  "name": "Unanswered",
  "emoji": "📩",
  "visibility": "personal",
  "config": {
    "filters": [
      { "field": "last_message_direction", "operator": "is", "value": "inbound" },
      { "field": "has_user_reply",         "operator": "is", "value": false }
    ],
    "sorts": [
      { "field": "last_message_at", "direction": "asc" }
    ]
  }
}
```

`visibility`: `"personal"` (only the creator), `"workspace"` (everyone), or `"restricted"` (per-user ACL).

### records_list — search with filter (any action)

`records_list` accepts filter conditions in its request body. The exact filter operator names mirror what the UI shows (`is`, `is_not`, `contains`, `older_than_days`, etc.). Use server-side filtering wherever possible to keep traffic low — reading 50 filtered records is cheaper than 500 unfiltered.

If you're unsure of the exact filter operator strings for a given field type, call `crm_fields_get` first to inspect the field, then iterate. The OpenAPI spec is the source of truth — when in doubt, check `docs.breakcold.com/api/openapi.json`.
