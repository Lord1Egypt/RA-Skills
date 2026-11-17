## Description:

Folder Inspector scans a local directory and lists files with their sizes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jayxu-d](https://clawhub.ai/user/jayxu-d)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to inspect an absolute local folder path and receive a concise listing of files and sizes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A malicious or malformed folder path could cause commands to run as the agent user.

Mitigation: Use a version that avoids shell interpolation, such as argument-array process execution or native filesystem APIs, before installing.

Risk: Inspected paths are written to a predictable temporary log file.

Mitigation: Remove or secure debug logging so local path information is not written to an undocumented /tmp file.

Risk: The helper script path is tied to a specific local installation path.

Mitigation: Resolve the helper script from the installed skill directory instead of a hard-coded user-specific path.

## Reference(s):


## Skill Output:

**Output Type(s):** [Text, Markdown]

**Output Format:** [Markdown table with file names and sizes, or an error message when inspection fails.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Lists immediate files in the requested directory and reports sizes in KB.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
