## Description:

Use Agent Wormhole for one-time sealed handoffs between autonomous agents, including encrypted mission briefs, scoped secrets, temporary artifacts, receipts, config drops, CLI/API usage, ECHO holder access, and Bankr x402 paid opens.

This skill is ready for commercial/non-commercial use.

## Publisher:

[builtbyecho](https://clawhub.ai/user/builtbyecho)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use Agent Wormhole to create one-time encrypted handoffs for mission briefs, scoped secrets, temporary artifacts, receipts, and configuration drops. It also guides use of the CLI/API, ECHO holder access, Bankr x402 paid opens, and service operation checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks users to run an unpinned external npm package in workflows that may involve secrets, private files, and wallet or payment configuration.

Mitigation: Use a pinned, reviewed package version in an isolated project with only required files and environment variables exposed.

Risk: Bankr x402 commands may perform real paid operations even when a maximum payment value is shown.

Mitigation: Treat Bankr x402 calls as real payments, use a separate payer wallet from the endpoint owner wallet, and verify intent before execution.

Risk: Wormhole codes grant one-time access to encrypted payloads and can expose the payload if shared publicly.

Mitigation: Share codes only with intended recipients, avoid logging plaintext secrets or payloads, prefer short TTLs, and clean up received artifacts when no longer needed.

## Reference(s):

- [Agent Wormhole ClawHub page](https://clawhub.ai/builtbyecho/skills/agent-wormhole)
- [Agent Wormhole holder/API route](https://storage.builtbyecho.xyz/agent-wormhole)
- [Agent Wormhole health endpoint](https://storage.builtbyecho.xyz/agent-wormhole/health)
- [Bankr x402 paid open endpoint](https://x402.bankr.bot/0x2a16625fad3b0d840ac02c7c59edea3781e340ae/agent-wormhole-open)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline bash commands and operational guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include CLI/API commands, endpoint checks, wallet/payment handling guidance, and safety reminders for encrypted one-time handoffs.]

## Skill Version(s):

0.1.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
