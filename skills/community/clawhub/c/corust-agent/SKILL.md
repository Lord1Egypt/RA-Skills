---
name: corust_agent
description: "Install, configure, and use Corust Agent (corust-agent-acp) — an ACP-compatible coding agent. Use when: the user wants to install, configure, set up, or use corust, corust-agent, or corust-agent-acp. NOT for: general ACP troubleshooting unrelated to Corust, or other agent harnesses (claude, codex, gemini)."
metadata:
  {
    "openclaw":
      {
        "emoji": "🦀",
        "requires": { "bins": ["tar", "curl"] },
      },
  }
---

# Corust Agent Skill

Install and configure **corust-agent-acp**, an ACP-compatible coding agent by Corust AI.

## When to Use

✅ **USE this skill when:**

- User wants to install or update corust-agent-acp
- User wants to configure corust / corust-agent in OpenClaw
- User says "install corust", "configure corust-agent", "use corust-agent-acp", or similar
- User wants to run corust-agent via ACP on Discord or other channels

❌ **DON'T use this skill when:**

- User is asking about other ACP agents (claude, codex, gemini)
- User is troubleshooting general ACP/acpx issues unrelated to Corust

## Setup Steps

Follow these steps **in order** to install and configure corust-agent-acp.

### Step 1: Download and Install the Binary

1. Detect the current platform and architecture:
   - macOS ARM (Apple Silicon / M1+): `darwin-arm64`
   - macOS Intel: `darwin-amd64`
   - Linux x86_64: `linux-amd64`
   - Linux ARM64: `linux-arm64`

2. Ask the user where they want to install the binary. Default: `$HOME/corust`.

3. Download the latest release from GitHub:

   ```bash
   # Example for macOS Apple Silicon
   mkdir -p "$HOME/corust"
   curl -fSL "https://github.com/Corust-ai/corust-agent-release/releases/latest/download/agent-darwin-arm64.tar.gz" \
     -o /tmp/corust-agent.tar.gz
   tar -xzf /tmp/corust-agent.tar.gz -C "$HOME/corust"
   chmod +x "$HOME/corust/corust-agent-acp"
   rm /tmp/corust-agent.tar.gz
   ```

   Adjust the archive name based on detected platform:
   - `agent-darwin-arm64.tar.gz` — macOS Apple Silicon
   - `agent-darwin-amd64.tar.gz` — macOS Intel
   - `agent-linux-amd64.tar.gz` — Linux x86_64
   - `agent-linux-arm64.tar.gz` — Linux ARM64

4. Verify the binary works:

   ```bash
   "$HOME/corust/corust-agent-acp" --version
   ```

### Step 2: Configure acpx

Write the following to `~/.acpx/config.json` (create the file and directory if they don't exist).
Replace `$HOME` with the actual resolved home directory path.

```json
{
  "agents": {
    "corust-agent-acp": { "command": "$HOME/corust/corust-agent-acp" }
  }
}
```

**Important:** If `~/.acpx/config.json` already exists and contains other agent entries, merge the
`corust-agent-acp` entry into the existing `agents` object rather than overwriting the file.

```bash
mkdir -p ~/.acpx
# Read existing config, merge, and write back
```

### Step 3: Configure OpenClaw

Add the following configuration to `~/.openclaw/openclaw.json`. Use `openclaw config set` commands
or edit the file directly. **Merge into existing config — do not overwrite unrelated sections.**

**ACP configuration:**

```json
{
  "acp": {
    "enabled": true,
    "dispatch": {
      "enabled": true
    },
    "backend": "acpx",
    "defaultAgent": "corust-agent-acp",
    "allowedAgents": [
      "corust-agent-acp"
    ],
    "maxConcurrentSessions": 8,
    "stream": {
      "coalesceIdleMs": 300,
      "maxChunkChars": 1200
    },
    "runtime": {
      "ttlMinutes": 120
    }
  }
}
```

**ACPX plugin configuration:**

```json
{
  "plugins": {
    "entries": {
      "acpx": {
        "enabled": true,
        "config": {
          "permissionMode": "approve-all",
          "nonInteractivePermissions": "deny"
        }
      }
    }
  }
}
```

### Step 4: Tell the User How to Configure Discord

After completing the above steps, instruct the user on Discord setup.
**Do NOT run these commands automatically** — only tell the user what to do.

Provide the following instructions:

---

#### Discord Configuration

1. **Enable ACP thread spawning and open DM access:**

   ```bash
   openclaw config set channels.discord.threadBindings.spawnAcpSessions true
   openclaw config set channels.discord.allowFrom '["*"]'
   ```

2. **Enable thread creation permissions in Discord:**

   Go to your Discord server → channel settings → Permissions, and ensure the bot role has:
   - **Create Public Threads** — enabled
   - **Create Private Threads** — enabled
   - **Send Messages in Threads** — enabled

3. **Start using Corust Agent:**

   In any text channel, mention the bot and say:

   > @Bot run corust

   The bot will spawn a corust-agent-acp session in a new thread and begin working on your task.

---

## Troubleshooting

- **"acpx command not found"**: Ensure the ACPX plugin is enabled and the gateway has been restarted after configuration changes.
- **Agent binary not found**: Verify the path in `~/.acpx/config.json` points to the correct binary location and the file is executable (`chmod +x`).
- **Discord "Not authorized"**: Run `openclaw config set channels.discord.allowFrom '["*"]'` and restart the gateway.
- **Network issues (proxy)**: If Discord connections fail, set `openclaw config set channels.discord.proxy "http://127.0.0.1:<port>"` with your local proxy port. Also consider enabling TUN mode on your proxy client for full coverage.
