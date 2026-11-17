## Description:

Earn yield on USDC by supplying to the Moonwell Flagship USDC vault on Base. Use when depositing USDC, withdrawing from the vault, checking position/APY, or generating yield reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sergey1997](https://clawhub.ai/user/sergey1997)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to manage USDC yield positions on Base through Moonwell vault deposits, withdrawals, status checks, reports, and reward compounding.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: This skill manages real funds through a hot-wallet private key.

Mitigation: Use a dedicated wallet with limited funds, keep only necessary ETH for gas, and review every transaction before execution.

Risk: The auto-compound path can sign under-validated Odos swap transactions and may deposit more USDC than expected.

Mitigation: Avoid auto-compound until transaction payload validation is reviewed; manually confirm that only intended reward proceeds are swapped and deposited.

Risk: Transaction previews are informational because scripts do not consistently require explicit user confirmation before signing.

Mitigation: Treat previews as review aids only and run commands in a controlled local environment with locked dependencies.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sergey1997/skills/gekko-yield)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Markdown, JSON, Guidance]

**Output Format:** [Markdown, plain text, JSON reports, and executable shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js and a locally configured Base wallet; transaction scripts may sign on-chain operations.]

## Skill Version(s):

1.0.0 (source: frontmatter, release evidence, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
