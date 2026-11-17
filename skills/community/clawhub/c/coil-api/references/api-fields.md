# Coil API Fields

Responses use snake_case. Request bodies generally accept the field names shown by the CLI and API route schemas.

## Auth Context

`GET /api/auth/status` returns:

| Field | Type | Notes |
| --- | --- | --- |
| `authenticated` | boolean | Whether the bearer token is valid. |
| `userId` | string/null | Human Clerk user ID when present. |
| `orgId` | string/null | Clerk organization ID. |
| `orgRole` | `org:admin`/`org:member`/null | Role for human sessions; API keys map to member behavior. |
| `tokenType` | string/null | Usually `session_token` or `api_key`. |
| `actor` | object | `{ type, id, name }` where type is `human` or `machine`. |

## CLI Output Envelope

Use `--json --output-version 2` on list commands when possible:

```json
{
  "resource": "scrapes",
  "items": [],
  "total": 0,
  "limit": 25,
  "offset": 0,
  "nextOffset": null,
  "truncated": false,
  "hint": null
}
```

## Human action

API success envelopes may include `meta.human_action`; blocked errors may
include the same object at `error.details.human_action`:

| Field | Type | Notes |
| --- | --- | --- |
| `kind` | `approval`/`review`/`reconciliation`/`operator_intervention` | Human handoff category. |
| `required` | boolean | Whether the human action is required to continue. |
| `label` | string | Short human-readable action description. |
| `url` | absolute HTTP(S) URL | Server-provided navigation URL. It is not a bearer token or approval capability. |
| `resource_type` | string/null | Optional Coil resource type. |
| `resource_id` | string/null | Optional resource identifier. |

The CLI preserves this action as a top-level `human_action` field for object
JSON results and V2 list envelopes. The V1 automations result list keeps its
array shape and adds `human_action` to the matching item. Text mode prints the
URL explicitly. Do not invent
one when the server does not return it. Legacy Actor Lab `approval_url` remains
available during the compatibility window.

### Provider integration status

`GET /api/integrations/{provider}` reports the current credential-scoped
`execution_readiness` records. If a current scope is `blocked`, the raw API
success envelope contains the same `Human action` object at both
`meta.human_action` (canonical) and `data.human_action` (temporary compatibility
alias for clients that unwrap `data`). The current CLI exposes one copy as
top-level `human_action` in JSON and prints its label and URL explicitly in
text mode.

`execution_readiness[].actionUrl` remains the separately validated provider
authorization URL and may be `null`; it must not be copied into the Coil
action. Relay the absolute Coil URL verbatim even when the provider URL is
`null`. Only `blocked` requires this operator handoff. `open`, `half_open`,
`degraded`, `ready`, and `unknown` retain automatic retry or reconciliation
semantics and do not advertise required human intervention.

## Scrape

| Field | Type | Notes |
| --- | --- | --- |
| `id` | string | UUID. |
| `org_id` | string | Tenant isolation key. |
| `name` | string | Human-visible scrape name. |
| `status` | string | `pending`, `running`, `completed`, `failed`, or legacy/null values. |
| `job_titles` | string[] | Prospect scrape filter. |
| `locations` | string[] | Prospect scrape filter. |
| `company_sizes` | string[] | Prospect scrape filter. |
| `industries_include` | string[]/null | Prospect filter. |
| `industries_exclude` | string[]/null | Prospect filter. |
| `search_url` | string/null | Sales Navigator source URL in create payloads. |
| `fetch_count` | number | Requested prospect count. |
| `prospect_count` | number | Current stored lead count. |
| `smartlead_campaign_id` | string/null | Optional auto-send campaign. |
| `created_by_user_id` | string/null | Human creator when known. |
| `created_at` | ISO string | Creation timestamp. |

Create payloads:

```json
{
  "type": "prospect",
  "name": "Q2 prospects",
  "job_titles": ["VP Sales"],
  "locations": ["United States"],
  "company_sizes": ["11-50"],
  "fetch_count": 100,
  "confirm_provider_spend": true
}
```

```json
{
  "type": "sales-nav",
  "name": "Sales Nav export",
  "search_url": "https://www.linkedin.com/sales/search/people?...",
  "user_agent": "Mozilla/5.0 ...",
  "linkedin_cookie": "li_at=...",
  "confirm_provider_spend": true
}
```

`confirm_provider_spend` is required for provider-backed acquisition. Sales Navigator credentials are resolved server-side for execution and must not be stored in recipe inputs or copied into logs.

## Lead

| Field | Type | Notes |
| --- | --- | --- |
| `id` | string | UUID. |
| `org_id` | string | Tenant isolation key. |
| `scrape_id` | string | Parent scrape. |
| `full_name` | string/null | Lead name. |
| `first_name` | string/null | First name. |
| `last_name` | string/null | Last name. |
| `email` | string/null | Email when known. |
| `linkedin` | string/null | LinkedIn profile URL. |
| `job_title` | string/null | Role/title. |
| `company_name` | string/null | Company. |
| `company_domain` | string/null | Company domain. |
| `location` | string/null | Lead location. |
| `is_bad_fit` | boolean/null | Qualification marker. |
| `added_to_smartlead` | boolean/null | SmartLead send marker. |
| `smartlead_campaign` | string/null | Campaign name. |
| `date_scraped` | string/null | Scrape date. |

Filter conditions use:

```json
{
  "column": "email",
  "operator": "is_not_empty",
  "value": ""
}
```

Supported operators include equality, contains, empty/not-empty, booleans, and date comparisons. Use `coil agent-context --json` for the current command manifest.

## Automation

| Field | Type | Notes |
| --- | --- | --- |
| `id` | string | UUID. |
| `org_id` | string | Tenant isolation key. |
| `name` | string | Automation name. |
| `webhook_url` | string | HTTPS webhook URL. |
| `input_fields` | string[] | Lead fields sent to the webhook. |
| `scope` | `global`/`scrape` | Whether automation applies globally or to one scrape. |
| `scrape_id` | string/null | Required for scrape-scoped automation. |
| `status` | `draft`/`published`/`disabled` | API-key agents create drafts. |
| `created_by_actor_type` | `human`/`machine` | Actor attribution. |
| `created_by_actor_id` | string | User ID or durable Coil agent ID. |
| `created_by_actor_name` | string/null | Durable agent display name when available. |
| `published_by_user_id` | string/null | Human admin publisher. |
| `published_at` | ISO string/null | Publication timestamp. |

Create payload:

```json
{
  "name": "Enrich leads",
  "webhook_url": "https://hooks.example.com/enrich",
  "input_fields": ["email", "company_name"],
  "scope": "global",
  "scrape_id": null
}
```

## Automation Result

| Field | Type | Notes |
| --- | --- | --- |
| `id` | string | UUID. |
| `automation_id` | string | Parent automation. |
| `lead_id` | string | Processed lead. |
| `status` | `pending`/`running`/`success`/`error`/`cancelled`/`reconciliation_required` | Delivery state. `reconciliation_required` is ambiguous provider delivery and requires a human action; it is never a retry instruction. |
| `result` | string/null | Webhook response or summary. |
| `error_message` | string/null | Failure detail. |
| `created_at` | ISO string | Creation timestamp. |
| `updated_at` | ISO string | Last status update. |

When automation creation or draft validation requires publication, or an
automation run/result requires reconciliation, the API returns
`meta.human_action` (or `error.details.human_action` for a blocked request).
The URL is an absolute, secret-free `/automations` navigation URL. Relay it
verbatim; opening it does not grant approval or change policy.

## Automation Result Link

| Field | Type | Notes |
| --- | --- | --- |
| `id` | string | UUID. |
| `automation_result_id` | string | Parent automation result. |
| `kind` | `webhook_evidence`/`smartlead_campaign`/`delivery_evidence` | Accepted evidence class. |
| `label` | string/null | Short label or delivery ID, max 120 characters. |
| `url` | string | HTTPS URL, max 2048 characters. `smartlead_campaign` URLs must use a `smartlead.ai` host. |
| `created_at` | ISO string | Creation timestamp. |

Create payload:

```json
{
  "kind": "webhook_evidence",
  "label": "n8n execution",
  "url": "https://logs.example.com/run/1"
}
```

## Automation Policy

| Field | Type | Notes |
| --- | --- | --- |
| `domains` | string[] | Exact or wildcard allowed webhook hosts. |
| `fields` | string[] | Allowed lead fields for automation payloads. |

Only human org admins can update policy.

## Settings

Settings are stored in org-scoped JSON. Common keys:

| Key | Type | Notes |
| --- | --- | --- |
| `has_smartlead_key` | boolean | Read-only redacted presence marker. |
| `smartlead_api_key` | string | Legacy setting. New writes are rejected; configure SmartLead with `printf '%s' "$SMARTLEAD_API_KEY" \| coil integrations set smartlead` or `PUT /api/integrations/smartlead`. |
| `default_columns` | string[] | Optional lead table defaults. |

## Agent Caveats

- API-key agents currently behave as org members, not org admins.
- A first-party credential authenticates a durable named agent. Credential IDs and agent IDs are separate; existing credentials were identity-preserving backfilled.
- Browser credential checking does not update `last_used_at` and does not prove that an external agent runtime is connected.
- Replacement uses temporary credential overlap and explicit old-credential revocation.
- Clerk organization API keys remain a separate compatibility path.
- Admin-gated actions include destructive scrape/automation operations, automation policy management, and automation publishing.
- Prefer `coil feedback` for platform friction discovered while operating Coil.
