## Description:

Ensures accurate current date handling by requiring a session_status check before queries involving today, now, relative time, or current events.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dbottrader](https://clawhub.ai/user/dbottrader)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to make assistants resolve the current date before answering time-sensitive or current-event queries. It helps reduce stale-year searches and unsupported date assumptions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill assumes a session_status tool exists for current-date resolution.

Mitigation: Use it in environments that provide session_status, or adapt the guidance to the available current-date tool before release.

Risk: Time-sensitive answers may become more dependent on successful current-date and real-time tool calls.

Mitigation: When tools fail or return incomplete data, require the agent to disclose uncertainty instead of filling gaps from prior knowledge.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dbottrader/skills/cp8-time-awareness)

## Skill Output:

**Output Type(s):** [guidance, text]

**Output Format:** [Markdown instructions for agent behavior]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Constrains current-date retrieval, time-sensitive search construction, and uncertainty disclosure when current-date tools fail.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
