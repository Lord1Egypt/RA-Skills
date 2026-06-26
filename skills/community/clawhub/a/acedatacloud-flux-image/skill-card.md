## Description: <br>
Flux Image helps agents generate and edit images with Flux models through the AceDataCloud API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Germey](https://clawhub.ai/user/Germey) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, designers, and other external users use this skill to create images from prompts, edit existing images with text instructions, choose appropriate Flux models and size options, and poll AceDataCloud image tasks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts, image URLs, and generated outputs may contain sensitive or confidential content. <br>
Mitigation: Do not submit confidential prompts, private images, internal URLs, or signed URLs unless your organization permits that data to be processed by AceDataCloud. <br>
Risk: An exposed AceDataCloud API token could allow unauthorized use or unexpected costs. <br>
Mitigation: Store the token in an environment variable or secret manager, avoid committing or sharing it, use a dedicated token where possible, and monitor usage. <br>
Risk: Higher-quality models, large counts, and repeated retries can increase cost and latency. <br>
Mitigation: Use faster models for iteration, set the count parameter deliberately, and reserve ultra or kontext models for final generation or editing tasks. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/Germey/acedatacloud-flux-image) <br>
- [AceDataCloud Flux image API endpoint](https://api.acedata.cloud/flux/images) <br>
- [AceDataCloud hosted Flux MCP server](https://flux.mcp.acedata.cloud/mcp) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, API Calls, Configuration] <br>
**Output Format:** [Markdown with inline bash and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires ACEDATACLOUD_API_TOKEN; image generation can be asynchronous and may require task polling.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
