---
name: feishu-openapi
description: |
  Use this skill for Feishu/Lark OpenAPI integration work: configuring OpenClaw Feishu bot accounts, setting app credentials outside the skill, reading or writing Feishu Docx documents, creating user-owned docs, appending or editing blocks, and using Sheets, Base, Wiki, Drive, or IM APIs. Trigger when the user asks for 飞书 API, 飞书在线文档 API, OpenAPI, app id or app secret setup, document token handling, OpenClaw Feishu routing, or replacing lark-cli with direct API calls.
---

# Feishu OpenAPI

## Purpose

Use this skill to connect an OpenClaw agent to Feishu/Lark through bot routing plus direct OpenAPI calls. The package is portable: another user supplies only their app credentials, user OAuth token when needed, account IDs, folder IDs, document tokens, and target content.

## API-Only Rule

All Feishu document and content operations must use OpenAPI through this skill's scripts. Do not use `lark-cli`, Feishu CLI tools, browser automation, or copied browser cookies for Docx, Sheets, Base, Wiki, Drive, or IM operations. OpenClaw CLI is allowed only for OpenClaw routing and channel checks, such as `openclaw agents bind` or `openclaw channels status`.

## Safety Rules

- Never print `.env`, app secrets, user access tokens, refresh tokens, or webhook secrets.
- Before write operations, identify whether the call uses a user token or tenant/app token.
- Treat `expires_in` and `refresh_token_expires_in` returned by Feishu as the source of truth. Do not hard-code token lifetimes.
- `refresh_token` is single-use. After any refresh, immediately persist both the new `FEISHU_USER_ACCESS_TOKEN` and the new `FEISHU_USER_REFRESH_TOKEN`.
- New cloud resources must be user-owned by default. For doc creation, prefer `FEISHU_USER_ACCESS_TOKEN`; only use app-owned creation when the user explicitly accepts that limitation.
- Sharing a bot-owned resource with the user is not the same as user ownership.
- For existing docs, do a read-only check first, then write, then verify by reading the updated doc or returned block IDs.
- If a tool action might already have run and the model response failed, verify current state before repeating the same write.
- Do not bake private IDs into reusable files. Put app IDs, app secrets, user IDs, tokens, folder tokens, and OpenClaw account IDs in `.env`, OpenClaw config, or command flags.

## Quick Start

1. Copy the skill directory into the target agent's skills folder.
2. Copy `references/env.example` to `.env` in the target workspace, then fill the required values.
3. Install optional service dependencies when using the full API wrapper:

```bash
python -m pip install -r scripts/requirements.txt
```

4. For user-owned document creation, get user tokens once:

```bash
python scripts/feishu_oauth_tool.py auth-url --env-file .env
# Open the returned authorization_url, authorize, then copy the full callback URL.
python scripts/feishu_oauth_tool.py exchange-code --env-file .env --callback-url "$CALLBACK_URL"
```

5. Run the standalone Docx helper with Python 3.9+:

```bash
python scripts/feishu_openapi_tool.py env-check --env-file .env
python scripts/feishu_openapi_tool.py resolve --input "https://example.feishu.cn/docx/ABC123"
python scripts/feishu_openapi_tool.py read-doc --doc "https://example.feishu.cn/docx/ABC123" --env-file .env
```

6. Run the full service wrapper for Sheets, Base, Wiki, Drive, and IM:

```bash
python scripts/feishu_service_tool.py wiki-list-spaces --env-file .env
python scripts/feishu_service_tool.py im-send-text --receive-id "$OPEN_ID" --text "hello" --env-file .env
```

## Environment Inputs

Required for tenant/app-token operations:

- `FEISHU_APP_ID`
- `FEISHU_APP_SECRET`
- `FEISHU_BASE_URL`, normally `https://open.feishu.cn`

Required for user-owned document creation:

- `FEISHU_USER_ACCESS_TOKEN`
- `FEISHU_USER_REFRESH_TOKEN` strongly recommended. User access tokens are short-lived; the helper can refresh and retry automatically when this is present.
- `FEISHU_OAUTH_REDIRECT_URI`, used by `scripts/feishu_oauth_tool.py` for first-time authorization.
- `FEISHU_OAUTH_SCOPE`, include `offline_access` when a refresh token is required.

Optional:

- `FEISHU_USER_OPEN_ID`
- `FEISHU_USER_TOKEN_FILE`, optional shared token store path. If omitted, the helper uses `~/.openclaw/feishu-user-tokens/<app-id-hash>.env` when available.
- `FEISHU_DEFAULT_FOLDER_TOKEN`

Read `references/setup.md` when setting up OpenClaw bot routing, credentials, OAuth, app permissions, or ownership behavior.

## Common Operations

Use `scripts/feishu_openapi_tool.py` for common Docx operations:

```bash
# Read a document by URL or token
python scripts/feishu_openapi_tool.py read-doc --doc "$DOC_URL" --env-file .env

# Create a user-owned document. This requires FEISHU_USER_ACCESS_TOKEN.
python scripts/feishu_openapi_tool.py create-doc --title "API test" --folder-token "$FOLDER_TOKEN" --env-file .env

# Append plain text to an existing doc
python scripts/feishu_openapi_tool.py append-text --doc "$DOC_TOKEN" --text "hello" --env-file .env

# Append red text
python scripts/feishu_openapi_tool.py append-text --doc "$DOC_TOKEN" --text "important" --red --env-file .env

# List document blocks for precise editing
python scripts/feishu_openapi_tool.py list-blocks --doc "$DOC_TOKEN" --env-file .env
```

Use `scripts/feishu_service_tool.py` when you need the broader service layer:

```bash
python scripts/feishu_service_tool.py doc-create --title "PRD" --folder-token "$FOLDER_TOKEN" --env-file .env
python scripts/feishu_service_tool.py sheet-query --spreadsheet "$SHEET_TOKEN" --env-file .env
python scripts/feishu_service_tool.py base-list-records --app "$BASE_TOKEN" --table-id "$TABLE_ID" --env-file .env
python scripts/feishu_service_tool.py drive-find-token --token "$FILE_TOKEN" --env-file .env
```

Read `references/interfaces.md` for the audited interface coverage and `references/operations.md` for command examples and write workflow.

## Portability Guidance

- Keep the public skill portable: no absolute paths, no local user secrets, no machine-specific agent names.
- Use `.env` for credentials and command flags for IDs or tokens.
- Keep the lightweight helper's interface stable: `env-check`, `resolve`, `read-doc`, `create-doc`, `append-text`, and `list-blocks`.
- Keep the full service wrapper's command names stable unless the corresponding service method changes.
- The copied `feishu_api` package under `scripts/` is self-contained for sharing and must not depend on the original user's OpenClaw workspace path.
