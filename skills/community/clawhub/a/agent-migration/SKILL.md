---
name: agent-migration
description: Safely rename or migrate an OpenClaw agent by updating config and naming, migrating session content, fixing session metadata, restarting, verifying, and asking separately before deleting the old agent.
input: old agent id, new agent id, new workspace, optional model change
output: new agent active; prior session content migrated unless explicitly skipped; old agent deletion handled only after separate confirmation
---

# Agent Migration

Use this skill when the user wants to rename or migrate an OpenClaw agent safely.

## Scope
This skill handles:
- agent id rename
- workspace rename
- config/path updates
- prior session content migration
- session display metadata updates
- restart and verification
- separate deletion confirmation for the old agent

## Defaults and boundaries
- Confirm old id, new id, new workspace, and whether model also changes.
- Migrate prior session content by default unless the user explicitly says not to.
- Do not skip migration just because a session does not look active.
- Do not hard-edit active lock files or force-rewrite a live session shell.
- Restart is required after migration.
- Never delete the old agent without a separate user confirmation.

## Files involved
- config: `~/.openclaw/openclaw.json`
- agent dirs: `~/.openclaw/agents/<id>/...`
- workspace: `/home/yln/claw-workspace/<name>`
- session metadata such as `sessions.json`

## Use the included files
- `references/checklist.md`
- `references/cleanup.md`
- `scripts/inspect_agent_migration.sh`
- `scripts/copy_session_content.sh`
- `scripts/verify_agent_migration.sh`

## Recommended commands
```bash
bash skills/agent-migration/scripts/inspect_agent_migration.sh <old-id> <new-id>
bash skills/agent-migration/scripts/copy_session_content.sh <old-id> <new-id>
bash skills/agent-migration/scripts/verify_agent_migration.sh <old-id> <new-id>
```

## Guardrails
- Keep config, workspace, and naming changes consistent.
- Update session display-layer metadata as part of the migration.
- Verify the new agent before offering deletion of the old one.
- Use `references/cleanup.md` only after the user separately confirms deletion.
