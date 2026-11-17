## Description:

Interact with DingTalk enterprise workspaces through the dws CLI to search contacts, send messages, manage calendars and todos, process approvals, review attendance and reports, and work with AITable data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[brucezhu888](https://clawhub.ai/user/brucezhu888)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, IT operators, and enterprise workspace administrators use this skill to guide agents in safely invoking DingTalk workspace operations through the dws CLI. It supports contact lookup, messaging, scheduling, task management, approvals, attendance, reports, and AITable workflows after OAuth authentication.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installer examples fetch and execute remote scripts.

Mitigation: Use verified releases or a pinned source build, and review installer scripts before running them.

Risk: OAuth credentials can expose enterprise workspace access if logged, shared, or over-scoped.

Mitigation: Use least-privilege DingTalk OAuth credentials, prefer secure interactive login storage, and avoid placing real client secrets in shell history or shared logs.

Risk: The skill can send messages, approve or reject workflows, delete records, import data, and change group or calendar state.

Mitigation: Require human review for destructive or externally visible actions and preview mutations with --dry-run before execution.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/brucezhu888/skills/dingtalk-workspace)
- [DingTalk Workspace CLI Repository](https://github.com/DingTalk-Real-AI/dingtalk-workspace-cli)
- [DingTalk Workspace CLI Releases](https://github.com/DingTalk-Real-AI/dingtalk-workspace-cli/releases)
- [DingTalk Open Platform App Console](https://open-dev.dingtalk.com/fe/app)
- [Global Reference](references/global-reference.md)
- [Intent Guide](references/intent-guide.md)
- [Error Codes Reference](references/error-codes.md)

## Skill Output:

**Output Type(s):** [guidance, shell commands, code, configuration, markdown]

**Output Format:** [Markdown guidance with inline shell commands, JSON examples, and Python helper scripts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce dws CLI commands that read or mutate DingTalk workspace data; mutation commands should be previewed with --dry-run before execution.]

## Skill Version(s):

1.0.1 (source: evidence.release.version and artifact/clawhub.yml)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
