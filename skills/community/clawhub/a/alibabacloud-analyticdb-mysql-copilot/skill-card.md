## Description: <br>
Alibaba Cloud AnalyticDB for MySQL Operations and Diagnosis Assistant that supports cluster information queries, performance monitoring, slow query diagnosis, running SQL analysis, and table-level optimization guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sdk-team](https://clawhub.ai/user/sdk-team) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, database administrators, and cloud operations teams use this skill to inspect Alibaba Cloud AnalyticDB for MySQL clusters and run guided diagnosis for performance, SQL, storage, and table-modeling issues through aliyun CLI commands. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can drive live Alibaba Cloud AnalyticDB for MySQL API calls and send diagnostic context to Alibaba Cloud services. <br>
Mitigation: Use a least-privilege read-only RAM role or short-lived STS credentials, confirm region and cluster parameters before execution, and review generated CLI commands before running them. <br>
Risk: Cluster metadata, connection details, diagnostic prompts, and credential status may be sensitive. <br>
Mitigation: Do not place long-lived access keys in chat, command lines, or logs; treat cluster and diagnostic outputs as sensitive operational data. <br>
Risk: The workflow changes aliyun CLI AI-mode and plugin settings and may install or update CLI plugins. <br>
Mitigation: Review installer and plugin-update commands before use and disable AI-mode when the workflow exits. <br>


## Reference(s): <br>
- [Cluster Information Query](references/cluster-info.md) <br>
- [Cluster Intelligent Diagnosis](references/cluster-diagnosis.md) <br>
- [RAM Policy](references/ram-policies.md) <br>
- [Region List](references/region-list.md) <br>
- [Aliyun CLI Installation Guide](references/cli-installation-guide.md) <br>
- [Alibaba Cloud CLI Credential Configuration](https://help.aliyun.com/zh/cli/configure-credentials) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and diagnostic tables] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include Alibaba Cloud CLI commands, summarized API results, option-card choices, and recommended next steps.] <br>

## Skill Version(s): <br>
0.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
