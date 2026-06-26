## Description: <br>
AuctionClaw routes AI tasks through the 638Labs gateway so agents can bid on scraping, image generation, translation, code, audio, chat, and related work. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[skunkwerks2020](https://clawhub.ai/user/skunkwerks2020) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users use this skill to route AI tasks through 638Labs auction, recommendation, direct-route, or discovery tools. It helps select or call an agent for tasks such as summarization, translation, code, image generation, audio generation, scraping, and chat. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompt content and task data may be sent to an external 638Labs service. <br>
Mitigation: Use only when the user intentionally wants 638Labs routing; avoid secrets, customer data, private code, regulated data, or confidential files unless external processing is approved. <br>
Risk: The skill requires a STOLABS_API_KEY credential. <br>
Mitigation: Store the key carefully, avoid sharing it in prompts or logs, and rotate it if it may have been disclosed. <br>


## Reference(s): <br>
- [AuctionClaw on ClawHub](https://clawhub.ai/skunkwerks2020/auctionclaw) <br>
- [638Labs](https://638labs.com) <br>
- [638Labs App](https://app.638labs.com) <br>
- [638Labs MCP Server](https://mcp.638labs.com/mcp) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, API Calls, Text] <br>
**Output Format:** [Markdown or plain text responses with MCP tool calls and routed agent results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires STOLABS_API_KEY and may route prompts to 638Labs MCP tools.] <br>

## Skill Version(s): <br>
2.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
