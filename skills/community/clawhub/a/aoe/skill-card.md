## Description:

Manage AI coding agent sessions via Agent of Empires (aoe)

This skill is ready for commercial/non-commercial use.

## Publisher:

[njbrake](https://clawhub.ai/user/njbrake)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to launch, organize, monitor, and communicate with AI coding-agent sessions through Agent of Empires. It provides command-line workflows for session lifecycle, groups, profiles, worktrees, and output capture.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: YOLO mode skips the agent tool's permission prompts, allowing actions to proceed without those checks.

Mitigation: Use YOLO mode only when its permission tradeoff is intended, and review agent actions and changes.

Risk: Purging a session can permanently delete its worktree or branch.

Mitigation: Check the selected session and deletion flags before running a purge command.

## Reference(s):

- [Agent of Empires project](https://github.com/agent-of-empires/agent-of-empires)
- [Sandbox guide](https://github.com/agent-of-empires/agent-of-empires/blob/main/docs/guides/sandbox.md)
- [Agent of Empires on ClawHub](https://clawhub.ai/njbrake/skills/aoe)

## Skill Output:

**Output Type(s):** [Shell commands, Guidance, JSON]

**Output Format:** [Markdown guidance with shell command examples and documented JSON output shapes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands and guidance are tailored to the requested agent-session management task.]

## Skill Version(s):

1.25.0 (source: release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
