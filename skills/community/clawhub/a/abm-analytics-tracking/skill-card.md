## Description:

Helps agents set up, improve, and audit analytics tracking, conversion measurement, event tracking, UTM strategy, GA4, and Google Tag Manager implementations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mariokarras](https://clawhub.ai/user/mariokarras)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, marketers, and growth teams use this skill to define tracking plans, event taxonomies, UTM conventions, GA4/GTM setup steps, validation checklists, and privacy-aware analytics implementation guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Analytics implementations can accidentally send PII, secrets, payment details, or unnecessary persistent identifiers to analytics or ad platforms.

Mitigation: Review event properties and data layer payloads before deployment, remove sensitive fields, and collect only data needed for the stated measurement decision.

Risk: Marketing and analytics tags can violate consent or privacy requirements when loaded before appropriate user consent.

Mitigation: Gate analytics and marketing tags behind consent where required, use consent mode or a consent management platform, and confirm regional privacy requirements before rollout.

## Reference(s):

- [Event Library Reference](references/event-library.md)
- [GA4 Implementation Reference](references/ga4-implementation.md)
- [Google Tag Manager Implementation Reference](references/gtm-implementation.md)
- [Google Analytics recommended events](https://support.google.com/analytics/answer/9267735)

## Skill Output:

**Output Type(s):** [text, markdown, code, configuration, guidance]

**Output Format:** [Markdown with tables, checklists, and inline JavaScript examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include tracking plans, event naming conventions, GTM data layer examples, GA4 setup guidance, and validation steps.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact frontmatter reports 1.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
