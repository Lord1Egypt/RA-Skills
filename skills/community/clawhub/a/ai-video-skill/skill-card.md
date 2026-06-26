## Description: <br>
AITuber AI Video Skill helps agents create AI videos with narration, visuals, captions, MP4 export, and download support through the AITuber API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dhivalogu](https://clawhub.ai/user/dhivalogu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and creators use this skill to let coding agents generate AITuber videos from scripts or ideas, choose voices and styles, poll generation status, export MP4 files, and retrieve download links. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can use an AITuber account to generate, export, and download videos, which may consume credits or require a paid subscription. <br>
Mitigation: Confirm generation and export actions before execution, and check subscription status and credit balance when cost is relevant. <br>
Risk: Prompts, scripts, and ideas sent through the skill are shared with the AITuber service. <br>
Mitigation: Avoid sending confidential or sensitive content unless the user is comfortable sharing it with AITuber. <br>
Risk: The optional MCP server provides executable tools beyond this skill's written guidance. <br>
Mitigation: Review the MCP server separately before enabling it in an agent environment. <br>
Risk: The skill depends on a secret API key for authenticated endpoints. <br>
Mitigation: Store AITUBER_API_KEY as a secret and avoid exposing it in logs, shell history, or generated files. <br>


## Reference(s): <br>
- [AITuber](https://aituber.app) <br>
- [AITuber API Documentation](https://app.aituber.app/api-docs) <br>
- [AITuber API OpenAPI Spec](https://app.aituber.app/api/v1/openapi.json) <br>
- [AITuber API Base URL](https://app.aituber.app/api/v1) <br>
- [AITuber MCP Server](https://github.com/aituberapp/aituber-mcp) <br>
- [ClawHub Skill Page](https://clawhub.ai/dhivalogu/ai-video-skill) <br>
- [ClawHub Publisher Profile](https://clawhub.ai/user/dhivalogu) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, API Calls, Configuration] <br>
**Output Format:** [Markdown with inline bash and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses AITUBER_API_KEY for authenticated AITuber account actions and curl for API requests.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
