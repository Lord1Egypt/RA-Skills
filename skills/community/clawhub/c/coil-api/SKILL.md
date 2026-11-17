---
name: coil-api
description: Use Coil's CLI and API for agent-operated outbound recipes, durable runs, lead management, automations, provider integrations, feedback, and runtime discovery. Use when an agent needs to install, authenticate, discover, or operate Coil through the same organization state humans use in the dashboard.
metadata:
  openclaw:
    requires:
      bins:
        - coil
    primaryEnv: COIL_API_KEY
    envVars:
      - name: COIL_API_KEY
        required: false
        description: Organization-scoped Coil API key; configure through an OpenClaw SecretRef or runtime secret manager before authenticated commands.
      - name: COIL_BASE_URL
        required: false
        description: Optional HTTPS API base URL override; the recommended public profile uses https://www.usecoil.com.
    install:
      - id: node
        kind: node
        package: "@usecoil/cli@0.1.4"
        bins:
          - coil
        label: Install the supported Coil CLI from npm
    emoji: "🌀"
    homepage: https://www.usecoil.com
---

# Coil API

Coil is an agent-operated outbound platform. Recipes are reusable workflows and runs are durable executions; prospect and Sales Navigator scrapes remain backing source/result records and compatibility commands.

The project principle is human-agent parity: when a feature exists in the UI, agents should have an API route, CLI command, and skill-level discoverability path for the same capability.

## First Command

Install the supported CLI if `coil` is not already available, then ask it what
it can do:

```bash
if ! command -v coil >/dev/null 2>&1; then
  npm install --global @usecoil/cli@0.1.4
fi
coil --version
```

Start every new Coil runtime by asking the CLI what it can do:

```bash
coil agent-context --json
```

For named environments:

```bash
coil --profile prod agent-context --json
```

`agent-context` returns the selected profile, API base URL, auth mode, actor context, global flags, command manifests, output version information, and current caveats.

## Authentication

Prefer profile-based CLI auth:

```bash
printf '%s' "$COIL_API_KEY" | coil auth login --profile prod --key -
coil auth use prod
coil --profile prod auth status --json
```

On PowerShell:

```powershell
$env:COIL_API_KEY | coil auth login --profile prod --key -
coil auth use prod
coil --profile prod auth status --json
```

Coil API keys are first-party organization API keys. They start with `ak_` and are already scoped to an organization.

Do not configure `COIL_ORG_ID`. Coil does not need it for CLI/API calls.

Environment fallback is supported when a profile is not available:

```bash
export COIL_API_KEY="ak_..."
export COIL_BASE_URL="https://your-coil-host.example.com"
coil scrapes list --json
```

The CLI's built-in base URL is for local development. For the public service,
explicitly run `coil config set-base-url https://www.usecoil.com --profile prod`
before authenticating. Use `COIL_BASE_URL` only as an environment fallback when
you cannot persist a profile.

## Runtime setup

This skill is portable across Codex, Claude Code, Hermes Agent, and OpenClaw.
The runtime-specific installer or registry handles placement; Coil operations
always use the same public JSON CLI:

```bash
npm install --global @usecoil/cli@0.1.4
coil config set-base-url https://www.usecoil.com --profile prod
printf '%s' "$COIL_API_KEY" | coil auth login --profile prod --key -
coil --profile prod agent-context --json
```

On PowerShell, use `$env:COIL_API_KEY | coil auth login --profile prod --key -`
for the authentication step.

Supply `COIL_API_KEY` through the runtime secret manager and never place it in
command arguments. OpenClaw may provide it through the `coil-api` skill entry;
other runtimes may use their own secret manager. Do not add `COIL_ORG_ID`.

## CLI JSON Rules

- Use `--json` for machine-readable output.
- Use `--output-version 2` for standard list envelopes where supported.
- Version 2 list output shape is `{ resource, items, total, limit, offset, nextOffset, truncated, hint }`.
- Diagnostics and errors go to stderr.
- Global flags: `--profile`, `--base-url`, `--json`, `--output-version`.

## Human action handoffs

When a raw Coil API success response includes `meta.human_action`, or a blocked
API error includes `error.details.human_action`, relay the returned action to
the user. In CLI `--json` success output, object results and V2 list envelopes
expose the same action as a top-level `human_action` field. The V1 automations
result list keeps its array shape and adds `human_action` to the matching item.
CLI errors preserve it under
`error.details.human_action`. State whether it is required or recommended,
include the exact `url` verbatim, and use its human-readable `label`. Do not
say only “go to the dashboard,” fabricate a URL, or direct draft review to the
public `/recipes` concept pages. If no specific recipe ID is available, use the
server-approved `/dashboard/recipes/review` queue. Treat opening the URL as
navigation only; the destination still authenticates and authorizes the human.

Older Actor Lab responses may also contain `approval_url`. Preserve and relay
that server-provided URL when present, while preferring the standardized
`human_action` object for machine reasoning.

Automation handoffs use the server-provided absolute `/automations` URL. After
an agent creates or validates a draft, relay the required publication action
verbatim: the human org admin must review and publish the draft. If a run or
result has `reconciliation_required`, relay the required reconciliation action
verbatim and do not retry the webhook. A policy-review action means a human
must decide the governance policy; it is not an instruction to weaken policy.

Provider integration status is a specific success-envelope case. When the
current credential-scoped `execution_readiness` contains a `blocked` scope,
`GET /api/integrations/{provider}` returns the same required Coil action at
`meta.human_action` and the temporary compatibility alias `data.human_action`.
The current CLI promotes one copy to top-level `human_action`; older clients
that unwrap `data` still retain the alias. Relay the Coil `url` verbatim even
when `execution_readiness[].actionUrl` is `null`. A non-null provider
`actionUrl` is a separate safe external provider-authorization link. Do not
invent, rewrite, or treat either URL as approval or authority. Automatic
`open`, `half_open`, `degraded`, `ready`, and `unknown` states do not require
this handoff.

## Common Workflows

### Orient

```bash
coil --profile prod agent-context --json
coil --profile prod config show --json
coil --profile prod auth status --json
```

### Guided activation

Use the server-derived activation state before starting a new workspace flow. Provider-backed runs require a healthy saved connection and explicit spend confirmation.

`coil activation status --json` may include a server-provided `human_action`.
State whether it is required or recommended and relay its absolute `url`
verbatim. Do not map `nextAction` to a guessed dashboard route. `start_run`
still needs explicit provider-spend confirmation; a human-action URL is only
navigation and does not grant approval or authority.

Machine recipe creation, draft updates, and template installation return a required
`human_action` for the specific `/dashboard/recipes/{recipeId}` detail surface.
Successful machine validation of a draft returns the same action. Relay its
absolute `url` verbatim. A machine publish `403` preserves the scoped action in
`error.details.human_action` when the draft exists; do not treat the URL as
approval or authority.

For `recipes create --json`, preserve every returned recipe field and relay the
top-level `human_action` when the server provides it. If the response contains
only `data` or omits valid metadata, report the unchanged recipe result. Never
infer or fabricate a dashboard URL or human action.

```bash
coil --profile prod activation status --json
coil --profile prod marketplace templates --json
coil --profile prod marketplace install coil.prospect-search --json
coil --profile prod recipes run <starter-recipe-id> --starter-run --confirm-provider-spend --new-scrape-name "Starter prospects" --titles "Founder" --locations "Singapore" --sizes "1-10" --fetch-count 25 --input '{"fetch_count":25}' --json
```

The starter flow is capped at 25 leads. A queued or running response is not success; inspect or wait for the durable recipe run before claiming usable leads.

### Provider connections

Credential mutation and testing require a human organization admin. Keep secrets on stdin and never place them in arguments, logs, issue bodies, or recipe inputs.

```bash
printf '%s' "$APIFY_API_TOKEN" | coil --profile prod integrations set apify --json
coil --profile prod integrations status apify --json
coil --profile prod integrations test apify --json
coil --profile prod integrations rotate --json
coil --profile prod integrations rotate --apply --json
coil --profile prod integrations disconnect apify --json
```

### Recipes and durable runs

```bash
coil --profile prod recipes list --status published --json
coil --profile prod recipes view <recipe-id> --json
coil --profile prod recipes validate <recipe-id> --json
coil --profile prod recipes run <recipe-id> --confirm-provider-spend --new-scrape-name "Q2 prospects" --input '{"fetch_count":100}' --json
coil --profile prod recipe-runs view <run-id> --json
coil --profile prod recipe-runs wait <run-id> --timeout 300 --interval 2 --json
coil --profile prod recipe-runs cancel <run-id> --json
coil --profile prod recipe-runs retry <run-id> --json
```

Publication and ambiguous-effect reconciliation require a human organization admin. If a run has an unresolved provider effect, relay the server-provided `human_action.url` from the view/wait/watch state (or `error.details.human_action` from a machine reconcile denial) verbatim. The URL opens `/dashboard/recipe-runs/{runId}` for evidence review; it is navigation only and does not prove provider acceptance or authorize a decision. Retry/cancel behavior follows the durable run state and `next_actions`, not the presence of a URL.

### Lead-list imports

```bash
coil --profile prod --json leads import ./prospects.csv --mapping '{"Work email":"email"}' --admission-key import-september-001
coil --profile prod recipe-runs view <run-id> --json
coil --profile prod recipe-runs import-outcomes <run-id> --outcome rejected --json
coil --profile prod recipe-runs leads <run-id> --json
```

Imports accept at most 2,000 data rows and 2 MiB of CSV input. Use header
mapping for ambiguous columns and a stable admission key when a retry could be
uncertain. A `202` response means durable admission, not terminal success. Do
not report completion until the run is terminal and its outcomes and attributed
leads have been inspected. Rejected-row PII is not printed. Successful inputs
are scrubbed after completion; failed or cancelled normalized replay data is
retained for up to 30 days. The original CSV is never stored.

### Scrapes

```bash
coil --profile prod scrapes list --json --output-version 2
coil --profile prod scrapes get <scrape-id> --json
coil --profile prod scrapes create --type prospect --name "Q2 prospects" --titles "VP Sales,Head of Growth" --locations "United States" --sizes "11-50,51-200" --confirm-provider-spend --json
printf '%s' "$LINKEDIN_COOKIE" | coil --profile prod scrapes create --type sales-nav --name "Sales Nav export" --url "https://www.linkedin.com/sales/search/people?..." --user-agent "Mozilla/5.0 ..." --cookie-stdin --confirm-provider-spend --json
```

### Leads

```bash
coil --profile prod leads list --limit 50 --json --output-version 2
# Add a scrape ID after `list` to scope the result to one run.
coil --profile prod leads get <lead-id> --json
coil --profile prod leads export <scrape-id> --output leads.csv
coil --profile prod leads export <scrape-id> --view <view-id> --output saved-view.csv
coil --profile prod leads export <scrape-id> --ids <lead-id-1>,<lead-id-2> --output selected.csv
coil --profile prod --json leads export <scrape-id> --output leads.csv
coil --profile prod leads emails <scrape-id>
```

### Automations

API-key agents can create draft automations. Human org admins publish drafts after validation.

Creation and successful draft validation may return a required `human_action`
with an absolute `/automations` URL. Tell the user that the draft is ready but
requires human admin review and publication, and relay `human_action.url`
verbatim. A machine publish attempt returns the same structured action in the
403 error details. When run or result state is `reconciliation_required`, the
same operations URL is a required human reconciliation handoff; never infer a
URL from a status string or replay the ambiguous webhook.

```bash
coil --profile prod automations create --name "Enrich leads" --webhook-url "https://hooks.example.com/enrich" --input-fields email,company_name --scope global --json
coil --profile prod automations list --status draft --json --output-version 2
coil --profile prod automations view <automation-id> --json
coil --profile prod automations validate <automation-id> --json
coil --profile prod automations results list --automation <automation-id> --json --output-version 2
coil --profile prod automations results links add <result-id> --kind webhook_evidence --url "https://logs.example.com/run/1" --label "n8n execution" --json
```

Publishing, deletion, and egress policy management require a human org admin session:

```bash
coil automations publish <automation-id> --json
coil automations policy get --json
coil automations policy set --domains hooks.example.com --fields email,company_name --json
```

### SmartLead

```bash
coil --profile prod integrations status smartlead --json
coil --profile prod smartlead campaigns --json
coil --profile prod smartlead sequences --campaign <campaign-id> --json
coil --profile prod smartlead send <scrape-id> --campaign <campaign-id> --filter '[{"column":"email","operator":"is_not_empty","value":""}]' --json
```

### Feedback

Use feedback when a Coil task exposes product friction or a platform bug. Do not include secrets.

```bash
coil feedback "SmartLead send failed for selected leads" --type bug --json
coil feedback draft --type feature "Add export link metadata" --json
coil feedback drafts --json --output-version 2
coil feedback resend <feedback-id> --json
```

## API Reference

Use the local reference files when you need raw HTTP details:

- `references/api-endpoints.md`
- `references/api-fields.md`

Prefer the CLI for routine operations because it handles auth, profiles, output normalization, and local retry behavior.
