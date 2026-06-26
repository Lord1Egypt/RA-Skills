## Description: <br>
Generates simulated WeChat group chat Excel (.xlsx) files with group_info, active_members, and message_stream sheets for training data, FAQ tests, workflow demos, and themed chat samples. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mellooc](https://clawhub.ai/user/mellooc) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, data builders, and AI workflow testers use this skill to define synthetic group chats, coordinate multi-role message generation, and write the result to Pai-compatible Excel workbooks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill writes or overwrites output files at paths provided by the user. <br>
Mitigation: Run it in a controlled workspace and review output paths before execution. <br>
Risk: Generated synthetic chat records may be inaccurate or unsuitable for a downstream training or evaluation task. <br>
Mitigation: Review the generated workbook contents and validate the data format before using it in downstream systems. <br>
Risk: The workflow may install or use the xlsx npm dependency under /tmp. <br>
Mitigation: Install dependencies from trusted package sources and use an isolated environment when generating workbooks. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/mellooc/chat-record-generator) <br>
- [Group schema reference](references/group-schema.md) <br>
- [XLSX format specification](references/xlsx-format.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, code, shell commands, configuration, files] <br>
**Output Format:** [Markdown guidance with JSON, JavaScript, and shell command snippets; generated Excel (.xlsx) files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes group definition JSON and Excel workbook outputs; generated data should be reviewed before downstream use.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
