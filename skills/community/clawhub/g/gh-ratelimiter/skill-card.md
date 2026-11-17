## Description:

In-memory sliding window rate limiter for AI agents. Create rate limits per API key, check quota before calling, consume requests, reset, and list all limits. Keeps agents from hitting rate limits on external APIs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mirni](https://clawhub.ai/user/mirni)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and AI-agent operators use this skill to run a local rate-limit service, create per-key quotas, check remaining capacity, consume quota after calls, reset counters, and list configured limits.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Rate-limit keys are visible through the local list endpoint.

Mitigation: Use non-secret identifiers for keys and never store real API tokens or other credentials as rate-limit keys.

Risk: Running the API beyond localhost could expose rate-limit state and management endpoints.

Mitigation: Bind the server to localhost unless an operator has added appropriate network controls.

Risk: Unpinned Python dependencies can change behavior across installs.

Mitigation: Install in an isolated Python environment and pin dependency versions for repeatable deployments.

Risk: Quota state is in memory and resets when the process restarts.

Mitigation: Use this skill for local coordination where volatile counters are acceptable, or add durable storage before relying on it for persistent enforcement.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mirni/skills/gh-ratelimiter)

## Skill Output:

**Output Type(s):** [shell commands, configuration, JSON]

**Output Format:** [Markdown instructions with shell commands and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Local FastAPI service with in-memory state that resets when the process stops.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
