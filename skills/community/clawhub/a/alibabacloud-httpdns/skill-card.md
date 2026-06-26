## Description: <br>
Helps agents manage Alibaba Cloud HTTPDNS OpenAPIs through the aliyun httpdns CLI, including account information lookup, domain management, cache refresh, and usage statistics. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sdk-team](https://clawhub.ai/user/sdk-team) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and cloud operators use this skill to operate Alibaba Cloud HTTPDNS resources from an agent, including masked account secret lookup, domain add/delete/list workflows, cache refresh, and resolve-count reporting. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can manage live Alibaba Cloud HTTPDNS resources, including mutating domain and cache operations. <br>
Mitigation: Use a least-privilege RAM profile and grant add, delete, or refresh permissions only when those operations are required. <br>
Risk: Account information lookup may expose secret-like fields if raw output is requested. <br>
Mitigation: Return masked account information by default and request raw account secrets only when truly necessary. <br>


## Reference(s): <br>
- [HTTPDNS OpenAPI Reference](references/api-reference.md) <br>
- [Related Commands](references/related-commands.md) <br>
- [Acceptance Criteria](references/acceptance-criteria.md) <br>
- [RAM Permissions](references/ram-policies.md) <br>
- [Verification Method](references/verification-method.md) <br>
- [Alibaba Cloud CLI Installation Guide](references/cli-installation-guide.md) <br>
- [Alibaba Cloud HTTPDNS API product](https://api.aliyun.com/product/Httpdns) <br>
- [Alibaba Cloud HTTPDNS API list](https://help.aliyun.com/document_detail/2868021.html) <br>
- [ListDomains documentation](https://www.alibabacloud.com/help/zh/doc-detail/56800.html) <br>
- [AddDomain documentation](https://www.alibabacloud.com/help/zh/doc-detail/30130.html) <br>
- [GetResolveStatistics documentation](https://api.aliyun.com/document/Httpdns/2016-02-01/GetResolveStatistics) <br>
- [RAM domain authorization](https://help.aliyun.com/document_detail/435245.html) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline bash command examples and masked command-output summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Sensitive account secret fields are masked by default unless raw output is explicitly requested.] <br>

## Skill Version(s): <br>
0.0.1-beta.1 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
