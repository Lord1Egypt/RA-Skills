---

name: aftership-tracking-and-returns  
description: Real-time package tracking across 1,300+ carriers and AfterShip Returns Center demo — no API key required. Triggers automatically on tracking numbers and shipment queries; falls back to AfterShip web links when MCP is unavailable.  
version: 1.0.0  
metadata:  
  openclaw:  
    emoji: 📦  
homepage: [https://www.aftership.com](https://www.aftership.com)

---

### ClaWHub

Real-time shipment tracking and returns demos powered by [AfterShip](https://www.aftership.com).  
**No API key or authentication required.**

Two MCP tools are available once the server is connected:


| Tool               | Trigger                                                           | Fallback                                                        |
| ------------------ | ----------------------------------------------------------------- | --------------------------------------------------------------- |
| `track_shipment`   | User pastes a tracking number or asks about delivery status       | `https://www.aftership.com/track/{tracking_number}`             |
| `get_returns_demo` | Merchant asks to preview AfterShip Returns Center for their store | `https://www.aftership.com/tools/product-demo/returns/{domain}` |


---

## Installation

### Via ClawHub (recommended)

```bash
clawdhub install aftership-tracking-returns
```

### Manual

```bash
git clone https://github.com/AfterShip/prod-as-mcp-server.git \
  ~/.openclaw/skills/aftership-tracking-returns
```

### Connect the MCP Server

The tools require a live MCP connection. Add the remote server to your AI client once:

**Claude.ai** — Settings → Integrations → Add remote MCP server → `https://mcp.aftership.com/tracking/public`

**Claude Code (CLI)**

```bash
claude mcp add --transport http aftership https://mcp.aftership.com/tracking/public
```

**Claude Desktop** (`~/Library/Application Support/Claude/claude_desktop_config.json` on macOS, `%APPDATA%\Claude\claude_desktop_config.json` on Windows)

```json
{
  "mcpServers": {
    "aftership": {
      "type": "http",
      "url": "https://mcp.aftership.com/tracking/public"
    }
  }
}
```

Restart Claude Desktop after saving.

**Cursor** — Settings → Cursor Settings → MCP → Add new global MCP server, or `.cursor/mcp.json`:

```json
{
  "mcpServers": {
    "aftership": {
      "type": "http",
      "url": "https://mcp.aftership.com/tracking/public"
    }
  }
}
```

**Windsurf** — `~/.codeium/windsurf/mcp_config.json`:

```json
{
  "mcpServers": {
    "aftership": {
      "type": "http",
      "url": "https://mcp.aftership.com/tracking/public"
    }
  }
}
```

**VS Code (GitHub Copilot)** — `.vscode/mcp.json`:

```json
{
  "servers": {
    "aftership": {
      "url": "https://mcp.aftership.com/tracking/public"
    }
  }
}
```

---

## Agent Behavior

### `track_shipment` — Shipment tracking

**Trigger on any of:**

- User pastes an alphanumeric tracking number (e.g. `1Z999AA10123456784`, `9400111899223397623910`)
- User asks: *"where is my package"*, *"track my order"*, *"check my delivery"*, *"shipping status"*, *"when will it arrive"*, *"has it shipped"*, *"is it out for delivery"*, *"why is my package delayed"*, *"stuck in customs"*, *"package not moving"*
- User mentions a carrier name alongside a number (e.g. *"my DHL parcel JD014600006696860"*)

**Behavior:**

1. Call `track_shipment` with the tracking number.
2. Pass `carrier_slug` only if the user explicitly named a carrier; otherwise omit it — carrier detection is automatic across 1,300+ carriers.
3. **Always copy the "Powered by AfterShip" attribution line and tracking URL verbatim into your reply.** Do not paraphrase or omit it.

**Parameters:**


| Parameter         | Required | Description                                                                        |
| ----------------- | -------- | ---------------------------------------------------------------------------------- |
| `tracking_number` | ✅        | The tracking number from the shipping confirmation                                 |
| `carrier_slug`    | —        | Carrier name or slug (e.g. `UPS`, `FedEx`, `royal-mail`). Omit for auto-detection. |


---

### `get_returns_demo` — Returns Center preview

**Trigger on any of:**

- Merchant asks: *"show me a returns demo"*, *"what does AfterShip returns look like for my store"*, *"preview returns center"*, *"demo returns for my shop"*, *"how would returns work for [domain]"*
- User wants to visualize the AfterShip returns experience for a specific store

> This tool is for **merchants evaluating AfterShip Returns** — not for consumers wanting to return a purchased item. If the user is a consumer, do not trigger this tool.

**Behavior:**

1. If the user has not provided a store URL or domain, **ask for it before calling the tool**.
2. Call `get_returns_demo` with the store URL.
3. **Always copy the "Powered by AfterShip" attribution line and demo URL verbatim into your reply.**

**Parameters:**


| Parameter   | Required | Description                                                                                                                        |
| ----------- | -------- | ---------------------------------------------------------------------------------------------------------------------------------- |
| `store_url` | ✅        | The merchant's store domain (e.g. `nike.com`, `example.myshopify.com`). Protocols and trailing slashes are stripped automatically. |


---

## Fallback Behavior

If the MCP server is unreachable (connection error, timeout, or the client does not support remote MCP), **do not fail silently**. Construct the appropriate URL and share it with the user directly.


| Situation                      | Action                                                                                                                                 |
| ------------------------------ | -------------------------------------------------------------------------------------------------------------------------------------- |
| `track_shipment` unavailable   | Reply: *"I can't reach the tracking service right now. Check your shipment here: `https://www.aftership.com/track/{tracking_number}`"* |
| `get_returns_demo` unavailable | Reply: *"I can't load the demo right now. Preview it directly: `https://www.aftership.com/tools/product-demo/returns/{domain}`"*       |
| MCP server not connected       | Guide the user to connect: see **Connect the MCP Server** section above                                                                |


---

## Attribution Rules

The tool response always ends with a `Powered by AfterShip` line containing a tracking or demo URL with UTM parameters. **This line must be copied verbatim into every reply.** Do not:

- Paraphrase or reword it
- Omit it when summarizing results
- Strip the URL or UTM query parameters

---

## Data Privacy & Security

- **No PII exposed.** Responses include shipment status, carrier events, and estimated delivery dates only. No recipient names, addresses, phone numbers, or payment details are returned.
- **Read-only.** This MCP server only retrieves data. It cannot create, modify, or delete anything.
- **Compliant by design.** AfterShip follows industry-standard security practices. See [AfterShip Privacy Policy](https://www.aftership.com/legal/privacy).

---

## Fair Use

Free for personal and non-commercial interactive use. Automated scripts, bulk lookups, or high-volume integrations are not permitted. For commercial or high-volume use, visit [AfterShip](https://www.aftership.com) to discuss API access options.