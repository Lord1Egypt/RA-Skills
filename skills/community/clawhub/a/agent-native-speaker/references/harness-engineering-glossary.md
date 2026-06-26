# Harness Engineering Glossary

> A reference glossary for Layer 1 (concept-level) teaching. Every term includes a simple definition, an analogy, and a common misconception.

---

## Agent Loop

| | |
|---|---|
| **What it is** | The core infinite loop that drives an Agent: receive input → process with LLM → execute tools if needed → return response → repeat |
| **Analogy** | A restaurant: customer orders → kitchen cooks → waiter serves → next customer. The waiter never stops walking the floor. |
| **Wrong model** | "The Agent just answers one question and stops." — No, it loops, optionally calling tools between each turn. |
| **Real-world design variants** | `while True` with state machine, async event loop, turn-bounded loop with max_turns |

## Tool Calling / Function Calling

| | |
|---|---|
| **What it is** | The mechanism by which an LLM requests execution of a predefined function (tool). The Agent handles the request, runs the tool, and feeds the result back to the LLM. |
| **Analogy** | A chef who can't chop vegetables, but has assistants who can. Chef says "chop the onion" → assistant does it → chef gets the chopped onion back and continues cooking. |
| **Wrong model** | "The LLM executes the tool itself." — No, the LLM only *requests* tool execution. The Agent framework executes and returns the result. |
| **Real-world design variants** | Parallel tool calls, sequential tool calls, tool call batching, tool choice enforcement (required/auto/none) |

## Tool Result / Tool Output

| | |
|---|---|
| **What it is** | The structured output returned after a tool executes, including stdout, stderr, return code, and error status. This is formatted and fed back to the LLM. |
| **Analogy** | You ask someone to check the mail. They come back and say "three letters, no packages" (success) or "I dropped the keys" (error). Both are results. |
| **Wrong model** | "If the tool fails, the Agent just stops." — No, errors are returned to the LLM, which can decide what to do next. |
| **Real-world design variants** | Error-flagged results, truncated output for large returns, streaming results |

## Memory / State Persistence

| | |
|---|---|
| **What it is** | How an Agent remembers information across turns (within a conversation) and across conversations (between sessions). |
| **Analogy** | Your own memory: working memory (what you're thinking about right now = context window), long-term (your birthday = persistent storage), searchable (past conversations = session history). |
| **Wrong model** | "The Agent remembers everything forever." — No, LLMs have a context window limit. Only what fits in the window is active. Everything else is stored and loaded on demand. |
| **Real-world design variants** | In-context (full history), summary compression, vector/semantic retrieval, key-value store, SQL/DB-backed |

## Session Management

| | |
|---|---|
| **What it is** | Tracking a single conversation thread: its ID, messages, timestamps, associated user, and metadata. Sessions enable continuity between turns. |
| **Analogy** | A restaurant check that tracks everything a table orders across the entire meal. The server (Agent) keeps adding to the same check until the table leaves. |
| **Wrong model** | "Every turn is independent." — No, sessions maintain conversation state, tool results, and context across turns. |
| **Real-world design variants** | DB-backed sessions, file-based sessions, stateless (reconstruct from message history) |

## Model Routing / Provider Abstraction

| | |
|---|---|
| **What it is** | Deciding which LLM to call for a given request. Supports different models for different tasks (e.g., cheap model for classification, expensive model for code generation) and provider fallback. |
| **Analogy** | A taxi dispatcher: calls a nearby cab for short trips (fast, cheap), calls a luxury car for important clients (expensive, quality). |
| **Wrong model** | "All Agent requests go to the same model." — No, many Agents route by task type, model capability, cost, or latency requirements. |
| **Real-world design variants** | Static model assignment, dynamic routing (by task analysis), fallback chains, cost-aware routing |

## Configuration System

| | |
|---|---|
| **What it is** | How an Agent loads its settings: API keys, model choices, tool definitions, behavior flags. Usually from config files (YAML, JSON, TOML), environment variables, or CLI flags. |
| **Analogy** | A car's dashboard. You set your preferred temperature, radio station, driving mode before you go. The car doesn't decide these for you. |
| **Wrong model** | "Config is just hardcoded in the code." — No, good Agent frameworks externalize config so you can change behavior without modifying code. |
| **Real-world design variants** | YAML files, environment variables (for secrets), CLI flags, remote config servers, layered configs (defaults + user overrides) |

## Error Handling / Retry / Fallback

| | |
|---|---|
| **What it is** | What the Agent does when something goes wrong: a tool crashes, a model API returns 429, a timeout occurs. Includes automatic retry logic and fallback strategies. |
| **Analogy** | When you call someone and they don't pick up: you wait (retry), call again (retry with backoff), or call their office line instead (fallback). |
| **Wrong model** | "Errors just crash the Agent." — No, well-designed Agents handle errors gracefully, with configurable retry policies. |
| **Real-world design variants** | Immediate retry, exponential backoff, fallback to different model, user notification, circuit breaker pattern |

## Entry Point / Bootstrap

| | |
|---|---|
| **What it is** | The starting point of an Agent application. Loads config, initializes components (LLM client, tools, memory, session manager), then hands control to the agent loop. |
| **Analogy** | When you walk into a restaurant: the host greets you (welcome), checks the reservation (config check), shows you to your table (init), then the waiter takes over (agent loop starts). |
| **Wrong model** | "The main function just calls the agent loop." — No, setup involves validation, error recovery, dependency injection, and graceful teardown at exit. |
| **Real-world design variants** | CLI entry point, server/main, worker/queue based, single-file script |

## Message Protocol

| | |
|---|---|
| **What it is** | The standard format for messages exchanged between user, Agent, and LLM. Typically includes role (user/assistant/system/tool), content, and metadata. |
| **Analogy** | An email: sender, recipient, subject, body, attachments. Everyone agrees on the format so mail servers can route it correctly. |
| **Wrong model** | "Messages are just text strings." — No, they're structured data with roles, tool call IDs, function names, and metadata for correct processing. |
| **Real-world design variants** | OpenAI-style message format, Anthropic-style, custom protocol with extended fields |

## Tool Orchestration

| | |
|---|---|
| **What it is** | The process of managing multiple tool calls within a single agent turn: parallel vs sequential execution, dependency resolution, result collection, and error isolation. |
| **Analogy** | A project manager who has three tasks: "order supplies, hire contractor, and — only after hiring — assign tasks." Some tasks can run in parallel, some depend on others. |
| **Wrong model** | "Tools are always called one at a time." — No, many Agents support parallel tool calls when they're independent of each other. |
| **Real-world design variants** | Sequential (one by one), parallel (batch), DAG-based (dependency graph), streaming (results as they arrive) |

## Provider Abstraction

| | |
|---|---|
| **What it is** | A uniform interface for calling different LLM providers (OpenAI, Anthropic, Groq, local models). The Agent code doesn't care which provider — it speaks a common protocol. |
| **Analogy** | A universal power adapter. Your laptop doesn't care if the socket is US, UK, or EU — the adapter handles the conversion. |
| **Wrong model** | "You hardcode which provider to use." — No, provider abstraction means switching from OpenAI to Anthropic is a config change, not a code change. |
| **Real-world design variants** | Adapter pattern, provider registry, middleware chain, custom provider plugins |
