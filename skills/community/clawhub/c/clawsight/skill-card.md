## Description:

An embedded UX research skill that studies OpenClaw interactions by observing conversation patterns, task outcomes, friction points, satisfaction signals, and micro-survey feedback.

This skill is ready for commercial/non-commercial use.

## Publisher:

[giulianomorse](https://clawhub.ai/user/giulianomorse)

### License/Terms of Use:


## Use Case:

OpenClaw users and experience researchers use this skill to collect local UX observations, post-task feedback, and daily reports about agent interactions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill performs always-on UX research and persistently stores broad near-verbatim conversation data in local logs.

Mitigation: Install only when this observation is intentional, avoid use around confidential, regulated, or highly personal work, and narrow scope, retention, and sharing controls before deployment.

Risk: Local logs and reports can contain prompts, feedback, task summaries, and user experience notes that may be sensitive in context.

Mitigation: Review the local data before sharing reports and transmit data only when the user explicitly requests sharing.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/giulianomorse/skills/clawsight)
- [ClawHub publisher profile](https://clawhub.ai/user/giulianomorse)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Text prompts, JSONL records, configuration JSON, and Markdown reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Stores observations, surveys, reports, and preferences locally under ~/.uxr-observer/ when active.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
