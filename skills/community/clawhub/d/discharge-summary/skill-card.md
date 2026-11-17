## Description:

Turns clinician-provided hospital stay details into a structured discharge summary covering admission reason, hospital course, diagnoses, procedures, medications, condition, follow-up, return precautions, and patient instructions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mohitagw15856](https://clawhub.ai/user/mohitagw15856)

### License/Terms of Use:

MIT-0

## Use Case:

Clinicians and clinical documentation teams use this skill to organize provided admission-to-discharge details into a scannable discharge summary for handoff and patient instructions. It is a documentation-formatting aid and requires clinician review before finalization.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Protected health information could be used outside an appropriate clinical or privacy-controlled environment.

Mitigation: Use the skill only in approved clinical/privacy environments for patient information.

Risk: Medication, diagnosis, follow-up, or return-precaution details could be incorrect or incomplete if source information is not reviewed.

Mitigation: Require a qualified clinician to verify all medications, diagnoses, follow-up, and return precautions before finalizing.

Risk: Missing clinical details could be filled in incorrectly during discharge-summary drafting.

Mitigation: Mark unavailable information as not documented and do not invent diagnoses, medications, doses, results, or procedures.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mohitagw15856/skills/discharge-summary)
- [Skill homepage](https://mohitagw15856.github.io/pm-claude-skills/skill/discharge-summary.html)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown discharge summary with structured clinical sections]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes missing-field notes and clinician-review reminders; no code execution or external data transfer.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
