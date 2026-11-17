## Description:

Chat Record Generator creates simulated group chat Excel (.xlsx) files with group_info, active_members, and message_stream sheets for Pai-compatible group chat training data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mellooc](https://clawhub.ai/user/mellooc)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, data teams, and test teams use this skill to generate synthetic WeChat-style group chat records for AI assistant training data, FAQ or knowledge base testing, multi-role workflow demonstrations, and themed chat samples.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The helper scripts depend on a local xlsx package path under /tmp, which could load unexpected code if that path is not controlled.

Mitigation: Install and pin the xlsx dependency in a project-owned directory and update the scripts to import that controlled dependency.

Risk: The scripts write caller-specified output files and could overwrite unintended paths.

Mitigation: Run the skill in a restricted workspace, review output paths before execution, and avoid elevated privileges.

Risk: The group definition helper has an output argument handling issue identified by security guidance.

Mitigation: Fix and test the output argument parsing before normal use.

## Reference(s):

- [Group Schema Reference](references/group-schema.md)
- [XLSX Format Specification](references/xlsx-format.md)
- [ClawHub Skill Page](https://clawhub.ai/mellooc/skills/chat-record-generator)
- [Publisher Profile](https://clawhub.ai/user/mellooc)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON message structures, JavaScript configuration, shell commands, and generated .xlsx files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces Pai-compatible Excel workbooks with group_info, active_members, and message_stream sheets.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
