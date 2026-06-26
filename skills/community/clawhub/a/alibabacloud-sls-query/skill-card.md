## Description: <br>
Alibaba Cloud SLS (Simple Log Service) log query and analysis skill that helps users write, explain, optimize, execute, or troubleshoot SLS index search, SQL analytics, and SPL scan or pipeline statements through the aliyun CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sdk-team](https://clawhub.ai/user/sdk-team) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to construct, validate, execute, and troubleshoot Alibaba Cloud SLS log queries and analytics workflows. It supports index search, SQL analytics, SPL pipelines, time-range handling, result extraction, and RAM permission guidance for SLS projects and logstores. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can give an agent access to Alibaba Cloud SLS logs through the local aliyun CLI. <br>
Mitigation: Use a dedicated RAM user or role limited to log:GetLogStoreLogs and log:GetIndex for only the required project and logstore. <br>
Risk: Credential exposure could occur if access keys are pasted into chat or passed on command lines. <br>
Mitigation: Configure credentials outside the agent session, check status only with aliyun configure list, and never paste, echo, or print AK/SK values. <br>
Risk: The bundled setup guidance includes broader cloud-administration examples outside the SLS query scope. <br>
Mitigation: Ignore unrelated ECS, VPC, RDS, and Function Compute setup examples unless separately reviewed and required for the deployment. <br>
Risk: Broad cross-account or administrator roles could expand the impact of mistaken or unsafe commands. <br>
Mitigation: Avoid broad roles and use least-privilege SLS permissions tied to the needed Alibaba Cloud account, project, and logstore. <br>


## Reference(s): <br>
- [Query Analysis Guide](references/query-analysis.md) <br>
- [SPL Guide](references/spl-guide.md) <br>
- [Functions Guide](references/functions-guide.md) <br>
- [Troubleshooting Guide](references/troubleshooting.md) <br>
- [Related APIs](references/related-apis.md) <br>
- [RAM Policies](references/ram-policies.md) <br>
- [Aliyun CLI Installation Guide](references/cli-installation-guide.md) <br>
- [Regions and Endpoints](references/regions.md) <br>
- [Acceptance Criteria](references/acceptance-criteria.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash commands, query statements, and extracted result summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include copy-paste-ready aliyun CLI commands, SLS query strings, jq extraction snippets, and concise explanations of query mode choices.] <br>

## Skill Version(s): <br>
0.0.1 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
