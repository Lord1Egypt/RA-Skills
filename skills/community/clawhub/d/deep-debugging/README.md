# 🕵️ Deep Debugging

**Stop blind fixes. Stabilize incidents first. Prove root cause before changing code.**

Deep Debugging is an evidence-first protocol for AI coding agents and developers. It prevents random patch loops by forcing a clear sequence: impact → evidence → hypothesis → binary search → minimal fix → verification → prevention.

## v2.2.0 — 9.5 polish

- Shorter core `SKILL.md` for lower context cost.
- Progressive references for incident, stack-specific, and report templates.
- Safe `scripts/incident_snapshot.sh` helper that prints metadata and env **key names only**, never secrets.
- More stack-neutral workflow while keeping optional NestJS/Next.js/Prisma/Auth/Webhook checklists.
- Explicit `Next optimization:` rule so remaining improvement potential is not hidden.

## Use it for

- unclear or recurring bugs
- failed deploys, red healthchecks, production-like failures
- `401`, `403`, `500`, broken login/session flows
- external API/webhook failures
- bugs where previous fixes did not hold

## Do not use it for

- obvious typos/compiler-pointed syntax errors
- missing install/setup steps
- trivial one-line route/config fixes
- cosmetic UI tweaks

## Core workflow

```text
Incident Gate → Quick Triage → Evidence → Hypothesis → Binary Search → Minimal Fix → Verification → Prevention
```

**Rule:** if you cannot state the proof, you do not know the cause yet. Never copy real tokens, cookies, credentials, customer data, or production secrets into reports.

---

*by brasco05 · evidence-first debugging for OpenClaw/ClawHub agents*
