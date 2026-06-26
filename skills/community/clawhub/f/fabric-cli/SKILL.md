---
name: fabric-cli
description: "Use this skill for Fabric.so CLI workflows with the `fabric` terminal command: diagnose/install/login, search or browse a Fabric library, save notes/links/files, create folders, ask the Fabric AI assistant, manage tasks/workspaces, generate shell completion, check subscription usage, produce JSON output, and use Fabric as persistent agent memory. Do not use for Microsoft Fabric/Azure/Power BI `fab`, Daniel Miessler's Fabric framework, Python Fabric SSH, Fabric.js, or textile/fashion fabric."
compatibility: Requires shell access. Live Fabric operations require the Fabric.so CLI executable named fabric, network access, and a Fabric account. Some workflows need user approval before installing software or changing remote state.
metadata:
  version: "2.0.0"
  source_url: "https://user-guide.fabric.so/ai-tools/CLI-usage"
  updated: "2026-04-29"
---

# Fabric.so CLI agent skill

Use this skill to operate the Fabric.so command-line interface, whose executable is `fabric`. Fabric.so is the personal/team knowledge workspace for notes, docs, files, links, tasks, search, and AI assistant workflows. This skill is not for Microsoft Fabric, Azure, Power BI, OneLake, lakehouses, capacities, semantic models, data pipelines, Daniel Miessler's unrelated Fabric pattern framework, Python Fabric SSH automation, Fabric.js canvas work, or physical cloth/textiles.

## First decision: is this the right Fabric?

Activate this skill when the user wants to use the Fabric.so CLI from a terminal, especially for library search, saving notes/links/files, workspace navigation, tasks, assistant questions, JSON output, automation, or agent memory.

Do not use this skill when the request is about Microsoft Fabric, Azure, Power BI, OneLake, lakehouses, notebooks, KQL, semantic models, capacities, tenants, deployment pipelines, or the `fab` CLI. Also do not use it for Daniel Miessler's Fabric framework, Fabric.js, Python Fabric SSH, or sewing/textile fabric.

If the user says only "Fabric CLI" and the surrounding terms are ambiguous, inspect the context. Terms such as library, note, bookmark, workspace memory, `fabric save`, `fabric search`, or `fabric ask` point to Fabric.so. Terms such as lakehouse, Power BI, tenant, capacity, OneLake, workspace item, or `fab` point elsewhere.

## Source-of-truth rule

The installed CLI may be newer than this skill. Before using an option not shown here, inspect live help:

```bash
fabric --help
fabric help COMMAND
fabric COMMAND --help
```

Prefer the global `--json` option for parseable, non-interactive output when supported:

```bash
fabric --json search "project notes"
fabric --json workspace current
fabric --json task list --todo
```

If JSON fails, retry without `--json`, inspect command help, and report the limitation. Do not invent JSON schemas; parse defensively.

## Safety and consent rules

Treat Fabric as a real remote workspace.

Read-only operations can proceed when relevant: `search`, `path`, `inbox`, `bin`, `workspace current`, `workspace list`, `task list`, `subscription`, and local help/version checks.

State-changing operations require a clear user request: `note`, `link`, `file`, `save`, `create`, `folder`, `task add`, `task done`, `task edit`, `workspace select`, and authentication setup. Destructive or hard-to-reverse operations require explicit confirmation immediately before execution: `task rm`, `logout`, deletion/move/bulk edits if exposed by installed help, and any broad content-changing command discovered from help.

Never run the remote installer unless the user explicitly asked to install Fabric CLI in the current environment. The official installer is:

```bash
curl -fsSL https://fabric.so/cli/install.sh | sh
```

For safer review, download the script to a temporary file, inspect it, then run only with approval.

Never print, store, or save API keys, tokens, passwords, cookies, or private secrets to Fabric. Redact secrets from generated memory notes. Prefer environment variables or browser-based `fabric login`. Use `fabric auth API_KEY` only when the key is already securely available or the user explicitly chooses that route.

Use stdin for long notes and shell-safe quoting for all user-provided text, paths, tags, URLs, titles, parent folders, task titles, and workspace names.

## Fast environment check

For live workflows, check that the Fabric.so CLI is present and not confused with another Fabric tool:

```bash
python3 scripts/fabric_check.py --json
```

When the user wants to actually use Fabric and read-only account checks are acceptable, run:

```bash
python3 scripts/fabric_check.py --deep --json
```

The checker is read-only. It does not install software, authenticate, write to Fabric, change workspace, or log out.

Use `scripts/fabric_help_cache.py` when you need current command help for several subcommands:

```bash
python3 scripts/fabric_help_cache.py --commands search,path,save,task,workspace --json
```

Use `scripts/fabric_command_plan.py` to build shell-quoted command plans without executing them.

## Core command map

The documented top-level usage is:

```bash
fabric [options] [command]
```

Known global options:

```bash
fabric --version
fabric --help
fabric --json COMMAND
```

High-level command purposes:

- `auth API_KEY`: store an API key for authentication.
- `login`: browser login.
- `logout`: clear stored credentials.
- `search [options] [query]`: search the current Fabric workspace.
- `path [options] [query]`: browse spaces and folders; no query lists root spaces.
- `create [options] KIND`: create `space`, `folder`, `note`, `link`, or `file` resources.
- `note [options] [content]`: create a note; reads stdin when content is omitted.
- `link [options] URL`: save a bookmark.
- `file [options] PATH`: upload a local file.
- `save [options] [input]`: smart-save a URL, local file path, text, or stdin.
- `folder [options] [name]`: create a folder, typically in Inbox unless `--parent` is supplied.
- `inbox [options]`: list Inbox items.
- `bin [options]`: list Bin items.
- `workspace list`, `workspace current`, `workspace select NAME`: inspect or choose workspaces.
- `ask [options] [question]`: ask the Fabric AI assistant a question or ask it to do something.
- `task list`, `task add`, `task done`, `task edit`, `task rm`, `task help`: manage Fabric tasks.
- `completion bash|zsh|fish`: generate shell completion.
- `help [command]`: display help.
- `subscription`: display workspace subscription, usage, and quota information.

Read `references/command-reference.md` for examples and option notes.

## Command-selection workflow

When finding information, verify workspace if it matters, use `search` for semantic/hybrid retrieval, use `path` for folders/spaces, use `--json` when parsing, and report query/tag/path/workspace limitations. Do not fabricate full item contents if the CLI returns only titles or snippets; use `ask` or another available Fabric connector if deeper content is needed.

When saving content, choose `save` when automatic type detection is enough, `note`/`link`/`file` when the user explicitly requests a type, and `create` when explicit resource control is useful. For long generated text, pipe stdin rather than placing the whole body in a shell argument. Verify by searching for a unique title, phrase, URL, or file name when useful.

When managing tasks, use `fabric task list` first when the task ID is unknown. Match by title, status, due date, and workspace. If multiple plausible tasks exist, ask the user to choose. Use ISO dates such as `YYYY-MM-DD`. Confirm before `task rm`.

When switching workspaces, record `fabric workspace current`, list workspaces if the target name may be ambiguous, run `fabric workspace select "NAME"` only when the user clearly asked or the operation requires it, then re-check current workspace before writing.

When using Fabric as agent memory, retrieve only relevant memory at the start of a task and save only when the user asks, prior instructions establish Fabric memory use, or the user has clearly opted in to persistent project memory. Save decisions, rationale, unresolved questions, next steps, relevant artefacts, and provenance. Do not save noisy transcripts or secrets.

## High-value examples

Search and browse:

```bash
fabric --json search "meeting notes"
fabric --json search "design" --tag work
fabric --json search --tag reading,todo
fabric --json path
fabric --json path "My Space"
fabric --json path "Inbox/Reports"
```

Create and save:

```bash
fabric --json create note "Meeting summary" --tag work
fabric --json create note "Q1 Review" --parent "Work/Projects"
fabric --json create folder "Projects" --tag client
fabric --json create folder "Archive" --parent "Work" --tag archive
fabric --json create folder "My Space" --parent /
fabric --json create link "https://example.com" --title "Article"
fabric --json create file "$HOME/Desktop/report.pdf"

fabric --json note "Quick reminder" --tag remember
fabric --json link "https://example.com" --title "Article" --tag reading
fabric --json file "$HOME/Downloads/report.pdf" --title "Q4 Report"
fabric --json save "https://example.com" --tag reading
fabric --json save "$HOME/Downloads/doc.pdf" --title "Report"
fabric --json save "Remember to call dentist" --tag personal
```

Save long generated text safely:

```bash
python3 scripts/fabric_memory_note.py \
  --title "Project Atlas handoff" \
  --project project-atlas \
  --summary "Decision: use the high-recall index. Next: benchmark precision." \
  --decision "Use high-recall index for nightly retrieval." \
  --next-step "Benchmark precision next week." \
  --tag handoff \
  --output /tmp/fabric-memory-note.md

fabric --json note --tag agent-memory < /tmp/fabric-memory-note.md
```

If the installed CLI supports multiple tags on note creation, add the project tag as well after checking help, for example `--tag project-atlas`.

Ask, tasks, workspaces, completion:

```bash
fabric --json ask "summarize everything tagged with project-atlas"
fabric --json task list --todo
fabric --json task add "Review PR" --priority HIGH
fabric --json task done TASK_ID
fabric --json workspace list
fabric --json workspace current
fabric workspace select "My Team"
fabric completion zsh
fabric --json subscription
```

## Available bundled resources

Use these files on demand rather than loading them all by default:

- `references/command-reference.md`: detailed command reference and official examples.
- `references/workflows.md`: repeatable agent workflows for search, save, tasks, workspaces, setup, and memory.
- `references/agent-memory.md`: how to use Fabric as persistent agent memory.
- `references/security-and-consent.md`: install, auth, secret-handling, and confirmation boundaries.
- `references/troubleshooting.md`: common failures and fixes.
- `references/sources.md`: source provenance and update notes.
- `references/v2-critical-analysis.md`: audit of v1 and rationale for v2 changes.
- `scripts/fabric_check.py`: read-only CLI/environment/account diagnostic.
- `scripts/fabric_help_cache.py`: read-only command-help capture for the installed CLI.
- `scripts/fabric_memory_note.py`: generate a redacted structured memory note.
- `scripts/fabric_command_plan.py`: build shell-quoted command plans without execution.
- `scripts/validate_skill.py`: validate this skill package during authoring.

## Final response checklist

Before replying after a Fabric CLI workflow, include the workspace used or whether it could not be verified; the command category used without exposing secrets; the created, found, updated, or uploaded item details, or the exact failure class; any uncertainty from missing auth, unsupported CLI options, ambiguous workspace/task matches, or limited output; and one concrete next step when the workflow could not be completed.
