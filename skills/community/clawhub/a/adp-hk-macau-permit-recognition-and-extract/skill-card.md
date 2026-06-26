## Description: <br>
基于来也科技 ADP 平台的港澳通行证智能识别与信息抽取 Skill，帮助代理通过 ADP CLI 从 URL、本地文件、文件夹或 Base64 输入中抽取证件字段并输出结构化 JSON。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[laiye-adp](https://clawhub.ai/user/laiye-adp) <br>

### License/Terms of Use: <br>
Commercial License Agreement <br>


## Use Case: <br>
External users, developers, and operations teams use this skill to configure the Laiye ADP CLI, locate the built-in Hong Kong and Macau permit extraction app, and extract structured permit fields for document review, enrollment, identity checks, or workflow integration. <br>

### Deployment Geography for Use: <br>
Global, with separate China Mainland and overseas ADP service endpoints. <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles sensitive identity-document images and extracted permit fields through Laiye ADP cloud services. <br>
Mitigation: Use it only when authorized to send those documents and fields to Laiye ADP, and confirm privacy, retention, and regional processing requirements before deployment. <br>
Risk: The skill requires an ADP API key. <br>
Mitigation: Protect the API key, avoid pasting it into shared logs or prompts, and prefer environment or secret-manager storage when configuring agents. <br>
Risk: Installer guidance includes pipe-to-shell options. <br>
Mitigation: Prefer npm or verified release artifacts, and review installer scripts before execution when those alternatives are not suitable. <br>
Risk: The documentation includes broader ADP CLI and administrative guidance beyond permit extraction. <br>
Mitigation: Limit agent permissions to the extraction and app-id lookup commands needed for this workflow unless broader ADP administration is intentionally required. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/laiye-adp/adp-hk-macau-permit-recognition-and-extract) <br>
- [Laiye ADP China Mainland Portal](https://adp.laiye.com/?utm_source=clawhub) <br>
- [Laiye ADP Overseas Portal](https://adp-global.laiye.com/?utm_source=clawhub) <br>
- [ADP CLI Releases](https://github.com/laiye-ai/adp-cli/releases) <br>
- [ADP CLI Issues](https://github.com/laiye-ai/adp-cli/issues) <br>
- [ADP CLI 使用指南](https://laiye-tech.feishu.cn/wiki/Hz3Vw1IQki3YQtk33gLcSdwSndc) <br>
- [Open API 使用指南](https://laiye-tech.feishu.cn/wiki/PO9Jw4cH3iV2ThkMPW2c539pnkc) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, json] <br>
**Output Format:** [Markdown guidance with shell commands and JSON result examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guides ADP CLI installation, credential configuration, app-id lookup, synchronous and asynchronous extraction, batch handling, and error interpretation.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
