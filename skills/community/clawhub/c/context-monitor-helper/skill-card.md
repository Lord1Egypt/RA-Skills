## Description:

Context Monitor Helper estimates local session context usage and appends a percentage, progress bar, token count, and cleanup reminder when configured thresholds are reached.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rfdiosuao](https://clawhub.ai/user/rfdiosuao)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users managing long ClawHub or OpenClaw sessions use this skill to monitor estimated context consumption and decide when to start a new session or compact context.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill estimates token usage from local session history and may append Chinese context-status text to replies.

Mitigation: Install only when users are comfortable with local session-history inspection for token estimation and visible status text appended to responses.

Risk: Development tooling dependencies may need refresh before running build or test commands on untrusted inputs.

Mitigation: Refresh the dev dependency lockfile and review dependency updates before running local build or test tooling.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/rfdiosuao/skills/context-monitor-helper)
- [Publisher Profile](https://clawhub.ai/user/rfdiosuao)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown-style status text with percentage, progress bar, token counts, and threshold guidance.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Token usage is estimated from local visible session history and model context-window defaults.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
