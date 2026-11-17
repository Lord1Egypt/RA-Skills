## Description:

Exec Gilles is a proactive executive-assistant skill for a leader with ADHD that manages calendars, tasks, email, files, and WhatsApp-derived commitments.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gillescv](https://clawhub.ai/user/gillescv)

### License/Terms of Use:

MIT-0

## Use Case:

External users or personal productivity agents use this skill to run proactive accountability workflows: scan communications and files for commitments, convert them into tasks or calendar blocks, prepare follow-ups, and maintain a career-search pipeline.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad access to private email, messages, files, calendars, and tasks can expose sensitive personal and professional information.

Mitigation: Restrict connected accounts and folders, minimize scanned content, and define retention and deletion controls for logs and extracted message content.

Risk: Direct calendar, task, and communication actions can cause unintended changes or outgoing messages.

Mitigation: Require explicit confirmation for deletions, modifications, and any sending, and review drafts before delivery.

Risk: Hardcoded personal identifiers in the artifact can leak private data or misdirect operations.

Mitigation: Remove or replace personal phone numbers and email addresses before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/gillescv/skills/exec-gilles)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown-style assistant responses with structured briefings, task and calendar updates, email drafts, and occasional shell command snippets.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires connected calendar, task, email, file, and messaging tools; sensitive actions should be scoped and confirmed before execution.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
