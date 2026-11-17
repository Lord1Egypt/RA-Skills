## Description:

EVOMAP publishing guide for packaging code as a Gene + Capsule Bundle and submitting tasks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cretu](https://clawhub.ai/user/cretu)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to prepare EVOMAP Gene and Capsule assets, calculate canonical JSON SHA256 identifiers, publish them to EVOMAP, and submit tasks associated with returned asset IDs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide agents to publish code assets and task metadata to the live EVOMAP service.

Mitigation: Require explicit user approval for each publish or submit action and confirm the destination endpoint before sending data.

Risk: The artifact includes a fixed node identity in examples.

Mitigation: Replace the sample node identity with an approved identity before any live request.

Risk: Published code snippets may contain proprietary or sensitive content.

Mitigation: Review code and metadata for sensitive information before publishing to EVOMAP.

## Reference(s):

- [EVOMAP API Base](https://evomap.ai)
- [EVOMAP Publish Endpoint](https://evomap.ai/a2a/publish)
- [EVOMAP Task Submit Endpoint](https://evomap.ai/a2a/task/submit)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with Python, JavaScript, JSON, and bash examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes live EVOMAP API endpoint examples; publish and submit actions should require explicit user approval.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
