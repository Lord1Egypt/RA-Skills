## Description:

Automatically generate NIH 2023-compliant Data Management and Sharing Plan (DMSP) drafts following FAIR principles.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aipoch-ai](https://clawhub.ai/user/aipoch-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Researchers, grant writers, and research administrators use this skill to draft NIH Data Management and Sharing Plans that address NIH 2023 required elements and FAIR principles from project metadata.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated DMSP drafts are saved locally and may include sensitive research, grant, or participant-related details supplied by the user.

Mitigation: Use an approved workspace, avoid entering PHI or confidential grant information unless authorized, and review generated files before sharing.

Risk: The tool accepts output paths that can overwrite writable files.

Mitigation: Use a controlled output directory and avoid passing untrusted, broad, or existing paths to --output.

## Reference(s):

- [NIH Data Management and Sharing Policy](https://sharing.nih.gov/data-management-and-sharing-policy)
- [NIH DMSP Template](references/nih_dmp_template.md)
- [FAIR Principles](https://www.go-fair.org/fair-principles/)

## Skill Output:

**Output Type(s):** [Markdown, Text, Shell commands, Code, Guidance]

**Output Format:** [Markdown document written to a local file or returned as text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may contain user-supplied research project details and are saved to disk by default.]

## Skill Version(s):

0.1.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
