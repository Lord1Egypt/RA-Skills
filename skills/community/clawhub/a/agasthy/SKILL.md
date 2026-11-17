---
name: agasthy
description: Answer questions about this developer machine with real data from AGASTHY - repositories and their uncommitted work, installed runtimes, packages and tools, which process holds a port, which coding-agent sessions are running and what they left behind, token usage and estimated cost per agent, and what would break if a package were removed. Use when the user asks about their own machine, projects, ports, disk, packages, coding agents or token spend, or before suggesting they uninstall something.
homepage: https://github.com/HMAKT99/Agasthy
version: 0.1.5
license: Apache-2.0
platforms: [macos, linux, windows]
metadata:
  {
    "hermes":
      {
        "tags": ["developer-tools", "machine", "coding-agents", "tokens"],
        "category": "devops",
        "requires_toolsets": ["terminal"],
      },
    "openclaw":
      {
        "emoji": "🧭",
        "homepage": "https://github.com/HMAKT99/Agasthy",
        "os": ["darwin", "linux", "win32"],
        "requires": { "bins": ["agasthy"] },
        "install":
          [
            {
              "id": "download-macos",
              "kind": "download",
              "os": ["darwin"],
              "url": "https://github.com/HMAKT99/Agasthy/releases/latest/download/agasthy-cli-macos-aarch64.tar.gz",
              "archive": "tar.gz",
              "bins": ["agasthy"],
              "label": "Download the AGASTHY CLI (macOS, Apple silicon)",
            },
            {
              "id": "download-linux",
              "kind": "download",
              "os": ["linux"],
              "url": "https://github.com/HMAKT99/Agasthy/releases/latest/download/agasthy-cli-linux-x86_64.tar.gz",
              "archive": "tar.gz",
              "bins": ["agasthy"],
              "label": "Download the AGASTHY CLI (Linux x64)",
            },
            {
              "id": "download-windows",
              "kind": "download",
              "os": ["win32"],
              "url": "https://github.com/HMAKT99/Agasthy/releases/latest/download/agasthy-cli-windows-x86_64.zip",
              "archive": "zip",
              "bins": ["agasthy"],
              "label": "Download the AGASTHY CLI (Windows x64)",
            },
          ],
      },
  }
---

# AGASTHY: facts about this machine

`agasthy` is a read-only command-line tool. It never changes the machine: it reads what the AGASTHY desktop app has already scanned, and it reads live process and token-usage data. Every command prints JSON.

## If `agasthy` is not installed

OpenClaw offers to download it. Elsewhere, tell the user to download the archive for their system from https://github.com/HMAKT99/Agasthy/releases/latest (`agasthy-cli-macos-aarch64.tar.gz`, `agasthy-cli-linux-x86_64.tar.gz` or `agasthy-cli-windows-x86_64.zip`), unpack it, and put `agasthy` on their PATH. Each archive has a `.sha256` checksum next to it. Do not download or install it yourself unless they ask.

## How to answer

1. **Start with `agasthy status`.** It shows when each kind of data was last scanned (`age_hours`). Mention the age when it matters ("as of the scan 6 hours ago"). If it says there is no database, the desktop app has not run yet: suggest installing AGASTHY from https://github.com/HMAKT99/Agasthy/releases/latest and running a scan, and use the live commands below meanwhile.
2. **Pick the narrowest command** from the table. Prefer queries over rescans; they are instant.
3. **Answer from the JSON only.** Quote names, paths, versions and numbers exactly. A value with `"status": "unavailable"` means unknown, never zero; say it is unknown.
4. **Never act on the machine for the user** (kill processes, uninstall, delete). Explain what AGASTHY found and point them to the AGASTHY app, which reviews every change with a dry run and lets them undo it. Suggest commands for the user to run only when they ask.

## Commands

| Question | Command |
| --- | --- |
| How fresh is the data? | `agasthy status` |
| Find a repository, package, runtime, tool, app, MCP server... | `agasthy find <text> [--kind KIND] [--limit N]` (add `--full` for all attributes) |
| Everything about one item, with evidence and relationships | `agasthy entity <id>` (ids come from `find`) |
| What breaks if I remove X? | `agasthy impact <id>` (gives `risk`, affected projects, a plan and how to recover) |
| Which dependencies do most projects share? | `agasthy shared` |
| Which coding agents are running, and what did they leave running? | `agasthy agents` |
| What is using port N / which process belongs to which project? | `agasthy processes` |
| How many tokens did my agents use, and what did it cost? | `agasthy usage [--days N]` (totals per agent; add `--full` for `sessions` and `days`, each with `agent`, `cwd` (the project folder), `tokens` and `estimated_cost_usd`, plus `models` per session or `model` and `day` per day) |
| Memory, CPU, disk right now | `agasthy telemetry` |

KIND is one of: `repository`, `application`, `binary`, `runtime`, `package`, `package_manager`, `tool`, `ai_tool`, `ai_provider`, `mcp_server`, `ai_config_file`, `finding`, `remote_project`.

## Reading the results

- **Uncommitted work:** in `agasthy find <name> --kind repository --full`, see `attributes.working_tree.value` (`modified`, `untracked`, `staged`, `clean`) and `attributes.head.value.branch`.
- **Agents:** each item in `sessions` has `label` (Claude Code, Codex, Cursor, Gemini CLI, Hermes, OpenClaw, ...), `project`, `total_memory_bytes`, `ports`, `mcp_servers` and `dev_servers`. `leftovers` are processes still running after the agent that started them exited; `agent_label` says which agent, when known.
- **Ports:** in `agasthy processes`, each item in `processes` has its own `ports` (the ports it listens on), plus `name`, `command`, `cwd`, `memory_bytes` and the `project` it belongs to. The top-level `ports` is only how many listening ports were found.
- **Token cost** is an estimate from public API list prices. People on a subscription plan are billed differently; say so when you quote a cost. Usage reads only token counters from each agent's local logs, never message text.
- **Impact:** `risk` is `low`, `medium` or `high`. `runtime_reports[].items[].outcome` says, per project, whether it `breaks` or `falls_back` to another installed copy.

## Privacy

Results contain local paths, project names and process command lines. Use them to answer the user here. Do not send them to other services or post them anywhere unless the user asks.
