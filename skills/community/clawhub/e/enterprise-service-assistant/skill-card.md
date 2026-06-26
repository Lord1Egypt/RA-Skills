## Description: <br>
Enterprise Service Assistant helps park operations teams manage customer records, fee collection, contract renewals, work orders, inventory, service matching, visit planning, move-outs, operational reports, and complaints from Excel-based ledgers. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[perrykono-debug](https://clawhub.ai/user/perrykono-debug) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees responsible for park or enterprise-service operations use this agent to read configured Excel or Tencent Docs data, identify operational risks, prepare follow-up messages, and generate daily or periodic service-work summaries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The artifact includes WeCom webhook behavior and a hard-coded webhook URL. <br>
Mitigation: Rotate or remove embedded webhook credentials, require administrator-approved outbound recipients, and keep external messaging disabled until reviewed. <br>
Risk: Broad scheduled automation can send operational reminders and reports without an operator present. <br>
Mitigation: Disable scheduled tasks by default and enable only reviewed schedules with clear owners, recipients, and run windows. <br>
Risk: The artifact contains high-impact legal-proceeding automation and collection workflows. <br>
Mitigation: Require human review and approval before generating, sending, filing, or acting on legal or collection-related outputs. <br>
Risk: The skill processes enterprise ledger data from Excel files and Tencent Docs templates. <br>
Mitigation: Use redacted test data until file paths, retention, cloud document access, and per-feature permissions are approved by an administrator. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/perrykono-debug/enterprise-service-assistant) <br>
- [Installation Guide](artifact/references/安装指引.md) <br>
- [Knowledge Base Configuration](artifact/references/知识库配置.md) <br>
- [Enterprise Service Product Catalog](artifact/references/企业赋能_服务产品清单.md) <br>
- [Customer Management Data Source Mapping](artifact/references/数据源_客户管理表.md) <br>
- [Fee Collection Data Source Mapping](artifact/references/数据源_费用收缴表.md) <br>
- [Value-Added Service Data Source Mapping](artifact/references/数据源_增值服务记录.md) <br>
- [Tencent Docs data-source template](https://docs.qq.com/smartsheet/DTGJwZUJTZU1tc3dk) <br>
- [Tencent Docs service catalog template](https://docs.qq.com/aio/DTHJ2Q0Jick5vV2RH) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and structured text with optional Python examples, configuration snippets, and outbound message templates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce operational reminders, risk labels, reports, message drafts, Excel update guidance, and WeCom notification payloads.] <br>

## Skill Version(s): <br>
2.3.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
