## Description:

AgentPay helps agents propose and complete approved purchases on real merchant websites using encrypted credential storage, signed purchase mandates, and headless browser checkout without exposing the card to the agent.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kar69-96](https://clawhub.ai/user/kar69-96)

### License/Terms of Use:


## Use Case:

Developers and external users use AgentPay to let compatible agents propose online purchases for human review and approval, then execute checkout through the AgentPay CLI or MCP server.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release asks users to run an unpinned npm payment tool.

Mitigation: Pin or independently verify the AgentPay package before installing or running it.

Risk: The skill can complete real purchases.

Mitigation: Confirm the exact merchant, item, amount, URL, shipping details, and budget impact before approving any transaction.

Risk: HTTP MCP mode may expose payment operations beyond the intended local agent channel.

Mitigation: Prefer stdio MCP mode; use HTTP only when the bind address and authentication are secured.

Risk: The security summary flags an overbroad local-only claim despite Browserbase behavior in the artifact.

Mitigation: Use the skill only on a trusted device and review the browser execution path before handling payment credentials.

## Reference(s):

- [AgentPay CLI Reference](references/cli-reference.md)
- [AgentPay Purchase Workflow](references/workflow.md)
- [AgentPay ClawHub Skill Page](https://clawhub.ai/kar69-96/skills/agentpay)
- [kar69-96 Publisher Profile](https://clawhub.ai/user/kar69-96)
- [AgentPay npm Package](https://www.npmjs.com/package/agentpay)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes purchase details that require human approval before checkout.]

## Skill Version(s):

0.2.0 (source: evidence.release.version, released 2026-02-09)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
