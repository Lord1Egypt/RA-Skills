## Description: <br>
解析征信报告、银行流水等信贷文件，返回结构化数据和分析报告地址。当用户需要分析征信报告（详版/简版）、企业征信、银行流水，或者提到信贷文件解析、征信查询、流水分析时使用此技能。用户需提供文件的公网 URL 和分析类型。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zoosss](https://clawhub.ai/user/zoosss) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to submit public URLs for Chinese credit reports, enterprise credit reports, or bank statements, then receive structured extraction results and a professional Chinese-language credit analysis. The workflow supports PDF, image, and Excel inputs, with optional PDF passwords for protected files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill processes highly sensitive credit reports, bank statements, identity details, and optional PDF passwords through public file URLs and an external service. <br>
Mitigation: Use only after trusting the publisher and provider; prefer short-lived access-controlled file links, revoke access after processing, and avoid sharing document passwords unless required. <br>
Risk: Generated report links and provider-side processing may have unclear retention, deletion, or access policies. <br>
Mitigation: Confirm ipipei retention, deletion, and report-link access policies before using the skill with real customer or regulated data. <br>
Risk: The artifact contains an embedded enterprise API key used to call the external service. <br>
Mitigation: Review credential ownership and rotation requirements before installation, and replace embedded credentials with controlled secret management where possible. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zoosss/credit-file-analyzer-zhengxin-liushui-ocr) <br>
- [ipipei production API endpoint](https://www.ipipei.com/prod-api) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, guidance] <br>
**Output Format:** [JSON from the analysis script, followed by human-facing Chinese markdown analysis guidance.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes a report link, key parsed credit or bank-statement fields, status and error fields, and optional AI analysis content when returned by the external service.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
