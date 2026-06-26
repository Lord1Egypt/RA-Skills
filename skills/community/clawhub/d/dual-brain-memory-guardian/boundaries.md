# Security Boundaries

## Never Store

| Category | Examples | Why |
|----------|----------|-----|
| Credentials | Passwords, API keys, tokens, SSH keys | Security breach risk |
| Financial | Card numbers, bank accounts, crypto seeds | Fraud risk |
| Medical | Diagnoses, medications, conditions | Privacy and compliance risk |
| Biometric | Voice patterns, behavioral fingerprints | Identity theft risk |
| Third parties | Information about other people | No consent obtained |
| Location patterns | Home/work addresses, routines | Physical safety risk |
| Access patterns | System access maps, role grants | Privilege escalation risk |

## Store with Caution

| Category | Rules |
|----------|-------|
| Work context | Decay after project ends, never leak across projects |
| Emotional states | Only if user explicitly shares, never infer |
| Relationships | Role-level only (for example, manager/client), no personal details |
| Schedules | General patterns only, avoid exact personal timing |

## Vector DB Gatekeeper (Pinecone)

Before any `upsertRecords` call, enforce these rules:

1. Replace real API keys, tokens, IPs, and emails with `<REDACTED>` forms.
2. Replace private key materials and obvious secret headers.
3. Remove or generalize sensitive person and confidential project names using context-label redaction and metadata key rules.
4. Block payloads that still contain private key material after redaction.
5. Keep metadata minimal and filter-oriented; avoid storing unnecessary raw details.

Implementation baseline lives in `src/pinecone/gatekeeper.js`.

## Dual-Brain Priority Safety

1. Markdown files in `~/dual-brain-memory-guardian/` are explicit contracts.
2. Pinecone recall is advisory context, not policy.
3. If conflict occurs, follow Markdown and optionally ask whether to update rules.

## Transparency Requirements

1. Audit on demand: user can request full memory summary.
2. Source tracking: each promoted rule should show when/how learned.
3. Explain actions: link behavior to rule source.
4. No hidden policy: behavior-affecting rule must be visible in Markdown.
5. Deletion verification: confirm both local and vector-side deletion outcomes.
6. Destructive reminder: before deleting data or database records, warn about irreversibility and confirm intent.

## Red Flags

Stop and review if any of these appears:

- Storing data "just in case"
- Inferring sensitive traits from weak signals
- Keeping data after user asks to forget
- Cross-project leakage of preferences
- Learning compliance/manipulation tactics
- Building personal psychological profiles

## Kill Switch

If user says "forget everything":

1. Export local memory if user asks for audit snapshot.
2. Wipe `~/dual-brain-memory-guardian/` tracked memory files.
3. Clear Pinecone tenant namespace (`npm run memory:forget-all`).
4. Confirm completion for both local and vector memory stores.
5. Start fresh with no hidden carry-over rules.

## Consent Model

| Data Type | Consent Level |
|-----------|---------------|
| Explicit corrections | Implied by correction itself |
| Inferred preferences | Ask after repeated observations |
| Project context | Ask when first material impact is detected |
| Cross-session patterns | Explicit opt-in required |
