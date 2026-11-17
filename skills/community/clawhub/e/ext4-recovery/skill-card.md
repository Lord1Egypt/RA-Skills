## Description:

Ext4 Recovery helps agents guide read-only recovery of deleted ext3/ext4 files and directory trees by inspecting jbd2 journal metadata and extracting data blocks that have not been reused.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yikenan](https://clawhub.ai/user/yikenan)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, system administrators, incident responders, and forensic analysts use this skill when an agent must assess whether deleted ext3/ext4 content can be recovered, select a cautious workflow, and run read-only diagnostic or recovery commands against a correctly identified offline device.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Raw block-device recovery work can cause accidental data loss if the source partition is mounted, written to, or confused with another device.

Mitigation: Use only a correctly identified offline source device, prefer a forensic image or narrowly scoped read-only commands, and write recovered files only to an empty directory on a separate filesystem.

Risk: The chmod/chown workaround can grant broad write-capable access to a disk device.

Mitigation: Do not use the chmod 660/chown device workaround from the artifact; use review-controlled read-only access instead.

Risk: Diagnostics may collect shell history and logs that expose unrelated secrets or sensitive operational details.

Mitigation: Redact shell history and logs before sharing diagnostic output with an agent or another reviewer.

## Reference(s):

- [ext4 / jbd2 on-disk format notes](references/jbd2-ondisk.md)
- [extundelete and ext4magic tool limits](references/tool-limits.md)
- [ClawHub skill release page](https://clawhub.ai/yikenan/skills/ext4-recovery)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Markdown guidance with inline shell commands and code snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include diagnostic interpretations, recovery command sequences, verification steps, and cautions about raw block-device handling.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
