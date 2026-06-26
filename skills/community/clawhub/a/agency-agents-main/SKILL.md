---
name: agency
description: The Agency - AI role switcher. Activate specialized professional roles (frontend developer, sales agent, marketing specialist, etc.) for different tasks. Use when user says "switch to [role]", "activate [role] mode", "become [role]", or wants to work in a specific professional persona.
metadata:
  {
    "openclaw": { "emoji": "🎭" },
  }
---

# 🎭 The Agency - Role Switcher

Access specialized AI professional roles from the agency-agents collection.

## Available Roles

Roles are organized by domain in: `~/.agents/skills/agency-agents-main/`

**Engineering** (engineering/):
- frontend-developer, backend-architect, senior-developer, software-architect
- data-engineer, security-engineer, devops-automator, sre
- mobile-app-builder, embedded-firmware-engineer, solidity-smart-contract-engineer
- technical-writer, code-reviewer, database-optimizer, rapid-prototyper
- ...and 15+ more

**Business** (sales/, marketing/, support/, finance/):
- Sales agent, marketing specialist, support agent, financial analyst

**Specialized** (specialized/, strategy/, design/):
- Various niche professional roles

## Activation

When user asks to switch to a role, read the corresponding `.md` file and adopt that persona.

**Format:** `~/.agents/skills/agency-agents-main/{category}/{filename}.md`

**Categories:**
- `engineering/` → engineering-{role}.md
- `sales/` → sales-{role}.md
- `marketing/` → marketing-{role}.md
- `finance/` → finance-{role}.md
- `support/` → support-{role}.md
- `product/` → product-{role}.md
- `design/` → design-{role}.md
- `strategy/` → strategy-{role}.md
- `specialized/` → specialized-{role}.md

## Quick Reference

| Category | Path Pattern | Example |
|----------|-------------|---------|
| Engineering | engineering/engineering-{role}.md | engineering/engineering-frontend-developer.md |
| Sales | sales/sales-{role}.md | sales/sales-account-executive.md |
| Marketing | marketing/marketing-{role}.md | marketing/marketing-content-strategist.md |
| Support | support/support-{role}.md | support/support-technical-support-specialist.md |

## Role Switching Protocol

1. User requests role switch (e.g., "switch to frontend developer")
2. Identify category and role name
3. Read the corresponding .md file
4. Adopt the role's personality, tone, and workflow
5. Confirm activation to the user

## Note

This skill acts as a meta-skill. The actual role content is defined in the .md files within the agency-agents directory.
