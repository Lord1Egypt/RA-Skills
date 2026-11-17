## Description:

AI agents borrow USDC based on their Moltbook karma score. Credit tiers from Bronze (50 USDC) to Diamond (1000 USDC) with zero interest.

This skill is ready for commercial/non-commercial use.

## Publisher:

[abdhilabs](https://clawhub.ai/user/abdhilabs)

### License/Terms of Use:

ISC

## Use Case:

External developers and agent operators use KarmaBank to register Moltbook-named agents, check reputation-based credit limits, and run CLI workflows for testnet USDC borrowing, repayment, history, and wallet setup.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may be installed or run in an environment with real Circle credentials or funds.

Mitigation: Review before installation and use only isolated testnet or sandbox credentials.

Risk: The npm install path includes a local file dependency that should be reviewed before execution.

Mitigation: Review local dependencies before running npm install, or disable install scripts until dependencies are trusted.

Risk: Pasting API keys or entity secrets into shell commands can expose credentials through shell history or logs.

Mitigation: Use environment files or a secret manager and avoid pasting secrets directly into commands.

Risk: The file-backed loan ledger is not suitable for real accounting.

Mitigation: Use the ledger only for test or demo workflows until persistence, audit trails, and fail-closed transfer handling are implemented.

Risk: Borrowing depends on Moltbook identity and reputation signals that require verification.

Mitigation: Verify Moltbook identity ownership and production API behavior before approving loans.

## Reference(s):

- [KarmaBank ClawHub Page](https://clawhub.ai/abdhilabs/skills/agent-credit-system)
- [KarmaBank Homepage](https://github.com/openclaw/agent-credit-system)
- [Moltbook](https://moltbook.com)
- [Moltbook API Base](https://www.moltbook.com/api/v1)
- [Circle Console](https://console.circle.com)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with CLI commands and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include npm, KarmaBank CLI, Circle, and Moltbook setup commands.]

## Skill Version(s):

1.0.0 (source: package.json and ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
