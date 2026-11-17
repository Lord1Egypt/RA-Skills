## Description:

Processes bulk prompt batches with alternating execution and reflection loops, checkpointing, Drive-folder handling, and rolling memory.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dodge1218](https://clawhub.ai/user/dodge1218)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and power users use this skill to preserve and process batches of prompts, pasted corpora, file-based prompt lists, or Drive-folder dumps item by item. It produces executed results, checkpoint notes, value rankings, action lists, and persistent memory files for later recall.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Complete pasted, file, or Drive content may be written to persistent workspace files and reused across sessions.

Mitigation: Use the skill only with content approved for local retention, and add retention, deletion, and redaction rules before handling secrets, credentials, regulated data, or confidential documents.

Risk: Imported document text may be processed as actionable instructions without clear confirmation boundaries.

Mitigation: Require explicit user confirmation before executing tasks derived from imported or Drive content, especially when outputs would modify files, run commands, or preserve sensitive material.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/dodge1218/skills/batch-cognition)
- [Drive Mode](references/drive-mode.md)
- [Rolling Decay Memory](references/rolling-decay-memory.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown batch documents with notes, status checklists, summaries, and optional code or command blocks.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes persistent batch, memory, value-stack, parked, discarded, and connection files in the workspace.]

## Skill Version(s):

1.1.0 (source: server release evidence; artifact frontmatter says 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
