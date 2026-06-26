# Retention Policy

Use a split retention policy so operational archives remain convenient while secrets archives stay tightly controlled.

## Recommended baseline

### Local machine
- Keep the last 14 daily backup run directories
- Keep the last 8 weekly backup run directories
- Keep the last 6 monthly backup run directories
- Keep encrypted secrets archives only as long as the matching operational archive is still in retention

### Private GitHub / cloud
- Push only the operational archive + manifest by default
- Keep the last 30 operational backup run directories or 90 days, whichever is shorter
- Never push plaintext secrets archives
- Push encrypted secrets archives only with explicit operator intent and a documented reason

## Operational rules

1. Verify each backup set before deleting older ones.
2. Do not keep standalone secrets archives after deleting their matching manifest.
3. Rotate age keys or passphrases whenever you suspect exposure.
4. Test one restore dry-run per quarter.
5. After a successful real restore, create a fresh backup set immediately.

## Suggested cleanup workflow

1. Sort backup run directories by timestamp.
2. Keep the newest sets that satisfy your daily/weekly/monthly targets.
3. Delete old run directories as a unit — operational archive, secrets archive, and manifest together.
4. Never keep orphaned manifests or orphaned secrets archives.
