## Description:

Guides agents through creating and uploading mobile-compatible H5 touchscreen game files to the aigames repository interface.

This skill is ready for commercial/non-commercial use.

## Publisher:

[brianclan](https://clawhub.ai/user/brianclan)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to create the required config.json, index.html, and preview.png files for a mobile H5 game and upload them to the external aigames service for publication.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can direct agents to upload local game files to an external service and publish the resulting game without a clear final consent boundary.

Mitigation: Confirm the destination URL, publication intent, and final game folder with the user before upload.

Risk: The uploaded files may contain secrets, private assets, or unsafe content if they are not reviewed before submission.

Mitigation: Inspect config.json, index.html, and preview.png before upload, avoid absolute or user-supplied paths, and remove secrets or private assets.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/brianclan/skills/creategame)
- [Publisher profile](https://clawhub.ai/user/brianclan)
- [aigames repository interface](https://www.idlab.top)
- [Published game URL pattern](https://thenext.games/game/)

## Skill Output:

**Output Type(s):** [Guidance, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with JSON and bash examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce or reference config.json, index.html, and preview.png files before upload.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
