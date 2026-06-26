# Fabric.so CLI command reference

This file is a compact, agent-oriented reference for the Fabric.so CLI executable named `fabric`. It is based on the public Fabric User Guide page for the CLI, checked on 2026-04-29, plus the Fabric CLI download page for agent-memory positioning. Always prefer live `fabric --help` and `fabric help COMMAND` for syntax that may have changed.

## Usage and global options

Documented usage:

```bash
fabric [options] [command]
```

Global options:

| Option | Meaning | Agent guidance |
| --- | --- | --- |
| `-V, --version` | Output version number | Use during local diagnostics. |
| `-h, --help` | Display help for command | Use before unrecognised options. |
| `--json` | Output JSON in non-interactive mode | Prefer for parsing, filtering, summarisation, and scripting. |

JSON output is documented as a global option, but individual command behaviour may vary by CLI version. If `fabric --json COMMAND` fails, inspect help and retry without JSON for diagnostics.

## Installation

Official installer:

```bash
curl -fsSL https://fabric.so/cli/install.sh | sh
```

Do not run this automatically unless the user explicitly requested installation in the current environment. For a safer workflow:

```bash
tmp_script="$(mktemp)"
curl -fsSL https://fabric.so/cli/install.sh -o "$tmp_script"
sed -n '1,200p' "$tmp_script"
# run with user approval:
sh "$tmp_script"
```

## Authentication and account commands

| Command | Purpose | Notes |
| --- | --- | --- |
| `fabric login` | Login via browser | Preferred for humans in an interactive terminal. |
| `fabric auth API_KEY` | Store API key | Use only when securely supplied. Never echo or save the key. |
| `fabric logout` | Clear stored credentials | State-changing; confirm first unless explicitly requested. |
| `fabric subscription` | Show workspace plan, usage, quotas | Read-only; useful for quota problems. |

## Search and browse

| Command | Purpose | Typical usage |
| --- | --- | --- |
| `fabric search [options] [query]` | Search the current Fabric workspace | Semantic/hybrid lookup by query and/or tag. |
| `fabric path [options] [query]` | Browse items and locations | No argument lists root spaces; path-like queries browse locations. |
| `fabric inbox [options]` | List Inbox items | Read-only location listing. |
| `fabric bin [options]` | List Bin items | Read-only location listing. |

Examples:

```bash
fabric --json search "meeting notes"
fabric --json search "design" --tag work
fabric --json search --tag reading,todo
fabric --json path
fabric --json path "My Space"
fabric --json path "Inbox/Reports"
fabric --json inbox
fabric --json bin
```

Use `search` when the user describes content semantically. Use `path` when the user describes a location, space, folder, Inbox path, or wants to browse.

## Create and save content

The docs state that `note`, `link`, and `file` are shortcuts for corresponding `create` commands. The `save` command is a smart command that detects URL, file path, text, or stdin and creates the appropriate resource.

| Command | Purpose | Notes |
| --- | --- | --- |
| `fabric create KIND` | Explicit resource creation | `KIND` can be `space`, `folder`, `note`, `link`, or `file`. |
| `fabric note [content]` | Create a note | Reads stdin if content is omitted. Good for long generated text. |
| `fabric link URL` | Save a bookmark | Use for URLs when type should be explicit. |
| `fabric file PATH` | Upload a local file | Check path existence first. |
| `fabric save [input]` | Smart-save | URL becomes bookmark, file path becomes upload, text becomes note, stdin is accepted. |
| `fabric folder [name]` | Create a folder | Inbox by default unless `--parent`, `/`, or path is used. |

Examples:

```bash
fabric --json create note "Meeting summary" --tag work
fabric --json create note "Q1 Review" --parent "Work/Projects"
fabric --json create folder "Projects" --tag client
fabric --json create folder "Archive" --parent "Work" --tag archive
fabric --json create folder "My Space" --parent /
fabric --json create link "https://example.com" --title "Article"
fabric --json create file "$HOME/Desktop/report.pdf"

fabric --json note "Quick reminder" --tag remember
fabric --json note "Ideas" --parent "Work/Projects"
fabric --json link "https://example.com" --title "Article" --tag reading
fabric --json link "https://example.com" --parent "Work/Reading"
fabric --json file "$HOME/Downloads/report.pdf" --title "Q4 Report"
fabric --json file "$HOME/Downloads/report.pdf" --parent "Work/Reports"

fabric --json save "https://example.com" --tag reading
fabric --json save "$HOME/Downloads/doc.pdf" --title "Report"
fabric --json save "Remember to call dentist" --tag personal
```

For multi-line notes, prefer stdin:

```bash
cat /tmp/generated-note.md | fabric --json note --tag agent-memory
```

If both a title and long body are needed, inspect `fabric note --help` or `fabric create note --help` for title/body support in the installed version before assuming syntax. If multiple tags are needed, inspect help for whether repeated `--tag` or comma-separated tags are supported for creation commands.

## Tasks

| Command | Purpose | Notes |
| --- | --- | --- |
| `fabric task list` | List tasks | Supports documented `--todo` and `--done`. |
| `fabric task add TITLE` | Create task | Supports documented `--due-date YYYY-MM-DD` and `--priority HIGH`. |
| `fabric task done TASK_ID` | Mark task completed | Requires task ID. List first if unknown. |
| `fabric task edit TASK_ID` | Edit task | Example uses `--title "New title"`. |
| `fabric task rm TASK_ID` | Delete task | Destructive; confirm first. |
| `fabric task help` | Display task help | Use for current syntax. |

Do not pass a task title to `task done`, `task edit`, or `task rm` unless installed help explicitly supports that. The public docs show task ID syntax.

## Workspaces, assistant, and completion

```bash
fabric --json workspace list
fabric --json workspace current
fabric workspace select "My Team"

fabric --json ask "summarize everything tagged with project-atlas"
fabric --json ask "find the onboarding notes and list open decisions"

fabric completion bash
fabric completion zsh
fabric completion fish
```

Use `ask` when the user wants Fabric's assistant to reason over Fabric context or perform assistant-capable actions. Use `search` when the agent needs raw result candidates to inspect, rank, cite, or use in a deterministic workflow.

Completion generation is read-only, but installation into shell startup files is a local file write and should be done only when the user asks for it.

## Undocumented or partially documented areas

The public page says almost all Fabric capabilities are exposed via the CLI, but it does not list complete syntax for every option, deletion/move/tag/edit command, or item-reading behaviour. For those tasks:

1. Run `fabric help COMMAND` and inspect options.
2. Use only syntax shown by installed help.
3. If no CLI operation is exposed, suggest Fabric MCP, the Fabric web app, or the API rather than guessing.

## JSON handling principles

- Do not assume stable field names beyond what the installed CLI returns.
- Save raw JSON to a temporary file for complex parsing, then use `jq` or Python.
- Keep command output compact; large library searches may need filtering or summarisation.
- If output is not JSON despite `--json`, record the command and stderr and fall back to text parsing only when safe.
