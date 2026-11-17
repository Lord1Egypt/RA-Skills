## Description:

A Chinese-language code review helper that reviews submitted code for code quality, potential bugs, performance issues, security vulnerabilities, and maintainability.

This skill is ready for commercial/non-commercial use.

## Publisher:

[olina1ye](https://clawhub.ai/user/olina1ye)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering teams use this skill to review pull requests, inspect code before refactoring, coach newcomers, and assess implementation risk in Chinese.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill needs read access to the code being reviewed, which may expose proprietary or sensitive source code to the reviewing agent.

Mitigation: Grant read access only to the intended repository or files, and avoid submitting secrets or unrelated sensitive code.

Risk: Automated review findings or suggested rewrites may be incomplete, incorrect, or unsuitable for the target codebase.

Mitigation: Treat findings and code examples as reviewer assistance, and require a human engineer to validate changes before merging or execution.

Risk: The skill is documented as a Chinese-language helper and does not define behavior for other output languages.

Mitigation: Use it where Chinese review output is acceptable, or verify language behavior before relying on it in multilingual workflows.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/olina1ye/skills/code-review-zh)

## Skill Output:

**Output Type(s):** [text, markdown, code, guidance]

**Output Format:** [Markdown review findings with optional code examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Chinese-language review output; requires read access to the code being reviewed.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
