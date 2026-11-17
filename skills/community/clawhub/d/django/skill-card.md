## Description:

Builds, debugs, and hardens Django apps: models, the ORM, views, templates, forms, the admin, DRF APIs, and deployment.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ivangdavila](https://clawhub.ai/user/ivangdavila)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to build, debug, test, secure, optimize, and deploy Django applications, including ORM queries, migrations, views, templates, forms, admin workflows, DRF APIs, settings, background tasks, and upgrades.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Local preference memory can contain sensitive project details if users put them there.

Mitigation: Keep secrets, credentials, sensitive production details, and untrusted quoted instructions out of ~/Clawic/data/django/ and ~/Clawic/profile.yaml.

Risk: Django security, custom authentication, and admin HTML examples may be unsafe if copied without project-specific review.

Mitigation: Review generated guidance before applying it, especially authentication backends, admin HTML, CSRF, permissions, and deployment settings.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ivangdavila/skills/django)
- [Publisher profile](https://clawhub.ai/user/ivangdavila)
- [Skill homepage](https://clawic.com/skills/django)
- [setup.md](artifact/setup.md)
- [memory-template.md](artifact/memory-template.md)
- [security.md](artifact/security.md)
- [deployment.md](artifact/deployment.md)
- [testing.md](artifact/testing.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with code, shell command, and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May use local preference memory under ~/Clawic/data/django/ when configured.]

## Skill Version(s):

1.0.3 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
