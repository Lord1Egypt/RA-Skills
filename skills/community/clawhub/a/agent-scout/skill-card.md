## Description: <br>
Create and configure Scout, a proactive research assistant agent with Telegram setup, OpenClaw agent configuration, skill provisioning, memory search, and inter-agent communication. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[stefanferreira](https://clawhub.ai/user/stefanferreira) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to configure a Scout research assistant agent with Telegram access, web and memory tools, skill discovery, and inter-agent messaging. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A persistent research agent connected to Telegram, memory, web tools, and inter-agent messaging can expose sensitive workspace or memory data if deployed without boundaries. <br>
Mitigation: Use a low-sensitivity workspace, restrict Telegram allowlists, review memory and search provider exposure, and require approval before browser automation, memory-derived sharing, or inter-agent messaging. <br>
Risk: Bot tokens and provider credentials can be exposed through shell history or tracked configuration files during setup. <br>
Mitigation: Store bot tokens and API keys outside shell history and version control, using the host platform's secret-management mechanism where available. <br>


## Reference(s): <br>
- [Agent Scout on ClawHub](https://clawhub.ai/stefanferreira/agent-scout) <br>
- [OpenClaw Agent Configuration](https://docs.openclaw.ai/concepts/agents) <br>
- [Telegram Bot Setup](https://docs.openclaw.ai/channels/telegram) <br>
- [Skill Discovery SOP](/skills/skill-discovery-sop) <br>
- [Browser Automation Core](/skills/browser-automation-core) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown with bash command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes setup, testing, maintenance, and troubleshooting guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
