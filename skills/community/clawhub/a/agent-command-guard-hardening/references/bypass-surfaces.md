# Bypass surfaces

A command wrapper in `PATH` is a convenience layer. State the residual surface in the same document as the guarantee; do not list only what it stops.

| Surface | Why the wrapper misses it | Can it be closed? |
|---|---|---|
| Absolute path | `/bin/rm` does not resolve through `PATH` | only by filesystem permissions or a sandbox |
| Nested shell | `bash -c 'rm ...'` invokes the real binary inside a child | no, at wrapper level |
| Interpreter one-liner | `python -c`, `node -e` call syscalls directly | no, at wrapper level |
| Non-inherited PATH | cron, launchd, systemd may use a different environment | per-service configuration |
| Symlink or renamed copy | a copy of the binary is not the wrapped name | only by path policy |
| Pipe to shell | the downloaded script runs with the shell's privileges | only by sandboxing |
| Direct syscall / library call | nothing passes through a shell | only by kernel policy |

## How to write the claim

Bad: “destructive commands are blocked.”

Good: “`rm`/`mv`/`chmod` invoked by name from an interactive shell are classified and logged; absolute-path invocation and nested interpreters remain possible and are not blocked.”

## Why logging is not optional

Blocking without logging removes the action and the evidence. Logging without blocking keeps both. If you can only get one, take logging and state that the block is not enforced.

## Escape hatches

Every interception needs a documented way to proceed, and every use must be logged as an `allow` with a reason. A guard with no escape hatch will eventually be removed entirely, taking the logging with it.
