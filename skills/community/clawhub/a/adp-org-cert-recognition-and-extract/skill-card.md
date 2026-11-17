## Description:

基于来也科技ADP平台的中国组织机构代码证智能识别与信息抽取Skill，支持关键字段抽取并输出结构化JSON，适用于企业资质核验和工商信息查询等场景。

This skill is ready for commercial/non-commercial use.

## Publisher:

[laiye-adp](https://clawhub.ai/user/laiye-adp)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and business operations teams use this skill to configure Laiye ADP CLI extraction for Chinese organization code certificates and convert supported image, PDF, URL, local-file, or Base64 inputs into structured business verification data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Certificate images and extracted business data are sent to the Laiye ADP cloud service.

Mitigation: Use the skill only when the user trusts Laiye ADP and is authorized to process the certificate images and extracted business data with that service.

Risk: Installation guidance includes curl-to-shell and PowerShell Invoke-Expression paths.

Mitigation: Prefer the npm package, a pinned reviewed release, or another verifiable install path before allowing an agent to execute installer commands.

Risk: ADP API keys and broader CLI commands could grant access beyond certificate-only extraction.

Mitigation: Protect the ADP API key and restrict agent use to the needed configuration, app lookup, and organization certificate extraction commands unless broader access is intentional.

Risk: Extracted fields can include sensitive values such as legal representative names and addresses.

Mitigation: Redact sensitive fields in logs, console output, stored files, and downstream displays according to the user's data handling requirements.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/laiye-adp/skills/adp-org-cert-recognition-and-extract)
- [Laiye ADP China portal](https://adp.laiye.com/?utm_source=clawhub)
- [Laiye ADP global portal](https://adp-global.laiye.com/?utm_source=clawhub)
- [ADP CLI user guide](https://laiye-tech.feishu.cn/wiki/Hz3Vw1IQki3YQtk33gLcSdwSndc)
- [ADP OpenAPI user guide](https://laiye-tech.feishu.cn/wiki/PO9Jw4cH3iV2ThkMPW2c539pnkc)
- [ADP public cloud operation manual](https://laiye-tech.feishu.cn/wiki/UDYIwG42pisBbFkJI39ctpeKnWh)
- [ADP CLI GitHub releases](https://github.com/laiye-ai/adp-cli/releases)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, JSON, Guidance]

**Output Format:** [Markdown guidance with CLI commands and structured JSON extraction output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports URL, local file, Base64, batch, and asynchronous extraction flows; batch results may be exported as per-file JSON outputs.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
