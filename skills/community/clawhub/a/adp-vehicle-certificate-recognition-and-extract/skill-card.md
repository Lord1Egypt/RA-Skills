## Description:

基于来也科技ADP平台的机动车整车出厂合格证智能识别与信息抽取Skill，支持合格证编号、发证日期、制造企业、车辆品牌、车辆型号、VIN、发动机信息、燃料种类、排放标准、外廓尺寸、总质量等30+关键字段抽取，并输出结构化JSON。

This skill is ready for commercial/non-commercial use.

## Publisher:

[laiye-adp](https://clawhub.ai/user/laiye-adp)

### License/Terms of Use:

Commercial License Agreement

## Use Case:

External users, developers, and operations teams use this skill to extract structured fields from Chinese motor vehicle factory certificates for registration, used-car transactions, vehicle asset management, and downstream business-system integration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Vehicle-certificate data is processed through Laiye ADP's cloud service using API-key based access.

Mitigation: Install and use the skill only when cloud processing is acceptable for the data, protect the API key, and confirm the configured ADP region matches the user's data-handling requirements.

Risk: The documented install paths include curl-to-bash, PowerShell invoke-expression, and an unpinned global npm install.

Mitigation: Prefer a pinned, verified release or reviewed local installer before allowing an agent to install or execute the CLI.

Risk: The security scan warns against letting an agent use broader custom-app management commands unless that administration is intended.

Mitigation: Limit agent execution to the vehicle-certificate extraction workflow and require explicit approval before custom application administration commands are used.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/laiye-adp/skills/adp-vehicle-certificate-recognition-and-extract)
- [Laiye ADP China portal](https://adp.laiye.com/?utm_source=clawhub)
- [Laiye ADP global portal](https://adp-global.laiye.com/?utm_source=clawhub)
- [ADP CLI usage guide](https://laiye-tech.feishu.cn/wiki/Hz3Vw1IQki3YQtk33gLcSdwSndc)
- [ADP Open API guide](https://laiye-tech.feishu.cn/wiki/PO9Jw4cH3iV2ThkMPW2c539pnkc)
- [ADP public cloud manual](https://laiye-tech.feishu.cn/wiki/UDYIwG42pisBbFkJI39ctpeKnWh)
- [ADP CLI releases](https://github.com/laiye-ai/adp-cli/releases)
- [ADP CLI issues](https://github.com/laiye-ai/adp-cli/issues)
- [Example extraction result](artifact/examples/extraction-result.json)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with CLI commands and structured JSON extraction results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Extraction results follow a field_key, field_name, field_values JSON structure and the bundled example contains 35 fields.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
