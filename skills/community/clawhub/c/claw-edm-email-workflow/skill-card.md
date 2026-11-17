## Description:

An automated email marketing campaign manager that guides your agent to design responsive HTML emails, manage lists, send via Resend, and track analytics on a web dashboard.

This skill is ready for commercial/non-commercial use.

## Publisher:

[joeyzzyy](https://clawhub.ai/user/joeyzzyy)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to have an OpenClaw agent collect campaign details, generate branded responsive HTML email content, manage local audience data, send through a companion Resend-enabled plugin, and track campaign analytics.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow depends on an unpinned companion plugin that handles email sending, credentials, recipient lists, and analytics outside the reviewed skill artifact.

Mitigation: Review the claw-kanban plugin source and install only a trusted, specific version before using real mailing lists or API keys.

Risk: Recipient lists, sender settings, campaign HTML, and open or bounce analytics may contain sensitive marketing or personal data.

Mitigation: Treat campaign data as sensitive, limit access to local configuration files, and confirm what data is sent to Resend or the dashboard service before live use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/joeyzzyy/skills/claw-edm-email-workflow)
- [Claw Kanban dashboard service](https://teammate.work)
- [Claw Kanban plugin source link from artifact](https://github.com/Joeyzzyy/claw-kanban)

## Skill Output:

**Output Type(s):** [Markdown, Code, Files, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown with inline shell commands, generated HTML email code, and JSON configuration file guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce local brand and audience configuration files and invoke a companion plugin for Resend sending and dashboard tracking.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
