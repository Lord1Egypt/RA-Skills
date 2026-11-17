## Description:

Provides modern PHP 8.4 and Laravel guidance for architecture, Eloquent, migrations, queues, and testing in framework-based PHP applications.

This skill is ready for commercial/non-commercial use.

## Publisher:

[iliaal](https://clawhub.ai/user/iliaal)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to build and test framework-based PHP applications with Laravel, Eloquent, Blade, and Artisan, applying guidance on architecture, persistence, queues, and testing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Queue-worker guidance could process real jobs without environment safeguards.

Mitigation: Review the guidance to ensure it is limited to an isolated development setup and a controlled test job.

Risk: The session cleanup example may not match the application's retention needs.

Mitigation: Check the cleanup behavior against the application's retention requirements.

Risk: The security scan was partial because a local reference was unresolved.

Mitigation: Review the unresolved reference and the remaining skill content before use.

## Reference(s):

- [Laravel Ecosystem Patterns](artifact/references/laravel-ecosystem.md)
- [Testing Laravel (PHPUnit)](artifact/references/testing.md)
- [Feature Testing Patterns](artifact/references/feature-testing.md)
- [Mocking and Faking](artifact/references/mocking-and-faking.md)
- [Factory Patterns](artifact/references/factories.md)
- [Production Performance](artifact/references/production-performance.md)
- [Laravel Common Pitfalls](artifact/references/common-pitfalls.md)
- [Laravel Pitfalls: Deep Reference](artifact/references/pitfalls-deep.md)
- [Framework and Boundary Patterns](artifact/references/framework-patterns.md)
- [Persistence and Job Patterns](artifact/references/persistence-and-jobs.md)
- [Testing and Pitfall Checklist](artifact/references/testing-and-pitfalls.md)

## Skill Output:

**Output Type(s):** [Code, Guidance, Shell commands, Configuration instructions]

**Output Format:** [Markdown with PHP code examples, Laravel configuration, and command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Output is tailored to the Laravel development or testing task.]

## Skill Version(s):

5.1.6 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
