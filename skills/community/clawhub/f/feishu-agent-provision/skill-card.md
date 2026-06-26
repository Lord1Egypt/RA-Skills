## Description: <br>
Creates, clones, deletes, diagnoses, and manages Feishu group AI agents with OpenClaw workspace setup, group routing, scheduled reports, and memory files. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lmqiang-711](https://clawhub.ai/user/lmqiang-711) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw operators use this skill to provision Feishu group agents, bind them to group routes, schedule reports, and manage lifecycle tasks such as clone, delete, diagnostics, and status review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can create, clone, delete, and reconfigure local OpenClaw agents, cron tasks, Feishu group routes, and agent workspaces. <br>
Mitigation: Install and run it only where the operator is comfortable granting administrative control over those resources, and review proposed OpenClaw configuration and shell commands before execution. <br>
Risk: High-impact actions may be triggered too broadly or controlled inconsistently. <br>
Mitigation: Use explicit skill-prefixed commands for create, clone, delete, diagnosis, and status workflows, and require the documented confirmation steps before destructive or persistent changes. <br>
Risk: Scheduled reports can deliver messages to Feishu groups and may route to the wrong target if delivery settings are wrong. <br>
Mitigation: Verify the Feishu group ID and cron delivery target before enabling scheduled reports, then send a test message and confirm route logs after configuration changes. <br>
Risk: Long-term backup memory may retain sensitive business details or secrets. <br>
Mitigation: Keep secrets and sensitive business data out of generated SOUL, USER, and backup memory files; store sensitive source data in separately controlled files when needed. <br>
Risk: The delete helper's agent ID validation path has a delete-script import bug noted by security evidence. <br>
Mitigation: Review and fix the validation/import issue before production use, then test deletion with a noncritical agent before relying on the workflow. <br>


## Reference(s): <br>
- [Feishu Agent Provision on ClawHub](https://clawhub.ai/lmqiang-711/feishu-agent-provision) <br>
- [Cron report template](references/cron-template.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON snippets, Python helper script outputs, and OpenClaw shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or modify local OpenClaw agent workspaces, routing configuration, cron tasks, and Feishu delivery settings when the helper scripts are run.] <br>

## Skill Version(s): <br>
3.2.8 (source: server release metadata and target metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
