# Private Adaptation Notes

This note explains how to adapt the public/generalized skill for a private company-specific version.

## Public version should keep
- generalized B2B CRM/admin positioning
- Ant Design-oriented structure and tokens
- page taxonomy
- prompt templates
- implementation-friendly guidance

## Private version can add back
- company-specific page naming
- internal menu structures
- internal URL patterns
- organization hierarchy assumptions
- team-specific tone or component constraints
- known product modules and their design templates

## Recommended pattern

Maintain two layers:

### Layer 1 — public skill
- reusable
- generalized
- safe for sharing or publishing

### Layer 2 — private adaptation docs
- company-specific
- internal-only
- built on top of the public skill

## Why this matters

This keeps the reusable design logic stable while preventing leakage of internal system structure or product details.
