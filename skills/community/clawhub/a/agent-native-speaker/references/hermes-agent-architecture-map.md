# Hermes Agent Architecture Map

> Source directory layout and key files for Hermes Agent. Used by Agent Native Speaker (Layer 2) to locate code when users ask about Hermes's internal design.

> **Note:** This map is a living reference. The actual source root may vary by installation. Always verify with `ls` or `search_files` before relying on a path.

## Source Layout

```
<hermes-home>/
├── src/                          # Main source code
│   ├── core/                     # Core engine
│   │   ├── agent_loop.py         # Main agent execution loop
│   │   ├── session_manager.py    # Session lifecycle and persistence
│   │   ├── memory_manager.py     # Long-term memory (MEMORY.md/USER.md)
│   │   ├── config_loader.py      # Config loading (YAML, env vars)
│   │   └── tool_handler.py       # Tool execution and result processing
│   ├── gateway/                  # Multi-platform gateway
│   │   ├── gateway.py            # Message routing and platform abstraction
│   │   ├── telegram_gateway.py   # Telegram adapter
│   │   ├── discord_gateway.py    # Discord adapter
│   │   └── cli_gateway.py        # Terminal/CLI adapter
│   ├── provider/                 # LLM provider abstraction
│   │   ├── base.py               # Abstract provider interface
│   │   ├── anthropic.py          # Anthropic API adapter
│   │   ├── openai.py             # OpenAI API adapter
│   │   └── openrouter.py         # OpenRouter API adapter
│   ├── tools/                    # Tool definitions
│   │   ├── registry.py           # Tool registration and discovery
│   │   ├── tool_manager.py       # Tool lifecycle management
│   │   └── builtin/              # Built-in tool implementations
│   └── agent/                    # Agent orchestration
│       ├── agent.py              # Agent class, orchestrates loop + tools + memory
│       └── context.py            # Context window management
├── config.yaml                   # User-facing config
├── state.db                      # SQLite database (sessions, messages)
├── memories/                     # Long-term memory store
│   ├── MEMORY.md                 # Environment/project notes
│   └── USER.md                   # User profile and preferences
├── skills/                       # Installed skills
└── hooks/                        # Lifecycle hooks
```

## Key Components

### Agent Loop (`src/core/agent_loop.py`)
- The heartbeat of the Agent
- Pattern: `while` loop with state machine
- States: WAITING_FOR_INPUT → PROCESSING → TOOL_CALL → RESPONDING
- Configurable max_turns to prevent infinite loops

### Memory System (`src/core/memory_manager.py` + `memories/`)
- Two tiers: session-scoped (SQLite messages table) + persistent (markdown files)
- Session memory: `state.db` → `messages` table (role, content, timestamp, tool_calls)
- Long-term memory: `memories/MEMORY.md` + `memories/USER.md` — plain text with `§` delimiters
- Injected into system prompt at session start

### Tool System (`src/core/tool_handler.py` + `src/tools/`)
- Tool registration via decorators or registry
- Tool execution in sandboxed environment
- Result formatted as tool role message back to LLM
- Error handling: `is_error` flag on ToolResult

### Session Management (`src/core/session_manager.py` + `state.db`)
- SQLite-backed: `sessions` table + `messages` table
- FTS5 full-text search on messages
- Cross-session recall via `session_search` tool

### Provider Layer (`src/provider/`)
- Adapter pattern: each provider implements a common interface
- Supports OpenAI, Anthropic, OpenRouter, and custom providers
- Model selection via config, fallback chains

## Common Search Targets

| Question | Search For |
|----------|-----------|
| "How does the agent loop work?" | `src/core/agent_loop.py` — `def run()`, `while` |
| "How is memory stored?" | `src/core/memory_manager.py` — `MEMORY.md`, `USER.md` |
| "How does tool calling work?" | `src/core/tool_handler.py` — `execute_tool`, `is_error` |
| "How are sessions managed?" | `src/core/session_manager.py` — `create_session`, `get_session` |
| "Where does the app start?" | Main entry point (varies by platform) |
| "How are configs loaded?" | `src/core/config_loader.py` — `load_config`, `yaml.safe_load` |
| "How are providers used?" | `src/provider/base.py` — `class Provider`, `complete()` |
