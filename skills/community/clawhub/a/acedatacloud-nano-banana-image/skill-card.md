## Description: <br>
Generate and edit AI images with NanoBanana (Gemini-based) via AceDataCloud API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Germey](https://clawhub.ai/user/Germey) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and creative automation users use this skill to create images from text prompts or edit existing images with natural-language instructions through AceDataCloud's NanoBanana API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts and source image URLs may be sent to AceDataCloud or its hosted MCP service. <br>
Mitigation: Avoid confidential prompts and private image links unless approved for that service. <br>
Risk: The skill requires an AceDataCloud API token. <br>
Mitigation: Use a dedicated token, keep it in approved secret storage or environment configuration, and do not hard-code it in shared files. <br>
Risk: The optional MCP package introduces an additional dependency path. <br>
Mitigation: Verify the MCP package and hosted endpoint before installing or connecting it in an agent environment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Germey/acedatacloud-nano-banana-image) <br>
- [AceDataCloud NanoBanana image API](https://api.acedata.cloud/nano-banana/images) <br>
- [Hosted NanoBanana MCP endpoint](https://nano-banana.mcp.acedata.cloud/mcp) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces API usage guidance and direct image URL handling details; generated images are returned by the external service.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
