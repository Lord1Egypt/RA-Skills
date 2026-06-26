## Description: <br>
OpenClaw-only sidecar for the original follow-builders skill. Use when the user wants to take over scheduling and delivery without modifying the upstream skill, configure digest delivery, inspect takeover status, or roll back to the original cron. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[amortalsodyssey](https://clawhub.ai/user/amortalsodyssey) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to take over scheduling and delivery for the original follow-builders digest without modifying the upstream skill. It configures OpenClaw or Feishu delivery, manages sidecar state, checks takeover status, and supports rollback. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The sidecar changes scheduled jobs by disabling the original digest cron and creating an hourly replacement. <br>
Mitigation: Confirm takeover intent before setup, inspect status after installation, and use rollback with original cron re-enable only when the user requests restoration. <br>
Risk: The skill can post digest content externally through OpenClaw or Feishu. <br>
Mitigation: Confirm the intended delivery target, account, and Feishu mode before enabling delivery. <br>
Risk: Direct Feishu mode stores app credentials in the sidecar state directory. <br>
Mitigation: Prefer OpenClaw account reuse; when direct credentials are necessary, protect the credentials file with restrictive permissions and rotate exposed secrets. <br>
Risk: The sidecar contacts GitHub, content feeds, avatar services, OpenClaw, and Feishu or Lark endpoints during normal operation. <br>
Mitigation: Keep Feishu domains to official feishu or lark endpoints and avoid untrusted avatar URLs. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/amortalsodyssey/follow-builders-sidecar) <br>
- [Publisher profile](https://clawhub.ai/user/amortalsodyssey) <br>
- [Project homepage](https://github.com/AMortalsOdyssey/follow-builders-sidecar) <br>
- [Original follow-builders project](https://github.com/zarazhangrui/follow-builders) <br>
- [README.md](artifact/README.md) <br>
- [SKILL.md](artifact/SKILL.md) <br>
- [Configuration schema](artifact/config/config-schema.json) <br>
- [Default content sources](artifact/config/default-sources.json) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, Markdown] <br>
**Output Format:** [Markdown guidance with bash commands and configuration options] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May generate or send digest content through OpenClaw or Feishu depending on the configured delivery mode.] <br>

## Skill Version(s): <br>
1.0.9 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
