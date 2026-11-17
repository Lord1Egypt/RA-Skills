## Description:

Upload a local file to DogeCloud OSS (DogeCloud 对象存储) and return a public URL + metadata.

This skill is ready for commercial/non-commercial use.

## Publisher:

[white0dew](https://clawhub.ai/user/white0dew)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to upload local files to DogeCloud OSS with temporary credentials and receive machine-readable public access metadata.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Uploaded files may be exposed through public URLs.

Mitigation: Use the skill only for files intended for DogeCloud upload and public access, and prefer a production public base URL when stable links are required.

Risk: Permanent DogeCloud credentials could be overexposed or overprivileged.

Mitigation: Use a dedicated low-privilege key, keep permanent AccessKey and SecretKey server-side, and default to OSS_UPLOAD with exact object scope.

Risk: Wildcard or OSS_FULL scopes can broaden access beyond a single intended object.

Mitigation: Avoid OSS_FULL and wildcard scopes unless explicitly required and reviewed for the intended upload.

## Reference(s):

- [DogeCloud OSS Notes](references/dogecloud-oss.md)
- [DogeCloud OSS Python SDK guide](https://docs.dogecloud.com/oss/sdk-full-python.md)
- [DogeCloud API access token documentation](https://docs.dogecloud.com/oss/api-access-token.md)
- [ClawHub skill page](https://clawhub.ai/white0dew/skills/doge-oss-skill)

## Skill Output:

**Output Type(s):** [JSON, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown guidance with shell commands and a JSON uploader result]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3 plus boto3 and requests; uploads use DogeCloud credentials supplied through environment variables or CLI options.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
