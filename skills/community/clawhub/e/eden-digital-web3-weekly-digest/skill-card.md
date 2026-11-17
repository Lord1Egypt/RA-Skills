## Description:

Generates a Web3 capital-markets weekly digest from public information about funding rounds, regulation, public-company digital asset treasury activity, mergers and acquisitions, and RWA project updates.

This skill is ready for commercial/non-commercial use.

## Publisher:

[baoyangispoor](https://clawhub.ai/user/baoyangispoor)

### License/Terms of Use:

MIT-0

## Use Case:

External users and analysts use this skill to draft a weekly Web3 industry capital-operations report with structured sections for regulation, funding, DAT activity, M&A, RWA progress, summary metrics, and editorial commentary.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The generated report can include incomplete or stale public Web3, financial, or regulatory information.

Mitigation: Review fetched facts and cited source material before publishing financial or regulatory summaries.

Risk: Some weekly DAT activity and project updates may not be available from the public sources used by the skill.

Mitigation: Use the skill's manual follow-up prompts to collect missing company announcements, weekly changes, or source links from the user.

## Reference(s):

- [Cryptorank Funding Rounds](https://cryptorank.io/funding-rounds)
- [CoinGecko Public Treasury API - Bitcoin](https://api.coingecko.com/api/v3/companies/public_treasury/bitcoin)
- [CoinGecko Public Treasury API - Ethereum](https://api.coingecko.com/api/v3/companies/public_treasury/ethereum)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown report sections with inline shell commands and manual follow-up prompts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs should flag incomplete public data and request user-supplied updates where automated sources are insufficient.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact frontmatter says 2.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
