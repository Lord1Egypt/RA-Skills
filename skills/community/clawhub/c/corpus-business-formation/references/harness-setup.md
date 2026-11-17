# Connecting Corpus — exact config per harness

Endpoint: `https://corpuslaw.us/api/mcp` — Streamable HTTP, no OAuth, works anonymously.

## The trap

Four clients use four **mutually incompatible** spellings of the same thing. Copying one
config into another silently fails. Verified against each vendor's current docs, 2026-08-20.

| Harness | Wrapper key | `type` value |
|---|---|---|
| Claude Code | `mcpServers` | `"http"` — a `url` with **no** `type` is a hard error |
| Cursor | `mcpServers` | **omit `type` entirely** |
| Cline | `mcpServers` | `"streamableHttp"` — camelCase |
| VS Code / Copilot | **`servers`** | `"http"` |

**Never configure SSE.** `GET /api/mcp` returns 405 — there is no SSE endpoint. Any client
set to `--transport sse` or `"type": "sse"` fails outright.

## Commands

```bash
# Claude Code   (flag is --transport http; "streamable-http" is JSON-only)
claude mcp add --transport http corpus https://corpuslaw.us/api/mcp

# OpenAI Codex  (experimental_use_rmcp_client is NO LONGER required)
codex mcp add corpus --url https://corpuslaw.us/api/mcp

# Hermes        (interactive; answer "no" when asked if it needs auth)
hermes mcp add corpus --url "https://corpuslaw.us/api/mcp"
hermes mcp test corpus
```

## Config files

```jsonc
// Claude Code — .mcp.json
{ "mcpServers": { "corpus": { "type": "http", "url": "https://corpuslaw.us/api/mcp" } } }

// Cursor — .cursor/mcp.json     (NO "type")
{ "mcpServers": { "corpus": { "url": "https://corpuslaw.us/api/mcp" } } }

// Cline                          (camelCase "streamableHttp")
{ "mcpServers": { "corpus": { "type": "streamableHttp", "url": "https://corpuslaw.us/api/mcp" } } }

// VS Code / Copilot — .vscode/mcp.json   ("servers", not "mcpServers")
{ "servers": { "corpus": { "type": "http", "url": "https://corpuslaw.us/api/mcp" } } }
```

```toml
# OpenAI Codex — ~/.codex/config.toml
[mcp_servers.corpus]
url = "https://corpuslaw.us/api/mcp"
```

```yaml
# Hermes — ~/.hermes/config.yaml
mcp_servers:
  corpus:
    url: "https://corpuslaw.us/api/mcp"
```

## Claude Desktop / claude.ai

Settings → Connectors → Add custom connector → paste the URL → Add. Leave the OAuth fields
blank. Works on all plans; Free is limited to one custom connector. This does **not** go in
`claude_desktop_config.json`, which is for local stdio servers only.

## Auth

None required. For higher research limits add a header — free keys are self-serve and
instant at https://corpuslaw.us/settings. In Hermes, pass `--auth header` and paste
the key when prompted (do not put it in `mcp.json`):

```bash
hermes mcp add corpus --url "https://corpuslaw.us/api/mcp" --auth header
```

Other clients set:

```json
"headers": { "Authorization": "Bearer cp_..." }
```
