## Description:

Designs API rate limiting strategies including token bucket, sliding window, fixed window, leaky bucket, and Redis-backed distributed rate limiting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[charlie-morrison](https://clawhub.ai/user/charlie-morrison)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to choose rate limiting algorithms, design per-user, per-IP, per-endpoint, and tier-based limits, and draft Redis-backed implementation guidance for APIs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated rate-limiter code or settings may be incorrect for a production API.

Mitigation: Review generated code and configuration before deployment, especially Redis connection settings and failover behavior.

Risk: Proxy IP handling or bypass rules may weaken enforcement if copied without environment-specific review.

Mitigation: Validate trusted proxy configuration, X-Forwarded-For handling, health-check bypasses, and monitoring exceptions against the deployment topology.

Risk: Access-log analysis commands may expose or process sensitive production log data.

Mitigation: Run log analysis only on approved data sources and follow internal controls for sensitive logs.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with tables, code blocks, shell commands, and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include rate-limit recommendations, endpoint overrides, Redis-backed implementation examples, response header guidance, and access-log analysis commands.]

## Skill Version(s):

1.0.1 (source: release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
