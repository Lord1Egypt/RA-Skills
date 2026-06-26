---
title: "Integrations"
source:
  - https://docs.github.com/en/copilot/reference/copilot-cli-reference/acp-server
  - https://docs.github.com/en/copilot/how-tos/copilot-cli/connecting-vs-code
category: reference
---

VS Code integration and ACP (Agent Client Protocol) server for IDE and tool integration.

## VS Code Integration

### Auto-Connect

CLI auto-connects to matching VS Code workspace on startup. Shows "Visual Studio Code connected" on success. Works from any terminal (integrated or external).

**Codespaces limitation:** local CLI cannot connect to remote codespace — run CLI inside codespace terminal.

### `/ide` Command

View connection status, connect to different workspace, disconnect. Toggle settings:
- **Auto-connect to matching IDE workspace**
- **Open file edit diffs in IDE**

### Features

**Selection as context:** CLI receives VS Code editor selection in real time. Selection indicator appears below the prompt, aligned right, updating as you select different code. Select code, then prompt `Debug this`.

**Diff view:** File edits appear as side-by-side diffs in VS Code. Accept (checkmark) or reject (X). Not shown when `--allow-all` is active.

**Live diagnostics:** Copilot accesses real-time errors/warnings from VS Code.

**Session sidebar:** Copilot Chat sidebar > Sessions icon. Lists recent sessions, shows transcripts, allows resuming.

**Unread indicator:** A dot icon and unread count appear next to the Chat icon in the VS Code title bar when CLI sessions haven't been viewed. Click to filter unread sessions; click again to clear filter.

**Resume sessions:** Right-click session > "Resume in Terminal" — continues in VS Code integrated terminal with full context.

## ACP Server (Preview)

The Agent Client Protocol standardizes client-agent communication. Copilot CLI can run as an ACP server for IDE integration, CI/CD, custom frontends, and multi-agent systems.

### Server Modes

```bash
copilot --acp --stdio    # stdio (recommended for IDE integration)
copilot --acp --port 3000  # TCP
```

### Client Integration (TypeScript)

```typescript
import * as acp from "@agentclientprotocol/sdk";
import { spawn } from "node:child_process";
import { Readable, Writable } from "node:stream";

const proc = spawn("copilot", ["--acp", "--stdio"], {
  stdio: ["pipe", "pipe", "inherit"],
});

const output = Writable.toWeb(proc.stdin) as WritableStream<Uint8Array>;
const input = Readable.toWeb(proc.stdout) as ReadableStream<Uint8Array>;
const stream = acp.ndJsonStream(output, input);

const client: acp.Client = {
  async requestPermission(params) {
    return { outcome: { outcome: "cancelled" } };
  },
  async sessionUpdate(params) {
    const update = params.update;
    if (update.sessionUpdate === "agent_message_chunk" && update.content.type === "text") {
      process.stdout.write(update.content.text);
    }
  },
};

const connection = new acp.ClientSideConnection((_agent) => client, stream);
await connection.initialize({ protocolVersion: acp.PROTOCOL_VERSION, clientCapabilities: {} });
const session = await connection.newSession({ cwd: process.cwd(), mcpServers: [] });
await connection.prompt({
  sessionId: session.sessionId,
  prompt: [{ type: "text", text: "Hello ACP Server!" }],
});
```

Key steps: spawn process → NDJSON stream → implement `Client` interface → initialize → create session → send prompts.
