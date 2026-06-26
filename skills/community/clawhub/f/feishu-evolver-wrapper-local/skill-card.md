## Description: <br>
Feishu-integrated wrapper for the capability-evolver that manages the evolution loop lifecycle, sends Feishu card reports, and provides dashboard visualization. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[muguozi1](https://clawhub.ai/user/muguozi1) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to run and monitor a capability-evolver loop with Feishu reporting, lifecycle controls, dashboard generation, and history export. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can run agents, alter local skill or workspace files, and push repository changes. <br>
Mitigation: Use a dedicated repository or branch, review generated changes before relying on them, and install only when autonomous evolver behavior is intended. <br>
Risk: The skill can maintain recurring watchdog jobs that continue execution after initial setup. <br>
Mitigation: Review lifecycle and watchdog settings before use, and disable or remove the OpenClaw Cron job when continuous operation is not desired. <br>
Risk: The skill can send logs, reports, dashboards, and history to Feishu targets. <br>
Mitigation: Review Feishu environment variables and target identifiers first, and avoid running in workspaces containing secrets or unrelated private data. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/muguozi1/feishu-evolver-wrapper-local) <br>
- [Publisher profile](https://clawhub.ai/user/muguozi1) <br>
- [Feishu Open Platform APIs used by artifact](https://open.feishu.cn/open-apis/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, API calls] <br>
**Output Format:** [Markdown, console text, Feishu card payloads, and lifecycle command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can start recurring watchdog jobs, send reports to Feishu, write local logs/state, and export evolution history when configured.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
