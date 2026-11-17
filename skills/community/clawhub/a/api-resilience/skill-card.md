## Description:

Guides agents in handling unreliable external APIs with retry backoff, rate limiting, circuit breakers, and graceful degradation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhaoxinghua09-cell](https://clawhub.ai/user/zhaoxinghua09-cell)

### License/Terms of Use:

MIT-0 (ClawHub listing); MIT for code; documentation and theory all rights reserved

## Use Case:

Developers and agent builders use this bilingual guide and simulated demo to plan retries, backoff, circuit breaking, and fallbacks when external services time out, rate-limit, or fail intermittently.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad timeout and reliability triggers may load this skill for general questions.

Mitigation: Check that the user's task involves unreliable external calls before applying its guidance.

Risk: Unreviewed resilience changes to live APIs can affect credentials, writes, deployments, or publishing.

Mitigation: Review production changes and their effects on live services before execution.

## Reference(s):

- [API Resilience on ClawHub](https://clawhub.ai/zhaoxinghua09-cell/skills/api-resilience)
- [LGD theory (conceptual background)](https://github.com/zhaoxinghua09-cell/lgd-theory)

## Skill Output:

**Output Type(s):** [Guidance, Code, Shell commands]

**Output Format:** [Markdown guidance and code examples; optional demo console text or JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Bilingual English and Chinese guidance; demo simulates failures rather than calling external APIs.]

## Skill Version(s):

1.0.5 (source: server-resolved ClawHub release; bundled frontmatter says 1.0.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
