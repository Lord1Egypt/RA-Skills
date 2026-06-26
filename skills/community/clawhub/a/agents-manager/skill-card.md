## Description: <br>
Manage Clawdbot agents: discover, profile, track capabilities, define routing hierarchy, and assign tasks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[agentandbot-design](https://clawhub.ai/user/agentandbot-design) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, operators, and agent maintainers use this skill to inventory Clawdbot agents, define reporting and delegation rules, check assignment permissions, and monitor agent health and task history. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill includes broad delegation defaults and a hard-coded external Telegram escalation target. <br>
Mitigation: Before installation, replace the bundled escalation target and review who receives human escalation messages. <br>
Risk: Agent spawning and long-running delegation can proceed beyond the user's intended scope if approvals are not enforced. <br>
Mitigation: Require explicit approval for spawned or long-running agents and keep the handshake protocol enabled for untrusted senders. <br>
Risk: The permission checker is not a strong authorization boundary without target validation fixes. <br>
Mitigation: Use can_assign.js as advisory guidance only until target validation is reviewed and hardened. <br>


## Reference(s): <br>
- [Agent Profile Schema](references/agent-profile-schema.md) <br>
- [Agent Registry](references/agent-registry.md) <br>
- [Health Check Template](references/health-check-template.md) <br>
- [Task Routing Rules](references/task-routing-rules.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/agentandbot-design/agents-manager) <br>
- [Skill Homepage](https://www.clawhub.com/skills/agents-manager) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with inline Node.js commands, JSON reports, Mermaid graphs, and registry updates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js for bundled scripts.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
