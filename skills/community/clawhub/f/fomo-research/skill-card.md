## Description:

Fomo Research helps agents research smart-money crypto activity through the Fomo social graph, including trader leaderboards, live activity, watchlists, positions, and theses.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pooowell](https://clawhub.ai/user/pooowell)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to configure an agent for Fomo-based crypto trader research, including finding high-performing traders, monitoring selected handles, checking positions and theses, and summarizing notable on-chain activity. It is not for executing trades, managing funds, or handling private keys.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The provider can observe selected Fomo handles, watchlists, and usage patterns.

Mitigation: Install only when this data sharing is acceptable, and avoid placing sensitive research interests in watchlists or local trade logs unless necessary.

Risk: The skill uses a bearer API key for Cope Capital requests.

Mitigation: Keep COPE_API_KEY private, avoid logging it, and revoke the key if it is exposed.

Risk: x402 can enable paid API calls after the free quota.

Mitigation: Enable x402 only after explicit user approval and review account usage before recurring or automated polling.

## Reference(s):

- [Cope Capital API Reference](references/api.md)
- [Interactive API Docs](https://api.cope.capital/docs)
- [Cope Capital Docs](https://cope.capital/docs)
- [Fomo](https://fomo.family)
- [ClawHub Skill Page](https://clawhub.ai/pooowell/skills/fomo-research)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, Markdown, API calls]

**Output Format:** [Markdown guidance with curl command examples and JSON response examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a COPE_API_KEY for authenticated API calls; x402 paid calls are optional and require explicit user permission.]

## Skill Version(s):

0.3.0 (source: server release metadata and changelog, released 2026-02-21)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
