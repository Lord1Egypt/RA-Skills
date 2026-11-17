---
name: bitsweave
description: Use the BitsWeave MCP server to read shared project context and save durable work for other agents.
---

# BitsWeave

Use the `bitsweave` MCP server before you create local notes or duplicate work.

1. Inspect the available BitsWeave tools.
2. Read the relevant project context before you make a change.
3. Save durable findings, decisions, tasks, and documents in BitsWeave.
4. Keep local files for source artifacts, not shared coordination notes.

The package connects to `https://bitsweave.com/api/mcp` with Streamable HTTP.
Complete the client OAuth flow when the first tool call requests it. Do not ask
the user to paste a token.

If the tools are absent, confirm that the plugin is enabled. Restart the
OpenClaw gateway after a new install.
