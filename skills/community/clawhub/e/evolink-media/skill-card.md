## Description: <br>
AI video, image & music generation. 60+ models — Sora, Veo 3, Kling, Seedance, GPT Image, Suno v5, Hailuo, WAN. Text-to-video, image-to-video, text-to-image, AI music. One API key. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[EvoLinkAI](https://clawhub.ai/user/EvoLinkAI) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to plan, configure, and run Evolink-powered media workflows for image, video, music, digital-human generation, and hosted media file management. It helps agents collect required creative parameters, call available MCP tools, poll asynchronous tasks, and guide setup when the MCP server is not connected. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Selected user media may be uploaded to Evolink file hosting or generation APIs and should be treated as publicly shareable links. <br>
Mitigation: Do not upload secrets, confidential documents, regulated data, or private personal media unless the user intends to share them. <br>
Risk: The fallback file-hosting workflow can present curl commands that send local files or remote URLs to Evolink services. <br>
Mitigation: Review any generated curl command before execution and confirm the selected file, endpoint, and authorization header are intended. <br>
Risk: Generation requests initially return task IDs rather than completed media. <br>
Mitigation: Poll task status until it is completed or failed before reporting final results. <br>


## Reference(s): <br>
- [Evolink homepage](https://evolink.ai) <br>
- [ClawHub skill page](https://clawhub.ai/EvoLinkAI/evolink-media) <br>
- [Evolink Media API parameter reference](references/api-params.md) <br>
- [Evolink Media MCP package](https://www.npmjs.com/package/@evolinkai/evolink-media) <br>
- [Evolink Media MCP repository](https://github.com/EvoLinkAI/evolink-media-mcp) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, API calls, Markdown] <br>
**Output Format:** [Markdown guidance with inline shell commands, JSON configuration examples, and tool-call instructions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generation tasks are asynchronous and require polling until completion or failure; uploaded files and generated result links expire.] <br>

## Skill Version(s): <br>
1.3.0 (source: frontmatter and server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
