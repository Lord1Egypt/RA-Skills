## Description:

Explains code snippets in multiple programming languages, including syntax, logic, purpose, and implementation details, using a Dify chatflow.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhangwp1](https://clawhub.ai/user/zhangwp1)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to submit code snippets and receive structured explanations of syntax, control flow, intended behavior, and implementation details.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release evidence reports a concrete API-key-like default value and marks the package suspicious.

Mitigation: Review before installing, replace the default API key with a securely managed Dify key, rotate the exposed-looking key if it was ever real, and verify the Dify endpoint before sending sensitive code.

Risk: Code snippets may be sent to a configured Dify chatflow for explanation.

Mitigation: Confirm the endpoint and chatflow are trusted before submitting proprietary or sensitive source code.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zhangwp1/skills/dify-code-interpreter)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Structured natural-language explanation]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a code snippet as input and depends on the configured Dify endpoint and chatflow.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
