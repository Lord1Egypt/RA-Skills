## Description: <br>
DeepSeek Web Query sends selected user queries to the DeepSeek web app through browser automation, checks login state, recovers Chrome DevTools MCP when needed, and returns the extracted Markdown response. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[andeymei](https://clawhub.ai/user/andeymei) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to route explicit DeepSeek or web-query requests through an authenticated DeepSeek browser session and return the response content to the agent. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Selected prompts may be sent to DeepSeek through an authenticated browser session. <br>
Mitigation: Use the skill only for explicit DeepSeek requests and avoid secrets, proprietary content, or other sensitive data. <br>
Risk: The skill may read clipboard content while extracting Markdown from the DeepSeek page. <br>
Mitigation: Clear sensitive clipboard data before use and review returned content before sharing it. <br>
Risk: MCP recovery steps may modify local mcporter configuration or run an unpinned npx package. <br>
Mitigation: Review recovery actions before allowing configuration changes and prefer pinned package versions where the operating environment permits. <br>


## Reference(s): <br>
- [DeepSeek web app](https://chat.deepseek.com/) <br>
- [ClawHub skill page](https://clawhub.ai/andeymei/deepseek-web-query) <br>
- [Publisher profile](https://clawhub.ai/user/andeymei) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown or plain text, with shell commands and configuration steps when recovery guidance is needed] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns extracted DeepSeek content directly without agent-side summarization when query execution succeeds.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
