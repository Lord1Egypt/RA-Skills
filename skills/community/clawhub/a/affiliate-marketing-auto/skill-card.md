## Description:

Automates affiliate product discovery, promotional content generation, tracking-link management, and revenue reporting for affiliate marketing workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lvjunjie-byte](https://clawhub.ai/user/lvjunjie-byte)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to find affiliate products, generate SEO and social promotional content, create UTM tracking links, and review revenue and conversion reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Affiliate platform credentials may be exposed if real API keys are placed directly in shared configuration or logs.

Mitigation: Use least-privilege keys, store secrets outside shared config, and avoid logging credential values.

Risk: Click tracking can collect IP addresses, user agents, referrers, and locations without sufficient privacy controls.

Mitigation: Add privacy notices, minimize collected fields, anonymize or aggregate identifiers where possible, and define retention controls before production use.

Risk: Flagged HTTP dependencies may carry known dependency risk.

Mitigation: Upgrade the npm dependencies identified by the security scan before production deployment.

Risk: Generated affiliate content may omit required disclosures or conflict with platform policies.

Mitigation: Review generated content for affiliate disclosures, accuracy, and each target platform's advertising rules before publishing.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/lvjunjie-byte/skills/affiliate-marketing-auto)
- [Publisher Profile](https://clawhub.ai/user/lvjunjie-byte)
- [Affiliate Documentation](https://docs.openclaw.ai/affiliate)
- [Artifact README](artifact/README.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown, JavaScript objects, configuration snippets, tracking URLs, and CSV/JSON/PDF report descriptors]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include product lists, generated promotional copy, UTM tracking links, click and conversion analytics, revenue reports, and exported report metadata.]

## Skill Version(s):

1.0.2 (source: ClawHub release evidence; artifact package files report 1.0.1 and artifact documentation reports 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
