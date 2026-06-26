# Backup Inventory Contract - Auto-Update

This document defines the backup ledger.

## OpenClaw Backups

For each core update, record:
- date
- version before update
- files or folders included
- backup path

## Skill Backups

For each skill update, record:
- slug
- installed version before update
- backup path
- whether restore was tested or only staged

## Retention Rule

Do not delete the newest working backup automatically.
If retention needs trimming, ask first or follow the user's explicit policy.
