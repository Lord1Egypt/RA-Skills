## Description:

Run Django management commands (migrate, showmigrations, makemigrations, check, version, logs, readonly) or Django ORM queries on any configured Django project.

This skill is ready for commercial/non-commercial use.

## Publisher:

[manojrammurthy](https://clawhub.ai/user/manojrammurthy)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to inspect and administer configured Django projects, including migrations, model and URL discovery, settings checks, logs, user listings, and ORM queries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can receive administrative access to the selected Django project and database.

Mitigation: Install only from a trusted publisher, verify the configured project and database before use, and keep read-only mode enabled unless write actions are intentionally needed.

Risk: The django-claw shell path should be treated as arbitrary Python execution rather than a safe read-only query tool.

Mitigation: Avoid using shell execution on production systems and review requested code before running it.

Risk: Setup may make persistent configuration changes for the OpenClaw environment.

Mitigation: Review the setup behavior before installation and confirm any saved project paths, settings modules, and gateway environment variables.

## Reference(s):

- [Django Claw on ClawHub](https://clawhub.ai/manojrammurthy/skills/django-claw-skill)
- [OpenClaw](https://openclaw.ai)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown with fenced raw script output and a one-line plain-English summary]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include Django management command results, database or model listings, log excerpts, setup configuration prompts, and error messages.]

## Skill Version(s):

0.1.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
