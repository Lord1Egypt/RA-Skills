## Description:

Helps an AI assistant record session milestones and decisions in a verifiable evidence chain and export a session evidence package.

This skill is ready for commercial/non-commercial use.

## Publisher:

[djboy520](https://clawhub.ai/user/djboy520)

### License/Terms of Use:

MIT-0

## Use Case:

People and teams using AI assistants can record key session events, decisions, and outputs, then export a package for independent verification.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Durable, exportable session records may expose private conversation details.

Mitigation: Obtain explicit start/stop consent, keep secrets and private text out of the log, and review it before attachment or export.

Risk: Auto mode and broad session cues may record activity without a fresh prompt.

Mitigation: Enable auto mode only after explicit opt-in and honor requests to stop recording.

Risk: Default credential handling may read a locally stored secret automatically.

Mitigation: Review credential settings before enabling the skill and avoid exposing secrets in evidence.

## Reference(s):

- [AEP Session Evidence on ClawHub](https://clawhub.ai/djboy520/skills/aep-session-evidence)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Guidance]

**Output Format:** [Markdown guidance and CLI commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create a session log and exportable .aep evidence package.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
