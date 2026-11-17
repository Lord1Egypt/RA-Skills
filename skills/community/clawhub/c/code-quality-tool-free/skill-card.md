## Description:

Provides code style guidance, basic security checks, and accessibility review points for developers who need quick code-quality feedback.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and small teams use this skill to perform lightweight code-quality reviews covering naming and formatting conventions, common security checks, and accessibility checklist items before committing or reviewing code.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can read project files and run local shell commands for quality checks.

Mitigation: Review proposed commands before execution, scope scans to intended directories, and confirm before running broad repository-wide checks.

Risk: Security checks may detect secrets or tokens in source files.

Mitigation: Report file locations and issue categories without printing full secret values.

Risk: The artifact includes optional Git pre-commit hook creation, which can persistently affect local development workflow.

Mitigation: Create the hook only after explicit user approval and document how to remove or disable it.

Risk: Security evidence flags unclear local-only versus external API language.

Mitigation: Treat network or API behavior as unconfirmed until the publisher clarifies whether any external service is contacted.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/code-quality-tool-free)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown report with command snippets and structured findings]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May read project files and propose local grep/find-based checks; results should avoid exposing full secret values.]

## Skill Version(s):

1.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
