## Description:

Converts comprehensive dental exam findings into a DRAFT phased, CDT-coded treatment plan with alternatives, risks, benefits, and an informed-consent prompt sheet for licensed-dentist review.

This skill is ready for commercial/non-commercial use.

## Publisher:

[archlab-space](https://clawhub.ai/user/archlab-space)

### License/Terms of Use:

MIT-0

## Use Case:

External dental professionals, dental residents, and treatment coordinators use this skill to turn clinician-supplied comprehensive exam findings into a structured draft treatment plan for licensed dentist review. It supports case presentation preparation, informed-consent discussion prompts, phasing, CDT-code confirmation, and non-binding cost narrative scaffolding.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Draft plans may contain incorrect diagnosis, coding, sequencing, fees, referrals, or consent language if used without clinician review.

Mitigation: Use only as a drafting aid and require a licensed dentist to verify diagnosis, CDT codes, sequencing, fees, referrals, and informed-consent materials before patient use.

Risk: Dental case details may include sensitive patient information.

Mitigation: Do not enter direct patient identifiers; use chart numbers or initials and redact full names, dates of birth, contact details, insurance member IDs, and other direct identifiers.

Risk: Patients could misread the output as a final treatment plan or signed informed consent.

Mitigation: Keep outputs marked DRAFT and route them to a licensed dentist or supervised staff member for review before presentation, signature, or treatment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/archlab-space/skills/dental-treatment-plan-presenter)
- [Open-Skill-Hub issues](https://github.com/archlab-space/Open-Skill-Hub/issues)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown draft treatment plan with tables, patient-facing summaries, decision points, and informed-consent prompts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are marked DRAFT and intended for licensed dentist review; the skill should not collect direct patient identifiers or provide final diagnoses, final CDT codes, binding fees, medication dosing, or signed consent.]

## Skill Version(s):

0.1.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
