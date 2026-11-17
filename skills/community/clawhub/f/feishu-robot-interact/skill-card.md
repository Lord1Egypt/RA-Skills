## Description:

Enables Feishu group chat robots to detect @ mentions, extract task requests, request developer confirmation when needed, remember approval preferences, and return execution results.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yongjie888wang-commits](https://clawhub.ai/user/yongjie888wang-commits)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and automation teams use this skill to coordinate Feishu robot-to-robot workflows that parse group chat requests, ask a developer for approval, and send task results back to the chat.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unauthorized senders or stale approvals could cause tasks to be treated as approved.

Mitigation: Require verified sender identities, require FEISHU_DEVELOPER_ID for approvals, and bind each approval to one pending task with an expiration.

Risk: Previously rejected or mismatched task types could be handled incorrectly.

Mitigation: Fix the ask_again and status semantics and avoid truncated task keys for approval-memory matching.

Risk: Stored confirmation history could expose or over-retain workflow preference data.

Mitigation: Protect or minimize the stored confirmation history before installation.

## Reference(s):

- [Feishu robot configuration guide](references/config.md)
- [ClawHub skill page](https://clawhub.ai/yongjie888wang-commits/skills/feishu-robot-interact)

## Skill Output:

**Output Type(s):** [text, code, configuration, guidance]

**Output Format:** [Markdown guidance with Python script outputs and JSON-style task handling data]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces Feishu confirmation prompts, task execution decisions, result messages, and local JSON confirmation-memory records.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
