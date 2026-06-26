# Operations

## Stable Interface

The lightweight helper `scripts/feishu_openapi_tool.py` should keep these commands stable:

- `env-check`: validate required environment variables without printing secrets.
- `resolve`: extract a Feishu token from a URL or return the raw token.
- `read-doc`: fetch document metadata, raw content, and optional block summaries.
- `create-doc`: create a Docx document. User token is required unless `--allow-app-owned` is set.
- `append-text`: append a text or red-text block.
- `list-blocks`: list block IDs, block types, parent IDs, children, and readable text.

All document and content commands in this skill are OpenAPI-only. Do not route Docx, Sheets, Base, Wiki, Drive, or IM operations through `lark-cli`, Feishu CLI tools, browser cookies, or browser automation.

## Token Handling

Accept both full URLs and raw tokens. Common URL forms include:

- `https://tenant.feishu.cn/docx/{document_id}`
- `https://tenant.feishu.cn/doc/{document_id}`
- `https://tenant.feishu.cn/wiki/{wiki_token}`
- `https://tenant.feishu.cn/sheets/{spreadsheet_token}`
- `https://tenant.feishu.cn/base/{app_token}`

For Docx operations, prefer `/docx/{document_id}`.

User OAuth tokens are obtained and refreshed with `scripts/feishu_oauth_tool.py`:

```bash
python scripts/feishu_oauth_tool.py auth-url --env-file .env
python scripts/feishu_oauth_tool.py exchange-code --env-file .env --callback-url "$CALLBACK_URL"
python scripts/feishu_oauth_tool.py refresh --env-file .env
```

Use `offline_access` in `FEISHU_OAUTH_SCOPE` when a refresh token is required.

Use returned expiry fields exactly:

- `expires_in` controls when `FEISHU_USER_ACCESS_TOKEN` expires.
- `refresh_token_expires_in` controls when `FEISHU_USER_REFRESH_TOKEN` expires.
- Some legacy SDK responses use `refresh_expires_in`; scripts accept both names.
- Refresh tokens are single-use, so each refresh must persist the newly returned access token and refresh token before any later call.

## Full Service Wrapper

Use `scripts/feishu_service_tool.py` when the target environment can install `scripts/requirements.txt`. It wraps the copied `feishu_api` service layer and returns compact JSON.

Docx:

```bash
python scripts/feishu_service_tool.py doc-create --title "PRD" --folder-token "$FOLDER_TOKEN" --env-file .env
python scripts/feishu_service_tool.py doc-read --doc "$DOC_TOKEN" --blocks --env-file .env
python scripts/feishu_service_tool.py doc-append-text --doc "$DOC_TOKEN" --text "hello" --env-file .env
python scripts/feishu_service_tool.py doc-update-block-text --doc "$DOC_TOKEN" --block-id "$BLOCK_ID" --text "new text" --env-file .env
python scripts/feishu_service_tool.py doc-replace-section --doc "$DOC_TOKEN" --heading "验收标准" --paragraph "1. ..." --env-file .env
```

Sheets:

```bash
python scripts/feishu_service_tool.py sheet-create --title "Pipeline" --folder-token "$FOLDER_TOKEN" --env-file .env
python scripts/feishu_service_tool.py sheet-get --spreadsheet "$SHEET_TOKEN" --env-file .env
python scripts/feishu_service_tool.py sheet-query --spreadsheet "$SHEET_TOKEN" --env-file .env
python scripts/feishu_service_tool.py sheet-find --spreadsheet "$SHEET_TOKEN" --sheet-id "$SHEET_ID" --text "keyword" --env-file .env
python scripts/feishu_service_tool.py sheet-replace --spreadsheet "$SHEET_TOKEN" --sheet-id "$SHEET_ID" --find "old" --replacement "new" --env-file .env
```

Base:

```bash
python scripts/feishu_service_tool.py base-create --name "CRM" --folder-token "$FOLDER_TOKEN" --env-file .env
python scripts/feishu_service_tool.py base-list-tables --app "$BASE_TOKEN" --env-file .env
python scripts/feishu_service_tool.py base-create-table --app "$BASE_TOKEN" --name "Leads" --fields-json '[{"field_name":"Name","type":1}]' --env-file .env
python scripts/feishu_service_tool.py base-list-fields --app "$BASE_TOKEN" --table-id "$TABLE_ID" --env-file .env
python scripts/feishu_service_tool.py base-list-records --app "$BASE_TOKEN" --table-id "$TABLE_ID" --env-file .env
python scripts/feishu_service_tool.py base-create-record --app "$BASE_TOKEN" --table-id "$TABLE_ID" --fields-json '{"Name":"Alice"}' --env-file .env
python scripts/feishu_service_tool.py base-update-record --app "$BASE_TOKEN" --table-id "$TABLE_ID" --record-id "$RECORD_ID" --fields-json '{"Name":"Alice B"}' --env-file .env
```

Wiki, Drive, and IM:

```bash
python scripts/feishu_service_tool.py wiki-list-spaces --env-file .env
python scripts/feishu_service_tool.py wiki-list-nodes --space-id "$SPACE_ID" --env-file .env
python scripts/feishu_service_tool.py wiki-get-node --token "$WIKI_OR_DOC_TOKEN" --obj-type docx --env-file .env
python scripts/feishu_service_tool.py drive-list-files --env-file .env
python scripts/feishu_service_tool.py drive-find-token --token "$FILE_TOKEN" --env-file .env
python scripts/feishu_service_tool.py im-send-text --receive-id "$OPEN_ID" --receive-id-type open_id --text "hello" --env-file .env
python scripts/feishu_service_tool.py im-get-message --message-id "$MESSAGE_ID" --env-file .env
python scripts/feishu_service_tool.py im-list-messages --chat-id "$CHAT_ID" --start-time "$START" --end-time "$END" --env-file .env
python scripts/feishu_service_tool.py im-reply-text --message-id "$MESSAGE_ID" --text "收到" --env-file .env
```

## Write Workflow

1. Resolve URL or token.
2. Read the resource and summarize title, revision, and block count.
3. Perform the smallest write needed.
4. Verify with another read or by checking returned block IDs.
5. Report exactly what changed, without exposing credentials.

## Extending Beyond Docx

Use the same structure for Sheets, Base, Wiki, Drive, and IM:

- Add a command with explicit required IDs.
- Keep credentials in `.env`.
- Do not infer destructive writes from vague user text.
- For create operations, preserve the user-owned default.
- Return compact JSON with IDs, URLs, changed records, and verification status.

Suggested command names:

- `sheet-create`
- `sheet-find`
- `sheet-replace`
- `base-create`
- `base-create-table`
- `base-create-record`
- `im-send-text`
- `wiki-list-spaces`
