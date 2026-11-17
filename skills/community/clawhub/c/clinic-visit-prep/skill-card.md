## Description:

Clinic Visit Prep helps patients organize pre-visit questions, prior records, checklists, and timelines without providing diagnoses.

This skill is ready for commercial/non-commercial use.

## Publisher:

[52yuanchangxing](https://clawhub.ai/user/52yuanchangxing)

### License/Terms of Use:

MIT-0

## Use Case:

External users and care-support workflows use this skill to prepare for clinic visits by turning symptoms, prior tests, planned questions, and missing information into a structured review draft.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release security summary flags extra local file-auditing and secret-scanning code beyond the clinic-visit preparation purpose.

Mitigation: Review the skill before installing, run it only on files intentionally provided for the visit-prep workflow, and avoid pointing it at private directories or source repositories.

Risk: Inputs may contain personal health information or other sensitive material.

Mitigation: Use explicit input and output paths, keep processing local, and remove or minimize sensitive details that are not needed for the clinic preparation draft.

Risk: Users may mistake organized visit-prep notes for clinical advice.

Mitigation: Use the output only to prepare questions and records for discussion with a clinician; do not rely on it for diagnosis or as a substitute for medical advice.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/52yuanchangxing/skills/clinic-visit-prep)
- [Publisher Profile](https://clawhub.ai/user/52yuanchangxing)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Structured Markdown or JSON, with optional shell command usage for the bundled local runner.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs emphasize review drafts, missing-information lists, clinic questions, document reminders, and post-visit note slots.]

## Skill Version(s):

1.0.0 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
