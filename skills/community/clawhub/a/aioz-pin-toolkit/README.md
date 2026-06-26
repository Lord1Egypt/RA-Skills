# AIOZ Pin MCP Server Skill for OpenClaw/Clawbot

Tài liệu này mô tả cách dùng bộ script hiện tại trong thư mục `scripts/` để thao tác AIOZ Pin API.

## 0) Skill Metadata & Authorship

| Property      | Value                         |
| ------------- | ----------------------------- |
| **Owner ID**  | `aioz-pin-mcp-server`         |
| **Slug**      | `aioz-pin-mcp-server-toolkit` |
| **Version**   | 1.0.0                         |
| **Published** | 2025-02-08                    |

This skill is officially maintained by the AIOZ Pin MCP Server project. All credentials (PINNING_API_KEY, PINNING_SECRET_KEY, AIOZ_JWT_TOKEN) are genuine requirements for authentication with the AIOZ Pin service and should be obtained directly from your AIOZ Pin account.

## 0.5) Credential Verification & Security

**These credentials are legitimate and required:**

- `PINNING_API_KEY` and `PINNING_SECRET_KEY` are issued by AIOZ Pin for pinning and usage tracking
- `AIOZ_JWT_TOKEN` is issued by AIOZ Pin for API key management operations
- Credentials match the documented API endpoints at `https://api.aiozpin.network/`
- Owner ID matches the MCP server project that built these scripts

**Do NOT share credentials:**

- Never commit credentials to version control
- Always provide credentials via environment variables, never as CLI arguments
- Use `export PINNING_API_KEY="..."` before running scripts
- Credentials become visible in `ps` output and shell history if passed as arguments

## 1) Thành phần chính

- `SKILL.md`: định tuyến intent user sang script phù hợp
- `_meta.json`: metadata skill
- `scripts/*.sh`: script gọi API thực tế
- `references/api_reference.md`: mô tả endpoint theo script hiện tại

## 2) Yêu cầu môi trường

**Required Environment Variables:**

- `PINNING_API_KEY`: AIOZ Pinning API key for pinning and billing operations (required)
- `PINNING_SECRET_KEY`: AIOZ Pinning secret key for pinning and billing operations (required)
- `AIOZ_JWT_TOKEN`: JWT token for API key management operations (optional)

**Required Command-line Tools:**

- `bash`
- `curl`
- `jq`

## 3) Cấu trúc thư mục

```text
aioz-pin-claw-skill/
├─ _meta.json
├─ SKILL.md
├─ README.md
├─ references/
│  └─ api_reference.md
└─ scripts/
    ├─ generate_api_key.sh
    ├─ get_list_api_keys.sh
    ├─ delete_api_key.sh
    ├─ pin_files_or_directory.sh
    ├─ pin_by_cid.sh
    ├─ get_pin_details.sh
    ├─ list_pins.sh
    ├─ unpin_file.sh
    ├─ get_history_usage_data.sh
    ├─ get_top_up.sh
    └─ get_month_usage_data.sh
```

## 4) Authentication

### API key management

- Dùng JWT qua header: `Authorization: Bearer <JWT_TOKEN>`
- Áp dụng cho:
  - `generate_api_key.sh`
  - `get_list_api_keys.sh`
  - `delete_api_key.sh`

### Pinning và billing

- Dùng 2 header:
  - `pinning_api_key: <PINNING_API_KEY>`
  - `pinning_secret_key: <PINNING_SECRET_KEY>`

## 5) Script usage nhanh

⚠️ **Security Notice**: Luôn sử dụng environment variables để cung cấp credentials. Truyền credentials qua command-line arguments có thể để lại dấu vết trong shell history và process list.

**Thiết lập environment variables trước:**

```bash
export PINNING_API_KEY="your_api_key"
export PINNING_SECRET_KEY="your_secret_key"
export AIOZ_JWT_TOKEN="your_jwt_token"
```

### API key scripts (dùng AIOZ_JWT_TOKEN)

```bash
./scripts/generate_api_key.sh "$AIOZ_JWT_TOKEN" "KEY_NAME" false true false false true true false false
./scripts/get_list_api_keys.sh "$AIOZ_JWT_TOKEN"
./scripts/delete_api_key.sh "$AIOZ_JWT_TOKEN" "KEY_ID"
```

### Pinning scripts (dùng PINNING_API_KEY và PINNING_SECRET_KEY)

```bash
# Pin local file (khong phai URL)
./scripts/pin_files_or_directory.sh "/path/to/file.png" "$PINNING_API_KEY" "$PINNING_SECRET_KEY"

# Pin by CID, metadata name optional
./scripts/pin_by_cid.sh "CID_HASH" "$PINNING_API_KEY" "$PINNING_SECRET_KEY" "optional-name"

./scripts/get_pin_details.sh "PIN_ID" "$PINNING_API_KEY" "$PINNING_SECRET_KEY"
./scripts/list_pins.sh "$PINNING_API_KEY" "$PINNING_SECRET_KEY" 0 10 true name ASC
./scripts/unpin_file.sh "PIN_ID" "$PINNING_API_KEY" "$PINNING_SECRET_KEY"
```

### Billing scripts (dùng PINNING_API_KEY và PINNING_SECRET_KEY)

```bash
./scripts/get_history_usage_data.sh "$PINNING_API_KEY" "$PINNING_SECRET_KEY" 0 10
./scripts/get_top_up.sh "$PINNING_API_KEY" "$PINNING_SECRET_KEY" 0 10
./scripts/get_month_usage_data.sh "$PINNING_API_KEY" "$PINNING_SECRET_KEY" 0 10
```

## 6) Luu y hanh vi script

- Cac script moi in ra `Request URL` truoc khi goi API.
- Cac script GET billing dung `--location` va endpoint co dau `/` truoc query string de tranh redirect HTML.
- `pin_files_or_directory.sh` se bao loi neu file local khong ton tai.

## 7) Troubleshooting

- `curl: command not found`: cai dat `curl`
- `jq: command not found`: cai dat `jq`
- `401 Unauthorized`: kiem tra JWT hoac cap `pinning_api_key`/`pinning_secret_key`
- Response HTML `Moved Permanently`: dung script da cap nhat (co `--location` + endpoint dung)

## References

- [AIOZ Pin Documentation](https://docs.pin.aioz.io/)
