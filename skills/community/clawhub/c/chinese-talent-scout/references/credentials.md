# Credential Model

This skill is a thin wrapper around local CLIs and workspace files. It does not define or collect its own secret fields.

## What needs credentials

- GitHub collection uses the local `gh api` CLI through `@talent-scout/shared`. Authenticate GitHub access with your existing GitHub CLI login or token configuration.
- AI-assisted evaluation and identity inference call local `openclaw agent ...` commands. Model-provider credentials are expected to be configured in OpenClaw, not in this skill bundle.
- `config request` and other delivery actions call local `openclaw message send ...`. Channel accounts and routing are expected to be configured in OpenClaw and `workspace-data/talents.yaml`.

## What this skill stores

- `workspace-data/talents.yaml` stores workspace configuration such as agent names, cron definitions, and optional delivery routing.
- This skill sets `TALENT_WORKSPACE` and `TALENT_CONFIG` environment variables for its own child processes so the workspace config can be found consistently.

## What this skill does not store

- No GitHub token parsing logic exists in this package.
- No model-provider API key parsing logic exists in this package.
- No channel secret or account secret is bundled into `SKILL.md`, `scripts/`, or `references/`.

## Operator guidance

- Keep secrets in the credential stores already used by `gh` and `openclaw`.
- Treat `workspace-data/talents.yaml` as configuration, not a secret vault.
- Before sharing a workspace export, review the generated ZIP contents and remove any local-only configuration you do not want to share.
