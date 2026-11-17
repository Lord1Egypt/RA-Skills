## Description:

Requires ordinary agent responses to be drafted, reviewed by a second AI instance, and revised before delivery, with draft text sent to the configured model API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[keaneyan](https://clawhub.ai/user/keaneyan)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to require a second-model critique of draft agent responses before delivery, helping catch factual errors, missing caveats, logical issues, and tone problems.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Draft responses may be sent to another model provider during review.

Mitigation: Use a trusted local reviewer model for sensitive sessions, or avoid installing the skill when working with confidential data, credentials, personal information, or proprietary code.

Risk: Mandatory review of nearly every ordinary response can add latency and token cost.

Mitigation: Install only when a second-model review step is desired and the added operational cost is acceptable.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/keaneyan/skills/adversary-review)

## Skill Output:

**Output Type(s):** [Guidance, Text]

**Output Format:** [Markdown instructions and reviewer critique text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Adds a second-model review step before ordinary responses; may add latency and token cost.]

## Skill Version(s):

1.2.0 (source: frontmatter, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
