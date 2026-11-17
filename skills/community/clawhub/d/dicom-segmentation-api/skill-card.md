## Description:

Deploy and manage medical image segmentation using TotalSegmentator and MONAI with DICOM upload, batch processing, 3D export, and statistics generation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sunshine-del-ux](https://clawhub.ai/user/sunshine-del-ux)

### License/Terms of Use:

MIT

## Use Case:

Developers and medical imaging engineers use this skill to stand up a DICOM segmentation API for CT/MRI analysis, including upload, segmentation task tracking, result retrieval, 3D export, and statistics generation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles sensitive DICOM uploads and the security evidence notes missing privacy, access-control, and deployment-scope guidance.

Mitigation: Use only de-identified or properly authorized DICOM data, and deploy the server only on localhost or a protected network unless authentication and TLS are in place.

Risk: The security evidence advises verification before use in clinical or regulated environments.

Mitigation: Review the missing server code and dependency file, then complete clinical, privacy, and regulatory validation before trusting outputs in a regulated workflow.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/sunshine-del-ux/skills/dicom-segmentation-api)
- [Publisher profile](https://clawhub.ai/user/sunshine-del-ux)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown with inline shell commands, endpoint descriptions, and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact/_meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
