# Skill Ledger Contract - Auto-Update

This document defines what belongs in the per-skill ledger.

## Every Skill Entry Needs

- slug
- install location
- installed version
- auto-update policy: yes, no, or inherit
- last backup path or date
- migration state: clean, pending, or ask-first

## Install-Time Questions

When a new skill lands, ask:
1. Do you want a quick explanation of what this skill adds?
2. Should this skill auto-update with the rest, stay manual, or simply inherit your default?

Then write the answer once so later sessions do not have to guess.

## Migration State Meaning

- `clean` - no known migration risk
- `pending` - review needed before or right after update
- `ask-first` - user wants explicit approval every time
