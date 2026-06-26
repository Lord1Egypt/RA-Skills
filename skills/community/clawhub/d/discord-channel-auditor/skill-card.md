## Description: <br>
Audits a Discord server guide channel against actual channels, detects channel drift, and posts an updated guide when changes are found. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[npfaerber](https://clawhub.ai/user/npfaerber) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Discord server owners, moderators, and community operators use this skill to keep a designated guide channel aligned with current Discord channels after channel changes or on a scheduled audit. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can edit and delete messages in a Discord guide channel. <br>
Mitigation: Install it only for designated guide channels where message updates are expected, and ensure the channel content is recoverable or backed up before unattended use. <br>
Risk: Bulk guide refreshes could remove useful existing guidance or publish inaccurate channel descriptions. <br>
Mitigation: Review planned changes before bulk deletion when possible, especially after major channel reorganizations. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/npfaerber/discord-channel-auditor) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance, API Calls] <br>
**Output Format:** [Markdown guide text with Discord message operations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses OpenClaw's Discord message tool; guide output is intended for one or two Discord messages within the 2000-character message limit.] <br>

## Skill Version(s): <br>
1.0.1 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
