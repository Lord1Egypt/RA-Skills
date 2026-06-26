## Description: <br>
Build high-performing OpenClaw agents end-to-end with comprehensive safety features for designing new agents, generating workspace files, and iterating on behavior, guardrails, autonomy, heartbeat plans, and skill rosters. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[YKaiXu](https://clawhub.ai/user/YKaiXu) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent builders use this skill to design OpenClaw agents, generate required workspace files, configure channel and model-provider setup, and produce validation prompts for agent behavior. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated agent templates may grant broad autonomous, persistent, or privileged behavior. <br>
Mitigation: Review and edit generated templates before use; reduce autonomy, remove no-approval language, and require explicit human approval for destructive, outbound, or privileged actions. <br>
Risk: Channel binding mistakes can cause a new agent to take over an existing agent's communication channel. <br>
Mitigation: Manually verify channel bindings before registration, use separate channel credentials for each agent, and keep backups of OpenClaw configuration before changes. <br>
Risk: Workspace or configuration files can expose credentials or private context if copied into generated agent workspaces. <br>
Mitigation: Keep credentials and session transcripts outside workspaces, avoid storing secrets in memory files, and review MEMORY.md usage for private versus shared contexts. <br>
Risk: The included systemd deployment section may be treated as an executable administration plan. <br>
Mitigation: Treat systemd guidance as optional administrator documentation and run privileged deployment steps only after manual review. <br>


## Reference(s): <br>
- [Agent Builder Plus on ClawHub](https://clawhub.ai/YKaiXu/agent-builder-plus) <br>
- [OpenClaw Agent Workspace](references/openclaw-workspace.md) <br>
- [OpenClaw Agent File Templates](references/templates.md) <br>
- [Agent Architecture Patterns](references/architecture.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with workspace-file templates, inline shell commands, configuration snippets, and validation prompts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generates or revises OpenClaw workspace files such as IDENTITY.md, SOUL.md, AGENTS.md, USER.md, HEARTBEAT.md, BOOTSTRAP.md, optional MEMORY.md, daily memory files, and TOOLS.md.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
