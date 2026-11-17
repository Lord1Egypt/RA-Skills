## Description:

Trust layer for agentic commerce that helps agents build a BOB Score from on-chain payment proofs and x402 receipts, then borrow USDC credit lines based on that score.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bankofbotsandy](https://clawhub.ai/user/bankofbotsandy)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and agent operators use this skill to connect agents to BOB, import on-chain and x402 payment proofs, inspect BOB Score history, and operate governed treasury and lending workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide agents through wallet, treasury, loan, and repayment workflows that may move funds or create financial obligations.

Mitigation: Require human review of the exact agent ID, amount, chain, destination, command source, and reversibility before enabling spending, loan acceptance, repayment, wallet sweep, webhook, API-key, or treasury commands.

Risk: The skill can encourage recurring inbox or cron processing of external operator commands.

Mitigation: Use recurring processing only with separate operator authentication, spend limits, and audit controls; avoid automatic command execution for high-impact actions.

Risk: The skill depends on local wallet keys and BOB credentials.

Mitigation: Install only in environments where a BOB-connected agent is intentionally allowed to access local wallet keys, BOB_API_KEY, and BOB_AGENT_ID.

## Reference(s):

- [BOB](https://bankofbots.ai)
- [BOB API Docs](https://api.bankofbots.ai/docs)
- [Agent Setup Guide](https://bankofbots.ai/docs/agent-setup)
- [npm package](https://www.npmjs.com/package/@bankofbots/skill)
- [BOB CLI releases](https://github.com/bankofbots/bob-cli/releases/latest)
- [BOB agent kit source](https://github.com/bankofbots/bob-agent-kit)
- [Command reference](references/commands.md)
- [Error recovery](references/errors.md)
- [Proof submission](references/proofs.md)
- [BOB Score tiers](references/scoring.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with bash command examples and JSON response examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires BOB_API_KEY and BOB_AGENT_ID; BOB_API_URL is optional.]

## Skill Version(s):

0.58.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
