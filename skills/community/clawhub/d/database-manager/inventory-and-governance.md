# Inventory and Governance

Use this file to keep ownership and blast-radius context explicit before major database work.

## Minimum Inventory Model

Track each system with:
- service or product name
- database engine and major version
- environment scope (dev, staging, prod)
- primary data owner
- backup owner
- incident escalation owner

Without ownership fields, incident response becomes slower and ambiguous.

## Data Criticality Tiers

Classify major datasets into one of these tiers:
- Tier 1: business-critical and customer-facing
- Tier 2: important but degradable for short windows
- Tier 3: internal analytics or recoverable convenience data

Use tier to set migration caution level and recovery urgency.

## Change Windows

Define allowed windows by environment:
- production: pre-approved windows only
- staging: flexible, but still documented
- development: unrestricted with local safeguards

When no window is declared, treat change as blocked.

## Ownership Checklist Before Execution

Before approving any high-impact operation, verify:
- technical owner is named
- business owner is named for Tier 1 data
- rollback approver is named
- communication channel is confirmed

## Governance Drift Signals

Investigate immediately when any pattern appears:
- new tables without owner mapping
- recurring emergency migrations
- backups lacking tested restore evidence
- schema documentation older than one quarter

Governance drift usually predicts reliability incidents within the next release cycles.
