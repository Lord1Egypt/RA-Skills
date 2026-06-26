## Description: <br>
Helps agents plan, implement, improve, audit, and troubleshoot analytics tracking for GA4, Google Tag Manager, UTM parameters, conversion events, and related measurement workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Giffywalls129](https://clawhub.ai/user/Giffywalls129) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, marketers, analysts, and developers use this skill to create tracking plans, event taxonomies, GA4/GTM implementations, UTM conventions, and validation checklists for marketing and product measurement. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Analytics plans may involve personal data, user identifiers, account identifiers, payment data, or transaction tracking. <br>
Mitigation: Confirm consent and legal basis, avoid PII and secrets in event properties, minimize identifiers, and review data retention before deployment. <br>
Risk: GA4 or GTM setup may require OAuth access and could store refresh tokens in the artifact directory. <br>
Mitigation: Grant only the minimum required Google/GTM access, protect token storage, and remove tokens when the work is complete. <br>
Risk: Publishing to the wrong GTM account, container, or workspace can change production tracking unexpectedly. <br>
Mitigation: Verify the exact GTM account, container, workspace, and publish step before applying or publishing changes. <br>
Risk: Browser-backed network workflows and ad or analytics blockers can make validation results incomplete. <br>
Mitigation: Use GA4 DebugView, GTM Preview mode, browser developer tools, and database-side checks to validate events before relying on metrics. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Giffywalls129/044) <br>
- [Event Library Reference](artifact/references/event-library.md) <br>
- [GA4 Implementation Reference](artifact/references/ga4-implementation.md) <br>
- [Google Tag Manager Implementation Reference](artifact/references/gtm-implementation.md) <br>
- [Google Analytics recommended events](https://support.google.com/analytics/answer/9267735) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, configuration, guidance] <br>
**Output Format:** [Markdown with tables, checklists, and inline JavaScript examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include GA4/GTM event taxonomies, tracking plans, UTM conventions, validation checklists, and debugging steps.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata; artifact metadata reports 1.1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
