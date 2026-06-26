## Description: <br>
Your AI executive team on Discord. 7 specialists (engineering, finance, marketing, devops, legal, management, chief of staff) each with its own model and personality. Use when setting up, configuring, scaling, or troubleshooting a multi-bot Discord workspace where you are the CEO and AI agents are your team. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wanikua](https://clawhub.ai/user/wanikua) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, operators, and teams use this skill to set up and run a multi-agent Discord workspace backed by Clawdbot, with specialist agents for engineering, finance, marketing, DevOps, management, legal, and routing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill depends on the external Clawdbot package and a long-running Discord bot gateway. <br>
Mitigation: Install only if you trust Clawdbot, review its package and configuration before deployment, and run it with the least privileges needed for the Discord workspace. <br>
Risk: The configuration requires LLM API keys and Discord bot tokens. <br>
Mitigation: Use dedicated low-permission tokens, keep ~/.clawdbot/clawdbot.json private, and do not commit keys or tokens to source control. <br>
Risk: Workspace memory files can persist across restarts. <br>
Mitigation: Review memory files regularly and remove sensitive or obsolete content before continuing long-running agent use. <br>
Risk: Sandboxing is off by default in the documented setup. <br>
Mitigation: Enable the documented read-only, no-network sandbox when agents do not need write access or outbound network access. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wanikua/become-ceo) <br>
- [Become CEO setup guide](https://github.com/wanikua/become-ceo) <br>
- [Clawdbot configuration template](references/clawdbot-template.json) <br>
- [Team structure](references/IDENTITY.md) <br>
- [Workspace rules](references/AGENTS.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces setup and operating guidance for a Clawdbot-based Discord AI team; users provide their own LLM provider, model IDs, API keys, and Discord bot tokens.] <br>

## Skill Version(s): <br>
1.5.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
