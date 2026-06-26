## Description: <br>
CEO小茂聚合技能包。用于外贸 CEO/业务负责人场景：协调汇报、Google Maps 商务联系人收集、OneABC 模型调用、邮件发送、WhatsApp 消息发送、WhatsApp 会话助理，并支持一键初始化模板文件。适用于想安装后快速搭建一套可配置业务工作流的人。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xingfan0828](https://clawhub.ai/user/xingfan0828) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External business operators and sales teams use this skill to set up a configurable foreign-trade outreach workflow for lead collection, email and WhatsApp dispatch, customer follow-up, and CEO-style progress reporting. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Automated outreach can send messages, attachments, or replies to real contacts. <br>
Mitigation: Use a small approved contact list, review templates and product files, and enable batch sending or auto-reply only after operator approval. <br>
Risk: The skill retains customer, contact, state, notification, and message log data in workspace files. <br>
Mitigation: Run it in a controlled workspace, limit file access, and review or purge generated contact and log files according to business policy. <br>
Risk: External service and agent calls require credentials and can expose business or customer content to the configured services. <br>
Mitigation: Use dedicated revocable credentials and confirm the configured OpenClaw agent permissions before running live workflows. <br>


## Reference(s): <br>
- [CEO小茂 Coordination Method](artifact/references/coordination-method.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/xingfan0828/ceo-xiaomao) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands, configuration examples, and generated workspace files when scripts are executed] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create local template files, CSV logs, and outbound message or API side effects when the bundled scripts are run.] <br>

## Skill Version(s): <br>
1.8.2 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
