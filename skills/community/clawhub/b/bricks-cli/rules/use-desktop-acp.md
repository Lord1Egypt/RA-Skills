# Use Desktop ACP

Connect to the BRICKS Project Desktop agent via ACP (Agent Client Protocol) for headless prompting, session management, and multi-agent orchestration.

**Prerequisites:**

- BRICKS Project Desktop is running ([docs](https://docs.bricks.tools/project))
- ACP is enabled in the app: Settings > Agent > Enable ACP
- `@fugood/bricks-cli` is installed (`bun add -g @fugood/bricks-cli`)
- The current directory is a BRICKS project (has `application.json`)

## 1. Verify Connection

```bash
# Check the bridge can reach BRICKS Project Desktop
echo '{"jsonrpc":"2.0","id":0,"method":"initialize","params":{"protocolVersion":1,"clientCapabilities":{},"clientInfo":{"name":"test"}}}' \
  | bricks desktop-acp-bridge
```

If you get `Cannot connect to BRICKS Project Desktop`, make sure the app is running and ACP is enabled.

## 2. Use with acpx

[acpx](https://github.com/openclaw/acpx) is a headless CLI client for the Agent Client Protocol. It manages sessions, queues prompts, and streams agent output.

```bash
# Install acpx
npm install -g acpx

# Create a session in the current project
acpx --agent 'bricks desktop-acp-bridge' sessions new

# Send a prompt
acpx --agent 'bricks desktop-acp-bridge' "list all files and summarize the project"

# Auto-approve all tool calls
acpx --agent 'bricks desktop-acp-bridge' --approve-all "fix the linting errors"

# Quiet mode (final output only)
acpx --agent 'bricks desktop-acp-bridge' --format quiet "what does this project do?"

# JSON output for automation
acpx --agent 'bricks desktop-acp-bridge' --format json "run the tests"
```

### Persistent acpx config

Add to `~/.acpx/config.json` to avoid repeating `--agent`:

```json
{
  "agents": {
    "bricks": {
      "command": "bricks desktop-acp-bridge"
    }
  }
}
```

Then use as:

```bash
acpx bricks sessions new
acpx bricks "refactor the auth module"
acpx bricks sessions list
acpx bricks sessions close
```

## 3. Use with OpenClaw

[OpenClaw](https://openclaw.ai) supports ACP via acpx. With the `bricks` agent configured in `~/.acpx/config.json` (see above), OpenClaw can connect to the BRICKS Project Desktop agent for multi-agent orchestration.

## Key Details

- **Sessions are shared** — conversations created via ACP appear in BRICKS Project Desktop's GUI and vice versa
- **Settings are shared** — default model and provider config come from the app's settings (credentials are not exposed to the ACP client)
- **MCP is shared** — `.mcp.json` tools configured in the project are available to the ACP agent
- **Project scoped** — the agent operates in the `cwd` passed by the ACP client; the directory must contain `application.json`
- **Auto-approve** — bash commands run without approval in ACP mode (headless); use acpx `--deny-all` to override

## Security Considerations

- **Prefer `--deny-all` over `--approve-all`:** The `--approve-all` flag permits the agent to run arbitrary bash commands in the project directory without confirmation. Use this only for trusted, well-scoped prompts. For exploratory or untrusted prompts, use `--deny-all` or omit both flags to get interactive approval.
- **Persistent config creates lasting access:** Writing `~/.acpx/config.json` means any process invoking `acpx bricks` can start an ACP session with project file access. Remove the config when not actively using ACP, especially on shared machines.
- **Disable ACP when idle:** Turn off "Enable ACP" in BRICKS Project Desktop Settings when not actively bridging to reduce the attack surface of the local Unix socket.
