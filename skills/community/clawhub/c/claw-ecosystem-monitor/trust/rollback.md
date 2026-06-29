# Rollback

This prototype has no remote side effects.

Rollback steps:

1. Delete generated snapshots under `data/YYYY-MM-DD/`.
2. Stop scheduled runs, if any were later added.
3. Remove any future public link or ClawHub listing.
4. If a source sends a warning or policy objection, pause that source and keep only the incident note needed for audit.

No payment or hosted-service rollback is required because this skill has no paid surface and no hosted backend.
