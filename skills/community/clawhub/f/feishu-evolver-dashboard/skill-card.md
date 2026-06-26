## Description: <br>
Feishu-integrated wrapper for the capability-evolver that manages the evolution loop lifecycle, sends rich Feishu card reports, and provides dashboard visualization. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[linbo405](https://clawhub.ai/user/linbo405) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to run and monitor a capability-evolver loop with Feishu reporting, dashboard visualization, lifecycle controls, history export, and watchdog-based restart behavior. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can run agents and schedule background work, which may continue automation without direct user interaction. <br>
Mitigation: Install it only in a dedicated evolver workspace and review cron, watchdog, and monitor behavior before enabling it. <br>
Risk: The skill can change repositories and push to origin main. <br>
Mitigation: Review repository remotes and use a disposable repository, protected branch, or disabled git sync where unintended commits or pushes would be harmful. <br>
Risk: The skill can upload local status, dashboard, and history information to Feishu destinations. <br>
Mitigation: Review Feishu targets and credentials before use, and avoid workspaces containing secrets or sensitive local history. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/linbo405/feishu-evolver-dashboard) <br>
- [Feishu message API endpoint used by artifact](https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type=) <br>
- [Feishu document blocks API endpoint used by artifact](https://open.feishu.cn/open-apis/docx/v1/documents/${DOC_TOKEN}/blocks/${DOC_TOKEN}/children) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown, JSON status data, Feishu card payloads, and Node.js command guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces Feishu reporting and local lifecycle status; behavior depends on Feishu credentials, OpenClaw availability, and evolver workspace state.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata; artifact package.json and _meta.json report 1.7.1) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
