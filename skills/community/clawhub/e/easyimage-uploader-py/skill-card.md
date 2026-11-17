## Description:

Upload local image files to an EasyImages 2.0 service and return the hosted image URL.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fm7077](https://clawhub.ai/user/fm7077)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to upload an existing local image file to an EasyImages 2.0 server and return a shareable hosted URL. It is suited for workflows that need file-path based image hosting with configurable server and token credentials.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The helper can upload any readable local file selected by the agent or user.

Mitigation: Confirm the exact local image path before each upload and avoid using the skill for sensitive files unless the user accepts sending them to the configured server.

Risk: The configured EasyImages server may use plaintext HTTP and receive both the upload token and file contents.

Mitigation: Use only trusted HTTPS EasyImages servers and treat EASYIMAGE_TOKEN as a secret.

Risk: Successful upload responses may include delete URLs that can control hosted content.

Mitigation: Do not expose delete URLs unless the user explicitly asks for deletion capability.

## Reference(s):

- [EasyImages 2.0 API notes](references/api.md)
- [EasyImages 2.0 upstream project](https://github.com/icret/EasyImages2.0)
- [ClawHub skill page](https://clawhub.ai/fm7077/skills/easyimage-uploader-py)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and JSON result interpretation]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns the hosted image URL as the primary result; thumbnail URLs may be mentioned when useful, and delete URLs are treated as sensitive.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
