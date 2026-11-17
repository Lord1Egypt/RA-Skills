## Description: <br>
Analytics Dashboard Free guides an agent through setting up a token-protected local web dashboard that aggregates mailbox, browser session, and task status files with periodic refresh. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and small teams use this skill to create a lightweight local dashboard for viewing mailbox, browser session, and task status data from one place. It is intended for dashboard-style reporting and monitoring, not real-time stream processing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The local dashboard may expose mailbox, browser session, or task status data if bound to a remote interface. <br>
Mitigation: Keep the host set to 127.0.0.1 by default; if remote access is required, use a strong token, HTTPS or reverse proxy controls, and network restrictions. <br>
Risk: Dashboard data can include sensitive local work context. <br>
Mitigation: Use the skill only for local dashboard data the user is comfortable viewing in a web UI, and avoid sharing dashboard data directories that contain sensitive content. <br>
Risk: The artifact references a server script but does not include that implementation. <br>
Mitigation: Confirm or create the implementation code before running commands, and review generated code before exposing the dashboard. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/thcjp/skills/analytics-dashboard-free) <br>
- [Publisher profile](https://clawhub.ai/user/thcjp) <br>
- [Skill homepage](https://skillhub.cn) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON configuration examples and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guides creation and operation of a local web dashboard; the release artifact does not include an implementation script.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
