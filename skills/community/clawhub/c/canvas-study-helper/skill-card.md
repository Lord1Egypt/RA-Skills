## Description:

Canvas Study Helper monitors Canvas LMS course announcements, assignments, and files, and helps generate Markdown study notes, mock tests, and CJK-capable PDF exports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[huaruoji](https://clawhub.ai/user/huaruoji)

### License/Terms of Use:

MIT

## Use Case:

Students and learning-support agents use this skill to check Canvas course updates, create structured study notes and mock tests, and convert Markdown learning materials into PDFs with Chinese and math formula support.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Canvas session cookies are handled through a local ~/.canvas_cookie file, which could expose authenticated Canvas access if the file is leaked, modified, or shared.

Mitigation: Review before installing or running; store only expected cookie keys, restrict the cookie file to 0600 permissions, and rotate or revoke Canvas sessions if exposure is suspected.

Risk: Authenticated Canvas requests can be sent to a user-configured institution hostname.

Mitigation: Validate the Canvas hostname before use and avoid following redirects with authenticated cookies.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands, templates, and generated PDF files from Markdown inputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires user-provided Canvas course IDs, institution hostname, local Canvas session cookies, and local PDF toolchain dependencies.]

## Skill Version(s):

1.1.0 (source: server release metadata, package.json, SKILL.md)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
