## Description:

Retrieves selected account credentials from 1Password, uses a headless browser to log in to a target site, and performs the user's requested page task.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tujinsama](https://clawhub.ai/user/tujinsama)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to automate browser login with selected 1Password credentials, then capture screenshots, extract page data, download files, or navigate to requested pages.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill is designed to access 1Password credentials and submit them through browser automation, and the security summary says it handles credential records too broadly without clear confirmation or domain-scoping safeguards.

Mitigation: Use a narrowly scoped 1Password service account, grant only needed vault access, require the user to specify the exact item and destination, and confirm the destination before credential retrieval or form submission.

Risk: Automated login can expose credentials if secrets are printed, logged, or written to files.

Mitigation: Do not print passwords, do not write credentials to files, and keep user-facing responses limited to confirmation that credentials were retrieved.

## Reference(s):


## Skill Output:

**Output Type(s):** [Text, Files, Shell commands, Guidance]

**Output Format:** [Markdown with inline shell commands and file references]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce screenshots or downloaded files in a downloads directory when the user requests file-based results.]

## Skill Version(s):

1.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
