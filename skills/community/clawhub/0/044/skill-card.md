## Description:

Helps agents set up, improve, audit, and debug analytics tracking for GA4, Google Tag Manager, conversion measurement, event tracking, UTM strategy, and related analytics tools.

This skill is ready for commercial/non-commercial use.

## Publisher:

[giffywalls129](https://clawhub.ai/user/giffywalls129)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, marketers, and analytics practitioners use this skill to plan, implement, validate, and troubleshoot tracking for marketing sites, products, SaaS funnels, and e-commerce workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Third-party analytics tracking can collect personal data, secrets, or sensitive URL parameters if implemented without review.

Mitigation: Use consent controls, data minimization, and privacy-law review; avoid sending names, emails, raw user data, secrets, or sensitive URL parameters to analytics vendors.

Risk: Incorrect tracking guidance can produce duplicate events or misleading conversion metrics.

Mitigation: Validate events in GA4 DebugView, GTM Preview mode, and browser developer tools, then compare analytics counts against source-of-truth systems.

## Reference(s):

- [Event Library Reference](references/event-library.md)
- [GA4 Implementation Reference](references/ga4-implementation.md)
- [Google Tag Manager Implementation Reference](references/gtm-implementation.md)
- [Google Analytics Recommended Events](https://support.google.com/analytics/answer/9267735)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with tables, checklists, and inline code examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include tracking plans, event taxonomies, UTM conventions, validation steps, and implementation snippets.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact frontmatter reports 1.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
