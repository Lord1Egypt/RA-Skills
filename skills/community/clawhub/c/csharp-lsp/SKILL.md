---
name: csharp-lsp
slug: csharp-lsp
version: 1.2.0
description: "C# language server providing code intelligence, diagnostics, and navigation for .cs and .csx files. Uses csharp-ls (lightweight Roslyn-based). Requires .sln or .csproj."
metadata:
  openclaw:
    emoji: "💜"
    requires:
      bins: ["dotnet"]
    os: ["linux", "darwin", "win32"]
    install:
      - id: dotnet
        kind: manual
        label: "Install .NET SDK (https://dot.net/download)"
---

# C# LSP

C# code intelligence via [csharp-ls](https://github.com/razzmatazz/csharp-language-server) — a lightweight Roslyn-based language server.

## Capabilities

- **Go-to-definition**: Jump to symbol definitions across solution
- **Find references**: Locate all usages of a symbol
- **Hover info**: Type signatures, XML docs, parameter info
- **Diagnostics**: Real-time compiler errors and warnings
- **Document symbols**: List classes, methods, properties in a file
- **Workspace symbol search**: Find symbols across the entire solution

Supported extensions: `.cs`, `.csx`

## Prerequisites

- **.NET SDK** (9.0+): https://dot.net/download
- **Python 3**: Required to run the lsp-query daemon
- **`.sln` or `.csproj`**: Project file is required (loose .cs files give limited results)

## Setup

Run the one-time setup script (idempotent — safe to re-run):

```bash
bash {baseDir}/scripts/setup.sh           # setup only
bash {baseDir}/scripts/setup.sh --verify  # setup + verification test
```

What it does:
1. Checks for .NET SDK
2. Installs `csharp-ls` via `dotnet tool install --global`
3. Registers `~/.dotnet/tools` in PATH
4. Creates `lsp-query` symlink
5. Creates cache directory

## Usage

```bash
# Set workspace to the directory containing .sln/.csproj
export LSP_WORKSPACE=/path/to/project

# Go to definition
lsp-query definition src/Program.cs 15 8

# Find all references
lsp-query references src/Models/User.cs 42 10

# Type info / hover
lsp-query hover src/Services/AuthService.cs 30 22

# List symbols in a file
lsp-query symbols src/Program.cs

# Search symbols across workspace
lsp-query workspace-symbols "UserService"

# Compiler diagnostics
lsp-query diagnostics src/Program.cs

# Check running servers
lsp-query servers

# Shut down daemon
lsp-query shutdown
```

Line/column numbers are **1-indexed**.

## Architecture

```
lsp-query CLI → Unix Socket → lsp-query daemon (Python)
                                   ↓
                              csharp-ls (subprocess, stdin/stdout JSON-RPC)
                                   ↓
                              Roslyn (.sln → full type system)
```

- **Daemon**: Auto-forks on first call. Shuts down after 5 min idle.
- **csharp-ls**: Starts on first C# query. Shuts down after 5 min idle.
- **Cold start**: Solution loading takes 30–60s for large projects. Subsequent queries ~200ms.

## Project Detection

1. **Solution file** (`.sln`) — best: enables cross-project references
2. **Project file** (`.csproj`) — good: single project analysis
3. **Loose `.cs` files** — limited: basic syntax only

## What's Included

```
{baseDir}/
├── SKILL.md              # This file
└── scripts/
    ├── setup.sh          # One-time setup (idempotent)
    └── lsp-query.py      # LSP daemon + CLI (self-contained)
```

## Troubleshooting

- **Install fails (`DotnetToolSettings.xml`)**: Pin version with `dotnet tool install --global csharp-ls --version 0.20.0`
- **Empty results**: Check that `LSP_WORKSPACE` points to a directory with `.sln` or `.csproj`
- **Slow first query**: Normal — Roslyn project loading takes 30–60s for large solutions
- **PATH issues**: Add `export PATH="$PATH:$HOME/.dotnet/tools"` to your shell profile
- **Stale daemon**: Run `lsp-query shutdown` and retry

## Links

- [csharp-ls on GitHub](https://github.com/razzmatazz/csharp-language-server)
- [.NET SDK Downloads](https://dot.net/download)
- [LSP Specification](https://microsoft.github.io/language-server-protocol/)
