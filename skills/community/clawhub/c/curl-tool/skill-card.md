## Description:

Transfer data using HTTP, HTTPS, FTP protocols. Test APIs and download files.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dinghaibin](https://clawhub.ai/user/dinghaibin)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to make simple HTTP or HTTPS requests, test API endpoints, send request bodies, add headers or basic auth, and save response content to files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Requests to untrusted URLs can expose the agent to malicious or unexpected response content.

Mitigation: Use the skill only with trusted URLs and prefer HTTPS endpoints.

Risk: Basic auth credentials or tokens placed directly in command-line arguments may be exposed through shell history or process listings.

Mitigation: Avoid putting passwords or tokens directly in commands when possible and prefer safer credential handling in the surrounding workflow.

Risk: The output option writes response content to a user-specified file path.

Mitigation: Choose output paths carefully and avoid overwriting important files.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/dinghaibin/skills/curl-tool)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Files, Guidance]

**Output Format:** [Plain text or Markdown with shell command examples; downloaded response bodies may be written to files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can include HTTP response headers when requested; file downloads write response content to a user-specified output path.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
