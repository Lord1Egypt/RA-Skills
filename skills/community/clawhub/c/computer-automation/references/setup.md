# Connecting AIVane to an AI client

Read this only when the AIVane MCP tools are missing (see "Check the connection first" in SKILL.md). After setup, ask the user to restart or reload the client.

## Cloud server

Address: `https://app.aivane.net/mcp` (Streamable HTTP, OAuth sign-in, free
account). No token is needed for clients that can sign in.

Claude Code:

```bash
claude mcp add --transport http aivane https://app.aivane.net/mcp
```

Then run `/mcp`, select `aivane` and authenticate in the browser.

Codex (CLI):

```bash
codex mcp add aivane --url https://app.aivane.net/mcp
codex mcp login aivane
```

or in `~/.codex/config.toml`:

```toml
[mcp_servers.aivane]
url = "https://app.aivane.net/mcp"
```

Cursor (`~/.cursor/mcp.json`), then Customize > MCPs > aivane > sign in:

```json
{
  "mcpServers": {
    "aivane": { "url": "https://app.aivane.net/mcp" }
  }
}
```

Hermes Agent (`~/.hermes/config.yaml`), then `hermes mcp login aivane`:

```yaml
mcp_servers:
  aivane:
    url: "https://app.aivane.net/mcp"
    auth: oauth
```

OpenClaw:

```bash
openclaw mcp add aivane --url https://app.aivane.net/mcp --transport streamable-http
openclaw mcp login aivane
```

Claude (claude.ai, Claude Desktop), ChatGPT and VS Code connect from their own
connector or MCP settings with the same address. Other clients: add a remote
HTTP MCP server with that URL. Clients that cannot sign in can use an access
token the user creates in AIVane under Settings > AI tools; the user pastes it
into their client config. Never ask for the token in chat. Current
instructions: https://aivane.net/docs/ai-tools/

## Local desktop server (Windows)

1. Install AIVane from https://aivane.net/download (the Microsoft Store
   edition has no connection command).
2. In AIVane open Settings > AI tools (MCP) and turn on
   "Allow AI tools to use AIVane".
3. Under "Automations AI tools can use", choose "Expose to AI tools" for each
   automation the agent may run, ideally with a short description.
4. Under "Connect an AI tool", copy the setup for the client (Claude Code
   command, Codex `~/.codex/config.toml` snippet, Cursor `mcp.json` snippet;
   Claude Desktop with the latest desktop app) into the client. It starts
   AIVane's local helper; do not hand-write that command.

Every plan, including Free, can use the local server. Runs use the user's own
computer and the agent's own AI usage.
