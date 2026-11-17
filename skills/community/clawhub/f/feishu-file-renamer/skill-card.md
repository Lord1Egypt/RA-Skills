## Description:

Restores Feishu-downloaded hash filenames to original names using message or table mappings, with batch renaming, conflict handling, and rename logs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rfdiosuao](https://clawhub.ai/user/rfdiosuao)

### License/Terms of Use:

MIT-0

## Use Case:

Operations, design, ecommerce, and document-management users use this skill to restore readable filenames for Feishu-downloaded files and batch-organize local downloads from chats, cloud documents, or Bitable mappings.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can rename arbitrary accessible local files based on parsed message mappings.

Mitigation: Use it only in a tightly scoped working directory or sandbox, preview planned renames, and require confirmation before batch operations.

Risk: Untrusted Feishu messages may provide unsafe mappings because message text is loosely parsed.

Mitigation: Avoid untrusted Feishu messages until path validation and explicit command triggers are enforced.

Risk: Rename logs are written to a predictable shared temporary path.

Mitigation: Write logs to a unique private location with restrictive permissions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/rfdiosuao/skills/feishu-file-renamer)
- [ClawHub publisher profile](https://clawhub.ai/user/rfdiosuao)
- [OpenClaw documentation](https://docs.openclaw.ai)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance, files]

**Output Format:** [Markdown responses with command examples, rename statistics, error summaries, and rename log paths.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May rename local files and write a rename log when executed.]

## Skill Version(s):

1.0.0 (source: server release metadata, package.json, README changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
