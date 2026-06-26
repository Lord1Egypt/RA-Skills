# Lark/Feishu Sheets & Drive OpenAPI Reference

Quick reference for the Sheets and Drive APIs used by this skill.

---

## Authentication

### Get Tenant Access Token

```
POST /open-apis/auth/v3/tenant_access_token/internal
```

Body:
```json
{"app_id": "cli_xxx", "app_secret": "xxx"}
```

Response:
```json
{"code": 0, "tenant_access_token": "t-xxx", "expire": 7200}
```

All subsequent requests use header: `Authorization: Bearer {tenant_access_token}`

---

## Spreadsheet Operations

### List Sheet Tabs

```
GET /open-apis/sheets/v3/spreadsheets/{spreadsheet_token}/sheets/query
```

Response:
```json
{
  "code": 0,
  "data": {
    "sheets": [
      {"sheet_id": "abc123", "title": "Sheet1", "index": 0},
      {"sheet_id": "def456", "title": "Sheet2", "index": 1}
    ]
  }
}
```

### Read Cell Values (Batch)

```
GET /open-apis/sheets/v2/spreadsheets/{spreadsheet_token}/values_batch_get?ranges={sheetId}!A1:Z200
```

- Multiple ranges: repeat `ranges` parameter.
- Range format: `{sheetId}!A1:Z200` or `{sheetTitle}!A1:Z200`.

Response:
```json
{
  "code": 0,
  "data": {
    "valueRanges": [
      {"range": "abc123!A1:Z200", "values": [["cell1", "cell2"], ["cell3", "cell4"]]}
    ]
  }
}
```

### Write Cell Values (Batch)

```
POST /open-apis/sheets/v2/spreadsheets/{spreadsheet_token}/values_batch_update
```

Body:
```json
{
  "valueRanges": [
    {"range": "abc123!A1:C2", "values": [["a", "b", "c"], ["d", "e", "f"]]}
  ],
  "valueInputOption": "USER_ENTERED"
}
```

`valueInputOption`:
- `USER_ENTERED` — the API parses values as if typed by a user (auto-detect numbers, dates, etc.)
- `RAW` — values are stored as-is (all strings)

### Add Sheet Tab

```
POST /open-apis/sheets/v2/spreadsheets/{spreadsheet_token}/sheets_batch_update
```

Body:
```json
{
  "requests": [
    {"addSheet": {"properties": {"title": "NewSheet"}}}
  ]
}
```

Response includes the new `sheetId` in `data.replies[0].addSheet.properties.sheetId`.

---

## Drive Operations

### Download File

```
GET /open-apis/drive/v1/files/{file_token}/download
```

- Response is binary file content (not JSON).
- The app/bot must have access to the file (shared to the app).

### Extracting file token from URL

```
https://xxx.larksuite.com/file/YOUR_FILE_TOKEN
                                ^^^^^^^^^^^^^^^
                                file_token
```

---

## URL Patterns

### Feishu (China)
```
Base: https://open.feishu.cn
Sheet URL: https://xxx.feishu.cn/sheets/{spreadsheet_token}?sheet={sheetId}
```

### Lark (International)
```
Base: https://open.larksuite.com
Sheet URL: https://xxx.larksuite.com/sheets/{spreadsheet_token}?sheet={sheetId}
```

### Extracting tokens from URL

```
https://xxx.larksuite.com/sheets/YOUR_SPREADSHEET_TOKEN?sheet=SHEET_ID
                                  ^^^^^^^^^^^^^^^^^^^^^^^^^    ^^^^^^^^
                                  spreadsheet_token            sheetId
```

---

## Common Error Codes

| Code | Meaning | Fix |
|------|---------|-----|
| 0 | Success | — |
| 99991663 | No permission | Share the sheet with the app, or enable Sheets permission in dev console |
| 99991668 | Invalid range | Check sheetId/title and range format |
| 99991400 | Bad request | Verify request body format |
| 99991672 | Sheet title already exists | Use a unique title for addSheet |

---

## Rate Limits

- Tenant token: ~20 requests/second per app
- Sheets read/write: ~50 requests/second per spreadsheet
- Token expires in 2 hours; re-fetch as needed
