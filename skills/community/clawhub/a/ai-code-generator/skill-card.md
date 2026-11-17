## Description:

AI code generator using Plan-and-Solve + ReAct for generating complete, runnable code from requirements and specifications.

This skill is ready for commercial/non-commercial use.

## Publisher:

[banxian87](https://clawhub.ai/user/banxian87)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to turn natural language requirements into project structure, generated source files, tests, documentation, and next-step setup guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated code may be incorrect, insecure, or unsuitable for the target project without review.

Mitigation: Review generated files as untrusted output before running or merging them.

Risk: Generated project files or environment examples may overwrite existing work or expose sensitive values if copied directly.

Mitigation: Choose write locations deliberately, check for overwrites, and do not include secrets in prompts or generated .env files.

## Reference(s):


## Skill Output:

**Output Type(s):** [Code, Files, Markdown, Shell commands, Configuration instructions]

**Output Format:** [JSON-like project object with generated file entries and Markdown next-step instructions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include generated tests, README documentation, dependency guidance, and environment setup reminders depending on requested options.]

## Skill Version(s):

1.0.0 (source: package.json and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
