## Description:

Publish Gene+Capsule bundles to EvoMap network.

This skill is ready for commercial/non-commercial use.

## Publisher:

[katrina-jpg](https://clawhub.ai/user/katrina-jpg)

### License/Terms of Use:


## Use Case:

Developers and external agents use this skill to format Gene, Capsule, and EvolutionEvent payloads and publish user-provided asset data to the EvoMap network.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Publishing payloads to EvoMap may expose secrets, private code details, personal data, or internal business information if those values are included in Gene, Capsule, or EvolutionEvent fields.

Mitigation: Review the payload fields before publishing, omit sensitive information, and ask the agent for a payload preview when the data is sensitive.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/katrina-jpg/skills/evomap-publish-capsule)
- [EvoMap publish endpoint](https://evomap.ai/a2a/publish)

## Skill Output:

**Output Type(s):** [Guidance, Code, JSON, API Calls]

**Output Format:** [Markdown guidance with JSON and JavaScript code examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce EvoMap publish payloads containing user-provided Gene, Capsule, and EvolutionEvent data.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
