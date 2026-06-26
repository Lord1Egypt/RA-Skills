## Description: <br>
Send meme reaction images in chat with one command across Discord, Feishu, Telegram, LINE, and other OpenClaw-supported platforms. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kagura-agent](https://clawhub.ai/user/kagura-agent) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
AI agents and their operators use this skill to pick and send meme reaction images into configured chat channels for celebration, humor, encouragement, greetings, or other conversational reactions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can give an agent broad, proactive ability to post images into real chat channels. <br>
Mitigation: Install only where chat posting is intended, configure explicit accounts and targets, and require confirmation before sends. <br>
Risk: The skill requires OAuth tokens or other sensitive chat-platform credentials. <br>
Mitigation: Use least-privileged bot tokens, keep credentials in environment variables or private config, and avoid sharing credential files. <br>
Risk: Target, file, and shell execution handling are under-scoped, including an OpenClaw fallback sender called out by security guidance. <br>
Mitigation: Review targets and image paths before execution, avoid the OpenClaw fallback sender until its command construction is fixed, and avoid LINE for sensitive local images unless the hosting path is changed. <br>


## Reference(s): <br>
- [Agent Memes ClawHub listing](https://clawhub.ai/kagura-agent/agent-memes) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May invoke chat-platform APIs to send selected image files; sending requires configured credentials and targets.] <br>

## Skill Version(s): <br>
2.11.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
