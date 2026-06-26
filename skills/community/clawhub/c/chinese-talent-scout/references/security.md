# Security Notes

This skill is designed to orchestrate local tooling with explicit boundaries.

## Data flow

- `collect` reads GitHub data through the local `gh` CLI and writes normalized outputs under `workspace-data/output/`.
- `process` and `evaluate` read local workspace files and may call OpenClaw agents for AI-assisted steps.
- `query` reads local processed/evaluated data and prints text output only.
- `export workspace` writes a local ZIP archive and returns its local path. It does not upload the archive.
- `config request` sends a text message through `openclaw message send` that references `workspace-data/talents.yaml` and the requested change. It avoids absolute local filesystem paths.

## Safety boundaries

- The skill is not always-on and does not request elevated platform privileges.
- Runtime file writes are scoped to the selected workspace directory.
- This skill does not modify other installed skills.
- Cron management only acts on jobs defined in the current workspace config and removes orphaned jobs with the `talent-` prefix.

## Audit checklist

- Review `packages/shared/src/github.ts` for GitHub network calls.
- Review `packages/shared/src/openclaw.ts` for OpenClaw agent, message, and cron commands.
- Use `scripts/talent-scout.sh config request --dry-run ...` to inspect delivery payloads before enabling a real channel target.
- Use a test workspace and non-production OpenClaw accounts when evaluating the skill for the first time.

## Trust signals for reviewers

- The skill is published as a self-contained bundle whose directory name matches the `name` field in `SKILL.md`.
- The published bundle includes only the runtime CLI, references, and configuration template needed by the skill.
- Credential handling is delegated to existing local CLIs instead of being reimplemented inside the skill.
