## Description: <br>
基于来也科技ADP平台的中国开户许可证智能识别与信息抽取Skill，支持核准号、编号、基本存款账户、法定代表人、开户银行、银行账号等关键字段抽取，并输出结构化JSON。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[laiye-adp](https://clawhub.ai/user/laiye-adp) <br>

### License/Terms of Use: <br>
Commercial License Agreement <br>


## Use Case: <br>
External developers and business teams use this skill to invoke Laiye ADP for Chinese account-opening permit recognition and extract banking, company, and representative fields into structured results for qualification checks, onboarding, and business-system integration. <br>

### Deployment Geography for Use: <br>
Global, with separate China mainland and overseas ADP service endpoints. <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends account-opening permits and extracted banking or business data to Laiye ADP cloud services. <br>
Mitigation: Use it only for documents the operator is authorized to process, select the approved ADP endpoint, and protect exported JSON results. <br>
Risk: The documentation includes remote shell and PowerShell installer examples. <br>
Mitigation: Prefer npm or verified release installation, and review any remote installer before execution. <br>
Risk: The ADP CLI exposes broad document-processing and custom-app management commands beyond permit extraction. <br>
Mitigation: Restrict agent use to configuration, app lookup, and permit extraction commands unless administrative app management is intentionally required. <br>
Risk: API keys are required to access the ADP service. <br>
Mitigation: Store credentials in approved secret storage or environment variables and avoid exposing them in logs, prompts, or shared outputs. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/laiye-adp/adp-bank-account-permit-recognition-and-extract) <br>
- [ADP China mainland portal](https://adp.laiye.com/?utm_source=clawhub) <br>
- [ADP global portal](https://adp-global.laiye.com/?utm_source=clawhub) <br>
- [ADP CLI releases](https://github.com/laiye-ai/adp-cli/releases) <br>
- [ADP CLI user guide](https://laiye-tech.feishu.cn/wiki/Hz3Vw1IQki3YQtk33gLcSdwSndc) <br>
- [ADP Open API guide](https://laiye-tech.feishu.cn/wiki/PO9Jw4cH3iV2ThkMPW2c539pnkc) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, JSON, Guidance] <br>
**Output Format:** [Markdown guidance with CLI commands and structured JSON extraction results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires an ADP API key, an ADP API base URL, and an account-opening permit app_id; results may be written to stdout or exported to JSON files.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
