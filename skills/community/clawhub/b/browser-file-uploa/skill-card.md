## Description:

Browser automation skill for uploading files to web pages with flexible path specification.

This skill is ready for commercial/non-commercial use.

## Publisher:

[weixizi](https://clawhub.ai/user/weixizi)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to automate file uploads in browser workflows, either by issuing agent-browser commands or by running the included Python helper with a target URL, local file path, optional selector, and wait time.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A file upload to the wrong website or with the wrong local path may disclose sensitive information.

Mitigation: Confirm the target URL and exact file path before each upload, and avoid secrets, credentials, private workspace files, or unknown sites unless the file is intended to be shared there.

Risk: Flexible path expansion can resolve environment variables, home-directory shortcuts, or workspace-relative paths to files the user did not mean to upload.

Mitigation: Review the resolved path before upload and prefer explicit paths when handling sensitive or business-critical files.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/weixizi/skills/browser-file-uploa)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Markdown guidance with shell command examples and Python script usage]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May operate on local file paths and user-specified web pages through agent-browser.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
