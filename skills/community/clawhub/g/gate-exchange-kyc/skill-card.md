## Description:

Gate KYC portal routing skill that helps users find the Gate identity verification portal and directs KYC actions to the official portal.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gate-exchange](https://clawhub.ai/user/gate-exchange)

### License/Terms of Use:

MIT-0

## Use Case:

External users and support-facing agents use this skill to route Gate KYC and identity verification requests to the official portal. It provides portal guidance only and does not perform verification, review documents, or approve KYC status.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill depends on mutable external runtime instructions.

Mitigation: Review the skill and referenced runtime guidance before deployment, and keep the deployed behavior limited to KYC portal routing.

Risk: Users may try to submit identity documents or API secrets in chat.

Mitigation: Direct users to the official Gate portal or support and do not request, accept, or process sensitive KYC documents or API secrets in chat.

Risk: Users could submit sensitive identity information to the wrong domain.

Mitigation: Tell users to verify they are on the official Gate domain before submitting KYC information.

## Reference(s):

- [Gate KYC MCP Specification](references/mcp.md)
- [Scenarios](references/scenarios.md)
- [Gate KYC Portal](https://www.gate.com/myaccount/profile/kyc_home)
- [ClawHub Skill Page](https://clawhub.ai/gate-exchange/skills/gate-exchange-kyc)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown guidance with an official portal URL and brief next steps]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Does not collect identity documents, mutate KYC status, or approve verification.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
