## Description:

Provides a Chinese-language checklist for reviewing code quality, maintainability, correctness, tests, severity, and embedded-systems concerns.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tlreal](https://clawhub.ai/user/tlreal)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering reviewers use this skill to structure Chinese-language code reviews, classify findings by severity, and summarize whether changes are ready to proceed.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may activate around code submission or task completion and produce Chinese-language review reports when another language is expected.

Mitigation: Use it when a Chinese-language structured code review is desired, or override the response language in the agent or user instruction.

Risk: The checklist can influence code acceptance decisions through severity-labeled findings and conclusions.

Mitigation: Review findings against project requirements and tests before making merge or release decisions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/tlreal/skills/code-review1)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown code review report in Chinese]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Severity-grouped findings with overview, strengths, and conclusion when applicable.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
