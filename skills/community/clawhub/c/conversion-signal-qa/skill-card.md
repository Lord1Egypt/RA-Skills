## Description:

Builds and fixes paid-ad conversion measurement checks, including event firing, UTM hygiene, cross-platform deduplication gates, attribution-window alignment, and offline or iOS-ATT modeled-gap flags.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aaron-he-zhu](https://clawhub.ai/user/aaron-he-zhu)

### License/Terms of Use:

MIT-0

## Use Case:

Marketing operators, analysts, and developers use this skill before launching or scaling paid campaigns to verify conversion events, UTMs, deduplication gates, attribution windows, and modeled-data gaps. It produces a launch-readiness report plus a reusable UTM and conversion-event specification.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: User-provided analytics or ecommerce exports may contain sensitive campaign, order, or personal data.

Mitigation: Provide only the fields needed for the QA task, remove PII from UTMs and pasted exports, and treat exported report text as evidence rather than instructions.

Risk: Saved pre-flight reports can persist account-specific measurement details.

Mitigation: Save reports and UTM/event specifications only after explicit user approval and review the content before saving.

Risk: Optional API connectors can expand access beyond manual exports.

Mitigation: Use connectors only deliberately; manual GA4, ecommerce, and traffic-acquisition exports are sufficient for the documented workflow.

## Reference(s):

- [Tracking Pre-Flight Checklist](artifact/references/preflight-checklist.md)
- [UTM / Event Spec Builder](artifact/references/utm-event-spec.md)
- [Project homepage](https://github.com/aaron-he-zhu/aaron-marketing-skills)
- [ClawHub skill page](https://clawhub.ai/aaron-he-zhu/skills/conversion-signal-qa)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown report with checklist results, UTM naming rules, conversion-event specification tables, and a handoff summary]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write a user-facing pre-flight report and reusable UTM/event specification to memory only after explicit user approval.]

## Skill Version(s):

19.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
