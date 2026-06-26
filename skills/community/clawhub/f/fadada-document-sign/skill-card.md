## Description: <br>
法大大电子签完整签署技能。覆盖合同发起、已有流程查询、撤回、下载等全生命周期操作。当用户说"发合同"、"查合同"、"查流程"、"查任务"、"撤回合同"、"撤销签署"、"下载合同"、"下载已签合同"等时触发。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fadada-esign](https://clawhub.ai/user/fadada-esign) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users, business teams, and developers use this skill to send contracts through Fadada e-signature workflows, query signing tasks, withdraw eligible tasks, and download completed signed contracts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles contracts, credentials, signer data, and signing or download links. <br>
Mitigation: Use a dedicated least-privilege Fadada app, store credentials in a secret manager or protected environment configuration, and treat signing links and downloaded contracts as sensitive legal documents. <br>
Risk: Security evidence says safeguards are under-scoped for real account use. <br>
Mitigation: Review and preferably patch the skill before installing it in a real account, then rotate any credential matching the README example. <br>
Risk: Verbose API response logging may expose sensitive workflow, signer, or document information. <br>
Mitigation: Disable verbose response logging or redact sensitive fields before operational use. <br>


## Reference(s): <br>
- [FASC API Reference](references/FASC_API_Reference.md) <br>
- [Fadada API credential guide](https://dev.fadada.com/api-guide/YYNLQW2Z2W/9QMQ2MU4FGK3AOXA) <br>
- [Fadada production API base URL](https://api.fadada.com/api/v5) <br>
- [Fadada UAT API base URL](https://uat-api.fadada.com/api/v5) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Configuration, API Calls, Files, Guidance] <br>
**Output Format:** [Markdown instructions, JSON card payloads, shell command examples, API responses, signing links, and downloaded contract files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Handles contracts, signer contact data, credentials, signing URLs, and downloaded legal documents.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
