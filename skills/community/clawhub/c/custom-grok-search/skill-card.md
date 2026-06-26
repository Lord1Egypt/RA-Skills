## Description: <br>
Uses xAI Grok-compatible Responses API endpoints to run web search, X/Twitter search, chat, image chat, and model listing commands through official xAI or configured third-party proxy services. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhangjiongjie](https://clawhub.ai/user/zhangjiongjie) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to perform Grok-powered web research, X/Twitter research, chat, image analysis prompts, and model discovery from a command-line workflow. It is most useful when an environment needs either official xAI credentials or a trusted Grok-compatible proxy endpoint. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads local xAI or custom Grok API credentials and sends prompts, search queries, or images to the configured endpoint. <br>
Mitigation: Use a dedicated low-scope API key, verify CUSTOM_GROK_* and XAI_* configuration before running commands, and avoid sending sensitive prompts or private images. <br>
Risk: When CUSTOM_GROK_APIKEY is present, traffic can be routed through a third-party Grok-compatible proxy. <br>
Mitigation: Prefer the official xAI base URL or a trusted self-hosted proxy, and install only when the configured endpoint is trusted. <br>


## Reference(s): <br>
- [Configuration reference](references/config.md) <br>
- [xAI tools documentation links](references/xai-tools-links.md) <br>
- [xAI Search Tools](https://docs.x.ai/docs/guides/tools/search-tools) <br>
- [xAI Tools Overview](https://docs.x.ai/docs/guides/tools/overview) <br>
- [xAI API Reference](https://docs.x.ai/docs/api-reference) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, Text, Links, Shell commands, Configuration guidance] <br>
**Output Format:** [JSON search results with citations, plain text chat responses, URL lists, and command-line diagnostics] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Search output can include query, mode, result records, citations, author metadata, timestamps, or raw API responses when debug flags are used.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
