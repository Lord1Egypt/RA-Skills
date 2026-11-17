## Description:

基于来也科技ADP平台的港澳通行证智能识别与信息抽取Skill，支持姓名、姓名拼音、性别、出生日期、证件号码、签发日期、有效期至、签发机关等字段抽取并输出结构化JSON。

This skill is ready for commercial/non-commercial use.

## Publisher:

[laiye-adp](https://clawhub.ai/user/laiye-adp)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to guide Laiye ADP CLI workflows for recognizing Hong Kong and Macau travel permit images or scans and extracting identity-document fields into JSON for review, onboarding, compliance, or document-processing systems.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installation guidance includes unpinned global npm and pipe-to-shell style commands.

Mitigation: Use a pinned, verifiable ADP CLI release and avoid running installers with Administrator or root privileges.

Risk: The skill processes identity documents through Laiye ADP cloud services.

Mitigation: Process documents only with consent, confirm data-handling requirements, and avoid submitting unnecessary identity data.

Risk: API keys and service configuration are required for ADP access.

Mitigation: Keep keys scoped and protected, prefer environment or secure configuration storage, and rotate credentials if exposed.

Risk: The bundled CLI documentation includes broader custom-app management commands beyond permit extraction.

Mitigation: Limit agent use to the extraction, parsing, and query commands needed for this workflow unless broader administration is explicitly intended.

Risk: Commercial authorization may be required for some uses under artifact/license.md.

Mitigation: Confirm applicable license terms with Laiye ADP before commercial deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/laiye-adp/skills/adp-hk-macau-permit-recognition-and-extract)
- [Laiye ADP China portal](https://adp.laiye.com/?utm_source=clawhub)
- [Laiye ADP global portal](https://adp-global.laiye.com/?utm_source=clawhub)
- [ADP CLI releases](https://github.com/laiye-ai/adp-cli/releases)
- [ADP CLI user guide](https://laiye-tech.feishu.cn/wiki/Hz3Vw1IQki3YQtk33gLcSdwSndc)
- [ADP Open API user guide](https://laiye-tech.feishu.cn/wiki/PO9Jw4cH3iV2ThkMPW2c539pnkc)
- [ADP public cloud operation manual](https://laiye-tech.feishu.cn/wiki/UDYIwG42pisBbFkJI39ctpeKnWh)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, JSON, Guidance]

**Output Format:** [Markdown guidance with ADP CLI commands and structured JSON extraction results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports local files, URLs, Base64 input, batch processing, async task queries, and optional exported result files.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
