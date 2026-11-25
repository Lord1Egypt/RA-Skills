# Adopt an exact validated candidate

Before replacing any personal app, CLI, Gateway or service, name the exact
artifact/hash/revision, targets, service owner, expected downtime and supported
rollback including state migrations. Reuse explicit approval covering these
actions; ask once for any missing scope. Use the native updater/installer with
OCM managing local environments, rather than a custom transaction around it.

After adoption, verify the actual launched executable/artifact, service owner,
live health, required plugins/tools and the requested user path. Keep the old
working artifact and recoverable state until these checks pass. Code-only
rollback may not reverse database migrations; inspect compatibility before
downgrading. Rollback retention is separate from optional disk cleanup.

Adoption is verified only when every approved component matches its validated
identity and the supported user path passes. On failure, record the actual
installation state and the supported recovery action; a successful installer
exit alone is insufficient.
