## Description: <br>
Physical presence display for AI agents. Shows a customizable monogram (A-Z), status state, and current activity on a dedicated terminal/screen. Provides faster feedback than chat - glance at the display to see what the agent is doing. Use when setting up always-on agent visibility. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[voidcooks](https://clawhub.ai/user/voidcooks) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent operators use this skill to configure a dedicated terminal or screen that shows an AI agent's current state and activity at a glance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill creates and updates local config.json and state.json files in the skill directory. <br>
Mitigation: Install and run it only when local status and configuration files in the skill directory are acceptable. <br>
Risk: Status messages are stored locally and displayed on screen, so sensitive task details could be exposed. <br>
Mitigation: Keep status messages non-sensitive and avoid including secrets, credentials, or private data in display text. <br>
Risk: Automatic configuration can inspect local Clawd or Clawdbot configuration files. <br>
Mitigation: Use manual configuration instead of --auto when local configuration inspection is not desired. <br>


## Reference(s): <br>
- [Clawd Presence on ClawHub](https://clawhub.ai/voidcooks/clawd-presence) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Text, Guidance] <br>
**Output Format:** [Markdown with inline bash commands and status values] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local status-display guidance and commands that create or update config.json and state.json in the skill directory.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
