## Description:

Decker AI 트레이딩 helps an agent guide Decker users through trading signals, portfolio status, order approvals, auto-order rules, news digests, Slack or Telegram linking, and exchange API key setup.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gigshow](https://clawhub.ai/user/gigshow)

### License/Terms of Use:

MIT-0

## Use Case:

External Decker users use this skill through Slack or Telegram to ask for crypto market signals, portfolio and position status, order approval flows, auto-order setup, news digests, and exchange onboarding guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can initiate account-linked trading workflows, including live trading or auto-order rules.

Mitigation: Review the execution mode before use, keep approvals enabled where available, and do not enable live trading or automation until the user understands how to disable rules and revoke access.

Risk: Exchange API keys and wallet private keys may control real assets.

Mitigation: Use least-privilege exchange keys, disable withdrawals, use dedicated trading wallets for DEX flows, and never provide a primary wallet private key.

Risk: Decker may receive user messages, Slack identifiers, portfolio or trading requests, and order parameters.

Mitigation: Share only the account and order information needed for the requested workflow, and review organizational privacy requirements before deployment.

Risk: Security evidence flags an unsafe secret-in-URL order request pattern.

Mitigation: Review URL logging, monitoring, and retention controls before deployment, and rotate any secret that may have been exposed.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/gigshow/skills/decker)
- [Decker Website](https://decker-ai.com)
- [Decker Slack Link](https://decker-ai.com/decker-link)
- [Decker Telegram Link](https://decker-ai.com/decker-link-telegram)
- [Decker OpenClaw/Slack User Guide](USER_GUIDE.md)
- [Decker Question List](references/QUESTIONS_LIST.md)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Concise natural-language responses with setup steps, status summaries, and order approval guidance.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May ask users to confirm account linkage, execution mode, and approval steps before trading actions.]

## Skill Version(s):

2.3.2 (source: server evidence, frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
