## Description:

Generate medical documents from clinical notes. Input: patient info, symptoms, diagnosis. Output: SOAP notes, discharge summaries, referral letters, prescription drafts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[loutai0307-prog](https://clawhub.ai/user/loutai0307-prog)

### License/Terms of Use:

MIT-0

## Use Case:

Clinicians and clinical support staff use this skill to draft SOAP notes, discharge summaries, referral letters, and prescription drafts from patient details and clinical notes. Outputs are drafts only and require licensed professional review before clinical use.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated clinical documents may be incorrect, incomplete, or unsuitable for a patient's actual care context.

Mitigation: Require review, correction, and approval by a licensed medical professional before use in clinical workflows.

Risk: Draft output includes built-in vendor branding that may be inappropriate in EHR, referral, prescription, or discharge records.

Mitigation: Remove the vendor footer before pasting generated content into clinical records.

Risk: Command-line inputs may include sensitive patient information.

Mitigation: Use only in environments approved for the clinical workflow and handle inputs according to applicable privacy and data-handling policies.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/loutai0307-prog/skills/bytesagain-medical-scribe)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Guidance]

**Output Format:** [Structured plain text medical document drafts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Draft SOAP notes, discharge summaries, referral letters, prescription drafts, and template listings include visible review warnings and vendor branding.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
