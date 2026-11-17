---
name: cargene
description: Japanese cars and car service in Japan, with sources. Use when the user asks about a Japanese car's generations, who developed it, its sales figures, which aftermarket parts are confirmed to fit it, or where in Japan to get a car inspection (shaken), car wash, wheel alignment or other service.
metadata: {"openclaw":{"requires":{"bins":["curl"]}}}
---

# CarGene

CarGene (https://car-gene.com) is a read-only database of Japanese car genealogy and car service shops in Japan. Every fact carries the source it was copied from. You reach it through its public MCP server, `https://api.car-gene.com/mcp`, with one HTTP request per call. No API key and no session.

## Call a tool

Send every call with the headers below and the `_meta` block as shown. Change only `Mcp-Method`, `Mcp-Name`, `method`, `name` and `arguments`.

List the tools and their input schemas first. The descriptions there are the reference for every argument:

```bash
curl -s https://api.car-gene.com/mcp \
  -H 'Content-Type: application/json' \
  -H 'Accept: application/json, text/event-stream' \
  -H 'MCP-Protocol-Version: 2026-07-28' \
  -H 'Mcp-Method: tools/list' \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/list","params":{"_meta":{"io.modelcontextprotocol/protocolVersion":"2026-07-28","io.modelcontextprotocol/clientCapabilities":{},"io.modelcontextprotocol/clientInfo":{"name":"cargene-clawhub-skill","version":"1.0.0"}}}}'
```

Then call one. For example, find a car by name:

```bash
curl -s https://api.car-gene.com/mcp \
  -H 'Content-Type: application/json' \
  -H 'Accept: application/json, text/event-stream' \
  -H 'MCP-Protocol-Version: 2026-07-28' \
  -H 'Mcp-Method: tools/call' \
  -H 'Mcp-Name: search_vehicles' \
  -d '{"jsonrpc":"2.0","id":2,"method":"tools/call","params":{"name":"search_vehicles","arguments":{"query":"Skyline"},"_meta":{"io.modelcontextprotocol/protocolVersion":"2026-07-28","io.modelcontextprotocol/clientCapabilities":{},"io.modelcontextprotocol/clientInfo":{"name":"cargene-clawhub-skill","version":"1.0.0"}}}}'
```

The answer is JSON in `result.content[0].text`. Names are in Japanese. English names also match in `search_vehicles`.

## Read the answer

- Start from `search_vehicles` and pass its ids to the other tools. Ids are opaque UUIDs. To match against outside data, use `chassis_code`.
- An empty list means CarGene has not researched it yet. It does not mean there is none.
- When you answer the user, quote the source that came with the fact, and link the car-gene.com page when the answer has one.
- Long lists return `next_offset` (or `next_year_from`). Call again with `offset` (or `year_from`) to read on.
