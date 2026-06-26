## Description: <br>
Use when setting up a new claw agent with tapes.dev telemetry and clawtel leaderboard reporting. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bdougie](https://clawhub.ai/user/bdougie) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to set up a claw agent with tapes.dev telemetry, clawtel leaderboard reporting, and the openclaw-in-a-box orchestrator skill. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill runs remote installers, downloads binaries, and fetches another skill without pinned versions. <br>
Mitigation: Review the remote sources before use and prefer pinned versions, checksums, or signatures when installing. <br>
Risk: The setup adds binaries to the system path. <br>
Mitigation: Confirm the install location, back up any existing binaries before overwriting them, and restrict permissions to trusted users. <br>
Risk: tapes stores AI request and response content in a local SQLite database. <br>
Mitigation: Use the skill only where local transcript logging is acceptable and define a retention or deletion plan for the tapes database. <br>
Risk: The downloaded openclaw-in-a-box skill can guide future agent behavior. <br>
Mitigation: Review and scan the downloaded skill before invoking it. <br>
Risk: The claw ingest key is shown once and enables leaderboard reporting. <br>
Mitigation: Store the key only in environment variables or a system keychain, and do not commit it to files. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/bdougie/clawtech-setup) <br>
- [tapes.dev installer](https://download.tapes.dev/install) <br>
- [clawtel releases](https://github.com/bdougie/clawtel/releases/latest) <br>
- [clawtel source](https://github.com/bdougie/clawtel) <br>
- [openclaw-in-a-box skill](https://raw.githubusercontent.com/papercomputeco/openclaw-in-a-box/main/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and configuration steps] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces setup instructions and a handoff summary for invoking openclaw-in-a-box.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
