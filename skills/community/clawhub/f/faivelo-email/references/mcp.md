# Faivelo MCP server

URL: `https://faivelo.com/api/mcp` (streamable HTTP). Registry name
`com.faivelo/mail`. Needs a Growth plan or higher, or the free trial.

## Auth

- **OAuth (interactive clients):** add the URL; the first call opens a
  browser where the user signs in and ticks which mailboxes the client may
  reach. Optionally allows creating new mailboxes (10 a day).
- **API key (headless agents):** `Authorization: Bearer fvl_live_...`.
  Clients that cannot set headers can use
  `https://faivelo.com/api/mcp/fvl_live_...` (the key then sits in config and
  logs; prefer the header).

## Add it

| Client | How |
| --- | --- |
| Claude Code | `claude mcp add --transport http faivelo https://faivelo.com/api/mcp` |
| Claude Code plugin | `/plugin marketplace add ethannschwartz/faivelo-mcp` then `/plugin install faivelo@faivelo` |
| claude.ai / Claude Desktop | Settings → Connectors → Add custom connector → paste the URL |
| Codex | `codex mcp add faivelo --url https://faivelo.com/api/mcp` |
| Gemini CLI | `gemini mcp add --transport http faivelo https://faivelo.com/api/mcp` |
| Cursor | `.cursor/mcp.json`: `{ "mcpServers": { "faivelo": { "url": "https://faivelo.com/api/mcp" } } }` |
| VS Code | `.vscode/mcp.json`: `{ "servers": { "faivelo": { "type": "http", "url": "https://faivelo.com/api/mcp" } } }` |
| Windsurf | `~/.codeium/windsurf/mcp_config.json`: `{ "mcpServers": { "faivelo": { "serverUrl": "https://faivelo.com/api/mcp" } } }` |

## Tools

- Reading: `list_messages`, `read_message`, `get_thread`, `search_messages`,
  `search_all_mailboxes`, `list_folders`, `get_attachment`, `get_contacts`
- Sending: `send_message`, `send_batch` (one templated email to many
  recipients in one call; use it instead of looping `send_message`),
  `get_batch_status`, `create_draft`, `update_draft`, `send_draft`,
  `list_scheduled`, `cancel_scheduled`, `get_delivery_status`
- Housekeeping: `flag_message`, `label_message`, `move_message`,
  `restore_message`, `mark_spam`, `mark_all_read`, `delete_message`,
  `empty_trash`
- Account: `list_mailboxes`, `create_mailbox`, `update_mailbox` (set or
  clear the name a mailbox sends as), `get_account_summary`,
  `get_setup_summary` (a shareable summary of what is set up),
  `get_domain_setup` (one domain's DNS records, found or missing, with what to add),
  `list_aliases`, `create_alias`, `delete_alias`
- Domains and DNS: `list_domains`, `list_dns_records`, `create_dns_record`,
  `update_dns_record`, `delete_dns_record` (mail-critical records need
  `force: true`)
- Drive (`drive:read`): `drive_list_files`, `drive_download_file`

Tools declare `readOnlyHint` / `destructiveHint`. Ask the user before sending
mail or deleting anything on their behalf.
