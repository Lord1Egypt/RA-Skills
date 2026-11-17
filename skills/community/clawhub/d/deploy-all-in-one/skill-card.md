## Description:

Deploy All-in-One scans a project for deployment-related configuration, credential, and CI/CD files, prepares deployment bundle information, and records a deployment manifest.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ink5725](https://clawhub.ai/user/ink5725)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and release engineers use this skill to automate deployment preparation by finding deployment-related project files and generating a manifest for CI/CD handoff. Security review should confirm that sensitive files are excluded or replaced with managed secret references before real project use.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may gather raw credential or secret files and place them in shared storage.

Mitigation: Exclude raw secrets by default, require an explicit file allowlist, and use a secret manager or CI/CD secret references for sensitive values.

Risk: The documented workflow runs without an intermediate confirmation step before packaging and upload.

Mitigation: Add a required review and approval step before any package is created or shared.

Risk: The deployment status can be misleading if packaging or upload did not actually occur.

Mitigation: Report dry-run, package creation, and upload status explicitly, and fail the workflow when expected artifacts or uploads are missing.

## Reference(s):

- [ClawHub skill page: deploy-all-in-one](https://clawhub.ai/ink5725/skills/deploy-all-in-one)
- [ClawHub publisher profile: ink5725](https://clawhub.ai/user/ink5725)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, files, JSON]

**Output Format:** [Plain text execution notes plus deployment package files and a JSON deployment manifest.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Manifest output includes file names, sizes, checksums, timestamps, and the intended shared-storage destination.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
