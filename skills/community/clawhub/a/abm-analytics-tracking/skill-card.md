## Description: <br>
Helps users set up, improve, audit, and debug analytics tracking, including GA4, Google Tag Manager, conversion events, UTM parameters, and measurement plans. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mariokarras](https://clawhub.ai/user/mariokarras) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Marketing, product, and engineering teams use this skill to design tracking plans, implement analytics events, configure GA4 and GTM, debug broken tracking, and align measurement with business decisions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Analytics examples can lead to collecting personal, billing, or payment-card details if copied without review. <br>
Mitigation: Use pseudonymous IDs, avoid direct identifiers and sensitive payment data in event properties, and review tracking plans before production use. <br>
Risk: Analytics and marketing tags may run before required consent in regulated regions. <br>
Mitigation: Gate GA4, GTM, and pixel tags behind applicable consent, configure consent mode or a consent management platform, and review settings against privacy requirements. <br>


## Reference(s): <br>
- [Event Library Reference](references/event-library.md) <br>
- [GA4 Implementation Reference](references/ga4-implementation.md) <br>
- [Google Tag Manager Implementation Reference](references/gtm-implementation.md) <br>
- [Google Analytics Recommended Events](https://support.google.com/analytics/answer/9267735) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, configuration, guidance] <br>
**Output Format:** [Markdown with tables, checklists, and inline JavaScript examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include tracking plans, event taxonomies, UTM conventions, validation steps, and privacy review guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata; artifact frontmatter reports 1.1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
