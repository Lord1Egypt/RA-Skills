# Fabric.so CLI workflow playbook

This file provides repeatable workflows for agents using the Fabric.so CLI. Use it when the user asks for a multi-step outcome rather than a single command.

## Workflow 1: diagnose setup and readiness

Use when the user says the CLI is broken, asks to install/login, or wants to know whether their terminal is ready.

1. Run local read-only checks:

```bash
python3 scripts/fabric_check.py --json
```

2. If `status` is `not_installed`, do not install automatically unless the user explicitly requested installation. Explain the official installer and suggest reviewing it first.

3. If the CLI exists and the user wants live Fabric access, run deeper read-only checks:

```bash
python3 scripts/fabric_check.py --deep --json
```

4. Classify the failure: missing binary/PATH, wrong tool, CLI help/version failure, authentication problem, workspace selection problem, network issue, or quota issue.

5. Provide the smallest safe next command, such as `fabric login`, `fabric workspace current`, `fabric workspace list`, or `fabric --json subscription`.

## Workflow 2: search Fabric and answer from results

Use when the user wants to retrieve notes, files, links, decisions, meeting notes, saved research, or project memory.

1. Determine query terms, tags, and workspace.
2. Verify current workspace if workspace matters.
3. Search broadly first: `fabric --json search "QUERY"`.
4. Narrow by tag or folder/path if helpful.
5. Summarise results with provenance: query, tags, workspace, item titles, paths, URLs if returned, and limitations.
6. If CLI results only include snippets/titles and the user asks for exact content, use `fabric ask` or another available Fabric connector if appropriate. Do not invent missing item bodies.

## Workflow 3: save a note, URL, or file

Use when the user asks to save, capture, upload, bookmark, or persist content.

1. Identify the content type: URL (`link` or `save`), local path (`file` or `save`), text/memory (`note` or `save`), or ambiguous (`save`).
2. Check workspace before writes when relevant: `fabric --json workspace current`.
3. For files, check local existence first: `test -f "$PATH"`.
4. Use safe command patterns:

```bash
fabric --json link "https://example.com" --title "Article" --tag reading
fabric --json file "$HOME/Downloads/report.pdf" --title "Q4 Report" --parent "Work/Reports"
fabric --json save "Remember to call dentist" --tag personal
```

5. For long text, write to a temp file or pipe stdin:

```bash
fabric --json note --tag agent-memory < /tmp/note.md
```

6. Verify if useful by searching for a unique phrase. Report workspace, title/path/tag, and any verification result.

## Workflow 4: create folders or organise locations

Use when the user asks to create spaces/folders or place content under a path.

1. Browse parent path: `fabric --json path "Work"`.
2. Create missing folder only when requested or necessary for the requested write.
3. Do not move or delete existing items unless explicitly requested and confirmed if destructive.
4. Verify with `fabric path "Parent/Child"`.

## Workflow 5: manage tasks

Creating a task:

```bash
fabric --json task add "Task title" --due-date 2026-04-20
fabric --json task add "Review PR" --priority HIGH
```

Completing or editing a task when ID is unknown:

1. List tasks: `fabric --json task list --todo`.
2. Match the candidate task by title, status, due date, workspace, or context.
3. If exactly one candidate is found, run `fabric --json task done "$TASK_ID"`.
4. If multiple candidates match, ask which one. Do not invent IDs.
5. For deletion, ask for explicit confirmation before `fabric --json task rm "$TASK_ID"`.

## Workflow 6: temporary workspace switch

1. Record current workspace: `fabric --json workspace current`.
2. List workspaces if the name is not exact: `fabric --json workspace list`.
3. Select: `fabric workspace select "My Team"`.
4. Re-check: `fabric --json workspace current`.
5. Perform the requested operation.
6. If the user asked for a temporary switch, restore the original workspace and report both changes.

## Workflow 7: use Fabric as agent memory

At task start:

```bash
fabric --json search "project-atlas agent-memory" --tag agent-memory
fabric --json search "project-atlas decision" --tag decision-log
```

During the task, keep memory candidates concise. Do not dump many irrelevant results into context.

At task end, only if opted in, generate and review a structured memory note:

```bash
python3 scripts/fabric_memory_note.py \
  --title "Project Atlas session handoff" \
  --project project-atlas \
  --summary-file /tmp/session-summary.txt \
  --decision "Use high-recall index for nightly retrieval." \
  --next-step "Benchmark precision next week." \
  --tag handoff \
  --output /tmp/fabric-memory.md

fabric --json note --tag agent-memory < /tmp/fabric-memory.md
```

Save only future-useful information, not raw transcripts. If installed help supports multiple tags for creation, add project and category tags.

## Workflow 8: shell completion

Generate completion scripts on request:

```bash
fabric completion bash
fabric completion zsh
fabric completion fish
```

If the user wants installation into their shell configuration, treat that as a local file modification. Inspect the target file path, append carefully, and preserve a backup.

## Workflow 9: ask Fabric assistant vs search

Use `search` when the agent needs candidates, paths, IDs, result metadata, deterministic provenance, parsing, filtering, or choosing items.

Use `ask` when the user wants a natural-language answer over Fabric context, asks Fabric's assistant to summarise/find/act, or CLI search cannot expose enough item content.
