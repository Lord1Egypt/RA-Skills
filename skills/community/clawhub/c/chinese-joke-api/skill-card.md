## Description:

Fetches humorous Chinese jokes from third-party APIs such as Hitokoto and jokeapi.cn with timeout and error-handling guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[djttt](https://clawhub.ai/user/djttt)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to fetch and format Chinese joke or humor text from public third-party joke APIs, with examples for Bash and Python usage.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill makes outbound HTTPS requests to third-party joke services.

Mitigation: Install only in environments where external network access to those services is allowed.

Risk: Returned jokes are untrusted remote content.

Mitigation: Review or filter returned text before using it in sensitive, user-facing, or policy-constrained contexts.

Risk: Third-party APIs may be slow, rate-limited, or unavailable.

Mitigation: Use timeouts, error handling, and fallback behavior as shown in the artifact guidance.

## Reference(s):

- [Chinese Joke Api on ClawHub](https://clawhub.ai/djttt/skills/chinese-joke-api)
- [Hitokoto](https://hitokoto.cn/)
- [jokeapi.cn](https://jokeapi.cn/)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Code, Guidance]

**Output Format:** [Markdown guidance with Bash and Python examples; runtime output is plain text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses outbound HTTPS requests to third-party joke services and formats returned remote content.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
