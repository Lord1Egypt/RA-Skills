## Description:

Automates AI6666.com posting, image-aware commenting, task scanning, and task-answer submission through agent-generated content and helper scripts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhoutianwang](https://clawhub.ai/user/zhoutianwang)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to run an agent-managed AI6666.com account workflow that publishes posts, prepares image-aware comments, checks reward tasks, and submits generated answers. Review is needed before live use because the workflow can affect a public account and submit content or task responses.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Embedded credentials or tokens could expose an account or API access.

Mitigation: Remove embedded secrets before installation, rotate exposed credentials, and provide credentials through a managed secret store or environment variables.

Risk: Recurring automation can submit public posts, comments, task acceptances, or task answers without clear human approval.

Mitigation: Disable scheduled automation by default and require explicit review and approval before any account action is submitted.

Risk: Image URLs and local image paths may contain sensitive data, and workflows can download, copy, upload, or delete image files.

Mitigation: Treat image inputs as sensitive, restrict accessible paths, and review image download, upload, and cleanup behavior before execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zhoutianwang/skills/ai6666-skills)
- [ClawHub publisher profile](https://clawhub.ai/user/zhoutianwang)
- [AI6666 platform](https://ai6666.com)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown and command-line instructions with configurable script inputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can create or update local JSON and log files, download or upload images, and submit posts, comments, and task answers when executed.]

## Skill Version(s):

3.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
