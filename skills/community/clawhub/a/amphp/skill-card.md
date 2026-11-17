## Description:

Helps coding agents write and migrate non-blocking async PHP with AMPHP v3, Revolt Event Loop, and the broader amphp/* ecosystem.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rekryt](https://clawhub.ai/user/rekryt)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and coding agents use this skill to generate, review, and migrate PHP code for AMPHP v3 async I/O, HTTP and WebSocket services, database access, pipelines, workers, tests, and related package setup.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Copyable examples may lead agents to produce unsafe file upload or credential-handling patterns.

Mitigation: Require sanitized upload filenames, environment-based secrets, and review of generated PHP before production use.

Risk: Generated server examples may expose development services or log sensitive data if used without review.

Mitigation: Use localhost-only development binds by default, avoid sensitive logging, and require explicit confirmation before deployment-facing changes.

Risk: Filesystem or database examples may become destructive when adapted to real projects.

Mitigation: Require confirmation before running destructive file or database commands and review generated code paths before execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/rekryt/skills/amphp)
- [README](README.md)
- [AMPHP v2 to v3 Migration](docs/v2-v3.md)
- [Common Mistakes and Gotchas](docs/common-mistakes.md)
- [Package Overview](docs/packages.md)
- [Constructor Signatures](docs/constructors.md)
- [Namespaces](docs/namespaces.md)
- [Blocking vs Async Replacements](resources/blocking-vs-async.md)
- [Advanced Patterns](references/advanced-patterns.md)
- [Class Examples](references/class-examples.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with PHP code blocks, Composer commands, and configuration notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Targets PHP 8.1+, AMPHP v3, revolt/event-loop ^1, and amphp/amp ^3.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
