## Description:

Code Review Pro prompts an agent to run a Chinese-language code review across logic, security, performance, and style with confidence-scored findings.

This skill is ready for commercial/non-commercial use.

## Publisher:

[softboypatrick](https://clawhub.ai/user/softboypatrick)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to have an agent review code for logical errors, security vulnerabilities, performance bottlenecks, and style issues. It is intended to return structured findings only when confidence is at least 70%, including severity, location, risk, and suggested remediation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Output may default to Chinese, which can reduce usability for teams expecting another language.

Mitigation: Explicitly tell the invoking agent what output language to use when applying the skill.

Risk: Review findings are advisory and confidence-scored, so issues or optimization suggestions may still need human validation before code changes.

Mitigation: Have a developer review findings and run relevant tests before applying suggested changes.

## Reference(s):

- [Code Review Pro ClawHub page](https://clawhub.ai/softboypatrick/skills/code-review-pro)
- [Source skill definition](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown with structured issue entries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Chinese-language findings; severe issues and suggestions include confidence, location, risk, and remediation guidance when applicable.]

## Skill Version(s):

1.0.0 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
