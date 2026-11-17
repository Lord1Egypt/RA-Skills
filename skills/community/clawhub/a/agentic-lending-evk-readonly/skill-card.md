## Description:

Provides read-only EVK-first lending workflow planning and verification for Api3-backed markets, including oracle route resolution, feed readiness review, EVK artifact preparation, deployability assessment, and post-deploy borrow-proof planning without transaction execution.

This skill is ready for commercial/non-commercial use.

## Publisher:

[daav3](https://clawhub.ai/user/daav3)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to plan or review Api3-backed Euler EVK lending-market workflows while staying in inspection, simulation, and readiness-assessment mode. It is suited for route resolution, feed funding classification, oracle and EVK preparation, blocker reporting, and borrow-proof planning that must stop before live execution.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Live borrowing configuration and command examples could move funds if reused as executable instructions.

Mitigation: Keep signer environment variables and wallet configurations out of committed files, and require a separate trusted live workflow with manual confirmation before any borrow, repay, approval, swap, funding, or deployment action.

Risk: Funding states such as executable or browser-assisted could be mistaken for permission to act.

Mitigation: Treat these states as planning outputs only; stop at dry-run artifacts or browser handoff readiness and do not complete purchases or submit transactions from this skill.

Risk: Deployment readiness could be confused with proof that a market is borrowable.

Mitigation: Require a separate borrow-proof workflow and explicit live confirmation before claiming live borrowability.

Risk: Illustrative addresses, token decimals, vaults, and router settings may not match a user's live market.

Mitigation: Derive proof configuration from fresh deployment outputs and current chain or wallet state before any live-capable workflow uses it.

## Reference(s):

- [Agentic Lending EVK workflow reference](references/api_reference.md)
- [Current capabilities and limits](references/current_capabilities.md)
- [EVK borrow-proof planning checklist](references/live-borrow-checklist.md)
- [Arbitrum eUSDC-1 isolated proof config example](references/arbitrum-eusdc1-isolated-example.json)
- [ClawHub skill page](https://clawhub.ai/daav3/skills/agentic-lending-evk-readonly)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown reports with inline shell commands and JSON configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only planning output; live transaction execution is out of scope.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
