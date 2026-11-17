# Coil API Endpoints

Base URL comes from the selected CLI profile or `COIL_BASE_URL`.

All authenticated requests use:

```http
Authorization: Bearer <session-token-or-ak-key>
Content-Type: application/json
```

Coil organization API keys (`ak_...`) are accepted by agent-compatible routes.

Coil first-party credentials authenticate durable named agents. The agent ID is
the machine actor ID; the credential ID identifies only one credential.
Existing credentials were identity-preserving backfilled. Credential
administration requires a human organization admin, and permanent credential
plaintext is returned only once.

## Auth and Context

| Method | Path | Notes |
| --- | --- | --- |
| GET | `/api/auth/status` | Returns authenticated actor, org, role, token type, and auth mode. |
| GET | `/api/auth/api-keys` | Lists Coil organization API keys for human org admins. |
| DELETE | `/api/auth/api-keys/{id}` | Revokes a Coil organization API key for human org admins. |
| POST | `/api/auth/verify-key` | Verifies a Coil organization API key without exposing it. |

Named-agent management is human-admin only:

| Method | Path | CLI |
| --- | --- | --- |
| GET | `/api/agents` | `coil agents list --json` |
| POST | `/api/agents` | `coil agents create --name ... --json` |
| GET | `/api/agents/{id}` | `coil agents view <agent-id> --json` |
| POST | `/api/agents/{id}/setup` | `coil agents setup <agent-id> --runtime ... --profile ... --json` |
| POST | `/api/agents/{id}/credentials` | `coil agents issue-credential <agent-id> --json` |
| DELETE | `/api/agents/{id}/credentials/{credentialId}` | `coil agents revoke-credential <agent-id> <credential-id> --json` |

`--replace` changes the generated local setup command. It does not revoke an
existing credential. Replacement credentials keep the same durable agent ID.

CLI discovery wrapper:

```bash
coil agent-context --json
```

When a response requires or recommends a human web handoff, the API returns a
typed `human_action` in success `meta` or blocked error `details`, and the CLI
preserves it in JSON output. Agents must relay the exact URL and its required
or recommended state. The URL does not grant authority or imply approval.

## Activation, Marketplace, and Recipes

| Method | Path | CLI |
| --- | --- | --- |
| GET | `/api/activation` | `coil activation status --json` |
| GET | `/api/marketplace/templates` | `coil marketplace templates --json` |
| POST | `/api/marketplace/templates/{id}/install` | `coil marketplace install <template-id> --json` |
| GET | `/api/recipes` | `coil recipes list --json` |
| GET | `/api/recipes/{id}` | `coil recipes view <recipe-id> --json` |
| POST | `/api/recipes/{id}/validate` | `coil recipes validate <recipe-id> --json` |
| POST | `/api/recipes/{id}/publish` | `coil recipes publish <recipe-id> --json` |
| POST | `/api/recipes/{id}/run` | `coil recipes run <recipe-id> --confirm-provider-spend ... --json` |
| GET | `/api/recipe-runs/{id}` | `coil recipe-runs view <run-id> --json` |
| POST | `/api/recipe-runs/{id}/cancel` | `coil recipe-runs cancel <run-id> --json` |
| POST | `/api/recipe-runs/{id}/retry` | `coil recipe-runs retry <run-id> --json` |

Provider-backed admission requires explicit spend confirmation. A `202` queued response is durable admission, not terminal success. Recipe publication and ambiguous-effect reconciliation require a human organization admin.

## Scrapes

| Method | Path | CLI |
| --- | --- | --- |
| GET | `/api/scrapes?limit=100` | `coil scrapes list --json` |
| POST | `/api/scrapes` | `coil scrapes create ... --json` |
| GET | `/api/scrapes/{id}` | `coil scrapes get <id> --json` |
| PATCH | `/api/scrapes/{id}` | `coil scrapes rename <id> --name ...` |
| DELETE | `/api/scrapes/{id}` | `coil scrapes delete <id> --force` |
| POST | `/api/scrapes/{id}/recount` | `coil scrapes recount <id> --json` |
| GET | `/api/scrapes/{id}/leads` | `coil leads list <scrape-id> --json` |
| GET | `/api/leads` | `coil leads list --json` |

Machine callers can create scrapes. Admin-gated destructive routes require a human org admin session.

## Leads

| Method | Path | CLI |
| --- | --- | --- |
| GET | `/api/scrapes/{scrapeId}/leads?limit=50&offset=0` | `coil leads list <scrape-id> --json` |
| GET | `/api/leads?limit=50&offset=0` | `coil leads list --json` |
| GET | `/api/leads/{id}` | `coil leads get <id> --json` |
| PATCH | `/api/leads/{id}` | `coil leads update <id> --fields '{...}' --json` |
| DELETE | `/api/leads/{id}` | `coil leads delete <id> --force --json` |
| PATCH | `/api/leads/bulk` | `coil leads bulk-update --ids ... --fields '{...}' --json` |
| POST | `/api/export/csv` | `coil leads export <scrape-id> [--filter/--view/--ids] [--output]` |
| GET | `/api/leads/emails?scrapeId={id}` | `coil leads emails <scrape-id>` |
| POST | `/api/leads/import` | `coil --json leads import <file> [--mapping ...] [--admission-key ...]` |
| GET | `/api/recipe-runs/{id}/import-outcomes` | `coil recipe-runs import-outcomes <run-id> --outcome rejected --json` |
| GET | `/api/recipe-runs/{id}/leads` | `coil recipe-runs leads <run-id> --json` |

Lead-list imports accept at most 2,000 data rows and 2 MiB of CSV input. The
CLI maps supported headers before admission; use `--mapping` for ambiguous
headers and a stable `--admission-key` when a retry may be uncertain. A `202`
response means durable admission, not terminal success. Inspect
`coil recipe-runs view`, `coil recipe-runs import-outcomes`, and
`coil recipe-runs leads` and wait for a terminal run state before reporting
completion. The API is organization-scoped, does not retain the original CSV,
and does not print rejected-row PII. Successful inputs are scrubbed after
completion; failed or cancelled normalized replay data is retained for up to
30 days.

## Automations

| Method | Path | CLI |
| --- | --- | --- |
| GET | `/api/automations?status=published` | `coil automations list --json` |
| POST | `/api/automations` | `coil automations create ... --json` |
| GET | `/api/automations/{id}` | `coil automations view <id> --json` |
| PATCH | `/api/automations/{id}` | `coil automations update <id> ... --json` |
| DELETE | `/api/automations/{id}` | `coil automations delete <id> --force --json` |
| POST | `/api/automations/{id}/validate` | `coil automations validate <id> --json` |
| POST | `/api/automations/{id}/publish` | `coil automations publish <id> --json` |
| POST | `/api/automations/{id}/run` | `coil automations run <id> --scrape <scrape-id> --json` |
| GET | `/api/automations/{id}/results` | `coil automations results list --automation <id> --json` |
| GET | `/api/automations/results` | `coil automations results list --json` |
| GET | `/api/automations/results/{resultId}` | `coil automations results view <result-id> --json` |
| GET | `/api/automations/results/{resultId}/links` | `coil automations results links list <result-id> --json` |
| POST | `/api/automations/results/{resultId}/links` | `coil automations results links add <result-id> --kind webhook_evidence --url https://... --json` |
| DELETE | `/api/automations/results/{resultId}/links/{linkId}` | `coil automations results links delete <result-id> <link-id> --json` |
| GET | `/api/automations/policy` | `coil automations policy get --json` |
| PUT | `/api/automations/policy` | `coil automations policy set --domains ... --fields ... --json` |

API-key callers create draft automations. Publishing, deletion, and policy changes require a human org admin session. Automation result links are deliberately narrow traceability records for delivery evidence; they are not a generic metadata surface.

Draft creation/validation, unresolved automation run/result reads, and exact
admission replays of unresolved runs may include
`meta.human_action` with the absolute `/automations` review or reconciliation
URL. Machine publication and reconciliation attempts preserve the same action
under `error.details.human_action`.

## Settings, Preferences, Members

| Method | Path | CLI |
| --- | --- | --- |
| GET | `/api/settings` | `coil settings get --json` |
| PATCH | `/api/settings` | `coil settings set <key> <value> --json` |
| GET | `/api/preferences/columns?scrapeId={id}` | `coil preferences get --scrape <id> --json` |
| PUT | `/api/preferences/columns` | `coil preferences set --scrape <id> ... --json` |
| GET | `/api/members` | `coil members list --json` |

## Integrations and SmartLead

| Method | Path | CLI |
| --- | --- | --- |
| GET | `/api/integrations` | `coil integrations list --json` |
| GET | `/api/integrations/{provider}` | `coil integrations status <provider> --json` |
| PUT | `/api/integrations/{provider}` | `printf '%s' "$PROVIDER_API_KEY" \| coil integrations set <provider> --json` |
| DELETE | `/api/integrations/{provider}` | `coil integrations disconnect <provider> --json` |
| POST | `/api/integrations/{provider}/test` | `coil integrations test <provider> --json` |
| POST | `/api/integrations/rotate` | `coil integrations rotate [--apply] --json` |
| GET | `/api/integrations/smartlead/campaigns` | `coil smartlead campaigns --json` |
| GET | `/api/integrations/smartlead/campaigns/sequences?campaignId={id}` | `coil smartlead sequences --campaign <id> --json` |
| POST | `/api/integrations/smartlead/send` | `coil smartlead send <scrape-id> --campaign <id> --json` |

`GET /api/integrations/{provider}` includes current credential-scoped
`execution_readiness`. For a `blocked` scope, the response returns one
server-generated absolute Coil operator URL at canonical `meta.human_action`
and the temporary compatibility alias `data.human_action`. Relay that Coil URL
verbatim even when `execution_readiness[].actionUrl` is `null`. The CLI exposes
one top-level `human_action` in JSON and an explicit text-mode URL. A safe,
non-null `execution_readiness[].actionUrl` remains a separate provider-side
authorization link and must not be rewritten or treated as Coil approval.
`open`, `half_open`, `degraded`, `ready`, and `unknown` states do not include a
required human action.

## Feedback

| Method | Path | CLI |
| --- | --- | --- |
| POST | `/api/feedback` | `coil feedback "..." --json` |

The CLI also supports local feedback drafts and resend commands for retryable failures.

## Activity and Usage

| Method | Path | CLI |
| --- | --- | --- |
| GET | `/api/activity` | `coil activity list --json` |
| GET | `/api/usage?view=summary` | `coil usage summary --json` |
| GET | `/api/usage?view=events` | `coil usage events --json` |
| GET | `/api/usage?view=limits` | `coil usage limits --json` |

Activity cursors are opaque. Usage endpoints require an organization admin, so machine API keys are intentionally rejected by the shared role gate.
