## Description:

解析征信报告、银行流水等信贷文件，返回结构化数据和分析报告地址。

This skill is ready for commercial/non-commercial use.

## Publisher:

[zoosss](https://clawhub.ai/user/zoosss)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to submit public URLs for Chinese credit reports, enterprise credit reports, and bank statement files, then receive structured extraction results and a Chinese credit analysis summary.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles sensitive credit reports and bank statements through a third-party service with under-disclosed data handling.

Mitigation: Use only documents the user is authorized to process, avoid long-lived public file URLs, and require an explicit privacy and consent review before broad use.

Risk: The security evidence reports an embedded enterprise API credential.

Mitigation: Remove and rotate the embedded credential, then require runtime secret injection before release or installation.

Risk: Passing PDF passwords on the command line can expose secrets through shell history or process listings.

Mitigation: Use safer password handling, such as a prompt or secret store, instead of command-line password arguments.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zoosss/skills/credit-file-analyzer-zhengxin-liushui-ocr)
- [ipipei API endpoint used by the skill](https://www.ipipei.com/prod-api)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Guidance]

**Output Format:** [Chinese Markdown guidance with shell commands and JSON parsing results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include an online report address, extracted credit or bank-statement fields, status fields, and a concise Chinese risk analysis.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
