# Agent Orchestrator Spec

## Overview

`supervisor.go` is the core entry point of the AI assistant agent. It is responsible for **assembling and initializing an LLM agent instance** (Supervisor) that understands user intent and calls the appropriate tools to fulfill requests. The module exposes two functions: `GetSupervisor` (builds the agent) and `Generate` (runs the agent to handle user messages).

## Glossary

- **Supervisor**: the orchestrating agent that understands user intent and selects the right tool to call. It does not execute business logic directly — it orchestrates tool calls.
- **Tool**: a callable unit that encapsulates a specific capability.
- **Legacy tool set**: the set of tools used by older client versions.
- **Current tool set**: the set of tools used by newer client versions.
- **ConfigOverrides**: sparse override config delivered by the debug platform, allowing dynamic control over tool enable/disable, tool description overrides, System Prompt overrides, and model parameter overrides.
- **ConfigID**: a debug config identifier; when non-empty, the request follows the debug/experiment path.

## Behavioral Contracts

### Scenario 1: Building the agent instance (GetSupervisor)

- **Precondition**: `context` has the request context injected (including client version, user info, session info, etc.).
- **Input**: `context.Context`
- **Expected behavior**:

  #### 1.1 Pre-load ConfigOverrides
  - Extract `configID` from context.
  - If `configID` is non-empty, attempt to load ConfigOverrides from storage and store in context.
  - Load failure does not block the flow — silently skip.

  #### 1.2 Select tool set by client version
  - Extract the client version from context and parse it into a structured version number.
  - **Version < 2.0.0 (Legacy)**: use the legacy tool set (ToolA, ToolB, ToolC, etc.).
  - **Version ≥ 2.0.0 (Current)**: use the V2 tool set (ToolA_V2, ToolB_V2, ToolC_V2, etc.).
  - **Version ≥ 3.0.0**: additionally append the new-capability tool.
  - **Version parse failure**: no version-specific tools are added; only log the error. [NOTE] On parse failure, `useLegacyTool` stays `false` and the code takes the current-version branch but with an empty tool list — meaning **the agent will have no tools available**.

  #### 1.3 Apply tool overrides
  - If `configID` is non-empty, filter and override the tool list:
    - Tools marked as disabled are removed.
    - Tools with an override description have their description replaced.

  #### 1.4 Load middlewares
  - Retrieve the handler-level middleware list, which includes:
    - **Format-patch middleware**: fixes tool call format issues.
    - **Output-parse middleware**: intercepts specific tags in the stream and converts them to structured data for the client.
    - **Routing middleware** (optional): injects skill routing capability. Failure to create does not block — silently skip.

  #### 1.5 Assemble AgentConfig
  - **Model**: specified online model, Temperature=1.0, MaxTokens=6144, Timeout=1min.
  - **System Prompt**: hardcoded default in code; overridden at runtime by the version managed in the Prompt platform.
  - **Cache strategy**: session-level cache.
  - **Tool execution mode**: sequential.
  - **Max iterations**: 100. [NOTE] 100 is far larger than what normal conversations require (typically < 10). If reached, it likely means the agent is stuck in a loop.
  - **Agent-level middlewares**:
    - `BeforeChatModel`: before each LLM call, refresh profile info and sync persisted tool messages.
    - `AfterChatModel`: after each LLM response, wait for async moderation result and persist message history.
    - `WrapToolCall`: wraps tool calls for parameter transformation, user-stop checking, and metrics.

  #### 1.6 Create AgentModel
  - Internally resolves the final config by priority:
    1. If `configID` exists and ConfigOverrides are present: fetch the online default config, then apply sparse overrides.
    2. If `configID` exists but no ConfigOverrides: fall back to the full debug config.
    3. If no `configID`: use the online default config (code default → config center → A/B experiment → Prompt platform).

- **Postcondition**: returns an agent instance ready for inference.
- **Error cases**:
  - Middleware creation fails: return error immediately; agent is not created.
  - AgentModel creation fails: return error immediately.
  - ConfigOverrides load failure, config read failure, Prompt fetch failure: all non-blocking; fall back to code defaults.

### Scenario 2: Running the agent to handle user messages (Generate)

- **Precondition**: context has the full business context injected.
- **Input**: `context.Context` + list of user messages.
- **Expected behavior**:
  1. Call `GetSupervisor` to build the agent instance.
  2. Report initialization stage latency metrics.
  3. Call `agent.Run` to start agent inference with streaming enabled. [NOTE] The stop channel is passed as `nil`; user cancellation relies on reading a stop signal from context instead.
  4. Return an event stream iterator; the caller consumes agent-produced events via the iterator.
- **Postcondition**: returns an event stream iterator for streaming consumption.
- **Error cases**:
  - `GetSupervisor` fails: return error; inference is not started.

## Constraints & Boundaries

### Tool execution
- All tools execute **sequentially** — no parallel calls.
- Certain tools are marked `ReturnDirectly`: their output is returned directly to the user without a second LLM pass.

### Version compatibility
- Version checks are performed independently in two places: tool set selection and System Prompt key selection. [NOTE] These two checks are independent — it is theoretically possible for the tool set and System Prompt version to be mismatched (e.g., if ConfigOverrides overrides the System Prompt key but not the tool set).

### Configuration priority
- Model parameters: code default < config center < A/B experiment.
- System Prompt: hardcoded default < Prompt platform version < ConfigOverrides.
- Tool list: code version selection < ConfigOverrides.

### What we don't do
- The Supervisor itself **executes no business logic** — all capabilities are encapsulated in tools.
- The Supervisor **does not manage conversation history persistence** — that is handled by middleware.
- The Supervisor **does not handle streaming delivery directly** — that is handled by the output-parse middleware.

## Dependencies

### Depends on
| Dependency | Purpose |
|---|---|
| **LLM service** | Inference |
| **Prompt platform** | System Prompt hosting and versioning |
| **Config center** | Agent model parameter configuration |
| **A/B experiment platform** | Gradual rollout of agent config changes |
| **KV storage** | Session cache, message persistence, ConfigOverrides storage |
| **Agent framework** | Agent construction, tool orchestration, middleware, streaming events |

### Depended on by
- The conversation entry service layer, which calls `Generate` to start agent inference.

## Open Questions

1. [NOTE] **Empty tool set on version parse failure**: the agent will have no tools and can only respond with plain text. Is this the intended behavior? Should it fall back to a default tool set?

2. [NOTE] **MaxIterations = 100**: this is far larger than what normal conversations need (typically < 10). Should a timeout mechanism or a more reasonable upper bound be added?

3. [NOTE] **Stop channel passed as nil in Generate**: actual user cancellation is implemented by reading a stop signal from context, not via this parameter. Is this parameter effectively deprecated?
