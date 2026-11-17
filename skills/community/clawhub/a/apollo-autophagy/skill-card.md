## Description:

Helps agents evaluate cleanup candidates and plan destructive cleanup or context reset actions to free space and recover from damaged context.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nic-yuan](https://clawhub.ai/user/nic-yuan)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators using OpenClaw-style agents use this skill to identify when temporary files, stale logs, trash, oversized memory, or damaged context should be cleaned. It supports explicit cleanup and reset workflows where confirmation, snapshots, and preservation of active work matter.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill is intended for destructive cleanup and context reset, including partially or fully irreversible actions.

Mitigation: Require explicit user confirmation for cleanup actions, double-confirm large context resets, and review the cleanup target list before deletion.

Risk: Ambiguous cleanup, delete, reset, or high-token triggers may lead to overbroad cleanup recommendations.

Mitigation: Treat triggers as prompts for review, not authorization, and preserve core memory, active task state, user preferences, skill documentation, and unrebuildable work.

Risk: The packaged script performs status checks and writes retained cleanup state in the OpenClaw workspace.

Mitigation: Inspect the script and generated state or log locations before installation or execution in shared or sensitive workspaces.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/nic-yuan/skills/apollo-autophagy)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown-style cleanup reports with shell command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include cleanup status details and retained state or log file paths for review.]

## Skill Version(s):

2.0.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
