---
name: claw-code
description: AI Agent Harness Runtime — TypeScript port of Claude Code's harness system. Use when: (1) user asks about claw-code, agent harness, or Claude Code internals; (2) user wants to run claw-code commands or query tool/command registries; (3) routing prompts to commands or tools; (4) bootstrapping agent sessions; (5) parity auditing against original TypeScript archive. Triggers on phrases like "claw-code", "harness runtime", "Claude Code port", "agent harness", "run turn loop", "route prompt".
---

# claw-code — AI Agent Harness Runtime

TypeScript port of Claude Code's harness system, compiled and ready to run.

## Quick Start

```bash
cd C:\Users\dae\.openclaw\workspace\skills\claw-code\scripts
node dist/main.js <command> [options]
```

Or build from source:
```bash
cd C:\Users\dae\.openclaw\workspace\skills\claw-code\scripts
npm install
npm run build
```

## Available Commands

### Info & Audit
```
node dist/main.js summary                          # Render workspace summary
node dist/main.js manifest                         # Print workspace manifest
node dist/main.js parity-audit                     # Compare against archive
node dist/main.js setup-report                     # Startup/prefetch report
node dist/main.js command-graph                    # Show command graph
node dist/main.js tool-pool                        # Show tool pool
node dist/main.js bootstrap-graph                  # Show bootstrap stages
```

### Query Registries
```
node dist/main.js subsystems --limit 16             # List Python modules
node dist/main.js commands --limit 20             # List mirrored commands
node dist/main.js commands --query <keyword>      # Search commands
node dist/main.js tools --limit 20                 # List mirrored tools
node dist/main.js tools --query <keyword>          # Search tools
node dist/main.js tools --simple-mode             # Core tools only
node dist/main.js tools --no-mcp                   # Exclude MCP tools
node dist/main.js show-command <name>               # Show one command
node dist/main.js show-tool <name>                 # Show one tool
```

### Runtime Execution
```
node dist/main.js route "<prompt>" --limit 5      # Route prompt to commands/tools
node dist/main.js bootstrap "<prompt>" --limit 5   # Bootstrap a session
node dist/main.js turn-loop "<prompt>" --max-turns 3   # Run turn loop
node dist/main.js flush-transcript "<prompt>"      # Persist session
node dist/main.js load-session <session_id>        # Load saved session
```

### Remote Modes
```
node dist/main.js remote-mode <target>
node dist/main.js ssh-mode <target>
node dist/main.js teleport-mode <target>
node dist/main.js direct-connect-mode <target>
node dist/main.js deep-link-mode <target>
```

### Execution
```
node dist/main.js exec-command <name> "<prompt>"   # Execute mirrored command
node dist/main.js exec-tool <name> <payload>       # Execute mirrored tool
```

## Project Structure

```
claw-code/
├── SKILL.md              # This file
└── scripts/
    ├── dist/             # Compiled JavaScript (ready to run)
    │   └── main.js       # CLI entry point
    ├── src/              # TypeScript source
    │   └── reference_data/  # Snapshot data
    ├── package.json
    └── tsconfig.json
```

## Architecture

- **Runtime Core** (`runtime.ts`) — PortRuntime class: route_prompt, bootstrap_session, run_turn_loop
- **Tool/Command Registries** — loaded from `reference_data/*.json` snapshots
- **Session Management** — session_store.ts, history.ts
- **Query Engine** — query_engine.ts with streaming support
- **Graphs** — bootstrap_graph.ts, command_graph.ts
- **Remote Modes** — remote_runtime.ts, direct_modes.ts
