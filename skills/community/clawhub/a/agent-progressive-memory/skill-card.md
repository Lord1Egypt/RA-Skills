## Description:

Agent Progressive Memory guides agents to load group-chat memory progressively through an index-first workflow and includes hooks for manual and pre-compaction memory flushing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[biociao](https://clawhub.ai/user/biociao)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and teams using OpenClaw use this skill to keep group or project collaboration memory structured, load only the most relevant memory files, and flush meaningful session updates back to local memory.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill installs persistent OpenClaw hooks and can automatically write local session/activity metadata before compaction.

Mitigation: Install only in trusted workspaces, document enablement status, and provide clear disable, uninstall, and retention controls.

Risk: Unsafe file handling may overwrite writable files through symlinks in memory directories.

Mitigation: Use trusted, non-shared memory directories and prefer a version that rejects symlinks and validates canonical paths before writing.

Risk: Memory flush behavior can retain session metadata and deltas beyond the current conversation.

Mitigation: Limit stored metadata, review memory files periodically, and avoid using attacker-writable or shared memory locations.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/biociao/skills/agent-progressive-memory)

## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands, configuration]

**Output Format:** [Markdown instructions with inline shell commands and hook configuration.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes local OpenClaw hook files that can update memory state when installed and enabled.]

## Skill Version(s):

1.2.3 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
