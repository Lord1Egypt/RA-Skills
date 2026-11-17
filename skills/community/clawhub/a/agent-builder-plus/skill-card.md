## Description:

Build high-performing OpenClaw agents end-to-end with comprehensive safety features.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ykaixu](https://clawhub.ai/user/ykaixu)

### License/Terms of Use:


## Use Case:

Developers and agent builders use this skill to interview for, design, generate, register, and test OpenClaw agent workspaces with persona files, operating rules, memory guidance, heartbeat behavior, guardrails, and model-provider configuration notes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Optional systemd setup can introduce root-level persistence.

Mitigation: Remove the sudo systemd section or require explicit operator approval and review before enabling any service.

Risk: Generated workflows may include commits, pushes, file deletion, policy-file edits, outbound messages, or private-service checks.

Mitigation: Require explicit approval before those actions and keep heartbeat or monitoring tasks narrowly scoped.

Risk: Workspace and model-provider examples can lead users to place credentials in generated files.

Mitigation: Keep real credentials out of workspace files and use the intended OpenClaw credential or auth-profile locations.

## Reference(s):

- [OpenClaw agent workspace](references/openclaw-workspace.md)
- [OpenClaw agent file templates](references/templates.md)
- [Agent Architecture Patterns](references/architecture.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline code blocks and generated workspace file content]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces OpenClaw workspace files, registration and verification commands, safety checklists, and acceptance-test prompts.]

## Skill Version(s):

1.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
