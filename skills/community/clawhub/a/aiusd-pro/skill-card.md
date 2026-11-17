## Description:

AIUSD Pro is an AI-powered trading agent that lets users trade, check balances, and manage positions through natural-language conversation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tech-fe-aiusd](https://clawhub.ai/user/tech-fe-aiusd)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use AIUSD Pro to interact with AIUSD for balances, trading, staking, position management, and market queries through natural-language chat. The skill guides an agent to run the AIUSD CLI, relay responses, and continue multi-turn confirmation flows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can initiate trading, staking, leverage, or wallet-related actions that may affect real funds.

Mitigation: Independently verify every asset, amount, venue, leverage level, fee, slippage value, wallet approval, and confirmation prompt before proceeding.

Risk: The CLI is resolved through npm at execution time, so behavior can change if an unreviewed package version is installed.

Mitigation: Prefer a pinned and reviewed CLI version before using the skill with production accounts or real funds.

Risk: Authentication and conversation state use browser links and session identifiers that may grant access to sensitive trading context.

Mitigation: Verify the login domain, keep session IDs private, and avoid sharing generated session links except with the intended user.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/tech-fe-aiusd/skills/aiusd-pro)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Markdown guidance with inline shell command examples and relayed CLI text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js >= 18 and the node binary; send operations are expected to run in background mode because responses can take 10-300 seconds.]

## Skill Version(s):

1.0.0 (source: server release metadata and target metadata; artifact frontmatter says 1.0.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
