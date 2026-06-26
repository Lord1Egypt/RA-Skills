## Description: <br>
Create, validate, and deploy forms with field types, validation patterns, conditional logic, and platform integrations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ivangdavila](https://clawhub.ai/user/ivangdavila) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, product teams, and operators use this skill to choose form platforms, define fields, generate form code, apply validation patterns, and connect submissions to webhooks, CRMs, databases, notifications, or self-hosted storage. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated forms and integration snippets may route submissions, personal data, or regulated data to unintended tools or storage locations. <br>
Mitigation: Confirm submission destinations before use, avoid sending sensitive fields to chat or broad automation tools, and define retention, deletion, access control, and encryption requirements for stored form data. <br>
Risk: Webhook, CRM, database, notification, and email examples involve API keys, tokens, and webhook secrets. <br>
Mitigation: Keep secrets out of prompts and logs, use environment variables or secret managers, use least-privilege tokens, require HTTPS, and verify webhook signatures and timestamps. <br>
Risk: Code, Docker, and package examples are starting points and may be incomplete for production hardening. <br>
Mitigation: Review generated snippets before deployment, pin package and container versions, enforce server-side validation, apply rate limiting and CSRF protection, and scan file uploads when enabled. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ivangdavila/forms) <br>
- [Forms skill definition](artifact/SKILL.md) <br>
- [Form types by use case](artifact/types.md) <br>
- [Form platforms comparison](artifact/platforms.md) <br>
- [Code generation for forms](artifact/code.md) <br>
- [Form validation patterns](artifact/validation.md) <br>
- [Form integrations](artifact/integrations.md) <br>
- [Self-hosted form solutions](artifact/selfhosted.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with inline code, shell commands, JSON, YAML, SQL, and TypeScript examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Instruction-only skill; generated snippets and configuration examples should be reviewed before use.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
