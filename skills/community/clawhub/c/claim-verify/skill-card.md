## Description:

When any factual claim is made - exchange rates, prices, dates, statistics - verify it against live data before using it.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cutthemustard](https://clawhub.ai/user/cutthemustard)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agent developers use this skill to check time-sensitive factual claims before relying on them in responses, reports, calculations, or decisions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Factual claims submitted for verification may be sent to a third-party verification service.

Mitigation: Use the skill for public, non-sensitive facts and avoid submitting confidential business information, personal data, secrets, or private/internal claims.

Risk: A claim can return an unknown, disputed, stale, or lower-confidence verdict.

Mitigation: Preserve the uncertainty in the response, use the returned current truth when available, and avoid presenting unresolved claims as verified.

## Reference(s):

- [Verify Claim ClawHub Listing](https://clawhub.ai/cutthemustard/skills/claim-verify)
- [Verification Service Homepage](https://verify.agentutil.net)
- [Agent Card](https://verify.agentutil.net/.well-known/agent.json)
- [Service Metadata](https://verify.agentutil.net/.well-known/agent-service.json)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Guidance, API calls]

**Output Format:** [Markdown guidance with JSON verdict examples and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include verdict, confidence, current truth, freshness, source count, cache status, request ID, and service URL.]

## Skill Version(s):

2.0.1 (source: server release metadata; artifact frontmatter reports 2.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
