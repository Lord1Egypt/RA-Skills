## Description:

Free image hosting with albums, privacy controls, and API access. Upload images by URL or file, organize into albums with folders, set privacy levels, and manage your hosted images.

This skill is ready for commercial/non-commercial use.

## Publisher:

[beeimg](https://clawhub.ai/user/beeimg)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to upload images to BeeIMG, organize hosted images into albums or folders, apply privacy settings, and manage deletion or album operations through BeeIMG API calls.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses BEEIMG_API_KEY to access the user's BeeIMG account.

Mitigation: Install only when BeeIMG access is intended, keep the API key in the environment, and avoid exposing it in prompts, logs, or shared command output.

Risk: Uploaded images may become publicly visible because public is the default privacy setting in examples.

Mitigation: Confirm the desired privacy level before upload or album creation, especially for sensitive images or share links.

Risk: Delete and album management actions can remove or reorganize hosted content.

Mitigation: Require explicit user confirmation before deleting images, folders, or albums or moving images between containers.

## Reference(s):

- [Beeimg Openclaw on ClawHub](https://clawhub.ai/beeimg/skills/beeimg)
- [BeeIMG Homepage](https://beeimg.com)
- [BeeIMG API Key](https://beeimg.com/api/newkey)
- [BeeIMG URL Upload API](https://beeimg.com/api/upload/url/json/)
- [BeeIMG File Upload API](https://beeimg.com/api/upload/file/json/)
- [BeeIMG Album API](https://beeimg.com/api/album)
- [BeeIMG MCP Server](https://beeimg.com/mcp)
- [BeeIMG Premium Comparison](https://beeimg.com/premium/compare)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and JSON response examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce curl commands that use BEEIMG_API_KEY and BeeIMG API endpoints.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
