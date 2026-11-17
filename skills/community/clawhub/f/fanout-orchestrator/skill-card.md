## Description:

Dispatches independent research, analysis, writing, or coding sub-tasks across parallel specialist streams and synthesizes the results.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oonyl](https://clawhub.ai/user/oonyl)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to split suitable tasks into independent parallel streams, route them to specialist agents, and combine the results into a concise synthesis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generic activation terms such as parallel may trigger fan-out for tasks that do not benefit from multiple streams.

Mitigation: Confirm the task decomposes into independent streams and has a clear synthesis step before dispatching parallel work.

Risk: Parallel streams can drift beyond the requested scope or return conflicting results.

Mitigation: Scope each stream narrowly, wait for all streams to finish, and synthesize tradeoffs or contradictions before returning the final answer.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Markdown with prose, structured result summaries, and command or code snippets when useful.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces per-stream results, synthesis, tradeoffs or contradictions, and a practical read for the user.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
