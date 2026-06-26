## Description: <br>
Send Bark (day.app) push notifications after Codex completes a task. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[caopulan](https://clawhub.ai/user/caopulan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to send Bark completion notifications with device name, project name, task status, and a short result summary after Codex or Claude finishes a run. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Notifications send device name, project name, task status, and a short task summary to the configured Bark service. <br>
Mitigation: Keep summaries generic, avoid secrets or confidential project details, and install only when that metadata disclosure is acceptable. <br>
Risk: A custom CODEX_BARK_BASE_URL can redirect notification content to a non-default endpoint. <br>
Mitigation: Set CODEX_BARK_BASE_URL only to an endpoint you trust. <br>
Risk: The Bark key is a credential used in the notification URL. <br>
Mitigation: Store CODEX_BARK_KEY in a local environment variable and avoid placing it in shared project files or task summaries. <br>


## Reference(s): <br>
- [Bark API endpoint](https://api.day.app) <br>
- [ClawHub skill page](https://clawhub.ai/caopulan/bark-notification) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and configuration values] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The helper script sends a URL-encoded POST request to the configured Bark endpoint and can print the request details in dry-run mode.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
