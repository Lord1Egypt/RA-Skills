## Description:

Absolute Mode changes an assistant's communication style to terse, high-density responses with configurable lite, full, and ultra intensity levels.

This skill is ready for commercial/non-commercial use.

## Publisher:

[samuellie](https://clawhub.ai/user/samuellie)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to make assistant responses more concise while preserving safety overrides for security warnings, destructive actions, and ambiguous prompts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The communication mode can activate unintentionally when users ask for phrases such as "max efficiency".

Mitigation: Confirm intent when activation is ambiguous and use "stop absolute mode" or "return to normal" to exit.

Risk: Highly compressed responses can reduce context around security, destructive actions, or ambiguous requests.

Mitigation: Suspend the mode for safety warnings, destructive actions, and clarification needs as specified by the artifact.

## Reference(s):


## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown or plain text responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Configurable intensity levels: lite, full, ultra.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
