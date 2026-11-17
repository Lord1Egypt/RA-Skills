## Description:

Create and manage short URLs with custom aliases, local tracking, and optional QR codes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dinghaibin](https://clawhub.ai/user/dinghaibin)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users can use this skill to create memorable local aliases for long URLs, inspect saved aliases, and generate QR codes for sharing links.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Saved URLs may contain private links, credentials, bearer tokens, or sensitive query parameters.

Mitigation: Avoid storing sensitive URLs and review local URL data before sharing or backing up the host environment.

Risk: Optional QR generation depends on an extra Python package installed in the user's environment.

Mitigation: Install optional QR dependencies in a virtual environment before using QR features.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, shell commands, code, guidance]

**Output Format:** [Markdown with inline shell commands and command output guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create local JSON storage in the user's home directory and optional QR image files when the script is run.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
