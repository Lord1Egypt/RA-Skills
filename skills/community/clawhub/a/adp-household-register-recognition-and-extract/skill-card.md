## Description: <br>
基于来也科技ADP平台的中国户口本智能识别与信息抽取Skill，调用 ADP CLI 从户口本图片、扫描件、URL、本地文件或 Base64 输入中抽取户籍字段并输出结构化 JSON。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[laiye-adp](https://clawhub.ai/user/laiye-adp) <br>

### License/Terms of Use: <br>
Commercial License Agreement <br>


## Use Case: <br>
External developers, automation teams, and business users can use this skill to extract structured household-register fields for identity verification, data entry, account-opening review, and similar document-processing workflows. The skill requires an ADP API key and sends documents to the Laiye ADP public cloud service. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill processes household-register documents that contain highly sensitive identity and household data and sends them to a cloud service. <br>
Mitigation: Use it only with authorization, confirm Laiye ADP privacy, retention, billing, and data-residency terms, and avoid uploading documents that are outside the approved workflow. <br>
Risk: The skill requires ADP API credentials. <br>
Mitigation: Protect API keys, prefer environment or encrypted CLI configuration, avoid logging secrets, and rotate credentials if exposure is suspected. <br>
Risk: The ADP CLI includes broader commands than household-register extraction, including custom app management. <br>
Mitigation: Restrict agent access to the documented household-register OOTB extraction, app-id lookup, cache, credit, and query commands unless administrative ADP control is intended. <br>
Risk: Installer examples include remote shell and PowerShell scripts. <br>
Mitigation: Prefer npm installation or reviewed release artifacts, and review any remote installer before execution. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/laiye-adp/adp-household-register-recognition-and-extract) <br>
- [ADP China portal](https://adp.laiye.com/?utm_source=clawhub) <br>
- [ADP Global portal](https://adp-global.laiye.com/?utm_source=clawhub) <br>
- [ADP CLI releases](https://github.com/laiye-ai/adp-cli/releases) <br>
- [ADP CLI user guide](https://laiye-tech.feishu.cn/wiki/Hz3Vw1IQki3YQtk33gLcSdwSndc) <br>
- [ADP Open API guide](https://laiye-tech.feishu.cn/wiki/PO9Jw4cH3iV2ThkMPW2c539pnkc) <br>
- [ADP public cloud operations manual](https://laiye-tech.feishu.cn/wiki/UDYIwG42pisBbFkJI39ctpeKnWh) <br>
- [ADP CLI issues](https://github.com/laiye-ai/adp-cli/issues) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, JSON, Guidance] <br>
**Output Format:** [Markdown guidance with ADP CLI commands and structured JSON extraction output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Single-file extraction may print JSON to stdout; batch and async workflows may write JSON result files, task IDs, summaries, or error JSON.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
