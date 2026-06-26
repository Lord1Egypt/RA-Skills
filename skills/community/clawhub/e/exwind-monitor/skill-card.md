## Description: <br>
Monitors the EXWIND website every 10 minutes and prepares Feishu notification text when new posts are detected. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lorexxar](https://clawhub.ai/user/lorexxar) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Users who follow EXWIND updates use this skill to run scheduled or manual checks and receive formatted Feishu messages when new blue posts, hotfixes, or news items appear. It helps an agent avoid duplicate alerts by tracking previously seen article IDs in a local state file. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can automatically check EXWIND every 10 minutes and prepare Feishu notifications. <br>
Mitigation: Install it only when scheduled EXWIND monitoring and Feishu alerts are intended. <br>
Risk: Notifications depend on the expected Feishu destination and local browser automation tool. <br>
Mitigation: Verify the Feishu destination and local agent-browser tool before enabling scheduled checks. <br>
Risk: Duplicate suppression uses a local /tmp state file of previously seen article IDs. <br>
Mitigation: Delete /tmp/exwind_state.json when duplicate tracking should be reset. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/lorexxar/exwind-monitor) <br>
- [EXWIND website](https://exwind.net/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Guidance] <br>
**Output Format:** [JSON status output containing Markdown notification text for Feishu when updates are found] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Checks a public website on a schedule, emits no-send JSON when no update is found, and keeps a local /tmp state file of previously seen article IDs.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
