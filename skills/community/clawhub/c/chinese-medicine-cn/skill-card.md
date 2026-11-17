## Description:

Chinese Medicine CN provides Chinese-language educational guidance for traditional Chinese medicine constitution assessment, herbs, formulas, acupoints, syndrome associations, and compatibility safety checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[1970168137](https://clawhub.ai/user/1970168137)

### License/Terms of Use:

MIT-0

## Use Case:

People interested in traditional Chinese medicine use this skill to learn about constitution patterns, herbs, classic formulas, acupoint wellness practices, seasonal health preservation, and non-diagnostic symptom-pattern associations. The skill is intended for cultural and educational reference, with health-related outputs directed back to licensed clinicians for medical decisions.

### Deployment Geography for Use:

China

## Known Risks and Mitigations:

Risk: The skill can expose exact herbal doses, preparation details, and formula modifications despite stating that it does not prescribe.

Mitigation: Treat herb and formula content as educational reference only; suppress personalized dosing, preparation, and modification guidance in consumer responses and direct users to licensed clinicians for treatment decisions.

Risk: The skill can expose needle insertion and moxibustion procedure details for acupoints.

Mitigation: Limit consumer-facing acupoint responses to general wellness or acupressure context, preserve contraindication warnings, and refer needling or moxibustion decisions to qualified practitioners.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/1970168137/skills/chinese-medicine-cn)
- [constitution_db.json](artifact/references/constitution_db.json)
- [syndrome_rules.json](artifact/references/syndrome_rules.json)
- [acupoints.json](artifact/references/acupoints.json)
- [herbs_db.json](artifact/references/herbs_db.json)
- [formulas.json](artifact/references/formulas.json)
- [contraindications.json](artifact/references/contraindications.json)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Chinese-language Markdown-style responses with structured sections and safety disclaimers]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include constitution summaries, herb or formula explanations, acupoint wellness guidance, symptom-pattern associations, and compatibility safety reports.]

## Skill Version(s):

1.0.0 (source: server release metadata and user changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
