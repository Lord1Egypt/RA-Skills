## Description: <br>
Alibaba Cloud SLS (Simple Log Service) index configuration manager skill that helps users inspect, create, update, delete, generate, and optimize Logstore index configurations through the aliyun CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sdk-team](https://clawhub.ai/user/sdk-team) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and cloud operations engineers use this skill to manage Alibaba Cloud SLS Logstore index configurations with the aliyun CLI. It supports inspection, complete configuration generation, optimization for query and SQL workloads, and controlled create, update, or delete operations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Update and delete commands can affect production log search behavior. <br>
Mitigation: Use a least-privilege RAM role, start with read-only GetIndex when possible, and require explicit confirmation before delete-index. <br>
Risk: Submitting an incomplete update can replace or remove existing index configuration. <br>
Mitigation: Review the complete JSON body and keep a backup of the current index before any update. <br>


## Reference(s): <br>
- [Manage Index Configuration](references/manage-index-config.md) <br>
- [Generate Index Configuration from Log Samples](references/generate-index-from-logs.md) <br>
- [Optimize Index Configuration](references/optimize-index-config.md) <br>
- [RAM Policies - SLS Index Configuration Manager](references/ram-policies.md) <br>
- [Aliyun CLI Installation & Configuration Guide](references/cli-installation-guide.md) <br>
- [Related APIs - SLS Index Configuration Manager](references/related-apis.md) <br>
- [Acceptance Criteria: sls-index-config-manager](references/acceptance-criteria.md) <br>
- [Alibaba Cloud SLS GetIndex API](https://help.aliyun.com/zh/sls/developer-reference/api-sls-2020-12-30-getindex) <br>
- [Alibaba Cloud SLS CreateIndex API](https://help.aliyun.com/zh/sls/developer-reference/api-sls-2020-12-30-createindex) <br>
- [Alibaba Cloud SLS UpdateIndex API](https://help.aliyun.com/zh/sls/developer-reference/api-sls-2020-12-30-updateindex) <br>
- [Alibaba Cloud SLS DeleteIndex API](https://help.aliyun.com/zh/sls/developer-reference/api-sls-2020-12-30-deleteindex) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, JSON, Markdown] <br>
**Output Format:** [Markdown with fenced JSON and bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs complete index configuration JSON before human-readable summaries; write operations require review of full JSON and explicit confirmation.] <br>

## Skill Version(s): <br>
0.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
