---
name: agentic_cli_coding
description: "Use this skill for any task that involves reading, understanding, searching, or modifying source code in a project — across JavaScript, TypeScript, Vue, React, Node, Python, Go, Ruby, PHP, Java, Rust, C/C++, shell scripts, JSON, YAML, HTML, CSS, SQL, and Markdown. Trigger whenever the user asks to fix a bug, add a feature, refactor, rename, restructure, search a codebase, locate a function or symbol, apply a patch, modify configuration, or make any multi-file change. Also use when the user references files by path or name and wants something done to them, when reviewing or auditing code, or when planning an edit before making it. Provides the `oce` command — a unified, validation-aware, transaction-capable editing toolkit that backs up every change and rolls back on syntax failure. Prefer `oce` over raw sed/awk/perl-i for any persistent edit; those are read-only here."
---

# Agentic CLI Coding

A code-editing toolkit for agents. Provides the `oce` command, which wraps reads, searches, edits, validation, formatting, backups, and multi-file transactions behind one predictable interface that always validates after writing and rolls back on syntax failure.

This skill exists because raw `sed`, `awk`, and `perl -i` are too sharp for autonomous use — they apply changes silently, give regex-style false matches, leave no audit trail, and can't roll back. `oce` keeps the speed of CLI editing while adding the safety rails an agent needs.

---

## Invocation — `oce` shorthand

Throughout this document, the command `oce <subcommand>` is shown for readability. The actual invocation is one of:

```bash
# Option A — direct (works immediately, no setup):
bash <skill-path>/scripts/oce.sh <subcommand> [args]

# Option B — one-time alias for the session (recommended for agents):
alias oce="bash <skill-path>/scripts/oce.sh"

# Option C — install a wrapper on PATH (persistent):
bash <skill-path>/scripts/install.sh
```

For agentic use, set up the alias once at the top of any session that involves editing, then use `oce <subcommand>` for the rest of the session. Replace `<skill-path>` with the actual install location of the skill (often something like `/home/agent/.skills/agentic_cli_coding`).

---

## Setup verification

After setting up the alias (or installing), run this once at the start of any editing session:

```bash
oce doctor
```

Exit code 0 with `Setup OK` means the toolkit is ready. The "core tools" must all be present (node, patch, diff, grep, acorn). Missing optional tools (prettier, gofmt, etc.) only affect formatting for that language — editing still works.

If you see `oce: command not found`, the alias wasn't set or the install wrapper isn't on PATH. Use Option A (direct invocation) instead.

---

## Methodology — how to approach any code task

Skip directly to the relevant step if the user's task is simple. For anything non-trivial, walk through all four.

### 1. Orient — understand the project

Before editing, know what you're editing.

```bash
oce tree --depth 2                  # What's in this project?
oce find "<keyword>" --type <lang>  # Where does the relevant code live?
oce ast symbols path/to/file.js     # What functions/classes does that file define?
```

Don't skip orientation just because you "know" the answer from training. Repository conventions vary; assumptions are how agents break codebases.

### 2. Read — load the exact context you'll need

```bash
oce read src/server.js --around "handleAuth" --context 20
oce grep-context "TODO" src/server.js -c 5
oce read src/auth.js --lines 45:120
```

Read enough surrounding context that you can predict what your edit will affect. The cheapest way to break code is to edit a function in isolation without seeing its callers.

### 3. Plan — write down what you'll change before changing anything

For non-trivial edits, state the plan explicitly before executing:

- **What's being added** (new lines, new files)
- **What's being removed** (deletions, deprecations)
- **What's being modified** (in-place changes)
- **What's at risk** (files that touch the same symbols, public APIs, tests)
- **What you'll validate** (which files need to compile, which tests should still pass)

If the change spans multiple files, **start a transaction** before the first edit:

```bash
TXN=$(oce transaction begin)
```

Then pass `--txn "$TXN"` to every subsequent `oce replace`, `oce insert`, `oce delete`, `oce write`, `oce patch`, or `oce ast` command. At the end you commit (validates everything atomically) or roll back (restores every file).

### 4. Execute — pick the right edit tool, then verify

The decision flow:

```
Need to change code?
├── Tiny, surgical, exact-string change         → oce replace
├── Insert new code at a known anchor           → oce insert --before-match | --after-match | --line
├── Remove specific lines or matching lines     → oce delete --lines | --match
├── Multi-line precision change with context    → oce patch apply  (write a unified diff)
├── Rename a JS/JSX identifier scope-wide       → oce ast rename
├── Replace an entire function/class body       → oce ast replace-symbol
├── Brand-new file or full rewrite              → oce write
└── Coordinated changes across multiple files   → oce transaction + any of the above
```

After every edit, the toolkit auto-validates the file's syntax and rolls back if it broke. You don't need to re-validate manually, but you should `oce diff <file>` to confirm the change matches your intent.

---

## Decision tree — which command for which job

```
DISCOVERY                            READING
────────────────                     ────────────────
project layout?       tree           full file?         read <file>
where is X?           find           specific lines?    read <file> --lines A:B
function/class list?  ast symbols    context around X?  read <file> --around X -c N
match in context?     grep-context   match with ctx?    grep-context X file -c N

EDITING (small)                      EDITING (large / structural)
────────────────                     ────────────────
exact string swap     replace        full file rewrite        write
insert at anchor      insert         apply unified diff       patch apply
delete lines/matches  delete         rename symbol (JS/JSX)   ast rename
                                     replace function body    ast replace-symbol

VERIFY & RECOVER
────────────────
syntax check          validate       (auto-runs after every edit)
canonical format      format         (manual)
view recent change    diff           (vs last backup)
list backups          backup list
restore               backup restore <file> [--at N]

MULTI-FILE ATOMIC
────────────────
TXN=$(oce transaction begin)
oce <edit> ... --txn "$TXN"   (repeat)
oce transaction validate "$TXN"
oce transaction commit "$TXN"   |   oce transaction rollback "$TXN"
```

---

## Standard workflows

### Modifying an existing function (single file)

```bash
oce find "function processRequest" --type js
oce read src/server.js --around "processRequest" --context 15
oce replace src/server.js \
  --old "return data;" \
  --new "return sanitize(data);"
oce diff src/server.js
```

### Adding a new code block at a known anchor

```bash
oce find "// END ROUTES" src/server.js
cat > /tmp/new_route.js <<'EOF'
app.get('/health', (req, res) => res.json({ ok: true }));
EOF
oce insert src/server.js --before-match "// END ROUTES" --content-file /tmp/new_route.js
```

### Multi-file rename / refactor

```bash
TXN=$(oce transaction begin)
oce replace src/auth.js --old "validateToken" --new "verifyToken" --all --txn "$TXN"
oce replace src/api.js  --old "validateToken" --new "verifyToken" --all --txn "$TXN"
oce replace tests/auth.test.js --old "validateToken" --new "verifyToken" --all --txn "$TXN"
oce transaction validate "$TXN"
oce transaction commit "$TXN"   # or rollback if anything looks wrong
```

For pure JS/JSX, `oce ast rename` is preferable — it walks the AST and only renames real identifier references, not strings or comments.

### Precise multi-line patch

When you need exact control over a multi-line change, write a unified diff:

```bash
cat > /tmp/fix.patch <<'EOF'
--- a/src/auth.js
+++ b/src/auth.js
@@ -12,6 +12,10 @@
 function authenticate(req) {
+  if (!req.headers.authorization) {
+    throw new Error('Missing auth header');
+  }
   const token = req.headers.authorization.split(' ')[1];
EOF

oce patch apply /tmp/fix.patch
```

The patch is dry-run-checked first; if it doesn't apply cleanly the command fails before touching anything. After applying, every affected file is validated and the entire patch is rolled back if any file's syntax broke.

### Recovering from a bad edit

```bash
oce backup list <file>           # See available snapshots
oce backup diff <file>           # Compare current vs. most recent backup
oce backup restore <file>        # Restore most recent backup
oce backup restore <file> --at 3 # Restore the 4th-most-recent (0-indexed)
```

Backups are auto-created before every destructive operation. They live in `.oce/backups/` in the workspace.

---

## Anti-patterns — never do these

These are the failure modes that bite agents most often. Internalize them.

**Do not use `sed -i`, `awk` redirected to the same file, or `perl -i`** for editing. They give zero validation, no backup, and silent partial-success on regex misses. Use `oce replace` (literal match) or `oce patch` (precise) instead.

**Do not use `oce write` to make small edits.** `write` replaces the entire file. If you only need to change three lines, use `replace`, `patch`, or `insert`. Full rewrites are reserved for new files or when you've already loaded and modified the entire file's content programmatically.

**Do not pass a non-unique `--old` to `oce replace` without `--all`.** The command will fail with an "ambiguous match" error — that's by design. Either make `--old` more specific (include surrounding context like an indent or a closing brace) or pass `--all` if you genuinely want every occurrence changed.

**Do not edit multiple files for a single logical change without a transaction.** If file 2's edit fails validation, file 1 is now in an inconsistent state. `transaction begin` + `--txn` + `commit`/`rollback` keeps everything atomic.

**Do not skip `oce diff` after a non-trivial edit.** It takes one command and tells you whether the change matches your mental model. The auto-validation only catches syntax errors, not logic errors.

**Do not assume a formatter ran.** `oce format` only runs if the formatter is installed. Check `oce doctor` output if you care.

**Do not edit binary files.** `oce` refuses by default; if you find yourself reaching for `OCE_MAX_FILE_SIZE` overrides or trying to bypass the binary check, stop and reconsider.

**Do not invent file paths.** Always confirm a file exists with `oce read` or `oce tree` before editing it. The toolkit will fail loudly on missing files, but the better habit is checking first.

---

## Output format — `--json` for programmatic parsing

Every command supports `--json`, which emits a single-line JSON object on stdout (or stderr for errors). Use this when chaining commands or parsing results.

Quick reference (full schema in `references/json-schema.md`):

```json
// Success
{"status":"success", "file":"src/x.js", "replacements":3, "backup":"/path/to/backup"}

// Error
{"status":"error", "message":"Found 5 matches; pass --all or make --old more unique"}

// Dry run
{"status":"dry_run", "file":"src/x.js", "matches":3, "message":"would replace 3 occurrence(s)"}

// Validation
{"status":"success", "file":"src/x.js", "language":"javascript", "validator":"node --check", "valid":true, "output":""}
```

For ambiguous results (find with many hits, ast symbols), the JSON includes a `matches` or `symbols` array.

---

## Global flags

These work on every command:

| Flag | Effect |
|---|---|
| `--json` | Emit machine-readable JSON instead of human text |
| `--dry-run` | Show what would happen, change nothing (writes only) |
| `--no-color` | Disable ANSI colors |
| `--txn <id>` | Register backups with a transaction (write commands only) |

---

## Language support summary

`oce` knows about and handles edits for files in: JavaScript (.js .mjs .cjs .jsx), TypeScript (.ts .tsx), Vue (.vue), Svelte (.svelte), Python (.py), Ruby (.rb), Go (.go), Rust (.rs), Java (.java), Kotlin (.kt), Swift (.swift), C/C++ (.c .h .cpp .hpp), C# (.cs), PHP (.php), Bash/Zsh (.sh .bash .zsh), JSON, YAML, TOML, XML, HTML, CSS/SCSS/LESS, Markdown, SQL, Dockerfile, Makefile.

Validation depth varies by what's installed locally. See `references/language-support.md` for the full matrix.

AST-level operations (`oce ast`) are JS/JSX-native (acorn parses them directly). On TypeScript files, AST commands work for the JS-compatible subset — for full TS support, install local `tsc`. For other languages, use text-based edits (`replace`, `patch`).

---

## Storage and state

The skill writes nothing to your home directory. All state lives in `.oce/` inside the current working directory:

```
<project>/.oce/
├── backups/         Snapshot of every file before destructive edit
├── transactions/    Active and historical transactions
└── edit.log         Audit log of every edit
```

You can safely add `.oce/` to `.gitignore`. To clean up, `oce backup clean [DAYS]` removes backups older than DAYS (default 30).

---

## Reference material

For deeper docs, read these as needed:

- **`references/json-schema.md`** — Exact JSON output schema for every command. Read this when chaining commands or parsing output programmatically.
- **`references/workflows.md`** — Longer worked examples: bug fix flow, feature add flow, refactor flow, dependency upgrade flow, Vue/React component editing.
- **`references/language-support.md`** — Per-language validator and formatter matrix; what works without extra installs, what needs project-local tooling.
- **`references/troubleshooting.md`** — Symptom → cause → fix table for the failure modes you'll hit in practice.

---

## One-line summary

`oce <verb> <file> [options]` — every verb backs up first, validates after, and rolls back on syntax failure. Use transactions for multi-file changes. Read before you write. Plan before you execute.
