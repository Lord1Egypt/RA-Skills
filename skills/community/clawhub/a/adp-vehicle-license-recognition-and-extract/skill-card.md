## Description:

基于来也科技ADP平台的中国机动车行驶证智能识别与信息抽取Skill，支持行驶证正副页20+关键字段抽取并输出结构化JSON。

This skill is ready for commercial/non-commercial use.

## Publisher:

[laiye-adp](https://clawhub.ai/user/laiye-adp)

### License/Terms of Use:

Commercial License Agreement

## Use Case:

External developers and operations teams use this skill to call Laiye ADP for Chinese vehicle-license recognition in vehicle registration, insurance onboarding, ride-hailing or freight-vehicle admission, and related document-processing workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill documentation includes remote installer commands that pipe downloaded scripts directly into a shell or PowerShell session.

Mitigation: Install from a pinned, verified ADP CLI release or review the installer source before execution.

Risk: Vehicle-license images and extracted JSON can contain sensitive personal or business data.

Mitigation: Confirm that uploading documents to Laiye ADP is permitted for the intended workflow and handle API keys, images, and JSON outputs as sensitive data.

Risk: The underlying CLI can perform broader custom-app and arbitrary-document processing beyond vehicle-license extraction.

Mitigation: Use only the vehicle-license extraction workflow unless the broader document-processing scope is explicitly intended and reviewed.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/laiye-adp/skills/adp-vehicle-license-recognition-and-extract)
- [ADP China Portal](https://adp.laiye.com/?utm_source=clawhub)
- [ADP Global Portal](https://adp-global.laiye.com/?utm_source=clawhub)
- [ADP CLI Releases](https://github.com/laiye-ai/adp-cli/releases)
- [ADP CLI User Guide](https://laiye-tech.feishu.cn/wiki/Hz3Vw1IQki3YQtk33gLcSdwSndc)
- [Open API User Guide](https://laiye-tech.feishu.cn/wiki/PO9Jw4cH3iV2ThkMPW2c539pnkc)
- [Public Cloud Operation Manual](https://laiye-tech.feishu.cn/wiki/UDYIwG42pisBbFkJI39ctpeKnWh)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, JSON, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON extraction output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports image, local file, folder, URL, and Base64 inputs through the ADP CLI; extracted vehicle-license results are returned as structured JSON.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
