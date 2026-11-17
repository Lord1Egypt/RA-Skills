## Description:

Batch anonymize DICOM medical images by removing patient sensitive information while preserving image data for research use.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aipoch-ai](https://clawhub.ai/user/aipoch-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, data engineers, and clinical research teams use this skill to prepare DICOM medical imaging files for research sharing by applying local de-identification routines, batch processing folders, and generating audit logs. Outputs still require institutional privacy review before release.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The anonymizer may leave sensitive medical data behind, including PHI in pixel data, structured reports, private tags, or other fields outside the implemented routines.

Mitigation: Validate all outputs through institutional privacy review and manual QA before research sharing or release.

Risk: Audit logs and returned result objects may contain sensitive linkage data such as pseudonyms, file paths, hashes, and processing outcomes.

Mitigation: Store audit logs and result data in approved protected locations with access controls, retention limits, and review before sharing.

Risk: Dependency and environment choices affect handling of real PHI.

Mitigation: Pin and audit dependencies, install in a reviewed local environment, and process real PHI only under approved privacy and security procedures.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/aipoch-ai/skills/dicom-anonymizer)
- [PHI tag reference](references/phi_tags.json)
- [Python dependency reference](references/requirements.txt)

## Skill Output:

**Output Type(s):** [Shell commands, Code, Files, Guidance]

**Output Format:** [Markdown with CLI and Python examples; anonymized DICOM files and optional JSON audit logs when executed.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Runs locally on user-provided DICOM paths; audit logs and result objects may contain sensitive linkage data and should be handled as sensitive.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
