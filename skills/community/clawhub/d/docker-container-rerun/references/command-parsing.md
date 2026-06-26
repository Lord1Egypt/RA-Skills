# Command Parsing Notes

Use these rules when extracting the image from `recreate_command`.

## Goal

Identify the image reference from a valid `docker run` command without rewriting the command.

## Practical Rules

- The command must begin with `docker run`.
- Docker options appear before the image.
- The image is the first non-option token after all `docker run` flags are consumed.
- Anything after the image belongs to the container command/args and must be preserved.

## Important Caveat

Shell parsing is tricky when users include quoting, line continuations, environment expansion, or embedded shell commands.

If extraction is not fully reliable from plain inspection, do one of these:

1. ask the user to confirm the image embedded in the recreate command, or
2. use a shell-safe parser/script before execution.

## What Not to Do

- Do not reorder flags.
- Do not normalize quoting unless required for execution by the shell.
- Do not infer missing options from `docker inspect`.
- Do not swap the image tag automatically.

## Safe Mental Model

Treat the provided `recreate_command` as immutable execution input. Extract only enough information to compare and pull the image; then execute the original command exactly as given.
