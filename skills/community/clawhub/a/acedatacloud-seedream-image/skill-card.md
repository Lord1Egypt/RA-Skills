## Description: <br>
Generate and edit AI images from text prompts or source images with Seedream models through the AceDataCloud API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Germey](https://clawhub.ai/user/Germey) <br>

### License/Terms of Use: <br>
Apache-2.0 <br>


## Use Case: <br>
Developers and external users use this skill to generate images from text prompts and edit existing images with inpainting or outpainting through AceDataCloud's Seedream API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts, source image URLs, and mask URLs are sent to AceDataCloud/Seedream. <br>
Mitigation: Use only approved non-sensitive content and follow organizational data-handling requirements before submitting images or URLs. <br>
Risk: The AceDataCloud API token can be exposed if copied into prompts, source files, logs, or shell history. <br>
Mitigation: Keep ACEDATACLOUD_API_TOKEN in an environment variable or secret manager and avoid hardcoding or committing it. <br>
Risk: Optional MCP package or hosted MCP usage adds another external integration path. <br>
Mitigation: Verify the mcp-seedream package or hosted MCP server before enabling it in agent workflows. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/Germey/acedatacloud-seedream-image) <br>
- [AceDataCloud Seedream Image API](https://api.acedata.cloud/seedream/images) <br>
- [Hosted Seedream MCP Server](https://seedream.mcp.acedata.cloud/mcp) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, API calls, Configuration] <br>
**Output Format:** [Markdown with bash, JSON, and curl examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires ACEDATACLOUD_API_TOKEN; API workflows may return direct image URLs.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
