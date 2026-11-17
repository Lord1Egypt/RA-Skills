## Description:

AgentImgHost REST API for uploading, listing, and deleting images. Returns direct public CDN URLs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jacobmaldonado](https://clawhub.ai/user/jacobmaldonado)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to upload image files to AgentImgHost, retrieve direct public CDN URLs, and manage hosted image deletion through the REST API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Uploaded images become publicly accessible by direct URL.

Mitigation: Do not upload screenshots or files containing secrets, personal data, customer data, or sensitive metadata.

Risk: Quota limits can automatically delete older hosted images when circular overwrite is enabled.

Mitigation: Disable circular overwrite when older hosted images must be retained.

Risk: The skill requires an AgentImgHost API key that grants upload and management access.

Mitigation: Provide the key only to trusted agents and rotate it if it may have been exposed.

## Reference(s):

- [AgentImgHost](https://agent-img.com)
- [AgentImgHost upload endpoint](https://agent-img.com/api/upload)
- [ClawHub skill page](https://clawhub.ai/jacobmaldonado/skills/agent-image-hosting)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration]

**Output Format:** [Markdown with inline bash and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires AGENTIMGHOST_API_KEY; uploaded images are publicly accessible by direct URL.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
