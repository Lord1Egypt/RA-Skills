## Description:

Agent Rate Limiter helps agents avoid 429 errors by checking local usage estimates, applying tier-based throttling, and using exponential backoff after rate-limit events.

This skill is ready for commercial/non-commercial use.

## Publisher:

[theagentwire](https://clawhub.ai/user/theagentwire)

### License/Terms of Use:


## Use Case:

Developers and agent operators use this skill to add a local rate-limit gate before expensive agent work, record estimated usage afterward, and pause or reduce activity when usage approaches a configured limit.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses heuristic local tracking rather than provider-side usage data, so estimates can be too high or too conservative.

Mitigation: Start with conservative limits, review status output, tune RATE_LIMIT_ESTIMATE for the account, and use the pause command after real 429 events.

Risk: Shared writable state files can cause multiple agent instances to overwrite or blend rate-limit history.

Mitigation: Set RATE_LIMIT_STATE to a private, per-instance JSON path and avoid shared writable directories.

Risk: Resetting or replacing the state file removes the skill's recorded usage history.

Mitigation: Use reset only when intentionally clearing history, and recheck status before resuming expensive agent work.

## Reference(s):

- [Agent Rate Limiter on ClawHub](https://clawhub.ai/theagentwire/skills/agent-rate-limiter)
- [theagentwire publisher profile](https://clawhub.ai/user/theagentwire)
- [The Agent Wire](https://theagentwire.ai)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance, JSON]

**Output Format:** [Markdown guidance with bash commands and JSON command responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses a local JSON state file and Python standard library commands; no API keys or external services are required.]

## Skill Version(s):

1.3.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
