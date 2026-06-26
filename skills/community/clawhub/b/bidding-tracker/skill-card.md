## Description: <br>
军政采招投标商机管理专用工具。负责项目登记/标书采购/封标/开标/结果录入/中标统计/胜算评估，不处理合同履约、发票、报销或其他非招投标事务。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhangpengle](https://clawhub.ai/user/zhangpengle) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees and external procurement teams use this skill to track military and government bidding opportunities across registration, document purchase, sealing, opening, result recording, win-rate statistics, and tender-document evaluation. It is scoped to bidding workflows and excludes contract fulfillment, invoicing, reimbursement, and other non-bidding operations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles sensitive military, government, or commercial procurement records. <br>
Mitigation: Install and run it only in a controlled workspace, and keep DB_PATH and ATTACHMENTS_DIR fixed to approved locations. <br>
Risk: The skill has broad local file access when evaluating tender documents. <br>
Mitigation: Do not pass arbitrary local files to the evaluate command; use only trusted PDF, Word, or text tender documents. <br>
Risk: Some query and script paths have weak access boundaries. <br>
Mitigation: Review role and query controls before using the skill with sensitive procurement records. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zhangpengle/bidding-tracker) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/zhangpengle) <br>
- [README](README.md) <br>
- [Skill usage guide](SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [JSON command responses and Markdown guidance with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Successful CLI commands return JSON on stdout; failures return JSON error details and a nonzero exit code.] <br>

## Skill Version(s): <br>
0.1.3 (source: evidence.release.version) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
