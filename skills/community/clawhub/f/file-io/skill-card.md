## Description:

Upload local files to filebin.net for quick sharing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[goog](https://clawhub.ai/user/goog)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to upload a selected local workspace file to filebin.net and return a shareable public link.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Selected files are uploaded to a public filebin.net URL.

Mitigation: Confirm the exact file before upload and avoid private or sensitive data.

Risk: Shell upload commands can fail or behave unexpectedly when file paths or URL components are not handled carefully.

Mitigation: Use safe process invocation or careful quoting and URL encoding when running the curl command.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/goog/skills/file-io)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Guidance]

**Output Format:** [Markdown with inline shell commands and shareable upload links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes a public file URL and bin page when upload succeeds.]

## Skill Version(s):

1.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
