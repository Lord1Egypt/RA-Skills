## Description:

Generate and edit images, video, and music with Google Gemini models via MCP.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chrischall](https://clawhub.ai/user/chrischall)

### License/Terms of Use:

MIT-0

## Use Case:

Developers can use the Gemini MCP server to create or edit images, generate short videos and music, and refine image results through Gemini models.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated media can contain inaccurate or misleading details, including incorrectly rendered text.

Mitigation: Review generated media, especially any text or factual details, before sharing or relying on it.

Risk: The MCP setup and upload features send inputs to external services, and some referenced paths were not available for inspection.

Mitigation: Check the upload destination and confirm that files are appropriate to send before using upload features.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chrischall/skills/gemini-mcp)
- [Project repository (linked in the skill documentation)](https://github.com/chrischall/gemini-mcp)
- [npm package](https://www.npmjs.com/package/@chrischall/gemini-mcp)
- [Gemini API key setup](https://aistudio.google.com/apikey)

## Skill Output:

**Output Type(s):** [Images, Video, Music/audio, Files]

**Output Format:** [PNG or JPEG images, MP4 video, and MP3 audio; optional inline media data and result metadata]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated media can be saved to disk or returned inline; video and music generation may run asynchronously.]

## Skill Version(s):

2.5.1 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
