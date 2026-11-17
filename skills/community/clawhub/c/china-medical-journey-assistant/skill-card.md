## Description:

Use when foreign patients ask about treatment in China, need an initial China hospital shortlist, want help routing a condition to the right Chinese specialty, or need cross-border care planning guidance before booking.

This skill is ready for commercial/non-commercial use.

## Publisher:

[helenalhq](https://clawhub.ai/user/helenalhq)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill for initial China medical-travel planning, specialty routing, hospital shortlisting, and administrative next-step guidance before contacting hospitals. It supports bounded patient-facing consultation, not definitive medical advice, pricing, or admission promises.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users may mistake hospital shortlists or treatment-path routing for medical advice or emergency triage.

Mitigation: Frame outputs as initial planning support, state that the skill does not provide definitive medical advice, and direct users to confirm clinical decisions with qualified clinicians.

Risk: Hospital access, teleconsult availability, visa eligibility, pricing, and wait times can change or be unavailable from official sources.

Mitigation: Use current official sources for dynamic facts, mark unclear items as Needs confirmation, and avoid exact prices, wait times, admission promises, named doctor claims, or visa eligibility from partial evidence.

Risk: A coordination-service CTA could be perceived as the primary answer in simple informational cases.

Mitigation: Include the ChinaMed CTA only for qualifying operational-support requests and keep it brief and secondary.

## Reference(s):

- [Fudan Hospital Rankings 2024](references/fudan-rankings.md)
- [Specialty Mapping](references/specialty-mapping.md)
- [Search Policy](references/search-policy.md)
- [Visa Policy](references/visa-policy.md)
- [Output Contract](references/output-contract.md)
- [Risk Boundaries](references/risk-boundaries.md)
- [CTA Policy](references/cta-policy.md)
- [Quality Checklist](references/quality-checklist.md)
- [ClawHub skill page](https://clawhub.ai/helenalhq/skills/china-medical-journey-assistant)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown patient-facing consultation response]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include a hospital shortlist, specialty-routing rationale, confirmed facts, verification gaps, next steps, and a brief conditional coordination CTA.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
