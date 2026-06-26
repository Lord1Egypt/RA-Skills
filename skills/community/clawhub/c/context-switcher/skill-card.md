## Description: <br>
Switches OpenClaw between Work/Focus, Personal, Creative, and Do Not Disturb modes, using natural-language or calendar triggers to adjust notifications, memory context, response style, and restore behavior. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Taha2053](https://clawhub.ai/user/Taha2053) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External OpenClaw users use this skill to switch their assistant into task-specific life modes that mute selected notifications, load local mode profiles, adjust response style, and restore the previous context after a timer or calendar event. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Packaged scripts may write state outside the advertised skill folder. <br>
Mitigation: Review the directory layout and script path logic before installation so state files remain inside ~/.openclaw/skills/context-switcher/. <br>
Risk: Automatic triggers can silently change notification behavior. <br>
Mitigation: Review or disable auto-triggering before use, especially when accidental notification muting would be disruptive. <br>
Risk: Do Not Disturb behavior can retain missed-message information locally. <br>
Mitigation: Review DND logging behavior and clear or disable local logs if retaining missed messages is not acceptable. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Taha2053/context-switcher) <br>
- [Project homepage](https://github.com/Taha2053/context-switcher) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Plain text confirmations and summaries, Markdown mode profiles, JSON state, and shell command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Local-only mode state is stored in current-context.json; DND sessions may retain a local missed-message log until restore.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
