## Description:

Reviews completed Hyperliquid activity against exchange records to separate trading outcomes from execution costs and process quality.

This skill is ready for commercial/non-commercial use.

## Publisher:

[galleonlabs](https://clawhub.ai/user/galleonlabs)

### License/Terms of Use:

MIT

## Use Case:

Traders and reviewers use this read-only skill to reconcile completed Hyperliquid orders, fills, fees, funding, and incidents with their trade tickets, then record an evidence-backed process finding.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Reviewing account history exposes sensitive financial records.

Mitigation: Provide only the account and history needed for the completed review; never share private keys or signer secrets.

Risk: An optional unpinned installation command may run unverified package code.

Mitigation: Avoid running the optional npx handoff unless its package and exact version have been verified and trusted.

Risk: Incomplete exchange history can produce misleading performance or protection claims.

Mitigation: Reconcile the available fills and funding; identify missing windows and mark unsupported conclusions unknown.

## Reference(s):

- [Review evidence](references/review-evidence.md)
- [Process and incident review](references/process-review.md)
- [Journal contract](references/journal-contract.md)
- [Official Hyperliquid tools](references/official-tools.md)
- [Hyperliquid info endpoint documentation](https://hyperliquid.gitbook.io/hyperliquid-docs/for-developers/api/info-endpoint)
- [Hyperliquid API limits](https://hyperliquid.gitbook.io/hyperliquid-docs/for-developers/api/rate-limits-and-user-limits)

## Skill Output:

**Output Type(s):** [Markdown, Text, Guidance]

**Output Format:** [Markdown review and append-only UTC journal entry]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Process grade, realized result, fees, funding, evidence gaps, and one follow-up finding.]

## Skill Version(s):

0.4.0 (source: frontmatter and server release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
