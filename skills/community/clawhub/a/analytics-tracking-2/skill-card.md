## Description:

Helps agents set up, improve, and audit analytics tracking for marketing and product decisions across event tracking, GA4, GTM, UTMs, and related analytics tools.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mrhuang09](https://clawhub.ai/user/mrhuang09)

### License/Terms of Use:


## Use Case:

Developers, marketers, and analytics practitioners use this skill to create tracking plans, define event naming and properties, implement GA4 or GTM tracking, validate conversion data, and review privacy-sensitive measurement choices.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Tracking examples copied into production without consent or privacy review may collect inappropriate personal data or send data to unapproved third-party destinations.

Mitigation: Confirm the consent flow, avoid PII and raw payment details, prefer pseudonymous identifiers, and review GA4, Google Ads, Facebook Pixel, Segment, Mixpanel, Amplitude, or other destinations against privacy and compliance requirements.

Risk: Analytics configuration errors can create duplicate, missing, or misleading conversion data.

Mitigation: Validate events and parameters in GA4 DebugView, GTM Preview Mode, and browser debugging tools before publishing production tags.

## Reference(s):

- [Event Library Reference](references/event-library.md)
- [GA4 Implementation Reference](references/ga4-implementation.md)
- [Google Tag Manager Implementation Reference](references/gtm-implementation.md)
- [Google Analytics recommended events](https://support.google.com/analytics/answer/9267735)
- [ClawHub skill page](https://clawhub.ai/mrhuang09/skills/analytics-tracking-2)
- [Publisher profile](https://clawhub.ai/user/mrhuang09)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Configuration, Guidance]

**Output Format:** [Markdown guidance with tables, checklists, and inline JavaScript or HTML examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include tracking plan templates, event naming recommendations, GA4 and GTM implementation snippets, validation steps, and privacy review reminders.]

## Skill Version(s):

0.1.0 (source: server release metadata; artifact metadata.version is 1.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
