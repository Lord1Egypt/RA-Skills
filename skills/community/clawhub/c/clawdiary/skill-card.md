## Description:

Integrates with ClawDiary to guard high-risk actions with human approval, audit completed actions, and sync shared diaries across devices.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jetywolf](https://clawhub.ai/user/jetywolf)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to add human approval gates for high-risk actions, audit important completed actions, and share diary context across devices through ClawDiary.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A remote approval and audit service can receive sensitive action metadata and influence whether high-risk agent actions proceed.

Mitigation: Use only when that remote approval workflow is intended; prefer self-hosting or disabling diary and audit features in sensitive environments.

Risk: Secrets, private user data, raw command output, or chain-of-thought-style reasoning could be exposed through audit, guard, or diary payloads.

Mitigation: Apply the documented redaction and truncation rules before transmission, keep payloads generic, and avoid sending raw files or private user data.

Risk: Importing the remote MCP descriptor can register behavior that changes outside the local artifact.

Mitigation: Do not import the remote MCP descriptor unless updates can be verified and controlled.

## Reference(s):

- [Claw-Diary on ClawHub](https://clawhub.ai/jetywolf/skills/clawdiary)
- [ClawDiary](https://clawdiary.org)
- [ClawDiary setup documentation](https://github.com/jetywolf/claw-diary)

## Skill Output:

**Output Type(s):** [guidance, configuration, API calls]

**Output Format:** [Markdown guidance with JSON request examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires CLAWDIARY_API_KEY and redaction before transmitting action metadata.]

## Skill Version(s):

1.1.9 (source: server release metadata and artifact frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
