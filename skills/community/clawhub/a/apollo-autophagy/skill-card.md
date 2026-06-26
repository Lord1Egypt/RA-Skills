## Description: <br>
Helps an agent identify and report cleanup candidates for destructive removal of unneeded files, logs, memory data, trash, or damaged context state. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nic-yuan](https://clawhub.ai/user/nic-yuan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill when an OpenClaw workspace or conversation context needs cleanup assessment, reset planning, or explicit destructive cleanup reporting. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill is designed for destructive cleanup and may lead an agent toward deleting files, memory, logs, or context state. <br>
Mitigation: Require a visible dry run, an explicit approval step for each deletion target, and double confirmation for any irreversible context reset. <br>
Risk: Automatic cleanup triggers and broad deletion categories can be ambiguous in real workspaces. <br>
Mitigation: Disable automatic cleanup from token thresholds and require the agent to list exact paths, records, and retained items before proposing deletion. <br>
Risk: Snapshots and cleanup logs may preserve sensitive context or data that the user expected to remove. <br>
Mitigation: Treat snapshots and logs as sensitive, disclose their location and retention period, and remove them according to the stated seven-day policy. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/nic-yuan/apollo-autophagy) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown cleanup report with shell command guidance and generated JSON state] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports cleanup status, risk level, cleanup targets, retained content, snapshot location, and timestamp.] <br>

## Skill Version(s): <br>
2.0.0 (source: SKILL.md frontmatter, server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
