## Description:

Public ClawHub text release for a Windows companion skill that bridges local AI CLIs and controlled workspace file operations, documenting the capability and setup path without including the local PowerShell execution layer.

This skill is ready for commercial/non-commercial use.

## Publisher:

[archibald80000-ai](https://clawhub.ai/user/archibald80000-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this documentation-first skill to understand how a separate Windows companion deployment can bridge local AI CLIs and guarded workspace file operations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The public ClawHub artifact does not include the local runtime layer that would mediate provider execution or workspace file access.

Mitigation: Review the separate local PowerShell and runtime package before deployment, especially execution boundaries and workspace file permissions.

Risk: Claude provider use depends on the user's local Claude CLI authentication and quota.

Mitigation: Confirm local provider installation, authentication, and quota before relying on Claude-backed execution.

## Reference(s):

- [ClawHub Skill Listing](https://clawhub.ai/archibald80000-ai/skills/cli-agent-bridge)
- [Approval Model Reference](references/auth-model.md)
- [Filesystem Operations Reference](references/fs-operations.md)
- [Provider Commands Reference](references/provider-commands.md)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Configuration instructions, Shell commands]

**Output Format:** [Markdown documentation with inline command and configuration references]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Text-only public release; runtime execution depends on a separate local companion package.]

## Skill Version(s):

0.2.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
