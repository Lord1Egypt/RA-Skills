## Description:

Generates simulated WeChat group chat Excel (.xlsx) files with group_info, active_members, and message_stream sheets compatible with the Pai platform format.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mellooc](https://clawhub.ai/user/mellooc)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, data teams, and test teams use this skill to create synthetic group-chat datasets for AI assistant training, FAQ or knowledge-base testing, multi-role conversation demos, and arbitrary topic samples.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The XLSX dependency is loaded from a shared temporary path, which could execute untrusted code if that path is contaminated.

Mitigation: Use a project-local, pinned xlsx dependency with a lockfile before running the script.

Risk: Generated files can overwrite existing files when default or reused output paths are selected.

Mitigation: Choose explicit, non-existing output paths for generated files.

## Reference(s):

- [Group Schema Reference](artifact/references/group-schema.md)
- [XLSX Format Specification](artifact/references/xlsx-format.md)
- [ClawHub Skill Page](https://clawhub.ai/mellooc/skills/chat-gene)

## Skill Output:

**Output Type(s):** [Text, JSON, Code, Shell commands, Configuration, Files]

**Output Format:** [Markdown guidance with JSON message arrays and generated .json/.xlsx files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated workbook contains group_info, active_members, and message_stream sheets with fixed field and time-format requirements.]

## Skill Version(s):

1.0.0 (source: release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
