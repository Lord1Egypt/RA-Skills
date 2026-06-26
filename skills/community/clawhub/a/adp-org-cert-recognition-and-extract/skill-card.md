## Description: <br>
基于来也科技ADP平台的中国组织机构代码证智能识别与信息抽取Skill，支持统一社会信用代码、机构名称、机构类型、法定代表人、地址、有效期、颁发单位和登记号等字段抽取，并输出结构化JSON。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[laiye-adp](https://clawhub.ai/user/laiye-adp) <br>

### License/Terms of Use: <br>
Commercial License Agreement <br>


## Use Case: <br>
Business users, developers, and agents use this skill to invoke Laiye ADP for Chinese organization code certificate recognition and structured field extraction. It is suited for enterprise qualification checks, business information lookup, and certificate data entry workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends potentially sensitive business certificate documents to the Laiye ADP cloud service. <br>
Mitigation: Use it only when organizational policy allows the documents to be processed by Laiye ADP, and avoid submitting confidential certificates outside approved workflows. <br>
Risk: The ADP API key grants account-level access beyond a single extraction request. <br>
Mitigation: Protect the API key, avoid logging it, and limit agent use to the certificate extraction commands needed for the task. <br>
Risk: The documented CLI includes broader app-management capabilities than the certificate-recognition use case requires. <br>
Mitigation: Do not let an agent use custom-app management commands unless that administrative action is explicitly intended. <br>
Risk: Pipe-to-shell installers can increase supply-chain exposure. <br>
Mitigation: Prefer npm installation or verified release artifacts when installing the ADP CLI. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/laiye-adp/adp-org-cert-recognition-and-extract) <br>
- [Laiye ADP China Portal](https://adp.laiye.com/) <br>
- [Laiye ADP Global Portal](https://adp-global.laiye.com/) <br>
- [ADP CLI Releases](https://github.com/laiye-ai/adp-cli/releases) <br>
- [ADP CLI Issues](https://github.com/laiye-ai/adp-cli/issues) <br>
- [ADP CLI User Guide](https://laiye-tech.feishu.cn/wiki/Hz3Vw1IQki3YQtk33gLcSdwSndc) <br>
- [ADP Open API Guide](https://laiye-tech.feishu.cn/wiki/PO9Jw4cH3iV2ThkMPW2c539pnkc) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance, JSON] <br>
**Output Format:** [Markdown guidance with inline shell commands and structured JSON extraction results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a configured Laiye ADP API key and app_id; batch and asynchronous modes can write JSON result files.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
