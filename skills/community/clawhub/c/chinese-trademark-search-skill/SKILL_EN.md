---
name: chinese-trademark-search-skill
description: Connects to the Chinese trademark search hosted platform API, handling trademark search, details, export, points and module checks, and binding guidance. Designed for use within OpenClaw / ClawHub via a local Node CLI skill invocation.
homepage: https://tm.zhengquai.com
metadata: {"skillKey":"chinese-trademark-search-skill","homepage":"https://tm.zhengquai.com","tags":["china","trademark","商标","search","openclaw","clawhub"]}
---

# Chinese Trademark Search Skill

This Skill connects to a "proprietary trademark SaaS platform API" within OpenClaw / ClawHub, enabling Chinese trademark search, detail viewing, export, module inspection, points checking, and binding guidance.

## Connection Boundaries

- This Skill only connects to the hosted platform API; it does not connect directly to upstream trademark data providers.
- It never asks users for upstream trademark API credentials.
- Users only need to configure a platform-level user token.
- If a user has not yet bound their platform account or organization, guide them through binding first, then proceed with search, detail, export, and other actions.
- Never fabricate trademark data; if nothing is found, state that clearly.
- Prefer summary display to avoid overly long output at once.

## OpenClaw Invocation

OpenClaw should invoke this Skill via the local Node CLI:

```bash
node {baseDir}/scripts/cli.mjs help
node {baseDir}/scripts/cli.mjs bind-help
node {baseDir}/scripts/cli.mjs capabilities
node {baseDir}/scripts/cli.mjs search --query "华源科技"
node {baseDir}/scripts/cli.mjs detail --tmid "tm_20260310_0001"
node {baseDir}/scripts/cli.mjs export --queryId "qry_20260310_0008" --tmids "tm_001,tm_002"
node {baseDir}/scripts/cli.mjs export-status --jobId "exp_20260310_0003"
node {baseDir}/scripts/cli.mjs modules
```

## Conversation Strategy

### 1. Prioritize Binding Guidance When Unbound

If any of `capabilities`, `search`, `detail`, `export`, or `modules` responses indicate the user is not bound:

- First call `bind-help`
- Tell the user the platform URL: `https://tm.zhengquai.com`
  - Registration page: `https://tm.zhengquai.com/register`
  - API Key generation: after logging in, go to the settings page `https://tm.zhengquai.com/settings/api-keys` (keys use the `tmu_` prefix and are shown only once at creation)
- Explain the binding steps
- Tell the user to complete binding before continuing with search or export
- Do not execute any cost-bearing actions

### 2. Notify Estimated Point Cost Before Search / Detail / Export

Before initiating any cost-bearing action, inform the user:

- Before search: estimated cost of 1 point (returns the first 50 results)
- Before detail: estimated cost of 2 points (viewing a trademark whose detail was already purchased is not charged again)
- Before export: estimated cost based on item count

Export estimated point cost tiers:

- 1-10 items: 1 point
- 11-50 items: 3 points
- 51-100 items: 5 points
- 101+ items: 10 points

Pagination: **not currently supported**. Each search returns only the first page (up to 50 results); passing `--page` greater than 1 is rejected locally by the CLI (`PAGINATION_NOT_SUPPORTED`) — no request is sent and no points are charged. `--pageSize` is deprecated; the platform always returns 50. If the user asks for the next page, explain that pagination is not currently supported and suggest refining the search keyword.

Trial points: new organizations receive 100 trial points valid for 90 days. The balance returned by `capabilities` is authoritative.

Billing reliability: failed searches (upstream errors) are automatically refunded; failed detail lookups (upstream errors) are automatically refunded; failed export job creation is automatically refunded. The CLI automatically attaches an idempotency header `X-OC-Request-Id`, so network retries will not cause double charges. When the platform refunds a charge it also releases that idempotency key, so retrying after a refund is charged normally — it is not a free retry.

### 3. Handling Insufficient Points

If the platform returns an insufficient points error (HTTP 402, error code `POINTS_NOT_ENOUGH`):

- Clearly state "insufficient points"
- Guide the user to top up: the `rechargeUrl` in the 402 response body (`https://tm.zhengquai.com/billing`) can be given to the user directly
- Never fabricate results
- Never retry cost-bearing API calls repeatedly

### 4. Handling Disabled Modules

If the platform returns a module-not-enabled error:

- Clearly state the specific module name
- Guide the user to purchase the corresponding module
- Never bypass platform module restrictions

Modules that may be involved:

- Renewal Monitoring
- Notifications
- WeChat Mini Program
- Company Page / Client Page
- External Monitoring
- White-Label Portal

### 5. Output Style

- Provide a summary first, then necessary details
- When there are too many search results, display the first few and explain that only the first 50 results are returned and pagination is not currently supported
- For export jobs, prioritize showing job status, estimated points, and how to retrieve the export file
- For any uncertain information, state "subject to platform response"

## Recommended Workflows

### Search

1. If needed, first call `capabilities`
2. Inform the user: "Estimated cost: 1 point"
3. Execute `search --query "<keyword>"`
4. Display a summary of results and remaining points (only the first page of up to 50 results is returned; pagination is not currently supported)

### Detail

1. Inform the user: "Estimated cost: 2 points" (viewing a trademark whose detail was already purchased is not charged again)
2. Execute `detail --tmid "<tmid>"`
3. Return core information: trademark name, applicant, international class, application number, registration number, status, validity period, etc.

### Export

1. First confirm how many items the user wants to export
2. Inform estimated point cost based on item count
3. Execute `export --queryId "<queryId>" --tmids "<comma-separated>"`
4. Return the export job ID, job status, estimated or actual point charge
5. To check export status, execute `export-status --jobId "<exportJobId>"` (a single check — the CLI never polls internally)
6. If the response carries `pending: true` (status `queued` / `processing`), run the command again later; if `completed`, return the download link

### Modules / Balance / Capabilities

1. Execute `capabilities` or `modules`
2. Describe the balance, available modules, and restricted actions
3. If there are disabled modules, clearly identify the module name and its purpose

## Legal Disclaimer

Trademark search results are for reference only, not legal advice. Users should consult a qualified trademark attorney or agent for legal guidance.
