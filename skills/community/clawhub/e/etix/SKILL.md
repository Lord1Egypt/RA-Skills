---
name: etix
description: Search Etix events, venues, and performers and pull event/venue details via MCP. Triggers on phrases like "find events on etix", "etix tickets for", "what's playing at <venue> on etix", "etix event details for", "search etix for <artist>", or any request involving Etix events, venues, performers, or showtimes. Requires etix-mcp installed and the ContextMint Bridge extension active with an open etix.com tab (see Setup below).
---

# etix-mcp

MCP server for Etix — natural-language search of events, venues, and performers, plus full event and venue detail. Routes through your signed-in etix.com tab via the ContextMint Bridge browser extension, so Etix's DataDome bot-wall sees a real browser session instead of a Node process. No Etix account is required — this is public event-discovery data.

- **npm:** [npmjs.com/package/etix-mcp](https://www.npmjs.com/package/etix-mcp)
- **Source:** [github.com/chrischall/etix-mcp](https://github.com/chrischall/etix-mcp)

> ⚠️ Etix does not publish a public consumer API, and its consumer site sits behind a DataDome interstitial. This server reads the same `/ticket/api/online/...` endpoints and server-rendered pages that etix.com itself uses, dispatched through your own signed-in browser tab via the ContextMint Bridge extension. Use at your own discretion.

## Setup

### 1. Install etix-mcp

`.mcp.json` (project) or `~/.claude/mcp.json` (global):

```json
{
  "mcpServers": {
    "etix": {
      "command": "npx",
      "args": ["-y", "etix-mcp"]
    }
  }
}
```

### 2. Install ContextMint Bridge (one-time, shared across all fetchproxy-based MCPs)

Download it from [ContextMint Bridge releases](https://github.com/nullnet-app/contextmint-bridge/releases):

- **Chrome:** unzip the Chrome zip, then load it at `chrome://extensions` (Developer mode → Load unpacked → the unzipped folder).
- **Safari:** ships inside the ContextMint app, which has no public download link yet — use Chrome for now.

ContextMint Bridge is the fetchproxy extension under its new name, from the same maintainer ([fetchproxy's README](https://github.com/chrischall/fetchproxy#extension) points to it). Its source is public at [nullnet-app/contextmint-bridge](https://github.com/nullnet-app/contextmint-bridge): build it yourself, or verify a release zip with `shasum -a 256 -c contextmint-bridge-chrome-<version>.zip.sha256` (the `.sha256` file is published beside it).

All fetchproxy MCPs share one extension and one port (`37149`).

### 3. Open etix.com and approve the pairing

Open [etix.com](https://www.etix.com/ticket/) in your browser and let it finish loading (so the DataDome check clears). The first tool call prints a one-time pairing code — approve it in the ContextMint Bridge popup. After that, run `etix_healthcheck` to confirm the bridge is green end-to-end.

## Tools

| Tool | Purpose |
| --- | --- |
| `etix_search` | Search events, venues, and performers by keyword. Each result carries its id + canonical etix.com URL. |
| `etix_get_event` | Full detail for an event/performance by `event_id` — name, date/time, venue (address + coordinates), organizer, price range and individual priced offer levels. |
| `etix_get_venue` | A venue by `venue_id` — name, organizer, address, and its list of upcoming events. |
| `etix_find_location` | Resolve a city or postal code to coordinates (building block for location-based browsing). |
| `etix_healthcheck` | End-to-end bridge check — round-trips `/robots.txt` and reports which hop failed (bridge down vs. extension not connected vs. DataDome challenge on your tab). Call when other tools fail. |

## In context groups

On a host that reads context-group hints (mcp-host's `family` group), every tool except `etix_healthcheck` carries `_meta.mint` with `domain: family`. Etix is public discovery with nothing of yours to list (no account, children or saved venues), so **no tool is canonical and none declares a subject**: a bare "what's on this weekend?" fan-out never calls Etix. `etix_search`, `etix_get_event` and `etix_find_location` are `lookup`; `etix_get_venue` is a non-canonical `whats-on` for a venue the person names.

A compound ask reaches Etix only when it names something to search, e.g. "anything on the family calendar this weekend, and are there tickets left for the jazz show at Middle C?" — the group answers its own canonical reads, then calls `etix_search` → `etix_get_venue` / `etix_get_event` for the named show. Every call rides the ContextMint Bridge, so with no etix.com tab open the group answers that Etix "needs your browser open" rather than an error.

## Acknowledgement of Terms

By using this MCP server, you acknowledge and agree to the following:

**1. This server uses your own etix.com session.** Every request is dispatched through your own browser tab via the ContextMint Bridge extension — your cookies, your TLS, your session.

**2. No public API.** Etix does not offer a public consumer API; this reads the website's own endpoints and pages. Etix may change them at any time.

**3. Use at your own discretion**, consistent with Etix's Terms of Use. This is an unofficial, AI-developed project with no affiliation to Etix.
