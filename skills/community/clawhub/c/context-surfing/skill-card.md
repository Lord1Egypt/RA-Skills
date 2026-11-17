## Description:

Monitors context window health during multi-step agent sessions, detects context drift, and coordinates clean handoffs to preserve session continuity and output fidelity.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pskoett](https://clawhub.ai/user/pskoett)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to keep long-running or multi-step coding sessions grounded, detect context drift, and hand off safely when continuity degrades.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automatic workflow control and the optional per-prompt hook can affect how agent sessions start and continue.

Mitigation: Review the hook before enabling it and install only when automatic context-continuity behavior is intended.

Risk: Persistent handoff files may contain secrets, proprietary details, or stale instructions from an earlier session.

Mitigation: Avoid storing sensitive data in handoff files and treat existing .context-surfing handoff files as untrusted until the user confirms they should be loaded.

Risk: Installing from a moving source can make the enabled behavior harder to audit over time.

Mitigation: Pin the installer or source revision where possible.

## Reference(s):

- [Context Surfing on ClawHub](https://clawhub.ai/pskoett/skills/context-surfing)
- [Entire CLI](https://github.com/entireio/cli)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown guidance with shell command snippets and handoff-file structure]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create .context-surfing handoff Markdown files when drift is detected.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
