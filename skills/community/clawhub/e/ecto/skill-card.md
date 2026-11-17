## Description:

Ghost.io Admin API CLI for managing blog posts, pages, tags, and content.

This skill is ready for commercial/non-commercial use.

## Publisher:

[visionik](https://clawhub.ai/user/visionik)

### License/Terms of Use:

MIT

## Use Case:

Developers, site operators, and agents use Ecto to manage Ghost blogs from the command line, including posts, pages, tags, images, webhooks, and site data. It supports multi-site workflows, markdown input, JSON output for scripting, and environment-based configuration overrides.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can give an agent broad authority over a live Ghost site, including publishing, deleting, scheduling, image upload, and webhook operations.

Mitigation: Use a staging site first, verify the selected --site value before write operations, and require review before publish, delete, schedule, image upload, or webhook commands.

Risk: Ghost Admin API keys are powerful secrets and may be stored in local configuration or supplied through environment variables.

Mitigation: Treat Admin API keys as secrets, avoid pasting them into shared prompts or logs, and scope access to the minimum site configuration needed.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/visionik/skills/ecto)
- [Ghost](https://ghost.io)
- [README](artifact/README.md)
- [Skill Instructions](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, JSON, Guidance]

**Output Format:** [Markdown guidance with CLI commands, configuration examples, and optional JSON command output.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May issue commands that read or modify a configured Ghost site, depending on the selected command and site configuration.]

## Skill Version(s):

0.1.0 (source: server release metadata and changelog, released 2026-01-26)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
