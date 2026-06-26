## Description: <br>
Bitcoin Lightning payment CLI for agents. Lowest LSP fees. Self-custody wallet with LNURL, typed exit codes, JSON envelope output, encrypted messaging, and daemon mode. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ovitrif](https://clawhub.ai/user/ovitrif) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and external agents use this skill to operate a self-custodial Bitcoin and Lightning wallet from shell commands, including wallet setup, balances, invoices, payments, liquidity orders, webhooks, and encrypted messaging. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Agent-accessible wallet commands can move real Bitcoin funds and manage Lightning channels with weak default guardrails. <br>
Mitigation: Require human approval for every pay, send, fee bump, and channel action, and enforce strict amount and fee limits before execution. <br>
Risk: Plaintext seed storage through --no-password can expose wallet funds if the agent environment is compromised. <br>
Mitigation: Use a small isolated wallet and prefer encrypted seed storage with BITKIT_PASSWORD instead of plaintext automation. <br>
Risk: Webhook destinations and installer/release downloads introduce external trust and data exposure concerns. <br>
Mitigation: Review webhook destinations and secrets, and verify the installer or release before running it. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/ovitrif/bitkit-cli) <br>
- [Bitkit CLI Homepage](https://github.com/synonymdev/bitkit-cli) <br>
- [Artifact README](artifact/README.md) <br>
- [Artifact Skill Reference](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, configuration, guidance, JSON] <br>
**Output Format:** [Markdown with inline shell commands, configuration snippets, and JSON envelope examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands should use --json for parseable envelopes; payment and wallet actions can affect real Bitcoin funds.] <br>

## Skill Version(s): <br>
0.2.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
