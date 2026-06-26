## Description: <br>
Deterministic, evidence-gated controller templates for OpenClaw that provide HEARTBEAT/ACTIVITIES, sprint template, and poll cron payload guidance without installing services or changing configuration by themselves. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[variable190](https://clawhub.ai/user/variable190) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and operators use this skill to set up a repeatable OpenClaw project-control loop with evidence-gated sprint execution, portfolio queue management, disabled-by-default polling, and optional control-plane logging. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Enabling heartbeat or poll cron can create an autonomous project-control loop that updates controller state. <br>
Mitigation: Keep cron and heartbeat disabled until HEARTBEAT.md and ACTIVITIES.md have been reviewed and a manual dry run succeeds. <br>
Risk: Heartbeat full-refresh reads may include memory or profile files that contain sensitive information. <br>
Mitigation: Remove secrets from memory/profile files before arming heartbeat automation. <br>
Risk: Optional Telegram or cross-context logging can send control-plane messages outside the local workspace. <br>
Mitigation: Enable external logging only for trusted destinations and keep logged messages limited to necessary control-plane status. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/variable190/deterministic-controller) <br>
- [OpenClaw config snippets](docs/openclaw_config_snippets.md) <br>
- [Poll cron payload](docs/poll_cron_payload.txt) <br>
- [Setup prompt](examples/setup_prompt.md) <br>
- [Project-to-sprint prompt](examples/project_to_sprint_prompt.md) <br>
- [HEARTBEAT template](templates/HEARTBEAT.md) <br>
- [ACTIVITIES template](templates/ACTIVITIES.md) <br>
- [Sprint template](templates/SPRINT_TEMPLATE.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown templates, copy/paste prompts, configuration snippets, and cron payload text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Docs-only release; users copy and adapt templates manually before enabling automation.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
