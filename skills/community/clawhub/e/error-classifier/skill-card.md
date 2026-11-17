## Description:

Classifies tool, API, build, test, and context-window errors into transient, permanent, validation, or context categories and returns the matching handling action.

This skill is ready for commercial/non-commercial use.

## Publisher:

[paudyyin](https://clawhub.ai/user/paudyyin)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use this skill to classify runtime, API, validation, and context-length failures and choose whether to retry, report to the user, request a fix, or compress context.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Raw exception messages may contain tokens, headers, URLs, or private file paths.

Mitigation: Redact sensitive values before forwarding classifier messages to users, models, logs, or telemetry.

Risk: Unknown errors default to transient handling and may be retried.

Mitigation: Set retry limits and review retry behavior before using the helper around production API calls or side-effecting operations.

## Reference(s):

- [Retry Strategies](references/retry_strategies.md)
- [ClawHub Skill Page](https://clawhub.ai/paudyyin/skills/error-classifier)

## Skill Output:

**Output Type(s):** [text, code, guidance]

**Output Format:** [Python classification values, handling-action objects, and concise human-readable handling messages]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses fixed priority order for overlapping matches and exponential backoff delays of 1, 2, and 4 seconds for retryable transient errors.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
