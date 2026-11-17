## Description:

Flap Skills helps agents create V5 tokens on BSC, buy or sell tokens with USDT, and run automated market-making or volume-generation flows through BNB Chain MCP.

This skill is ready for commercial/non-commercial use.

## Publisher:

[flap-builder](https://clawhub.ai/user/flap-builder)

### License/Terms of Use:

MIT

## Use Case:

Developers and token operators use this skill to launch V5 tokens and execute BSC token trading or market-making workflows from an agent session. The skill requires a configured BNB Chain MCP wallet and can initiate real on-chain transactions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can automate real BSC token trades and volume-generation activity using a funded wallet.

Mitigation: Use a dedicated wallet funded only with amounts the user can afford to lose, and require explicit confirmation before enabling trading or market-making runs.

Risk: The workflow can rely on broad or ongoing token approvals without per-action user control.

Mitigation: Prefer capped approvals, avoid unlimited allowances when possible, record the approved spender and amount, and revoke allowances and worker permissions after use.

Risk: Market-making worker keys may be generated as local JSON files.

Mitigation: Store worker key files outside shared, synced, or repository directories, collect remaining funds after use, and delete the files when they are no longer needed.

Risk: Automated market-making may continue until stopped and may not enforce a loss cap.

Mitigation: Set explicit operational limits where supported, monitor active runs, and stop the bot promptly when the intended activity is complete.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/flap-builder/skills/flap-skills)
- [Project Homepage](https://github.com/flap-builder/flap-skills)
- [BNB Chain MCP Skills Documentation](https://docs.bnbchain.org/showcase/mcp/skills/)
- [Flap Portal Token Launcher Documentation](https://docs.flap.sh/flap/developers/token-launcher-developers/launch-token-through-portal)
- [Flap Deployed Contract Addresses](https://docs.flap.sh/flap/developers/token-launcher-developers/deployed-contract-addresses)
- [Contract ABI Reference](artifact/references/contract-abi.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, API calls, Guidance]

**Output Format:** [Markdown guidance with inline shell commands, configuration values, contract call parameters, and agent action steps.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May generate local worker key JSON files and transaction instructions for BSC token operations.]

## Skill Version(s):

1.8.0 (source: SKILL.md frontmatter, package.json, ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
