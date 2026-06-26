# Setup - Database Manager

Use this file on first activation or whenever `~/database-manager/` is missing key files.

## Operating Attitude

- Solve the active database question first.
- Keep setup practical and short.
- Default to safe operations with explicit checkpoints.

## First Activation

1. Confirm whether the user wants local files created for persistent database operations.
2. If approved, create the base structure:

```bash
mkdir -p ~/database-manager/archive
touch ~/database-manager/{memory.md,inventory.md,standards.md,migrations.md,backups.md,incidents.md}
chmod 700 ~/database-manager
chmod 600 ~/database-manager/{memory.md,inventory.md,standards.md,migrations.md,backups.md,incidents.md}
```

3. If `memory.md` is empty, initialize it from `memory-template.md`.
4. Continue directly with the requested database planning or execution task.

## Integration Priority

Within the first natural exchanges, clarify activation boundaries:
- Always activate for schema, migration, or query performance requests.
- Activate only when the user explicitly asks for database help.
- Activate only for selected environments, systems, or projects.

Store this preference in local memory as plain-language context.

## Baseline Context to Capture

Capture context that improves future decisions:
- Main database engines and versions in use
- Critical systems and data domains
- Recovery objectives (RTO and RPO targets)
- Migration deployment windows and freeze periods
- Non-negotiable constraints (compliance, uptime, and cost limits)

If context is missing, proceed with labeled assumptions.

## Runtime Defaults

- Start with inventory clarity before proposing schema changes.
- For risky operations, build preflight and rollback plans first.
- Prefer staged rollouts over all-at-once execution.
- Escalate uncertainty by proposing a dry run before production changes.

## Optional Depth

Use additional files when needed:
- `inventory-and-governance.md` for ownership and data criticality mapping
- `query-operations.md` for query review and lock-risk checks
- `migration-and-release.md` for deployment and rollback sequencing
- `backup-and-recovery.md` for restore drill design and evidence tracking
- `incident-playbook.md` for incident timeline and mitigation order
- `templates.md` for reusable runbooks and checklists
