## Description: <br>
Unified interface for all providers and all modalities: use the `genai-calling` skill to operate the published `genai-calling` CLI/SDK across text/image/audio/video/embedding workflows, with support for authenticated local MCP workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Gravtice-Agent](https://clawhub.ai/user/Gravtice-Agent) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to configure and call the `genai-calling` CLI, Python SDK, and local MCP server for multimodal generation workflows across supported providers. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Provider credentials are required for normal API calls and may be stored in project-local or user-wide environment files. <br>
Mitigation: Use only the provider keys needed for the task, keep `.env` files private, and do not commit credentials. <br>
Risk: Local MCP workflows can expose provider-backed generation tools if run without appropriate authentication. <br>
Mitigation: Set `GENAI_CALLING_MCP_BEARER_TOKEN` or token rules before exposing the MCP server. <br>
Risk: Private or loopback URL downloads are blocked by default but can be enabled by configuration. <br>
Mitigation: Leave private URL protection enabled unless the operator has reviewed and accepted the local network access risk. <br>
Risk: The security evidence reports no unsafe behavior, but advises checking install prompts and displayed files before installation. <br>
Mitigation: Review install prompts for unexpected package installs, credential requests, persistent background behavior, or access to private local data. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/Gravtice-Agent/genai-calling) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash and Python code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes provider environment variable guidance, CLI examples, SDK snippets, MCP server commands, and troubleshooting notes.] <br>

## Skill Version(s): <br>
1.0.2 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
