# Architecture

## Overview

csharp-lsp provides C# code intelligence through a three-layer architecture:

```
┌─────────────┐     Unix Socket     ┌──────────────────┐     stdin/stdout     ┌───────────┐
│ lsp-query   │ ──────────────────▸ │ lsp-query daemon │ ─────────────────▸  │ csharp-ls │
│ CLI         │                     │ (Python)         │   JSON-RPC (LSP)    │ (Roslyn)  │
└─────────────┘                     └──────────────────┘                     └───────────┘
  one-shot                            persistent                              persistent
  process                             background                              subprocess
```

## Components

### lsp-query CLI

The user-facing command. Each invocation:

1. Checks if daemon is running (via pid file)
2. If not, forks a new daemon process (`fork()` + `setsid()`)
3. Connects to daemon via Unix socket (`~/.cache/lsp-query/daemon.sock`)
4. Sends JSON request, receives JSON response, prints result, exits

### lsp-query Daemon (MultiLangDaemon)

A single Python process managing LSP clients for multiple languages. For C#:

1. Receives query from CLI via Unix socket
2. Determines language from file extension (`.cs` → csharp)
3. Lazy-starts `csharp-ls` subprocess if not already running
4. Forwards LSP request, collects response
5. Returns result to CLI

**Lifecycle:**
- Created on first `lsp-query` call (auto-fork)
- Stays alive serving subsequent requests
- Shuts down after 5 minutes of inactivity (configurable via `LSP_TIMEOUT`)

### csharp-ls (Language Server)

Roslyn-based C# language server running as a subprocess:

1. Communicates via stdin/stdout using JSON-RPC (LSP protocol)
2. On startup, loads the solution file (`.sln`) and builds the full type system
3. Responds to LSP requests: hover, definition, references, symbols, diagnostics

**Key behavior:**
- **Initialize handshake**: Daemon sends `rootUri` (solution path). Server responds with capabilities.
- **Server-to-client requests**: csharp-ls sends `client/registerCapability`, `workspace/configuration`, `window/workDoneProgress/create` — daemon responds with `result: null` to unblock.
- **Solution loading**: Roslyn compiles all `.csproj` → full type system. Takes 30–60s for large solutions.
- **Diagnostics signal**: `publishDiagnostics` notification indicates loading is complete.

## Communication Flow

```
CLI                    Daemon                   csharp-ls
 │                       │                         │
 │──── connect ─────────▸│                         │
 │                       │──── spawn ─────────────▸│
 │                       │◂──── initialize ───────▸│
 │                       │◂── registerCapability ──│
 │                       │── result: null ────────▸│
 │                       │◂── workspace/config ────│
 │                       │── result: null ────────▸│
 │                       │◂── publishDiagnostics ──│ (loading done)
 │                       │                         │
 │── hover request ─────▸│                         │
 │                       │── textDocument/hover ──▸│
 │                       │◂── hover result ────────│
 │◂── response ──────────│                         │
 │                       │                         │
 │                       │   (5 min idle)          │
 │                       │── shutdown ────────────▸│
 │                       │                         ✕
 │                       │   (5 min idle)
 │                       ✕
```

## File Locations

| File | Purpose |
|------|---------|
| `~/.cache/lsp-query/daemon.sock` | Unix socket for CLI↔daemon |
| `~/.cache/lsp-query/daemon.sock.pid` | Daemon PID file |
| `/tmp/lsp-query-debug.log` | Debug log (when `LSP_DEBUG=1`) |
| `~/.dotnet/tools/csharp-ls` | Language server binary |

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `LSP_WORKSPACE` | current dir | Root directory containing `.sln`/`.csproj` |
| `LSP_TIMEOUT` | `300` | Idle timeout in seconds before server shutdown |
| `LSP_DEBUG` | (unset) | Set to `1` for debug logging to `/tmp/lsp-query-debug.log` |
