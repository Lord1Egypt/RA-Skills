---
name: connect-to-skilder
description: One-shot instruction to connect this AI agent to Skilder over MCP using the official remote endpoint and OAuth. Paste this whole skill into an agent's chat once. It should act on it immediately, without asking the user anything first.
version: 1.0.2
homepage: https://github.com/skilder-ai/skills
---

You've just been handed this as a one-time instruction. Proceed automatically. Don't
ask the user any clarifying questions first. The endpoint is fixed and already known:

    https://app.skilder.ai/mcp

You don't need a workspace name, a link, or a key to get started.

## Do this now

1. **Register the server.** Add `https://app.skilder.ai/mcp` as a remote Streamable
   HTTP MCP server for yourself, using whatever mechanism you already have:
   - Claude Code: run `claude mcp add skilder-ai --transport http https://app.skilder.ai/mcp`
   - Codex: run `codex mcp add skilder-ai --url https://app.skilder.ai/mcp`
   - Any host where you can edit your own MCP config (`.mcp.json`, Cursor's
     `~/.cursor/mcp.json`, VS Code's `.vscode/mcp.json`,
     `claude_desktop_config.json`, etc.): add this entry, keeping the host's own
     top-level key (`mcpServers` on most hosts, `servers` on VS Code):

         "skilder-ai": {
           "type": "http",
           "url": "https://app.skilder.ai/mcp"
         }
   - If you have no way at all to configure your own MCP servers, say so as a single
     fact and stop there. Don't turn it into a question back to the user.

2. **Trigger the connection.** Call the server right away (e.g. `tools/list`). This
   is expected to redirect through a one-time browser sign-in to Skilder. That's
   the OAuth handshake, and approving it is the only step a human touches. Don't ask
   permission to attempt this; just do it and report what happens.

3. **Confirm and report.** Once connected, list what the server now exposes, and
   tell the user which Roles and Skills are available. Don't wait to be asked.

4. **Only if OAuth genuinely isn't possible** in your environment (no browser
   redirect support at all): say so, then fall back to the key-based config from
   Skilder's Connect page → Advanced. That does require a key from the user, the
   one unavoidable exception to "don't ask."

That's it: one endpoint, no setup questions, act now.
