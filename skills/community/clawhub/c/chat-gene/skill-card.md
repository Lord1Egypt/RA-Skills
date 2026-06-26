## Description: <br>
生成模拟微信群聊记录的 Excel (.xlsx) 文件，包含 group_info、active_members 和 message_stream 三个 sheet，用于训练数据、FAQ/知识库测试、多角色对话演示和群聊样本生成。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mellooc](https://clawhub.ai/user/mellooc) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to define synthetic group-chat participants, generate multi-role message streams, and write ClawHub/Pai-compatible group chat Excel workbooks. It is most useful for creating test or training datasets without relying on real chat logs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Local Node.js scripts and the xlsx npm dependency must run on the user's machine. <br>
Mitigation: Install and run the dependency only in an environment where local script execution is acceptable. <br>
Risk: Generated chat logs could be mistaken for real conversations or used to impersonate real people. <br>
Mitigation: Treat outputs as synthetic data and avoid using real identities without permission. <br>
Risk: Default or careless output paths could overwrite important files. <br>
Mitigation: Use explicit input and output paths and review them before running the writer script. <br>


## Reference(s): <br>
- [Group Schema Reference](references/group-schema.md) <br>
- [XLSX Format Specification](references/xlsx-format.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/mellooc/chat-gene) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Files] <br>
**Output Format:** [Markdown guidance with JSON inputs, JavaScript helpers, shell commands, and generated .xlsx files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces synthetic group_info, active_members, and message_stream workbook data; requires local Node.js and the xlsx npm dependency.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
