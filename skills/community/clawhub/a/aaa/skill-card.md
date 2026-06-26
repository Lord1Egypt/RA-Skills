## Description: <br>
Guides agents through Web of Science literature search, screening, metadata extraction, and Feishu Base writeback using authorized Shenzhen University access and local lark-cli. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[samadhifire](https://clawhub.ai/user/samadhifire) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users with authorized Web of Science, Shenzhen University, and Feishu access use this skill to collect, screen, and export academic literature records into Feishu Base tables. <br>

### Deployment Geography for Use: <br>
Global, subject to the user's authorized Web of Science, Shenzhen University, and Feishu access. <br>

## Known Risks and Mitigations: <br>
Risk: The workflow may access Web of Science, Shenzhen University, or Feishu accounts. <br>
Mitigation: Use only user-authorized sessions, pause for MFA or captcha steps, and do not store passwords, verification codes, or other credentials. <br>
Risk: The workflow may write records to the wrong Feishu Base, subtable, or field layout. <br>
Mitigation: Confirm the Base link, target subtable, field changes, and append-versus-overwrite behavior before writeback. <br>
Risk: Unconfirmed search scope or screening rules may produce irrelevant or misleading literature sets. <br>
Mitigation: Confirm the topic, target count, database scope, and screening rule before searching or exporting records. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/samadhifire/aaa) <br>
- [Publisher Profile](https://clawhub.ai/user/samadhifire) <br>
- [WOS to Feishu Playbook](artifact/references/playbook.md) <br>
- [Shenzhen University Web of Science Access](https://www.lib.szu.edu.cn/er?key=web+of+science) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline commands and structured table-field specifications] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include Web of Science search queries, screening criteria, Feishu Base field schemas, paper metadata, and writeback verification notes.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
