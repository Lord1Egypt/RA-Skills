---
name: app-store-connect
description: This skill should be used when the user asks about App Store Connect data — their apps, builds, TestFlight beta testers, customer reviews, sales reports, or team users. Triggers on phrases like "check App Store Connect", "list my apps", "TestFlight builds", "beta testers", "App Store reviews", "respond to review", "sales report", "invite tester", "App Store Connect users", or any request involving Apple developer / App Store Connect / TestFlight management.
---

# app-store-connect-mcp

MCP server for App Store Connect — 22 tools covering apps, TestFlight, customer reviews, sales/finance reports, team users, and a credential healthcheck via the [App Store Connect API](https://developer.apple.com/documentation/appstoreconnectapi).

## Setup

Set three env vars in your MCP host config:

- `APP_STORE_CONNECT_KEY_ID` — 10-character Key ID (e.g. `ABC1234567`)
- `APP_STORE_CONNECT_ISSUER_ID` — Team Issuer ID (UUID)
- `APP_STORE_CONNECT_PRIVATE_KEY_PATH` — absolute path to your downloaded `.p8` file (or paste PEM into `APP_STORE_CONNECT_PRIVATE_KEY`)

Generate a key at [appstoreconnect.apple.com → Users and Access → Integrations → App Store Connect API](https://appstoreconnect.apple.com/access/integrations/api). Save the `.p8` (only downloadable once).

## Tools

### Apps
- `list_apps` — List apps (filter by bundleId/name)
- `get_app` — App details by ID
- `list_app_store_versions` — Releases for an app
- `get_app_infos` — Age rating and store-state info

### TestFlight
- `list_builds` — Recent builds, newest first
- `get_build` — Single build details
- `list_beta_groups` — Internal & external beta groups
- `list_beta_testers` — Testers, filter by app/group/email
- `invite_beta_tester` — Add a new tester (optionally to groups/builds)
- `delete_beta_tester` — Remove tester from team
- `add_testers_to_beta_group` — Bulk add to a group
- `remove_testers_from_beta_group` — Bulk remove from a group
- `submit_build_for_beta_review` — Send build for beta review

### Customer Reviews
- `list_customer_reviews` — Reviews for an app, filter by rating/territory
- `get_customer_review` — Single review with developer response
- `respond_to_review` — Post or update reply

### Sales & Finance
- `download_sales_report` — Daily/weekly/monthly/yearly units & sales TSV
- `download_finance_report` — Region-scoped finance/proceeds TSV; `Total_*` trailer lines come back in a separate `summary` object, not in `rows`

### Team Users
- `list_users` — Team users
- `list_user_invitations` — Pending invitations
- `invite_user` — Invite new team member with roles; app visibility is explicit: `allAppsVisible: true` or a non-empty `visibleAppIds` (there is no all-apps default, and `allAppsVisible: false` alone is refused)

### Health
- `asc_healthcheck` — Is this connector working? Reports which of the three key settings resolved, whether App Store Connect accepted the signed JWT, and what to fix. Start here when another tool fails: a 401 here means a revoked key, a key/issuer team mismatch, or local clock drift — never a wrong password.

## Common workflows

**Triage low-rated reviews**
1. `list_customer_reviews` with `rating: 1` (sorted `-createdDate` by default)
2. For each, `get_customer_review` to see if there's already a response
3. `respond_to_review` to reply

**Promote a build to external testers**
1. `list_builds` with `appId` to find the build (look for `processingState: VALID`)
2. `submit_build_for_beta_review` with that build's ID
3. After Apple approval, `add_testers_to_beta_group` for the external group

**Onboard a new beta tester**
1. `list_beta_groups` with `appId` to find the right group
2. `invite_beta_tester` with `email`, optional name, and `betaGroupIds`

**Daily sales pull**
- `download_sales_report` with your `vendorNumber` (from App Store Connect → Payments and Financial Reports), `reportDate: YYYY-MM-DD`, default `frequency: DAILY`
- Reports are typically available ~24h after the close of the date

## Notes

- App Store Connect uses JSON:API: filters are `filter[name]=value`, sorts use `-` prefix for descending.
- Every write (invites, deletions, group membership, review responses, beta review submission) asks the user to confirm first. Where the client can show a prompt, it does (unless the server sets `MCP_CONFIRM_ELICITATION=off`). Otherwise the first call sends nothing and returns `status: "confirmation-required"` with a preview and a `confirmToken`: show the preview to the user, and only after they approve call the same tool again with the same arguments plus `confirmToken`. Tokens are single-use and expire; if the arguments change you get `DRAFT_CHANGED` with a fresh preview.
- All write operations (invites, deletions, review responses, beta review submission) require an API key with sufficient role (App Manager or Admin for most TestFlight/team work).
- Sales reports come back as gzipped TSVs and are auto-parsed into row objects. The tool truncates after `limit` rows (default 500) but reports the total row count.
- Expect a real `.p8` file path (or PEM string). The MCP signs short-lived (20-minute) ES256 JWTs locally — your private key never leaves the machine.
