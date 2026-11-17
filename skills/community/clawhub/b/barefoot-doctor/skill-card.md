## Description:

Barefoot Doctor AI Assistant provides supervised educational reference guidance for integrative medicine topics based on the classic Barefoot Doctor's Manual (1969).

This skill is ready for commercial/non-commercial use.

## Publisher:

[johnsmithfan](https://clawhub.ai/user/johnsmithfan)

### License/Terms of Use:

MIT-0

## Use Case:

External users can use this skill as supervised educational reference support for integrative medicine prompts covering symptom discussion, TCM pattern differentiation, first-aid topics, herbs, acupuncture, and prevention. It should not be used for direct diagnosis, emergency triage, medication dosing, herbal prescribing, pediatric dosing, acupuncture, bloodletting, or moxibustion advice without licensed clinician or pharmacist oversight.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill gives broad, high-stakes medical and emergency guidance that could be mistaken for direct diagnosis or triage.

Mitigation: Use only in tightly supervised educational or historical reference settings; route urgent, worsening, pediatric, pregnancy, poisoning, dosing, or emergency questions to local emergency services and licensed clinicians.

Risk: Herbal, medication, pediatric dosing, and interaction guidance can cause harm if applied without patient-specific clinical review.

Mitigation: Require licensed clinician or pharmacist oversight before any user-facing medication, herbal, dosing, pediatric, pregnancy, or interaction recommendation.

Risk: Acupuncture, bloodletting, and moxibustion instructions can lead to injury when followed by untrained users.

Mitigation: Remove or gate invasive and procedure-style instructions, prefer non-invasive education, and refer procedural care to qualified practitioners.

Risk: The artifact uses China-specific emergency-services language that may be unsafe outside that locale.

Mitigation: Revise emergency wording to direct users to their local emergency number and local medical services before release in other geographies.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/johnsmithfan/skills/barefoot-doctor)
- [Barefoot Doctor - Method Patterns & Code Templates](artifact/references/method-patterns.md)
- [Barefoot Doctor - Copy-Paste Prompt Templates](artifact/01-implement-method.md)
- [Barefoot Doctor - Robustness & Safety Checklists](artifact/02-robustness-checks.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Guidance]

**Output Format:** [Markdown guidance and structured JSON-style response templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes triage, TCM and Western assessment sections, recommendations, warnings, follow-up criteria, and disclaimer fields.]

## Skill Version(s):

2.0.0 (source: server release and SKILL.md changelog, released 2026-04-26)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
