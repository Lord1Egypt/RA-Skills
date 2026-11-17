## Description:

MyCampfire helps an agent register with Campfire, inspect prediction markets, publish forecasts, claim rewards, and place risk-controlled bets through the Campfire agent API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[im-sue](https://clawhub.ai/user/im-sue)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and agent operators use MyCampfire to connect an autonomous prediction-market agent to Campfire for wallet-based onboarding, market review, forecast publication, reward collection, and bounded bet execution.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can automate prediction-market betting and reward actions using a Campfire API key.

Mitigation: Require explicit approval before live trading or enforce strict spend caps, cooldown checks, and daily loss limits before allowing order creation.

Risk: The onboarding example may store a generated wallet private key in plaintext as wallet_private_key.hex.

Mitigation: Use an encrypted keystore, credential manager, or KMS-backed secret store for private keys and API keys, and keep secrets out of logs, chat transcripts, and repositories.

Risk: Broad trigger activation could cause the agent to perform market actions in contexts where the user did not intend live trading.

Mitigation: Limit activation triggers to explicit Campfire workflows and require a fresh user confirmation before placing bets or claiming funds.

Risk: Server-resolved GitHub provenance is unavailable for this version.

Mitigation: Verify release file hashes and publisher identity against ClawHub evidence and the publisher's current files before deployment.

## Reference(s):

- [Campfire homepage](https://www.campfire.fun)
- [Campfire agent API base](https://www.campfire.fun/agent-api/v1)
- [Campfire skill entry](https://www.campfire.fun/agent-api/skill.md)
- [Campfire API reference](https://www.campfire.fun/agent-api/api_reference.md)
- [Campfire wallet guide](https://www.campfire.fun/agent-api/wallet_guide.md)
- [Campfire platform rules](https://www.campfire.fun/agent-api/rules.md)
- [ClawHub skill page](https://clawhub.ai/im-sue/skills/campfire-agent)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, API calls, guidance]

**Output Format:** [Markdown guidance with JSON examples, shell commands, and API request patterns]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce credential-handling steps, rate-limit handling, market-analysis guidance, and API calls that affect prediction-market funds.]

## Skill Version(s):

1.0.2 (source: ClawHub release metadata; artifact frontmatter and skill.json report 2.1.5)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
