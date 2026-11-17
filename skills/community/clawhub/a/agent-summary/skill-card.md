## Description:

Agent Summary periodically checks subagent status and recent session history to generate concise progress summaries for active workers.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wangxiaofei860208-source](https://clawhub.ai/user/wangxiaofei860208-source)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and coordinators use this skill to monitor active subagents and present short progress summaries only when worker state changes, completes, or fails.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads recent subagent session history to create progress summaries, which may expose sensitive worker context to the coordinating agent.

Mitigation: Install it only in workspaces where subagent status review is intended, and limit summary inputs to the latest relevant worker messages.

Risk: Overly frequent progress checks can create unnecessary noise or token usage.

Mitigation: Follow the artifact guidance to poll no more than every 30 seconds, report only changes or terminal states, and respect quiet hours.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wangxiaofei860208-source/skills/agent-summary)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown status summaries with short text labels and optional workflow guidance.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Intended summaries are 3-5 words, update at most every 30 seconds, and are suppressed during quiet hours when configured.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
