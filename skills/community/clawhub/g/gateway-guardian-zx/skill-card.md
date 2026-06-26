## Description: <br>
OpenClaw Gateway Guardian monitors a local OpenClaw Gateway, restarts it after downtime, backs up configuration changes, and can switch to a fallback model. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhangss110](https://clawhub.ai/user/zhangss110) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to keep an OpenClaw Gateway available on a workstation or server by monitoring the gateway port, attempting recovery, preserving configuration backups, and notifying on incidents. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The watchdog can run persistently and may automatically kill any process listening on the configured gateway port. <br>
Mitigation: Review the configured port and recovery behavior before enabling auto-start; disable or fix the force-kill behavior if other services may share the host. <br>
Risk: Configuration backups may contain sensitive OpenClaw settings. <br>
Mitigation: Protect the watchdog backup directory with appropriate local permissions and avoid storing secrets in the OpenClaw configuration when possible. <br>
Risk: Incident notifications can send status and error summaries to a Feishu webhook. <br>
Mitigation: Use only a trusted webhook and review logs for sensitive content before enabling external notifications. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zhangss110/gateway-guardian-zx) <br>
- [Publisher profile](https://clawhub.ai/user/zhangss110) <br>
- [Declared project homepage](https://github.com/zhangss110/openclaw-watchdog) <br>
- [Feishu custom bot documentation](https://open.feishu.cn/document/ukTMukTMukTM/uADOwUjLwgDM14CM4ATN) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local operational guidance for running and configuring the watchdog; no structured API output is declared.] <br>

## Skill Version(s): <br>
1.1.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
