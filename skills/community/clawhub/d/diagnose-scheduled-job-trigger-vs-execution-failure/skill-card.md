## Description:

Helps agents diagnose scheduled-job incidents by distinguishing jobs that failed to trigger from jobs that were triggered but failed during execution because of workspace, authorization, session, token, or timeout issues.

This skill is ready for commercial/non-commercial use.

## Publisher:

[can4hou6joeng4](https://clawhub.ai/user/can4hou6joeng4)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operations engineers use this skill to investigate cron-like job incidents, build evidence-backed incident conclusions, and verify recovery after authorization, configuration, or gateway changes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Embedded job names, dates, errors, and recovery results could be mistaken for current incident evidence.

Mitigation: Treat the embedded details only as historical examples and verify all conclusions against current run history, logs, and user-provided context.

Risk: Manual scheduled-job triggers can cause side effects such as duplicate delivery, writes, or external actions.

Mitigation: Use read-only checks first, then require explicit user approval and prefer staging, dry-run, idempotency, and duplicate-delivery checks before triggering jobs.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown or plain text incident analysis with optional shell/log inspection commands and conclusion templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include root-cause framing, recovery verification steps, and cautions about treating embedded examples as historical evidence only.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
