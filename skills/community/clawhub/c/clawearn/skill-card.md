## Description:

Modular prediction market trading platform for OpenClaw bots. Trade on Polymarket, manage wallets, transfer USDC, and automate trading strategies.

This skill is ready for commercial/non-commercial use.

## Publisher:

[stonega](https://clawhub.ai/user/stonega)

### License/Terms of Use:


## Use Case:

External developers and OpenClaw bot operators use this skill to configure wallet management, monitor balances and positions, and guide Polymarket trading workflows from an agent.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Real-money wallet authority and autonomous trading guidance can move or lose funds.

Mitigation: Use a low-balance dedicated hot wallet and require explicit human confirmation for every trade, transfer, withdrawal, and approval.

Risk: Remote installation and heartbeat self-update commands can replace skill content from network sources.

Mitigation: Do not run the remote installer or enable self-updates until the source and each update are independently verified.

Risk: Private keys may be exposed through command-line arguments, plaintext files, logs, or agent messages.

Mitigation: Use secure credential storage, avoid passing private keys on the command line, and redact secrets from logs and prompts.

Risk: Unlimited token approvals can leave funds exposed if an approved contract or key is compromised.

Mitigation: Avoid unlimited allowances where possible, review approvals before signing, and revoke unused approvals.

## Reference(s):

- [Claw Earn ClawHub page](https://clawhub.ai/stonega/skills/clawearn)
- [Clawearn homepage](https://clawearn.xyz)
- [Clawearn documentation](https://docs.clawearn.xyz)
- [Polymarket documentation](https://docs.polymarket.com)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples, JSON configuration snippets, and status-response templates.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guides real-money wallet, transfer, market search, order, monitoring, and incident-response workflows.]

## Skill Version(s):

1.2.0 (source: ClawHub release evidence; artifact frontmatter lists 1.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
