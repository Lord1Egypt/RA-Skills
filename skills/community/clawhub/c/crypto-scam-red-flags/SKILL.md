---
name: crypto-scam-red-flags
description: A scam-screening skill that reviews offers, messages, or influencer claims and points out concrete red flags. Use when the user receives a suspicious offer, DM, or investment pitch. Prompt-only.
---

# crypto-scam-red-flags

A scam-screening skill that reviews offers, messages, or influencer claims and points out concrete red flags.

## Workflow

1. Take the pasted message, offer text, DM, or campaign description.
2. Look for urgency, guaranteed returns, impersonation, fake support behavior, secrecy, wallet-drain patterns, or emotional manipulation.
3. Classify the situation: likely scam, suspicious, unclear, or low-obvious-risk.
4. Explain why each red flag matters.
5. Give the safest next step: do not click, verify independently, or walk away.

## Output Format

- Risk verdict
- Red flags found
- Why they matter
- Safest next action
- What not to share or sign

## Quality Bar

- Uses evidence from the supplied text, not vague fear.
- Stays practical and protective.
- Makes the user safer even when certainty is impossible.
- Avoids false confidence like "100% safe."

## Edge Cases

- Some real promotions look spammy; say when independent verification is still needed.
- Cannot inspect links, smart contracts, or domains in real time.

## Compatibility

- Best with pasted text or manually transcribed screenshot content.
- Prompt-only, strong complement to wallet safety education.
