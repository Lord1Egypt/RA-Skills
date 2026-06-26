---
name: clawpage-create-management-page
description: "Trigger when user asks for a management/admin page that lists all created pages in a read-only UI (keywords: 管理页, 页面管理, 列出所有页面, pages dashboard, admin page). This skill creates or updates the current management page. Default publish policy: TTL 3h and password protected."
---

# Clawpage Create/Update Management Page

## When to use

- User wants a page that displays all pages they have created
- User expects read-only management view (no edit/delete actions from UI)
- User asks to create or refresh the current management page

## Data-flow rule

> The default workflow pre-fetches page data **at publish time via CLI `curl`** (see Workflow step 3) and inlines the JSON into the static HTML. The rendered management page makes **zero live API calls from the browser**, ships **zero tokens**, and requires no SDK.
>
> **Never embed an `sk_*` owner token into browser-shipped JS — even on a pagecode-protected page.** Pagecodes can be shared, page HTML can be inspected, browser caches persist, and any leak gives full account control. There is currently no token-scoping primitive that can safely live in the browser.

### Refresh strategies

If the user asks to "refresh now" without re-publishing, pick the **least-privilege** option that meets their need:

1. **Republish (recommended default).** Treat refresh as a new publish run — re-fetch via CLI, re-render HTML, `npx -y @clawpage.ai/cli publish --page-id [PAGE_ID]`. Token never leaves the CLI / your machine. This is what every other Clawpage page does.
2. **Manual refresh button → CLI hint.** Render a button that copies the republish command to clipboard or links to a docs section; user runs it from their terminal.
3. **Public-data-only auto-refresh.** If the page only needs to refresh `public` data tables / public stats endpoints, embed the SDK **without any token** — anonymous public reads are safe even on a publicly accessible page.

**Forbidden:** any code that ships an `sk_*` token to the browser, including:
- `const c = new Clawpage({ token: "sk_..." })` in inline `<script>` tags
- token in `localStorage` / `sessionStorage` / cookies set by the page
- token in `data-*` attributes or HTML comments

## Inputs and conventions

- Management page directory (preferred fixed path): `~/.clawpage/pages/page-management-center`
- Management page bootstrap template (default): `general_template` (shipped with `@clawpage.ai/cli`; copy via `npx -y @clawpage.ai/cli scaffold general_template <target>`)
- Publish script: ``npx -y @clawpage.ai/cli publish``
- API reference: `${CLAUDE_SKILL_DIR}/references/api-quickref.md`
- Shared contracts: `${CLAUDE_SKILL_DIR}/references/prompt-contracts.md`
- Security defaults (unless user explicitly overrides):
  - `ttlMs = 10800000` (3 hours)
  - must be password protected (`pagecode` must not be null/empty)

## Workflow

1. Resolve `[MANAGEMENT_PAGE_DIR]` once:
- A valid management-page project must satisfy both:
  - has `meta.md`
  - `meta.md` contains `metadata.management_page: true`
- Preferred path: `~/.clawpage/pages/page-management-center`
- If the preferred path does not exist or lacks the marker, scan both `~/.clawpage/pages/*/meta.md` and `./.pages/*/meta.md` for projects satisfying the rule and pick one deterministic path.
- If none found, initialize a new project:
  - if `~/.clawpage/pages/page-management-center` does not exist: use it.
  - if it exists but lacks the marker: use `~/.clawpage/pages/page-management-center-v2` (or next available `-vN`). Project-scoped equivalent: `./.pages/page-management-center` / `-vN`.

**Note:** Replace `[MANAGEMENT_PAGE_DIR]` with the resolved path. The CLI accepts bare names (`page-management-center` → `~/.clawpage/pages/page-management-center`) and cwd-relative paths.

```bash
npx -y @clawpage.ai/cli scaffold general_template [MANAGEMENT_PAGE_DIR]
```

2. Ensure metadata in `[MANAGEMENT_PAGE_DIR]/meta.md` is explicit:
- `metadata.name`
- `metadata.description`
- required marker: `metadata.management_page: true`

3. Pull latest page list via API. 
- Use the token from `~/.clawpage/keys.local.json` (or `./keys.local.json` if project-scoped).
- Example command:
```bash
curl -sS https://api.clawpage.ai/api/pages?page=1&limit=50 \
  -H "Authorization: Bearer [YOUR_TOKEN]"
```
- include key fields: `pageId`, `pageName`, `rootUrl`, `publicUrl`, `currentVersion`, expiry/protection status.
- capture data acquisition time as `dataFetchedAt` (ISO string + readable local time).
- The management page stays static — the rendered HTML ships with the data pre-inlined; it does NOT re-fetch in the browser. If the user explicitly asks for live refresh or edit actions, switch that surface to the Browser SDK per `${CLAUDE_SKILL_DIR}/use-sdk/SKILL.md` (and note the `/api/pages` SDK gap).

4. Build a high-quality read-only UI (refer to `${CLAUDE_SKILL_DIR}/references/design-guidelines.md`):
- **Recommended tone:** professional / tech-dashboard — data-focused layout with clear hierarchy.
- clarity: search/filter/sort/read-only cards or table.
- no mutation controls (no delete/update API buttons).
- expose share-relevant URLs and protection/expiry summaries.
- show data acquisition time in the header: `Data fetched at: <dataFetchedAt> (<timezone>)`
- apply distinctive fonts and cohesive color palette per design guidelines.
- add page-load stagger animations for the page card list.

5. Apply localization/output contracts from `${CLAUDE_SKILL_DIR}/references/prompt-contracts.md`.

6. Pre-publish hard checks (must pass):
- `meta.md` metadata complete.
- required placeholders preserved.
- dry-run succeeds.

7. Publish:
- **Identify PAGE_ID**: Use `read_file` to read `[MANAGEMENT_PAGE_DIR]/meta.md` and extract `metadata.page_id` from the YAML frontmatter. Do not use fragile shell regex.
- **Identify PAGECODE**: If creating or if a reset is needed, generate a 6-8 character random safe string (e.g., base64url or alphanumeric).

- **Create mode** (if `page_id` is missing):
```bash
npx -y @clawpage.ai/cli publish \
  --page-dir [MANAGEMENT_PAGE_DIR] \
  --title "[TITLE]" \
  --subtitle "[SUBTITLE]" \
  --ttl-ms 10800000 \
  --pagecode "[GENERATED_PAGECODE]"
```
- Write back the returned `pageId` to `metadata.page_id` in `[MANAGEMENT_PAGE_DIR]/meta.md`.

- **Update mode** (if `page_id` exists):
```bash
npx -y @clawpage.ai/cli publish \
  --page-dir [MANAGEMENT_PAGE_DIR] \
  --page-id "[PAGE_ID]" \
  --title "[TITLE]" \
  --subtitle "[SUBTITLE]" \
  --ttl-ms 10800000
```
- *Note:* Add `--pagecode "[GENERATED_PAGECODE]"` only if rotating password or enforcing security on a previously public page.

8. Return fixed output fields from `${CLAUDE_SKILL_DIR}/references/prompt-contracts.md`.

9. Mandatory post-publish reminder:
- state: "This management page is valid for 3 hours by default and is password protected."
- include actual values: `ttlMsApplied`, `expiresAt`, `pagecodeProtected`, `pagecode`, `dataFetchedAt`.


## Failure handling (error code -> action)

- `LOCAL_KEYS_FILE_MISSING` or `LOCAL_TOKEN_MISSING` -> **stop and confirm with the user before registering.** Show:
  > "No Clawpage account is configured. To create a management page I need to register a new account. This creates a long-lived API token at `~/.clawpage/keys.local.json`. Proceed? (yes / pick a username / cancel)"
  
  Only run `npx -y @clawpage.ai/cli init` after explicit `yes`.
- `UNAUTHORIZED` -> verify token in `./keys.local.json`, then retry.
- `PAGE_NOT_FOUND` -> verify bound `pageId`; if missing/invalid, create once then persist returned `pageId`.
- `USERNAME_TAKEN` (register flow) -> propose 3 alternatives, user picks one, retry register.
- `IP_DAILY_REGISTRATION_LIMIT_REACHED` -> stop and ask user to retry next day or use existing account.
- `OWNER_DAILY_PAGE_CREATE_LIMIT_REACHED` -> stop create attempts and retry later.
- `OWNER_MONTHLY_PERMANENT_PAGE_LIMIT_REACHED` -> keep management page temporary (3h TTL), avoid permanent publish.
- `NETWORK_ERROR` / `SERVER_ERROR` -> report status/body context and retry after network/server check.
