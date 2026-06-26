## Description: <br>
Set up a Bird Buddy smart feeder integration with Home Assistant that configures ha-birdbuddy, a camera entity, automations, a dashboard, and Telegram notifications. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mykclawd](https://clawhub.ai/user/mykclawd) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Home Assistant users and smart-home developers use this skill to connect a Bird Buddy feeder to Home Assistant, add live or cached camera snapshots, import alert automations, and route selected notifications to Telegram. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The setup uses Bird Buddy, Home Assistant, and Telegram credentials that can expose account access if copied into public files, logs, or chats. <br>
Mitigation: Store real tokens in Home Assistant secrets or another protected secret store, and avoid committing or pasting credentials into logs or chat transcripts. <br>
Risk: Bird Buddy and Home Assistant events may be sent to Telegram, which can share household activity or feeder details outside Home Assistant. <br>
Mitigation: Review each automation before enabling it and remove notification fields that should not be sent to Telegram. <br>
Risk: Imported Home Assistant automations and configuration changes can affect existing dashboards, notification routing, and entity behavior. <br>
Mitigation: Review the YAML, Python, and dashboard configuration before applying it, then test the integration in Home Assistant before relying on alerts. <br>


## Reference(s): <br>
- [ha-birdbuddy custom component](https://github.com/jhansche/ha-birdbuddy) <br>
- [Camera entity reference](references/camera.py) <br>
- [Automation templates](references/automations.yaml) <br>
- [Telegram rest_command template](references/rest_commands.yaml) <br>
- [Dashboard configuration](assets/dashboard_config.json) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with YAML, JSON, Python, and shell snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes placeholders for Home Assistant, Bird Buddy, and Telegram values that users should replace with protected secrets.] <br>

## Skill Version(s): <br>
1.0.0 (source: evidence.release.version and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
