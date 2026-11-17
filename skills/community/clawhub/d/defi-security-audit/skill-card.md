## Description:

Analyze a DeFi protocol for vulnerabilities, mechanism safety, and risk factors.

This skill is ready for commercial/non-commercial use.

## Publisher:

[truenorth-lj](https://clawhub.ai/user/truenorth-lj)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, security analysts, and DeFi researchers use this skill to assess protocol governance, oracle design, admin privileges, economic mechanisms, and public risk signals before making security or risk decisions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Live web and blockchain API lookups can disclose protocol names, contract addresses, or investigation targets to external services.

Mitigation: Avoid submitting confidential protocol names, unreleased addresses, or private investigation targets unless external disclosure is acceptable.

Risk: Helper scripts and API workflows may use API keys or local environment files.

Mitigation: Use a dedicated low-privilege Etherscan API key and avoid storing unrelated secrets in parent .env files.

Risk: Installation and helper workflows may involve unpinned package or shell commands.

Mitigation: Review unpinned npx, pip, or pipe-to-shell commands before running them.

Risk: The skill is a research aid, not a formal smart contract audit.

Mitigation: Treat generated reports as risk-analysis guidance and obtain independent expert review before making high-impact decisions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/truenorth-lj/skills/defi-security-audit)
- [Methodology](docs/methodology.md)
- [Audit report index](docs/audit-reports.md)
- [DeFiLlama API](https://api.llama.fi/protocols)
- [GoPlus Security API](https://api.gopluslabs.io/api/v1)
- [RugCheck token reports](https://api.rugcheck.xyz/v1/tokens/{mint_address}/report)
- [Birdeye token security](https://public-api.birdeye.so/public/token_security?address={mint_address})

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown risk report with supporting command examples and source notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports include triage and confidence scores, risk ratings, information gaps, and evidence-based recommendations.]

## Skill Version(s):

1.2.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
