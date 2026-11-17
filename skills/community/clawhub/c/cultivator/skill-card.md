## Description:

藏在戒指中的戒指老爷爷，为使用者（主角）提供修行中的帮助和指导，传授修炼的相关知识。

This skill is ready for commercial/non-commercial use.

## Publisher:

[imomoe233](https://clawhub.ai/user/imomoe233)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill as a cultivation-themed life and programming assistant that answers normal questions first, then appends lightweight roleplay progress, daily tasks, experience, inventory, and knowledge tracking.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill persistently profiles conversations and gamified life/task history without clear consent, deletion, retention, or sensitive-data controls.

Mitigation: Install only with informed opt-in, keep the profile local and inspectable, and prefer a version with clear export, delete, retention, and no-storage controls.

Risk: Conversation history, task logs, images, and profile fields may capture secrets, credentials, medical, financial, or highly personal information.

Mitigation: Avoid sharing sensitive information while the skill is active, redact private details before persistence, and disable or delete storage when handling sensitive topics.

Risk: Automatic task and image matching can misclassify user activity or record inaccurate progress.

Mitigation: Require user confirmation for ambiguous or sensitive task evidence and keep completion rewards reversible through profile inspection and edits.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/imomoe233/skills/cultivator)
- [SKILL.md](artifact/SKILL.md)
- [Daily task templates](artifact/templates/daily_tasks.json)
- [Initial cultivator data](artifact/cultivator_data.json)

## Skill Output:

**Output Type(s):** [text, markdown, json, shell commands, guidance]

**Output Format:** [Markdown-style assistant responses with cultivation status text and JSON-backed profile/task updates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May read and rewrite a persistent local cultivator_data.json profile and use date commands for daily task refreshes.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
