## Description:

Uploads a local file to Qiniu Cloud Storage and returns a shareable URL.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ahsbnb](https://clawhub.ai/user/ahsbnb)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to upload a specified local file to a configured Qiniu Kodo bucket and return a shareable URL. It is intended only for non-sensitive files that can safely be exposed through the configured bucket policy.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Uploaded files may become publicly accessible depending on the configured Qiniu bucket policy.

Mitigation: Use the skill only for non-sensitive files and confirm the bucket access policy before uploading.

Risk: The skill can report failure after a successful upload, which may leave uploaded public files behind without returning a usable link.

Mitigation: Fix or wait for a fix to the URL-generation bug before relying on the result, and maintain a cleanup process for uploaded objects.

Risk: The skill depends on local Qiniu credentials and the qiniu Python package.

Mitigation: Verify the package source and version, and keep local credential configuration access restricted.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ahsbnb/skills/file-to-link)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Plain text URL on stdout with errors and operational guidance on stderr.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the qiniu Python package and local Qiniu credentials configured outside the artifact.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
