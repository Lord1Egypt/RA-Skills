## Description:

Autonomous wallet operations for AI agents on Monad, including swaps, staking, wallet deployment, memecoin trading, and spending-policy management through natural language.

This skill is ready for commercial/non-commercial use.

## Publisher:

[0xsoydev](https://clawhub.ai/user/0xsoydev)

### License/Terms of Use:

MIT

## Use Case:

Developers and external agent operators use ClankerKit to let OpenClaw agents manage Monad wallets, trading, staking, payments, and spending policies through tool calls.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The agent can receive broad live authority to move funds, trade assets, and call contracts.

Mitigation: Install only with low-value or test wallets unless strict spending limits, token allowlists, contract allowlists, and approval thresholds are configured.

Risk: Private keys in environment variables can grant signing authority if exposed.

Mitigation: Use dedicated agent keys with minimal balances and rotate or revoke keys if any environment or logs are compromised.

Risk: Autonomous trades or arbitrary calldata can send funds to unintended recipients or contracts.

Mitigation: Review recipients, contract addresses, calldata, swap routes, and smart-trade auto-execution settings before allowing live execution.

Risk: Outdated dependencies or SDK behavior can affect transaction safety.

Mitigation: Update dependencies and retest wallet, policy, swap, and staking flows before production use.

## Reference(s):

- [ClankerKit ClawHub Skill Page](https://clawhub.ai/0xsoydev/skills/clankerkit)
- [ClankerKit README](artifact/README.md)
- [ClankerKit Skill Definition](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [Text, Configuration, Shell commands, Guidance]

**Output Format:** [Markdown and structured JSON-like tool results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires wallet, policy, owner, and agent private-key environment variables; configured tools may execute live blockchain transactions.]

## Skill Version(s):

0.1.0 (source: server release and package.json; skill.json declares 0.2.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
