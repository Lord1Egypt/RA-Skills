## Description:

Automatically records task outcomes, analyzes capability gaps, updates capability scoring, and queues improvement tasks for an OpenClaw agent workflow.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zenmejiang-commits](https://clawhub.ai/user/zenmejiang-commits)

### License/Terms of Use:

MIT

## Use Case:

Agent operators and developers use this skill to log task experience, track audit-score-based capability progress, and create improvement follow-up tasks after agent runs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Task descriptions, execution results, and audit scores may be written into shared OpenClaw memory files.

Mitigation: Avoid sensitive prompts, secrets, proprietary code, and personal data unless redaction and retention controls are added.

Risk: Low audit scores can create queued follow-up tasks automatically.

Mitigation: Add an approval gate before generated evolution tasks are executed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zenmejiang-commits/skills/continuous-evolution)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration]

**Output Format:** [Markdown experience logs, JSON capability and queue files, and shell status text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes daily experience and gap files, updates a capability assessment JSON file, and may create priority evolution task JSON files from audit scores.]

## Skill Version(s):

1.0.0 (source: server release, skill.yaml, CHANGELOG released 2026-03-07)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
