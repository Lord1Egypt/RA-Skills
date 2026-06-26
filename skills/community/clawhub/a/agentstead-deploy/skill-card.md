## Description: <br>
Deploys OpenClaw AI agents to AgentStead cloud hosting and helps create, configure, connect, start, stop, list, and subscribe hosted agents via the AgentStead API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[angusmolt](https://clawhub.ai/user/angusmolt) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to create and manage AgentStead-hosted AI agents, configure personalities and model plans, connect messaging channels, and control running agents. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow handles AgentStead account credentials, saved auth tokens, and messaging bot tokens. <br>
Mitigation: Prefer the interactive password prompt, avoid passing passwords as command-line arguments, use limited-scope bot tokens, and delete or revoke $HOME/.agentstead-token when it is no longer needed. <br>
Risk: The skill can trigger billable hosted-agent and ASTD subscription actions. <br>
Mitigation: Confirm the selected plan, subscription cost, wallet impact, and target agent ID before running create or subscribe commands. <br>
Risk: The skill asks the agent to create and execute a local shell helper that sends API requests. <br>
Mitigation: Review the helper before running it and keep network use limited to the intended AgentStead API endpoint. <br>


## Reference(s): <br>
- [AgentStead](https://agentstead.com) <br>
- [Agentstead Deploy on ClawHub](https://clawhub.ai/angusmolt/agentstead-deploy) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with bash commands and a shell helper script] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes API examples for AgentStead account login, agent lifecycle operations, channel setup, and subscription actions.] <br>

## Skill Version(s): <br>
1.4.1 (source: server release metadata and openclaw.skill.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
