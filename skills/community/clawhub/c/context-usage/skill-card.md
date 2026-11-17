## Description:

Checks the current session's context window usage, including model name, estimated token usage, utilization percentage, cache data, and status guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[goog](https://clawhub.ai/user/goog)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to check how much of the current session context window is in use and decide whether monitoring or compaction guidance is needed.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may suggest using a separate compaction helper when context usage is high.

Mitigation: Review that separate skill independently before following its guidance.

## Reference(s):


## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown summary]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include model name, token usage, cache hit rate, utilization percentage, and context status.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
