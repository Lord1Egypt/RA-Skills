## Description: <br>
当用户询问数据库或操作系统相关知识、需要基于 BIC-QA 知识库检索专业资料时使用。调用官方 API 需要有效凭据，详见正文 Setup <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bbsyd2](https://clawhub.ai/user/bbsyd2) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to query the BIC-QA knowledge base for database and operating-system answers through the official HTTPS API. It is most useful when the agent has a configured BIC-QA API key and a question that can be mapped to a supported database or OS topic. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a BIC-QA API key and includes a plaintext config-file setup option. <br>
Mitigation: Use a dedicated, rotatable API key, avoid committing it to repositories, and prefer an environment variable or OS-backed secret manager when available. <br>
Risk: The skill depends on an external API for database and operating-system answers. <br>
Mitigation: Stop when credentials are missing or the API fails, and avoid substituting unsupported model knowledge for the BIC-QA result. <br>


## Reference(s): <br>
- [BIC-QA Homepage](https://www.bic-qa.com) <br>
- [ClawHub Skill Listing](https://clawhub.ai/bbsyd2/bic-qa) <br>
- [Publisher Profile](https://clawhub.ai/user/bbsyd2) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, API calls, markdown] <br>
**Output Format:** [Markdown with inline bash and curl examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a user-provided BIC-QA API key; API responses are expected as JSON with an answer field such as result.] <br>

## Skill Version(s): <br>
1.0.2 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
