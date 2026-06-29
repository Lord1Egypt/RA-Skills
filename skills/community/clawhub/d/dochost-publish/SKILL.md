---
name: dochost-publish
description: |
  Publish Markdown or HTML to a clean, shareable dochost.io link and hand the URL
  back to the user. Use when the user says "publish this", "share this as a link",
  "put this on the web", "make a page from this", "turn this into a link", or in
  Chinese "发布", "分享成链接", "做个网页", "生成链接" — for any document, report,
  README, or HTML the assistant produced. Works on any agent that can make an HTTP
  request (OpenClaw, Hermes, Claude, Cursor, ChatGPT, or a plain shell). Returns a
  public dochost.io/d/... URL.
---

# Publish to dochost

Turn Markdown or HTML into a hosted web page at its own URL, in one call. The page
renders live (Markdown **and** HTML), so the recipient sees a real page, not a raw
`.md` blob. Free links last 7 days; permanent links, passwords, custom slugs and
branding removal follow the account's plan.

## One-time setup

The agent publishes **as a dochost user**, authenticated with an API key.

1. Sign in at <https://dochost.io>, open **Settings → API keys**, create a key.
2. Make it available to the agent as the environment variable `DOCHOST_API_KEY`.

That's the whole setup. Entitlements (link lifetime, password, custom slug,
branding) come from the account that owns the key, never from tool input.

## How to publish

Send one JSON-RPC `tools/call` to the dochost MCP endpoint with the key as a
Bearer token. No handshake or `initialize` call is needed (the server is stateless).

```bash
curl -sS -X POST https://dochost.io/api/mcp \
  -H "Authorization: Bearer $DOCHOST_API_KEY" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "id": 1,
    "method": "tools/call",
    "params": {
      "name": "publish",
      "arguments": {
        "body": "# My report\n\nHello world.",
        "format": "markdown"
      }
    }
  }'
```

### Reading the result

The response is JSON-RPC. The tool payload is a JSON string inside
`result.content[0].text`. Parse it and read `url`:

```bash
# ...pipe the curl output through jq:
| jq -r '.result.content[0].text | fromjson | .url'
```

A success payload looks like:

```json
{ "ok": true, "slug": "q3-report", "url": "https://dochost.io/d/q3-report",
  "editToken": "…", "expiresAt": "2026-06-22T12:00:00.000Z" }
```

**Give the user the `url`.** Mention `expiresAt` if it is set (free links expire;
`null` means permanent). Keep `editToken` only if the user may want to edit later.

## `publish` arguments

| Argument | Type | Notes |
|---|---|---|
| `body` | string (**required**) | The Markdown or HTML to publish. |
| `format` | `"markdown"` \| `"html"` | Auto-detected when omitted. Set it if the content is ambiguous. |
| `public` | boolean | List on dochost Explore. Default `false` (unlisted). |
| `customSlug` | string · paid | Choose the link path instead of a random slug. |
| `password` | string · paid | Gate the page behind a password. |
| `noBranding` | boolean · paid | Hide the dochost footer badge. |

## List previously published pages

```bash
curl -sS -X POST https://dochost.io/api/mcp \
  -H "Authorization: Bearer $DOCHOST_API_KEY" \
  -H "Content-Type: application/json" -H "Accept: application/json" \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/call",
       "params":{"name":"list_my_pages","arguments":{"limit":10}}}'
```

Returns compact records (slug, url, title, createdAt, expiresAt) — never page bodies.

## Errors the user should hear about

The payload has `ok: false` and a plain-English `message` on failure. Common cases:

- `RATE_LIMITED` — too many publishes; the message says how long to wait.
- Quota / size limits — free plan caps page count and document size; the message
  tells the user to delete a page or upgrade.
- Blocked URL — the content contained an unsafe link and was not published.
- Invalid / taken `customSlug` — pick a different slug (lowercase, numbers, hyphens).

Relay the `message` verbatim; it is written for end users.

## Notes

- Never put secrets, tokens, or private keys in `body` — published pages are public
  URLs (a password only gates the rendered page, not the fact a URL exists).
- Anonymous publishing is disabled by design; a valid key is required.
- Native MCP clients can instead add the server as a tool — see the repo's
  `clients/` guides. This skill uses plain HTTP so it works even where MCP isn't wired.
