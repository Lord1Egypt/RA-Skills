## Description:

This skill guides agents to fact check and verify claims, current dates, versions, API references, URLs, and technical details before returning user-facing work.

This skill is ready for commercial/non-commercial use.

## Publisher:

[futurizerush](https://clawhub.ai/user/futurizerush)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, technical writers, and agents use this skill to verify factual and technical claims before shipping answers, documentation, code guidance, or release notes. It is most useful when outputs mention versions, API shapes, field names, CLI flags, dates, URLs, or other claims that can become stale.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Verification may involve outbound requests to package registries, GitHub, documentation sites, APIs, or user-provided URLs, which can expose request metadata or response data.

Mitigation: Avoid checking sensitive internal endpoints or authenticated APIs unless the user explicitly intends that verification and accepts the exposure risk.

Risk: Fact-checking may still leave claims unverified when the required source, tool, or access is unavailable.

Mitigation: Label unsupported claims as unverified or unverifiable rather than presenting them as confirmed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/futurizerush/skills/fact-check-verify)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown verification reports, concise status labels, and optional shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include verified, corrected, unverified, or unverifiable labels with evidence notes.]

## Skill Version(s):

0.1.1 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
