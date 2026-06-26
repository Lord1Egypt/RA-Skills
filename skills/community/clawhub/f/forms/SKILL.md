---
name: Forms
slug: forms
version: 1.0.0
description: Create, validate, and deploy forms with field types, validation patterns, conditional logic, and platform integrations.
metadata: {"clawdbot":{"emoji":"📝","requires":{"bins":[]},"os":["linux","darwin","win32"]}}
---

## Quick Reference

| Topic | File |
|-------|------|
| Field types by use case | `types.md` |
| Platform comparisons | `platforms.md` |
| Code generation (React, Flutter) | `code.md` |
| Validation patterns | `validation.md` |
| Integrations (webhooks, CRMs) | `integrations.md` |
| Self-hosted options | `selfhosted.md` |

## User Profile

<!-- Edit to customize form suggestions -->

### Preferred Stack
<!-- react | flutter | vue | html | no-code -->

### Primary Use Case
<!-- leads | surveys | applications | feedback | registration -->

### Default Platform
<!-- google-forms | typeform | tally | heyform | code-only -->

## Data Storage

Store form definitions and templates in ~/forms/:
- templates — Reusable form definitions (JSON/YAML)
- submissions — Collected responses (if self-hosted)
- feedback — What converts well, what fails

## Core Rules

- Ask use case before suggesting fields — lead form ≠ application form
- Progressive disclosure: start minimal, reveal complexity if needed
- Mobile-first: every form must work on phone
- Never more than 7 fields for lead capture — each field drops conversion ~10%
- Multi-step > single long form for 5+ fields
- Validate on blur, not just submit — immediate feedback
- Always include: clear labels, error states, success confirmation
- GDPR checkbox mandatory for EU — link to privacy policy
- Honeypot over CAPTCHA when possible — less friction
- File uploads need type + size limits — prevent abuse
- Conditional logic syntax: `IF field=value THEN show/hide field`
- Test on real devices — emulators miss keyboard quirks
