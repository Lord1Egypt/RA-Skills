---
name: codewiki
description: |
  Trigger a one-shot workflow that clones (or pulls) a Git repository,
  generates a structured wiki from it using the `codewiki` CLI, and
  optionally renders the result into static MkDocs / VitePress sites with
  an HTTP preview. Use this skill whenever the user asks to "generate a
  wiki", "document this repo", "create a code wiki", or invokes
  `/codewiki <input>`.
dependencies:
  - name: CodeWiki
    url: https://github.com/FSoft-AI4Code/CodeWiki
    required: true
    binary: codewiki
---

# Skill: `codewiki`

## When to trigger

Invoke this skill when the user:

- Types `/codewiki <input>`, **or**
- Asks in natural language to generate a wiki / documentation from a repository
  (e.g. *"generate a wiki for anthropics/claude-code"*).

## Trigger command

```
/codewiki <user_input>
```

## Dependencies

This skill depends on **[CodeWiki](https://github.com/FSoft-AI4Code/CodeWiki)**
(`FSoft-AI4Code/CodeWiki`). The `codewiki` CLI — provided by that project —
must be installed and available on `$PATH` before the underlying script can
run. The script's startup `check_dependencies` step will fail with exit code
`2` and a clear message if `codewiki` is missing.

If the user has not installed CodeWiki yet, direct them to
<https://github.com/FSoft-AI4Code/CodeWiki> and have them follow the install
instructions there **before** confirming execution.

When the user requests rendering (`--render`), two additional host tools are
required: `python3` (MkDocs) and `node` + `npm` (VitePress). The
per-renderer dependencies are installed automatically into isolated
sandboxes (Python venv / private `node_modules`) at render time, so the user
never needs to run `pip install` or `npm install` manually. If either host
tool is missing, `render_docs.sh` exits with a friendly install hint.

## Agent execution logic

Follow these steps in order. Do **not** execute the underlying script until
the user has explicitly confirmed.

### 1. Parse `<user_input>`

Extract five fields from the user's input. Accept natural-language phrasing
and shorthand.

| Field        | Required | Accepted forms                                              | Default  |
|--------------|----------|------------------------------------------------------------|----------|
| repository   | yes      | `group/repo`, `https://github.com/...`, `git@github.com:...` | —        |
| output dir   | no       | any local path                                              | `.`      |
| instructions | no       | free-form text describing focus / constraints               | (none)   |
| render stack | no       | `mkdocs`, `vitepress`, `both`, or "skip"                    | skip     |
| serve        | no       | boolean, optionally with a port number                      | off      |

Detection heuristics:

- **repository**: the first token matching `^\w[\w.-]*/[\w.-]+$`, or starting
  with `https://` or `git@`.
- **output dir**: a token following words like `into`, `to`, `under`, `at`,
  or a path-looking token (`./`, `/`, or containing `/`).
- **instructions**: everything remaining after repository and output are
  removed. Treat quoted strings as a single instruction block.
- **render stack**: triggered by keywords like `render`, `mkdocs`,
  `vitepress`, `build site`, `static site`. Map `mkdocs` / `vitepress` /
  `both` directly. The word "render" alone (without a named stack) should
  be clarified with the user before defaulting — do **not** silently pick a
  stack.
- **serve**: triggered by `serve`, `preview`, `open in browser`,
  `live preview`. If a port number appears nearby (e.g. "on 3000"), use it;
  otherwise omit the port and let `render_docs.sh` default to 8000. Serving
  implies `--render` is also set — if `--serve` is requested but no stack is
  named, ask the user which stack to render.

### 2. Present a structured confirmation overview

Render the parsed options back to the user in a compact block before doing
anything. Example:

```
╭─ codewiki — parameters ──────────────────────────────╮
│ Repository   : anthropics/claude-code                │
│   (expanded) : https://github.com/anthropics/        │
│                claude-code.git                       │
│ Output dir   : .                                     │
│ Instructions : "Focus on the auth module; skip       │
│                vendored code."                       │
│ Render stack : both                                  │
│ Serve        : on, port 3000                         │
╰──────────────────────────────────────────────────────╯
```

If a field was inferred from natural language (not stated literally), mark it
with `(inferred)` so the user can correct it. If `Serve` is on, always show
the URLs that will be served (`http://localhost:PORT` for mkdocs,
`http://localhost:PORT+1` for vitepress when `--render both`) so the user
knows what to expect.

### 3. Prompt for confirmation or modification (STRICT)

Present exactly two actionable paths. Do not run the script yet.

> **Confirm to execute, or tell me what to change.**
>
> - Reply `yes` / `confirm` / `go` → I will run:
>   ```bash
>   ./scripts/codewiki.sh -r anthropics/claude-code \
>               -o . \
>               -i "Focus on the auth module; skip vendored code." \
>               --render both \
>               --serve 3000
>   ```
> - Reply `modify: <field> = <value>` → I will update the parameter table
>   and re-prompt.
> - Reply `cancel` → abort without side effects.

### 4. Execute (only after confirmation)

Run the underlying script with the exact flags agreed above. Stream its
output to the conversation. On completion, report:

- The path to the generated wiki (typically `<output>/<repo>/wiki`).
- The paths to any rendered static sites
  (`<output>/<repo>/mkdocs/site`, `<output>/<repo>/vitepress/site`).
- The preview URLs if `--serve` was used.
- Any warnings from `codewiki` or `render_docs.sh` worth the user's
  attention.

If `--serve` was used, the script blocks in the foreground serving HTTP.
Tell the user explicitly to press `Ctrl-C` when done previewing — the
cleanup trap will tear down the server(s) automatically.

## Hard rules

- **Never** run `codewiki.sh` before the user confirms. This skill clones
  remote repositories — that is a side effect with network and disk cost.
  Rendering and serving add further disk and long-running process side
  effects.
- **Never** invent a repository when none was provided. If parsing yields no
  repository, ask the user for one.
- **Never** silently pick a render stack. If the user says "render" but
  does not name `mkdocs` / `vitepress` / `both`, ask which stack they want.
- **Never** start `--serve` without `--render`. The script will reject this
  with exit code 1, but call it out during parsing so the user is not
  surprised.
- **Always** show the expanded clone URL when the user supplied a shorthand
  `group/repo` form, so they can verify the target before cloning.
- **Always** show which ports will be opened when `--serve` is used.
- **Preserve** instruction text verbatim. Do not reword, summarize, or trim
  it before passing it to `-i`.
