## Description:

Error Recovery - Strategies for handling failures gracefully

This skill is ready for commercial/non-commercial use.

## Publisher:

[hanxiao-bot](https://clawhub.ai/user/hanxiao-bot)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to guide agents through resilient handling of rate limits, billing failures, provider overload, context overflow, role-ordering corruption, transient HTTP failures, and tool errors.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sensitive or unnecessary private data may be placed into MEMORY.md when following session recovery advice.

Mitigation: Avoid storing secrets or unnecessary private data in MEMORY.md, and review memory content before use or sharing.

Risk: Recovery patterns can hide persistent failures if errors are suppressed or retries are unbounded.

Mitigation: Log failures, keep retries bounded, use fallback or circuit breaker behavior, and escalate persistent errors for review.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/hanxiao-bot/skills/error-recovery)

## Skill Output:

**Output Type(s):** [guidance, markdown, code]

**Output Format:** [Markdown guidance with JavaScript code examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Provides retry, fallback, circuit breaker, tool failure, and session recovery patterns.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
