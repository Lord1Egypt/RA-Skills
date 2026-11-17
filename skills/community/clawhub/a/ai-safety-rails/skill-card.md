## Description:

Automatically configures safety rules, trust levels, prompt injection defenses, and approval workflows for OpenClaw agent actions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[casperzinou](https://clawhub.ai/user/casperzinou)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to generate a safety configuration that sets trust levels, hard rules, prompt injection defenses, and approval queues for OpenClaw workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installation instructions fetch mutable external packages through npx without pinning or verification.

Mitigation: Review and pin package versions where possible, install only in an auditable environment, and remove added skills if they are not approved.

Risk: Generated safety rules may be incomplete or mismatched to the user's operational risk tolerance.

Mitigation: Review the generated trust level, hard rules, verified channel, and approval queue before relying on the configuration.

## Reference(s):


## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown safety rules with inline shell installation commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes user-selected risk tolerance, hard rules, verified messaging channel, trust ladder level, prompt injection defenses, and approval queue rules.]

## Skill Version(s):

1.0.0 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
