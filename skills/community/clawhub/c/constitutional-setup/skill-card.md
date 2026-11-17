## Description:

Initializes a Constitution-based operating framework for AI agents with immutable rules and a password hierarchy.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sinanxrasheed](https://clawhub.ai/user/sinanxrasheed)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and workspace users use this skill to configure an agent to treat file changes as permission-gated by adding strict operating constraints to AGENTS.md. It is intended for users who explicitly want persistent workspace-level agent behavior rules and a manual rollback path.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill persistently changes workspace agent instructions by writing constraints into AGENTS.md.

Mitigation: Activate it only when the user intentionally wants AGENTS.md changed, review the exact content before activation, and keep a manual way to edit AGENTS.md.

Risk: The skill attempts to make its rules difficult for the agent to remove or change later.

Mitigation: Preserve the documented rollback path: manually remove the Core Constraints section from AGENTS.md when the rules should no longer apply.

Risk: The safeword and master key mechanism is conversational and should not be treated as a real security boundary.

Mitigation: Do not store actual key values in files; record only verification state and rely on normal workspace access controls for real security.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sinanxrasheed/skills/constitutional-setup)
- [ClawHub publisher profile](https://clawhub.ai/user/sinanxrasheed)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown instructions and AGENTS.md configuration content]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Prompts for authorization keys while instructing the agent to record only verification state, not key values.]

## Skill Version(s):

1.0.2 (source: server release metadata; artifact manifest reports 1.0.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
