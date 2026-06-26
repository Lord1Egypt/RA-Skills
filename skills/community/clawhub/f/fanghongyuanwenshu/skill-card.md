## Description: <br>
Searches China Judgments Online with a user-provided account, filters court documents by case cause, region, year, document type, and trial procedure, extracts judgment text, and exports results to Excel. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fong12368](https://clawhub.ai/user/fong12368) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Legal practitioners, researchers, and analysts use this skill to collect court-document metadata and full judgment text from China Judgments Online for case research and reference workflows. The skill is intended for users who can supply valid site credentials and understand the access-policy risks of automated browsing. <br>

### Deployment Geography for Use: <br>
Global, subject to China Judgments Online account access, site rules, and applicable local legal requirements. <br>

## Known Risks and Mitigations: <br>
Risk: Automated access to a protected court website may conflict with site rules or trigger account controls. <br>
Mitigation: Use only an account authorized for this site, keep request volume low, prefer test mode, and review site terms before full-mode collection. <br>
Risk: The security evidence flags under-disclosed CAPTCHA automation and decrypted site-response extraction. <br>
Mitigation: Review the script and security guidance before installation; avoid use where anti-bot or access-control circumvention is prohibited. <br>
Risk: Local configuration retains the account identifier and search settings. <br>
Mitigation: Delete artifact/scripts/.wenshu_config.json after use or before sharing the environment, and do not commit generated configuration. <br>
Risk: Exported court documents may contain personal or otherwise sensitive legal information. <br>
Mitigation: Restrict access to generated Excel files and review contents before sharing or reusing them. <br>


## Reference(s): <br>
- [ClawHub skill release](https://clawhub.ai/fong12368/fanghongyuanwenshu) <br>
- [Publisher profile](https://clawhub.ai/user/fong12368) <br>
- [China Judgments Online](https://wenshu.court.gov.cn/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration, Files] <br>
**Output Format:** [Markdown guidance and Python-script execution that writes an .xlsx workbook.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The workbook contains 13 court-document columns, including cleaned judgment text; local .wenshu_config.json stores account identifier and search settings while masking the password.] <br>

## Skill Version(s): <br>
10.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
