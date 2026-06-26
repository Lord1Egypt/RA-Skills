## Description: <br>
Browser automation via HTTP API for headless browser control, web automation, form filling, data extraction, interactive element interaction, browser launches, page navigation, screenshots, page structure extraction, and element clicks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dexifried](https://clawhub.ai/user/dexifried) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use PinchTab to control a trusted local browser automation server for browser workflow automation, page navigation, form interaction, page snapshots, screenshots, and data extraction. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses a published fixed bearer token for the local PinchTab server. <br>
Mitigation: Replace the published token with a user-controlled secret before use. <br>
Risk: Browser screenshots can be stored locally or sent through Telegram and may contain private account, personal, or business data. <br>
Mitigation: Avoid saving or sending sensitive screenshots, and review destinations before enabling Telegram delivery. <br>
Risk: Navigation and click actions can affect logged-in sites through the controlled browser. <br>
Mitigation: Run the server only for trusted local users and supervise actions on authenticated pages. <br>


## Reference(s): <br>
- [PinchTab ClawHub Release](https://clawhub.ai/dexifried/dexifried-pinchtab) <br>
- [API Endpoints](references/api-endpoints.md) <br>
- [Common Workflows](references/common-workflows.md) <br>
- [Troubleshooting](references/troubleshooting.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands, JSON API payload examples, and script-based browser automation workflows] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce local screenshot files and optional Telegram photo sends when configured by the user.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
