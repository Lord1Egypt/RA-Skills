## Description:

Build, debug, or review repeatable Box API integrations and agent workflows for efficient calls, bulk work, and 429 handling.

This skill is ready for commercial/non-commercial use.

## Publisher:

[iskysun96](https://clawhub.ai/user/iskysun96)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to design and review Box API integrations that reduce unnecessary calls, manage bulk jobs and rate limits, and preserve access controls and result coverage.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Implementations based on the guidance may change Box content or mishandle access tokens.

Mitigation: Review copy, move, update, upload, webhook, and token-handling workflows before use with business content.

Risk: Bulk requests or poorly coordinated retries may trigger rate limits or duplicate uncertain writes.

Mitigation: Bound shared concurrency, honor Retry-After, persist per-item outcomes, and reconcile uncertain writes before retrying.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/iskysun96/skills/box-integration-best-practices)
- [Box API rate limits](https://developer.box.com/guides/api-calls/permissions-and-errors/rate-limits)
- [Box marker-based pagination](https://developer.box.com/guides/api-calls/pagination/marker-based)
- [Box metadata query limitations](https://developer.box.com/guides/metadata/queries/limitations)
- [Box Platform Activity report](https://support.box.com/hc/en-us/articles/4415109521171-Platform-Activity-Report)
- [Box token downscoping](https://developer.box.com/guides/authentication/tokens/downscope)

## Skill Output:

**Output Type(s):** [Guidance, Text]

**Output Format:** [Markdown or text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Advisory only; the skill does not execute Box actions.]

## Skill Version(s):

1.0.0 (source: ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
