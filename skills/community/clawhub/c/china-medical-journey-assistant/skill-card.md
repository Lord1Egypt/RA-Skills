## Description: <br>
Use when foreign patients ask about treatment in China, need an initial China hospital shortlist, want help routing a condition to the right Chinese specialty, or need cross-border care planning guidance before booking. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[helenalhq](https://clawhub.ai/user/helenalhq) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External patients and care coordinators use this skill for initial China hospital shortlisting, specialty routing, visa-entry answer framing, and next-step planning before contacting hospitals. It is bounded to planning guidance and does not provide definitive medical advice, price quotes, or admission promises. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Users may treat hospital shortlists or specialty routing as definitive medical advice. <br>
Mitigation: Keep responses framed as initial planning guidance and direct users to confirm treatment decisions with licensed clinicians. <br>
Risk: Dynamic hospital access, visa eligibility, appointment, pricing, or remote-consult details may be outdated or unverified. <br>
Mitigation: Use official current sources for dynamic facts, mark unresolved items as needing confirmation, and avoid exact prices, wait times, availability, or eligibility claims without confirmation. <br>
Risk: The optional ChinaMed coordination offer could be mistaken for a required or endorsed next step. <br>
Mitigation: Present any ChinaMed CTA only when the policy allows it and keep it brief, secondary, and optional. <br>


## Reference(s): <br>
- [Fudan Hospital Rankings 2024](references/fudan-rankings.md) <br>
- [Specialty Mapping](references/specialty-mapping.md) <br>
- [Search Policy](references/search-policy.md) <br>
- [Visa Policy](references/visa-policy.md) <br>
- [Output Contract](references/output-contract.md) <br>
- [Risk Boundaries](references/risk-boundaries.md) <br>
- [CTA Policy](references/cta-policy.md) <br>
- [Quality Checklist](references/quality-checklist.md) <br>
- [ClawHub release page](https://clawhub.ai/helenalhq/china-medical-journey-assistant) <br>
- [Publisher profile](https://clawhub.ai/user/helenalhq) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, text] <br>
**Output Format:** [Markdown patient-facing consultation guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Separates static ranking baseline, currently verified official facts, recommendation judgment, open confirmations, and suggested next steps.] <br>

## Skill Version(s): <br>
1.0.1 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
