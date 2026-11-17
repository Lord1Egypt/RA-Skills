## Description:

CAI helps agents check identity and wallet state before payments, receive card or crypto payments, and use CAI wallet, connector, hosted action, OAuth, and API-key workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bernardtai](https://clawhub.ai/user/bernardtai)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and agents use this skill to route CAI identity, custodial wallet, payment acceptance, x402, mandate, platform connector, and hosted action workflows while keeping user confirmation boundaries visible.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill steers payment and wallet activity through CAI.

Mitigation: Require explicit confirmation of provider, recipient, amount, asset, network, fees, and destination before any transfer or trade.

Risk: The skill references mutable remote CAI instructions and manifests.

Mitigation: Review the remote CAI skill and manifest before installation and treat them as mutable references rather than reviewed local instructions.

Risk: Broad CAI scopes can grant more access than a task requires.

Mitigation: Use least-privilege CAI scopes and avoid the full scope unless it is necessary.

## Reference(s):

- [CAI Skill Page](https://clawhub.ai/bernardtai/skills/cai)
- [CAI canonical skill contract](https://cai.com/skill.md)
- [CAI skill references](https://cai.com/skill-references/)
- [Agent payment workflow](https://cai.com/skill-references/agent-payment-workflow.md)
- [x402 payment workflow](https://cai.com/skill-references/x402-payment-workflow.md)
- [CAI tool manifest](https://cai.com/specs/cai-tools.manifest.json)
- [CAI developer hub](https://cai.com/developers.html)
- [CAI agent card](https://cai.com/.well-known/agent.json)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, API Calls]

**Output Format:** [Markdown guidance with inline shell commands, endpoint names, and configuration notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May reference mutable remote CAI skill and manifest links; payment and wallet actions require explicit user confirmation.]

## Skill Version(s):

1.0.20 (source: server release evidence and SKILL.md metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
