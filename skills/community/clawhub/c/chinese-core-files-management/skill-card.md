## Description:

Helps an OpenClaw agent manage persistent core Markdown files, including identity, agent rules, user context, memory, tools, and bootstrap files, while applying organization and language rules.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kofna3369](https://clawhub.ai/user/kofna3369)

### License/Terms of Use:

MIT-0

## Use Case:

OpenClaw users and agent operators use this skill to inspect, organize, back up, and update core workspace Markdown files without duplicating content across persistent files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can read and rewrite sensitive persistent OpenClaw workspace files.

Mitigation: Require review of the exact files touched and inspect diffs before writes.

Risk: Untrusted text could be copied into memory, tools, agents, identity, or bootstrap files.

Mitigation: Validate content before adding it to core files and reject untrusted instructions or configuration.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kofna3369/skills/chinese-core-files-management)
- [Artifact skill definition](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with file paths, checklists, and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose reads, writes, edits, backups, and validation steps for OpenClaw workspace Markdown files.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata; artifact body states 1.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
