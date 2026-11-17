## Description:

基于来也科技ADP平台的中国机动车驾驶证智能识别与信息抽取Skill。支持驾驶证正副页全量字段的精准抽取：驾驶证证号、姓名、性别、国籍、住址、出生日期、初次领证日期、准驾车型、有效期始至、签发机构、档案编号，输出结构化JSON，零配置开箱即用，适用于驾驶员资质核验、网约车/货运司机准入审核等场景。

This skill is ready for commercial/non-commercial use.

## Publisher:

[laiye-adp](https://clawhub.ai/user/laiye-adp)

### License/Terms of Use:

Commercial License Agreement

## Use Case:

External users and developers use this skill to guide ADP CLI setup and extract structured JSON fields from Chinese motor vehicle driving license images, PDFs, URLs, local files, Base64 input, or batches. The primary use cases are driver qualification verification, ride-hailing or freight onboarding checks, and license data entry workflows.

### Deployment Geography for Use:

Global, with China mainland and overseas ADP service endpoints documented separately

## Known Risks and Mitigations:

Risk: Driving license extraction handles personal data such as license numbers, names, birth dates, addresses, and file numbers.

Mitigation: Mask or omit PII in logs, console output, files, user interfaces, and downstream sharing; send only documents the user is authorized to process.

Risk: API keys and service credentials are required for ADP access.

Mitigation: Use least-privilege accounts where available, avoid exposing API keys in chat or logs, and prefer environment or secure local configuration over repeated plaintext entry.

Risk: The artifact includes curl-to-shell and PowerShell iex installer options that execute remote scripts.

Mitigation: Prefer the npm package or versioned release binaries, and review installer scripts before using remote script installation.

Risk: The ADP CLI supports broader custom-app and generic document commands beyond the driving-license workflow.

Mitigation: Use the documented out-of-the-box driving-license app flow, especially app-type 0 discovery and extract commands, unless the user intentionally requests wider ADP CLI capabilities.

## Reference(s):

- [ClawHub Skill Listing](https://clawhub.ai/laiye-adp/skills/adp-driving-license-recognition-and-extract)
- [ADP China Mainland Portal](https://adp.laiye.com/?utm_source=clawhub)
- [ADP Global Portal](https://adp-global.laiye.com/?utm_source=clawhub)
- [ADP CLI User Guide](https://laiye-tech.feishu.cn/wiki/Hz3Vw1IQki3YQtk33gLcSdwSndc)
- [Open API User Guide](https://laiye-tech.feishu.cn/wiki/PO9Jw4cH3iV2ThkMPW2c539pnkc)
- [ADP Public Cloud Operation Manual](https://laiye-tech.feishu.cn/wiki/UDYIwG42pisBbFkJI39ctpeKnWh)
- [ADP CLI Releases](https://github.com/laiye-ai/adp-cli/releases)
- [ADP CLI Issues](https://github.com/laiye-ai/adp-cli/issues)
- [Laiye ADP Product Page](https://laiye.com/product/adp-platform)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, JSON, guidance]

**Output Format:** [Markdown guidance with inline shell commands; extraction results are structured JSON from the ADP CLI.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Covers single-file, batch, URL, Base64, and asynchronous CLI workflows.]

## Skill Version(s):

1.0.0 (source: evidence.release.version and target metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
