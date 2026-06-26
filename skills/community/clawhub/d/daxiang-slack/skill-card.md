## Description: <br>
Interact with Slack workspaces through browser automation to check unreads, navigate channels and DMs, send messages, search conversations, and extract Slack data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[daxiangnaoyang](https://clawhub.ai/user/daxiangnaoyang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees, external collaborators, and developers use this skill to let an agent operate an authenticated Slack browser session for explicit Slack tasks such as reviewing unread channels, searching conversations, capturing screenshots, and producing Slack analysis reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill gives an agent broad access to an authenticated Slack browser session. <br>
Mitigation: Use it only for explicit, narrow Slack tasks in workspaces where the user is authorized to access the requested content. <br>
Risk: The skill can save Slack messages, screenshots, raw snapshots, and reports that may contain private or sensitive workspace content. <br>
Mitigation: Avoid capturing DMs or private content unless necessary and authorized, redact generated artifacts before sharing, and delete local Slack artifacts after the task is complete. <br>
Risk: The skill can send Slack messages through the authenticated browser session. <br>
Mitigation: Review message text, recipients, and channel context before allowing the agent to send or post content. <br>


## Reference(s): <br>
- [Common Slack Tasks & Patterns](references/slack-tasks.md) <br>
- [Slack Analysis Report Template](templates/slack-report-template.md) <br>
- [Slack Help Center](https://slack.com/help) <br>
- [Slack Web App](https://app.slack.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands, screenshots, JSON snapshots, and optional report templates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce local screenshots, text snapshots, JSON snapshots, and Slack analysis reports.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
