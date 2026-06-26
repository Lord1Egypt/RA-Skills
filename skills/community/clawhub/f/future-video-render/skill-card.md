## Description: <br>
Future Video Render helps agents submit, quote, monitor, cancel, download, and retrieve Future Video Studio video renders through the hosted MCP server or direct API fallback. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ariadne-coil](https://clawhub.ai/user/ariadne-coil) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to create multi-shot Future Video Studio renders, choose account or pay-per-render billing, attach supported assets, poll for completion, and return the final video URL. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can initiate renders that spend wallet credits or require pay-per-render payment. <br>
Mitigation: Require explicit user approval after showing the render summary, requested duration and resolution, and quoted amount or budget before submission or payment. <br>
Risk: API keys, claim tokens, payment URLs, uploaded files, and signed final video URLs are sensitive. <br>
Mitigation: Use the configured Future Video Studio credential path only for trusted Future Video Studio endpoints, avoid raw card collection, and return signed video URLs promptly because they may expire. <br>


## Reference(s): <br>
- [Future Video Studio API Docs](https://future.video/api-docs) <br>
- [Future Video Studio MCP Manifest](https://mcp.future.video/server.json) <br>
- [Future Video Studio Well-Known MCP Manifest](https://mcp.future.video/.well-known/mcp-server.json) <br>
- [Future Video Studio MCP Endpoint](https://mcp.future.video/mcp) <br>
- [Artifact API Reference](references/api.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON examples, shell commands, configuration notes, render status summaries, and final video URLs when available.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May involve sensitive API keys, claim tokens, payment URLs, uploaded assets, and signed final video URLs.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
