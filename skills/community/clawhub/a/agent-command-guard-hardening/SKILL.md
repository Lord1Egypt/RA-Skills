---
name: agent-command-guard-hardening
description: "Harden an agent's command interception layer safely: snapshot the baseline, test a matrix of should-block, negative-control, and known-bypass cases, verify classification rather than executing destructive commands, and document the bypass surface. Use when adding or changing guards around rm, mv, chmod, sudo, launchctl, dd, or any command wrapper. Tool-agnostic; includes a matrix runner and a bypass scanner."
license: MIT
---

# Agent Command Guard Hardening

Changing a guard is a safety change, and safety changes need evidence. This skill makes the evidence reproducible: baseline first, matrix before and after, negative controls always, bypass surface stated.

> Developed through agent operation and corrected against real failures, not hand-authored as a prompt template.

## Applicability

**Use for**
- Adding or modifying interception for destructive or privileged commands.
- A guard that is suspected of being bypassed (absolute paths, `bash -c`, interpreter one-liners).
- Proving that a new guard blocks more without blocking routine use.

**Do not use for**
- General code review.
- Replacing OS-level permissions. A wrapper is convenience and logging, not a security boundary.
- Environments where you cannot test safely; test classification, not execution.

## Boundary

Required: a place to store the baseline, a way to invoke the classifier without executing the command, and the ability to restore the previous wrapper.

Known limits:
- A wrapper in `PATH` cannot stop absolute-path invocation unless the filesystem denies it.
- Nested interpreters (`bash -c`, `python -c`, `eval`) can reconstruct any command.
- Cron and services may not inherit the modified `PATH`.
- Blocking without logging is worse than logging without blocking: you lose the evidence and keep the breakage.

**Never claim a bypass is closed when it is only narrowed.** State the residual surface.

## Step 1 — Baseline before touching anything

Snapshot, in a timestamped directory:
- the current wrapper files (byte copies),
- SHA-256 of each,
- the effective `PATH` and `which -a` for every controlled command.

**Completion criterion:** all three artefacts exist and are non-empty; the hash file covers every wrapper you will modify.

## Step 2 — Build the matrix

Three classes, all mandatory:

| Class | Purpose | Example |
|---|---|---|
| Should block | proves the guard works | `rm -rf /tmp/x`, `sudo ...`, `chmod -R 777 .` |
| Negative control | proves no over-blocking | `mv --help`, `chmod --help`, `launchctl list` |
| Known bypass | keeps you honest | absolute path invocation, `bash -c '...'`, interpreter one-liner |

A matrix without negative controls only measures enthusiasm.

**Completion criterion:** every case has an expected decision (`allow` / `deny`), and at least three negative controls exist.

## Step 3 — Classify, do not execute

The guard must expose a classification entry point, for example:

```
guard_classify <bin> <arg>...   # prints allow | deny, exit 0
```

Run the matrix against that entry point. **Never run the destructive command to “see what happens”.** Classification and execution are separate contracts.

**Completion criterion:** `scripts/matrix_run.py` produces a pass/fail line per case, with zero command execution.

## Step 4 — Implementation shape

- One shared library holds logging, real-binary resolution (skipping its own directory), deny/allow policy, and argument-level rules.
- Each wrapper is two lines: source the library, call `guard_main <bin> "$@"`.
- Argument-level rules matter: `chmod` only when `-R` or `777`; `mv` only when the source is in a protected path; `osascript` only for quit or `do shell script`.

**Completion criterion:** every wrapper has a corresponding case in the matrix.

## Step 5 — Syntax check before enabling

A wrapper with a syntax error makes the wrapped command fail silently — worse than no guard. Run the interpreter's syntax check (`bash -n`, `node --check`, `python -m py_compile`) on every modified file before it is reachable.

**Completion criterion:** syntax check passes on all modified files; a deliberate broken copy is confirmed to fail the check.

## Step 6 — Re-run the same matrix

Same cases, same classifier contract, after the change. Diff the decisions line by line. Every difference must be explained as either an intended new block or a regression to fix.

**Completion criterion:** a diff table exists; no negative control changed to `deny`.

## Step 7 — Log, document, roll back

- Log every decision as JSONL: `ts, pid, ppid, cwd, bin, argv, decision`.
- Log escape-hatch usage too (for example `GUARD_ALLOW_DESTRUCTIVE=1`, whatever the local convention is) as `allow` with a reason.
- Document the bypass surface at the level of the wrapper: absolute paths, nested interpreters, non-inherited `PATH`, direct syscalls.
- Provide rollback: restore from the byte copies; remember that rollback may itself need the escape hatch.

**Completion criterion:** a sample log line exists; the bypass list is written in the same document as the guarantee.

## Detection layer (separate from blocking)

If the goal is to record outbound actions rather than block them, do not match the whole command string. `echo 'git push'` and `pgrep -f 'git push'` will both false-positive.

1. Split on `;`, `&&`, `||`, `|`, newline.
2. Take the first token of each segment as the command name; skip `sudo`, `env`, and `VAR=` prefixes.
3. Apply argument-level rules to the remainder (`-X POST`, `--data`, `-F` for HTTP clients; `:` for rsync).
4. Self-test with positive and negative samples before enabling.

`scripts/bypass_scan.py` finds the risky invocation forms in a set of files; it is a scanner, not a blocker.

## Discipline

- Every interception needs an escape hatch, and every use of it is logged.
- Negative controls are not optional: testing only what should be blocked measures nothing.
- Do not describe a narrowed bypass as closed.
- A wrapper that silently breaks routine commands is a regression, not a hardening.

## Final self-check

1. Baseline artefacts exist and are non-empty.
2. Matrix has should-block, negative-control, and known-bypass classes.
3. Classification was tested without executing destructive commands.
4. Syntax check passed before enabling.
5. Before/after diff explained; no negative control regressed.
6. Bypass surface documented next to the guarantee.
7. Rollback procedure exists and was read by someone other than its author.
