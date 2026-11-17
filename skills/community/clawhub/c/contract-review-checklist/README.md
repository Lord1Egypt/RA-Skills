# Contract Review Checklist Pack

> Contract risk review checklists — clause-by-clause red-flag scanning by contract type, risk grading with rewrite suggestions, missing-clause detection, and a negotiation-ready review report. Not "AI lawyer": structured triage before counsel review.

**Category:** legal-automation  |  **License:** CC-BY-4.0  |  **Version:** 1.0.0
**Price:** Free on GitHub & skills.sh (CC BY 4.0). Curated bundle on Gumroad: $29 (Pro $59).

## What it does

This is not an 'AI lawyer' — it standardizes the checking motions of legal review so a contract gets a first-pass triage in 30 minutes instead of a billable discovery session.

A five-layer review framework: counterparty screening, type-differentiated red-flag clause scan, missing-clause detection, cross-document consistency check, and risk-graded output with rewrite suggestions.

## What you get

- Counterparty screening: legal entity, signing authority, license alignment.
- 12-item core red-flag checklist (sales/service agreements) plus type-specific variants (NDAs, employment, lease, etc.).
- Missing-clause detection (liability, dispute resolution, force majeure, notice, termination).
- Risk grading (HIGH = do not sign unamended / MEDIUM = negotiate / LOW = acknowledge) with a rewrite suggestion per finding and a negotiation-ready review report.

## How to use

- **As an agent skill:** drop `SKILL.md` into your agent's skills folder, or install from the GitHub repo below.
- **As a prompt pack:** open `SKILL.md` and follow the workflow section step by step.
- Works with any agent that reads `SKILL.md` (Claude Code, OpenCode, Cursor, Gemini CLI, Cline, and more).

## Install

```bash
# skills.sh / ClawHub
npx skills add https://github.com/chinabizskills/contract-review-checklist
# ClawHub (after publish)
openclaw skills install @chinabizskills/contract-review-checklist
```

Or clone: `git clone https://github.com/chinabizskills/contract-review-checklist.git`

## Pricing & license

Licensed under **CC BY 4.0** — free to use, share, and adapt (attribution required). A curated, expanded bundle (with the Pro templates) is sold on Gumroad for $29 (Pro $59). The free GitHub/skills.sh version is the complete, working skill.

## Tags

legal, contracts, risk-review, msa, negotiation

## Contents

- `SKILL.md` — the skill definition / prompt library (this is the product).
- `README.md` — this file.
- `skill-card.md` — ClawHub metadata card.
- `RELEASE_NOTES.md` — version history.

---

Part of the **China-Biz Skills** collection by RAY — practical AI agent skills for business, e-commerce, support, legal triage, and content.
