## Description:

Uploads user-selected local files or binary data to internal BS3 storage and returns a shareable file URL.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bagayalu](https://clawhub.ai/user/bagayalu)

### License/Terms of Use:

MIT-0

## Use Case:

Employees and developers use this skill when an agent needs to upload selected files, images, documents, or binary data to internal BS3 storage and return a URL for sharing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can upload arbitrary local data to shareable storage.

Mitigation: Require explicit user confirmation of the exact file path and intended destination before each upload.

Risk: Uploads use an unauthenticated plaintext connection with unclear scope.

Mitigation: Restrict installation to environments that need this internal bucket and prefer HTTPS, authenticated uploads, and pinned dependencies before broad deployment.

Risk: Uploaded content may expose secrets or regulated data through returned URLs.

Mitigation: Avoid uploading secrets or regulated data and confirm a real expiry mechanism before using the skill for sensitive workflows.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/bagayalu/skills/file-upload-test)
- [ClawHub publisher profile](https://clawhub.ai/user/bagayalu)

## Skill Output:

**Output Type(s):** [text, code, shell commands, configuration, guidance]

**Output Format:** [Plain text URL output with Python API return strings and CLI status text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns a shareable storage URL after applying an 8-character UUID prefix to the object key.]

## Skill Version(s):

1.0.1 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
