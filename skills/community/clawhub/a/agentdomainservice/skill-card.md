## Description:

Domain availability API built for AI agents to check single domains, explore names across common TLDs, filter by budget, and get suggestions with JSON or TXT responses.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gregm711](https://clawhub.ai/user/gregm711)

### License/Terms of Use:

MIT

## Use Case:

External users, developers, and AI agents use this skill to check domain availability, get purchase quotes, register domains through supported payment methods, and manage DNS, nameservers, settings, transfer, and token recovery workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can spend money or change live domain settings, including purchases, DNS deletion, nameserver changes, unlocks, transfers, recovery, and auto-renew settings.

Mitigation: Require explicit user confirmation after showing the exact domain, price or setting, payment method, token use, and expected service impact before taking those actions.

Risk: Management tokens control domain operations and may be needed for future changes.

Mitigation: Tell the user to store any management token securely and avoid exposing it in shared logs, prompts, or public outputs.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/gregm711/skills/agentdomainservice)
- [ClawDaddy Service](https://clawdaddy.app)
- [ClawDaddy Agent Documentation](https://clawdaddy.app/llms.txt)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with HTTP request examples and JSON or TXT response examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include domain names, price quotes, payment method details, bearer-token usage, DNS records, nameserver settings, and service-impact guidance.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
