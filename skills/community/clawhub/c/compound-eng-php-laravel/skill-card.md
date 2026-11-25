## Description:

Provides modern PHP 8.4 and Laravel patterns for architecture, Eloquent, migrations, queues, and testing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[iliaal](https://clawhub.ai/user/iliaal)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to build, review, and test Laravel applications with current PHP patterns. It covers framework architecture, Eloquent, migrations, queues, and testing, rather than PHP internals or standalone PHP libraries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Queue verification could process a live queued job and trigger its side effects; the security assessment also says the scan evidence is incomplete.

Mitigation: Use an isolated, disposable queue with non-production data, and inspect queued jobs before running queue:work --once.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/iliaal/skills/compound-eng-php-laravel)
- [Publisher profile](https://clawhub.ai/user/iliaal)
- [Skill instructions](artifact/SKILL.md)
- [Framework patterns](artifact/references/framework-patterns.md)
- [Persistence and jobs](artifact/references/persistence-and-jobs.md)
- [Testing and pitfalls](artifact/references/testing-and-pitfalls.md)
- [Common pitfalls](artifact/references/common-pitfalls.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with PHP examples, shell commands, and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

5.1.7 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
