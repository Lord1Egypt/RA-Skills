## Description: <br>
Writes a structured handoff package when a local agent determines cloud Claude Code is needed, while leaving review and execution under user control. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[stephenlthorn](https://clawhub.ai/user/stephenlthorn) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering agents use this skill to package local investigation, escalation rationale, plans, errors, and ready-to-run Claude Code commands when a task should be handed off for cloud assistance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated handoff files can contain task details, project paths, commands, and other sensitive project context. <br>
Mitigation: Review generated handoff files for secrets or sensitive details before sharing them or asking Claude Code to act on them. <br>
Risk: Notifications can expose task summaries, paths, and commands to an environment-selected notification endpoint. <br>
Mitigation: Set OPENCLAW_NOTIFY_ENDPOINT only to a trusted destination, or leave it unset when notification forwarding is not intended. <br>
Risk: Persistent local metadata logs can retain handoff history on the user machine. <br>
Mitigation: Check the local .openclaw-skills data and home-directory handoff log retention against the environment's privacy and cleanup requirements. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [markdown, shell commands, text, guidance] <br>
**Output Format:** [Markdown handoff file with a shell command and text summary] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes handoff files under .openclaw-skills/handoffs and may write local notification status and handoff log files.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
