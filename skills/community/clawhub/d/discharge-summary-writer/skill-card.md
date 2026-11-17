## Description:

Generate hospital discharge summaries from admission data, hospital course, medications, and follow-up plans.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aipoch-ai](https://clawhub.ai/user/aipoch-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Clinical documentation users and developers can use this skill to draft discharge summaries from structured inpatient data for physician review before inclusion in medical records.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated discharge summaries can contain incorrect or altered clinical content, especially when untrusted patient text is passed into the generator.

Mitigation: Review every generated summary with a qualified clinician and verify medications, diagnoses, identifiers, dates, and follow-up instructions against official medical records.

Risk: The script can overwrite arbitrary writable files through the output path.

Mitigation: Run the skill in a sandbox or dedicated workspace and constrain output paths to approved locations.

Risk: The language setting is unreliable until English rendering or explicit locale handling is fixed.

Mitigation: Validate the rendered language and locale before use, and avoid relying on English output until locale handling is confirmed.

## Reference(s):

- [Standard Discharge Summary Template](references/discharge_template.md)
- [Section Writing Guidelines](references/section_guidelines.md)
- [Standardized Medical Terminology](references/medical_terms.json)
- [Example Patient Data](references/example_patient.json)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Guidance]

**Output Format:** [Markdown discharge summary, structured Markdown, or JSON file]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires structured patient JSON input and clinician review before use; the local script writes the selected output file.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
