## Description:

Build, modify, and debug feapder 1.9.2 spiders and projects with the framework's native patterns.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fqxue](https://clawhub.ai/user/fqxue)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to write, modify, and debug feapder 1.9.2 crawler projects, including AirSpider, Spider, TaskSpider, BatchSpider, request parsing, persistence, settings, and CLI workflows. It is especially tailored for Chinese feapder requests and defaults to Chinese logs and comments where helpful.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill relies on an older feapder 1.9.2 crawler snapshot with unsafe Redis parsing paths noted by the security evidence.

Mitigation: Use it only for feapder 1.9.2 work, avoid shared or untrusted Redis for task queues and response caches, and patch or disable eval-based paths before sensitive use.

Risk: Crawler examples and debugging workflows can expose live session cookies or database credentials.

Mitigation: Do not paste live cookies into shell examples, keep database credentials out of shell history and source files, and prefer environment-managed secrets.

Risk: Generated guidance may include database or task-state updates that affect crawler persistence.

Mitigation: Test DB and task updates against non-production systems before using the resulting crawler code in production.

## Reference(s):

- [ClawHub skill release page](https://clawhub.ai/fqxue/skills/feapder)
- [Spider types and scaffolding](references/spider-types-and-scaffolding.md)
- [Code patterns](references/code-patterns.md)
- [Settings, debugging, and source anchors](references/settings-debugging-and-sources.md)
- [Vendored feapder 1.9.2 README](references/vendor/feapder-1.9.2/README.md)
- [feapder upstream project](https://github.com/Boris-code/feapder)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with code blocks, shell commands, and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce Chinese log messages and comments by default for feapder examples.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
