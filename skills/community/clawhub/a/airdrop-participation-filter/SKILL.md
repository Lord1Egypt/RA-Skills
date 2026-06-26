---
name: airdrop-participation-filter
description: A decision helper that helps users decide whether to participate in an airdrop campaign. Use when the user considers joining an airdrop. Prompt-only.
---

# airdrop-participation-filter

A decision helper that helps users decide whether to participate in an airdrop campaign.

## Workflow

1. Ask what the airdrop is: which protocol, what the qualification criteria are, and what the potential value might be.
2. Assess time commitment, risk of exposure to unknown protocols, and opportunity cost.
3. Check whether the user has the technical setup to participate safely.
4. Flag disguised data collection, VPN restrictions, and regulatory gray areas.
5. Give a recommendation: worth it, conditional, or skip.

## Output Format

- Airdrop summary
- Participation recommendation
- Time and risk assessment
- Safety checklist before joining
- What to watch for during participation

## Quality Bar

- Does not over-promise potential airdrop value.
- Focuses on whether participation is worth the user's time and risk.
- Flags security risks of interacting with early-stage or unknown protocols.

## Edge Cases

- If the user needs to connect a wallet or deposit funds, flag this as a red flag.
- If the qualification criteria require significant personal data, flag regulatory risk.

## Compatibility

- Prompt-only, no wallet connection required.
- Works from user-described or pasted campaign details.
