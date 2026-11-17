## Description:

Checks system health and maintenance status, then automatically detects and repairs common issues.

This skill is ready for commercial/non-commercial use.

## Publisher:

[alfredming-2026](https://clawhub.ai/user/alfredming-2026)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to respond to system maintenance, health-check, and troubleshooting requests. It runs a local maintenance script when appropriate, reviews the output, and summarizes whether issues were repaired or the system is healthy.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad troubleshooting or maintenance requests can cause the agent to run a local repair script that is not included in the artifact.

Mitigation: Use only in controlled environments where /home/admin/.openclaw/workspace/scripts/system-maintenance.sh is trusted, reviewed, and protected from unauthorized modification.

Risk: Automatic repair actions may change system state before the user has reviewed the planned maintenance.

Mitigation: Require explicit confirmation before running repairs and prefer releases that bundle or verify the maintenance script.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown or plain text summary with shell command execution details and log references]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May reference local maintenance logs when reporting health-check or repair results.]

## Skill Version(s):

1.0.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
