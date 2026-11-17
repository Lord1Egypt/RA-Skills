## Description:

Prevents AI agents from hitting API rate limits by checking local usage tiers, recording requests, and backing off after 429 responses.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kakaxiazai](https://clawhub.ai/user/kakaxiazai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to add a local gate before expensive LLM operations, record request usage, and pause or downshift work before or after rate-limit errors.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The local state file may expose usage patterns or be altered when stored in a shared or world-writable location.

Mitigation: Use a private RATE_LIMIT_STATE path with restricted permissions and avoid shared directories.

Risk: Resetting the limiter deletes prior rate-limit history, which can make near-term estimates less reliable.

Mitigation: Run reset only when intentionally clearing history, then start with conservative limits until new usage data accumulates.

Risk: Cron or prompt integrations can change when an agent pauses, resumes, or skips work.

Mitigation: Review integrations before enabling them so throttling decisions remain under operator control.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kakaxiazai/skills/api-agent-rate-limiter-1-3-1)
- [The Agent Wire](https://theagentwire.ai)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, JSON, Guidance]

**Output Format:** [Markdown instructions with bash examples and JSON command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses a local JSON state file and configurable environment variables; no external services or API keys.]

## Skill Version(s):

1.0.0 (source: server release evidence; artifact metadata version 1.3.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
