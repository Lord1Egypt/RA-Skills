# claw-janitor Security Notes

## Safety boundaries

`claw-janitor` is designed to be conservative by default.

- Never follows symlinks during size scan or deletion.
- Never crosses mount/device boundaries in recursive deletion.
- Blocks sensitive paths using exact + tree blacklist rules.
- Blocks dangerous path segments like `.git`, `.env`, `.ssh`, `.kube`, `node_modules`.
- Seals current working directory tree and OpenClaw workspace tree.

## Not cleaned automatically

- Hugging Face / Ollama / Torch model caches are only scanned and reported (not auto-deleted).
- Protected directories and descendants (e.g. workspace, ssh/config trees).

## Principle

If a target is ambiguous or risky, skip it.

## Recommended usage

- Use `--dry-run` first.
- Use `--report-file` for auditing.
- Use `--only` / `--skip` to scope execution.
