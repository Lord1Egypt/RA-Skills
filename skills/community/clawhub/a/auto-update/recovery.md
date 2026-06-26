# Rollback and Recovery - Auto-Update

Freshness is not worth chaos. Recovery rules are part of the product.

## OpenClaw Recovery

If an OpenClaw update causes problems:
- restore the backed-up tailoring files first
- pin or reinstall the last known-good version if needed
- run doctor and health before calling it recovered

## Skill Recovery

If a skill update breaks behavior:
- restore the previous skill folder from backup
- mark that skill as manual or `ask-first`
- keep the migration note so the same surprise does not repeat

## Never Do This

- never delete the pre-update backup on the same run
- never call a restore complete without verifying the affected workflow
- never silently put a broken target back into auto-update
