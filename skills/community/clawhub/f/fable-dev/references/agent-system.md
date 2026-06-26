# Agent / AI System Reference

Fable's AI system uses Google ADK (Agent Development Kit) with a multi-provider LLM registry. The system supports chat sessions, streaming responses, tool execution with confirmation, planning mode, observer mode, and user-defined agents.

## Architecture

```
useChat hook (frontend)
    | window.api.sendMessageStreaming(projectId, sessionId, content, contextItems, modelId, mode, agentId)
    |
AgentHandlers.sendMessageStreaming()
    |
AgentService.sendMessageStreaming()
    ├→ SessionService.addMessage() -- persist user message
    ├→ Load agent definition (built-in or project-defined)
    ├→ Build chat history from ChatDatabaseService
    └→ AdkRunner.streamWithAdk(input) -- AsyncGenerator
        ├→ ProviderRegistry.resolve(modelId) -- get adapter + provider model
        ├→ ToolFactory.buildTools() -- filtered by agent.allowedTools
        ├→ Create ADK LlmAgent + Runner
        └→ Yield AdkStreamEvent for each chunk/tool-call/done
            |
        IpcTransport.send("agent:streamEvent", event)
            |
        useChat hook receives events via window.api.onAgentStreamEvent()
```

## Provider Registry

**File**: `src/backend/services/agent/providers/registry.ts`
**Config**: `src/config/models.json`

Maps user-facing model IDs to provider adapters:
- `ProviderRegistry.resolve(modelId)` -> `{ adapter, providerModelId }`
- `ProviderRegistry.listModels()` -> `ModelOption[]`
- `ProviderRegistry.getDefaultModelId()` -> string

### Adapters

| Adapter | File | Providers |
|---|---|---|
| `OpenAICompatibleAdapter` | `providers/openai-compatible.ts` | OpenAI, DeepSeek |
| `GoogleAdapter` | `providers/google.ts` | Gemini |
| `AnthropicAdapter` | `providers/anthropic.ts` | Claude |

Each adapter implements `ProviderAdapter.complete(request)` returning a response stream.

## Tool System

### Tool Descriptors (shared)

**File**: `src/shared/toolDescriptors.ts`

Defines 43 tools shared between the UI command system and LLM agents:

**File tools**: readContent, writeContent, create, rename, move, delete, duplicate, updateMetadata, getTree, search
**Graph tools**: read, query (neighbors/path/subgraph/components/centrality), addNode, removeNode, addEdge, removeEdge, updateNode, updateEdge
**Reference tools**: getReferences

Each descriptor:
```typescript
interface ToolDescriptor {
    commandId: string;          // e.g., "file.readContent"
    toolName: string;           // e.g., "read_file"
    description: string;
    parameters: Record<string, ToolParameterDescriptor>;
    required: string[];
    requiresConfirmation?: boolean;  // Pauses for user approval
    readOnly?: boolean;              // Safe for observer mode
}
```

### Tool Factory (backend)

**File**: `src/backend/services/agent/toolFactory.ts`

`buildTools(projectId, fsService, agentToolAllowlist?, observerMode?)`:
1. Filters descriptors by agent's `allowedTools` list
2. In observer mode, further filters to `READ_ONLY_TOOL_IDS` only
3. Builds ADK `FunctionTool` for each remaining descriptor
4. Executor functions validate inputs and call `IndexedFsService` or graph utilities

### Tool Confirmation Flow

For tools with `requiresConfirmation: true`:
1. Tool execution pauses
2. Backend emits `tool_confirm_request` stream event with `requestId`
3. Frontend shows confirmation UI in chat
4. User approves/denies
5. Frontend calls `window.api.resolveToolConfirmation(requestId, approved)`
6. `AgentService.resolveToolConfirmation()` resolves the pending promise
7. Tool execution resumes or returns denial message

## Chat Persistence

### ChatDatabaseService

**File**: `src/backend/services/agent/chatDatabaseService.ts`

Per-project SQLite at `<project_root>/.fable/chat.db`. Singleton instances cached by project root.

Tables:
```sql
chat_sessions (id, title, created_at, updated_at)
chat_messages (id, session_id, role, content, timestamp, metadata, agent_id)
```

### SessionService

**File**: `src/backend/services/agent/sessionService.ts`

Higher-level CRUD over ChatDatabaseService with type transformations:
- `createSession()`, `getSession()`, `listSessions()`, `deleteSession()`
- `forkSession(sourceSessionId, beforeMessageId)` -- copies messages to new session
- `addMessage()`, `getMessages()`

## Built-in Agents

**File**: `src/backend/services/agent/prompts.ts`

| Agent | Purpose | Tool Access |
|---|---|---|
| `default` | General assistant | All tools |
| `editor` | Writing/editing focus | Write-focused tools |
| `reader` | Read-only analysis | Read-only tools |
| `writer` | Creative writing | Write tools + content tools |

Each agent has:
- `id`, `name`, `abbreviation`
- `instruction` -- system prompt text
- `allowedTools` -- array of tool command IDs

System instruction = `SYSTEM_CONTEXT` (platform facts) + agent-specific instruction.

## User-Defined Agents

**File**: `src/backend/services/agent/projectAgentLoader.ts`

Files with `metadata.subType === "agent"` are loaded as custom agents:

```json
{
    "name": "My Agent",
    "abbreviation": "MA",
    "instruction": "You are a helpful assistant...",
    "allowedTools": ["file.readContent", "file.writeContent"]
}
```

- Tool list validated against known `toolDescriptors`
- Agent ID derived from file ID: `agent${fileId}`
- Invalid agents skipped gracefully
- Loaded via `getAvailableAgents(projectId, fsService)`

## Streaming Events

**Type**: `AdkStreamEvent` (defined in `src/types.ts`)

| Event | Fields | Purpose |
|---|---|---|
| `text_delta` | `text` | Incremental text chunk |
| `text` | `text` | Complete text (on done) |
| `tool_call` | `toolName`, `args`, `callId` | Tool invocation start |
| `tool_result` | `toolName`, `result`, `callId` | Tool execution result |
| `tool_confirm_request` | `requestId`, `toolName`, `args` | Awaiting user approval |
| `done` | `messageId` | Generation complete |
| `error` | `error` | Generation failed |

## Planning Mode

When `mode === "plan"`:
- No tools are provided to the LLM
- Uses `PLANNING_OUTPUT_SCHEMA` (JSON schema) for structured output
- Output includes: `goal`, `assumptions`, `steps[]`, `risks`, `verification`
- Each step may have `clarifyQuestions[]` for user follow-up
- Frontend renders plan structure in `ChatView`

## Observer Mode

When `observerMode === true`:
- Only tools in `READ_ONLY_TOOL_IDS` set are available
- Prevents any write operations (create, delete, rename, move, write)
- Used for safe browsing/analysis of project content

## AgentFlow Execution

**File**: `src/backend/services/agentFlow/agentFlowRunner.ts`

Visual workflow execution for `agentflow` files:

```typescript
startAgentFlowRun({ projectId, fileId, options, onStreamEvent })
    -> validates graph structure
    -> traverses nodes (agent -> ifElse -> while -> userApproval -> end)
    -> executes agent nodes via AdkRunner
    -> handles conditional branching and loop counting
    -> max 5 minutes per run
```

Events: `AgentFlowStreamEvent` -- `run_started`, `node_start`, `node_end`, `text_delta`, `approval_request`, `run_completed`, `run_error`

Approval flow similar to tool confirmation: emits `approval_request`, waits for `resolveAgentFlowApproval()`.

## Frontend Chat Hook

**File**: `src/frontend/hooks/useChat.ts`

`useChat(projectId)` manages full chat lifecycle:
- **State**: `sessions`, `currentSession`, `messages`, `isLoading`, `isSending`, `streamLog`
- **Actions**: `loadSessions`, `createSession`, `selectSession`, `deleteSession`, `sendMessage`, `stopGeneration`, `resolveConfirmation`, `forkSession`
- **Stream handling**: Subscribes to `window.api.onAgentStreamEvent()`, accumulates text deltas, tracks tool calls in `streamLog`

## Adding a New LLM Provider

1. Create adapter in `src/backend/services/agent/providers/` implementing `ProviderAdapter`
2. Register in `src/backend/services/agent/providers/registry.ts`
3. Add model entries to `src/config/models.json`
4. Add any required API key to environment config

## Adding a New Agent Tool

1. Add `ToolDescriptor` in `src/shared/toolDescriptors.ts`
2. Add executor function in `toolFactory.ts` `buildExecutors()`
3. If read-only, add to `READ_ONLY_TOOL_IDS`
4. If needs confirmation, set `requiresConfirmation: true`
5. Add i18n keys for tool name in `chat.json` (both locales)
6. Update agent definitions' `allowedTools` if needed
