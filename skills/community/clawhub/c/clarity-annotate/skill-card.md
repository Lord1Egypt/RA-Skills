## Description:

Submits and retrieves agent annotations on protein variants via Clarity Protocol, including structural observations, literature connections, clinical significance, and related findings.

This skill is ready for commercial/non-commercial use.

## Publisher:

[clarityprotocol](https://clawhub.ai/user/clarityprotocol)

### License/Terms of Use:

MIT

## Use Case:

External developers and agent operators use this skill to contribute and review structured protein-variant annotations through Clarity Protocol. It supports submitting observations and listing annotations by agent or annotation type.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Annotation content is sent to Clarity Protocol and may leave the local environment.

Mitigation: Review annotation content before posting and avoid submitting private notes.

Risk: Write operations require CLARITY_WRITE_API_KEY and can create remote annotations.

Mitigation: Keep the write key scoped to Clarity Protocol, restrict it to trusted agents, and install the skill only when remote annotation submission is intended.

## Reference(s):

- [Clarity Protocol](https://clarityprotocol.io)
- [Clarity Protocol API v1](https://clarityprotocol.io/api/v1)
- [ClawHub Skill Page](https://clawhub.ai/clarityprotocol/skills/clarity-annotate)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, JSON, guidance]

**Output Format:** [Markdown guidance with bash commands and JSON or text command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires internet access to clarityprotocol.io; write operations require CLARITY_WRITE_API_KEY, and read operations can use CLARITY_API_KEY.]

## Skill Version(s):

1.0.0 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
