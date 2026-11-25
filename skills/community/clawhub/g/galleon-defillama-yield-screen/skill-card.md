## Description:

Screen DefiLlama yield pools by exact asset exposure, chain, TVL and base versus reward APY, then investigate shortlisted pool history.

This skill is ready for commercial/non-commercial use.

## Publisher:

[galleonlabs](https://clawhub.ai/user/galleonlabs)

### License/Terms of Use:

MIT

## Use Case:

Developers and analysts use this skill to compare DeFi yield pools for a requested token and chain, inspect base and reward returns, and prepare a shortlist with historical context and unresolved exit checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security scan was benign with medium confidence, but one referenced local path was unresolved, leaving part of the analysis incomplete.

Mitigation: Review the unresolved reference and the related source material before relying on the affected guidance.

Risk: A yield shortlist does not establish available withdrawal capacity, protocol safety, or returns a user can realize.

Mitigation: Check the specific protocol's caps, pause state, withdrawals, and net yield after costs before any execution decision.

## Reference(s):

- [Bounded yield retrieval](artifact/references/requests.md)
- [Official sources and methodology links](artifact/references/sources.md)
- [DefiLlama API documentation](https://api-docs.defillama.com/)
- [DefiLlama yield adapter schema and methodology](https://github.com/DefiLlama/yield-server)
- [Circle USDC contract addresses](https://developers.circle.com/stablecoins/usdc-contract-addresses)
- [DefiLlama provider update cadence FAQ](https://docs.llama.fi/faqs/frequently-asked-questions)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, JSON, Guidance]

**Output Format:** [Markdown shortlist with evidence notes; optional JSON screening results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Up to five ranked pools and up to three history checks; preserves missing APY decomposition and exclusion reasons.]

## Skill Version(s):

0.8.0 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
