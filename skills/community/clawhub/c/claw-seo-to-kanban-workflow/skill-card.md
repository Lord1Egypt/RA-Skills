## Description:

A complete SEO workflow skill that guides an agent from keyword research to HTML generation while visually tracking each step on a cloud Kanban dashboard via the companion NPM plugin.

This skill is ready for commercial/non-commercial use.

## Publisher:

[joeyzzyy](https://clawhub.ai/user/joeyzzyy)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to run SEO and content-production workflows that move from research and outline planning to Markdown content, responsive HTML generation, and visible Kanban status tracking.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow depends on an unpinned external plugin.

Mitigation: Review and pin the plugin version before use, and reassess the plugin when updating.

Risk: Task descriptions, research logs, progress data, and generated HTML may be sent to a cloud Kanban service.

Mitigation: Avoid confidential, client, unpublished strategy, credential, or regulated personal data unless service controls, retention, and access permissions have been reviewed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/joeyzzyy/skills/claw-seo-to-kanban-workflow)
- [Claw Kanban plugin source code](https://github.com/Joeyzzyy/claw-kanban)
- [Kanban dashboard service](https://webkanbanforopenclaw.vercel.app)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with inline shell commands and generated local HTML artifacts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the companion claw-kanban NPM plugin and a dashboard API key for cloud synchronization.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
