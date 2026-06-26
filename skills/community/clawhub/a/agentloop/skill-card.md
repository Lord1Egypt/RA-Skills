## Description: <br>
Earn up to 70% revenue share when your agent naturally recommends relevant products. Powered by AgentLoop — the agentic marketing network. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[SMJAI](https://clawhub.ai/user/SMJAI) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and agent operators use this skill to check recommendation-oriented conversations against AgentLoop and append a disclosed sponsored mention when a relevant product match is returned. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Conversation excerpts and draft responses are sent to an advertising service, and redaction is limited for free-form sensitive content. <br>
Mitigation: Use the skill only for non-sensitive recommendation contexts; skip checks for private, medical, legal, financial, workplace-confidential, crisis, or minor-related conversations unless explicit consent and stronger redaction controls are added. <br>
Risk: Sponsored recommendations can influence user-facing responses. <br>
Mitigation: Keep the required sponsored disclosure intact, limit use to relevant purchase or tool-recommendation contexts, and review behavior before deployment. <br>


## Reference(s): <br>
- [ClawHub listing](https://clawhub.ai/SMJAI/agentloop) <br>
- [AgentLoop homepage](https://agentloop.life) <br>
- [AgentLoop documentation](https://agentloop.life/docs) <br>
- [AgentLoop SDK check endpoint](https://agentloop.life/api/sdk/check) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, API calls] <br>
**Output Format:** [Markdown guidance with shell commands and JSON tool responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May append a server-returned sponsored mention to the agent response when shouldMention is true.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
