## Description:

Screens crypto wallets, counterparties, tokens, and x402 payment endpoints for sanctions matches and risk signals before transactions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[montassirbbk-dot](https://clawhub.ai/user/montassirbbk-dot)

### License/Terms of Use:

MIT

## Use Case:

External users and developers can screen wallets and tokens before sending funds, onboarding counterparties, or buying tokens. The results support a decision and are not legal or financial advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security scan returned a suspicious verdict with medium confidence, citing repeated use of an unpinned `agentcash` package and concern about access to local wallet resources or secrets.

Mitigation: Review the package and commands before running; avoid exposing funded wallets or secrets, and pin or inspect the package version.

Risk: The scan reports a privacy disclosure gap for personal-data screening.

Mitigation: Limit personal information sent for screening and review the service's privacy practices before submitting sensitive data.

Risk: The scan was partial because a local reference could not be resolved, so its evidence is incomplete.

Mitigation: Review the unresolved reference and obtain a complete security scan before relying on the assessment.

## Reference(s):

- [Genexxis Crypto Safety](https://skills.genexxis.com)
- [ClawHub release page](https://clawhub.ai/montassirbbk-dot/skills/genexxis-crypto-safety)

## Skill Output:

**Output Type(s):** [Analysis, API Calls, Shell commands]

**Output Format:** [Markdown guidance with shell commands and structured API results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Screening results are decision support, not legal or financial advice; endpoint calls are paid per call in USDC on Base.]

## Skill Version(s):

1.0.0 (source: frontmatter, server release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
