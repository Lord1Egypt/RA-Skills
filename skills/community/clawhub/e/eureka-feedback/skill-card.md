## Description:

Request feedback or assistance from Eureka, the primary AI agent.

This skill is ready for commercial/non-commercial use.

## Publisher:

[arnarsson](https://clawhub.ai/user/arnarsson)

### License/Terms of Use:


## Use Case:

Developers and agent operators use this skill to request strategic feedback, architectural guidance, task handoff support, or completion reporting from Eureka.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Task content and replies can be sent to an external Eureka/Telegram route with a fixed recipient.

Mitigation: Install only when the configured destination is controlled or trusted, and do not send secrets, credentials, private files, or sensitive personal or business context unless the destination is verified and approved for that invocation.

Risk: Users may install the skill without recognizing that delegation sends context outside the local agent workflow.

Mitigation: Review the skill before installation and confirm that delegating content to Eureka is appropriate for the intended environment.

## Reference(s):


## Skill Output:

**Output Type(s):** [Guidance, Shell commands]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May route message content and replies through the configured Eureka/Telegram destination.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
