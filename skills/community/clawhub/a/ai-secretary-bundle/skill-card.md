## Description:

AI Secretary Bundle helps busy professionals manage email summaries, schedule reminders, daily news briefings, and task tracking through an OpenClaw-based assistant workflow.

This skill is ready for commercial/non-commercial use.

## Publisher:

[daimingvip-a11y](https://clawhub.ai/user/daimingvip-a11y)

### License/Terms of Use:

MIT-0

## Use Case:

External users and professionals use this skill to coordinate routine administrative workflows, including mailbox review, recurring reminders, news digests, and task summaries. It is aimed at personal productivity and lightweight office support rather than autonomous unsupervised decision-making.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow can access sensitive mailbox, calendar, and task information.

Mitigation: Use app-specific passwords or OAuth, keep configuration files out of version control, and restrict mailbox permissions to the minimum needed.

Risk: Recurring scheduled jobs may read private data or trigger actions without timely user review.

Mitigation: Review or disable cron jobs before use and require confirmation before sending emails or sharing generated summaries.

Risk: The bundle depends on separately installed skills and an install script that were not fully reviewed in the provided artifact.

Mitigation: Review dependency skills and install scripts before installation, and prefer pinned versions or trusted releases.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/daimingvip-a11y/skills/ai-secretary-bundle)
- [Publisher Profile](https://clawhub.ai/user/daimingvip-a11y)
- [AI Secretary Documentation](https://docs.clawhub.com/ai-secretary)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown and configuration-oriented assistant responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include suggested commands, YAML configuration snippets, schedule definitions, email or task summaries, and action recommendations.]

## Skill Version(s):

1.0.0 (source: server release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
