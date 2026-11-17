## Description:

Generates simulated WeChat-style group chat records as Excel (.xlsx) files with group_info, active_members, and message_stream sheets for Pai platform training data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mellooc](https://clawhub.ai/user/mellooc)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and AI workflow builders use this skill to create synthetic group-chat Excel datasets for assistant training, FAQ or knowledge-base testing, multi-role conversation demonstrations, and topic-specific chat samples.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unsafe output-file handling could write generated workbooks to an unintended location.

Mitigation: Run only in a contained workspace, pass an explicit safe output filename, inspect paths before execution, and avoid elevated privileges.

Risk: The xlsx dependency is unpinned and loaded from a shared temporary path.

Mitigation: Install a pinned xlsx version through a project lockfile and avoid the shared /tmp dependency path.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mellooc/skills/chat-record-gene)
- [Group schema reference](artifact/references/group-schema.md)
- [XLSX format reference](artifact/references/xlsx-format.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Files]

**Output Format:** [Markdown guidance with JSON snippets, JavaScript scripts, shell commands, and generated .xlsx files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces group definition JSON and Excel workbooks; expected sheets are group_info, active_members, and message_stream.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
