## Description: <br>
Queries bank bill reconciliation progress from a specified Feishu Bitable when a user asks about a bank or branch. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[runkecheng](https://clawhub.ai/user/runkecheng) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Finance and operations employees use this skill to look up a bank or branch and summarize bill issuance and reconciliation status. It reads the configured Feishu Bitable and returns a concise reconciliation progress table. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill exposes bank reconciliation amounts and business contact information to the agent during use. <br>
Mitigation: Install it only where the agent is authorized to access the specified Feishu Bitable, and use appropriately scoped Feishu credentials. <br>


## Reference(s): <br>
- [Field schema](references/schema.md) <br>
- [Feishu Bitable data source](https://sqb.feishu.cn/wiki/Jc6Ywg8zki3zqbkdYsBciFDknzg?table=tblEf5Jz9ncE0QDG&view=vewMajMqop) <br>
- [ClawHub skill page](https://clawhub.ai/runkecheng/bank-reconciliation-query) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, API calls, guidance] <br>
**Output Format:** [Markdown table with supporting text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Summarizes bank name, business contact, bill cycle, issuance status, and reconciliation completion by period.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
