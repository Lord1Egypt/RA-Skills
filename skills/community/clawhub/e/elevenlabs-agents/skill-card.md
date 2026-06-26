## Description: <br>
Create, manage, and deploy ElevenLabs conversational AI agents. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[PennyroyalTea](https://clawhub.ai/user/PennyroyalTea) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to manage ElevenLabs conversational AI agents, including listing, creating, syncing, deploying, adding webhook tools, and retrieving widget embed code. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can initialize local project files and modify ElevenLabs agent or tool configuration without clearly showing the changes. <br>
Mitigation: Ask the agent to preview files it will create or change before continuing. <br>
Risk: The skill can push agent, deployment, webhook, or tool changes to ElevenLabs with insufficient user review. <br>
Mitigation: Require a dry-run or preview and explicit approval before any push, deployment, or webhook/tool change. <br>
Risk: Using the ElevenLabs CLI may require account-level access or API key authentication. <br>
Mitigation: Install only if you trust the local ElevenLabs CLI, and avoid sharing API keys directly in chat when possible. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/PennyroyalTea/elevenlabs-agents) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown summaries, tables, HTML snippets, and ElevenLabs CLI actions.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the local elevenlabs CLI and may create or update local agent and tool configuration files.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
