## Description: <br>
根据公司 URL 或名称，自动完成公司背景调研、联系人挖掘、邮箱验证，并生成本地及 OKKI 档案记录。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cjboy007](https://clawhub.ai/user/cjboy007) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Sales and business-development agents use this skill to research a company from a URL or name, identify relevant contacts, validate email candidates when authorized, and prepare local plus OKKI CRM records. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: SMTP probing of target email servers can be sensitive and may be unauthorized. <br>
Mitigation: Use only for authorized business research, keep SMTP probing disabled unless explicitly approved for the exact targets, and never send DATA during validation. <br>
Risk: The skill can create local files and OKKI CRM records without clear approval steps. <br>
Mitigation: Require a preview and explicit approval before creating local profiles or CRM records. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/cjboy007/farreach-company-intel) <br>
- [Publisher profile](https://clawhub.ai/user/cjboy007) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown client profile, tabular contact lists, and command or code snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include local client profile paths, validated email status, and OKKI CRM record fields.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
