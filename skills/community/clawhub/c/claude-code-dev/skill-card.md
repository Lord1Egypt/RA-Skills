## Description:

Guides OpenClaw agents in using Claude Code for coding, debugging, refactoring, and pull request review through ACP integration or PTY-backed CLI sessions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xwz119](https://clawhub.ai/user/xwz119)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to route programming requests from OpenClaw to Claude Code, configure ACP or CLI sessions, and manage coding workflows such as debugging, refactoring, and pull request review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Always-approved coding-agent access can allow Claude Code to act beyond the intended task scope.

Mitigation: Run the skill in a dedicated, low-privilege workspace, review diffs and logs, and use tighter approval settings when interactive approval is available.

Risk: Persistent or background sessions can continue work with broad workspace or credential access.

Mitigation: Avoid production checkouts and broad credentials, prefer pinned plugin versions where possible, and close sessions when the coding task is complete.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xwz119/skills/claude-code-dev)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration]

**Output Format:** [Markdown guidance with bash, JSON, and command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include background session commands, approval settings, and budget controls for Claude Code workflows.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
