## Description: <br>
当用户需要分析数据库 AWR（或兼容）报告时使用。调用官方 API 需要有效凭据，详见正文 Setup <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bbsyd2](https://clawhub.ai/user/bbsyd2) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Database administrators, developers, and operations engineers use this skill to submit Oracle AWR or compatible database performance reports to the BIC-QA analysis API. It helps configure credentials, upload report files, choose language and database parameters, and explain asynchronous results delivery by email. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uploads selected AWR or compatible database performance reports to BIC-QA's external API, and those reports may contain secrets, hostnames, schema names, workload details, or customer data. <br>
Mitigation: Review and redact reports before upload, and use the API only when external sharing is approved by the user's organization. <br>
Risk: The API requires a BIC-QA API key for authentication. <br>
Mitigation: Use an approved API key, keep it out of public files and logs, and send it only to api.bic-qa.com in the Authorization header. <br>


## Reference(s): <br>
- [BIC-QA homepage](https://www.bic-qa.com) <br>
- [ClawHub skill page](https://clawhub.ai/bbsyd2/bic-awr) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, API calls] <br>
**Output Format:** [Markdown with shell commands and API request examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes credential setup, multipart upload guidance, JSON request examples, language selection, and error-handling guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: evidence release and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
