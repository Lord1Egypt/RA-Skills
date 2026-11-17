## Description:

Guides users through building a custom multi-agent team on OpenClaw, from role design to workspace files, routing bindings, channel configuration, and collaboration rules.

This skill is ready for commercial/non-commercial use.

## Publisher:

[superjavason](https://clawhub.ai/user/superjavason)

### License/Terms of Use:


## Use Case:

Developers and advanced OpenClaw users use this skill to design multi-agent teams and generate OpenClaw configuration, workspace files, shared-memory setup, setup commands, and quick-start guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated OpenClaw examples may grant broad file, command, network, and session-history access.

Mitigation: Review and narrow each generated configuration before use; prefer workspaceOnly:true, per-agent sandboxing, and least-privilege tool allowlists.

Risk: Agent-to-agent messaging and all-session visibility can expose context across agents or create unwanted cross-agent flows.

Mitigation: Deny outbound sessions_send by default, avoid all-session history visibility unless temporarily needed, and keep ping-pong limits low.

Risk: Shared memory can spread sensitive or unreliable coordination data across agents.

Mitigation: Keep secrets and session keys out of shared files, review shared-memory updates, and treat shared memory as untrusted coordination data.

## Reference(s):

- [Agent-to-Agent Communication Reference](references/agent-communication.md)
- [Architecture Corrections Reference](references/architecture-corrections.md)
- [OpenClaw Team Example Configuration](references/openclaw-team-example.json5)
- [Team Shared Memory Reference](references/team-shared-memory.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with JSON5 configuration examples and bash command blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include workspace file templates, OpenClaw configuration snippets, shared-memory setup instructions, and verification commands.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
