# Agent MCP Installation Reference

**Status:** implementation contract
**Retrieved:** 2026-07-28

`api-to-typemcp` produces local stdio MCP projects. Project-only generation is the default. Only after contained generated-project verification may the skill offer agent installation. Detection is read-only; installation requires selected targets, a displayed secret-free plan, and a separate final confirmation.

## Global safety contract

- The installer never reads `.env`, resolves credentials, or writes secret values into an agent config, plan, log, backup, or portable export. It displays environment-variable names only.
- `generate` never scans or edits agent configuration.
- Unknown, malformed, symlinked, fingerprint-changed, or unsupported targets fail closed.
- Portable export does not modify an agent configuration. It writes a secret-free standard `mcpServers` snippet under generated-project `agent-install/`.
- Per-target failure never implies another target is installed; a changed target has a same-directory backup and target-local rollback.
- Protected writes remain fail-closed under `TYPE_MCP_ALLOW_PROTECTED_OPERATIONS`.

## hermes

**Official reference:** https://hermes-agent.nousresearch.com/docs/user-guide/features/mcp
**Retrieved:** 2026-07-29

Native registration uses only the documented `hermes mcp add <name> --command node --args <absolute-entry>` CLI path. The reviewed plan records the CLI-managed candidate path for operator visibility but the installer never reads or edits it directly. After registration, it runs `hermes mcp test <name>`; any non-zero result triggers `hermes mcp remove <name>` as compensating rollback. Hermes CLI currently exposes no cwd flag, so the generated absolute `dist/index.js` entrypoint is used and the plan reports the canonical project cwd for review. Environment variable values are never read or passed; users provide required values through their Hermes execution environment.

## claude-code

**Official reference:** https://docs.anthropic.com/en/docs/claude-code/mcp
**Retrieved:** 2026-07-29

Native registration uses the documented stdio form `claude mcp add --transport stdio <name> -- node <absolute-entry>`, where `--` separates Claude Code options from the server command. The installer never reads or edits Claude settings directly. It verifies registration using `claude mcp list` and requires the named server in successful output; a failed or absent discovery triggers `claude mcp remove <name>` as compensating rollback. Claude Code’s documented add form has no cwd argument, so the generated absolute entrypoint is used and the canonical project cwd remains plan-visible only. Environment variable values are never read or passed; users provide required values through their Claude Code execution environment.

## codex

**Official reference:** https://developers.openai.com/codex/cli/reference
**Retrieved:** 2026-07-28

Preferred path: `codex mcp add`, `codex mcp get`, and `codex mcp list`. Native entries use TOML `mcp_servers`. Without a safe CLI path, append only a missing validated table; reject existing target tables or syntax that cannot be preserved.

## cursor

**Official reference:** https://cursor.com/docs/mcp
**Retrieved:** 2026-07-28

Cursor uses a selected user/workspace JSON `mcpServers` object in `mcp.json`. Direct mutation is only for valid non-symlink JSON with preservation guarantees; otherwise return portable export.

**Verification:** reread/schema-check the exact target, then reload Cursor MCP configuration or restart and have the user confirm the named server appears. Do not call an upstream API tool.

## vscode-copilot

**Official reference:** https://code.visualstudio.com/docs/agent-customization/mcp-servers
**Retrieved:** 2026-07-28

VS Code/Copilot supports explicit workspace `.vscode/mcp.json` or user-profile MCP scope. Workspace credentials must not be hardcoded. Only valid non-symlink JSON with `mcpServers` can be changed.

**Verification:** reread/schema-check the target, then use the MCP view/refresh flow and have the user confirm the server appears. Do not invoke a generated API tool.

## gemini-cli

**Official reference:** https://geminicli.com/docs/tools/mcp-server/
**Retrieved:** 2026-07-28

Gemini CLI uses top-level `mcpServers` in explicit project or global `settings.json`. The plan records scope and no host/project secret values are read.

**Verification:** reread/schema-check `settings.json`, restart Gemini CLI, and use its MCP inspection flow to confirm local discovery. Failed discovery rolls back this target only.

## opencode

**Official reference:** https://opencode.ai/docs/mcp-servers/
**Retrieved:** 2026-07-28

OpenCode supports local and remote MCP servers. `~/.config/opencode/opencode.json` is a **Linux/XDG example**, not a universal path. Native local servers are under `mcp.servers` with a command array. Prefer documented `opencode mcp add`; otherwise mutate only valid non-symlink JSON and fail closed if format differs.

**Verification:** use OpenCode MCP server-management inspection after registration plus reread/schema-check of direct JSON writes. Confirm discovery without calling upstream tools.

## Portable entry shape

```json
{
  "mcpServers": {
    "example-mcp": {
      "command": "node",
      "args": ["/absolute/generated-project/dist/index.js"],
      "cwd": "/absolute/generated-project"
    }
  }
}
```

Required environment variables are names only; users provide values outside generated artifacts and agent configuration.
