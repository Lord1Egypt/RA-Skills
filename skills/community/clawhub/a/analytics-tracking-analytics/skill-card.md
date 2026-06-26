## Description: <br>
Guides GA4 analytics implementation for event tracking, conversions, attribution, User ID tracking, CTA attribution, and data quality. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kostja94](https://clawhub.ai/user/kostja94) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, marketers, and analytics practitioners use this skill to plan GA4 setup, define meaningful event and conversion tracking, map attribution needs, and prepare validation checklists. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: User ID tracking can expose personal data or create privacy compliance issues if raw identifiers are sent to GA4. <br>
Mitigation: Use pseudonymous internal IDs rather than emails, names, phone numbers, or other raw personal data, and confirm consent, retention, access controls, GA4 policy, and applicable privacy-law requirements before enabling User ID. <br>
Risk: Inconsistent UTM values or poorly validated conversion events can fragment attribution data and lead to misleading channel optimization decisions. <br>
Mitigation: Standardize UTM conventions, test events before launch, verify parameters in GA4 Realtime or DebugView, and check for duplicate events or missing values. <br>


## Reference(s): <br>
- [UTM.io - UTMs for Marketing Attribution](https://web.utm.io/blog/utms-for-marketing-attribution/) <br>
- [GA4 - Get started with attribution](https://support.google.com/analytics/answer/10596866) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, configuration, guidance] <br>
**Output Format:** [Markdown with event tables, implementation notes, conversion mappings, testing checklists, and JavaScript snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include GA4 event names, event parameters, conversion mappings, attribution notes, and validation steps.] <br>

## Skill Version(s): <br>
1.3.1 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
