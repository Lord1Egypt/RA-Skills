# Installation — Cloudways MCP Server

This skill targets the **official Cloudways (Remote) MCP** — a Cloudways-hosted MCP at `https://mcp.cloudways.com/mcp/` that you connect to directly, without self-hosting.

> **Source of truth:** [How to Use Cloudways MCP Server for AI-Based Server Management](https://support.cloudways.com/en/articles/14654372-how-to-use-cloudways-mcp-server-for-ai-based-server-management). The endpoint, headers, and steps below are from that article; if Cloudways changes them, the article wins.

**Prerequisites**

- A valid Cloudways account with API access.
- Your Cloudways **email** + **API key**.
- **Node.js v18+** (only for the Claude Desktop path, which uses the `mcp-remote` bridge). Claude Code connects over native HTTP and does not need it.

---

## Step 1 — Generate API credentials

1. Log in to [platform.cloudways.com](https://platform.cloudways.com).
2. Open **API Integration** (bottom-left of the platform).
3. Click **Generate API Key** (or copy an existing key).
4. Copy your **account email** and **API key**.

> The API key grants **everything** the account can do in the UI. Treat it like a password — never commit it or print it in responses.

**Required headers** (every request; header names are case-sensitive):

| Header | Value |
|--------|-------|
| `X-CW-Email` | your Cloudways account email |
| `X-CW-Api-Key` | your Cloudways API key |
| `X-Mcp-Host` | the client you connect from (`claude-code`, `claude-desktop`, …) |

---

## Step 2 — Connect Claude to the MCP

### Claude Code (native HTTP — recommended)

```bash
claude mcp add --transport http \
  --header "X-CW-Email: <your-cloudways-email>" \
  --header "X-CW-Api-Key: <your-cloudways-api-key>" \
  --header "X-Mcp-Host: claude-code" \
  -s user \
  cloudways https://mcp.cloudways.com/mcp/
```

`-s user` stores it at the user level so it persists across projects. Verify with `claude mcp list`; remove later with `claude mcp remove cloudways`.

### Claude Desktop (via `mcp-remote` bridge — needs Node v18+)

Claude Desktop does not natively support remote HTTP MCP servers, so it uses the `mcp-remote` Node bridge. Config file:

- **macOS:** `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Windows:** `%APPDATA%\Claude\claude_desktop_config.json`

```json
{
  "mcpServers": {
    "cloudways": {
      "command": "npx",
      "args": [
        "mcp-remote",
        "https://mcp.cloudways.com/mcp/",
        "--header", "X-CW-Email:<your-cloudways-email>",
        "--header", "X-CW-Api-Key:<your-cloudways-api-key>",
        "--header", "X-Mcp-Host:claude-desktop"
      ]
    }
  }
}
```

> **No spaces around the colon** in `--header` values for the bridge: use `X-CW-Email:user@example.com`, not `X-CW-Email: user@example.com`. After saving, **fully quit** Claude Desktop (Cmd-Q / tray → Quit — closing the window is not enough) and reopen.

> Keep real credentials out of version control. For Claude Code, prefer the `claude mcp add` command above (stored in your user config) or a git-ignored `.mcp.json`. See `.mcp.json.example` in the repo root for the per-account shape. Header names are case-sensitive.

---

## Multi-account configuration — multiple Cloudways accounts

Each Cloudways account is a **separate** MCP connection with its own credentials, so it appears under its own prefix (`mcp__cloudways-clientA__*`). Give each a descriptive, client-based name — that name becomes the tool prefix. Same endpoint for all; only the `X-CW-Email` / `X-CW-Api-Key` differ.

```bash
# one `claude mcp add` per account, with that account's credentials:
claude mcp add --transport http \
  --header "X-CW-Email: clientA@example.com" \
  --header "X-CW-Api-Key: <clientA-api-key>" \
  --header "X-Mcp-Host: claude-code" \
  -s user cloudways-clientA https://mcp.cloudways.com/mcp/
```

(See `.mcp.json.example` for the JSON form across multiple accounts.)

### Safety rules for multi-account (mandatory)

- **Consistent names:** uniform `cloudways-<client>` prefix so Claude (and you) immediately recognize which account each tool belongs to.
- **Separate secrets:** don't keep all the keys in one place. Prefer a secrets manager (a vault project per client) over plain config files.
- **Don't mix:** never reuse one API key across accounts, and never take a server/app ID from one account against another's connection.
- **No granular access:** the API key has full account access and there is **no per-tool permission control** at the MCP layer — scope who holds each key accordingly.
- **Runtime:** account identification, cross-account search, and per-account write-confirmations are documented in `SKILL.md` → **Multi-account**.

---

## Step 3 — Verify the connection

In Claude, ask: **"Show me all my Cloudways servers"** → calls `server_list` and returns your servers (name, status, provider, region, IP). That round-trip confirms the endpoint + credentials.

(There is no `ping` / `customer_info` tool on the official MCP — `server_list` is the liveness + auth check. Identify which account you're on by the connection prefix.)

| Symptom | Meaning | Fix |
|---------|---------|-----|
| Connection failed / red indicator | wrong URL | endpoint must be exactly `https://mcp.cloudways.com/mcp/` (trailing slash) |
| `401 Unauthorized` | bad credentials | re-check email + API key (case-sensitive headers) from API Integration |
| No `mcp__cloudways*__*` tools | not connected / stale cache | restart the client (see "Tools not appearing" below) |
| Timeout | transient network | retry after a moment |
| `mcp-remote not found` (Desktop) | Node missing | install Node.js v18+, ensure `npx` is on PATH |

To test credentials directly against the public Cloudways API (independent of MCP):

```bash
curl -X POST "https://api.cloudways.com/api/v1/oauth/access_token" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "email=YOUR_EMAIL&api_key=YOUR_API_KEY"
```

API reference: <https://developers.cloudways.com/>

---

## Tools not appearing / after an update

MCP clients **cache the tool list** on first connect. If new tools don't show up, or the agent says a tool doesn't exist:

- **Quickest:** in the client's MCP server settings, toggle `cloudways` off then on.
- **If no toggle:** **fully quit** the client (Cmd-Q on macOS / File → Exit / tray → Quit — closing the window is not enough) and reopen.

Then re-test with "Show me all my Cloudways projects" (`project_list`).

---

## Notes

- This skill does **not** cover self-hosting an MCP server — the official hosted MCP is the supported path.
- Tool names throughout this skill match the official article's catalog (see `tools-catalog.md`). The **live** `mcp__cloudways*__*` tools remain the source of truth if Cloudways adds or renames any.
