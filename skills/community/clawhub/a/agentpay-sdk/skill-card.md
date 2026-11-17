## Description:

AgentPay SDK helps agents install and operate the AgentPay CLI for wallet setup, funding, policy changes, transfers, approvals, broadcasts, x402 payments, MPP payments, and supported merchant payment flows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wlfi-dev1](https://clawhub.ai/user/wlfi-dev1)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to install AgentPay, set up or recover self-custodial local wallets, check funding, configure payment policies, and execute or approve EVM payment flows through the current agentpay CLI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The documented one-click installer uses remote shell execution.

Mitigation: Review the skill before installing and prefer a local copy or verifiable release installation over curl-piped shell commands.

Risk: Payment flows may accept server-selected charges or initiate outbound transactions.

Mitigation: Require explicit confirmation of chain, token, recipient, amount, and broadcast intent before any payment, and use conservative wallet policies and manual approval limits.

Risk: External QR fallback URLs can expose payment metadata.

Mitigation: Avoid external QR fallback URLs when privacy matters.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/wlfi-dev1/skills/agentpay-sdk)
- [World Liberty Financial](https://worldlibertyfinancial.com)
- [MPP Services Directory](https://mpp.dev/services/llms.txt)
- [Capabilities](references/capabilities.md)
- [Install And Workflows](references/install-and-workflows.md)
- [Intents And Policies](references/intents-and-policies.md)
- [MPP Services](references/mpp-services.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands, configuration guidance, and occasional JSON snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs should require explicit user confirmation for chain, token, recipient, amount, and broadcast intent before payment actions.]

## Skill Version(s):

0.3.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
