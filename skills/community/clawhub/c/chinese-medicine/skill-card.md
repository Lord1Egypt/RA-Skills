## Description:

Guides users through Chinese Medicine body constitution self-assessment, symptom pattern exploration, acupressure, herbs, formulas, and safety checks with educational wellness framing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[1970168137](https://clawhub.ai/user/1970168137)

### License/Terms of Use:

MIT-0

## Use Case:

External users can use this skill to explore Chinese Medicine concepts, constitution tendencies, acupressure points, herb and formula background, and safety considerations. The skill frames outputs as educational wellness guidance and directs users to qualified healthcare professionals for health concerns.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Reference data may expose herbal dosing, formula quantities, moxibustion, and acupuncture needling information despite educational safety framing.

Mitigation: Use guardrails that prevent dosage, self-needling, moxibustion, labor-induction, or individualized treatment instructions; present general education and refer users to qualified practitioners.

Risk: Pregnancy-sensitive points, contraindicated herbs, hepatotoxicity warnings, and drug interaction information could be misused without clinical context.

Mitigation: Require conservative safety screening, avoid recommending pregnancy-sensitive or high-risk interventions, and direct users with pregnancy, medication, liver disease, or serious symptoms to licensed healthcare professionals.

Risk: Symptom pattern exploration may be mistaken for medical diagnosis or treatment advice.

Mitigation: Keep outputs explicitly non-diagnostic, use tendency-focused language, include health disclaimers, and advise professional evaluation for health concerns.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/1970168137/skills/chinese-medicine)
- [Constitution database](artifact/references/constitution_db.json)
- [Syndrome rules](artifact/references/syndrome_rules.json)
- [Acupoints reference](artifact/references/acupoints.json)
- [Herbs database](artifact/references/herbs_db.json)
- [Formulas reference](artifact/references/formulas.json)
- [Contraindications reference](artifact/references/contraindications.json)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown or structured text with educational summaries, wellness recommendations, safety notes, and disclaimers]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Health-related responses should remain non-diagnostic, avoid individualized treatment or dosing instructions, and recommend qualified healthcare consultation.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
