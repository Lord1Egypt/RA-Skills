## Description: <br>
基于来也科技 ADP 平台的机动车整车出厂合格证智能识别与信息抽取 Skill，可从车辆合格证图片或扫描件中抽取 30+ 个关键字段并输出结构化 JSON。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[laiye-adp](https://clawhub.ai/user/laiye-adp) <br>

### License/Terms of Use: <br>
Commercial License Agreement <br>


## Use Case: <br>
External users and developers use this skill to run Laiye ADP vehicle-certificate extraction from local files, URLs, Base64 content, folders, or async tasks. It is intended for workflows such as vehicle registration, used-car transactions, vehicle asset management, and structured certificate data entry. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a Laiye ADP API key and sends vehicle-certificate files to a cloud document-processing service. <br>
Mitigation: Use only approved ADP accounts and endpoints, keep API keys out of prompts and logs, and confirm that uploaded documents are permitted for cloud processing. <br>
Risk: The installation guidance includes one-line remote installer scripts as alternatives to package or release installation. <br>
Mitigation: Prefer npm installation or verified release binaries, and review any remote installer script before execution. <br>
Risk: The underlying CLI supports broader document-processing and custom-app commands beyond this vehicle-certificate workflow. <br>
Mitigation: Limit agent access to the vehicle-certificate extraction app_id and avoid granting broad filesystem or arbitrary URL access unless needed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/laiye-adp/adp-vehicle-certificate-recognition-and-extract) <br>
- [ADP China portal](https://adp.laiye.com/?utm_source=clawhub) <br>
- [ADP global portal](https://adp-global.laiye.com/?utm_source=clawhub) <br>
- [ADP CLI releases](https://github.com/laiye-ai/adp-cli/releases) <br>
- [ADP CLI user guide](https://laiye-tech.feishu.cn/wiki/Hz3Vw1IQki3YQtk33gLcSdwSndc) <br>
- [ADP Open API guide](https://laiye-tech.feishu.cn/wiki/PO9Jw4cH3iV2ThkMPW2c539pnkc) <br>
- [ADP public cloud manual](https://laiye-tech.feishu.cn/wiki/UDYIwG42pisBbFkJI39ctpeKnWh) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance, json] <br>
**Output Format:** [Markdown guidance with inline shell commands; ADP extraction results are structured JSON.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a Laiye ADP API key, ADP service endpoint, and the account-specific vehicle-certificate app_id.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
