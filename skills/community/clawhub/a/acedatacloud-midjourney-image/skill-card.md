## Description: <br>
Generate, edit, blend, upscale, and describe images with Midjourney via AceDataCloud API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Germey](https://clawhub.ai/user/Germey) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and creators use this skill to guide an agent through Midjourney image workflows via AceDataCloud, including text-to-image generation, image edits, blending, upscaling, variations, reverse prompting, and image-to-video generation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts, image URLs, and related metadata are sent to AceDataCloud or Midjourney-related services. <br>
Mitigation: Use a dedicated API token where possible and avoid sending secrets, confidential images, internal URLs, regulated personal data, or other sensitive content. <br>
Risk: The optional mcp-midjourney package or hosted MCP endpoint can expand the agent's interaction surface. <br>
Mitigation: Verify the package or hosted endpoint before enabling it and review the exact tools exposed to the agent. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Germey/acedatacloud-midjourney-image) <br>
- [AceDataCloud Midjourney Imagine API endpoint](https://api.acedata.cloud/midjourney/imagine) <br>
- [AceDataCloud hosted Midjourney MCP endpoint](https://midjourney.mcp.acedata.cloud/mcp) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, API calls, Configuration] <br>
**Output Format:** [Markdown with inline shell and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce prompts, HTTP request examples, task polling guidance, and MCP setup instructions; generated images, descriptions, and videos are returned by the third-party service.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
