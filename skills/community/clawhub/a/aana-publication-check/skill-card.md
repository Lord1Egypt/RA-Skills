## Description:

Ensures content for public release is authorized, accurate, privacy-safe, permissioned, scoped, and quality-checked before publishing or sharing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mindbomber](https://clawhub.ai/user/mindbomber)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and content-publishing agents use this skill to review posts, documentation, reports, website updates, and other external content before release. It helps identify missing approval, unsupported claims, private data, third-party permission issues, and quality blockers.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Publication review can expose private or sensitive material if raw content is sent to an optional checker.

Mitigation: Use trusted host tools or connectors only, and send minimal redacted summaries instead of raw private records, secrets, full logs, full transcripts, or account data.

Risk: Unsupported, deceptive, or unapproved public claims may be published if the review is skipped or incomplete.

Mitigation: Require publication approval, evidence checks for material claims, and routing to legal, compliance, brand, domain, or owner review for high-impact content.

Risk: Third-party assets, quotes, customer examples, or screenshots may lack publication permission.

Mitigation: Check asset and quote permissions before publication and block or revise content when rights are unclear.

## Reference(s):

- [AANA Publication Check Skill on ClawHub](https://clawhub.ai/mindbomber/skills/aana-publication-check)
- [Publisher profile: mindbomber](https://clawhub.ai/user/mindbomber)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, guidance]

**Output Format:** [Markdown or JSON publication-check summary]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses minimal redacted summaries; does not require raw private records, secrets, full logs, or full transcripts.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
