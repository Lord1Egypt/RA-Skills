# Session Search

Searches past sessions by keyword and returns matching session IDs, with validation to prevent false positives.

## When to Use

- Finding a past session that touched a specific topic, file, or feature
- Locating where a particular task was discussed, planned, or executed
- Cross-referencing earlier work before starting a related task

## Invocation

```bash
/session search <keyword>                  # search current project sessions
/session search --today <keyword>          # only sessions modified today
/session search --project <path> <keyword> # search a specific project path
```

For backward compatibility, `/session id <keyword>` is routed to this topic.

## Search Procedure

1. Determine project JSONL directory (`~/.claude/projects/{project_name}/`)
2. Grep JSONL files for keyword — matches user messages (`"type":"user"`) + file paths
3. Sort results by modification time descending
4. Run **Result Validation** (below) before reporting

```bash
# Project JSONL path
PROJECT_DIR=~/.claude/projects/{project_name}

# Keyword search (matches both user messages and file paths)
# stat mtime: GNU `stat -c %Y` (Linux), BSD `stat -f %m` (macOS) — fall back across both
grep -l "<keyword>" "$PROJECT_DIR"/*.jsonl | while read f; do
  ts=$(stat -c %Y "$f" 2>/dev/null || stat -f %m "$f")
  sid=$(basename "$f" .jsonl)
  echo "$ts $sid"
done | sort -rn | head -5
```

## Restricting Search Scope (Skill Procedure)

These are not script flags — they are implemented by the skill at invocation time:

- `--today`: Filter results to sessions modified today (skill uses `find -newer`)
- `--project <path>`: Specify a particular project path (skill overrides CWD-based detection)

## Output Format

```text
03-26 11:28 | a6aea9f3-3376-4cf3-be6f-33a7122ab283
03-25 10:02 | e972a8b7-da04-4b9f-8d26-fad0350a2e09
```

## Result Validation Before Reporting (HARD STOP)

A keyword match alone does NOT prove "task X was performed in this session." Before reporting matches, run these checks:

### Verb ambiguity check

Phrases like "the session that installed X", "the session that did X" can mean (a) the session where the action was actually executed, (b) the session where the action was planned or documented, or (c) the session where the keyword merely appeared. If the verb is ambiguous, ask the user before returning a single answer — match strength does not justify guessing intent.

### Artifact location check

For each matched session, extract `file_path` from `Write`/`Edit` tool inputs. Compare the path against where the project actually stores that kind of artifact (its documented convention, the rest of the repo's existing files of the same type, or the path the user later moved the file to). If the matched session wrote the artifact somewhere else, surface that mismatch in the report instead of treating the match as proof of completion. Prefix the line with `⚠️` and show both the path that was used and the path the artifact normally lives at.

A misplaced artifact often means a downstream consumer (autonomous agent loop, CI job, sync process) never saw the work and the follow-up never happened. Treat a path mismatch as a likely "task orphaned" signal, not just a cosmetic issue, and check whether any later session actually picked the task up.

### Action class classification

Classify each match as one of:

- **Executed** — the keyword appears inside a tool input that actually performed the action (`Bash` running the relevant command, network calls, service control, etc.)
- **Planned** — the keyword appears only inside `Write`/`Edit` tool inputs that produced plan/research documents
- **Mentioned** — the keyword appears only in user messages or file content snippets, with no related tool execution

Report the class alongside the session ID so the caller can pick the right one.

### When validation is inconclusive

If the top match falls into the "artifact location mismatch" or "ambiguous verb" categories, do NOT collapse the answer to a single session. Return a classified candidate list and ask the user to confirm which interpretation matches their intent.

## Usage Examples

```bash
/session search Makefile remove          # find sessions touching Makefile removal
/session search --today ansible/Makefile # today's sessions referencing that file path
/session id Makefile remove              # legacy alias — routed here for compatibility
```
