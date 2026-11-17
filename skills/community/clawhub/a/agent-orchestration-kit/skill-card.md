## Description:

Set up and manage multi-agent task orchestration on OpenClaw with async dispatch, leader coordination, real-time tracking, and approval workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kuan0808](https://clawhub.ai/user/kuan0808)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to scaffold a leader-led multi-agent team, dispatch work asynchronously, track task files, and gate externally impactful results behind owner approval.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup can change OpenClaw configuration, create persistent workspaces, and enable broad cross-session visibility.

Mitigation: Run the config patcher in dry-run mode first, inspect the openclaw.json diff, restrict session visibility where supported, and keep the generated backup for rollback.

Risk: The orchestration kit gives some agents command-oriented operational authority.

Mitigation: Deny exec for non-operational agents, keep irreversible actions behind explicit owner approval, and review each agent's tool-deny settings before use.

Risk: The security evidence reports an installer path-scoping weakness.

Mitigation: Use a simple safe workspace name, avoid untrusted paths or shell metacharacters in setup arguments, and review generated workspace paths before applying changes.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kuan0808/skills/agent-orchestration-kit)
- [Architecture](references/architecture.md)
- [Approval Workflow](references/approval-workflow.md)
- [Communication Signals](references/signals.md)
- [Brief Templates](references/brief-templates.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with bash commands and helper scripts for OpenClaw workspace and configuration setup]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces setup instructions, workspace templates, task-tracking conventions, callback protocols, and OpenClaw configuration changes when the included scripts are run.]

## Skill Version(s):

0.2.0 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
