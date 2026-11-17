## Description:

Runs a complete local Dawn strategy workflow: authenticate, research markets with SDK tools, generate Python strategy code, launch background runs, monitor logs, and stop strategies.

This skill is ready for commercial/non-commercial use.

## Publisher:

[njdawn](https://clawhub.ai/user/njdawn)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to operate Dawn CLI workflows for prediction-market research, strategy creation, paper or live strategy launches, monitoring, and wallet-aware trading operations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide live prediction-market trading and wallet operations.

Mitigation: Use paper mode by default and require fresh, explicit user confirmation before any live launch or direct trade.

Risk: Agents may be given tools that execute buy or sell orders.

Mitigation: Avoid giving LLM agents direct buy/sell authority; keep execution behind user-reviewed Dawn CLI commands or confirmed workflows.

Risk: Wallet balances, portfolio data, strategy prompts, and logs may be exposed to Dawn services or configured model providers.

Mitigation: Review provider settings, credentials, and logs before use, and limit sensitive data shared with model-backed strategy logic.

Risk: Strategy dependencies can be installed from npm or Python package sources.

Mitigation: Review and pin npm and Python dependencies before launching strategies, especially for live trading.

## Reference(s):

- [Dawn homepage](https://dawn.ai)
- [Dawn CLI dashboard](https://cli.dawn.ai/dashboard)
- [OpenWallet](https://openwallet.sh/)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands and Python code]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include generated local strategy code, Dawn CLI commands, authentication and wallet setup steps, monitoring instructions, and direct-trade confirmation prompts.]

## Skill Version(s):

1.4.3 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
