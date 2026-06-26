## Description: <br>
合同续租预警与方案生成技能，基于真实Excel台账（美兰中心C+服务.xlsx）提前识别到期合同、分析企业画像并生成续租方案。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[perrykono-debug](https://clawhub.ai/user/perrykono-debug) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Operations and leasing teams use this skill to identify contracts nearing expiration, analyze tenant profile signals, generate renewal plans, and send renewal reminders through WeCom. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads a named tenant workbook that may contain business or customer information. <br>
Mitigation: Install and run it only in an environment authorized to process that workbook. <br>
Risk: WeCom webhook notifications may disclose renewal details to an unintended group if configured incorrectly. <br>
Mitigation: Configure the webhook for the intended internal group only and test notifications before enabling routine use. <br>
Risk: Scheduled checks and workbook writes can affect operational renewal workflows. <br>
Mitigation: Confirm the schedule, approval process, and workbook-write behavior before enabling daily automation. <br>


## Reference(s): <br>
- [Contract Renewal on ClawHub](https://clawhub.ai/perrykono-debug/contract-renewal) <br>
- [Publisher profile: perrykono-debug](https://clawhub.ai/user/perrykono-debug) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, configuration, guidance] <br>
**Output Format:** [Markdown and plain-text renewal alerts, JSON-like renewal data, and Python automation guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May read and update the configured tenant workbook and may send WeCom webhook notifications when configured.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
