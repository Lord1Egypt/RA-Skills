## Description: <br>
基于来也科技ADP平台的中国护照智能识别与信息抽取Skill。支持护照资料页关键字段的精准抽取——姓名、姓名拼音、性别、出生日期、出生地、国籍、护照号码、签发日期、有效期至、签发机关，输出结构化JSON，零配置开箱即用，适用于出入境审核、签证办理、身份核验等场景。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[laiye-adp](https://clawhub.ai/user/laiye-adp) <br>

### License/Terms of Use: <br>
Commercial License Agreement <br>


## Use Case: <br>
External users and developers use this skill to identify Chinese passport document pages and extract key passport fields into structured JSON through Laiye ADP. It supports single-file, URL, Base64, batch, and async extraction workflows for identity verification, visa processing, and document intake scenarios. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends passport data to Laiye ADP's cloud service. <br>
Mitigation: Use it only when authorized to process the passports and when the ADP cloud service is appropriate for the data handling requirements. <br>
Risk: API keys and exported passport extraction results are sensitive. <br>
Mitigation: Store credentials securely, avoid exposing API keys in prompts or logs, and treat exported JSON results as confidential data. <br>
Risk: The artifact includes pipe-to-shell installer examples and broader ADP administration guidance. <br>
Mitigation: Prefer npm or reviewed release downloads, and restrict agent use to passport-specific extract commands and the OOTB passport app ID unless broader ADP actions are explicitly approved. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/laiye-adp/adp-passport-recognition-and-extract) <br>
- [ADP China Portal](https://adp.laiye.com/?utm_source=clawhub) <br>
- [ADP Global Portal](https://adp-global.laiye.com/?utm_source=clawhub) <br>
- [ADP CLI User Guide](https://laiye-tech.feishu.cn/wiki/Hz3Vw1IQki3YQtk33gLcSdwSndc) <br>
- [ADP Open API User Guide](https://laiye-tech.feishu.cn/wiki/PO9Jw4cH3iV2ThkMPW2c539pnkc) <br>
- [ADP Public Cloud Operation Manual](https://laiye-tech.feishu.cn/wiki/UDYIwG42pisBbFkJI39ctpeKnWh) <br>
- [ADP CLI Releases](https://github.com/laiye-ai/adp-cli/releases) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, JSON, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and structured JSON extraction results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Laiye ADP credentials and produces sensitive passport extraction data that should be handled as confidential.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
