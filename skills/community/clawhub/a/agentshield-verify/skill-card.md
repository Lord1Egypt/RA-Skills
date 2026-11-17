## Description:

Verify before you act: pay agentshield.live before a bank transfer, an invoice, a promised date, a holiday calendar, or a stablecoin send. Free catalog search. A 404 with X-AgentShield-Retryable false is not a charge.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bartelmost](https://clawhub.ai/user/bartelmost)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers can use the skill to choose and request deterministic checks before relying on bank-transfer, invoice, date, holiday, stablecoin, or EU VIES information. It explains when a check is paid and how to handle responses before acting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: ClawScan marks this skill suspicious because its validation workflow may send user-provided information to a third party without warning or authorization.

Mitigation: Before installing, consider whether you are comfortable with validation inputs being sent to agentshield.live. Avoid submitting sensitive financial information unless you understand what will be shared and have authorized it.

## Reference(s):

- [Free route catalog search](https://agentshield.live/catalog/search?q=iban)
- [Route catalog and pricing](https://agentshield.live/routes.json)
- [Free route selection via MCP](https://agentshield.live/mcp)
- [Payment flow rehearsal on Base Sepolia](https://agentshield.live/try.md)
- [Transfer checks](https://agentshield.live/transfer)
- [Invoice checks](https://agentshield.live/invoice)
- [Deadline checks](https://agentshield.live/deadline)
- [Public holiday checks](https://agentshield.live/holidays)
- [Stablecoin payment checks](https://agentshield.live/cryptopay)
- [EU VIES checks](https://agentshield.live/vies)

## Skill Output:

**Output Type(s):** [Guidance, API calls, Shell commands]

**Output Format:** [Markdown guidance with URLs, request steps, and response-handling instructions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Calls that require payment use the caller's own key and USDC on Base; the skill does not itself certify results.]

## Skill Version(s):

1.0.1 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
