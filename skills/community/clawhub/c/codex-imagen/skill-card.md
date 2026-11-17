## Description:

Generate or edit raster images by calling the ChatGPT/Codex Responses image_generation tool with local Codex or OpenClaw OAuth credentials, then save decoded image files for OpenClaw and other agent workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[darkamenosa](https://clawhub.ai/user/darkamenosa)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to generate or edit image files from prompts or reference images inside OpenClaw and related agent workflows. It is useful when an agent needs saved PNG outputs or JSON metadata without using an OpenAI API key.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can send locally discovered OAuth access tokens to configurable request endpoints.

Mitigation: Install only when the publisher is trusted, run in a controlled environment, and avoid custom --base-url, --refresh-url, or CODEX_REFRESH_TOKEN_URL_OVERRIDE values unless the endpoint is fully trusted.

Risk: Prompts and local reference images can be uploaded to the configured image-generation backend.

Mitigation: Do not pass sensitive prompts or local images unless the user understands where that data will be sent and has approval to process it there.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/darkamenosa/skills/codex-imagen)
- [README](README.md)
- [Codex Responses Backend Endpoint](https://chatgpt.com/backend-api/codex/responses)
- [OpenAI OAuth Refresh Endpoint](https://auth.openai.com/oauth/token)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, files, guidance]

**Output Format:** [Saved PNG file paths or JSON metadata, with Markdown guidance and shell commands for agent use]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Streaming can save partial image outputs before timeout; JSON mode reports image paths, hashes, request metadata, retry state, timeout state, and auth refresh state.]

## Skill Version(s):

0.2.6 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
