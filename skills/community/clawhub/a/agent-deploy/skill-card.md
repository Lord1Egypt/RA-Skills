## Description: <br>
Agent Deploy creates isolated OpenClaw agents with Telegram bot routing, dedicated workspaces, session storage, safe config updates, doctor validation, and rollback. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Joe7921](https://clawhub.ai/user/Joe7921) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to deploy, list, and remove isolated OpenClaw agents that are routed through separate Telegram bot accounts. It is intended for multi-agent OpenClaw setups that need scripted configuration updates with validation and rollback. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Newly deployed Telegram agents can inherit existing OpenClaw auth profiles and API keys. <br>
Mitigation: Use dedicated least-privilege credentials and review the generated auth-profiles.json for each new agent before relying on it. <br>
Risk: Telegram bot tokens and copied credentials may be exposed through prompts, logs, shell history, or generated configuration. <br>
Mitigation: Avoid sharing tokens in chat or logs, keep bot tokens private, and rotate credentials if exposure is suspected. <br>
Risk: Removing an agent does not delete its workspace and may leave copied credentials or local files behind. <br>
Mitigation: After removal, manually clean up the agent workspace and any copied credentials that are no longer needed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Joe7921/agent-deploy) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with bash command invocations and terminal output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Deploy commands create or update OpenClaw agent, binding, Telegram account, workspace, and auth-profile configuration; list and remove commands print terminal status output.] <br>

## Skill Version(s): <br>
2.4.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
