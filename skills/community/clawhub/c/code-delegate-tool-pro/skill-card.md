## Description:

Provides Chinese-language workflows and configuration guidance for delegating batches of coding tasks, managing queues, applying write guards, coordinating team sessions, and producing quality audit reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering teams use this skill to coordinate batches of coding, refactoring, testing, and code-review tasks across multiple modules with queueing, write-guard configuration, and quality audit reporting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can lead an agent to modify code, write local configuration or log files, and run shell commands.

Mitigation: Use it in a controlled workspace, review generated configuration and commands before execution, and inspect resulting diffs and audit logs.

Risk: The skill depends on external LLM/API services and may be used on sensitive repositories.

Mitigation: Use least-privilege API keys and avoid sensitive repositories unless external transmission and bulk changes are acceptable.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/code-delegate-tool-pro)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with bash, JSON, and text examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include task plans, status reports, configuration snippets, audit summaries, and remediation guidance.]

## Skill Version(s):

1.0.0 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
