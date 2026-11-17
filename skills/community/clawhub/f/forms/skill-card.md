## Description:

Create, validate, and deploy forms with field types, validation patterns, conditional logic, and platform integrations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ivangdavila](https://clawhub.ai/user/ivangdavila)

### License/Terms of Use:


## Use Case:

Developers, builders, and operators use this skill to design mobile-friendly forms, choose form platforms, generate implementation snippets, add validation, and plan integrations or self-hosted deployments.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Form submissions can contain personal or regulated data.

Mitigation: Define consent, retention, deletion, encryption, and access controls before collecting real submissions.

Risk: Integration examples may expose or mishandle API tokens and webhook secrets if copied directly.

Mitigation: Keep credentials server-side and out of URLs, use HTTPS, verify webhook signatures, and review snippets before production use.

Risk: Self-hosted deployment examples may rely on moving package or container versions.

Mitigation: Pin Docker images and npm package versions before deploying.

Risk: Notifications and integrations can over-share submission contents.

Mitigation: Send only the fields needed for the workflow and avoid forwarding full submission contents to chat or email by default.

## Reference(s):

- [Forms Skill Page](https://clawhub.ai/ivangdavila/skills/forms)
- [Publisher Profile](https://clawhub.ai/user/ivangdavila)
- [SKILL.md](artifact/SKILL.md)
- [Code Generation for Forms](artifact/code.md)
- [Form Integrations](artifact/integrations.md)
- [Form Platforms Comparison](artifact/platforms.md)
- [Self-Hosted Form Solutions](artifact/selfhosted.md)
- [Form Types by Use Case](artifact/types.md)
- [Form Validation Patterns](artifact/validation.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline code blocks, shell commands, JSON, YAML, TypeScript, Dart, SQL, and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces implementation guidance and examples for form design, validation, integrations, storage, and deployment; generated snippets should be reviewed before production use.]

## Skill Version(s):

1.0.0 (source: release evidence, artifact frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
