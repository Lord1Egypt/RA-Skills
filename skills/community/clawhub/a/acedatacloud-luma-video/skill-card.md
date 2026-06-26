## Description: <br>
Generate AI videos with Luma Dream Machine via the AceDataCloud API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Germey](https://clawhub.ai/user/Germey) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, creators, and agent users use this skill to generate videos from text prompts, animate reference images, or extend existing videos through AceDataCloud's Luma Dream Machine API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generation prompts, image URLs, video IDs, and related metadata are sent to AceDataCloud/Luma. <br>
Mitigation: Use the skill only for data approved for external processing and review the provider's privacy and retention terms before confidential work. <br>
Risk: The required API token could be exposed through prompts, logs, shared shells, or copied examples. <br>
Mitigation: Use a dedicated AceDataCloud token, keep it in environment variables or a secrets manager, and avoid pasting tokens into prompts or shared artifacts. <br>
Risk: Public start or end image URLs may expose private assets or internal network locations. <br>
Mitigation: Use only approved public assets and avoid private, signed, or internal URLs in generation requests. <br>
Risk: Prompt enhancement can alter the user's intended video content. <br>
Mitigation: Set enhancement to false for literal prompts and review generated outputs before publication or downstream use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Germey/acedatacloud-luma-video) <br>
- [AceDataCloud Luma video endpoint](https://api.acedata.cloud/luma/videos) <br>
- [AceDataCloud Luma MCP server](https://luma.mcp.acedata.cloud/mcp) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with bash and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include API request examples, parameter guidance, authentication setup, polling guidance, and MCP tool names.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
