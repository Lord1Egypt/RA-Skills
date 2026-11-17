## Description:

Check Claude Code / Claude Max usage limits when a user asks about usage, limits, quota, or remaining Claude capacity.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aligurelli](https://clawhub.ai/user/aligurelli)

### License/Terms of Use:


## Use Case:

Developers and agent users use this skill to check logged-in Claude Code or Claude Max quota from the local Claude CLI and report usage and reset times in a concise table.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads Claude usage and spending details from a locally logged-in Claude CLI, which may reveal account, plan, quota, or spending information.

Mitigation: Install and run it only when this visibility is intended, and review the reported output before sharing it.

Risk: The skill depends on an installed, logged-in Claude CLI and an interactive PTY; it may fail or require manual login when those prerequisites are missing.

Mitigation: Confirm the `claude` binary is installed, run the login flow manually if needed, and use an agent environment that supports PTY sessions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/aligurelli/skills/claude-usage-checker)
- [Publisher profile](https://clawhub.ai/user/aligurelli)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown table with concise explanatory text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports usage percentages, reset times, and extra usage spending details when available from the Claude CLI.]

## Skill Version(s):

1.3.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
