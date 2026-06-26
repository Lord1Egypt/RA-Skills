---
name: emergence-deepseek-tui
description: "Use DeepSeek TUI CLI as an autonomous code assistant - two modes: `deepseek exec` (headless, text-in/text-out, no filesystem access) for delegation from another agent, and `deepseek run` (interactive, full tool-calling with filesystem) for direct coding."
version: 1.0.0
author: Emergence Science
license: MIT
metadata:
  hermes:
    tags: [deepseek-tui, coding, code-generation, multi-agent, delegation, headless-llm, cli-tools]
    related_skills: [writing-plans, plan, subagent-driven-development, systematic-debugging, test-driven-development]
---

# Emergence DeepSeek TUI

Use the **DeepSeek TUI** CLI (v0.8.16) as a code assistant from within your agent workflow. This skill teaches OpenClaw / Hermes agents how to delegate coding tasks to DeepSeek in two modes.

---

## Version

```
deepseek (npm wrapper) v0.8.16
binary version: v0.8.16
repo: https://github.com/Hmbown/DeepSeek-TUI.git
```

Install:
- **Homebrew:** `brew install hmbown/tap/deepseek-tui`
- **npm:** `npm install -g deepseek-tui`

---

## Two Modes of Operation

DeepSeek TUI has two fundamentally different modes, each with different capabilities:

| Mode | Command | Filesystem Access | Tool-Calling | Use Case |
|------|---------|-------------------|-------------|----------|
| **Headless** | `deepseek exec <PROMPT>` | ❌ No | ❌ Cannot execute tools | Delegate code gen from another agent |
| **Interactive** | `deepseek run` | ✅ Yes (via tools) | ✅ Full tool-calling | Direct coding, file editing, debugging |

### Mode 1: `deepseek exec` — Headless (Agent Delegation)

`deepseek exec <PROMPT>` calls the DeepSeek API in pure text-in/text-out mode. The model may **generate tool call syntax in its chain-of-thought output** (e.g. `<function_calls><invoke name="list_files">`), but these are never actually executed — they are only displayed as part of the model's reasoning text. No filesystem access, no tool execution.

```
┌─────────────────────────────────────┐
│  Your Agent (Hermes/OpenClaw)       │
│  ┌───────────────────────────────┐  │
│  │ 1. Read files (understand)    │  │
│  │ 2. Craft prompt with context  │  │
│  │ 3. deepseek exec "<prompt>"   │  │
│  │ 4. Validate output            │  │
│  │ 5. Apply changes              │  │
│  └───────────────────────────────┘  │
└─────────────────────────────────────┘
```

**You must provide all file context in the prompt** — DeepSeek exec is truly filesystem-blind.

### Mode 2: `deepseek run` — Interactive (Direct Coding)

`deepseek run` launches the full TUI with real tool-calling capabilities:

- `list_files` — browse directories
- `read_file` — read file contents
- `write_file` / `edit_file` — modify files
- `terminal` / `bash` — execute shell commands
- `grep` / `search` — search codebase
- And more...

When invoked from the workspace directory, it can read the entire project. Use this for direct coding sessions where you want DeepSeek to explore, edit, and build autonomously.

---

## How to Use (Headless Exec Mode)

### Step 1 — Understand the Codebase First

Read all relevant files yourself *before* invoking DeepSeek. You need to know:

- Existing patterns and conventions
- Interfaces, types, and component signatures
- Exact insertion points and file structure

DeepSeek **exec** cannot see your filesystem, so **you must provide context** in the prompt.

### Step 2 — Craft a Focused Prompt

Do NOT dump entire files. Structure your prompt like this:

```
[One-line context about the project]
[Interface of components being used]
[Example of existing usage pattern]
[Numbered change list — specific, actionable]
[Important constraints]
```

### Step 3 — Invoke DeepSeek

```bash
# Option A: pipeline from a file
deepseek exec "$(cat /path/to/prompt.txt)" 2>&1

# Option B: inline (shorter prompts)
deepseek exec "Add a blue button that says 'Click Me' to the homepage." 2>&1
```

### Step 4 — Validate the Output

DeepSeek's headless mode may display tool calls in its response **as simulated reasoning text** — ignore these. The actual output is the text content. Watch for:

| Behavior | Action |
|----------|--------|
| ✓ Returns correct code snippets | Extract from markdown blocks, apply |
| ✗ Restructures/rewrites entire files | Discard, extract only the snippets you need |
| ✗ Hallucinates interfaces or APIs | Cross-check against your own codebase context |
| ✗ Displays `<function_calls>` blocks | These are simulated reasoning, not real tool execution |

### Step 5 — Apply Changes Yourself

Use targeted file editing tools (like `patch` or `write_file`) to apply only the confirmed snippets. Never blindly trust full-file output from exec mode.

### Step 6 — Build & Verify

```bash
cd /path/to/project
npm run build  # or npx next build, cargo build, etc.
```

---

## How to Use (Interactive Run Mode)

When you want DeepSeek to explore and edit files directly:

```bash
cd /path/to/project
deepseek run
```

Or pass a goal directly:
```bash
deepseek run "Add a CommandBlock to the skills page similar to the bounties page"
```

In this mode, DeepSeek has full tool access and can read/write files, search, and execute commands autonomously. This is the mode the user discovered where "it reads all files in the current workspace."

---

## Best Practices

1. **Use `exec` for delegation, `run` for autonomy** — if you have your own tooling to read files and want tight control, use exec. If you want DeepSeek to explore and figure things out, use run.
2. **Be surgically specific** in exec mode — tell DeepSeek exact line numbers, anchor comments, and import paths
3. **Validate by building** — always compile/typecheck after applying DeepSeek's output
4. **Use targeted edits** — `patch` (find-and-replace) over writing entire files
5. **Keep prompts under 10KB** in exec mode — large prompts may degrade output quality; split across multiple calls if needed
6. **Exec mode shows tool calls as text** — do not be misled. The `<function_calls>` blocks in exec output are simulated reasoning, not real execution

## Real-World Example

In a real session, DeepSeek exec generated code to add a `CommandBlock` installation component to an Emergence Science skills detail page:

1. Read the existing bounty page to understand the `CommandBlock` pattern
2. Read the target skills page to find insertion points
3. Crafted prompt with: `CommandBlock` interface, existing usage example, exact insertion instructions
4. Ran `deepseek exec` → got confirmed import and JSX snippets (with simulated tool calls in the output)
5. Applied with `patch`, built with `npx next build` → ✅ clean

## Troubleshooting

| Problem | Fix |
|---------|-----|
| DeepSeek returns nothing (exec) | Check API key and network: `deepseek exec "hello"` |
| Output shows `<function_calls>` blocks | These are simulated reasoning, not real execution — treat as text output |
| Output is truncated | Break task into smaller prompts |
| Hallucinated code structure | Be more explicit about file paths and existing code |
| Too slow | DeepSeek V4 is fast (~2-5s per call); long responses may indicate poor prompting |
| Files not found (interactive mode) | Ensure you `cd` into the correct workspace before `deepseek run` |
