## Description: <br>
Coordinator Agent monitors OpenClaw agent workspaces, sends change-only fleet briefings to Telegram or optional Discord and Slack channels, prioritizes errors and handoffs, flags trend anomalies, and can retrigger missed cron jobs when enabled. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[waltspence](https://clawhub.ai/user/waltspence) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to monitor multiple OpenClaw agents, receive concise fleet status briefings, identify missed jobs or error-heavy agents, and optionally retrigger missed cron work when that behavior is safe. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The coordinator can read every configured agent workspace, including workspaces that may contain credentials, secrets, or sensitive data. <br>
Mitigation: Restrict the workspace list to only the agents that need monitoring and exclude workspaces containing secrets or private data. <br>
Risk: Briefing content is sent to Telegram and may also be sent to Discord or Slack. <br>
Mitigation: Review the briefing content before enabling external messaging channels and use only approved destinations. <br>
Risk: Using broad copied credentials can give the coordinator more access than it needs. <br>
Mitigation: Use a dedicated, scoped auth profile with read access to selected workspaces and write access only to configured messaging channels. <br>
Risk: Self-healing can retrigger missed cron jobs and cause duplicate execution. <br>
Mitigation: Leave self-healing disabled unless the affected cron jobs are idempotent and safe to run more than once. <br>


## Reference(s): <br>
- [Coordinator Agent ClawHub Release](https://clawhub.ai/waltspence/coordinator-agent) <br>
- [Publisher Profile](https://clawhub.ai/user/waltspence) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces change-only fleet briefings and setup guidance for OpenClaw workspaces and messaging channels.] <br>

## Skill Version(s): <br>
1.2.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
