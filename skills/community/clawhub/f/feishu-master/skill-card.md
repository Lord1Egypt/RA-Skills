## Description: <br>
AI Tool Extension for Feishu API - A progressively extensible skill that enables AI tools to leverage Feishu capabilities on demand. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[soraclub](https://clawhub.ai/user/soraclub) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to authenticate with Feishu and perform Feishu Open Platform API tasks, starting with tenant token retrieval and group member lookup. It also guides agents to add new API scripts only when a requested Feishu capability is not already indexed. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill gives an agent broad Feishu workspace API authority through app-level credentials. <br>
Mitigation: Install only when the agent is intended to use Feishu app credentials, and prefer a least-privileged test app when possible. <br>
Risk: Credential files and token caches could expose Feishu access if mishandled. <br>
Mitigation: Keep scripts/env/app.json and token_cache.json out of source control and protect them with restrictive file permissions. <br>
Risk: Newly generated API scripts or future send, update, delete, admin, or bulk operations could perform unintended actions. <br>
Mitigation: Review generated scripts before first execution and require explicit human approval for higher-impact Feishu operations. <br>


## Reference(s): <br>
- [Feishu Open Platform](https://open.feishu.cn/) <br>
- [Feishu API Documentation](https://open.feishu.cn/document/server-docs/) <br>
- [Feishu tenant_access_token API](https://open.feishu.cn/document/server-docs/authentication-management/access-token/tenant_access_token) <br>
- [Feishu group member list API](https://open.feishu.cn/document/server-docs/im-v1/group-group/get_group_member_list) <br>
- [references/feishu_api.md](references/feishu_api.md) <br>
- [references/doc_urls.txt](references/doc_urls.txt) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, code, shell commands, configuration, JSON] <br>
**Output Format:** [Markdown guidance with shell commands and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Feishu app credentials in local configuration; API scripts return standard JSON responses.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
