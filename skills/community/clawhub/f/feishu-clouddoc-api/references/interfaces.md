# Audited Interfaces

This package contains the Feishu OpenAPI interfaces currently used by the OpenClaw Feishu integration. Private app IDs, app secrets, user IDs, tokens, and workspace-specific account IDs are intentionally excluded.

Document and content interfaces are API-only. This package does not depend on `lark-cli` or any Feishu CLI state for Docx, Sheets, Base, Wiki, Drive, or IM operations.

## Bot And OpenClaw Integration

- OpenClaw Feishu account configuration through `channels.feishu.accounts.<account-id>`.
- Agent binding through `openclaw agents bind --agent <agent-id> --bind feishu:<account-id>`.
- Websocket bot connection mode.
- Pairing or allowlist-based DM access.
- Group allowlist plus mention behavior.

The skill documents the setup flow but does not write OpenClaw config by itself, because each install needs the target user's account IDs and secrets.

## Lightweight Docx Helper

Script: `scripts/feishu_openapi_tool.py`

Stable commands:

- `env-check`
- `resolve`
- `read-doc`
- `list-blocks`
- `create-doc`
- `append-text`

Use this helper first when only Docx read/create/append operations are needed. It is stdlib-first and can refresh user tokens when a refresh token or token store is configured.

## OAuth User Token Helper

Script: `scripts/feishu_oauth_tool.py`

Stable commands:

- `auth-url`: generate the Feishu authorization URL with state and optional PKCE.
- `exchange-code`: exchange the callback `code` for user tokens and save them outside the skill.
- `refresh`: refresh and persist user tokens.

This helper gets `FEISHU_USER_ACCESS_TOKEN` for user-owned operations. It stores secrets in `.env` or the shared local token store, never in the skill package.

## Full Service Wrapper

Script: `scripts/feishu_service_tool.py`

The wrapper exposes these areas:

- Docx: create, read, append text, append red text, update a block, replace a heading section.
- Sheets: create spreadsheet, get spreadsheet, list/query sheets, find text, replace text.
- Base: create base, list tables, create table, list fields, list records, create record, update record.
- Wiki: list spaces, list nodes, get node info.
- Drive: list files, find a file by token.
- IM: send text, get message, list chat messages, reply text.

Install `scripts/requirements.txt` before using the full wrapper.

## Copied Service Package

Package: `scripts/feishu_api/`

Included services:

- `DocsService`
- `SheetsService`
- `BaseAppService`
- `WikiService`
- `DriveService`
- `IMService`

The package is copied into the skill so the colleague does not need the original user's `~/.openclaw` workspace. It reads credentials from environment variables or an `.env` path supplied through `--env-file`.

## Credentials Kept Out Of Package

Configure these per install:

- `FEISHU_APP_ID`
- `FEISHU_APP_SECRET`
- `FEISHU_BASE_URL`
- `FEISHU_USER_ACCESS_TOKEN`
- `FEISHU_USER_REFRESH_TOKEN`
- `FEISHU_USER_OPEN_ID`
- `FEISHU_USER_TOKEN_FILE`
- `FEISHU_DEFAULT_FOLDER_TOKEN`
- OpenClaw Feishu account IDs and route bindings.

Never commit real values for these fields into the shared skill.
