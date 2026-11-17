## Description:

Screens DefiLlama yield pools by exact asset exposure, chain, TVL, and return type, then checks the history of shortlisted pools.

This skill is ready for commercial/non-commercial use.

## Publisher:

[galleonlabs](https://clawhub.ai/user/galleonlabs)

### License/Terms of Use:

MIT

## Use Case:

Researchers and developers use this skill to compare public stablecoin or lending yields, separate base returns from incentives, and prepare a shortlist for further due diligence.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Public APY and TVL data do not establish protocol safety, withdrawable capacity, or realizable returns.

Mitigation: Check the protocol's withdrawal conditions, caps, pause state, and net yield separately before any user-directed transaction.

Risk: Incentive-heavy or stale headline APY can mislead comparisons.

Mitigation: Distinguish base from reward APY, preserve missing values, report retrieval time, and inspect recent pool history.

## Reference(s):

- [Yield retrieval recipe](references/requests.md)
- [Official sources](references/sources.md)
- [DefiLlama API documentation](https://api-docs.defillama.com/)
- [DefiLlama yield adapter methodology](https://github.com/DefiLlama/yield-server)

## Skill Output:

**Output Type(s):** [Analysis, Guidance]

**Output Format:** [Markdown shortlist with ranked pool data, exclusions, and caveats]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Up to five pools; includes source, timestamps when available, and unresolved exit or capacity checks.]

## Skill Version(s):

0.6.1 (source: release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
