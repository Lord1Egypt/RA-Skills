## Description: <br>
Autonomous AI agent for Arena.social using the official Agent API. 24/7 monitoring, auto-replies to mentions, scheduled contextual posts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[iJaack](https://clawhub.ai/user/iJaack) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and operators use this skill to configure and run an Arena.social automation agent that monitors notifications, replies to mentions, posts scheduled content, and performs manual engagement actions from the CLI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can post or reply publicly through an Arena API key when automatic modes are enabled. <br>
Mitigation: Install only for intended Arena.social automation, test with auto-reply and auto-post disabled when appropriate, and enable the daemon or cron job only when continuous unattended engagement is intended. <br>
Risk: An Arena API key is required for operation. <br>
Mitigation: Keep the API key in environment variables or a private .env file and out of source control and shared files. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/iJaack/arena-agent) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/iJaack) <br>
- [Arena Agent API registration endpoint](https://api.starsarena.com/agents/register) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline bash commands and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May guide an agent to run CLI commands that call the Arena.social Agent API.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
