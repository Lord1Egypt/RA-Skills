# TypeScript SDK API Reference

## Installation
```bash
npm install @anthropic-ai/claude-agent-sdk
```

The SDK bundles the local Claude Code binary as an optional dependency. If skipped, set `pathToClaudeCodeExecutable`.

## query() Function

```typescript
function query({ prompt, options }: {
    prompt: string | AsyncIterable<SDKUserMessage>;
    options?: Options;
}): Query;  // AsyncGenerator<SDKMessage, void>
```

## startup()

Pre-warms the CLI subprocess to avoid cold start latency:

```typescript
const warm = await startup({ options: { maxTurns: 3 } });
for await (const msg of warm.query("What files are here?")) { ... }
```

## tool() and createSdkMcpServer()

```typescript
import { z } from "zod";
const searchTool = tool("search", "Search the web",
    { query: z.string() },
    async ({ query }) => ({ content: [{ type: "text", text: `Results: ${query}` }] })
);
const server = createSdkMcpServer({ name: "my-server", tools: [searchTool] });
```

## Session Management

- `listSessions({ dir?, limit?, includeWorktrees? })` → `Promise<SDKSessionInfo[]>`
- `getSessionMessages(sessionId, { dir?, limit?, offset? })` → `Promise<SessionMessage[]>`
- `getSessionInfo(sessionId, { dir? })` → `Promise<SDKSessionInfo | undefined>`
- `renameSession(sessionId, title, { dir? })` → `Promise<void>`
- `tagSession(sessionId, tag, { dir? })` → `Promise<void>`
- `resolveSettings({ cwd?, settingSources?, ... })` → `Promise<ResolvedSettings>` (alpha)

## Options Key Fields

| Field | Type | Description |
|-------|------|-------------|
| `allowedTools` | `string[]` | Auto-approved tools |
| `disallowedTools` | `string[]` | Blocked tools |
| `permissionMode` | `PermissionMode` | default/acceptEdits/plan/dontAsk/bypassPermissions |
| `systemPrompt` | `string` | Custom system prompt |
| `maxTurns` | `number` | Maximum turns |
| `maxBudgetUsd` | `number` | Maximum budget (USD) |
| `mcpServers` | `Record<string, McpServerConfig>` | MCP servers |
| `hooks` | `Record<string, HookMatcher[]>` | Hook configuration |
| `agents` | `Record<string, AgentDefinition>` | Sub-agents |
| `canUseTool` | `CanUseTool` | Tool approval callback |
| `includePartialMessages` | `boolean` | Enable streaming output |
| `settingSources` | `SettingSource[]` | user/project/local |
| `cwd` | `string` | Working directory |
| `env` | `Record<string, string>` | Environment variables |
| `model` | `string` | Model selection |
| `continue` | `boolean` | Continue most recent session |
| `resume` | `string` | Resume session by ID |
| `forkSession` | `boolean` | Fork the session |
| `persistSession` | `boolean` | Persist session to disk |
| `abortController` | `AbortController` | Cancellation control |
| `effort` | `EffortLevel` | low/medium/high/xhigh/max |
| `additionalDirectories` | `string[]` | Additional accessible directories |
| `pathToClaudeCodeExecutable` | `string` | CLI binary path |

## Message Types

| type field | Description |
|------------|-------------|
| `"system"` | Session event (subtype: init) |
| `"assistant"` | Claude response (message.message.content) |
| `"user"` | Tool results |
| `"result"` | Final result (subtype, result, total_cost_usd, session_id) |
| `"stream_event"` | Stream event |
| `"compact_boundary"` | Compaction boundary |

## AgentDefinition

```typescript
{
    description: string;   // When to use
    prompt: string;        // System prompt
    tools?: string[];      // Allowed tools
    disallowedTools?: string[];
    model?: string;        // sonnet/opus/haiku/inherit
    skills?: string[];
    maxTurns?: number;
    background?: boolean;
    effort?: EffortLevel;
    permissionMode?: PermissionMode;
}
```

> **V2 Session API (deprecated):** The experimental `createSession()` + `send`/`stream` pattern is deprecated. Use V1 `query()` + session options (`resume`, `forkSession`, `continue`).