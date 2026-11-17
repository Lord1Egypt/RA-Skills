## Description:

Guides agents through Solana Pump.fun token launches with CrewPay KOL Autohire and on-chain creator fee-sharing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fxams](https://clawhub.ai/user/fxams)

### License/Terms of Use:

MIT-0

## Use Case:

Agents and their operators use this skill to assemble KOL crews, review launch costs and fee shares, and launch Solana tokens through CrewPay after human approval.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A real mainnet launch spends SOL and may proceed with an incomplete fee-share lock.

Mitigation: Review dry-run costs and fee shares, require human approval before launch, and confirm the fee-share lock afterward.

Risk: Exposed launcher-wallet or API credentials could compromise funds or account access.

Mitigation: Use a dedicated low-balance burner wallet, keep its secret only in the local MCP environment, and rotate exposed keys.

## Reference(s):

- [CrewPay skill release](https://clawhub.ai/fxams/skills/crewpay)
- [CrewPay homepage](https://crewpay.dev)
- [CrewPay agent documentation](https://crewpay.dev/llms-full.txt)
- [CrewPay OpenAPI specification](https://api.crewpay.dev/openapi.json)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration instructions]

**Output Format:** [Markdown with shell examples and launch steps]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes dry-run results, approval links, and fee-share checks when available.]

## Skill Version(s):

1.1.6 (source: frontmatter and server release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
