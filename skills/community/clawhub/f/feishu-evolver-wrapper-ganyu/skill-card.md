## Description: <br>
Feishu-integrated wrapper for the capability-evolver that manages the evolution loop lifecycle, sends Feishu card reports, exports history, and provides dashboard visualization. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[foras910521-lab](https://clawhub.ai/user/foras910521-lab) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw operators use this skill to run and supervise a capability-evolver loop with Feishu reporting, lifecycle controls, dashboard summaries, and history export. It is intended for dedicated workspaces where unattended evolution, reporting, and repository synchronization are acceptable. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can run unattended agent and shell-command workflows through lifecycle management and watchdog behavior. <br>
Mitigation: Install it only in a dedicated OpenClaw workspace and review or disable watchdog, cron, and daemon paths before enabling continuous operation. <br>
Risk: The skill can modify repository state and push changes as part of its synchronization flow. <br>
Mitigation: Use a controlled repository or branch, require review before trusting pushed changes, and disable git sync where automatic commits or pushes are not acceptable. <br>
Risk: The skill can export local operational data and reports to Feishu targets. <br>
Mitigation: Configure Feishu targets explicitly, restrict credentials and document tokens, and review exported history or report content for sensitive data. <br>
Risk: The skill includes auto-heal and repair behavior for other skills and workspace state. <br>
Mitigation: Avoid running it against untrusted skill directories and disable auto-heal or self-repair behavior unless workspace-level modification is intended. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/foras910521-lab/feishu-evolver-wrapper-ganyu) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, API calls, Files] <br>
**Output Format:** [Console output, Markdown dashboards and reports, Feishu cards or document updates, lifecycle state files, and git operations.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires an OpenClaw workspace, a capability-evolver installation, and explicit Feishu configuration for remote reporting.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
