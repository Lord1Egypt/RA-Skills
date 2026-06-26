# OpenClaw Skill: csharp-lsp

[![CI](https://github.com/leafbird/openclaw-csharp-lsp/actions/workflows/test.yml/badge.svg)](https://github.com/leafbird/openclaw-csharp-lsp/actions)
[![ClawHub](https://img.shields.io/badge/ClawHub-csharp--lsp-7c3aed)](https://clawhub.ai/skills/csharp-lsp)
[![Version](https://img.shields.io/github/v/tag/leafbird/openclaw-csharp-lsp?label=version&sort=semver)](https://github.com/leafbird/openclaw-csharp-lsp/releases)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![.NET](https://img.shields.io/badge/.NET-9.0+-512BD4)](https://dot.net/download)
[![csharp-ls](https://img.shields.io/badge/LSP-csharp--ls-68217A)](https://github.com/razzmatazz/csharp-language-server)
[![Platform](https://img.shields.io/badge/platform-Linux%20%7C%20macOS-lightgrey)]()

C# code intelligence for [OpenClaw](https://github.com/openclaw/openclaw) agents — powered by [csharp-ls](https://github.com/razzmatazz/csharp-language-server), a lightweight Roslyn-based language server.

> Go-to-definition, find references, hover, diagnostics, symbol search — all from the command line.

## Features

- **Go-to-definition** — jump to symbol definitions across entire solution
- **Find references** — locate all usages of a symbol (200+ refs in seconds)
- **Hover info** — type signatures, XML docs, parameter info
- **Diagnostics** — real-time compiler errors and warnings
- **Document symbols** — list classes, methods, properties in a file
- **Workspace symbol search** — find symbols across the entire solution
- **Daemon architecture** — persistent background process, ~200ms per query after cold start

## Quick Start

### Prerequisites

- [.NET SDK](https://dot.net/download) 9.0+
- Python 3
- A C# project with `.sln` or `.csproj`

### Install

**Option A: ClawHub** (recommended for OpenClaw users)

```bash
clawhub install csharp-lsp
bash skills/csharp-lsp/scripts/setup.sh --verify
```

**Option B: GitHub**

```bash
git clone https://github.com/leafbird/openclaw-csharp-lsp.git skills/csharp-lsp
bash skills/csharp-lsp/scripts/setup.sh --verify
```

The setup script is **idempotent** — safe to run multiple times.

### Use

```bash
export LSP_WORKSPACE=/path/to/your/solution

lsp-query hover     src/Program.cs 15 8      # type info
lsp-query definition src/Program.cs 15 8     # go to definition
lsp-query references src/Models/User.cs 42 10 # find all references
lsp-query symbols   src/Program.cs            # list symbols
lsp-query workspace-symbols "UserService"     # search workspace
lsp-query diagnostics src/Program.cs          # compiler errors
```

Line/column numbers are **1-indexed**.

## How It Works

```
lsp-query CLI ──Unix Socket──▸ lsp-query daemon (Python)
                                     │
                                     ▼
                               csharp-ls (subprocess)
                                     │
                                     ▼
                               Roslyn engine (.sln → full type system)
```

1. First `lsp-query` call auto-forks a background daemon
2. Daemon lazy-starts `csharp-ls` on first C# query
3. Roslyn loads the solution (30–60s for large projects)
4. Subsequent queries: **~200ms**
5. Both daemon and server auto-shutdown after 5 min idle

See [docs/architecture.md](docs/architecture.md) for details.

## Project Structure

```
csharp-lsp/
├── README.md
├── SKILL.md              # OpenClaw skill descriptor
├── CHANGELOG.md
├── LICENSE
├── scripts/
│   ├── setup.sh          # One-time setup (idempotent)
│   └── lsp-query.py      # LSP daemon + CLI (self-contained)
├── tests/
│   ├── Dockerfile
│   └── test.sh           # Docker-based integration tests
├── docs/
│   ├── architecture.md
│   ├── deployment.md
│   └── troubleshooting.md
└── .github/
    └── workflows/
        └── test.yml      # CI: auto-test on push/PR
```

## Testing

Run the full test suite in a clean Docker environment:

```bash
bash tests/test.sh
```

Tests verify: clean install, hover, definition, references, symbols, and idempotency.

## Troubleshooting

See [docs/troubleshooting.md](docs/troubleshooting.md) for common issues.

Quick fixes:
- **Empty results?** — Check `LSP_WORKSPACE` points to a dir with `.sln`/`.csproj`
- **Slow first query?** — Normal. Roslyn loading takes 30–60s. After that, ~200ms.
- **Stale daemon?** — `lsp-query shutdown` and retry

## License

MIT

## Links

- [csharp-ls](https://github.com/razzmatazz/csharp-language-server) — the language server
- [OpenClaw](https://github.com/openclaw/openclaw) — AI agent framework
- [LSP Specification](https://microsoft.github.io/language-server-protocol/)
