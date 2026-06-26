# Supervisor Module Spec

## 1. Module Overview

**File**: `internal/orchestrator/supervisor.go`

**Core responsibility**: this file is the **main entry point** of the AI assistant agent. It builds and runs a ReAct LLM agent (Supervisor) that understands user intent and calls different tools to fulfill requests.

---

## 2. Exported Interface

- **`GetSupervisor`**: builds and returns a fully configured agent instance without running inference.
- **`Generate`**: the main external entry point, called by the service layer. Accepts a list of user messages, starts agent inference, and returns an event stream iterator.

## 3. Core Build Logic

### 3.1 ConfigOverrides pre-loading
If `configID` is present in context, pre-load ConfigOverrides and store in context. Used downstream to override model parameters, system prompt, tool enable/disable, and tool descriptions.

### 3.2 Client version branching — tool set selection

| Version range | Tool set |
|--------------|----------|
| `< 2.0.0` (Legacy) | ToolA, ToolB, ToolC, ToolD, ToolE, ToolF |
| `>= 2.0.0` (Current) | ToolA_V2, ToolB_V2, ToolC_V2, ToolD_V2, ToolE_V2, ToolF_V2 |
| `>= 3.0.0` (additional) | NewCapabilityTool |

### 3.3 Tool overrides
When ConfigOverrides are present, tools can be disabled by name or have their descriptions replaced.

### 3.4 Middleware loading
Three handler-level middlewares:
- **Format patch**: fixes tool call format compatibility issues
- **Output parse**: intercepts specific tags in the stream and converts them to structured data
- **Routing middleware**: injects skill routing capability

### 3.5 Agent model config
- **Cache**: session cache, supports multi-turn conversations
- **Max iterations**: 100-step ReAct loop
- **Sequential tool execution**: prevents concurrent delivery from causing client rendering issues
- **ReturnDirectly**: certain tools return their output directly without a second LLM pass

### 3.6 Multi-layer config override chain
`code default → config center → A/B experiment → ConfigOverrides`

## 4. Key Design Decisions
1. **Single agent + multiple tools, flat architecture** — the LLM autonomously decides which tool to call
2. **Version compatibility**: two tool sets maintained via version branching
3. **Config-driven + middleware decoupling**: agent behavior can be adjusted flexibly via config platforms
4. **Content moderation integration**: async moderation intercept after LLM output
5. **supervisor.go contains no business logic** — purely responsible for assembling and starting the agent
