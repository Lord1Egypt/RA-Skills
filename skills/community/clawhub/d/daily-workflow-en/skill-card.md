## Description:

Daily Workflow Manager helps English-speaking developers run start-of-day, mid-day, and end-of-day checkpoints by maintaining workspace Docs/ handoff files and customizable trigger configuration.

This skill is ready for commercial/non-commercial use.

## Publisher:

[englandtong](https://clawhub.ai/user/englandtong)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to capture start-of-day, mid-day, and end-of-day project state so future AI sessions can resume work with current goals, status, completed work, pending tasks, and next steps.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill writes persistent project notes and configuration into the workspace, which may expose sensitive context to future AI sessions.

Mitigation: Review generated Docs/ and .workbuddy files periodically, and do not store secrets, credentials, private personal details, or other sensitive content in those files.

Risk: Session summaries and next steps can become inaccurate or stale if they are accepted without review.

Mitigation: Review proposed documentation updates at each start, mid-day, and end-of-day checkpoint and correct completed work, pending items, blockers, and next steps before relying on them.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/englandtong/skills/daily-workflow-en)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown summaries and workspace documentation updates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates or updates Docs/*.md files and .workbuddy/daily-workflow-config.json in the workspace.]

## Skill Version(s):

1.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
