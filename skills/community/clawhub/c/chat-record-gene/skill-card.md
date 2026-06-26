## Description: <br>
Generates simulated WeChat-style group chat Excel (.xlsx) files with group_info, active_members, and message_stream sheets compatible with Pai platform group-chat training data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mellooc](https://clawhub.ai/user/mellooc) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and dataset builders use this skill to create synthetic group chat records for AI assistant training data, group-chat FAQ or knowledge-base testing, multi-role conversation demonstrations, and themed chat sample spreadsheets. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill writes local JSON and XLSX files, so an imprecise output path could overwrite workspace files. <br>
Mitigation: Specify explicit output paths in the workspace and check for existing files before running the write step. <br>
Risk: The XLSX writer depends on the xlsx npm package and may use a shared /tmp dependency location. <br>
Mitigation: Install a pinned xlsx version in a project-local dependency directory when stronger dependency control is required. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/mellooc/chat-record-gene) <br>
- [Group schema reference](references/group-schema.md) <br>
- [XLSX format reference](references/xlsx-format.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Files, Guidance] <br>
**Output Format:** [Markdown guidance with JSON inputs, JavaScript scripts, shell commands, and generated .xlsx files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates local JSON and XLSX files using Node.js and the xlsx package.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
