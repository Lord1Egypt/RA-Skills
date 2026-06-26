# Clawpage Prompt Contracts

Use this file as the single source for shared prompt contracts across router/create/update skills.

## 1. Placeholder Ownership & Localization Contract

**A. System-Managed Placeholders (DO NOT REPLACE)**
- Format: `__UPPERCASE__` (e.g., `__DEFAULT_CSS__`, `__DEFAULT_JS__`).
- Rule: The Agent **must leave these untouched** in the HTML. The publish script will compute and replace them automatically.
- *Exception*: `__CONTENT_HTML__` MUST be replaced by the Agent with rich UI components (including page title, subtitle, timestamps, and any metadata the page needs).

**B. LLM-Rendered Content**
- The Agent renders **everything visible** on the page: title, subtitle, and all UI content.
- The Agent should write the page `<title>` tag directly with the actual title.
- **Do NOT show expiry time on the page.** Expiry is a hosting detail, not page content — communicate it to the user in the post-publish chat message using `expiresAt` from the JSON result.
- User-visible text must be localized to the user's language; infer language from prompt and ask only when unclear.

## 2. Output Schema (Fixed Fields)

For successful create/update runs, always return these fields in the JSON output (field names must stay stable):

| field | required | nullable | meaning |
|---|---|---|---|
| `summary` | yes | no | 1-2 sentence human summary |
| `mode` | yes | no | `created` or `updated` |
| `pageId` | yes | no | remote page id |
| `publicUrl` | yes | yes | public sharing URL when no password |
| `rootUrl` | yes | yes | preview URL without `pagecode` |
| `accessUrl` | yes | yes | URL with `pagecode` when protected (always in JSON, see Sharing Contract for human text) |
| `shareRecommendedUrl` | yes | yes | prefer `publicUrl`, otherwise `rootUrl` |
| `pagecode` | yes | yes | current pagecode if any |
| `pagecodeProtected` | yes | yes | whether page is password protected |
| `pagecodeUpdated` | yes | no | whether protection changed this run |
| `ttlMsApplied` | yes | yes | effective TTL after this run |
| `expiresAt` | yes | yes | effective expiry ISO timestamp |
| `warnings` | yes | no | array of strings for quota/limit warnings (may be empty if endpoint provides none) |
| `htmlPath` | yes | no | local bundled html path |

Failure output must include:

| field | required | meaning |
|---|---|---|
| `ok` | yes | always `false` |
| `errorCode` | yes | normalized error code |
| `errorMessage` | yes | short root cause |
| `action` | yes | concrete next action |

When calling `npx -y @clawpage.ai/cli publish`, this schema should be emitted as JSON even on failure (`ok: false` + non-zero exit code).

## 3. Sharing Contract (Human-readable responses)

- If `publicUrl` exists, recommend sharing `publicUrl`.
- If `publicUrl` is null and protection exists, you **MUST provide BOTH the `accessUrl` (for easy one-click access) AND the `rootUrl`** alongside the `pagecode`.
- Always provide the `pagecode` (访达码) as a separate clearly visible text block so the user can easily copy and input it.

## 4. Pre-Publish Hard Checklist

Run and pass all checks before publish:

1. `meta.md` metadata is complete (`metadata.name`, `metadata.description`; keep/update `metadata.page_id` when available).
2. Required HTML placeholders are preserved: `__CONTENT_HTML__`, `__DEFAULT_CSS__`, `__DEFAULT_JS__`.
3. Dry-run succeeds: `npx -y @clawpage.ai/cli publish --page-dir <dir> --dry-run`.
4. **Non-empty content gate (mandatory):** before returning links, verify published HTML is not an empty shell.
   - Ensure `index.html` does not leave `__CONTENT_HTML__` unresolved — it must be replaced with real content HTML before publish.
   - If this gate fails, do not send URL; fill in the content and republish first.

## 5. Error Code -> Action Mapping

- `LOCAL_KEYS_FILE_MISSING` or `LOCAL_TOKEN_MISSING`: **always require explicit user confirmation before registering an account.** Account registration creates a long-lived `sk_*` token persisted to `~/.clawpage/keys.local.json` — that's a credential side effect the user must consent to. Show the user:
  > "I need a Clawpage account to publish. Should I register a new one? (yes / suggest username `<X>` / cancel)"
  
  Only after explicit `yes` (or username acceptance), run `npx -y @clawpage.ai/cli init [username]`. **DO NOT create a Clawpage intro/welcome page after registration** — go directly to the user's original request.
- `UNAUTHORIZED` (HTTP 401): verify `keys.local.json` token, then retry publish.
- `PAGE_NOT_FOUND` (HTTP 404): verify `pageId` ownership/existence; if local page has no binding, create first and write back `pageId`.
- `409 USERNAME_TAKEN`: for register flow, propose 3 alternatives and retry with user choice.
- `429 IP_DAILY_REGISTRATION_LIMIT_REACHED`: stop and ask user to retry next day or use existing account.
- `429 OWNER_DAILY_PAGE_CREATE_LIMIT_REACHED`: stop create attempts and ask user to retry later.
- `429 OWNER_MONTHLY_PERMANENT_PAGE_LIMIT_REACHED`: suggest shorter TTL or deleting/repurposing permanent pages.
- `NETWORK_ERROR`: check network connectivity/DNS and api-host reachability, then retry.
- `SERVER_ERROR`: keep request payload and retry later after checking server status / `--api-host`.
