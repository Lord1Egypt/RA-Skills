## Description: <br>
Generate videos through Filtrix Remote MCP for text-to-video, image-to-video, video task polling, and downloading completed videos. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lumenclaw-cloud](https://clawhub.ai/user/lumenclaw-cloud) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and creators use this skill to submit text-to-video or image-to-video jobs through Filtrix MCP, monitor generation status, and download completed videos. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts, selected input images, and generated-video metadata are sent to the Filtrix service. <br>
Mitigation: Use only content approved for that external service and avoid sensitive or regulated media unless the service is approved for the use case. <br>
Risk: API key use and generation requests can affect account access and credits. <br>
Mitigation: Prefer a scoped or revocable key when available, set FILTRIX_MCP_API_KEY explicitly, and use idempotency keys for retries to reduce duplicate billing risk. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/lumenclaw-cloud/filtrix-video-gen) <br>
- [MCP Tools Reference](references/mcp-tools.md) <br>
- [Video Prompt Guide](references/prompts.md) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance, Files] <br>
**Output Format:** [Markdown guidance with bash commands, text status output, optional JSON payloads, and downloaded video files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses a Filtrix MCP API key, accepts prompts and optional input images, returns request IDs and status, and can download completed video outputs.] <br>

## Skill Version(s): <br>
0.1.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
